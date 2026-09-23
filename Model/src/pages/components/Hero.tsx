import React from "react";
import { Link } from "react-router-dom";

const Hero: React.FC = () => {
  return (
    <section className="relative min-h-screen overflow-hidden bg-slate-100">
      {/* Background decorations */}
      <div className="pointer-events-none absolute -right-40 -top-40 h-96 w-96 rounded-full bg-gray-100 blur-3xl" />

      <div className="pointer-events-none absolute -bottom-40 -left-40 h-96 w-96 rounded-full bg-gray-100 blur-3xl" />

      {/* Main Hero Container */}
      <div className="relative mx-auto flex min-h-[calc(100vh-73px)] max-w-7xl flex-col items-center px-5 py-16 text-center md:px-8 lg:py-20">

        {/* ========================================= */}
        {/* HERO CONTENT */}
        {/* ========================================= */}

        <div className="flex w-full max-w-4xl flex-col items-center">

          {/* Small Label */}
          <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-gray-200 bg-gray-50 px-4 py-2 text-sm font-medium text-gray-600">
            <span className="h-2 w-2 rounded-full bg-black" />
            Offline Adaptive Learning
          </div>

          {/* Heading */}
          <h1 className="text-4xl font-bold leading-tight tracking-tight text-black sm:text-5xl md:text-6xl lg:text-7xl">
            Learn Smarter.
            <br />
            <span className="text-gray-400">
              Learn Your Way.
            </span>
          </h1>

          {/* Description */}
          <p className="mt-6 max-w-2xl text-base leading-7 text-gray-500 sm:text-lg">
            An adaptive learning platform that understands your strengths,
            identifies your weaknesses, and adjusts your learning experience
            to your level — even when you are offline.
          </p>

          {/* Buttons - FLEX COLUMN */}
          <div className="mt-8 flex w-full max-w-xs flex-col gap-3">
            <Link
              to="/register"
              className="rounded-xl bg-black px-7 py-3.5 font-semibold text-white shadow-sm transition duration-300 hover:-translate-y-0.5 hover:bg-gray-800 hover:shadow-lg"
            >
              Get Started →
            </Link>

            <a
              href="#how-it-works"
              className="rounded-xl border border-gray-300 bg-white px-7 py-3.5 font-semibold text-black transition duration-300 hover:-translate-y-0.5 hover:bg-gray-50"
            >
              How It Works
            </a>
          </div>

          {/* Trust Indicators */}
          <div className="mt-8 flex flex-col items-center gap-3 text-sm text-gray-400 sm:flex-row sm:gap-6">
            <span>✓ Works Offline</span>
            <span>✓ Personalized</span>
            <span>✓ Curriculum Aligned</span>
          </div>
        </div>

        {/* ========================================= */}
        {/* LEARNING DASHBOARD */}
        {/* ========================================= */}

        <div className="relative mt-14 flex w-full max-w-2xl flex-col">

          {/* Main Dashboard Card */}
          <div className="rounded-3xl border border-gray-200 bg-white p-5 text-left shadow-xl sm:p-7">

            {/* Dashboard Header */}
            <div className="flex items-center justify-between border-b border-gray-100 pb-5">

              <div className="flex flex-col">
                <p className="text-xs font-semibold uppercase tracking-widest text-gray-400">
                  Learning Dashboard
                </p>

                <h2 className="mt-1 text-lg font-bold text-black">
                  Your Learning
                </h2>
              </div>

              {/* Logo */}
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-black text-lg font-bold text-white">
                A
              </div>
            </div>

            {/* ========================================= */}
            {/* OVERALL PROGRESS */}
            {/* ========================================= */}

            <div className="mt-6 rounded-2xl bg-gray-50 p-5">

              {/* Top section */}
              <div className="flex items-start justify-between">

                {/* Progress Text */}
                <div className="flex flex-col">
                  <p className="text-sm text-gray-500">
                    Overall Progress
                  </p>

                  <p className="mt-1 text-3xl font-bold text-black">
                    68%
                  </p>
                </div>

                {/* Progress Circle */}
                <div className="flex h-16 w-16 items-center justify-center rounded-full border-8 border-gray-200">
                  <span className="text-sm font-bold text-gray-600">
                    68
                  </span>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="mt-5 h-3 w-full overflow-hidden rounded-full bg-gray-200">
                <div
                  className="h-full rounded-full bg-black transition-all duration-700"
                  style={{ width: "68%" }}
                />
              </div>

              {/* Progress Description */}
              <div className="mt-3 flex items-center justify-between text-xs text-gray-400">
                <span>Learning progress</span>
                <span>68% completed</span>
              </div>
            </div>

            {/* ========================================= */}
            {/* SUBJECT PROGRESS */}
            {/* ========================================= */}

            <div className="mt-6">

              <div className="mb-4 flex items-center justify-between">
                <h3 className="font-semibold text-black">
                  Subject Progress
                </h3>

                <span className="text-xs text-gray-400">
                  Updated today
                </span>
              </div>

              {/* Mathematics */}
              <div className="mb-5">

                <div className="mb-2 flex justify-between text-sm">
                  <span className="font-medium text-gray-700">
                    Mathematics
                  </span>

                  <span className="text-gray-400">
                    72%
                  </span>
                </div>

                <div className="h-2 overflow-hidden rounded-full bg-gray-100">
                  <div className="h-full w-[72%] rounded-full bg-gray-400" />
                </div>
              </div>

              {/* Physics */}
              <div className="mb-5">

                <div className="mb-2 flex justify-between text-sm">
                  <span className="font-medium text-gray-700">
                    Physics
                  </span>

                  <span className="text-gray-400">
                    54%
                  </span>
                </div>

                <div className="h-2 overflow-hidden rounded-full bg-gray-100">
                  <div className="h-full w-[54%] rounded-full bg-gray-400" />
                </div>
              </div>

              {/* Biology */}
              <div>

                <div className="mb-2 flex justify-between text-sm">
                  <span className="font-medium text-gray-700">
                    Biology
                  </span>

                  <span className="text-gray-400">
                    81%
                  </span>
                </div>

                <div className="h-2 overflow-hidden rounded-full bg-gray-100">
                  <div className="h-full w-[81%] rounded-full bg-gray-400" />
                </div>
              </div>
            </div>

            {/* ========================================= */}
            {/* AI RECOMMENDATION */}
            {/* ========================================= */}

            <div className="mt-6 flex gap-3 rounded-2xl border border-gray-200 bg-white p-4">

              {/* AI Icon */}
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-black text-white">
                🤖
              </div>

              {/* Recommendation Text */}
              <div>
                <p className="text-xs font-semibold uppercase tracking-wide text-gray-400">
                  AI Recommendation
                </p>

                <p className="mt-1 text-sm font-semibold text-black">
                  Practice Physics next
                </p>

                <p className="mt-1 text-xs leading-5 text-gray-500">
                  Based on your recent performance.
                </p>
              </div>
            </div>
          </div>

          {/* ========================================= */}
          {/* OFFLINE BADGE */}
          {/* ========================================= */}

          <div className="absolute -bottom-5 -left-5 hidden rounded-2xl border border-gray-200 bg-white p-4 shadow-lg sm:block">

            <div className="flex items-center gap-3">

              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gray-100 text-lg">
                📶
              </div>

              <div>
                <p className="text-sm font-bold text-black">
                  Offline Ready
                </p>

                <p className="text-xs text-gray-500">
                  Keep learning anywhere
                </p>
              </div>

            </div>
          </div>

          {/* ========================================= */}
          {/* ADAPTIVE BADGE */}
          {/* ========================================= */}

          <div className="absolute -right-5 top-20 hidden rounded-2xl border border-gray-200 bg-white p-4 shadow-lg sm:block">

            <div className="flex items-center gap-3">

              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gray-100 text-lg">
                🧠
              </div>

              <div>
                <p className="text-sm font-bold text-black">
                  Adaptive
                </p>

                <p className="text-xs text-gray-500">
                  Learns your level
                </p>
              </div>

            </div>
          </div>
        </div>

        {/* ========================================= */}
        {/* BOTTOM INFORMATION */}
        {/* ========================================= */}

        <div className="mt-20 flex w-full max-w-4xl flex-col items-center border-t border-gray-100 pt-10">

          <p className="text-sm font-medium text-gray-400">
            Designed for modern students
          </p>

          <div className="mt-5 flex flex-col items-center gap-4 text-sm text-gray-500 sm:flex-row sm:gap-8">
            <span>Primary</span>
            <span>Secondary</span>
            <span>A-Level</span>
            <span>Offline Learning</span>
            <span>AI Support</span>
          </div>
        </div>

      </div>
    </section>
  );
};

export default Hero;