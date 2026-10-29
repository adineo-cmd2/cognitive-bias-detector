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

  if (!mounted) return <p className="text-sm text-soft">Loading chart…</p>;
  if (error) return <p className="text-sm text-rust">{error}</p>;
  if (data.length === 0)
    return (
      <p className="text-sm text-soft">
        No data for the radar yet — upload writing to fill it in.
      </p>
    );

  return (
    <div className="h-80">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart data={data} outerRadius="75%">
          <PolarGrid stroke="#ddcfb4" />
          <PolarAngleAxis
            dataKey="bias_type"
            tick={{ fill: '#2a2520', fontSize: 11 }}
          />
          <Radar dataKey="count" stroke="#9c2f24" fill="#9c2f24" fillOpacity={0.22} />
          <Tooltip
            contentStyle={{
              background: '#fffaf0',
              border: '1px solid #ddcfb4',
              borderRadius: 0,
              fontFamily: 'Karla, sans-serif',
              fontSize: 12,
              color: '#2a2520',
            }}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}
