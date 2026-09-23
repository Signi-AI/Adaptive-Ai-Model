import React from "react";
import { Link } from "react-router-dom";

const AppHeader: React.FC = () => {
  return (
    <header className="sticky top-0 z-40 flex h-16 items-center justify-between border-b border-gray-200 bg-white/95 px-4 backdrop-blur-md sm:px-6">

      {/* Mobile Logo */}
      <Link
        to="/learning"
        className="flex items-center gap-2 lg:hidden"
      >
        <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-black text-sm font-bold text-white">
          A
        </div>

        <span className="text-sm font-bold text-black">
          AdaptiveLearn
        </span>
      </Link>

      {/* Desktop Page Title */}
      <div className="hidden lg:block">
        <p className="text-sm font-semibold text-black">
          Learning Dashboard
        </p>

        <p className="text-xs text-gray-400">
          Continue your learning journey
        </p>
      </div>

      {/* Right Side */}
      <div className="ml-auto flex items-center gap-3">

        {/* Offline */}
        <div className="hidden items-center gap-2 rounded-full border border-gray-200 bg-gray-50 px-3 py-2 sm:flex">

          <span className="h-2 w-2 rounded-full bg-green-500" />

          <span className="text-xs font-medium text-gray-600">
            Offline Ready
          </span>

        </div>

        {/* Notification */}
        <button
          type="button"
          className="flex h-9 w-9 items-center justify-center rounded-xl border border-gray-200 bg-white text-sm transition hover:bg-gray-100"
          aria-label="Notifications"
        >
          🔔
        </button>

        {/* Profile */}
        <Link
          to="/profile"
          className="flex h-9 w-9 items-center justify-center rounded-full bg-black text-[11px] font-bold text-white"
        >
          CM
        </Link>

      </div>
    </header>
  );
};

export default AppHeader;