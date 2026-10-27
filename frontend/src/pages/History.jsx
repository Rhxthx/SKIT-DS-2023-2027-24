import React from 'react'
import { Clock, Trees } from 'lucide-react'
import { detections } from '../data/mockData.js'

export default function History() {
  return (
    <div style={{ maxWidth: 1000, margin: '0 auto', padding: '48px 24px', color: '#fff' }}>
      <h1 style={{ fontSize: 40, fontWeight: 700, marginBottom: 8, textAlign: 'center' }}>
        Detection History
      </h1>
      <p style={{ opacity: 0.7, marginBottom: 32, textAlign: 'center' }}>
        Your previously analyzed animal images.
      </p>

      {!detections || detections.length === 0 ? (
        <p style={{ textAlign: 'center' }}>
          No detections yet. Upload an image from the Home page.
        </p>
      ) : (
        <div style={{ display: 'grid', gap: 16 }}>
          {detections.map((d) => (
            <div
              key={d.id}
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
                  width: 56,
                  height: 56,
                  borderRadius: 14,
                  background: 'rgba(76,175,110,0.2)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: 30,
                }}
              >
                {d.thumbnailEmoji}
              </div>

              <div style={{ flex: 1 }}>
                <h3 style={{ margin: 0, fontSize: 20 }}>{d.animal}</h3>
                <i style={{ opacity: 0.7 }}>{d.scientificName}</i>
                <div style={{ opacity: 0.6, fontSize: 13, marginTop: 4, display: 'flex', alignItems: 'center', gap: 4 }}>
                  <Trees size={13} /> {d.habitat}
                </div>
              </div>

              <div style={{ textAlign: 'right' }}>
                <div style={{ fontWeight: 700, fontSize: 18, color: '#4caf6e' }}>
                  {d.confidence}%
                </div>
                <div style={{ fontSize: 12, opacity: 0.8, marginTop: 2 }}>
                  {d.conservationStatus}
                </div>
                <div style={{ opacity: 0.6, fontSize: 12, display: 'flex', alignItems: 'center', gap: 4, justifyContent: 'flex-end', marginTop: 2 }}>
                  <Clock size={12} /> {d.date}, {d.time}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}