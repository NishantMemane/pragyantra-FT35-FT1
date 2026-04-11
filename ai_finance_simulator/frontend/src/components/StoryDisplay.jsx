import React from 'react';

/**
 * StoryDisplay — shows the AI-generated narrative.
 * Props: story (string), mode ('forward'|'reverse'), loading (bool)
 */
export default function StoryDisplay({ story, mode, loading }) {
  if (loading) {
    return (
      <div className="card" style={{ marginTop: 24, padding: '28px 32px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 16 }}>
          <div className="spinner" style={{ width: 20, height: 20, borderWidth: 2 }} />
          <span style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
            Generating your personal AI analysis…
          </span>
        </div>
        {[100, 85, 70].map((w, i) => (
          <div key={i} style={{
            height: 14, borderRadius: 7,
            background: 'var(--bg-secondary)',
            width: `${w}%`,
            marginBottom: 10,
            animation: 'fadeIn 0.4s ease',
          }} />
        ))}
      </div>
    );
  }

  if (!story) return null;

  const icon  = mode === 'reverse' ? '🔁' : '🔮';
  const title = mode === 'reverse'
    ? 'What This Means For Your Goal'
    : 'What This Decision Means For You';

  return (
    <div
      className="card animate-fadeIn"
      style={{
        marginTop: 28,
        borderLeft: `4px solid var(--accent-blue)`,
        padding: '28px 32px',
        background: 'rgba(30,58,138,0.04)',
        borderRadius: 'var(--radius)',
      }}
    >
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: 10,
        marginBottom: 14,
      }}>
        <span style={{ fontSize: 22 }}>{icon}</span>
        <div className="heading-md" style={{ color: 'var(--accent-blue)' }}>{title}</div>
        <span className="badge badge-blue" style={{ marginLeft: 'auto' }}>AI Analysis</span>
      </div>
      <p style={{
        fontFamily: 'Times New Roman, Times, serif',
        fontSize: '1.05rem',
        lineHeight: 1.85,
        color: 'var(--text-secondary)',
        fontStyle: 'italic',
      }}>
        {story}
      </p>
    </div>
  );
}