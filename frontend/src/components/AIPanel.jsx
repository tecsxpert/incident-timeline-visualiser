import { useState } from "react";
import API from "../services/api";

export default function AIPanel({ incidentId }) {
  const [aiDescription, setAiDescription] = useState("");
  const [aiRecommendations, setAiRecommendations] = useState([]);
  const [aiReport, setAiReport] = useState(null);
  const [loadingDesc, setLoadingDesc] = useState(false);
  const [loadingRec, setLoadingRec] = useState(false);
  const [loadingReport, setLoadingReport] = useState(false);
  const [error, setError] = useState("");

  const handleDescribe = async () => {
    setLoadingDesc(true);
    setError("");
    try {
      const res = await API.post(`/api/incidents/${incidentId}/describe`);
      setAiDescription(res.data.ai_description || res.data);
    } catch {
      setError("Failed to get AI description. Please try again.");
    }
    setLoadingDesc(false);
  };

  const handleRecommend = async () => {
    setLoadingRec(true);
    setError("");
    try {
      const res = await API.post(`/api/incidents/${incidentId}/recommend`);
      setAiRecommendations(res.data || []);
    } catch {
      setError("Failed to get AI recommendations. Please try again.");
    }
    setLoadingRec(false);
  };

  const handleReport = async () => {
    setLoadingReport(true);
    setError("");
    try {
      const res = await API.post(`/api/incidents/${incidentId}/report`);
      setAiReport(res.data);
    } catch {
      setError("Failed to generate AI report. Please try again.");
    }
    setLoadingReport(false);
  };

  return (
    <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mt-6">
      <h2 className="text-xl font-bold text-blue-800 mb-4">
        🤖 AI Assistant
      </h2>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded mb-4 text-sm">
          {error}
        </div>
      )}

      {/* AI Action Buttons */}
      <div className="flex gap-3 mb-6 flex-wrap">
        <button
          onClick={handleDescribe}
          disabled={loadingDesc}
          className="bg-blue-800 text-white px-4 py-2 rounded hover:bg-blue-700 transition flex items-center gap-2"
        >
          {loadingDesc ? (
            <>
              <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"/>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
              </svg>
              Describing...
            </>
          ) : "🔍 AI Describe"}
        </button>

        <button
          onClick={handleRecommend}
          disabled={loadingRec}
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition flex items-center gap-2"
        >
          {loadingRec ? (
            <>
              <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"/>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
              </svg>
              Getting recommendations...
            </>
          ) : "💡 AI Recommend"}
        </button>

        <button
          onClick={handleReport}
          disabled={loadingReport}
          className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700 transition flex items-center gap-2"
        >
          {loadingReport ? (
            <>
              <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"/>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
              </svg>
              Generating report...
            </>
          ) : "📋 Generate Report"}
        </button>
      </div>

      {/* AI Description */}
      {aiDescription && (
        <div className="bg-white rounded-lg p-4 mb-4 border border-blue-100">
          <h3 className="font-bold text-blue-800 mb-2">
            🔍 AI Description
          </h3>
          <p className="text-gray-700">{aiDescription}</p>
        </div>
      )}

      {/* AI Recommendations */}
      {aiRecommendations.length > 0 && (
        <div className="bg-white rounded-lg p-4 mb-4 border border-green-100">
          <h3 className="font-bold text-green-700 mb-3">
            💡 AI Recommendations
          </h3>
          <div className="space-y-3">
            {aiRecommendations.map((rec, index) => (
              <div
                key={index}
                className="border-l-4 border-green-400 pl-3 py-1"
              >
                <div className="flex justify-between items-start">
                  <p className="font-medium text-gray-800">
                    {rec.action_type || `Recommendation ${index + 1}`}
                  </p>
                  <span className={`text-xs px-2 py-1 rounded font-medium
                    ${rec.priority === 'HIGH' ? 'bg-red-100 text-red-700' :
                      rec.priority === 'MEDIUM' ? 'bg-yellow-100 text-yellow-700' :
                      'bg-green-100 text-green-700'}`}>
                    {rec.priority || 'MEDIUM'}
                  </span>
                </div>
                <p className="text-gray-600 text-sm mt-1">{rec.description}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* AI Report */}
      {aiReport && (
        <div className="bg-white rounded-lg p-4 border border-purple-100">
          <h3 className="font-bold text-purple-700 mb-3">
            📋 AI Generated Report
          </h3>
          {aiReport.title && (
            <h4 className="font-bold text-gray-800 mb-2">{aiReport.title}</h4>
          )}
          {aiReport.summary && (
            <div className="mb-3">
              <p className="text-sm font-medium text-gray-500">Summary</p>
              <p className="text-gray-700">{aiReport.summary}</p>
            </div>
          )}
          {aiReport.overview && (
            <div className="mb-3">
              <p className="text-sm font-medium text-gray-500">Overview</p>
              <p className="text-gray-700">{aiReport.overview}</p>
            </div>
          )}
          {aiReport.recommendations && (
            <div>
              <p className="text-sm font-medium text-gray-500 mb-1">
                Recommendations
              </p>
              <ul className="list-disc list-inside space-y-1">
                {aiReport.recommendations.map((r, i) => (
                  <li key={i} className="text-gray-700 text-sm">{r}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

    </div>
  );
}