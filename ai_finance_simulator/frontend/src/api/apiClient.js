import axios from 'axios';

// Vite proxy forwards /api → http://localhost:8000
const BASE_URL = import.meta.env.VITE_API_URL || '';

const api = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' },
  timeout: 60000,   // Ollama can be slow — allow 60 s
});

// ── Profile ──────────────────────────────────────────────────────────────────
/**
 * POST /api/profile
 * body: UserProfile
 */
export const submitProfile = (profileData) =>
  api.post('/api/profile', profileData).then(r => r.data);

// ── Orchestrate (AI routing) ──────────────────────────────────────────────────
/**
 * POST /api/orchestrate
 * body: { message, profile }
 */
export const orchestrate = (message, profile) =>
  api.post('/api/orchestrate', { message, profile }).then(r => r.data);

// ── Forward Simulation ────────────────────────────────────────────────────────
/**
 * POST /api/simulate/forward
 * body: { profile: UserProfile, decision: DecisionParams }
 *
 * IMPORTANT: backend expects { profile: {...}, decision: {...} }
 * NOT a spread of both objects.
 */
export const simulateForward = (profile, decision) =>
  api.post('/api/simulate/forward', { profile, decision }).then(r => r.data);

// ── Reverse Simulation ────────────────────────────────────────────────────────
/**
 * POST /api/simulate/reverse
 * body: { profile: UserProfile }
 */
export const simulateReverse = (profile) =>
  api.post('/api/simulate/reverse', { profile }).then(r => r.data);


// ════════════════════════════════════════════════════════════════════════════
// MOCK DATA — used as fallback when backend is offline
// ════════════════════════════════════════════════════════════════════════════

export const getMockForwardResult = (profile, decision) => {
  const years  = profile.goal_age - profile.age;
  const labels = Array.from({ length: years + 1 }, (_, i) => profile.age + i);

  const grow = (start, rate, n) =>
    Array.from({ length: n + 1 }, (_, i) =>
      Math.round(start * Math.pow(1 + rate, i))
    );

  const base   = Math.max(0, (profile.monthly_income - profile.monthly_expenses) * 12);
  const best   = grow(base, 0.14,  years);
  const exp    = grow(base, 0.105, years);
  const worst  = grow(base, 0.07,  years);
  const ghost  = grow(base * 0.75, 0.105, years);

  const decType = decision?.type || 'SIP';
  const decAmt  = decision?.amount || decision?.monthly_sip || 5000;

  return {
    labels,
    best_case:              best,
    expected_case:          exp,
    worst_case:             worst,
    without_decision:       ghost,
    best_final:             best[years],
    expected_final:         exp[years],
    worst_final:            worst[years],
    goal_achieved:          exp[years] >= profile.goal_amount,
    shortfall:              Math.max(0, profile.goal_amount - exp[years]),
    post_tax_expected_final: Math.round(exp[years] * 0.91),
    ltcg_tax_paid:          Math.round(exp[years] * 0.09),
    story: `Based on your ${decType} of ₹${Number(decAmt).toLocaleString('en-IN')}, you are projected to accumulate approximately ₹${(exp[years] / 100000).toFixed(1)}L over ${years} years. Your disciplined approach puts you ${exp[years] >= profile.goal_amount ? 'ahead of' : 'slightly behind'} your goal of ₹${(profile.goal_amount / 100000).toFixed(0)}L. Remember — the power of compounding is strongest in the final years, so consistency matters more than timing.`,
  };
};

export const getMockReverseResult = (profile) => {
  const years = profile.goal_age - profile.age;
  const r = 0.10 / 12;
  const n = years * 12;
  const fv = profile.goal_amount;
  const sip  = Math.round((fv * r) / (Math.pow(1 + r, n) - 1) / (1 + r));
  const sip2 = Math.round(sip * 1.20);
  const sip5 = Math.round(sip * 1.56);

  return {
    required_monthly_sip:    sip,
    if_delayed_2_years:      sip2,
    if_delayed_5_years:      sip5,
    existing_savings_growth: Math.round((profile.existing_savings || 0) * Math.pow(1.10, years)),
    total_contribution:      sip * n,
    total_returns:           Math.max(0, fv - sip * n),
    story: `To reach ₹${(profile.goal_amount / 100000).toFixed(0)}L by age ${profile.goal_age}, you need just ₹${sip.toLocaleString('en-IN')}/month starting today. Delaying by 2 years pushes this to ₹${sip2.toLocaleString('en-IN')} — a ${Math.round(((sip2 - sip) / sip) * 100)}% increase with zero extra benefit. Start now, even with a smaller amount, and let compounding do the heavy lifting.`,
  };
};

export default api;
