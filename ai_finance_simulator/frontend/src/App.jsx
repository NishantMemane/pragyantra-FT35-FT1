import React from 'react';
import ProfileSetup from './components/ProfileSetup';
import ScenarioCards from './components/ScenarioCards';
import ChartContainer from './components/ChartContainer';
import ReverseCards from './components/ReverseCards';
import StoryDisplay from './components/StoryDisplay';
import ModeToggle from './components/ModeToggle';
import {
  simulateForward,
  simulateReverse,
  getMockForwardResult,
  getMockReverseResult,
} from './api/apiClient';

// ── Helpers ───────────────────────────────────────────────────────────────────
const STAGE = { LANDING: 'landing', PROFILE: 'profile', SIMULATE: 'simulate', RESULTS: 'results' };

// ── Navbar ────────────────────────────────────────────────────────────────────
function Navbar({ profile, onReset, backendLive }) {
  return (
    <nav style={{
      background: 'rgba(255,255,255,0.92)',
      backdropFilter: 'blur(14px)',
      borderBottom: '1px solid var(--border)',
      position: 'sticky',
      top: 0,
      zIndex: 100,
      boxShadow: '0 1px 12px rgba(0,0,0,0.06)',
    }}>
      <div className="container" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', height: 64 }}>

        {/* Logo */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <div style={{
            width: 38, height: 38, borderRadius: 10,
            background: 'var(--gradient-brand)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: 18, boxShadow: '0 4px 14px rgba(30,58,138,0.30)',
          }}>📊</div>
          <div>
            <div style={{
              fontFamily: 'Times New Roman, Times, serif',
              fontWeight: 900, fontSize: '1.05rem',
              letterSpacing: '-0.01em', color: 'var(--text-primary)',
            }}>FinSim AI</div>
            <div style={{ fontSize: '0.62rem', color: 'var(--text-muted)', letterSpacing: '0.06em', textTransform: 'uppercase' }}>
              Financial Decision Engine
            </div>
          </div>
        </div>

        {/* Right */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <span className={`badge ${backendLive ? 'badge-green' : 'badge-amber'}`}
            style={{ display: 'flex', gap: 5, alignItems: 'center' }}>
            <div className="glow-dot" style={{ width: 6, height: 6 }} />
            {backendLive ? 'Live Backend' : 'Demo Mode'}
          </span>
          <a href="http://localhost:8000/docs" target="_blank" rel="noreferrer"
            className="btn btn-secondary"
            style={{ padding: '6px 14px', fontSize: '0.78rem' }}>
            📖 API Docs
          </a>
          {profile && (
            <button id="reset-profile-btn" className="btn btn-secondary"
              onClick={onReset} style={{ padding: '6px 14px', fontSize: '0.78rem' }}>
              ↺ New Profile
            </button>
          )}
        </div>
      </div>
    </nav>
  );
}

// ── Hero ──────────────────────────────────────────────────────────────────────
function Hero({ onStart }) {
  return (
    <div style={{
      minHeight: 'calc(100vh - 64px)',
      display: 'flex', flexDirection: 'column',
      alignItems: 'center', justifyContent: 'center',
      padding: '60px 24px', textAlign: 'center',
      position: 'relative', overflow: 'hidden',
      background: '#ffffff',
    }}>
      {/* Subtle grid */}
      <div style={{
        position: 'absolute', inset: 0,
        backgroundImage: 'radial-gradient(rgba(30,58,138,0.05) 1px, transparent 1px)',
        backgroundSize: '28px 28px', pointerEvents: 'none',
      }} />
      {/* Glow blobs */}
      <div style={{
        position: 'absolute', top: '18%', left: '12%',
        width: 420, height: 420,
        background: 'radial-gradient(circle, rgba(30,58,138,0.08) 0%, transparent 70%)',
        pointerEvents: 'none',
      }} />
      <div style={{
        position: 'absolute', bottom: '18%', right: '8%',
        width: 360, height: 360,
        background: 'radial-gradient(circle, rgba(109,40,217,0.07) 0%, transparent 70%)',
        pointerEvents: 'none',
      }} />

      <div style={{ position: 'relative', maxWidth: 800 }}>
        {/* Badge */}
        <div className="animate-fadeUp stagger-1" style={{ display: 'inline-flex', alignItems: 'center', gap: 8, marginBottom: 24 }}>
          <span className="badge badge-violet">🏆 Pragma Hackathon — FT-1</span>
        </div>

        {/* Heading */}
        <h1 className="heading-xl animate-fadeUp stagger-2" style={{ marginBottom: 20 }}>
          AI-Powered{' '}
          <span className="text-gradient">Financial Decision</span>
          <br />Simulation Engine
        </h1>

        {/* Sub */}
        <p className="animate-fadeUp stagger-3" style={{
          color: 'var(--text-secondary)', fontSize: '1.1rem',
          lineHeight: 1.75, maxWidth: 620, margin: '0 auto 36px',
        }}>
          Model real Indian financial decisions — SIPs, loans, home purchases — using
          Monte Carlo simulations, tax engines, and AI storytelling. See your financial future today.
        </p>

        {/* CTA */}
        <div className="animate-fadeUp stagger-4"
          style={{ display: 'flex', gap: 16, justifyContent: 'center', flexWrap: 'wrap' }}>
          <button id="hero-start-btn" className="btn btn-primary"
            onClick={onStart} style={{ padding: '14px 34px', fontSize: '1.05rem' }}>
            🚀 Start Simulation
          </button>
          <a href="http://localhost:8000/docs" target="_blank" rel="noreferrer"
            className="btn btn-secondary" style={{ padding: '14px 34px', fontSize: '1.05rem' }}>
            📖 API Docs
          </a>
        </div>

        {/* Feature pills */}
        <div className="animate-fadeUp stagger-5"
          style={{ display: 'flex', gap: 10, justifyContent: 'center', flexWrap: 'wrap', marginTop: 40 }}>
          {[
            '🎲 Monte Carlo (500 runs)',
            '🧾 Indian Tax Engine',
            '🔮 Forward Simulation',
            '🔁 Reverse Goal Planning',
            '🤖 AI Storytelling',
            '📈 LTCG Analysis',
          ].map(feat => (
            <span key={feat} style={{
              background: 'rgba(30,58,138,0.07)',
              border: '1px solid rgba(30,58,138,0.15)',
              borderRadius: 99, padding: '5px 14px',
              fontSize: '0.8rem', color: 'var(--text-secondary)',
              fontFamily: 'Times New Roman, Times, serif',
            }}>{feat}</span>
          ))}
        </div>

        {/* Stats */}
        <div className="animate-fadeUp stagger-5"
          style={{ display: 'flex', gap: 40, justifyContent: 'center', marginTop: 56, flexWrap: 'wrap' }}>
          {[
            { value: '500', label: 'Monte Carlo runs' },
            { value: '4',   label: 'Tax engines' },
            { value: '4',   label: 'Decision types' },
            { value: '∞',   label: 'Possibilities' },
          ].map(stat => (
            <div key={stat.label} style={{ textAlign: 'center' }}>
              <div style={{
                fontFamily: 'Times New Roman, Times, serif',
                fontSize: '2.4rem', fontWeight: 900,
                background: 'var(--gradient-brand)',
                WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
              }}>{stat.value}</div>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: 2 }}>{stat.label}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ── Main App ──────────────────────────────────────────────────────────────────
export default function App() {
  const [stage, setStage]                   = React.useState(STAGE.LANDING);
  const [profile, setProfile]               = React.useState(null);
  const [mode, setMode]                     = React.useState('forward');
  const [result, setResult]                 = React.useState(null);
  const [loading, setLoading]               = React.useState(false);
  const [selectedScenario, setSelectedScenario] = React.useState(null);
  const [backendLive, setBackendLive]       = React.useState(false);
  const [apiError, setApiError]             = React.useState(null);

  // ── Simulate handler ────────────────────────────────────────────────────────
  const handleSimulate = async (decisionOrNull, scenario) => {
    setLoading(true);
    setResult(null);
    setApiError(null);
    setSelectedScenario(scenario || null);

    try {
      let data;

      if (mode === 'forward') {
        try {
          data = await simulateForward(profile, decisionOrNull);
          setBackendLive(true);
        } catch (err) {
          console.warn('Backend unavailable, using mock data:', err.message);
          setApiError('Backend offline — showing demo data. Start uvicorn to get live results.');
          await new Promise(r => setTimeout(r, 800));
          data = getMockForwardResult(profile, decisionOrNull);
        }
      } else {
        try {
          data = await simulateReverse(profile);
          setBackendLive(true);
        } catch (err) {
          console.warn('Backend unavailable, using mock data:', err.message);
          setApiError('Backend offline — showing demo data. Start uvicorn to get live results.');
          await new Promise(r => setTimeout(r, 800));
          data = getMockReverseResult(profile);
        }
      }

      setResult(data);
      setStage(STAGE.RESULTS);
    } catch (err) {
      console.error('Simulation failed entirely:', err);
      setApiError('Simulation failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleReverseSimulate = () => handleSimulate(null, null);

  const handleProfileComplete = (p) => {
    setProfile(p);
    setStage(STAGE.SIMULATE);
    setResult(null);
    setApiError(null);
  };

  const handleReset = () => {
    setStage(STAGE.LANDING);
    setProfile(null);
    setResult(null);
    setMode('forward');
    setApiError(null);
  };

  const handleBack = () => {
    setStage(STAGE.SIMULATE);
    setResult(null);
    setApiError(null);
  };

  // ── Render ─────────────────────────────────────────────────────────────────
  return (
    <>
      <Navbar profile={profile} onReset={handleReset} backendLive={backendLive} />

      <main style={{ flex: 1 }}>

        {/* ── Landing ── */}
        {stage === STAGE.LANDING && <Hero onStart={() => setStage(STAGE.PROFILE)} />}

        {/* ── Profile Setup ── */}
        {stage === STAGE.PROFILE && (
          <div className="container section">
            <div style={{ textAlign: 'center', marginBottom: 40 }}>
              <h2 className="heading-lg" style={{ marginBottom: 8 }}>Build Your Financial Profile</h2>
              <p style={{ color: 'var(--text-secondary)' }}>
                We'll use this to personalise every simulation to your situation
              </p>
            </div>
            <ProfileSetup onComplete={handleProfileComplete} />
          </div>
        )}

        {/* ── Simulation Input ── */}
        {stage === STAGE.SIMULATE && profile && (
          <div className="container section">
            {/* Mode selector */}
            <div style={{
              display: 'flex', alignItems: 'center',
              justifyContent: 'space-between', flexWrap: 'wrap',
              gap: 16, marginBottom: 32,
            }}>
              <div>
                <h2 className="heading-lg" style={{ marginBottom: 4 }}>Run Simulation</h2>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.88rem' }}>
                  <strong>Forward</strong>: model a decision's impact &nbsp;|&nbsp;
                  <strong>Reverse</strong>: calculate SIP for your goal
                </p>
              </div>
              <ModeToggle mode={mode} onChange={m => { setMode(m); setResult(null); }} />
            </div>

            {/* API error banner */}
            {apiError && (
              <div className="alert-banner alert-warning" style={{ marginBottom: 20 }}>
                ⚠️ {apiError}
              </div>
            )}

            {/* Forward mode */}
            {mode === 'forward' && (
              <ScenarioCards profile={profile} onSimulate={handleSimulate} loading={loading} />
            )}

            {/* Reverse mode */}
            {mode === 'reverse' && (
              <div style={{ maxWidth: 660 }}>
                <div className="card" style={{ borderColor: 'rgba(109,40,217,0.25)' }}>
                  <div style={{ display: 'flex', gap: 14, alignItems: 'flex-start', marginBottom: 20 }}>
                    <span style={{ fontSize: 38 }}>🔁</span>
                    <div>
                      <div className="heading-md" style={{ marginBottom: 6 }}>Reverse Goal Planner</div>
                      <p style={{ color: 'var(--text-secondary)', fontSize: '0.88rem', lineHeight: 1.65 }}>
                        You want <strong style={{ color: 'var(--text-primary)' }}>
                          ₹{(profile.goal_amount / 100000).toFixed(0)}L
                        </strong> by age <strong style={{ color: 'var(--text-primary)' }}>{profile.goal_age}</strong>.
                        We'll calculate exactly how much monthly SIP you need to start today — and the cost of waiting.
                      </p>
                    </div>
                  </div>

                  {/* Mini stats */}
                  <div className="grid-3" style={{ marginBottom: 20, gap: 12 }}>
                    {[
                      { label: 'Goal',       value: `₹${(profile.goal_amount / 100000).toFixed(0)}L` },
                      { label: 'By Age',     value: profile.goal_age },
                      { label: 'Years Left', value: `${profile.goal_age - profile.age} yrs` },
                    ].map(item => (
                      <div key={item.label} style={{
                        background: 'var(--bg-secondary)',
                        borderRadius: 10, padding: '12px 16px', textAlign: 'center',
                        border: '1px solid var(--border)',
                      }}>
                        <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: 4, fontWeight: 700, letterSpacing: '0.06em' }}>
                          {item.label}
                        </div>
                        <div style={{
                          fontFamily: 'Times New Roman, Times, serif',
                          fontSize: '1.5rem', fontWeight: 800, color: 'var(--accent-violet)',
                        }}>
                          {item.value}
                        </div>
                      </div>
                    ))}
                  </div>

                  <button
                    id="reverse-simulate-btn"
                    className="btn btn-primary"
                    onClick={handleReverseSimulate}
                    disabled={loading}
                    style={{ background: 'linear-gradient(135deg, #6d28d9, #4c1d95)', boxShadow: '0 4px 18px rgba(109,40,217,0.35)' }}
                  >
                    {loading ? '⏳ Calculating…' : '🔁 Calculate Required SIP →'}
                  </button>
                </div>
              </div>
            )}

            {/* Loading */}
            {loading && (
              <div className="animate-fadeIn"
                style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 16, padding: '60px 0' }}>
                <div className="spinner" />
                <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
                  Running 500 Monte Carlo simulations…
                </div>
                <div style={{ color: 'var(--text-muted)', fontSize: '0.78rem' }}>
                  Applying Indian tax engine · LTCG rules · AI narrative
                </div>
              </div>
            )}
          </div>
        )}

        {/* ── Results ── */}
        {stage === STAGE.RESULTS && result && profile && (
          <div className="container section">
            {/* Back + header */}
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 32, flexWrap: 'wrap' }}>
              <button id="back-to-simulate-btn" className="btn btn-secondary"
                onClick={handleBack} style={{ padding: '8px 16px', fontSize: '0.85rem' }}>
                ← Back
              </button>
              <div>
                <h2 className="heading-lg" style={{ marginBottom: 2 }}>
                  {mode === 'forward' ? '🔮 Forward Simulation Results' : '🔁 Reverse Goal Analysis'}
                </h2>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.82rem' }}>
                  {selectedScenario ? `Scenario: ${selectedScenario.emoji} ${selectedScenario.title}` : 'Goal-based planning'}
                  &nbsp;·&nbsp;
                  {backendLive ? 'Live results from FastAPI + Monte Carlo engine' : 'Demo mode — start uvicorn for live AI results'}
                </p>
              </div>
              <button id="new-simulation-btn" className="btn btn-primary"
                onClick={() => setStage(STAGE.SIMULATE)}
                style={{ marginLeft: 'auto', padding: '8px 18px', fontSize: '0.85rem' }}>
                + New Simulation
              </button>
            </div>

            {/* API error banner */}
            {apiError && (
              <div className="alert-banner alert-warning">⚠️ {apiError}</div>
            )}

            {/* Charts / Cards */}
            {mode === 'forward'
              ? <ChartContainer result={result} profile={profile} scenario={selectedScenario} />
              : <ReverseCards result={result} profile={profile} />
            }

            {/* AI Story */}
            <StoryDisplay story={result.story} mode={mode} loading={false} />
          </div>
        )}
      </main>

      {/* Footer */}
      <footer style={{
        borderTop: '1px solid var(--border)',
        background: 'var(--bg-secondary)',
        padding: '20px 0',
      }}>
        <div className="container" style={{
          display: 'flex', justifyContent: 'space-between',
          alignItems: 'center', flexWrap: 'wrap', gap: 12,
          fontSize: '0.78rem', color: 'var(--text-muted)',
          fontFamily: 'Times New Roman, Times, serif',
        }}>
          <span>🏆 Pragma Hackathon · FT-1: AI Financial Decision Simulation Engine</span>
          <span>Built with ❤️ · React + Vite + FastAPI + Monte Carlo</span>
        </div>
      </footer>
    </>
  );
}
