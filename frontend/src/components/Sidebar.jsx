import { Link } from "react-router-dom";

function Sidebar() {
  return (
    <div className="w-64 bg-gray-800 text-white h-screen p-5">
      <h2 className="text-xl font-bold mb-6">Resume App</h2>

      <ul className="space-y-4">
        <li>
          <Link to="/dashboard">📊 Dashboard</Link>
        </li>

        <li>
          <Link to="/analyze">📂 Analyze Resume</Link>
        </li>

        <li>
          <button
                    onClick={() => {
          localStorage.removeItem("token");
          window.location.href = "/";
        }}
          >
            🚪 Logout
          </button>
        </li>
      </ul>
    </div>
  );
}

export default Sidebar;