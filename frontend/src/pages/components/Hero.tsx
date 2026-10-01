import React from "react";
import { Link } from "react-router-dom";
import logo from "../../assets/logo.jpeg";
import heroBg from "../../assets/herobg.jpeg";

const Hero: React.FC = () => {
  const line1 = ["Learn", "Smarter"];
  const line2 = ["Learn", "Your", "Way"];

  return (
    <section
      className="relative overflow-hidden bg-cover bg-center bg-no-repeat px-6 pt-20 pb-16 text-center md:pt-28 md:pb-24"
      style={{ backgroundImage: `url(${heroBg})` }}
    >
      {/* Light semi-transparent overlay to ensure readability */}
      <div className="absolute inset-0 bg-white/75 backdrop-blur-[2px]" />

      {/* Glow Blur */}
      <div className="pointer-events-none absolute left-1/2 top-0 h-[400px] w-[600px] -translate-x-1/2 rounded-full bg-gradient-to-tr from-purple-300/30 to-indigo-200/20 blur-3xl" />

      <div className="relative z-10 mx-auto max-w-4xl">
        {/* Top Tag / Pill */}
        <div className="inline-flex items-center gap-2.5 rounded-full border border-purple-200/60 bg-white/90 px-4 py-1.5 text-xs font-semibold text-gray-800 shadow-sm backdrop-blur-md transition-all duration-300 hover:scale-105 hover:border-purple-300 hover:shadow-md cursor-default">
          <div className="relative flex h-5 w-5 items-center justify-center overflow-hidden rounded-full ring-2 ring-purple-100">
            <img
              src={logo}
              alt="LearnAI Logo"
              className="h-full w-full object-cover transition-transform duration-500 hover:scale-110"
            />
          </div>
          <span className="h-2 w-2 rounded-full bg-purple-600 animate-pulse"></span>
          <span className="tracking-wide">Offline Adaptive Learning</span>
        </div>

        {/* Headline */}
        <h1 className="mt-8 text-5xl font-black tracking-tight text-gray-900 sm:text-6xl md:text-7xl">
          <span className="flex flex-wrap justify-center gap-x-4">
            {line1.map((word, index) => (
              <span
                key={word}
                style={{ animationDelay: `${index * 150}ms` }}
                className="inline-block transition-all duration-300 hover:scale-105 hover:-translate-y-1 hover:text-purple-600 cursor-pointer"
              >
                {word}
              </span>
            ))}
          </span>

          <span className="mt-2 flex flex-wrap justify-center gap-x-4 text-gray-400">
            {line2.map((word, index) => (
              <span
                key={word}
                style={{ animationDelay: `${(index + line1.length) * 150}ms` }}
                className="inline-block transition-all duration-300 hover:scale-105 hover:-translate-y-1 hover:text-gray-900 cursor-pointer"
              >
                {word}
              </span>
            ))}
          </span>
        </h1>

        {/* Subtitle */}
        <p className="mx-auto mt-6 max-w-2xl text-base font-normal text-gray-600 sm:text-lg sm:leading-relaxed">
          An adaptive learning platform that understands your strengths, identifies your
          weaknesses, and adjusts your learning experience to your level — even when you
          are offline.
        </p>

        {/* Action Buttons */}
        <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link
            to="/register"
            className="group relative w-full sm:w-auto overflow-hidden rounded-2xl bg-gray-900 px-8 py-4 text-sm font-semibold text-white shadow-lg shadow-gray-900/10 transition-all duration-300 hover:bg-purple-600 hover:shadow-purple-500/25 hover:-translate-y-0.5 active:scale-95"
          >
            <span className="inline-flex items-center gap-2 transition-transform duration-200 group-hover:translate-x-1">
              Get Started
              <span className="text-base">&rarr;</span>
            </span>
          </Link>

          <a
            href="#how-it-works"
            className="w-full sm:w-auto rounded-2xl border border-gray-200/80 bg-white/90 px-8 py-4 text-sm font-semibold text-gray-800 shadow-sm backdrop-blur-md transition-all duration-300 hover:bg-gray-50 hover:border-gray-300 hover:shadow-md hover:-translate-y-0.5 active:scale-95"
          >
            How It Works
          </a>
        </div>

        {/* Highlights */}
        <div className="mt-12 flex flex-wrap items-center justify-center gap-8 text-xs font-semibold uppercase tracking-wider text-gray-600 sm:text-sm">
          <div className="flex items-center gap-2 transition-transform duration-200 hover:scale-105">
            <span className="flex h-5 w-5 items-center justify-center rounded-full bg-purple-100 text-purple-700 text-xs font-bold">
              ✓
            </span>
            <span>Works Offline</span>
          </div>

          <div className="flex items-center gap-2 transition-transform duration-200 hover:scale-105">
            <span className="flex h-5 w-5 items-center justify-center rounded-full bg-purple-100 text-purple-700 text-xs font-bold">
              ✓
            </span>
            <span>Personalized</span>
          </div>

          <div className="flex items-center gap-2 transition-transform duration-200 hover:scale-105">
            <span className="flex h-5 w-5 items-center justify-center rounded-full bg-purple-100 text-purple-700 text-xs font-bold">
              ✓
            </span>
            <span>Curriculum Aligned</span>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;