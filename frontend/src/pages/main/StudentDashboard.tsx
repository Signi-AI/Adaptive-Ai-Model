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
  ChevronRight,
  Target,
  Trophy,
} from "lucide-react";
import logo from "../../assets/logo.jpeg";
import StudentSidebar from "../main/StudentSidebar";

interface CircularProgressProps {
  value: number;
  size?: number;
  strokeWidth?: number;
  label?: string;
  subLabel?: string;
  dark?: boolean;
  color?: string;
}

const CircularProgress: React.FC<CircularProgressProps> = ({
  value,
  size = 110,
  strokeWidth = 10,
  label,
  subLabel,
  dark = false,
  color = "text-blue-600",
}) => {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (value / 100) * circumference;

  return (
    <div
      className="relative flex shrink-0 items-center justify-center"
      style={{ width: size, height: size }}
    >
      <svg
        width={size}
        height={size}
        viewBox={`0 0 ${size} ${size}`}
        className="-rotate-90"
      >
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="currentColor"
          strokeWidth={strokeWidth}
          className={dark ? "text-white/15" : "text-slate-100"}
        />

        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="currentColor"
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          className={`${color} transition-all duration-1000`}
        />
      </svg>

      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span
          className={`text-xl font-extrabold tracking-tight ${
            dark ? "text-white" : "text-slate-900"
          }`}
        >
          {value}%
        </span>

        {label && (
          <span
            className={`mt-0.5 text-[9px] font-semibold uppercase tracking-wider ${
              dark ? "text-white/70" : "text-slate-400"
            }`}
          >
            {label}
          </span>
        )}

        {subLabel && (
          <span
            className={`text-[9px] ${
              dark ? "text-white/60" : "text-slate-400"
            }`}
          >
            {subLabel}
          </span>
        )}
      </div>
    </div>
  );
};

const SmallCircularProgress: React.FC<{
  value: number;
  color?: string;
}> = ({ value, color = "text-blue-600" }) => {
  const size = 58;
  const strokeWidth = 6;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (value / 100) * circumference;

  return (
    <div className="relative h-[58px] w-[58px] shrink-0">
      <svg
        width="58"
        height="58"
        viewBox="0 0 58 58"
        className="-rotate-90"
      >
        <circle
          cx="29"
          cy="29"
          r={radius}
          fill="none"
          stroke="currentColor"
          strokeWidth={strokeWidth}
          className="text-slate-100"
        />

        <circle
          cx="29"
          cy="29"
          r={radius}
          fill="none"
          stroke="currentColor"
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          className={`${color} transition-all duration-1000`}
        />
      </svg>

      <span className="absolute inset-0 flex items-center justify-center text-[11px] font-extrabold text-slate-800">
        {value}%
      </span>
    </div>
  );
};

const StudentDashboard: React.FC = () => {
  const unreadCount = 2;

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900 antialiased">
      <StudentSidebar />

      <main className="ml-60 min-h-screen">
        {/* TOP BAR */}
        <header className="sticky top-0 z-30 flex h-20 items-center justify-between border-b border-slate-200 bg-white/95 px-8 backdrop-blur-xl">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
              <img
                src={logo}
                alt="LearnAI Logo"
                className="h-full w-full object-cover"
              />
            </div>

            <div>
              <h1 className="text-lg font-extrabold tracking-tight text-slate-800">
                Dashboard
              </h1>

              <p className="text-xs text-slate-500">
                Your personalized learning space
              </p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <Link
              to="/notifications"
              className="relative flex h-10 w-10 items-center justify-center rounded-xl border border-slate-200 bg-white text-slate-500 shadow-sm transition hover:border-blue-200 hover:bg-blue-50 hover:text-blue-600"
              aria-label={`${unreadCount} unread notifications`}
            >
              <Bell size={18} />

              {unreadCount > 0 && (
                <span className="absolute -right-1 -top-1 flex h-4 w-4 items-center justify-center rounded-full bg-red-500 text-[10px] font-extrabold text-white ring-2 ring-white">
                  {unreadCount}
                </span>
              )}
            </Link>

            <Link
              to="/profile"
              className="flex items-center gap-3 rounded-2xl border border-slate-200 bg-white p-1.5 pr-4 shadow-sm transition hover:border-blue-200 hover:bg-blue-50/40"
            >
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-slate-800 font-extrabold text-white">
                S
              </div>

              <div className="text-left">
                <p className="text-xs font-bold leading-tight text-slate-800">
                  Student
                </p>

                <p className="text-[10px] font-medium text-slate-500">
                  Form 2
                </p>
              </div>
            </Link>
          </div>
        </header>

        <div className="mx-auto max-w-7xl space-y-7 p-8">
          {/* HERO */}
          <section className="relative overflow-hidden rounded-[28px] bg-slate-800 p-8 text-white shadow-lg shadow-slate-900/10">
            <div className="absolute -right-20 -top-24 h-72 w-72 rounded-full bg-blue-500/10 blur-3xl" />

            <div className="absolute -bottom-32 right-24 h-64 w-64 rounded-full bg-slate-700/50 blur-3xl" />

            <div className="relative z-10 flex flex-col justify-between gap-8 lg:flex-row lg:items-center">
              <div className="max-w-2xl">
                <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/10 px-3 py-1.5 text-[11px] font-bold text-slate-200 backdrop-blur">
                  <Sparkles size={13} />
                  AI Tutor Active
                </div>

                <h2 className="text-3xl font-extrabold tracking-tight sm:text-4xl">
                  Ready to continue learning?
                </h2>

                <p className="mt-3 max-w-xl text-sm leading-6 text-slate-300">
                  Continue your lessons, practice with your AI Tutor, and
                  improve your learning progress every day.
                </p>

                <div className="mt-6 flex flex-wrap gap-3">
                  <Link
                    to="/subjects"
                    className="inline-flex items-center gap-2 rounded-xl bg-blue-600 px-5 py-3 text-xs font-bold text-white shadow-sm transition hover:bg-blue-700 active:scale-95"
                  >
                    Start Learning
                    <ArrowUpRight size={14} />
                  </Link>

                  <Link
                    to="/learn"
                    className="inline-flex items-center gap-2 rounded-xl border border-white/10 bg-white/10 px-5 py-3 text-xs font-bold text-white backdrop-blur transition hover:bg-white/15 active:scale-95"
                  >
                    <BrainCircuit size={15} />
                    Ask AI Tutor
                  </Link>
                </div>
              </div>

              <div className="hidden pr-8 lg:block">
                <div className="rounded-3xl border border-white/10 bg-white/5 p-5 backdrop-blur-md">
                  <CircularProgress
                    value={68}
                    size={145}
                    strokeWidth={11}
                    label="Overall"
                    subLabel="Progress"
                    dark
                    color="text-blue-500"
                  />
                </div>
              </div>
            </div>
          </section>

          {/* QUICK STATS */}
          <section className="grid grid-cols-1 gap-5 sm:grid-cols-2 xl:grid-cols-4">
            {/* SUBJECTS */}
            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:border-blue-200 hover:shadow-md">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-xs font-semibold text-slate-500">
                    My Subjects
                  </p>

                  <h3 className="mt-2 text-3xl font-extrabold text-slate-800">
                    6
                  </h3>
                </div>

                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-50 text-blue-600">
                  <BookOpen size={19} />
                </div>
              </div>

              <div className="mt-4 flex items-center justify-between">
                <span className="text-[11px] text-slate-500">
                  Active courses
                </span>

                <span className="text-[11px] font-bold text-green-600">
                  +1 this term
                </span>
              </div>
            </div>

            {/* COMPLETED */}
            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:border-green-200 hover:shadow-md">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-xs font-semibold text-slate-500">
                    Lessons Completed
                  </p>

                  <h3 className="mt-2 text-3xl font-extrabold text-slate-800">
                    24
                  </h3>
                </div>

                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-green-50 text-green-600">
                  <CheckCircle2 size={19} />
                </div>
              </div>

              <div className="mt-4 flex items-center justify-between">
                <span className="text-[11px] text-slate-500">
                  This term
                </span>

                <span className="text-[11px] font-bold text-green-600">
                  +3 this week
                </span>
              </div>
            </div>

            {/* PROGRESS */}
            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:border-blue-200 hover:shadow-md">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-xs font-semibold text-slate-500">
                    Overall Progress
                  </p>

                  <h3 className="mt-2 text-3xl font-extrabold text-slate-800">
                    68%
                  </h3>
                </div>

                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-50 text-blue-600">
                  <TrendingUp size={19} />
                </div>
              </div>

              <p className="mt-4 text-[11px] text-slate-500">
                On track for your term goal
              </p>
            </div>

            {/* STREAK */}
            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:border-amber-200 hover:shadow-md">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-xs font-semibold text-slate-500">
                    Learning Streak
                  </p>

                  <h3 className="mt-2 text-3xl font-extrabold text-slate-800">
                    7
                    <span className="ml-1 text-base font-bold text-slate-400">
                      days
                    </span>
                  </h3>
                </div>

                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-50 text-amber-600">
                  <Flame size={19} />
                </div>
              </div>

              <p className="mt-4 text-[11px] font-bold text-amber-600">
                🔥 Personal record
              </p>
            </div>
          </section>

          {/* LEARNING PROGRESS */}
          <section className="rounded-3xl border border-slate-200 bg-white p-7 shadow-sm">
            <div className="mb-7 flex items-center justify-between">
              <div>
                <h2 className="text-lg font-extrabold text-slate-800">
                  Learning Progress
                </h2>

                <p className="mt-1 text-xs text-slate-500">
                  Track your performance across your subjects
                </p>
              </div>

              <Link
                to="/progress"
                className="flex items-center gap-1 text-xs font-bold text-blue-600 transition hover:text-blue-700"
              >
                View progress
                <ChevronRight size={14} />
              </Link>
            </div>

            <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
              {/* OVERALL */}
              <div className="flex flex-col items-center justify-center rounded-2xl bg-slate-50 p-6">
                <CircularProgress
                  value={68}
                  size={150}
                  strokeWidth={12}
                  label="Overall"
                  subLabel="Progress"
                  color="text-blue-600"
                />

                <div className="mt-5 text-center">
                  <p className="text-sm font-bold text-slate-800">
                    Good progress!
                  </p>

                  <p className="mt-1 text-[11px] text-slate-500">
                    Keep learning consistently.
                  </p>
                </div>
              </div>

              {/* SUBJECTS */}
              <div className="space-y-5 md:col-span-2">
                {/* MATHEMATICS */}
                <div className="flex items-center gap-4 rounded-2xl border border-slate-100 p-4 transition hover:border-blue-200 hover:bg-blue-50/30">
                  <SmallCircularProgress
                    value={75}
                    color="text-blue-600"
                  />

                  <div className="min-w-0 flex-1">
                    <div className="flex items-center justify-between gap-3">
                      <div>
                        <h3 className="text-sm font-bold text-slate-800">
                          Mathematics
                        </h3>

                        <p className="mt-0.5 text-[11px] text-slate-500">
                          Algebra • Form 2
                        </p>
                      </div>

                      <span className="hidden text-[11px] font-semibold text-blue-600 sm:block">
                        Lesson 4 of 6
                      </span>
                    </div>
                  </div>
                </div>

                {/* SCIENCE */}
                <div className="flex items-center gap-4 rounded-2xl border border-slate-100 p-4 transition hover:border-green-200 hover:bg-green-50/30">
                  <SmallCircularProgress
                    value={45}
                    color="text-green-600"
                  />

                  <div className="min-w-0 flex-1">
                    <div className="flex items-center justify-between gap-3">
                      <div>
                        <h3 className="text-sm font-bold text-slate-800">
                          Science
                        </h3>

                        <p className="mt-0.5 text-[11px] text-slate-500">
                          Biology • Form 2
                        </p>
                      </div>

                      <span className="hidden text-[11px] font-semibold text-green-600 sm:block">
                        Lesson 2 of 5
                      </span>
                    </div>
                  </div>
                </div>

                {/* ENGLISH */}
                <div className="flex items-center gap-4 rounded-2xl border border-slate-100 p-4 transition hover:border-amber-200 hover:bg-amber-50/30">
                  <SmallCircularProgress
                    value={82}
                    color="text-amber-500"
                  />

                  <div className="min-w-0 flex-1">
                    <div className="flex items-center justify-between gap-3">
                      <div>
                        <h3 className="text-sm font-bold text-slate-800">
                          English
                        </h3>

                        <p className="mt-0.5 text-[11px] text-slate-500">
                          Grammar • Form 2
                        </p>
                      </div>

                      <span className="hidden text-[11px] font-semibold text-amber-600 sm:block">
                        Lesson 5 of 6
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* CONTINUE LEARNING */}
          <section>
            <div className="mb-4 flex items-center justify-between">
              <div>
                <h2 className="flex items-center gap-2 text-lg font-extrabold text-slate-800">
                  <BookOpen size={19} className="text-blue-600" />
                  Continue Learning
                </h2>

                <p className="mt-1 text-xs text-slate-500">
                  Pick up where you left off
                </p>
              </div>

              <Link
                to="/subjects"
                className="flex items-center gap-1 text-xs font-bold text-blue-600 transition hover:text-blue-700"
              >
                View all
                <ChevronRight size={14} />
              </Link>
            </div>

            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
              {/* MATHEMATICS */}
              <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm transition hover:-translate-y-0.5 hover:border-blue-200 hover:shadow-md">
                <div className="flex items-center gap-5">
                  <SmallCircularProgress
                    value={75}
                    color="text-blue-600"
                  />

                  <div className="min-w-0 flex-1">
                    <div className="flex items-center justify-between gap-3">
                      <div>
                        <h3 className="text-base font-extrabold text-slate-800">
                          Mathematics
                        </h3>

                        <p className="mt-1 text-xs text-slate-500">
                          Algebra • Form 2
                        </p>
                      </div>

                      <span className="rounded-lg bg-blue-50 px-2.5 py-1 text-[10px] font-bold text-blue-600">
                        75%
                      </span>
                    </div>
                  </div>
                </div>

                <div className="mt-6 rounded-2xl bg-slate-50 p-4">
                  <div className="flex items-center justify-between text-[11px]">
                    <span className="font-medium text-slate-500">
                      Current lesson
                    </span>

                    <span className="font-bold text-slate-700">
                      4 of 6
                    </span>
                  </div>

                  <p className="mt-2 text-xs font-bold text-slate-800">
                    Introduction to Equations
                  </p>
                </div>

                <Link
                  to="/subjects"
                  className="mt-5 flex w-full items-center justify-center gap-2 rounded-xl bg-blue-600 py-3 text-xs font-bold text-white shadow-sm transition hover:bg-blue-700 active:scale-[0.98]"
                >
                  Continue Lesson
                  <ChevronRight size={14} />
                </Link>
              </div>

              {/* SCIENCE */}
              <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm transition hover:-translate-y-0.5 hover:border-green-200 hover:shadow-md">
                <div className="flex items-center gap-5">
                  <SmallCircularProgress
                    value={45}
                    color="text-green-600"
                  />

                  <div className="min-w-0 flex-1">
                    <div className="flex items-center justify-between gap-3">
                      <div>
                        <h3 className="text-base font-extrabold text-slate-800">
                          Science
                        </h3>

                        <p className="mt-1 text-xs text-slate-500">
                          Biology • Form 2
                        </p>
                      </div>

                      <span className="rounded-lg bg-green-50 px-2.5 py-1 text-[10px] font-bold text-green-600">
                        45%
                      </span>
                    </div>
                  </div>
                </div>

                <div className="mt-6 rounded-2xl bg-slate-50 p-4">
                  <div className="flex items-center justify-between text-[11px]">
                    <span className="font-medium text-slate-500">
                      Current lesson
                    </span>

                    <span className="font-bold text-slate-700">
                      2 of 5
                    </span>
                  </div>

                  <p className="mt-2 text-xs font-bold text-slate-800">
                    Human Body Systems
                  </p>
                </div>

                <Link
                  to="/subjects"
                  className="mt-5 flex w-full items-center justify-center gap-2 rounded-xl bg-green-600 py-3 text-xs font-bold text-white shadow-sm transition hover:bg-green-700 active:scale-[0.98]"
                >
                  Continue Lesson
                  <ChevronRight size={14} />
                </Link>
              </div>
            </div>
          </section>

          {/* AI TUTOR + RECENT ACTIVITY */}
          <section className="grid grid-cols-1 gap-6 lg:grid-cols-2">
            {/* AI TUTOR */}
            <div className="relative overflow-hidden rounded-3xl bg-slate-800 p-7 text-white shadow-lg shadow-slate-900/10">
              <div className="absolute -right-12 -top-12 h-40 w-40 rounded-full bg-blue-500/10" />

              <div className="absolute -bottom-16 left-20 h-32 w-32 rounded-full bg-slate-700/60 blur-2xl" />

              <div className="relative">
                <div className="flex items-center gap-4">
                  <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-600 text-white shadow-md">
                    <BrainCircuit size={24} />
                  </div>

                  <div>
                    <h2 className="text-lg font-extrabold">
                      AI Tutor Assistant
                    </h2>

                    <p className="text-xs text-slate-400">
                      Your personal learning partner
                    </p>
                  </div>
                </div>

                <p className="mt-5 text-xs leading-6 text-slate-300">
                  Ask questions, get step-by-step explanations, practice
                  exercises, and prepare for your upcoming quizzes.
                </p>

                <Link
                  to="/learn"
                  className="mt-6 inline-flex items-center gap-2 rounded-xl bg-blue-600 px-5 py-3 text-xs font-bold text-white shadow-sm transition hover:bg-blue-700 active:scale-95"
                >
                  <Sparkles size={14} />
                  Ask AI Tutor
                  <ArrowUpRight size={14} />
                </Link>
              </div>
            </div>

            {/* RECENT ACTIVITY */}
            <div className="rounded-3xl border border-slate-200 bg-white p-7 shadow-sm">
              <div className="mb-6 flex items-center justify-between">
                <div>
                  <h2 className="flex items-center gap-2 text-base font-extrabold text-slate-800">
                    <Clock size={18} className="text-blue-600" />
                    Recent Activity
                  </h2>

                  <p className="mt-1 text-[11px] text-slate-500">
                    Your latest learning activities
                  </p>
                </div>

                <Link
                  to="/progress"
                  className="text-[11px] font-bold text-blue-600 hover:text-blue-700"
                >
                  View all
                </Link>
              </div>

              <div className="space-y-5">
                {/* ACTIVITY 1 */}
                <div className="flex items-start gap-3.5">
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-green-100 bg-green-50 text-green-600">
                    <CheckCircle2 size={18} />
                  </div>

                  <div className="flex-1">
                    <p className="text-xs font-bold text-slate-800">
                      Completed Algebra Lesson
                    </p>

                    <p className="mt-1 text-[11px] text-slate-500">
                      2 hours ago • Score: 90%
                    </p>
                  </div>

                  <span className="text-[10px] font-bold text-green-600">
                    +10 XP
                  </span>
                </div>

                {/* ACTIVITY 2 */}
                <div className="flex items-start gap-3.5">
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-blue-100 bg-blue-50 text-blue-600">
                    <HelpCircle size={18} />
                  </div>

                  <div className="flex-1">
                    <p className="text-xs font-bold text-slate-800">
                      Asked AI Tutor a question
                    </p>

                    <p className="mt-1 text-[11px] text-slate-500">
                      Yesterday • Quadratic Equations
                    </p>
                  </div>
                </div>

                {/* ACTIVITY 3 */}
                <div className="flex items-start gap-3.5">
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-amber-100 bg-amber-50 text-amber-600">
                    <Trophy size={18} />
                  </div>

                  <div className="flex-1">
                    <p className="text-xs font-bold text-slate-800">
                      Completed Science Quiz
                    </p>

                    <p className="mt-1 text-[11px] text-slate-500">
                      2 days ago • Score: 85%
                    </p>
                  </div>

                  <span className="text-[10px] font-bold text-amber-600">
                    +20 XP
                  </span>
                </div>
              </div>
            </div>
          </section>

          {/* DAILY GOAL */}
          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
              <div className="flex items-center gap-4">
                <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-800 text-white shadow-sm">
                  <Target size={22} />
                </div>

                <div>
                  <h2 className="text-base font-extrabold text-slate-800">
                    Today's Learning Goal
                  </h2>

                  <p className="mt-1 text-xs text-slate-500">
                    Complete 3 lessons today to maintain your streak.
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-5">
                <CircularProgress
                  value={67}
                  size={82}
                  strokeWidth={7}
                  color="text-blue-600"
                />

                <div>
                  <p className="text-sm font-extrabold text-slate-800">
                    2 of 3 lessons
                  </p>

                  <p className="mt-1 text-[11px] text-slate-500">
                    One more to go!
                  </p>
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