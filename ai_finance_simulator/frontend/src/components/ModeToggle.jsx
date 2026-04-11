import React from 'react';

/**
 * ModeToggle — switches between Forward and Reverse simulation modes.
 * Props: mode ('forward'|'reverse'), onChange(newMode)
 *
 * NOTE: App.jsx calls this as <ModeToggle mode={mode} onChange={...} />
 */
export default function ModeToggle({ mode, onChange }) {
  const tabs = [
    { value: 'forward', label: '⚡ Forward — Simulate a Decision' },
    { value: 'reverse', label: '🎯 Reverse — Reach a Goal' },
  ];

  return (
    <div className="tabs">
      {tabs.map(t => (
        <button
          key={t.value}
          id={`mode-${t.value}-btn`}
          className={`tab${mode === t.value ? ' active' : ''}`}
          onClick={() => onChange(t.value)}
        >
          {t.label}
        </button>
      ))}
    </div>
  );
}