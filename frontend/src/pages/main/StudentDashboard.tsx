import React from "react";
import { Link } from "react-router-dom";
import {
  Bell,
  BookOpen,
  CheckCircle2,
  TrendingUp,
  Flame,
  Sparkles,
  BrainCircuit,
  ArrowUpRight,
  Clock,
  HelpCircle,
  Award,
  ChevronRight,
} from "lucide-react";
import logo from "../../assets/logo.jpeg";
import StudentSidebar from "../main/StudentSidebar";

const StudentDashboard: React.FC = () => {
  // Number of unread notifications
  const unreadCount = 2;

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900 antialiased">
      {/* Sidebar */}
      <StudentSidebar />

      {/* Main Area */}
      <main className="ml-60 min-h-screen">
        {/* TOP BAR */}
        <header className="sticky top-0 z-30 flex h-20 items-center justify-between border-b border-slate-200/80 bg-white/90 px-8 backdrop-blur-md">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center overflow-hidden rounded-xl border border-slate-200 shadow-sm">
              <img src={logo} alt="LearnAI Logo" className="h-full w-full object-cover" />
            </div>
            <div>
              <h1 className="text-lg font-bold tracking-tight text-slate-900">Dashboard</h1>
              <p className="text-xs text-slate-500">Your personalized learning space</p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            {/* Notification Button */}
            <Link
              to="/notifications"
              className="relative flex h-10 w-10 items-center justify-center rounded-xl border border-slate-200 bg-white text-slate-600 transition-all hover:bg-slate-100 hover:text-slate-900 shadow-sm"
              aria-label={`${unreadCount} unread notifications`}
            >
              <Bell size={18} />
              {unreadCount > 0 && (
                <span className="absolute -top-1 -right-1 flex h-4 w-4 items-center justify-center rounded-full bg-rose-500 text-[10px] font-extrabold text-white ring-2 ring-white">
                  {unreadCount}
                </span>
              )}
            </Link>

            {/* Profile Avatar */}
            <Link
              to="/profile"
              className="flex items-center gap-3 rounded-2xl border border-slate-200 bg-white p-1.5 pr-4 shadow-sm transition-all hover:border-slate-300 hover:bg-slate-50"
            >
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-slate-900 font-extrabold text-white shadow-sm">
                S
              </div>
              <div className="text-left">
                <p className="text-xs font-bold text-slate-900 leading-tight">Student</p>
                <p className="text-[10px] font-medium text-slate-500">Form 2</p>
              </div>
            </Link>
          </div>
        </header>

        {/* DASHBOARD CONTENT */}
        <div className="relative mx-auto max-w-6xl space-y-8 p-8">
          {/* WELCOME BANNER */}
          <section className="relative overflow-hidden rounded-3xl border border-slate-200/80 bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 p-8 shadow-xl shadow-slate-900/5 text-white">
            <div className="relative z-10 max-w-2xl">
              <span className="inline-flex items-center gap-1.5 rounded-full border border-purple-400/30 bg-purple-500/20 px-3 py-1 text-xs font-semibold text-purple-200 mb-3 backdrop-blur-md">
                <Sparkles size={12} /> AI Tutor Active
              </span>
              <h2 className="text-3xl font-extrabold tracking-tight">
                Ready to continue learning? 
              </h2>
              <p className="mt-2 text-sm text-slate-300 leading-relaxed">
                Continue your lessons, practice with your AI Tutor, and track your daily learning progress.
              </p>

              <div className="mt-6 flex items-center gap-3">
                <Link
                  to="/subjects"
                  className="inline-flex items-center gap-2 rounded-xl bg-white px-5 py-2.5 text-xs font-semibold text-slate-900 shadow-sm hover:bg-slate-100 transition-all active:scale-95"
                >
                  <span>Start Learning</span>
                  <ArrowUpRight size={14} />
                </Link>
                <Link
                  to="/ai-tutor"
                  className="inline-flex items-center gap-2 rounded-xl border border-slate-700 bg-slate-800/80 px-5 py-2.5 text-xs font-semibold text-slate-200 hover:bg-slate-700 hover:text-white transition-all"
                >
                  <BrainCircuit size={14} className="text-purple-400" />
                  <span>Ask AI Tutor</span>
                </Link>
              </div>
            </div>

            <div className="absolute right-6 -bottom-10 opacity-10 pointer-events-none hidden lg:block">
              <Sparkles size={280} className="text-white" />
            </div>
          </section>

          {/* STATISTICS GRID */}
          <section className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {/* Enrolled Subjects */}
            <div className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-sm transition-all hover:border-slate-300 hover:shadow-md">
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-semibold text-slate-500">My Subjects</span>
                <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-purple-50 text-purple-600 border border-purple-100">
                  <BookOpen size={18} />
                </div>
              </div>
              <h3 className="text-3xl font-extrabold text-slate-900">6</h3>
              <p className="mt-1 text-xs text-slate-500">Active enrolled courses</p>
            </div>

            {/* Lessons Completed */}
            <div className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-sm transition-all hover:border-slate-300 hover:shadow-md">
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-semibold text-slate-500">Lessons Completed</span>
                <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-blue-50 text-blue-600 border border-blue-100">
                  <CheckCircle2 size={18} />
                </div>
              </div>
              <h3 className="text-3xl font-extrabold text-slate-900">24</h3>
              <p className="mt-1 text-xs font-medium text-emerald-600">+3 finished this week</p>
            </div>

            {/* Overall Progress */}
            <div className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-sm transition-all hover:border-slate-300 hover:shadow-md">
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-semibold text-slate-500">Overall Progress</span>
                <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600 border border-emerald-100">
                  <TrendingUp size={18} />
                </div>
              </div>
              <h3 className="text-3xl font-extrabold text-slate-900">68%</h3>
              <p className="mt-1 text-xs text-slate-500">On track for term goal</p>
            </div>

            {/* Learning Streak */}
            <div className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-sm transition-all hover:border-slate-300 hover:shadow-md">
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-semibold text-slate-500">Learning Streak</span>
                <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-amber-50 text-amber-600 border border-amber-100">
                  <Flame size={18} />
                </div>
              </div>
              <h3 className="text-3xl font-extrabold text-slate-900">7 Days</h3>
              <p className="mt-1 text-xs font-bold text-amber-600">🔥 Personal record!</p>
            </div>
          </section>

          {/* CONTINUE LEARNING SECTION */}
          <section>
            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                <BookOpen size={20} className="text-purple-600" />
                Continue Learning
              </h2>

              <Link
                to="/subjects"
                className="text-xs font-bold text-slate-700 hover:text-slate-900 flex items-center gap-1 transition-all"
              >
                <span>View all subjects</span>
                <ChevronRight size={14} />
              </Link>
            </div>

            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
              {/* Mathematics Card */}
              <div className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-sm transition-all hover:shadow-md">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-base font-bold text-slate-900">Mathematics</h3>
                    <p className="text-xs text-slate-500">Algebra • Form 2</p>
                  </div>
                  <span className="rounded-lg border border-purple-200 bg-purple-50 px-3 py-1 text-xs font-bold text-purple-700">
                    75%
                  </span>
                </div>

                <div className="mt-5">
                  <div className="mb-2 flex justify-between text-xs text-slate-500">
                    <span>Introduction to Equations</span>
                    <span className="font-semibold text-slate-700">Lesson 4 of 6</span>
                  </div>
                  <div className="h-2.5 w-full rounded-full bg-slate-100 overflow-hidden">
                    <div className="h-2.5 rounded-full bg-slate-900 w-[75%]" />
                  </div>
                </div>

                <Link
                  to="/subjects"
                  className="mt-6 flex items-center justify-center gap-2 w-full rounded-xl bg-slate-900 py-2.5 text-xs font-semibold text-white hover:bg-slate-800 transition-all shadow-sm active:scale-95"
                >
                  <span>Continue Lesson</span>
                  <ChevronRight size={14} />
                </Link>
              </div>

              {/* Science Card */}
              <div className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-sm transition-all hover:shadow-md">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-base font-bold text-slate-900">Science</h3>
                    <p className="text-xs text-slate-500">Biology • Form 2</p>
                  </div>
                  <span className="rounded-lg border border-blue-200 bg-blue-50 px-3 py-1 text-xs font-bold text-blue-700">
                    45%
                  </span>
                </div>

                <div className="mt-5">
                  <div className="mb-2 flex justify-between text-xs text-slate-500">
                    <span>Human Body Systems</span>
                    <span className="font-semibold text-slate-700">Lesson 2 of 5</span>
                  </div>
                  <div className="h-2.5 w-full rounded-full bg-slate-100 overflow-hidden">
                    <div className="h-2.5 rounded-full bg-slate-900 w-[45%]" />
                  </div>
                </div>

                <Link
                  to="/subjects"
                  className="mt-6 flex items-center justify-center gap-2 w-full rounded-xl bg-slate-900 py-2.5 text-xs font-semibold text-white hover:bg-slate-800 transition-all shadow-sm active:scale-95"
                >
                  <span>Continue Lesson</span>
                  <ChevronRight size={14} />
                </Link>
              </div>
            </div>
          </section>

          {/* AI TUTOR + RECENT ACTIVITY */}
          <section className="grid grid-cols-1 gap-6 lg:grid-cols-2">
            {/* AI TUTOR PROMPT CARD */}
            <div className="rounded-3xl border border-slate-200/80 bg-white p-7 shadow-sm flex flex-col justify-between">
              <div>
                <div className="flex items-center gap-4">
                  <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-900 text-white shadow-md">
                    <BrainCircuit size={24} />
                  </div>
                  <div>
                    <h2 className="text-lg font-bold text-slate-900">AI Tutor Assistant</h2>
                    <p className="text-xs text-slate-500">Your personal 24/7 learning partner</p>
                  </div>
                </div>

                <p className="mt-4 text-xs leading-relaxed text-slate-600">
                  Ask questions, get step-by-step problem explanations, practice interactive exercises, and prepare for upcoming quizzes.
                </p>
              </div>

              <div className="mt-6">
                <Link
                  to="/ai-tutor"
                  className="inline-flex items-center gap-2 rounded-xl bg-slate-900 px-5 py-2.5 text-xs font-semibold text-white shadow-sm hover:bg-slate-800 transition-all active:scale-95"
                >
                  <Sparkles size={14} className="text-amber-400" />
                  <span>Ask AI Tutor</span>
                </Link>
              </div>
            </div>

            {/* RECENT ACTIVITY TIMELINE */}
            <div className="rounded-3xl border border-slate-200/80 bg-white p-7 shadow-sm">
              <h2 className="text-base font-bold text-slate-900 mb-5 flex items-center gap-2">
                <Clock size={18} className="text-slate-700" />
                Recent Activity
              </h2>

              <div className="space-y-4">
                <div className="flex items-start gap-3.5">
                  <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600 border border-emerald-100">
                    <CheckCircle2 size={18} />
                  </div>
                  <div>
                    <p className="text-xs font-semibold text-slate-900">Completed Algebra Lesson</p>
                    <p className="text-[11px] text-slate-500 mt-0.5">2 hours ago • Score: 90%</p>
                  </div>
                </div>

                <div className="flex items-start gap-3.5">
                  <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-purple-50 text-purple-600 border border-purple-100">
                    <HelpCircle size={18} />
                  </div>
                  <div>
                    <p className="text-xs font-semibold text-slate-900">Asked AI Tutor a question</p>
                    <p className="text-[11px] text-slate-500 mt-0.5">Yesterday • Quadratic Equations</p>
                  </div>
                </div>

                <div className="flex items-start gap-3.5">
                  <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-blue-50 text-blue-600 border border-blue-100">
                    <Award size={18} />
                  </div>
                  <div>
                    <p className="text-xs font-semibold text-slate-900">Completed Science Quiz</p>
                    <p className="text-[11px] text-slate-500 mt-0.5">2 days ago • Score: 85%</p>
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