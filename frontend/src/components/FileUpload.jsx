import { useState } from "react";
import API from "../services/api";

export default function FileUpload() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const allowedTypes = [
    "image/jpeg",
    "image/png",
    "application/pdf",
    "text/csv",
  ];
  const maxSize = 5 * 1024 * 1024; // 5MB

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setMessage("");
    setError("");

    if (!selectedFile) return;

    // Validate file type
    if (!allowedTypes.includes(selectedFile.type)) {
      setError("❌ Invalid file type! Only JPG, PNG, PDF, CSV allowed.");
      setFile(null);
      return;
    }

    // Validate file size
    if (selectedFile.size > maxSize) {
      setError("❌ File too large! Maximum size is 5MB.");
      setFile(null);
      return;
    }

    setFile(selectedFile);
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file first!");
      return;
    }

    setUploading(true);
    setError("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      await API.post("/api/incidents/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setMessage("✅ File uploaded successfully!");
      setFile(null);
    } catch {
      setError("❌ Upload failed. Please try again when backend is running.");
    }
    setUploading(false);
  };

  return (
    <div className="bg-white rounded-lg shadow p-6 mt-6">
      <h2 className="text-xl font-bold text-blue-800 mb-4">
        📎 File Upload
      </h2>

      {/* Upload Area */}
      <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center mb-4">
        <input
          type="file"
          onChange={handleFileChange}
          accept=".jpg,.jpeg,.png,.pdf,.csv"
          className="hidden"
          id="fileInput"
        />
        <label
          htmlFor="fileInput"
          className="cursor-pointer"
        >
          <div className="text-4xl mb-2">📁</div>
          <p className="text-gray-600 font-medium">
            Click to select a file
          </p>
          <p className="text-gray-400 text-sm mt-1">
            JPG, PNG, PDF, CSV — Max 5MB
          </p>
        </label>
      </div>

      {/* Selected File Info */}
      {file && (
        <div className="bg-gray-50 rounded p-3 mb-4 flex justify-between items-center">
          <div>
            <p className="font-medium text-gray-800">{file.name}</p>
            <p className="text-sm text-gray-500">
              {(file.size / 1024).toFixed(1)} KB
            </p>
          </div>
          <button
            onClick={() => setFile(null)}
            className="text-red-500 hover:text-red-700"
          >
            ✕
          </button>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded mb-4 text-sm">
          {error}
        </div>
      )}

      {/* Success Message */}
      {message && (
        <div className="bg-green-50 border border-green-200 text-green-600 px-4 py-3 rounded mb-4 text-sm">
          {message}
        </div>
      )}

      {/* Upload Button */}
      <button
        onClick={handleUpload}
        disabled={uploading || !file}
        className="w-full bg-blue-800 text-white py-2 px-4 rounded hover:bg-blue-700 transition disabled:opacity-50 font-medium"
      >
        {uploading ? "Uploading..." : "Upload File"}
      </button>

      {/* Allowed Types Info */}
      <div className="mt-4 text-xs text-gray-400">
        <p>✅ Allowed: JPG, PNG, PDF, CSV</p>
        <p>✅ Maximum size: 5MB</p>
      </div>
    </div>
  );
}