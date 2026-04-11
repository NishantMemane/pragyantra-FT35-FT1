import React from 'react';

const formatINR = (n) => {
  if (!n && n !== 0) return '—';
  if (n >= 10000000) return `₹${(n / 10000000).toFixed(2)} Cr`;
  if (n >= 100000)   return `₹${(n / 100000).toFixed(2)} L`;
  if (n >= 1000)     return `₹${(n / 1000).toFixed(1)} K`;
  return `₹${Number(n).toLocaleString('en-IN')}`;
};

/**
 * ReverseCards — displays reverse simulation results.
 * Props: result (ReverseResult object), profile (UserProfile object)
 */
export default function ReverseCards({ result, profile }) {
  if (!result) return null;

  const sip    = result.required_monthly_sip   || 0;
  const sip2   = result.if_delayed_2_years     || 0;
  const sip5   = result.if_delayed_5_years     || 0;
  const savings = result.existing_savings_growth || 0;
  const contrib = result.total_contribution     || 0;
  const returns = result.total_returns          || 0;

  const extra2 = Math.max(0, sip2 - sip);
  const extra5 = Math.max(0, sip5 - sip);
  const pct2   = sip > 0 ? ((extra2 / sip) * 100).toFixed(0) : 0;
  const pct5   = sip > 0 ? ((extra5 / sip) * 100).toFixed(0) : 0;

  const cards = [
    {
      label: 'Start Today',
      tag: '🟢 BEST OPTION',
      sip,
      extraLabel: null,
      color: '#065f46',
      gradBg: 'rgba(6,95,70,0.06)',
      borderColor: 'rgba(6,95,70,0.30)',
      sub: 'Lowest commitment. Best outcome.',
    },
    {
      label: 'Delay 2 Years',
      tag: '🟡 WAIT 2 YEARS',
      sip: sip2,
      extraLabel: extra2 > 0 ? `+${formatINR(extra2)}/mo extra (+${pct2}%)` : null,
      color: '#92400e',
      gradBg: 'rgba(146,64,14,0.06)',
      borderColor: 'rgba(146,64,14,0.30)',
      sub: 'Compounding works against you.',
    },
    {
      label: 'Delay 5 Years',
      tag: '🔴 WAIT 5 YEARS',
      sip: sip5,
      extraLabel: extra5 > 0 ? `+${formatINR(extra5)}/mo extra (+${pct5}%)` : null,
      color: '#9f1239',
      gradBg: 'rgba(159,18,57,0.06)',
      borderColor: 'rgba(159,18,57,0.30)',
      sub: 'Every year costs you significantly more.',
    },
  ];

  return (
    <div className="animate-fadeUp">
      {/* Header */}
      <div style={{ textAlign: 'center', marginBottom: 32 }}>
        <div className="heading-lg" style={{ marginBottom: 8 }}>
          How Much You Need To Save Monthly
        </div>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem' }}>
          The cost of waiting grows every year — start early, pay less
        </p>
      </div>

      {/* 3 SIP cards */}
      <div className="grid-3" style={{ marginBottom: 28 }}>
        {cards.map((c, i) => (
          <div
            key={c.label}
            className={`card animate-fadeUp stagger-${i + 1}`}
            style={{
              borderColor: c.borderColor,
              background: c.gradBg,
              textAlign: 'center',
              padding: '32px 24px',
            }}
          >
            {/* Tag */}
            <div style={{
              fontSize: '0.72rem',
              fontWeight: 800,
              letterSpacing: '0.1em',
              color: c.color,
              textTransform: 'uppercase',
              marginBottom: 16,
              fontFamily: 'Times New Roman, Times, serif',
            }}>
              {c.tag}
            </div>

            {/* SIP amount */}
            <div style={{
              fontFamily: 'Times New Roman, Times, serif',
              fontSize: 'clamp(1.8rem, 4vw, 2.8rem)',
              fontWeight: 900,
              color: c.color,
              letterSpacing: '-0.02em',
              lineHeight: 1.1,
              marginBottom: 6,
            }}>
              {formatINR(c.sip)}
            </div>
            <div style={{ color: c.color, fontSize: '1rem', fontWeight: 700, marginBottom: 16 }}>/ month</div>

            {/* Extra cost badge */}
            {c.extraLabel && (
              <div style={{
                display: 'inline-block',
                background: 'rgba(146,64,14,0.12)',
                color: c.color,
                border: `1px solid ${c.borderColor}`,
                borderRadius: 99,
                padding: '4px 12px',
                fontSize: '0.78rem',
                fontWeight: 700,
                marginBottom: 16,
              }}>
                {c.extraLabel}
              </div>
            )}

            <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', lineHeight: 1.5 }}>
              {c.sub}
            </p>
          </div>
        ))}
      </div>

      {/* Summary strip */}
      <div className="card" style={{
        background: 'var(--bg-secondary)',
        display: 'flex',
        flexWrap: 'wrap',
        gap: 24,
        justifyContent: 'center',
        padding: '20px 28px',
        textAlign: 'center',
      }}>
        {[
          { label: 'Savings Grow To', value: formatINR(savings), icon: '🏦' },
          { label: 'Total You Invest', value: formatINR(contrib), icon: '📥' },
          { label: 'Total Gains',     value: formatINR(returns), icon: '📈' },
        ].map(item => (
          <div key={item.label} style={{ minWidth: 120 }}>
            <div style={{ fontSize: '1.1rem', marginBottom: 4 }}>{item.icon}</div>
            <div style={{
              fontFamily: 'Times New Roman, Times, serif',
              fontSize: '1.3rem',
              fontWeight: 800,
              color: 'var(--text-primary)',
            }}>
              {item.value}
            </div>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              {item.label}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}