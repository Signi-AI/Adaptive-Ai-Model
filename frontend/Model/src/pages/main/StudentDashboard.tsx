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

      {/* Menu */}
      <nav className="flex-1 overflow-y-auto px-4 py-6">
        <p className="mb-3 px-3 text-xs font-semibold uppercase tracking-wider text-gray-400">
          Main Menu
        </p>

        <div className="space-y-2">
          {menuItems.map((item) => {
            const active = location.pathname === item.path;

            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium transition ${
                  active
                    ? "bg-purple-100 text-purple-700"
                    : "text-gray-600 hover:bg-gray-100 hover:text-purple-600"
                }`}
              >
                <span className="text-lg">{item.icon}</span>
                <span>{item.name}</span>
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
          <span>Logout</span>
        </button>
      </div>
    </aside>
  );
};


const StudentDashboard: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">

      {/* Sidebar */}
      <StudentSidebar />

      {/* Main Content */}
      <main className="ml-64 min-h-screen">

        {/* Top Header */}
        <header className="sticky top-0 z-30 flex h-20 items-center justify-between border-b border-gray-200 bg-white px-8">
          
          <div>
            <h2 className="text-xl font-semibold text-gray-900">
              Dashboard
            </h2>
            <p className="text-sm text-gray-500">
              Your personalized learning space
            </p>
          </div>

          <div className="flex items-center gap-5">

            {/* Notification */}
            <Link
              to="/notifications"
              className="relative flex h-10 w-10 items-center justify-center rounded-full bg-gray-100 text-lg transition hover:bg-purple-100"
            >
              🔔
              <span className="absolute right-1 top-1 h-2.5 w-2.5 rounded-full bg-red-500" />
            </Link>

            {/* Student Profile */}
            <Link
              to="/profile"
              className="flex items-center gap-3"
            >
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-purple-600 font-semibold text-white">
                S
              </div>

              <div className="hidden md:block">
                <p className="text-sm font-semibold text-gray-900">
                  Student
                </p>
                <p className="text-xs text-gray-500">
                  Form 2
                </p>
              </div>
            </Link>

          </div>
        </header>

        {/* Dashboard Content */}
        <div className="space-y-8 p-8">

          {/* Welcome */}
          <section className="rounded-2xl bg-purple-600 p-8 text-white">
            <div className="max-w-2xl">
              <p className="mb-2 text-sm font-medium text-purple-200">
                Welcome back 👋
              </p>

              <h1 className="text-3xl font-bold">
                Ready to continue learning?
              </h1>

              <p className="mt-3 text-purple-100">
                Learn with your AI-powered personal learning assistant
                and improve your skills every day.
              </p>

              <Link
                to="/subjects"
                className="mt-6 inline-block rounded-lg bg-white px-5 py-3 font-semibold text-purple-600 transition hover:bg-gray-100"
              >
                Start Learning
              </Link>
            </div>
          </section>

          {/* Quick Stats */}
          <section className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">

            <div className="rounded-2xl border border-gray-200 bg-white p-6">
              <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-xl bg-purple-100 text-xl">
                📚
              </div>

              <p className="text-sm text-gray-500">
                Subjects
              </p>

              <h3 className="mt-1 text-2xl font-bold text-gray-900">
                6
              </h3>
            </div>

            <div className="rounded-2xl border border-gray-200 bg-white p-6">
              <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-xl bg-blue-100 text-xl">
                📖
              </div>

              <p className="text-sm text-gray-500">
                Lessons Completed
              </p>

              <h3 className="mt-1 text-2xl font-bold text-gray-900">
                24
              </h3>
            </div>

            <div className="rounded-2xl border border-gray-200 bg-white p-6">
              <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-xl bg-green-100 text-xl">
                📊
              </div>

              <p className="text-sm text-gray-500">
                Overall Progress
              </p>

              <h3 className="mt-1 text-2xl font-bold text-gray-900">
                68%
              </h3>
            </div>

            <div className="rounded-2xl border border-gray-200 bg-white p-6">
              <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-xl bg-orange-100 text-xl">
                🔥
              </div>

              <p className="text-sm text-gray-500">
                Learning Streak
              </p>

              <h3 className="mt-1 text-2xl font-bold text-gray-900">
                7 Days
              </h3>
            </div>

          </section>

          {/* Continue Learning */}
          <section>
            <div className="mb-5 flex items-center justify-between">
              <h2 className="text-xl font-bold text-gray-900">
                Continue Learning
              </h2>

              <Link
                to="/subjects"
                className="text-sm font-semibold text-purple-600 hover:text-purple-700"
              >
                View all
              </Link>
            </div>

            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">

              {/* Mathematics */}
              <div className="rounded-2xl border border-gray-200 bg-white p-6">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-4">
                    <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-purple-100 text-2xl">
                      📐
                    </div>

                    <div>
                      <h3 className="font-bold text-gray-900">
                        Mathematics
                      </h3>

                      <p className="text-sm text-gray-500">
                        Algebra
                      </p>
                    </div>
                  </div>

                  <span className="rounded-full bg-green-100 px-3 py-1 text-xs font-semibold text-green-600">
                    75%
                  </span>
                </div>

                <div className="mt-5">
                  <div className="mb-2 flex justify-between text-xs text-gray-500">
                    <span>
                      Introduction to Equations
                    </span>
                    <span>75%</span>
                  </div>

                  <div className="h-2 rounded-full bg-gray-200">
                    <div className="h-2 w-3/4 rounded-full bg-purple-600" />
                  </div>
                </div>

                <Link
                  to="/subjects"
                  className="mt-5 block rounded-lg bg-purple-600 py-3 text-center text-sm font-semibold text-white transition hover:bg-purple-700"
                >
                  Continue Learning
                </Link>
              </div>

              {/* Science */}
              <div className="rounded-2xl border border-gray-200 bg-white p-6">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-4">
                    <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-blue-100 text-2xl">
                      🔬
                    </div>

                    <div>
                      <h3 className="font-bold text-gray-900">
                        Science
                      </h3>

                      <p className="text-sm text-gray-500">
                        Biology
                      </p>
                    </div>
                  </div>

                  <span className="rounded-full bg-blue-100 px-3 py-1 text-xs font-semibold text-blue-600">
                    45%
                  </span>
                </div>

                <div className="mt-5">
                  <div className="mb-2 flex justify-between text-xs text-gray-500">
                    <span>
                      Human Body Systems
                    </span>
                    <span>45%</span>
                  </div>

                  <div className="h-2 rounded-full bg-gray-200">
                    <div className="h-2 w-[45%] rounded-full bg-blue-600" />
                  </div>
                </div>

                <Link
                  to="/subjects"
                  className="mt-5 block rounded-lg bg-blue-600 py-3 text-center text-sm font-semibold text-white transition hover:bg-blue-700"
                >
                  Continue Learning
                </Link>
              </div>

            </div>
          </section>

          {/* Bottom Section */}
          <section className="grid grid-cols-1 gap-6 lg:grid-cols-2">

            {/* AI Tutor */}
            <div className="rounded-2xl bg-gray-900 p-7 text-white">
              <div className="flex items-center gap-4">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-purple-600 text-2xl">
                  🤖
                </div>

                <div>
                  <h2 className="text-xl font-bold">
                    AI Tutor
                  </h2>

                  <p className="text-sm text-gray-400">
                    Need help with your studies?
                  </p>
                </div>
              </div>

              <p className="mt-5 text-sm leading-6 text-gray-300">
                Ask questions, get explanations, practice exercises,
                and receive personalized learning support from your AI tutor.
              </p>

              <Link
                to="/ai-tutor"
                className="mt-6 inline-block rounded-lg bg-purple-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-purple-700"
              >
                Ask AI Tutor
              </Link>
            </div>

            {/* Recent Activity */}
            <div className="rounded-2xl border border-gray-200 bg-white p-7">
              <h2 className="text-xl font-bold text-gray-900">
                Recent Activity
              </h2>

              <div className="mt-5 space-y-5">

                <div className="flex gap-4">
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-green-100">
                    ✓
                  </div>

                  <div>
                    <p className="text-sm font-medium text-gray-900">
                      Completed Algebra Lesson
                    </p>

                    <p className="mt-1 text-xs text-gray-500">
                      2 hours ago
                    </p>
                  </div>
                </div>

                <div className="flex gap-4">
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-purple-100">
                    🤖
                  </div>

                  <div>
                    <p className="text-sm font-medium text-gray-900">
                      Asked AI Tutor a question
                    </p>

                    <p className="mt-1 text-xs text-gray-500">
                      Yesterday
                    </p>
                  </div>
                </div>

                <div className="flex gap-4">
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-blue-100">
                    📝
                  </div>

                  <div>
                    <p className="text-sm font-medium text-gray-900">
                      Completed Science Quiz
                    </p>

                    <p className="mt-1 text-xs text-gray-500">
                      2 days ago
                    </p>
                  </div>
                </div>

              </div>
            </div>

          </section>

        </div>
      </main>
    </div>
  );
};

export default StudentDashboard;



 