import React from 'react';

/**
 * ScenarioCards — lets the user pick a financial decision to simulate.
 * Props: profile, onSimulate(decisionParams, scenarioMeta), loading
 */

const SCENARIOS = [
  {
    id: 'loan',
    emoji: '🏦',
    title: 'Personal Loan',
    subtitle: 'See the true cost of borrowing',
    color: '#9f1239',
    gradientBg: 'rgba(159,18,57,0.06)',
    borderColor: 'rgba(159,18,57,0.25)',
    defaultDecision: {
      type: 'LOAN',
      amount: 500000,
      interest_rate: 12,
      tenure_months: 36,
    },
    fields: [
      { key: 'amount', label: 'Loan Amount (₹)', placeholder: '500000', min: 10000 },
      { key: 'interest_rate', label: 'Annual Interest Rate (%)', placeholder: '12', min: 1, max: 36 },
      { key: 'tenure_months', label: 'Tenure (months)', placeholder: '36', min: 3, max: 360 },
    ],
  },
  {
    id: 'sip',
    emoji: '📈',
    title: 'Start a SIP',
    subtitle: 'Model a new monthly investment',
    color: '#065f46',
    gradientBg: 'rgba(6,95,70,0.06)',
    borderColor: 'rgba(6,95,70,0.25)',
    defaultDecision: {
      type: 'SIP',
      monthly_sip: 10000,
      interest_rate: 12,
    },
    fields: [
      { key: 'monthly_sip', label: 'Monthly SIP Amount (₹)', placeholder: '10000', min: 500 },
      { key: 'interest_rate', label: 'Expected Return (%)', placeholder: '12', min: 1, max: 30 },
    ],
  },
  {
    id: 'lumpsum',
    emoji: '💰',
    title: 'Lump Sum Investment',
    subtitle: 'Invest a large amount at once',
    color: '#1e3a8a',
    gradientBg: 'rgba(30,58,138,0.06)',
    borderColor: 'rgba(30,58,138,0.25)',
    defaultDecision: {
      type: 'LUMPSUM',
      amount: 200000,
      interest_rate: 12,
    },
    fields: [
      { key: 'amount', label: 'Lump Sum Amount (₹)', placeholder: '200000', min: 10000 },
      { key: 'interest_rate', label: 'Expected Return (%)', placeholder: '12', min: 1, max: 30 },
    ],
  },
  {
    id: 'delay',
    emoji: '⏳',
    title: 'Cost of Delay',
    subtitle: 'See how waiting hurts your wealth',
    color: '#92400e',
    gradientBg: 'rgba(146,64,14,0.06)',
    borderColor: 'rgba(146,64,14,0.25)',
    defaultDecision: {
      type: 'DELAY',
      delay_years: 2,
    },
    fields: [
      { key: 'delay_years', label: 'Delay (years)', placeholder: '2', min: 1, max: 10 },
    ],
  },
];

export default function ScenarioCards({ profile, onSimulate, loading }) {
  const [selected, setSelected] = React.useState(null);
  const [formValues, setFormValues] = React.useState({});

  const handleSelect = (sc) => {
    setSelected(sc.id);
    setFormValues({ ...sc.defaultDecision });
  };

  const handleChange = (key, val) => {
    setFormValues(prev => ({ ...prev, [key]: val === '' ? '' : Number(val) }));
  };

  const handleRun = () => {
    const sc = SCENARIOS.find(s => s.id === selected);
    if (!sc) return;
    const decision = { ...formValues };
    onSimulate(decision, { title: sc.title, emoji: sc.emoji });
  };

  const activeScenario = SCENARIOS.find(s => s.id === selected);

  return (
    <div>
      <div style={{ marginBottom: 20 }}>
        <div className="heading-md" style={{ marginBottom: 6 }}>Choose a Financial Decision</div>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
          Select a scenario and customise the parameters to run a 500-path Monte Carlo simulation.
        </p>
      </div>

      {/* Scenario picker grid */}
      <div className="grid-2" style={{ marginBottom: 28 }}>
        {SCENARIOS.map(sc => (
          <div
            key={sc.id}
            className={`scenario-card${selected === sc.id ? ' selected' : ''}`}
            onClick={() => handleSelect(sc)}
            style={{
              borderColor: selected === sc.id ? sc.color : 'var(--border)',
              background: selected === sc.id ? sc.gradientBg : 'var(--bg-card)',
            }}
            role="button"
            tabIndex={0}
            onKeyDown={e => e.key === 'Enter' && handleSelect(sc)}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 8 }}>
              <div style={{
                width: 44, height: 44, borderRadius: 12,
                background: sc.gradientBg,
                border: `1px solid ${sc.borderColor}`,
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontSize: 20,
              }}>
                {sc.emoji}
              </div>
              <div>
                <div style={{ fontWeight: 700, fontSize: '1rem', color: 'var(--text-primary)', fontFamily: 'Times New Roman, Times, serif' }}>
                  {sc.title}
                </div>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{sc.subtitle}</div>
              </div>
            </div>
            {selected === sc.id && (
              <div style={{ width: 24, height: 24, borderRadius: '50%', background: sc.color, display: 'flex', alignItems: 'center', justifyContent: 'center', marginLeft: 'auto', color: '#fff', fontSize: 13, fontWeight: 800 }}>
                ✓
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Parameter form */}
      {activeScenario && (
        <div
          className="card animate-fadeIn"
          style={{ borderColor: activeScenario.borderColor, marginBottom: 20 }}
        >
          <div className="heading-md" style={{ marginBottom: 4 }}>
            {activeScenario.emoji} {activeScenario.title} — Parameters
          </div>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginBottom: 20 }}>
            Adjust parameters below. We'll run 500 independent futures for each scenario.
          </p>

          <div className="grid-2" style={{ gap: 16 }}>
            {activeScenario.fields.map(f => (
              <div className="input-group" key={f.key}>
                <label className="input-label">{f.label}</label>
                <input
                  id={`sim-${f.key}`}
                  type="number"
                  className="input-field"
                  placeholder={f.placeholder}
                  value={formValues[f.key] ?? ''}
                  min={f.min}
                  max={f.max}
                  onChange={e => handleChange(f.key, e.target.value)}
                />
              </div>
            ))}
          </div>

          {/* Profile summary */}
          {profile && (
            <div style={{
              marginTop: 20,
              padding: '12px 16px',
              background: 'var(--bg-secondary)',
              borderRadius: 10,
              fontSize: '0.82rem',
              display: 'flex',
              gap: 20,
              flexWrap: 'wrap',
              color: 'var(--text-secondary)',
            }}>
              <span>👤 Age {profile.age}</span>
              <span>💰 ₹{(profile.monthly_income / 1000).toFixed(0)}K/mo</span>
              <span>🎯 Goal ₹{(profile.goal_amount / 100000).toFixed(0)}L by {profile.goal_age}</span>
            </div>
          )}

          <div style={{ marginTop: 20 }}>
            <button
              id="run-simulation-btn"
              className="btn btn-primary"
              onClick={handleRun}
              disabled={loading}
            >
              {loading ? '⏳ Running…' : `🚀 Run ${activeScenario.title} Simulation →`}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}