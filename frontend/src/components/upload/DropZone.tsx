import { useState } from 'react';
import { apiGet, apiUpload } from '../../lib/apiClient';

interface FileStatus {
  name: string;
  stage: 'uploading' | 'analysing' | 'done' | 'error';
  chunks?: number;
  biases?: number;
  message?: string;
}

export default function DropZone() {
  const [files, setFiles] = useState<FileStatus[]>([]);
  const [dragOver, setDragOver] = useState(false);
  const [error, setError] = useState('');

  async function uploadOne(file: File) {
    setFiles((prev) => [...prev, { name: file.name, stage: 'uploading' }]);
    try {
      // Upload bytes; backend chunks + embeds immediately.
      await apiUpload('/api/documents/upload', file);
      setFiles((prev) =>
        prev.map((f) =>
          f.name === file.name && f.stage === 'uploading'
            ? { ...f, stage: 'analysing' }
            : f,
        ),
      );
      // Re-fetch document row to report chunk/bias counts for this file.
      const docs: unknown = await apiGet('/api/documents');
      const list = Array.isArray(docs) ? docs : [];
      const match = list.find(
        (d: { filename?: string }) => d.filename === file.name,
      ) as { chunks?: number; biases?: number } | undefined;
      setFiles((prev) =>
        prev.map((f) =>
          f.name === file.name && f.stage === 'analysing'
            ? {
                ...f,
                stage: 'done',
                chunks: match?.chunks,
                biases: match?.biases,
              }
            : f,
        ),
      );
    } catch (e: unknown) {
      setFiles((prev) =>
        prev.map((f) =>
          f.name === file.name && f.stage !== 'done'
            ? {
                ...f,
                stage: 'error',
                message: e instanceof Error ? e.message : 'Upload failed.',
              }
            : f,
        ),
      );
    }
  }

  function handleFiles(list: FileList | File[]) {
    setError('');
    const arr = Array.from(list);
    const bad = arr.find((f) => !/\.(txt|md|pdf)$/i.test(f.name));
    if (bad) {
      setError(`Unsupported file type: ${bad.name} (use .txt/.md/.pdf).`);
      return;
    }
    for (const f of arr) void uploadOne(f);
  }

  return (
    <div>
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setDragOver(true);
        }}
        onDragLeave={() => setDragOver(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDragOver(false);
          if (e.dataTransfer.files.length > 0) handleFiles(e.dataTransfer.files);
        }}
        className={`rounded border-2 border-dashed p-8 text-center ${
          dragOver ? 'border-rust bg-sand' : 'border-sand bg-white'
        }`}
      >
        <p className="text-charcoal">
          Drag &amp; drop your writing here, or{' '}
          <label className="cursor-pointer font-bold text-rust underline">
            browse files
            <input
              type="file"
              multiple
              accept=".txt,.md,.pdf"
              className="hidden"
              onChange={(e) => {
                if (e.target.files) handleFiles(e.target.files);
                e.target.value = '';
              }}
            />
          </label>
        </p>
        <p className="mt-2 text-sm opacity-70">.txt, .md, .pdf — multiple files OK</p>
      </div>
      {error && <p className="mt-3 text-sm text-rust">{error}</p>}
      <ul className="mt-4 flex flex-col gap-2">
        {files.map((f, index) => (
          <li key={`${f.name}-${index}`} className="rounded border border-sand bg-white px-3 py-2 text-sm">
            <span className="font-bold">{f.name}</span>{' '}
            <span className="opacity-70">
              {f.stage === 'uploading' && 'uploading…'}
              {f.stage === 'analysing' && 'analysing…'}
              {f.stage === 'done' &&
                `done${f.chunks !== undefined ? ` — ${f.chunks} chunks` : ''}${
                  f.biases !== undefined ? `, ${f.biases} bias flags` : ''
                }`}
              {f.stage === 'error' && `error: ${f.message ?? 'upload failed'}`}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}
