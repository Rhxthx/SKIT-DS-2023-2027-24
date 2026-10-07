<<<<<<< Updated upstream
import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { UploadCloud, ImagePlus, CheckCircle2, PawPrint, Trees, Ruler, Weight, Palette, Beef, Users2, Lightbulb } from 'lucide-react'
import { detections } from '../data/mockData.js'

const sample = detections[0]

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
  const navigate = useNavigate()

  const handleFile = (e) => {
    const file = e.target.files?.[0]
    if (file) setFileName(file.name)
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
          <div className="upload-card">
            <label className="upload-drop">
              <input type="file" accept="image/jpeg,image/png,image/jpg" onChange={handleFile} hidden />
              <UploadCloud size={40} strokeWidth={1.6} />
              <p className="upload-title">Upload an Image</p>
              <p className="upload-sub">Drag &amp; drop an image here or click to browse</p>
              <p className="upload-formats">(JPG, PNG, JPEG)</p>
              {fileName && <p className="upload-filename">Selected: {fileName}</p>}
            </label>
            <div className="upload-divider"><span>OR</span></div>
            <label className="btn btn-primary upload-btn">
              <input type="file" accept="image/jpeg,image/png,image/jpg" onChange={handleFile} hidden />
              <ImagePlus size={18} /> Choose Image
            </label>
          </div>

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
=======
>>>>>>> Stashed changes
