import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { UploadCloud, ImagePlus, CheckCircle2, PawPrint, Trees, Ruler, Weight, Palette, Beef, Users2, Lightbulb, Loader2 } from 'lucide-react'
import { detections } from '../data/mockData.js'

const sample = detections[0]

const ACCEPTED_TYPES = ['image/jpeg', 'image/png', 'image/jpg']
const MAX_SIZE_MB = 10

const details = [
  { icon: PawPrint, label: 'Species', value: sample.animal },
  { icon: Users2, label: 'Family', value: sample.family },
  { icon: Beef, label: 'Food Habits', value: sample.diet },
  { icon: Palette, label: 'Color', value: sample.color },
  { icon: Trees, label: 'Habitat', value: sample.habitat },
  { icon: Ruler, label: 'Size', value: sample.size },
  { icon: Weight, label: 'Weight', value: sample.weight },
]

const steps = [
  { title: 'Upload an image', desc: 'Choose a photo containing an animal from your device.' },
  { title: 'Image processing', desc: 'The photo is prepared and cleaned up for analysis.' },
  { title: 'Detection & classification', desc: 'The model reads visual patterns and predicts a species.' },
  { title: 'Explore the result', desc: 'View the species profile and learn more about it.' },
]

export default function Home() {
  const [fileName, setFileName] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [showResult, setShowResult] = useState(true)
  const [isDragging, setIsDragging] = useState(false)
  const [uploadError, setUploadError] = useState('')
  const navigate = useNavigate()

  // shared by click-to-upload and drag-and-drop
  const processFile = async (file) => {
    if (!file || isAnalyzing) return

    // validate before doing anything else
    if (!ACCEPTED_TYPES.includes(file.type)) {
      setUploadError('Please upload a JPG, JPEG or PNG image.')
      return
    }
    if (file.size > MAX_SIZE_MB * 1024 * 1024) {
      setUploadError(`Image is too large. Maximum size is ${MAX_SIZE_MB}MB.`)
      return
    }

    setUploadError('')
    if (previewUrl) URL.revokeObjectURL(previewUrl)
    setPreviewUrl(URL.createObjectURL(file))
    setFileName(file.name)
    setShowResult(false)
    setIsAnalyzing(true)

    // minimum time the loader stays visible, so it doesn't just flash
    const minDelay = new Promise((resolve) => setTimeout(resolve, 2000))

    // send the image to the backend, which saves the prediction in the database
    const upload = (async () => {
      try {
        const API = import.meta.env.VITE_API_URL || 'https://wildlife-animal-detection-production.up.railway.app'
        const formData = new FormData()
        formData.append('image', file)
        await fetch(`${API}/api/predictions/`, { method: 'POST', body: formData })
      } catch (err) {
        console.error('upload failed', err)
      }
    })()

    await Promise.all([upload, minDelay])

    setIsAnalyzing(false)
    setShowResult(true)
  }

  const handleFile = (e) => {
    const file = e.target.files?.[0]
    // lets the user pick the same image again later
    e.target.value = ''
    processFile(file)
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e) => {
    // ignore leave events fired by child elements
    if (e.currentTarget.contains(e.relatedTarget)) return
    setIsDragging(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)
    processFile(e.dataTransfer.files?.[0])
  }

  return (
    <>
      <section className="hero">
        <div className="hero-text">
          <h1>Wildlife Image Recognition</h1>
          <p>
            Upload an image, and let AI identify the animal, along with its key details
            and interesting facts.
          </p>
        </div>

        <div className="hero-panels">
          <div
            className={'upload-card' + (isDragging ? ' upload-card-dragging' : '')}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            <label className="upload-drop">
              <input type="file" accept="image/jpeg,image/png,image/jpg" onChange={handleFile} hidden />
              <UploadCloud size={40} strokeWidth={1.6} />
              <p className="upload-title">{isDragging ? 'Drop your image here' : 'Upload an Image'}</p>
              <p className="upload-sub">Drag &amp; drop an image here or click to browse</p>
              <p className="upload-formats">(JPG, PNG, JPEG, max {MAX_SIZE_MB}MB)</p>
              {fileName && <p className="upload-filename">Selected: {fileName}</p>}
            </label>
            {uploadError && <p className="form-error upload-error">{uploadError}</p>}
            <div className="upload-divider"><span>OR</span></div>
            <label className="btn btn-primary upload-btn">
              <input type="file" accept="image/jpeg,image/png,image/jpg" onChange={handleFile} hidden />
              <ImagePlus size={18} /> Choose Image
            </label>
          </div>

          {isAnalyzing ? (
            <div className="result-card skeleton-card">
              <div className="analyzing-photo">
                {previewUrl && <img src={previewUrl} alt="Uploaded preview" />}
                <div className="analyzing-overlay">
                  <Loader2 className="spin" size={38} />
                  <p>Analyzing your image…</p>
                </div>
              </div>
              <div className="analyzing-bar"><div className="analyzing-bar-fill" /></div>
              <div className="skeleton skeleton-line skeleton-line-lg" />
              <div className="skeleton skeleton-line skeleton-line-sm" />
              <div className="skeleton skeleton-line" />
              <div className="skeleton skeleton-line" />
              <div className="skeleton skeleton-line" />
            </div>
          ) : showResult ? (
          <div className="result-card">
            <div className="result-photo">
              <span className="result-emoji">{sample.thumbnailEmoji}</span>
            </div>
            <div className="result-summary">
              <span className="badge badge-success"><CheckCircle2 size={14} /> Detected</span>
              <h3>{sample.animal}</h3>
              <p className="scientific-name">{sample.scientificName}</p>
              <div className="confidence">
                <div className="confidence-row">
                  <span>Confidence Score</span>
                  <span className="confidence-value">{sample.confidence}%</span>
                </div>
                <div className="confidence-track">
                  <div className="confidence-fill" style={{ width: `${sample.confidence}%` }} />
                </div>
              </div>
            </div>

            <div className="details-block">
              <p className="details-heading"><PawPrint size={16} /> Animal Details</p>
              <ul className="details-list">
                {details.map(({ icon: Icon, label, value }) => (
                  <li key={label}>
                    <span className="details-icon"><Icon size={15} /></span>
                    <span className="details-label">{label}</span>
                    <span className="details-value">{value}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="fun-fact">
              <span className="fun-fact-icon"><Lightbulb size={18} /></span>
              <div>
                <p className="fun-fact-heading">Fun Fact</p>
                <p>{sample.funFact}</p>
              </div>
            </div>

            <button className="btn btn-secondary result-cta" onClick={() => navigate(`/results/${sample.id}`)}>
              View full result
            </button>
          </div>
          ) : null}
        </div>
      </section>

      <section className="how-it-works">
        <h2>Upload → Analyze → Detect → Display Result</h2>
        <div className="steps-grid">
          {steps.map((s, i) => (
            <div className="step-card" key={s.title}>
              <span className="step-number">{i + 1}</span>
              <h3>{s.title}</h3>
              <p>{s.desc}</p>
            </div>
          ))}
        </div>
      </section>
    </>
  )
}