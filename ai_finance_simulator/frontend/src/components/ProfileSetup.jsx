import React from 'react';

const formatINR = (n) => {
  if (!n && n !== 0) return '—';
  if (n >= 10000000) return `₹${(n / 10000000).toFixed(2)}Cr`;
  if (n >= 100000)   return `₹${(n / 100000).toFixed(1)}L`;
  if (n >= 1000)     return `₹${(n / 1000).toFixed(1)}K`;
  return `₹${n.toLocaleString('en-IN')}`;
};

export default function ProfileSetup({ onComplete }) {
  const [form, setForm] = React.useState({
    age: '',
    monthly_income: '',
    monthly_expenses: '',
    existing_savings: '',
    goal_amount: '',
    goal_age: '',
  });
  const [errors, setErrors] = React.useState({});
  const [step, setStep] = React.useState(0);

  const fields = [
    {
      key: 'age',
      label: 'Your Current Age',
      placeholder: 'e.g. 28',
      icon: '🎂',
      hint: 'How old are you today?',
      min: 18, max: 70,
    },
    {
      key: 'monthly_income',
      label: 'Monthly Income (₹)',
      placeholder: 'e.g. 80000',
      icon: '💰',
      hint: 'Your total take-home monthly income',
      min: 1000,
    },
    {
      key: 'monthly_expenses',
      label: 'Monthly Expenses (₹)',
      placeholder: 'Leave blank for 60% of income',
      icon: '🛒',
      hint: 'Optional — defaults to 60% of income',
      optional: true,
    },
    {
      key: 'existing_savings',
      label: 'Existing Savings / Investments (₹)',
      placeholder: 'e.g. 200000',
      icon: '🏦',
      hint: 'Total corpus you already have saved',
      optional: true,
    },
    {
      key: 'goal_amount',
      label: 'Financial Goal Amount (₹)',
      placeholder: 'e.g. 5000000',
      icon: '🎯',
      hint: 'How much do you want to accumulate?',
      min: 10000,
    },
    {
      key: 'goal_age',
      label: 'Goal Target Age',
      placeholder: 'e.g. 50',
      icon: '📅',
      hint: 'By what age do you want to achieve this?',
      min: form.age ? parseInt(form.age) + 1 : 20,
      max: 80,
    },
  ];

  const current = fields[step];

  const validate = () => {
    const val = form[current.key];
    if (!current.optional && (!val || val.trim() === '')) {
      return 'This field is required';
    }
    if (val && isNaN(Number(val))) return 'Must be a number';
    if (current.min && val && Number(val) < current.min)
      return `Minimum value is ${current.min}`;
    if (current.max && val && Number(val) > current.max)
      return `Maximum value is ${current.max}`;
    if (current.key === 'goal_age' && val && form.age && Number(val) <= Number(form.age))
      return 'Goal age must be greater than current age';
    return null;
  };

  const handleNext = () => {
    const err = validate();
    if (err) { setErrors({ [current.key]: err }); return; }
    setErrors({});
    if (step < fields.length - 1) { setStep(s => s + 1); return; }
    // submit
    const income = Number(form.monthly_income);
    const profile = {
      age: Number(form.age),
      monthly_income: income,
      monthly_expenses: form.monthly_expenses ? Number(form.monthly_expenses) : Math.round(income * 0.6),
      existing_savings: form.existing_savings ? Number(form.existing_savings) : 0,
      goal_amount: Number(form.goal_amount),
      goal_age: Number(form.goal_age),
    };
    onComplete(profile);
  };

  const handleKeyDown = (e) => { if (e.key === 'Enter') handleNext(); };

  const progress = ((step + 1) / fields.length) * 100;
  const investable = form.monthly_income
    ? Math.max(0, Number(form.monthly_income) - (form.monthly_expenses ? Number(form.monthly_expenses) : Number(form.monthly_income) * 0.6))
    : null;

  return (
    <div className="animate-fadeUp" style={{ maxWidth: 540, margin: '0 auto' }}>
      {/* Progress */}
      <div style={{ marginBottom: 32 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
            Step {step + 1} of {fields.length}
          </span>
          <span style={{ fontSize: '0.8rem', color: 'var(--accent-blue)', fontWeight: 600 }}>
            {Math.round(progress)}% complete
          </span>
        </div>
        <div className="progress-bar">
          <div className="progress-fill" style={{ width: `${progress}%` }} />
        </div>

        {/* Step dots */}
        <div style={{ display: 'flex', gap: 8, marginTop: 12, justifyContent: 'center' }}>
          {fields.map((_, i) => (
            <div
              key={i}
              style={{
                width: i === step ? 24 : 8,
                height: 8,
                borderRadius: 99,
                background: i <= step ? 'var(--accent-blue)' : 'var(--border)',
                transition: 'all 0.3s',
              }}
            />
          ))}
        </div>
      </div>

      {/* Card */}
      <div className="card" style={{ padding: '40px 36px' }}>
        <div style={{ textAlign: 'center', marginBottom: 32 }}>
          <div style={{ fontSize: 40, marginBottom: 12 }}>{current.icon}</div>
          <div className="heading-md" style={{ marginBottom: 6 }}>{current.label}</div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>{current.hint}</div>
        </div>

        <div className="input-group" style={{ marginBottom: 8 }}>
          <input
            id={`profile-${current.key}`}
            type="number"
            className="input-field"
            placeholder={current.placeholder}
            value={form[current.key]}
            onChange={e => setForm(f => ({ ...f, [current.key]: e.target.value }))}
            onKeyDown={handleKeyDown}
            autoFocus
            style={{ fontSize: '1.2rem', padding: '16px', textAlign: 'center' }}
          />
          {errors[current.key] && (
            <div style={{ color: 'var(--accent-rose)', fontSize: '0.8rem', textAlign: 'center' }}>
              ⚠ {errors[current.key]}
            </div>
          )}
          {current.optional && (
            <div style={{ color: 'var(--text-muted)', fontSize: '0.75rem', textAlign: 'center' }}>
              Optional — press Enter or Next to skip
            </div>
          )}
        </div>

        {/* Live insight */}
        {current.key === 'monthly_expenses' && investable !== null && (
          <div style={{
            background: 'rgba(16,185,129,0.08)',
            border: '1px solid rgba(16,185,129,0.2)',
            borderRadius: 10,
            padding: '10px 14px',
            marginBottom: 16,
            display: 'flex',
            alignItems: 'center',
            gap: 8,
            fontSize: '0.85rem',
          }}>
            <span>💡</span>
            <span style={{ color: 'var(--accent-emerald)' }}>
              Monthly investable amount: <strong>{formatINR(investable)}</strong>
            </span>
          </div>
        )}

        <div style={{ display: 'flex', gap: 12, marginTop: 24 }}>
          {step > 0 && (
            <button
              id="profile-back-btn"
              className="btn btn-secondary"
              onClick={() => { setStep(s => s - 1); setErrors({}); }}
              style={{ flex: 1 }}
            >
              ← Back
            </button>
          )}
          <button
            id="profile-next-btn"
            className="btn btn-primary"
            onClick={handleNext}
            style={{ flex: 2 }}
          >
            {step === fields.length - 1 ? '🚀 Start Simulation' : 'Next →'}
          </button>
        </div>
      </div>

      {/* Summary preview */}
      {step > 1 && (
        <div className="card" style={{ marginTop: 16, padding: '16px 20px' }}>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: 8, fontWeight: 600, textTransform: 'uppercase' }}>
            Profile so far
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 12 }}>
            {['age', 'monthly_income', 'monthly_expenses'].map(k => form[k] && (
              <div key={k} style={{ display: 'flex', gap: 4, fontSize: '0.8rem' }}>
                <span style={{ color: 'var(--text-secondary)' }}>{fields.find(f => f.key === k)?.label}:</span>
                <span style={{ color: 'var(--text-primary)', fontWeight: 600 }}>
                  {k === 'age' ? form[k] + ' yrs' : formatINR(Number(form[k]))}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
