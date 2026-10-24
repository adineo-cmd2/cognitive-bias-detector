import { useEffect, useMemo, useState } from 'react';
import {
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { apiGet } from '../../lib/apiClient';

interface TrendPoint {
  week: string;
  bias_type: string;
  count: number;
}

interface ChartRow {
  week: string;
  count: number;
}

const ALL = '__all__';

export default function BiasTimeline() {
  const [trend, setTrend] = useState<TrendPoint[]>([]);
  const [filter, setFilter] = useState<string>(ALL);
  const [mounted, setMounted] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    setMounted(true);
    apiGet('/api/analytics/trend')
      .then((data) => {
        setTrend((data.trend ?? []) as TrendPoint[]);
      })
      .catch((e: unknown) =>
        setError(e instanceof Error ? e.message : 'Failed to load trend.'),
      );
  }, []);

  const biasTypes = useMemo(
    () => Array.from(new Set(trend.map((t) => t.bias_type))).sort(),
    [trend],
  );

  const rows: ChartRow[] = useMemo(() => {
    const byWeek = new Map<string, number>();
    for (const t of trend) {
      if (filter !== ALL && t.bias_type !== filter) continue;
      byWeek.set(t.week, (byWeek.get(t.week) ?? 0) + t.count);
    }
    return Array.from(byWeek.entries())
      .map(([week, count]) => ({ week, count }))
      .sort((a, b) => (a.week < b.week ? -1 : 1));
  }, [trend, filter]);

  if (!mounted) return <p className="text-sm opacity-70">Loading timeline…</p>;
  if (error) return <p className="text-sm text-rust">{error}</p>;
  if (trend.length === 0)
    return (
      <p className="text-sm opacity-70">
        No trend data yet. Flags accumulate by week once you upload writing.
      </p>
    );

  return (
    <div>
      <label className="mb-2 block text-sm">
        Bias type:{' '}
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="rounded border border-sand bg-white px-2 py-1"
        >
          <option value={ALL}>All biases</option>
          {biasTypes.map((b) => (
            <option key={b} value={b}>
              {b.replace(/_/g, ' ')}
            </option>
          ))}
        </select>
      </label>
      {rows.length === 0 ? (
        <p className="text-sm opacity-70">No points for this filter.</p>
      ) : (
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={rows}>
              <XAxis dataKey="week" tick={{ fill: '#292524', fontSize: 12 }} />
              <YAxis
                allowDecimals={false}
                tick={{ fill: '#292524', fontSize: 12 }}
              />
              <Tooltip />
              <Line
                type="monotone"
                dataKey="count"
                stroke="#b3402a"
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}
