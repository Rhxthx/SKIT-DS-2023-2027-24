import React, { useEffect, useState } from 'react'
import { Clock, PawPrint } from 'lucide-react'

const API = import.meta.env.VITE_API_URL || 'https://wildlife-animal-detection-production.up.railway.app'

export default function History() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  // load saved predictions from the backend
  useEffect(() => {
    fetch(`${API}/api/predictions/`)
      .then((res) => res.json())
      .then((data) => setItems(data.predictions || []))
      .catch(() => setError('Could not load history. Please try again later.'))
      .finally(() => setLoading(false))
  }, [])

  return (
    <div style={{ maxWidth: 1000, margin: '0 auto', padding: '48px 24px', color: '#fff' }}>
      <h1 style={{ fontSize: 40, fontWeight: 700, marginBottom: 8, textAlign: 'center' }}>
        Detection History
      </h1>
      <p style={{ opacity: 0.7, marginBottom: 32, textAlign: 'center' }}>
        Your previously analyzed animal images.
      </p>

      {loading ? (
        <p style={{ textAlign: 'center' }}>Loading...</p>
      ) : error ? (
        <p style={{ textAlign: 'center' }}>{error}</p>
      ) : items.length === 0 ? (
        <p style={{ textAlign: 'center' }}>
          No detections yet. Upload an image from the Home page.
        </p>
      ) : (
        <div style={{ display: 'grid', gap: 16 }}>
          {items.map((d) => {
            const isUrl = d.image_path && d.image_path.startsWith('http')
            const top = d.detections && d.detections.length > 0 ? d.detections[0] : null
            const when = d.created_at ? new Date(d.created_at) : null
            return (
              <div
                key={d._id}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 16,
                  padding: 20,
                  borderRadius: 16,
                  background: 'rgba(255,255,255,0.05)',
                  border: '1px solid rgba(255,255,255,0.1)',
                }}
              >
                <div
                  style={{
                    width: 72,
                    height: 72,
                    borderRadius: 14,
                    overflow: 'hidden',
                    background: 'rgba(76,175,110,0.2)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    flexShrink: 0,
                  }}
                >
                {isUrl ? (
                    <a href={d.image_path} target="_blank" rel="noopener noreferrer" title="Open full image" style={{ width: '100%', height: '100%' }}>
                      <img src={d.image_path} alt="Uploaded animal" style={{ width: '100%', height: '100%', objectFit: 'cover', cursor: 'pointer' }} />
                    </a>
                  ) : (
                </div>

                <div style={{ flex: 1 }}>
                  <h3 style={{ margin: 0, fontSize: 20 }}>
                    {top ? top.class_name : 'Detection pending'}
                  </h3>
                  <div style={{ opacity: 0.7, fontSize: 14, marginTop: 4 }}>
                    Animals detected: {d.animal_count ?? 0}
                  </div>
                </div>

                <div style={{ textAlign: 'right' }}>
                  {top && (
                    <div style={{ fontWeight: 700, fontSize: 18, color: '#4caf6e' }}>
                      {Math.round(top.confidence * 100)}%
                    </div>
                  )}
                  {when && (
                    <div style={{ opacity: 0.6, fontSize: 12, display: 'flex', alignItems: 'center', gap: 4, justifyContent: 'flex-end', marginTop: 2 }}>
                      <Clock size={12} /> {when.toLocaleDateString()}, {when.toLocaleTimeString()}
                    </div>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
