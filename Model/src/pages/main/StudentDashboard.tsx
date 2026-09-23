import React from "react";
import { Link } from "react-router-dom";
import StudentSidebar from "../main/StudentSidebar";

const StudentDashboard: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">

      {/* Sidebar */}
      <StudentSidebar />

      {/* Main Area */}
      <main className="ml-64 min-h-screen">

        {/* Top Bar */}
        <header className="sticky top-0 z-30 flex h-20 items-center justify-between border-b border-gray-200 bg-white px-8">

          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              Dashboard
            </h1>

            <p className="text-sm text-gray-500">
              Your personalized learning space
            </p>
          </div>

          <div className="flex items-center gap-5">

            {/* Notification */}
            <Link
              to="/notifications"
              className="relative flex h-10 w-10 items-center justify-center rounded-full bg-gray-100 hover:bg-purple-100"
            >
              <span className="absolute right-1 top-1 h-2.5 w-2.5 rounded-full bg-red-500" />
            </Link>

            {/* Profile */}
            <Link
              to="/profile"
              className="flex items-center gap-3"
            >
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-purple-600 font-bold text-white">
                S
              </div>

              <div>
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

          {/* Welcome Section */}
          <section className="rounded-2xl bg-slate-100 p-8 text-white">

            <p className="text-sm font-medium text-purple-300">
              Welcome back
            </p>

            <h2 className="mt-2 text-3xl font-bold text-black">
              Ready to continue learning?
            </h2>

            <p className="mt-3 max-w-2xl text-purple-400">
              Continue your lessons, practice with your AI Tutor,
              and track your learning progress.
            </p>

            <Link
              to="/subjects"
              className="mt-6 inline-block rounded-lg bg-white px-6 py-3 font-semibold text-purple-600 hover:bg-gray-100"
            >
              Start Learning
            </Link>

          </section>

          {/* Statistics */}
          <section className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">

            {/* Subjects */}
            <div className="rounded-2xl border border-gray-200 bg-white p-6">

              <p className="mb-4 text-sm font-medium text-purple-600">
                Subjects
              </p>

              <p className="text-sm text-gray-500">
                My Subjects
              </p>

              <h3 className="mt-1 text-2xl font-bold text-gray-900">
                6
              </h3>
            </div>

            {/* Lessons */}
            <div className="rounded-2xl border border-gray-200 bg-white p-6">

              <p className="mb-4 text-sm font-medium text-blue-600">
                Lessons
              </p>

              <p className="text-sm text-gray-500">
                Lessons Completed
              </p>

              <h3 className="mt-1 text-2xl font-bold text-gray-900">
                24
              </h3>
            </div>

            {/* Progress */}
            <div className="rounded-2xl border border-gray-200 bg-white p-6">

              <p className="mb-4 text-sm font-medium text-green-600">
                Progress
              </p>

              <p className="text-sm text-gray-500">
                Overall Progress
              </p>

              <h3 className="mt-1 text-2xl font-bold text-gray-900">
                68%
              </h3>
            </div>

            {/* Streak */}
            <div className="rounded-2xl border border-gray-200 bg-white p-6">

              <p className="mb-4 text-sm font-medium text-orange-600">
                Streak
              </p>

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

                <div className="flex items-center justify-between">

                  <div className="flex items-center gap-4">

                    <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-purple-100">
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

                    <span>
                      75%
                    </span>
                  </div>

                  <div className="h-2 rounded-full bg-gray-200">
                    <div className="h-2 w-3/4 rounded-full bg-slate-100" />
                  </div>

                </div>

                <Link
                  to="/subjects"
                  className="mt-5 block rounded-lg bg-slate-100 py-3 text-center text-sm font-semibold text-black hover:bg-slate-300"
                >
                  Continue Learning
                </Link>

              </div>

              {/* Science */}
              <div className="rounded-2xl border border-gray-200 bg-white p-6">

                <div className="flex items-center justify-between">

                  <div className="flex items-center gap-4">

                    <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-blue-100">
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

                  <span className="rounded-full bg-blue-100 px-3 py-1 text-xs font-semibold text-black">
                    45%
                  </span>

                </div>

                <div className="mt-5">

                  <div className="mb-2 flex justify-between text-xs text-gray-500">
                    <span>
                      Human Body Systems
                    </span>

                    <span>
                      45%
                    </span>
                  </div>

                  <div className="h-2 rounded-full bg-gray-200">
                    <div className="h-2 w-[45%] rounded-full bg-slate-100" />
                  </div>

                </div>

                <Link
                  to="/subjects"
                  className="mt-5 block rounded-lg bg-slate-100 py-3 text-center text-sm font-semibold text-black hover:bg-slate-300"
                >
                  Continue Learning
                </Link>

              </div>

            </div>

          </section>

          {/* AI Tutor + Recent Activity */}
          <section className="grid grid-cols-1 gap-6 lg:grid-cols-2">

            {/* AI Tutor */}
            <div className="rounded-2xl bg-gray-900 p-7 text-white">

              <div className="flex items-center gap-4">

                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-purple-300">
                </div>

                <div>
                  <h2 className="text-xl font-bold">
                    AI Tutor
                  </h2>

                  <p className="text-sm text-gray-400">
                    Your personal learning assistant
                  </p>
                </div>

              </div>

              <p className="mt-5 text-sm leading-6 text-gray-300">
                Ask questions, get explanations, practice exercises,
                and receive personalized help with your studies.
              </p>

              <Link
                to="/ai-tutor"
                className="mt-6 inline-block rounded-lg bg-slate-100 px-5 py-3 text-sm font-semibold text-black hover:bg-slate-300"
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

                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-green-100">
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

                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-slate-100">
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

                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-100">
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