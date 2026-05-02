import { useEffect, useState } from "react";
import API from "../services/api";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer
} from "recharts";

export default function Dashboard() {
  const [stats, setStats] = useState({
    total: 0,
    open: 0,
    resolved: 0,
    critical: 0,
  });
  const [chartData, setChartData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    API.get("/api/incidents/stats")
      .then((res) => {
        setStats(res.data);
        setChartData([
          { name: "Open", value: res.data.open },
          { name: "In Progress", value: res.data.inProgress },
          { name: "Resolved", value: res.data.resolved },
          { name: "Closed", value: res.data.closed },
        ]);
        setLoading(false);
      })
      .catch(() => {
        // Use dummy data if backend not available
        setStats({
          total: 0,
          open: 0,
          resolved: 0,
          critical: 0,
        });
        setChartData([
          { name: "Open", value: 0 },
          { name: "In Progress", value: 0 },
          { name: "Resolved", value: 0 },
          { name: "Closed", value: 0 },
        ]);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <p className="text-gray-500 text-lg">Loading dashboard...</p>
      </div>
    );
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-blue-800 mb-6">Dashboard</h1>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        
        {/* Total Incidents */}
        <div className="bg-white rounded-lg shadow p-6 border-l-4 border-blue-800">
          <p className="text-sm text-gray-500">Total Incidents</p>
          <p className="text-3xl font-bold text-blue-800 mt-2">
            {stats.total}
          </p>
        </div>

        {/* Open Incidents */}
        <div className="bg-white rounded-lg shadow p-6 border-l-4 border-yellow-500">
          <p className="text-sm text-gray-500">Open Incidents</p>
          <p className="text-3xl font-bold text-yellow-500 mt-2">
            {stats.open}
          </p>
        </div>

        {/* Resolved Incidents */}
        <div className="bg-white rounded-lg shadow p-6 border-l-4 border-green-500">
          <p className="text-sm text-gray-500">Resolved Incidents</p>
          <p className="text-3xl font-bold text-green-500 mt-2">
            {stats.resolved}
          </p>
        </div>

        {/* Critical Incidents */}
        <div className="bg-white rounded-lg shadow p-6 border-l-4 border-red-500">
          <p className="text-sm text-gray-500">Critical Incidents</p>
          <p className="text-3xl font-bold text-red-500 mt-2">
            {stats.critical}
          </p>
        </div>

      </div>

      {/* Chart */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-bold text-gray-700 mb-4">
          Incidents by Status
        </h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="value" fill="#1B4F8A" name="Incidents" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}