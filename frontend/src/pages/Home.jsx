import { useEffect, useState } from "react";
import API from "../services/api";
import SearchBar from "../components/SearchBar";

export default function Home({ onEdit, onView }) {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(0);
  const [totalPages, setTotalPages] = useState(0);
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [fromDate, setFromDate] = useState("");
  const [toDate, setToDate] = useState("");

  const handleExportCSV = async () => {
    try {
      const res = await API.get("/api/incidents/export", {
        responseType: "blob",
      });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "incidents.csv");
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch {
      alert("Export failed. Please try again when backend is running.");
    }
  };

  const fetchIncidents = (pageNum = 0) => {
    setLoading(true);

    let url = `/api/incidents/all?page=${pageNum}&size=10`;

    if (searchTerm) url = `/api/incidents/search?q=${searchTerm}&page=${pageNum}&size=10`;
    if (statusFilter) url += `&status=${statusFilter}`;
    if (fromDate) url += `&from=${fromDate}`;
    if (toDate) url += `&to=${toDate}`;

    API.get(url)
      .then((res) => {
        if (res.data.content) {
          setIncidents(res.data.content);
          setTotalPages(res.data.totalPages);
        } else {
          setIncidents(res.data);
        }
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load incidents.");
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchIncidents(page);
  }, [page, searchTerm, statusFilter, fromDate, toDate]);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <p className="text-gray-500 text-lg">Loading incidents...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold text-blue-800">
            All Incidents
          </h1>
          <button
            onClick={handleExportCSV}
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition flex items-center gap-2"
          >
            📥 Export CSV
          </button>
        </div>
        <SearchBar
          onSearch={(term) => { setSearchTerm(term); setPage(0); }}
          onStatusFilter={(status) => { setStatusFilter(status); setPage(0); }}
          onDateFilter={(from, to) => { setFromDate(from); setToDate(to); setPage(0); }}
        />
        <div className="text-center py-20">
          <p className="text-red-500 text-lg">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">

      {/* Header with Export Button */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-blue-800">
          All Incidents
        </h1>
        <button
          onClick={handleExportCSV}
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition flex items-center gap-2"
        >
          📥 Export CSV
        </button>
      </div>

      {/* Search Bar */}
      <SearchBar
        onSearch={(term) => { setSearchTerm(term); setPage(0); }}
        onStatusFilter={(status) => { setStatusFilter(status); setPage(0); }}
        onDateFilter={(from, to) => { setFromDate(from); setToDate(to); setPage(0); }}
      />

      {incidents.length === 0 ? (
        <div className="text-center py-20">
          <p className="text-gray-400 text-lg">No incidents found.</p>
          <p className="text-gray-300 text-sm mt-2">
            Create your first incident to get started.
          </p>
        </div>
      ) : (
        <>
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white border border-gray-200 rounded-lg shadow">
              <thead className="bg-blue-800 text-white">
                <tr>
                  <th className="px-4 py-3 text-left">ID</th>
                  <th className="px-4 py-3 text-left">Title</th>
                  <th className="px-4 py-3 text-left">Type</th>
                  <th className="px-4 py-3 text-left">Severity</th>
                  <th className="px-4 py-3 text-left">Status</th>
                  <th className="px-4 py-3 text-left">Reported By</th>
                  <th className="px-4 py-3 text-left">Date</th>
                  <th className="px-4 py-3 text-left">Actions</th>
                </tr>
              </thead>
              <tbody>
                {incidents.map((incident, index) => (
                  <tr
                    key={incident.id}
                    className={index % 2 === 0 ? "bg-white" : "bg-gray-50"}
                  >
                    <td className="px-4 py-3">{incident.id}</td>
                    <td className="px-4 py-3">{incident.title}</td>
                    <td className="px-4 py-3">{incident.incidentType}</td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-1 rounded text-sm font-medium
                        ${incident.severity === 'CRITICAL' ? 'bg-red-100 text-red-800' :
                          incident.severity === 'HIGH' ? 'bg-orange-100 text-orange-800' :
                          incident.severity === 'MEDIUM' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-green-100 text-green-800'}`}>
                        {incident.severity}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-1 rounded text-sm font-medium
                        ${incident.status === 'OPEN' ? 'bg-blue-100 text-blue-800' :
                          incident.status === 'IN_PROGRESS' ? 'bg-yellow-100 text-yellow-800' :
                          incident.status === 'RESOLVED' ? 'bg-green-100 text-green-800' :
                          'bg-gray-100 text-gray-800'}`}>
                        {incident.status}
                      </span>
                    </td>
                    <td className="px-4 py-3">{incident.reportedBy}</td>
                    <td className="px-4 py-3">
                      {new Date(incident.incidentDate).toLocaleDateString()}
                    </td>
                    <td className="px-4 py-3 flex gap-2">
                      <button
                        onClick={() => onView(incident.id)}
                        className="bg-gray-600 text-white px-3 py-1 rounded text-sm hover:bg-gray-700"
                      >
                        View
                      </button>
                      <button
                        onClick={() => onEdit(incident.id)}
                        className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700"
                      >
                        Edit
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex justify-center items-center mt-6 space-x-4">
              <button
                onClick={() => setPage(page - 1)}
                disabled={page === 0}
                className="px-4 py-2 bg-blue-800 text-white rounded disabled:opacity-50 hover:bg-blue-700"
              >
                Previous
              </button>
              <span className="text-gray-600">
                Page {page + 1} of {totalPages}
              </span>
              <button
                onClick={() => setPage(page + 1)}
                disabled={page === totalPages - 1}
                className="px-4 py-2 bg-blue-800 text-white rounded disabled:opacity-50 hover:bg-blue-700"
              >
                Next
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}