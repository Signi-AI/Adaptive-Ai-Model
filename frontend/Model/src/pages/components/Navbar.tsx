import React from "react";
import { Link } from "react-router-dom";

const Navbar: React.FC = () => {
  return (
    <nav className="fixed top-0 z-50 w-full border-b border-gray-200 bg-white ">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-1 md:px-6">

        {/* Logo */}
        <Link
          to="/"
          className="text-2xl font-bold text-purple-600 mr-2"
        >
          LearnAI
        </Link>

        {/* Navigation */}
        <div className="flex items-center gap-2 md:gap-8">

          {/* Home */}
          <Link
            to="/"
            className="font-medium text-gray-700 transition hover:text-purple-600"
          >
            Home
          </Link>

          {/* Features - same page */}
          <a
            href="#features"
            className="font-medium text-gray-700 transition hover:text-purple-600"
          >
            Features
          </a>

          {/* About - same page */}
          <a
            href="#about"
            className="font-medium text-gray-700 transition hover:text-purple-600"
          >
            About
          </a>

          {/* Register */}
          <Link
            to="/register"
            className="font-medium text-gray-700 transition hover:text-purple-600"
          >
            Register
          </Link>

          {/* Login */}
          <Link
            to="/login"
            className="rounded-lg bg-purple-600 px-5 py-2.5 font-medium text-white transition hover:bg-purple-700"
          >
            Login
          </Link>

        </div>
      </div>
    </nav>
  );
};

export default Navbar;
