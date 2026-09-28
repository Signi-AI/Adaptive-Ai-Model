import React, { useState } from "react";
import { Link } from "react-router-dom";

const Register: React.FC = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [educationLevel, setEducationLevel] = useState("");
  const [classLevel, setClassLevel] = useState("");

  return (
    <div className="min-h-screen bg-gray-50 px-4 py-10">
      <div className="mx-auto flex min-h-[90vh] max-w-md items-center justify-center">

        <div className="w-full rounded-2xl bg-white p-8 shadow-lg">

          {/* Logo */}
          <div className="mb-8 text-center">
           

            <h1 className="text-3xl font-bold text-gray-900">
              Create your account
            </h1>

            <p className="mt-2 text-gray-500">
              Start your personalized learning journey with LearnAI
            </p>
          </div>

          {/* Registration Form */}
          <form className="space-y-5">

            {/* Full Name */}
            <div>
              <label className="mb-2 block text-sm font-medium text-gray-700">
                Full Name
              </label>

              <input
                type="text"
                placeholder="Enter your full name"
                className="w-full rounded-lg border border-gray-300 px-4 py-3 outline-none transition focus:border-purple-600 focus:ring-2 focus:ring-purple-100"
              />
            </div>

            {/* Email */}
            <div>
              <label className="mb-2 block text-sm font-medium text-gray-700">
                Email
              </label>

              <input
                type="email"
                placeholder="Enter your email"
                className="w-full rounded-lg border border-gray-300 px-4 py-3 outline-none transition focus:border-purple-600 focus:ring-2 focus:ring-purple-100"
              />
            </div>

            {/* Education Level */}
            <div>
              <label className="mb-2 block text-sm font-medium text-gray-700">
                Level of Education
              </label>

              <select
                value={educationLevel}
                onChange={(e) => {
                  setEducationLevel(e.target.value);
                  setClassLevel("");
                }}
                className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-700 outline-none transition focus:border-purple-600 focus:ring-2 focus:ring-purple-100"
              >
                <option value="">Select education level</option>

                <option value="Primary">
                  Primary School
                </option>

                <option value="O-Level">
                  O-Level
                </option>

                <option value="A-Level">
                  A-Level
                </option>

                <option value="College">
                  College
                </option>

                <option value="University">
                  University
                </option>
              </select>
            </div>

            {/* Class / Form */}
            <div>
              <label className="mb-2 block text-sm font-medium text-gray-700">
                Class / Form
              </label>

              <select
                value={classLevel}
                onChange={(e) => setClassLevel(e.target.value)}
                disabled={!educationLevel}
                className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-700 outline-none transition focus:border-purple-600 focus:ring-2 focus:ring-purple-100 disabled:cursor-not-allowed disabled:bg-gray-100"
              >
                <option value="">
                  {educationLevel
                    ? "Select your class"
                    : "Select education level first"}
                </option>

                {/* Primary School */}
                {educationLevel === "Primary" && (
                  <>
                    <option value="Standard 1">
                      Standard 1
                    </option>

                    <option value="Standard 2">
                      Standard 2
                    </option>

                    <option value="Standard 3">
                      Standard 3
                    </option>

                    <option value="Standard 4">
                      Standard 4
                    </option>

                    <option value="Standard 5">
                      Standard 5
                    </option>

                    <option value="Standard 6">
                      Standard 6
                    </option>

                    <option value="Standard 7">
                      Standard 7
                    </option>
                  </>
                )}

                {/* O-Level */}
                {educationLevel === "O-Level" && (
                  <>
                    <option value="Form 1">
                      Form 1
                    </option>

                    <option value="Form 2">
                      Form 2
                    </option>

                    <option value="Form 3">
                      Form 3
                    </option>

                    <option value="Form 4">
                      Form 4
                    </option>
                  </>
                )}

                {/* A-Level */}
                {educationLevel === "A-Level" && (
                  <>
                    <option value="Form 5">
                      Form 5
                    </option>

                    <option value="Form 6">
                      Form 6
                    </option>
                  </>
                )}

                {/* College */}
                {educationLevel === "College" && (
                  <>
                    <option value="Certificate">
                      Certificate
                    </option>

                    <option value="Diploma">
                      Diploma
                    </option>
                  </>
                )}

                {/* University */}
                {educationLevel === "University" && (
                  <>
                    <option value="Year 1">
                      Year 1
                    </option>

                    <option value="Year 2">
                      Year 2
                    </option>

                    <option value="Year 3">
                      Year 3
                    </option>

                    <option value="Year 4">
                      Year 4
                    </option>

                    <option value="Year 5">
                      Year 5
                    </option>
                  </>
                )}
              </select>
            </div>

            {/* Password */}
            <div>
              <label className="mb-2 block text-sm font-medium text-gray-700">
                Password
              </label>

              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  placeholder="Create a password"
                  className="w-full rounded-lg border border-gray-300 px-4 py-3 pr-20 outline-none transition focus:border-purple-600 focus:ring-2 focus:ring-purple-100"
                />

                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-sm font-medium text-purple-600"
                >
                  {showPassword ? "Hide" : "Show"}
                </button>
              </div>
            </div>

            {/* Confirm Password */}
            <div>
              <label className="mb-2 block text-sm font-medium text-gray-700">
                Confirm Password
              </label>

              <input
                type="password"
                placeholder="Confirm your password"
                className="w-full rounded-lg border border-gray-300 px-4 py-3 outline-none transition focus:border-purple-600 focus:ring-2 focus:ring-purple-100"
              />
            </div>

            {/* Create Account */}
            <button
              type="submit"
              className="w-full rounded-lg bg-purple-600 py-3 font-semibold text-white transition hover:bg-purple-700"
            >
              Create Account
            </button>
          </form>

          {/* Login */}
          <p className="mt-6 text-center text-sm text-gray-600">
            Already have an account?{" "}

            <Link
              to="/login"
              className="font-semibold text-purple-600 hover:text-purple-700"
            >
              Login
            </Link>
          </p>

        </div>
      </div>
    </div>
  );
};

export default Register;
