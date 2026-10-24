import { useEffect, useState } from 'react';
import { apiGet } from '../../lib/apiClient';

interface RankedEntry {
  bias_type: string;
  count: number;
  examples: string[];
}

export default function BiasListPanel() {
  const [ranked, setRanked] = useState<RankedEntry[]>([]);
  const [open, setOpen] = useState<string | null>(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiGet('/api/profile/bias-map')
      .then((data) => {
        setRanked((data.ranked ?? []) as RankedEntry[]);
      })
      .catch((e: unknown) =>
        setError(e instanceof Error ? e.message : 'Failed to load bias map.'),
      )
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p className="text-sm opacity-70">Loading bias map…</p>;
  if (error) return <p className="text-sm text-rust">{error}</p>;
  if (ranked.length === 0)
    return (
      <p className="text-sm opacity-70">
        No bias flags yet. Upload some writing first — your ranked biases will
        appear here.
      </p>
    );

  const max = Math.max(...ranked.map((r) => r.count), 1);

  return (
    <ul className="flex flex-col gap-3">
      {ranked.map((r) => (
        <li key={r.bias_type} className="rounded border border-sand bg-white p-3">
          <button
            className="flex w-full items-center justify-between text-left"
            onClick={() => setOpen(open === r.bias_type ? null : r.bias_type)}
          >
            <span className="font-bold text-charcoal">
              {r.bias_type.replace(/_/g, ' ')}
            </span>
            <span className="mono-n text-sm text-charcoal">×{r.count}</span>
          </button>
          <div className="mt-2 h-2 rounded bg-sand">
            <div
              className="h-2 rounded bg-rust"
              style={{ width: `${Math.round((r.count / max) * 100)}%` }}
            />
          </div>
          {open === r.bias_type && (
            <ul className="mt-2 flex flex-col gap-2">
              {r.examples.map((ex, i) => (
                <li
                  key={i}
                  className="border-l-4 border-rust bg-cream px-3 py-2 text-sm italic text-charcoal"
                >
                  “{ex}”
                </li>
              ))}
            </ul>
          )}
        </li>
      ))}
    </ul>
  );
}
