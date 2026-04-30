import { useAuth } from "../context/AuthContext";

export default function ProtectedRoute({ children }) {
  const { user } = useAuth();

  if (!user) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="text-center">
          <p className="text-red-500 text-lg font-medium">
            🔒 Access Denied!
          </p>
          <p className="text-gray-500 mt-2">
            Please login to access this page.
          </p>
        </div>
      </div>
    );
  }

  return children;
}