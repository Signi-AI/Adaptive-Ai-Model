import React from "react";
import { Link } from "react-router-dom";
import logo from "../../assets/logo.jpeg";

const Navbar: React.FC = () => {
  return (
    <nav className="fixed top-0 z-50 w-full border-b border-gray-100 bg-white/80 backdrop-blur-md transition-all duration-300">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 md:px-8">
        
        {/* Logo & Brand */}
        <Link
          to="/"
          className="group flex items-center gap-3 transition-transform duration-200 active:scale-95"
        >
          <div className="relative flex h-10 w-10 items-center justify-center overflow-hidden rounded-xl bg-purple-50 p-1 ring-1 ring-purple-100 transition-all duration-300 group-hover:scale-105 group-hover:shadow-md">
            <img
              src={logo}
              alt="LearnAI Logo"
              className="h-full w-full rounded-lg object-cover"
            />
          </div>
          <span className="text-xl font-bold tracking-tight text-gray-900 transition-colors duration-200 group-hover:text-purple-600">
            LearnAI
          </span>
        </Link>

        {/* Navigation Links */}
        <div className="flex items-center gap-3 text-sm font-semibold text-gray-600 md:gap-8">
          
          <Link
            to="/"
            className="transition-colors duration-200 hover:text-purple-600"
          >
            Home
          </Link>

          <a
            href="#features"
            className="transition-colors duration-200 hover:text-purple-600"
          >
            Features
          </a>

          <a
            href="#about"
            className="transition-colors duration-200 hover:text-purple-600"
          >
            About
          </a>

          <Link
            to="/register"
            className="transition-colors duration-200 hover:text-purple-600"
          >
            Register
          </Link>

          {/* Login Button */}
          <Link
            to="/login"
            className="rounded-xl bg-gray-900 px-5 py-2.5 font-semibold text-white shadow-sm transition-all duration-300 hover:bg-purple-600 hover:shadow-purple-500/20 hover:-translate-y-0.5 active:scale-95"
          >
            Login
          </Link>

        </div>
      </div>
    </nav>
  );
};

export default Navbar;