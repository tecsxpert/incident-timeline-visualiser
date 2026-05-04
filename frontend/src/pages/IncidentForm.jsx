import { useState, useEffect } from "react";
import API from "../services/api";

export default function IncidentForm({ incidentId, onSuccess }) {
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    incidentType: "",
    severity: "LOW",
    status: "OPEN",
    reportedBy: "",
    assignedTo: "",
    incidentDate: "",
    resolutionNotes: "",
  });

  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  // If editing, load existing data
  useEffect(() => {
    if (incidentId) {
      API.get(`/api/incidents/${incidentId}`)
        .then((res) => setFormData(res.data))
        .catch(() => setMessage("Failed to load incident data."));
    }
  }, [incidentId]);

  // Validate form
  const validate = () => {
    const newErrors = {};
    if (!formData.title.trim()) newErrors.title = "Title is required";
    if (!formData.incidentType.trim()) newErrors.incidentType = "Incident type is required";
    if (!formData.reportedBy.trim()) newErrors.reportedBy = "Reported by is required";
    if (!formData.incidentDate) newErrors.incidentDate = "Incident date is required";
    return newErrors;
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setErrors({ ...errors, [e.target.name]: "" });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const validationErrors = validate();
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setLoading(true);
    try {
      if (incidentId) {
        await API.put(`/api/incidents/${incidentId}`, formData);
        setMessage("✅ Incident updated successfully!");
      } else {
        await API.post("/api/incidents/create", formData);
        setMessage("✅ Incident created successfully!");
      }
      if (onSuccess) onSuccess();
    } catch {
      setMessage("❌ Failed to save incident. Please try again.");
    }
    setLoading(false);
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow mt-8">
      <h2 className="text-2xl font-bold text-blue-800 mb-6">
        {incidentId ? "Edit Incident" : "Create New Incident"}
      </h2>

      {message && (
        <p className="mb-4 text-sm font-medium text-center">{message}</p>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">

        {/* Title */}
        <div>
          <label className="block text-sm font-medium text-gray-700">Title *</label>
          <input
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            className="mt-1 w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter incident title"
          />
          {errors.title && <p className="text-red-500 text-sm mt-1">{errors.title}</p>}
        </div>

        {/* Description */}
        <div>
          <label className="block text-sm font-medium text-gray-700">Description</label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows={3}
            className="mt-1 w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Describe the incident"
          />
        </div>

        {/* Incident Type */}
        <div>
          <label className="block text-sm font-medium text-gray-700">Incident Type *</label>
          <input
            type="text"
            name="incidentType"
            value={formData.incidentType}
            onChange={handleChange}
            className="mt-1 w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="e.g. Security, Network, Hardware"
          />
          {errors.incidentType && <p className="text-red-500 text-sm mt-1">{errors.incidentType}</p>}
        </div>

        {/* Severity and Status */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Severity *</label>
            <select
              name="severity"
              value={formData.severity}
              onChange={handleChange}
              className="mt-1 w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="LOW">LOW</option>
              <option value="MEDIUM">MEDIUM</option>
              <option value="HIGH">HIGH</option>
              <option value="CRITICAL">CRITICAL</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Status *</label>
            <select
              name="status"
              value={formData.status}
              onChange={handleChange}
              className="mt-1 w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="OPEN">OPEN</option>
              <option value="IN_PROGRESS">IN PROGRESS</option>
              <option value="RESOLVED">RESOLVED</option>
              <option value="CLOSED">CLOSED</option>
            </select>
          </div>
        </div>

        {/* Reported By */}
        <div>
          <label className="block text-sm font-medium text-gray-700">Reported By *</label>
          <input
            type="text"
            name="reportedBy"
            value={formData.reportedBy}
            onChange={handleChange}
            className="mt-1 w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Your name"
          />
          {errors.reportedBy && <p className="text-red-500 text-sm mt-1">{errors.reportedBy}</p>}
        </div>

        {/* Assigned To */}
        <div>
          <label className="block text-sm font-medium text-gray-700">Assigned To</label>
          <input
            type="text"
            name="assignedTo"
            value={formData.assignedTo}
            onChange={handleChange}
            className="mt-1 w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Assignee name"
          />
        </div>

        {/* Incident Date */}
        <div>
          <label className="block text-sm font-medium text-gray-700">Incident Date *</label>
          <input
            type="datetime-local"
            name="incidentDate"
            value={formData.incidentDate}
            onChange={handleChange}
            className="mt-1 w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          {errors.incidentDate && <p className="text-red-500 text-sm mt-1">{errors.incidentDate}</p>}
        </div>

        {/* Resolution Notes */}
        <div>
          <label className="block text-sm font-medium text-gray-700">Resolution Notes</label>
          <textarea
            name="resolutionNotes"
            value={formData.resolutionNotes}
            onChange={handleChange}
            rows={3}
            className="mt-1 w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="How was this resolved?"
          />
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-800 text-white py-2 px-4 rounded hover:bg-blue-700 transition duration-200 font-medium"
        >
          {loading ? "Saving..." : incidentId ? "Update Incident" : "Create Incident"}
        </button>

      </form>
    </div>
  );
}