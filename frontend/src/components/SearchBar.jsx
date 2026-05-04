import { useState, useEffect } from "react";

export default function SearchBar({ onSearch, onStatusFilter, onDateFilter }) {
  const [searchTerm, setSearchTerm] = useState("");
  const [status, setStatus] = useState("");
  const [fromDate, setFromDate] = useState("");
  const [toDate, setToDate] = useState("");

  // Debounced search — waits 500ms after user stops typing
  useEffect(() => {
    const timer = setTimeout(() => {
      onSearch(searchTerm);
    }, 500);
    return () => clearTimeout(timer);
  }, [searchTerm]);

  const handleStatusChange = (e) => {
    setStatus(e.target.value);
    onStatusFilter(e.target.value);
  };

  const handleDateFilter = () => {
    onDateFilter(fromDate, toDate);
  };

  const handleClear = () => {
    setSearchTerm("");
    setStatus("");
    setFromDate("");
    setToDate("");
    onSearch("");
    onStatusFilter("");
    onDateFilter("", "");
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow mb-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">

        {/* Search Input */}
        <div className="md:col-span-2">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Search
          </label>
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search by title, type, reported by..."
            className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Status Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Status
          </label>
          <select
            value={status}
            onChange={handleStatusChange}
            className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Statuses</option>
            <option value="OPEN">OPEN</option>
            <option value="IN_PROGRESS">IN PROGRESS</option>
            <option value="RESOLVED">RESOLVED</option>
            <option value="CLOSED">CLOSED</option>
          </select>
        </div>

        {/* Clear Button */}
        <div className="flex items-end">
          <button
            onClick={handleClear}
            className="w-full bg-gray-500 text-white py-2 px-4 rounded hover:bg-gray-600 transition"
          >
            Clear Filters
          </button>
        </div>

        {/* Date Range */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            From Date
          </label>
          <input
            type="date"
            value={fromDate}
            onChange={(e) => setFromDate(e.target.value)}
            className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            To Date
          </label>
          <input
            type="date"
            value={toDate}
            onChange={(e) => setToDate(e.target.value)}
            className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Apply Date Filter */}
        <div className="flex items-end">
          <button
            onClick={handleDateFilter}
            className="w-full bg-blue-800 text-white py-2 px-4 rounded hover:bg-blue-700 transition"
          >
            Apply Date Filter
          </button>
        </div>

      </div>
    </div>
  );
}