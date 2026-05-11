import { useState, useEffect } from "react";
import { AuthProvider, useAuth } from "./context/AuthContext";
import Login from "./pages/Login";
import Home from "./pages/Home";
import IncidentForm from "./pages/IncidentForm";
import IncidentDetail from "./pages/IncidentDetail";
import Dashboard from "./pages/Dashboard";
import Analytics from "./pages/Analytics";
import ProtectedRoute from "./components/ProtectedRoute";
import FileUpload from "./components/FileUpload";

function AppContent() {
  const { user, logout } = useAuth();
  const [currentPage, setCurrentPage] = useState("home");
  const [editId, setEditId] = useState(null);
  const [detailId, setDetailId] = useState(null);
  const [menuOpen, setMenuOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(window.innerWidth < 600);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 600);
      if (window.innerWidth >= 600) setMenuOpen(false);
    };
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const navigateTo = (page, id = null) => {
    setCurrentPage(page);
    setMenuOpen(false);
    if (page === "edit") setEditId(id);
    if (page === "detail") setDetailId(id);
  };

  if (!user) {
    return <Login onSuccess={() => navigateTo("home")} />;
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navbar */}
      <nav className="bg-blue-800 text-white px-6 py-4">
        <div className="flex justify-between items-center">
          <h1 className="text-lg font-bold">
            Incident Timeline Visualiser
          </h1>

          {/* Hamburger Button - Mobile Only */}
          {isMobile && (
            <button
              onClick={() => setMenuOpen(!menuOpen)}
              className="focus:outline-none text-2xl"
            >
              {menuOpen ? "✕" : "☰"}
            </button>
          )}

          {/* Desktop Menu */}
          {!isMobile && (
            <div className="flex space-x-4 items-center">
              <button
                onClick={() => navigateTo("home")}
                className="hover:underline"
              >
                Home
              </button>
              <button
                onClick={() => navigateTo("dashboard")}
                className="hover:underline"
              >
                Dashboard
              </button>
              <button
                onClick={() => navigateTo("analytics")}
                className="hover:underline"
              >
                Analytics
              </button>
              <button
                onClick={() => navigateTo("upload")}
                className="hover:underline"
              >
                Upload
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
          )}
        </div>

        {/* Mobile Menu */}
        {isMobile && menuOpen && (
          <div className="mt-4 flex flex-col space-y-3">
            <button
              onClick={() => navigateTo("home")}
              className="text-left py-2 border-b border-blue-700"
            >
              Home
            </button>
            <button
              onClick={() => navigateTo("dashboard")}
              className="text-left py-2 border-b border-blue-700"
            >
              Dashboard
            </button>
            <button
              onClick={() => navigateTo("analytics")}
              className="text-left py-2 border-b border-blue-700"
            >
              Analytics
            </button>
            <button
              onClick={() => navigateTo("upload")}
              className="text-left py-2 border-b border-blue-700"
            >
              Upload
            </button>
            <button
              onClick={() => navigateTo("create")}
              className="text-left bg-white text-blue-800 px-4 py-2 rounded font-medium"
            >
              + New Incident
            </button>
            <button
              onClick={logout}
              className="text-left bg-red-500 text-white px-4 py-2 rounded font-medium"
            >
              Logout
            </button>
          </div>
        )}
      </nav>

      {/* Pages */}
      <ProtectedRoute>
        {currentPage === "home" && (
          <Home
            onEdit={(id) => navigateTo("edit", id)}
            onView={(id) => navigateTo("detail", id)}
          />
        )}
        {currentPage === "dashboard" && <Dashboard />}
        {currentPage === "analytics" && <Analytics />}
        {currentPage === "upload" && (
          <div className="max-w-2xl mx-auto mt-8 px-6">
            <h1 className="text-2xl font-bold text-blue-800 mb-6">
              Upload File
            </h1>
            <FileUpload />
          </div>
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
        {currentPage === "detail" && (
          <IncidentDetail
            incidentId={detailId}
            onEdit={(id) => navigateTo("edit", id)}
            onBack={() => navigateTo("home")}
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