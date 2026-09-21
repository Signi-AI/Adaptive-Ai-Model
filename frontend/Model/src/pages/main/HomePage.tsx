import React from "react";
import { Link } from "react-router-dom";

import AppHeader from "../components/AppHeader";
import AppSidebar from "../components/Appsidebar";
import MobileNavigation from "../components/Mobilenavigation";
import SubjectCard from "../components/SubjectCard";
import Dashboard from "./Dashbord";
import About from "../components/About";

interface Subject {
  id: string;
  name: string;
  description: string;
  progress: number;
  topics: number;
  completedTopics: number;
  icon: string;
}

const HomePage: React.FC = () => {
  const subjects: Subject[] = [
    {
      id: "mathematics",
      name: "Mathematics",
      description: "Numbers, algebra, geometry and problem solving.",
      progress: 72,
      topics: 18,
      completedTopics: 13,
      icon: "∑",
    },
    {
      id: "english",
      name: "English",
      description: "Grammar, writing, comprehension and communication.",
      progress: 81,
      topics: 16,
      completedTopics: 13,
      icon: "A",
    },
    {
      id: "biology",
      name: "Biology",
      description: "Cells, genetics, living organisms and ecology.",
      progress: 70,
      topics: 20,
      completedTopics: 14,
      icon: "⌬",
    },
    {
      id: "chemistry",
      name: "Chemistry",
      description: "Atoms, matter, reactions and chemical processes.",
      progress: 63,
      topics: 17,
      completedTopics: 11,
      icon: "⚗",
    },
    {
      id: "physics",
      name: "Physics",
      description: "Motion, forces, energy and physical systems.",
      progress: 52,
      topics: 19,
      completedTopics: 10,
      icon: "Φ",
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50 text-black">

      {/* ================= SIDEBAR ================= */}
      <AppSidebar />

      {/* ================= APP CONTENT ================= */}
      <div className="lg:ml-64">

        {/* Header */}
        <AppHeader />
        

        {/* Main */}
        <main className="pb-24 lg:pb-10">

          <div className="mx-auto max-w-7xl px-5 py-7 sm:px-6 lg:px-8">

            {/* ================= WELCOME ================= */}
            <section className="flex flex-col gap-5 md:flex-row md:items-end md:justify-between">

              <div>
                <p className="text-sm font-medium text-gray-400">
                  Welcome back
                </p>

                <h1 className="mt-1 text-3xl font-bold tracking-tight sm:text-4xl">
                  Hello, Comfotha 👋
                </h1>

                <p className="mt-3 max-w-2xl text-sm leading-6 text-gray-500 sm:text-base">
                  Continue your learning journey and improve your skills
                  at your own pace.
                </p>
              </div>
              <div>
                <About/>
              </div>

              <Link
                to="/subjects"
                className="inline-flex w-fit items-center rounded-xl bg-black px-5 py-3 text-sm font-semibold text-white transition hover:bg-gray-800"
              >
                Explore Subjects →
              </Link>

            </section>

            {/* ================= STATISTICS ================= */}
            <section className="mt-8 grid grid-cols-2 gap-4 lg:grid-cols-4">

              {/* Progress */}
              <div className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">

                <p className="text-xs font-semibold uppercase tracking-widest text-gray-400">
                  Overall Progress
                </p>

                <p className="mt-2 text-3xl font-bold">
                  68%
                </p>

                <div className="mt-4 h-2 overflow-hidden rounded-full bg-gray-100">
                  <div className="h-full w-[68%] rounded-full bg-black" />
                </div>

              </div>

              {/* Topics */}
              <div className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">

                <p className="text-xs font-semibold uppercase tracking-widest text-gray-400">
                  Topics
                </p>

                <p className="mt-2 text-3xl font-bold">
                  24
                </p>

                <p className="mt-1 text-sm text-gray-400">
                  Completed
                </p>

              </div>

              {/* Assignments */}
              <div className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">

                <p className="text-xs font-semibold uppercase tracking-widest text-gray-400">
                  Assignments
                </p>

                <p className="mt-2 text-3xl font-bold">
                  18
                </p>

                <p className="mt-1 text-sm text-gray-400">
                  15 completed
                </p>

              </div>

              {/* Streak */}
              <div className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">

                <p className="text-xs font-semibold uppercase tracking-widest text-gray-400">
                  Learning Streak
                </p>

                <p className="mt-2 text-3xl font-bold">
                  7 days
                </p>

                <p className="mt-1 text-sm text-gray-400">
                  Keep going
                </p>

              </div>

            </section>

            {/* ================= CONTINUE LEARNING ================= */}
            <section className="mt-8">

              <div className="mb-4">
                <p className="text-xs font-semibold uppercase tracking-widest text-gray-400">
                  Continue
                </p>

                <h2 className="mt-1 text-2xl font-bold">
                  Continue Learning
                </h2>
              </div>

              <div className="rounded-3xl bg-black p-6 text-white shadow-lg sm:p-8">

                <div className="flex flex-col gap-7 lg:flex-row lg:items-center lg:justify-between">

                  <div className="max-w-2xl">

                    <div className="flex items-center gap-4">

                      <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-white text-xl font-bold text-black">
                        Φ
                      </div>

                      <div>
                        <p className="text-xs uppercase tracking-widest text-gray-500">
                          Physics
                        </p>

                        <h3 className="mt-1 text-xl font-bold">
                          Motion and Speed
                        </h3>
                      </div>

                    </div>

                    <p className="mt-5 text-sm leading-6 text-gray-400">
                      Continue studying speed, velocity, distance and
                      acceleration.
                    </p>

                    <div className="mt-5">

                      <div className="mb-2 flex justify-between text-xs">
                        <span className="text-gray-400">
                          Progress
                        </span>

                        <span className="font-semibold text-white">
                          65%
                        </span>
                      </div>

                      <div className="h-2 overflow-hidden rounded-full bg-gray-800">
                        <div className="h-full w-[65%] rounded-full bg-white" />
                      </div>

                    </div>
                    <div>
                      <Dashboard/>
                    </div>

                  </div>

                  <Link
                    to="/subjects/physics"
                    className="rounded-xl bg-white px-6 py-3 text-center text-sm font-semibold text-black transition hover:bg-gray-100"
                  >
                    Continue →
                  </Link>

                </div>

              </div>

            </section>

            {/* ================= SUBJECTS ================= */}
            <section className="mt-10">

              <div className="flex items-end justify-between">

                <div>
                  <p className="text-xs font-semibold uppercase tracking-widest text-gray-400">
                    Learning
                  </p>

                  <h2 className="mt-1 text-2xl font-bold">
                    My Subjects
                  </h2>
                </div>

                <Link
                  to="/subjects"
                  className="text-sm font-semibold text-gray-500 transition hover:text-black"
                >
                  View all →
                </Link>

              </div>

              <div className="mt-5 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">

                {subjects.map((subject) => (
                  <SubjectCard
                    key={subject.id}
                    {...subject}
                  />
                ))}

              </div>

            </section>

            {/* ================= RECOMMENDATIONS ================= */}
            <section className="mt-10 grid gap-5 lg:grid-cols-2">

              {/* AI Recommendation */}
              <div className="rounded-3xl border border-gray-200 bg-white p-6 shadow-sm">

                <div className="flex gap-4">

                  <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-black text-sm font-bold text-white">
                    AI
                  </div>

                  <div>

                    <p className="text-xs font-semibold uppercase tracking-widest text-gray-400">
                      AI Recommendation
                    </p>

                    <h3 className="mt-2 text-xl font-bold">
                      Practice Physics
                    </h3>

                    <p className="mt-2 text-sm leading-6 text-gray-500">
                      Your recent performance suggests spending more time
                      practicing Motion and Speed.
                    </p>

                    <Link
                      to="/subjects/physics"
                      className="mt-5 inline-flex text-sm font-semibold text-black transition hover:text-gray-500"
                    >
                      Start practice →
                    </Link>

                  </div>

                </div>

              </div>

              {/* Offline */}
              <div className="rounded-3xl border border-gray-200 bg-gray-100 p-6">

                <div className="flex gap-4">

                  <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-white text-xl shadow-sm">
                    📶
                  </div>

                  <div>

                    <p className="text-xs font-semibold uppercase tracking-widest text-gray-400">
                      Offline Learning
                    </p>

                    <h3 className="mt-2 text-xl font-bold">
                      Ready to learn offline
                    </h3>

                    <p className="mt-2 text-sm leading-6 text-gray-500">
                      Your downloaded lessons and learning progress remain
                      available without an internet connection.
                    </p>

                    <div className="mt-4 flex items-center gap-2 text-sm font-semibold">

                      <span className="h-2 w-2 rounded-full bg-green-500" />

                      Offline ready

                    </div>

                  </div>

                </div>

              </div>

            </section>

            {/* ================= RECENT ACTIVITY ================= */}
            <section className="mt-10">

              <div>
                <p className="text-xs font-semibold uppercase tracking-widest text-gray-400">
                  Learning History
                </p>

                <h2 className="mt-1 text-2xl font-bold">
                  Recent Activity
                </h2>
              </div>

              <div className="mt-5 overflow-hidden rounded-3xl border border-gray-200 bg-white shadow-sm">

                {/* Activity 1 */}
                <div className="flex flex-col gap-4 border-b border-gray-100 p-5 sm:flex-row sm:items-center sm:justify-between">

                  <div className="flex items-center gap-4">

                    <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-gray-100 font-bold">
                      ✓
                    </div>

                    <div>
                      <h3 className="text-sm font-semibold">
                        Motion and Speed Quiz
                      </h3>

                      <p className="mt-1 text-xs text-gray-400">
                        Physics · Today
                      </p>
                    </div>

                  </div>

                  <div>
                    <span className="text-xs text-gray-400">
                      Score
                    </span>

                    <p className="font-bold">
                      72%
                    </p>
                  </div>

                </div>

                {/* Activity 2 */}
                <div className="flex flex-col gap-4 border-b border-gray-100 p-5 sm:flex-row sm:items-center sm:justify-between">

                  <div className="flex items-center gap-4">

                    <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-gray-100 font-bold">
                      ✓
                    </div>

                    <div>
                      <h3 className="text-sm font-semibold">
                        Quadratic Equations
                      </h3>

                      <p className="mt-1 text-xs text-gray-400">
                        Mathematics · Yesterday
                      </p>
                    </div>

                  </div>

                  <div>
                    <span className="text-xs text-gray-400">
                      Score
                    </span>

                    <p className="font-bold">
                      86%
                    </p>
                  </div>

                </div>

                {/* Activity 3 */}
                <div className="flex flex-col gap-4 p-5 sm:flex-row sm:items-center sm:justify-between">

                  <div className="flex items-center gap-4">

                    <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-gray-100 font-bold">
                      ✓
                    </div>

                    <div>
                      <h3 className="text-sm font-semibold">
                        Cell Structure Assignment
                      </h3>

                      <p className="mt-1 text-xs text-gray-400">
                        Biology · 2 days ago
                      </p>
                    </div>

                  </div>

                  <div>
                    <span className="text-xs text-gray-400">
                      Score
                    </span>

                    <p className="font-bold">
                      78%
                    </p>
                  </div>

                </div>

              </div>

            </section>

          </div>

        </main>

        {/* Mobile Navigation */}
        <MobileNavigation />

      </div>

    </div>
  );
};

export default HomePage;