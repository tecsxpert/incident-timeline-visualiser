import { useEffect, useState } from "react";
import API from "../services/api";
import AIPanel from "../components/AIPanel";

export default function IncidentDetail({ incidentId, onEdit, onBack }) {
  const [incident, setIncident] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [deleteMsg, setDeleteMsg] = useState("");

  useEffect(() => {
    API.get(`/api/incidents/${incidentId}`)
      .then((res) => {
        setIncident(res.data);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load incident details.");
        setLoading(false);
      });
  }, [incidentId]);

  const handleDelete = async () => {
    if (window.confirm("Are you sure you want to delete this incident?")) {
      try {
        await API.delete(`/api/incidents/${incidentId}`);
        setDeleteMsg("✅ Incident deleted successfully!");
        setTimeout(() => onBack(), 1500);
      } catch {
        setDeleteMsg("❌ Failed to delete incident.");
      }
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <p className="text-gray-500 text-lg">Loading incident details...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center h-screen">
        <p className="text-red-500 text-lg">{error}</p>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto p-6 mt-8">

      {/* Back Button */}
      <button
        onClick={onBack}
        className="mb-4 text-blue-800 hover:underline flex items-center gap-1"
      >
        ← Back to List
      </button>

      {deleteMsg && (
        <p className="mb-4 text-center font-medium">{deleteMsg}</p>
      )}

      <div className="bg-white rounded-lg shadow p-6">

        {/* Header */}
        <div className="flex justify-between items-start mb-6">
          <h1 className="text-2xl font-bold text-blue-800">
            {incident.title}
          </h1>
          {/* Score Badge */}
          <span className={`px-3 py-1 rounded-full text-sm font-bold
            ${incident.severity === 'CRITICAL' ? 'bg-red-100 text-red-800' :
              incident.severity === 'HIGH' ? 'bg-orange-100 text-orange-800' :
              incident.severity === 'MEDIUM' ? 'bg-yellow-100 text-yellow-800' :
              'bg-green-100 text-green-800'}`}>
            {incident.severity}
          </span>
        </div>

        {/* Details Grid */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div>
            <p className="text-sm text-gray-500">Incident Type</p>
            <p className="font-medium">{incident.incidentType}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Status</p>
            <span className={`px-2 py-1 rounded text-sm font-medium
              ${incident.status === 'OPEN' ? 'bg-blue-100 text-blue-800' :
                incident.status === 'IN_PROGRESS' ? 'bg-yellow-100 text-yellow-800' :
                incident.status === 'RESOLVED' ? 'bg-green-100 text-green-800' :
                'bg-gray-100 text-gray-800'}`}>
              {incident.status}
            </span>
          </div>
          <div>
            <p className="text-sm text-gray-500">Reported By</p>
            <p className="font-medium">{incident.reportedBy}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Assigned To</p>
            <p className="font-medium">
              {incident.assignedTo || "Not assigned"}
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Incident Date</p>
            <p className="font-medium">
              {new Date(incident.incidentDate).toLocaleString()}
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Resolved Date</p>
            <p className="font-medium">
              {incident.resolvedDate
                ? new Date(incident.resolvedDate).toLocaleString()
                : "Not resolved yet"}
            </p>
          </div>
        </div>

        {/* Description */}
        {incident.description && (
          <div className="mb-4">
            <p className="text-sm text-gray-500 mb-1">Description</p>
            <p className="text-gray-700 bg-gray-50 p-3 rounded">
              {incident.description}
            </p>
          </div>
        )}

        {/* Resolution Notes */}
        {incident.resolutionNotes && (
          <div className="mb-6">
            <p className="text-sm text-gray-500 mb-1">Resolution Notes</p>
            <p className="text-gray-700 bg-gray-50 p-3 rounded">
              {incident.resolutionNotes}
            </p>
          </div>
        )}

        {/* AI Description */}
        {incident.aiDescription && (
          <div className="mb-4 bg-blue-50 p-4 rounded">
            <p className="text-sm text-blue-800 font-medium mb-1">
              🤖 AI Description
            </p>
            <p className="text-gray-700">{incident.aiDescription}</p>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex gap-4 mt-6">
          <button
            onClick={() => onEdit(incident.id)}
            className="bg-blue-800 text-white px-6 py-2 rounded hover:bg-blue-700 transition"
          >
            ✏️ Edit Incident
          </button>
          <button
            onClick={handleDelete}
            className="bg-red-500 text-white px-6 py-2 rounded hover:bg-red-600 transition"
          >
            🗑️ Delete Incident
          </button>
        </div>

      </div>

      {/* AI Panel */}
      <AIPanel incidentId={incidentId} />

    </div>
  );
}