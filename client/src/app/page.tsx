"use client";

import { useState } from "react";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleSubmit = async () => {
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setResult(data);
    } catch (error) {
      alert("Something went wrong. Try again.");
    }

    setLoading(false);
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return "bg-green-100 text-green-800";
    if (score >= 50) return "bg-yellow-100 text-yellow-800";
    return "bg-red-100 text-red-800";
  };

  const renderContent = (val: any) => {
    if (typeof val === "string") return val;
    if (typeof val === "object" && val?.content) return val.content;
    return JSON.stringify(val); // fallback for debugging
  };

  return (
    <main className="min-h-screen bg-gray-100 text-gray-900 px-4 py-8 flex flex-col items-center">
      <h1 className="text-4xl font-bold mb-4">📄 Resume Analyzer</h1>
      <p className="text-gray-600 mb-6 text-center max-w-xl">
        Upload your PDF resume and get ATS score, section breakdown, feedback, and suggestions to improve your resume.
      </p>

      <div className="w-full max-w-md flex flex-col items-center space-y-4">
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          className="w-full border border-gray-300 rounded px-3 py-2 bg-white"
        />

        <button
          onClick={handleSubmit}
          disabled={!file || loading}
          className="bg-blue-600 text-white w-full px-4 py-2 rounded hover:bg-blue-700 transition disabled:opacity-50"
        >
          {loading ? "Analyzing..." : "Upload & Analyze"}
        </button>
      </div>

      {/* Results */}
      {result && (
        <div className="mt-10 w-full max-w-4xl bg-white p-6 rounded-lg shadow space-y-6">
          {/* ATS Score */}
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-semibold">ATS Score</h2>
            <span
              className={`text-lg font-bold px-4 py-1 rounded-full ${getScoreColor(result.ats_score)}`}
            >
              {result.ats_score} / 100
            </span>
          </div>

          {/* Sections */}
          {result.llm_analysis?.sections && (
            <div>
              <h3 className="text-xl font-semibold mb-2">📂 Resume Sections</h3>
              <div className="space-y-2">
                {Object.entries(result.llm_analysis.sections).map(([key, val]) => (
                  <div key={key} className="border border-gray-200 rounded p-3 bg-gray-50">
                    <p className="font-semibold">{key}</p>
                    <p className="text-sm mt-1 whitespace-pre-wrap">{renderContent(val)}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* LLM Analysis */}
          {result.llm_analysis?.analysis && (
            <div>
              <h3 className="text-xl font-semibold mb-2">🧠 Section-wise Analysis</h3>
              <div className="space-y-2">
                {Object.entries(result.llm_analysis.analysis).map(([key, val]) => (
                  <div key={key} className="border border-gray-200 rounded p-3 bg-gray-50">
                    <p className="font-semibold">{key}</p>
                    <p className="text-sm mt-1 whitespace-pre-wrap">{renderContent(val)}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Suggestions */}
          {result.llm_analysis?.suggestions?.length > 0 && (
            <div>
              <h3 className="text-xl font-semibold mb-2">✅ Suggestions to Improve</h3>
              <ul className="list-disc list-inside space-y-1 text-sm text-gray-800">
                {result.llm_analysis.suggestions.map((s: string, i: number) => (
                  <li key={i}>{s}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </main>
  );
}
