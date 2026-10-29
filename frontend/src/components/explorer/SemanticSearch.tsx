import { useState } from 'react';
import { apiGet } from '../../lib/apiClient';

interface SearchResult {
  chunk_id: number;
  document: string;
  snippet: string;
  score: number;
  biases: string[];
}

export default function SemanticSearch() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [searched, setSearched] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function run(e?: React.FormEvent) {
    e?.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    setError('');
    try {
      const data = await apiGet(
        `/api/search?q=${encodeURIComponent(query)}&k=8`,
      );
      setResults((data.results ?? []) as SearchResult[]);
      setSearched(true);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Search failed.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <form onSubmit={run} className="flex flex-col gap-2 sm:flex-row">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search a topic, e.g. risk or teamwork"
          className="flex-1 rounded border border-sand bg-white px-3 py-2 text-charcoal"
        />
        <button
          type="submit"
          disabled={loading}
          className="rounded bg-rust px-4 py-2 font-bold text-cream disabled:opacity-50"
        >
          {loading ? 'Searching…' : 'Search'}
        </button>
      </form>
      {error && <p className="mt-3 text-sm text-rust">{error}</p>}
      {searched && !error && results.length === 0 && (
        <p className="mt-3 text-sm text-soft">No matching passages found.</p>
      )}
      <ul className="mt-4 flex flex-col gap-3">
        {results.map((r) => (
          <li key={r.chunk_id} className="rounded border border-sand bg-white p-3">
            <p className="text-sm text-charcoal">{r.snippet}</p>
            <div className="mt-2 flex flex-wrap items-center gap-2 text-xs">
              <span className="mono-n text-soft">{r.document}</span>
              <span className="mono-n text-soft">
                score {r.score.toFixed(3)}
              </span>
              {r.biases.map((b) => (
                <span
                  key={b}
                  className="rounded bg-sand px-2 py-0.5 font-bold text-rust"
                >
                  {b.replace(/_/g, ' ')}
                </span>
              ))}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
