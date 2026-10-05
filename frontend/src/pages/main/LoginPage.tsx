import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { GoogleAuthProvider, signInWithPopup } from "firebase/auth";

import logo from "../../assets/logo.jpeg";
import heroBg from "../../assets/herobg.jpeg";
import { auth } from "../../../src/Firebase";

const Login: React.FC = () => {
  const navigate = useNavigate();

  const [showPassword, setShowPassword] = useState(false);
  const [loadingGoogle, setLoadingGoogle] = useState(false);
  const [error, setError] = useState("");

  // Email/password login
  const handleLogin = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    setError("");

    // Redirect to TutorHome
    navigate("/learn");
  };

  // Google Login
  const handleGoogleLogin = async () => {
    if (loadingGoogle) return;

    setError("");
    setLoadingGoogle(true);

    try {
      const provider = new GoogleAuthProvider();

      provider.setCustomParameters({
        prompt: "select_account",
      });

      const result = await signInWithPopup(auth, provider);

      const user = result.user;

      console.log("Google login successful:", {
        uid: user.uid,
        name: user.displayName,
        email: user.email,
        photo: user.photoURL,
      });

      // Redirect to TutorHome
      navigate("/learn");
    } catch (error: any) {
      console.error("Google login error:", error);

      switch (error?.code) {
        case "auth/popup-closed-by-user":
          setError("Google sign-in was cancelled.");
          break;

        case "auth/popup-blocked":
          setError(
            "Google sign-in popup was blocked. Please allow popups for this website."
          );
          break;

        case "auth/cancelled-popup-request":
          setError(
            "Another Google sign-in request is already running."
          );
          break;

        case "auth/unauthorized-domain":
          setError(
            "This website is not authorized in Firebase. Add your current domain in Firebase Authentication settings."
          );
          break;

        case "auth/api-key-not-valid":
          setError(
            "The Firebase API key is invalid. Check your Firebase configuration."
          );
          break;

        case "auth/account-exists-with-different-credential":
          setError(
            "An account already exists with this email using another sign-in method."
          );
          break;

        case "auth/network-request-failed":
          setError(
            "Network error. Please check your internet connection and try again."
          );
          break;

        default:
          setError(
            error?.message ||
              "Google sign-in failed. Please try again."
          );
      }
    } finally {
      setLoadingGoogle(false);
    }
  };

  return (
    <div
      className="relative min-h-screen w-full bg-cover bg-center bg-no-repeat px-4 py-12"
      style={{ backgroundImage: `url(${heroBg})` }}
    >
      {/* Background overlay */}
      <div className="absolute inset-0 bg-white/80 backdrop-blur-[2px]" />

      {/* Login container */}
      <div className="relative z-10 mx-auto flex min-h-[90vh] max-w-md items-center justify-center">
        <div className="w-full rounded-3xl border border-gray-100 bg-white/95 p-8 shadow-xl backdrop-blur-md">
          {/* Logo and heading */}
          <div className="mb-8 text-center">
            <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center overflow-hidden rounded-full ring-4 ring-purple-100 shadow-md">
              <img
                src={logo}
                alt="LearnAI Logo"
                className="h-full w-full object-cover"
              />
            </div>

            <h1 className="text-3xl font-extrabold tracking-tight text-gray-900">
              Welcome Back
            </h1>

            <p className="mt-2 text-sm text-gray-500">
              Login to continue your learning journey
            </p>
          </div>

          {/* Error message */}
          {error && (
            <div className="mb-5 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-600">
              {error}
            </div>
          )}

          {/* Google Login */}
          <button
            type="button"
            onClick={handleGoogleLogin}
            disabled={loadingGoogle}
            className={`flex w-full items-center justify-center gap-3 rounded-xl border border-gray-200 bg-white py-3 text-sm font-semibold text-gray-700 shadow-sm transition-all duration-300 ${
              loadingGoogle
                ? "cursor-not-allowed opacity-70"
                : "hover:border-gray-300 hover:bg-gray-50 hover:shadow-md active:scale-95"
            }`}
          >
            {loadingGoogle ? (
              <>
                <svg
                  className="h-5 w-5 animate-spin"
                  viewBox="0 0 24 24"
                  fill="none"
                >
                  <circle
                    cx="12"
                    cy="12"
                    r="9"
                    stroke="currentColor"
                    strokeWidth="3"
                    className="opacity-25"
                  />

                  <path
                    d="M21 12a9 9 0 0 0-9-9"
                    stroke="currentColor"
                    strokeWidth="3"
                    strokeLinecap="round"
                  />
                </svg>

                <span>Signing in...</span>
              </>
            ) : (
              <>
                {/* Google icon */}
                <svg
                  className="h-5 w-5"
                  viewBox="0 0 24 24"
                  aria-hidden="true"
                >
                  <path
                    fill="#4285F4"
                    d="M21.35 12.27c0-.68-.06-1.34-.17-1.97H12v3.73h5.23a4.47 4.47 0 0 1-1.94 2.93v2.44h3.14c1.84-1.69 2.92-4.18 2.92-7.13Z"
                  />

                  <path
                    fill="#34A853"
                    d="M12 21.99c2.63 0 4.84-.87 6.45-2.35l-3.14-2.44c-.87.58-1.98.92-3.31.92-2.54 0-4.69-1.72-5.46-4.03H3.3v2.52A9.75 9.75 0 0 0 12 21.99Z"
                  />

                  <path
                    fill="#FBBC05"
                    d="M6.54 14.09A5.86 5.86 0 0 1 6.23 12c0-.72.12-1.42.31-2.09V7.39H3.3A9.75 9.75 0 0 0 2.25 12c0 1.57.38 3.05 1.05 4.61l3.24-2.52Z"
                  />

                  <path
                    fill="#EA4335"
                    d="M12 5.88c1.43 0 2.71.49 3.72 1.45l2.79-2.79C16.83 2.96 14.63 2.01 12 2.01a9.75 9.75 0 0 0-8.7 5.38l3.24 2.52C7.31 7.6 9.46 5.88 12 5.88Z"
                  />
                </svg>

                <span>Continue with Google</span>
              </>
            )}
          </button>

          {/* Divider */}
          <div className="relative my-6 flex items-center justify-center">
            <div className="w-full border-t border-gray-200" />

            <span className="absolute bg-white px-3 text-xs font-semibold uppercase tracking-wider text-gray-400">
              Or continue with email
            </span>
          </div>

          {/* Email login form */}
          <form onSubmit={handleLogin} className="space-y-4">
            {/* Username / Email */}
            <div>
              <label
                htmlFor="email"
                className="mb-1.5 block text-sm font-semibold text-gray-700"
              >
                Username or Email
              </label>

              <input
                id="email"
                type="text"
                placeholder="Enter your username or email"
                required
                className="w-full rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 text-sm text-gray-900 outline-none transition focus:border-purple-500 focus:bg-white focus:ring-2 focus:ring-purple-100"
              />
            </div>

            {/* Password */}
            <div>
              <div className="mb-1.5 flex items-center justify-between">
                <label
                  htmlFor="password"
                  className="block text-sm font-semibold text-gray-700"
                >
                  Password
                </label>

                <Link
                  to="/forgot-password"
                  className="text-xs font-semibold text-purple-600 transition hover:text-purple-700"
                >
                  Forgot password?
                </Link>
              </div>

              <div className="relative">
                <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  placeholder="Enter your password"
                  required
                  className="w-full rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 pr-20 text-sm text-gray-900 outline-none transition focus:border-purple-500 focus:bg-white focus:ring-2 focus:ring-purple-100"
                />

                <button
                  type="button"
                  onClick={() =>
                    setShowPassword(!showPassword)
                  }
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-xs font-semibold text-gray-500 transition hover:text-purple-600"
                >
                  {showPassword ? "Hide" : "Show"}
                </button>
              </div>
            </div>

            {/* Login button */}
            <button
              type="submit"
              className="w-full rounded-xl bg-purple-600 py-3 text-sm font-bold text-white shadow-md transition-all duration-300 hover:bg-purple-700 hover:shadow-lg active:scale-[0.98]"
            >
              Login →
            </button>
          </form>

          {/* Register */}
          <p className="mt-6 text-center text-sm text-gray-600">
            Don't have an account?{" "}
            <Link
              to="/register"
              className="font-bold text-purple-600 transition hover:text-purple-700"
            >
              Create account
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;