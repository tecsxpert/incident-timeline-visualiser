import { useState } from "react";
import { AuthProvider, useAuth } from "./context/AuthContext";
import Login from "./pages/Login";
import Home from "./pages/Home";
import IncidentForm from "./pages/IncidentForm";
import ProtectedRoute from "./components/ProtectedRoute";

function AppContent() {
  const { user, logout } = useAuth();
  const [currentPage, setCurrentPage] = useState("home");
  const [editId, setEditId] = useState(null);

  const navigateTo = (page, id = null) => {
    setCurrentPage(page);
    setEditId(id);
  };

  // If not logged in → show login page
  if (!user) {
    return <Login onSuccess={() => navigateTo("home")} />;
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navbar */}
      <nav className="bg-blue-800 text-white px-6 py-4 flex justify-between items-center">
        <h1 className="text-xl font-bold">Incident Timeline Visualiser</h1>
        <div className="space-x-4 flex items-center">
          <button
            onClick={() => navigateTo("home")}
            className="hover:underline"
          >
            Home
          </button>
          <button
            onClick={() => navigateTo("create")}
            className="bg-white text-blue-800 px-4 py-1 rounded font-medium hover:bg-gray-100"
          >
            + New Incident
          </button>
          <button
            onClick={logout}
            className="bg-red-500 text-white px-4 py-1 rounded font-medium hover:bg-red-600"
          >
            Logout
          </button>
        </div>
      </nav>

      {/* Pages */}
      <ProtectedRoute>
        {currentPage === "home" && (
          <Home onEdit={(id) => navigateTo("edit", id)} />
        )}
        {currentPage === "create" && (
          <IncidentForm onSuccess={() => navigateTo("home")} />
        )}
        {currentPage === "edit" && (
          <IncidentForm
            incidentId={editId}
            onSuccess={() => navigateTo("home")}
          />
        )}
      </ProtectedRoute>
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
