import React from 'react';
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, ReferenceLine, Legend,
} from 'recharts';

const formatINR = (n) => {
  if (n >= 10000000) return `₹${(n / 10000000).toFixed(2)}Cr`;
  if (n >= 100000)   return `₹${(n / 100000).toFixed(1)}L`;
  if (n >= 1000)     return `₹${(n / 1000).toFixed(0)}K`;
  return `₹${n}`;
};

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{
      background: 'var(--bg-card)',
      border: '1px solid var(--border-bright)',
      borderRadius: 10,
      padding: '12px 16px',
      boxShadow: 'var(--shadow-card)',
      minWidth: 180,
    }}>
      <div style={{ color: 'var(--text-secondary)', fontSize: '0.78rem', marginBottom: 8 }}>
        Age {label}
      </div>
      {payload.map(p => (
        <div key={p.name} style={{ display: 'flex', justifyContent: 'space-between', gap: 16, fontSize: '0.85rem', marginBottom: 4 }}>
          <span style={{ color: p.color }}>{p.name}</span>
          <span style={{ fontWeight: 700, color: 'var(--text-primary)' }}>{formatINR(p.value)}</span>
        </div>
      ))}
    </div>
  );
};

export default function ChartContainer({ result, profile, scenario }) {
  const [activeLines, setActiveLines] = React.useState({
    'Best Case': true,
    'Expected': true,
    'Worst Case': true,
    'Without Decision': true,
  });

  const chartData = result.labels.map((age, i) => ({
    age,
    'Best Case': result.best_case[i],
    'Expected': result.expected_case[i],
    'Worst Case': result.worst_case[i],
    'Without Decision': result.without_decision[i],
  }));

  const goalYear = profile.goal_age;
  const achieved = result.goal_achieved;
  const shortfall = result.shortfall;

  const lines = [
    { key: 'Best Case',        color: '#065f46', strokeDash: '',      fill: 'rgba(6,95,70,0.08)'    },
    { key: 'Expected',         color: '#1e3a8a', strokeDash: '',      fill: 'rgba(30,58,138,0.10)'  },
    { key: 'Worst Case',       color: '#92400e', strokeDash: '5 5',  fill: 'rgba(146,64,14,0.06)'  },
    { key: 'Without Decision', color: '#6b7280', strokeDash: '6 3',  fill: 'rgba(107,114,128,0.05)'},
  ];

  const toggleLine = (key) => {
    setActiveLines(prev => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div className="animate-fadeUp">
      {/* KPI cards */}
      <div className="grid-4" style={{ marginBottom: 28 }}>
        {[
          {
            label: 'Best Case (P90)',
            value: formatINR(result.best_final),
            color: '#10b981',
            icon: '🚀',
            sub: '10% probability',
          },
          {
            label: 'Expected (P50)',
            value: formatINR(result.expected_final),
            color: result.goal_achieved ? '#10b981' : '#f59e0b',
            icon: '📊',
            sub: result.goal_achieved ? '✅ Goal achieved!' : '⚠ Slightly short',
          },
          {
            label: 'Worst Case (P10)',
            value: formatINR(result.worst_final),
            color: '#f43f5e',
            icon: '⚡',
            sub: 'Conservative scenario',
          },
          {
            label: shortfall > 0 ? 'Shortfall' : 'Surplus',
            value: formatINR(Math.abs(shortfall)),
            color: shortfall > 0 ? '#f43f5e' : '#10b981',
            icon: shortfall > 0 ? '⚠️' : '🎯',
            sub: shortfall > 0 ? 'vs your goal' : 'above your goal',
          },
        ].map((kpi, i) => (
          <div
            key={kpi.label}
            className={`card animate-fadeUp stagger-${i + 1}`}
            style={{
              borderColor: kpi.color + '30',
              background: `linear-gradient(135deg, ${kpi.color}10, transparent)`,
              padding: '20px 22px',
            }}
          >
            <div style={{ fontSize: 24, marginBottom: 8 }}>{kpi.icon}</div>
            <div style={{ fontSize: '0.72rem', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: 4 }}>
              {kpi.label}
            </div>
            <div style={{ fontFamily: 'Outfit, sans-serif', fontSize: '1.6rem', fontWeight: 800, color: kpi.color, letterSpacing: '-0.02em' }}>
              {kpi.value}
            </div>
            <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: 4 }}>{kpi.sub}</div>
          </div>
        ))}
      </div>

      {/* Tax info */}
      {result.ltcg_tax_paid > 0 && (
        <div style={{
          background: 'rgba(245,158,11,0.08)',
          border: '1px solid rgba(245,158,11,0.2)',
          borderRadius: 10,
          padding: '10px 16px',
          marginBottom: 20,
          display: 'flex',
          gap: 16,
          alignItems: 'center',
          fontSize: '0.85rem',
          flexWrap: 'wrap',
        }}>
          <span>🧾</span>
          <span style={{ color: 'var(--text-secondary)' }}>
            LTCG Tax applied: <strong style={{ color: 'var(--accent-amber)' }}>{formatINR(result.ltcg_tax_paid)}</strong>
          </span>
          <span style={{ color: 'var(--text-secondary)' }}>
            Post-tax corpus: <strong style={{ color: 'var(--accent-emerald)' }}>{formatINR(result.post_tax_expected_final)}</strong>
          </span>
        </div>
      )}

      {/* Chart legend toggles */}
      <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap', marginBottom: 16 }}>
        {lines.map(l => (
          <button
            key={l.key}
            onClick={() => toggleLine(l.key)}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 6,
              padding: '5px 12px',
              borderRadius: 99,
              border: `1px solid ${activeLines[l.key] ? l.color + '60' : 'var(--border)'}`,
              background: activeLines[l.key] ? l.color + '15' : 'transparent',
              color: activeLines[l.key] ? l.color : 'var(--text-muted)',
              cursor: 'pointer',
              fontSize: '0.78rem',
              fontWeight: 600,
              transition: 'all 0.2s',
            }}
          >
            <span style={{ width: 20, height: 2, background: l.key === 'Worst Case' || l.key === 'Without Decision' ? 'repeating-linear-gradient(to right, ' + l.color + ' 0, ' + l.color + ' 5px, transparent 5px, transparent 8px)' : l.color, display: 'inline-block', borderRadius: 2 }} />
            {l.key}
          </button>
        ))}
      </div>

      {/* Main chart */}
      <div className="card" style={{ padding: '24px 12px 12px', marginBottom: 24 }}>
        <div style={{ padding: '0 12px', marginBottom: 16, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <div className="heading-md">Wealth Growth Projection</div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
              Age {profile.age} → {profile.goal_age} ({profile.goal_age - profile.age} years)
            </div>
          </div>
          <span className={`badge ${achieved ? 'badge-green' : 'badge-amber'}`}>
            {achieved ? '✅ On Track' : '⚠ Behind Goal'}
          </span>
        </div>

        <ResponsiveContainer width="100%" height={340}>
          <AreaChart data={chartData} margin={{ top: 10, right: 20, left: 10, bottom: 0 }}>
              {/* Graidents removed due to React Router conflict with local # anchors */}
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.06)" />
            <XAxis
              dataKey="age"
              stroke="var(--text-muted)"
              tick={{ fill: 'var(--text-secondary)', fontSize: 11 }}
              tickFormatter={v => `${v}`}
            />
            <YAxis
              stroke="var(--text-muted)"
              tick={{ fill: 'var(--text-secondary)', fontSize: 11 }}
              tickFormatter={formatINR}
              width={65}
            />
            <Tooltip content={<CustomTooltip />} />
            <ReferenceLine
              x={goalYear}
              stroke="rgba(0,0,0,0.20)"
              strokeDasharray="4 4"
              label={{ value: 'Goal Age', fill: 'var(--text-muted)', fontSize: 11 }}
            />
            <ReferenceLine
              y={profile.goal_amount}
              stroke="rgba(16,185,129,0.4)"
              strokeDasharray="6 3"
              label={{ value: `Goal ₹${(profile.goal_amount/100000).toFixed(0)}L`, fill: '#10b981', fontSize: 11, position: 'insideTopRight' }}
            />
            {lines.map(l => (
              activeLines[l.key] && (
                <Area
                  key={l.key}
                  type="monotone"
                  dataKey={l.key}
                  stroke={l.color}
                  strokeWidth={l.key === 'Expected' ? 2.5 : 1.5}
                  strokeDasharray={l.strokeDash}
                  fill={l.color}
                  fillOpacity={0.15}
                  dot={false}
                  activeDot={{ r: 5, fill: l.color }}
                />
              )
            ))}
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
