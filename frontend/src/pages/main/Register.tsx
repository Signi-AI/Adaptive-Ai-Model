import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import logo from "../../assets/logo.jpeg";
import heroBg from "../../assets/herobg.jpeg";
import { registerStudent, signIn } from "../../lib/api";

const toRegisteredClassLevel = (classLevel: string) => {
  const standard = /^Standard ([1-7])$/.exec(classLevel);
  if (standard) return `STD_${standard[1]}`;

  const form = /^Form ([1-6])$/.exec(classLevel);
  if (form) return `FORM_${form[1]}`;

  return null;
};

const Register: React.FC = () => {
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const [educationLevel, setEducationLevel] = useState("");
  const [classLevel, setClassLevel] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError("");

    const form = new FormData(event.currentTarget);
    const fullName = String(form.get("full_name") || "").trim();
    const username = String(form.get("username") || "").trim();
    const password = String(form.get("password") || "");
    const confirmPassword = String(form.get("confirm_password") || "");
    const registeredClassLevel = toRegisteredClassLevel(classLevel);

    if (password !== confirmPassword) {
      setError("The passwords do not match.");
      return;
    }

    if (!registeredClassLevel) {
      setError("Registration currently supports Standard 1–7 and Form 1–6.");
      return;
    }

    setIsSubmitting(true);
    try {
      await registerStudent({
        username,
        full_name: fullName,
        password,
        class_level: registeredClassLevel,
      });
      // Sign in immediately so this browser switches to the new student's
      // own profile, progress, recommendations, and tutor context.
      await signIn(username, password);
      navigate("/tutorhome", { replace: true });
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unable to create the account. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div
      className="relative min-h-screen w-full bg-cover bg-center bg-no-repeat px-4 py-12"
      style={{ backgroundImage: `url(${heroBg})` }}
    >
      {/* Semi-transparent overlay */}
      <div className="absolute inset-0 bg-white/80 backdrop-blur-[2px]" />

      <div className="relative z-10 mx-auto flex min-h-[90vh] max-w-md items-center justify-center">

        <div className="w-full rounded-3xl border border-gray-100 bg-white/95 p-8 shadow-xl backdrop-blur-md">

          {/* Header & Logo */}
          <div className="mb-8 text-center">
            <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center overflow-hidden rounded-full ring-4 ring-purple-100 shadow-md">
              <img
                src={logo}
                alt="LearnAI Logo"
                className="h-full w-full object-cover"
              />
            </div>

            <h1 className="text-3xl font-extrabold tracking-tight text-gray-900">
              Create your account
            </h1>

            <p className="mt-2 text-sm text-gray-500">
              Start your personalized learning journey with LearnAI
            </p>
          </div>

          {/* Registration Form */}
          <form className="space-y-4" onSubmit={handleSubmit}>

            {error && (
              <div role="alert" className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                {error}
              </div>
            )}

            {/* Full Name */}
            <div>
              <label className="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-gray-700">
                Full Name
              </label>

              <input
                type="text"
                name="full_name"
                placeholder="Enter your full name"
                required
                className="w-full rounded-xl border border-gray-200 bg-white/80 px-4 py-3 text-sm text-gray-900 outline-none transition-all duration-200 focus:border-purple-600 focus:bg-white focus:ring-2 focus:ring-purple-100"
              />
            </div>

            {/* Username */}
            <div>
              <label className="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-gray-700">
                Username
              </label>

              <input
                type="text"
                name="username"
                placeholder="Choose a username"
                minLength={3}
                maxLength={32}
                pattern="[A-Za-z0-9_]+"
                required
                className="w-full rounded-xl border border-gray-200 bg-white/80 px-4 py-3 text-sm text-gray-900 outline-none transition-all duration-200 focus:border-purple-600 focus:bg-white focus:ring-2 focus:ring-purple-100"
              />
            </div>

            {/* Education Level */}
            <div>
              <label className="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-gray-700">
                Level of Education
              </label>

              <select
                value={educationLevel}
                onChange={(e) => {
                  setEducationLevel(e.target.value);
                  setClassLevel("");
                }}
                required
                className="w-full rounded-xl border border-gray-200 bg-white/80 px-4 py-3 text-sm text-gray-900 outline-none transition-all duration-200 focus:border-purple-600 focus:bg-white focus:ring-2 focus:ring-purple-100"
              >
                <option value="">Select education level</option>
                <option value="Primary">Primary School</option>
                <option value="O-Level">O-Level</option>
                <option value="A-Level">A-Level</option>
                <option value="College">College</option>
                <option value="University">University</option>
              </select>
            </div>

            {/* Class / Form */}
            <div>
              <label className="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-gray-700">
                Class / Form
              </label>

              <select
                value={classLevel}
                onChange={(e) => setClassLevel(e.target.value)}
                disabled={!educationLevel}
                required
                className="w-full rounded-xl border border-gray-200 bg-white/80 px-4 py-3 text-sm text-gray-900 outline-none transition-all duration-200 focus:border-purple-600 focus:bg-white focus:ring-2 focus:ring-purple-100 disabled:cursor-not-allowed disabled:bg-gray-100 disabled:text-gray-400"
              >
                <option value="">
                  {educationLevel
                    ? "Select your class"
                    : "Select education level first"}
                </option>

                {/* Primary School */}
                {educationLevel === "Primary" && (
                  <>
                    <option value="Standard 1">Standard 1</option>
                    <option value="Standard 2">Standard 2</option>
                    <option value="Standard 3">Standard 3</option>
                    <option value="Standard 4">Standard 4</option>
                    <option value="Standard 5">Standard 5</option>
                    <option value="Standard 6">Standard 6</option>
                    <option value="Standard 7">Standard 7</option>
                  </>
                )}

                {/* O-Level */}
                {educationLevel === "O-Level" && (
                  <>
                    <option value="Form 1">Form 1</option>
                    <option value="Form 2">Form 2</option>
                    <option value="Form 3">Form 3</option>
                    <option value="Form 4">Form 4</option>
                  </>
                )}

                {/* A-Level */}
                {educationLevel === "A-Level" && (
                  <>
                    <option value="Form 5">Form 5</option>
                    <option value="Form 6">Form 6</option>
                  </>
                )}

                {/* College */}
                {educationLevel === "College" && (
                  <>
                    <option value="Certificate">Certificate</option>
                    <option value="Diploma">Diploma</option>
                  </>
                )}

                {/* University */}
                {educationLevel === "University" && (
                  <>
                    <option value="Year 1">Year 1</option>
                    <option value="Year 2">Year 2</option>
                    <option value="Year 3">Year 3</option>
                    <option value="Year 4">Year 4</option>
                    <option value="Year 5">Year 5</option>
                  </>
                )}
              </select>
            </div>

            {/* Password */}
            <div>
              <label className="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-gray-700">
                Password
              </label>

              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  name="password"
                  placeholder="Create a password"
                  minLength={4}
                  required
                  className="w-full rounded-xl border border-gray-200 bg-white/80 px-4 py-3 pr-16 text-sm text-gray-900 outline-none transition-all duration-200 focus:border-purple-600 focus:bg-white focus:ring-2 focus:ring-purple-100"
                />

                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-xs font-bold uppercase tracking-wider text-purple-600 hover:text-purple-700"
                >
                  {showPassword ? "Hide" : "Show"}
                </button>
              </div>
            </div>

            {/* Confirm Password */}
            <div>
              <label className="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-gray-700">
                Confirm Password
              </label>

              <input
                type="password"
                name="confirm_password"
                placeholder="Confirm your password"
                minLength={4}
                required
                className="w-full rounded-xl border border-gray-200 bg-white/80 px-4 py-3 text-sm text-gray-900 outline-none transition-all duration-200 focus:border-purple-600 focus:bg-white focus:ring-2 focus:ring-purple-100"
              />
            </div>

            {/* Create Account Button */}
            <button
              type="submit"
              disabled={isSubmitting}
              className="mt-2 w-full rounded-xl bg-gray-900 py-3.5 text-sm font-semibold text-white shadow-lg shadow-gray-900/10 transition-all duration-300 hover:bg-purple-600 hover:shadow-purple-500/25 hover:-translate-y-0.5 active:scale-95 disabled:cursor-not-allowed disabled:opacity-70"
            >
              {isSubmitting ? "Creating account..." : "Create Account →"}
            </button>
          </form>

          {/* Footer Link */}
          <p className="mt-6 text-center text-sm text-gray-600">
            Already have an account?{" "}
            <Link
              to="/login"
              className="font-bold text-purple-600 hover:text-purple-700 hover:underline"
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
