import { useEffect, useState } from "react";
import API from "../services/api";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer,
  LineChart, Line, PieChart, Pie, Cell
} from "recharts";

const COLORS = ["#1B4F8A", "#F59E0B", "#10B981", "#EF4444"];

export default function Analytics() {
  const [period, setPeriod] = useState("30");
  const [severityData, setSeverityData] = useState([]);
  const [statusData, setStatusData] = useState([]);
  const [timelineData, setTimelineData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    API.get(`/api/incidents/analytics?period=${period}`)
      .then((res) => {
        setSeverityData(res.data.bySeverity || []);
        setStatusData(res.data.byStatus || []);
        setTimelineData(res.data.timeline || []);
        setLoading(false);
      })
      .catch(() => {
        // Use dummy data if backend not available
        setSeverityData([
          { name: "LOW", value: 0 },
          { name: "MEDIUM", value: 0 },
          { name: "HIGH", value: 0 },
          { name: "CRITICAL", value: 0 },
        ]);
        setStatusData([
          { name: "Open", value: 0 },
          { name: "In Progress", value: 0 },
          { name: "Resolved", value: 0 },
          { name: "Closed", value: 0 },
        ]);
        setTimelineData([]);
        setLoading(false);
      });
  }, [period]);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <p className="text-gray-500 text-lg">Loading analytics...</p>
      </div>
    );
  }

  return (
    <div className="p-6">

      {/* Header with Period Selector */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-blue-800">
          Analytics
        </h1>
        <div className="flex items-center gap-2">
          <label className="text-sm font-medium text-gray-700">
            Period:
          </label>
          <select
            value={period}
            onChange={(e) => setPeriod(e.target.value)}
            className="border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="7">Last 7 days</option>
            <option value="30">Last 30 days</option>
            <option value="90">Last 90 days</option>
          </select>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        {/* Incidents by Severity */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-bold text-gray-700 mb-4">
            Incidents by Severity
          </h2>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={severityData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="value" name="Incidents">
                {severityData.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={COLORS[index % COLORS.length]}
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Incidents by Status - Pie Chart */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-bold text-gray-700 mb-4">
            Incidents by Status
          </h2>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={statusData}
                cx="50%"
                cy="50%"
                outerRadius={80}
                dataKey="value"
                nameKey="name"
                label={({ name, value }) => `${name}: ${value}`}
              >
                {statusData.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={COLORS[index % COLORS.length]}
                  />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Incidents Timeline - Line Chart */}
        <div className="bg-white rounded-lg shadow p-6 md:col-span-2">
          <h2 className="text-lg font-bold text-gray-700 mb-4">
            Incidents Over Time
          </h2>
          {timelineData.length === 0 ? (
            <div className="text-center py-10">
              <p className="text-gray-400">
                No timeline data available yet.
              </p>
              <p className="text-gray-300 text-sm mt-1">
                Data will appear when backend is connected.
              </p>
            </div>
          ) : (
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={timelineData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="count"
                  stroke="#1B4F8A"
                  name="Incidents"
                  strokeWidth={2}
                />
              </LineChart>
            </ResponsiveContainer>
          )}
        </div>

      </div>
    </div>
  );
}