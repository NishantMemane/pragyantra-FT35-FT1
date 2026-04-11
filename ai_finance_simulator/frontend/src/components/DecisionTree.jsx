import React, { useState, useEffect } from 'react';

/**
 * DecisionTree — standalone decision parameter form.
 * Props: decisionType ('LOAN'|'SIP'|'DELAY'|'LUMPSUM'), userProfile, onSubmit(decision)
 *
 * This component is available for external use. The main simulation flow
 * uses ScenarioCards instead, which bundles type selection + params together.
 */
export default function DecisionTree({ decisionType, userProfile, onSubmit }) {
  const [amount, setAmount]           = useState('');
  const [interestRate, setInterestRate] = useState('');
  const [tenureMonths, setTenureMonths] = useState('');
  const [monthlySip, setMonthlySip]   = useState('');
  const [delayYears, setDelayYears]   = useState('2');
  const [instrument, setInstrument]   = useState('equity');
  const [calculatedEmi, setCalcEmi]   = useState(0);

  const calcEmi = (p, r, n) => {
    if (!p || !r || !n) return 0;
    const mr = r / 12 / 100;
    if (mr === 0) return Math.round(p / n);
    return Math.round(p * mr * Math.pow(1 + mr, n) / (Math.pow(1 + mr, n) - 1));
  };

  useEffect(() => {
    if (decisionType === 'LOAN' && amount && interestRate && tenureMonths) {
      setCalcEmi(calcEmi(+amount, +interestRate, +tenureMonths));
    } else {
      setCalcEmi(0);
    }
  }, [amount, interestRate, tenureMonths, decisionType]);

  const handleSubmit = () => {
    const decision = {
      type: decisionType,
      amount: 0, interest_rate: 0, tenure_months: 0,
      monthly_emi: 0, cash_flow_reduction: 0,
      monthly_sip: 0, delay_years: 0, instrument: 'equity',
    };
    if (decisionType === 'LOAN') {
      decision.amount = +amount;
      decision.interest_rate = +interestRate;
      decision.tenure_months = +tenureMonths;
      decision.monthly_emi = calculatedEmi;
      decision.cash_flow_reduction = calculatedEmi;
    } else if (decisionType === 'SIP') {
      decision.monthly_sip = +monthlySip;
      decision.cash_flow_reduction = +monthlySip;
    } else if (decisionType === 'DELAY') {
      decision.delay_years = +delayYears;
    } else if (decisionType === 'LUMPSUM') {
      decision.amount = +amount;
      decision.instrument = instrument;
    }
    onSubmit(decision);
  };

  const titles = { LOAN: 'Loan Details', SIP: 'SIP Investment', DELAY: 'Delay Details', LUMPSUM: 'Lump Sum Investment' };

  return (
    <div className="card" style={{ maxWidth: 600, margin: '0 auto' }}>
      <div className="heading-md" style={{ marginBottom: 4 }}>{titles[decisionType] || 'Decision Details'}</div>
      <p style={{ color: 'var(--text-secondary)', fontSize: '0.88rem', marginBottom: 24 }}>
        Tell us more so we can simulate your exact scenario
      </p>

      {/* LOAN */}
      {decisionType === 'LOAN' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          {[
            { label: 'Loan Amount (₹)', val: amount, set: setAmount, ph: '500000' },
            { label: 'Annual Interest Rate (%)', val: interestRate, set: setInterestRate, ph: '12', step: '0.1' },
            { label: 'Tenure (months)', val: tenureMonths, set: setTenureMonths, ph: '36' },
          ].map(f => (
            <div className="input-group" key={f.label}>
              <label className="input-label">{f.label}</label>
              <input type="number" className="input-field" placeholder={f.ph}
                step={f.step || '1'} value={f.val}
                onChange={e => f.set(e.target.value)} />
            </div>
          ))}
          {calculatedEmi > 0 && (
            <div className="alert-banner alert-info">
              💡 Your monthly EMI will be <strong>₹{calculatedEmi.toLocaleString('en-IN')}</strong>
            </div>
          )}
        </div>
      )}

      {/* SIP */}
      {decisionType === 'SIP' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <div className="input-group">
            <label className="input-label">Monthly SIP Amount (₹)</label>
            <input type="number" className="input-field" placeholder="10000"
              value={monthlySip} onChange={e => setMonthlySip(e.target.value)} />
          </div>
          <div className="alert-banner alert-info">
            💡 This amount will be invested every month over your goal horizon.
          </div>
        </div>
      )}

      {/* DELAY */}
      {decisionType === 'DELAY' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <div className="input-group">
            <label className="input-label">Delay by how many years?</label>
            <input type="range" min="1" max="10" value={delayYears}
              onChange={e => setDelayYears(e.target.value)}
              style={{ accentColor: 'var(--accent-blue)', width: '100%' }} />
            <div style={{
              textAlign: 'center', fontSize: '2rem', fontWeight: 900,
              color: 'var(--accent-blue)', fontFamily: 'Times New Roman, Times, serif',
            }}>
              {delayYears} year{+delayYears !== 1 ? 's' : ''}
            </div>
          </div>
          <div className="alert-banner alert-warning">
            ⚠️ Every year you delay will significantly increase the monthly amount you need to invest.
          </div>
        </div>
      )}

      {/* LUMPSUM */}
      {decisionType === 'LUMPSUM' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <div className="input-group">
            <label className="input-label">Lump Sum Amount (₹)</label>
            <input type="number" className="input-field" placeholder="500000"
              value={amount} onChange={e => setAmount(e.target.value)} />
          </div>
          <div className="input-group">
            <label className="input-label">Instrument</label>
            <select className="input-field" value={instrument}
              onChange={e => setInstrument(e.target.value)}>
              <option value="equity">Equity Mutual Fund (~12% expected)</option>
              <option value="fd">Fixed Deposit (~7% expected)</option>
            </select>
          </div>
        </div>
      )}

      <button id="decision-tree-submit-btn" className="btn btn-primary"
        onClick={handleSubmit} style={{ marginTop: 28, width: '100%', justifyContent: 'center', padding: '14px' }}>
        🚀 Run Simulation →
      </button>
    </div>
  );
}