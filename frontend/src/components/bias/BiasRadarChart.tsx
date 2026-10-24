import { useEffect, useState } from 'react';
import {
  PolarAngleAxis,
  PolarGrid,
  Radar,
  RadarChart,
  ResponsiveContainer,
  Tooltip,
} from 'recharts';
import { apiGet } from '../../lib/apiClient';

interface RadarEntry {
  bias_type: string;
  count: number;
}

export default function BiasRadarChart() {
  const [data, setData] = useState<RadarEntry[]>([]);
  const [mounted, setMounted] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    setMounted(true);
    apiGet('/api/profile/bias-map')
      .then((res) => {
        setData((res.radar ?? []) as RadarEntry[]);
      })
      .catch((e: unknown) =>
        setError(e instanceof Error ? e.message : 'Failed to load radar.'),
      );
  }, []);

  if (!mounted) return <p className="text-sm opacity-70">Loading chart…</p>;
  if (error) return <p className="text-sm text-rust">{error}</p>;
  if (data.length === 0)
    return (
      <p className="text-sm opacity-70">
        No data for the radar yet — upload writing to fill it in.
      </p>
    );

  return (
    <div className="h-80">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart data={data} outerRadius="75%">
          <PolarGrid stroke="#e8dcc3" />
          <PolarAngleAxis
            dataKey="bias_type"
            tick={{ fill: '#292524', fontSize: 11 }}
          />
          <Radar dataKey="count" stroke="#b3402a" fill="#b3402a" fillOpacity={0.4} />
          <Tooltip />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}
