import React from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";

const StudentSidebar: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const menuItems = [
    {
      name: "Dashboard",
      path: "/student-dashboard",
      icon: "🏠",
    },
    {
      name: "My Subjects",
      path: "/subjects",
      icon: "📚",
    },
    {
      name: "AI Tutor",
      path: "/ai-tutor",
      icon: "🤖",
    },
    {
      name: "Learning Materials",
      path: "/materials",
      icon: "📖",
    },
    {
      name: "My Progress",
      path: "/progress",
      icon: "📊",
    },
    {
      name: "Assignments",
      path: "/assignments",
      icon: "📝",
    },
    {
      name: "Notifications",
      path: "/notifications",
      icon: "🔔",
    },
  ];

  return (
    <aside className="fixed left-0 top-0 z-40 flex h-screen w-64 flex-col border-r border-gray-200 bg-white">

      {/* Logo */}
      <div className="flex h-20 items-center border-b border-gray-200 px-6">
        <Link
          to="/student-dashboard"
          className="flex items-center gap-3"
        >
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-purple-600 font-bold text-white">
            AI
          </div>

          <div>
            <h1 className="text-xl font-bold text-gray-900">
              LearnAI
            </h1>

            <p className="text-xs text-gray-500">
              Student App
            </p>
          </div>
        </Link>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto px-4 py-6">

        <p className="mb-3 px-3 text-xs font-semibold uppercase tracking-wider text-gray-400">
          Main Menu
        </p>

        <div className="space-y-2">
          {menuItems.map((item) => {
            const isActive = location.pathname === item.path;

            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium transition ${
                  isActive
                    ? "bg-purple-100 text-purple-700"
                    : "text-gray-600 hover:bg-gray-100 hover:text-purple-600"
                }`}
              >
                <span className="text-lg">
                  {item.icon}
                </span>

                <span>
                  {item.name}
                </span>
              </Link>
            );
          })}
        </div>

        {/* Account */}
        <p className="mb-3 mt-8 px-3 text-xs font-semibold uppercase tracking-wider text-gray-400">
          Account
        </p>

        <div className="space-y-2">

          <Link
            to="/profile"
            className={`flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium transition ${
              location.pathname === "/profile"
                ? "bg-purple-100 text-purple-700"
                : "text-gray-600 hover:bg-gray-100 hover:text-purple-600"
            }`}
          >
            <span className="text-lg">👤</span>
            <span>Profile</span>
          </Link>

          <Link
            to="/settings"
            className={`flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium transition ${
              location.pathname === "/settings"
                ? "bg-purple-100 text-purple-700"
                : "text-gray-600 hover:bg-gray-100 hover:text-purple-600"
            }`}
          >
            <span className="text-lg">⚙️</span>
            <span>Settings</span>
          </Link>

        </div>
      </nav>

      {/* Logout */}
      <div className="border-t border-gray-200 p-4">

        <button
          type="button"
          onClick={() => navigate("/login")}
          className="flex w-full items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium text-red-500 transition hover:bg-red-50"
        >
          <span className="text-lg">🚪</span>

          <span>
            Logout
          </span>
        </button>

      </div>
    </aside>
  );
};

export default StudentSidebar;

