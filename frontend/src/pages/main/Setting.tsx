import React, { useState} from "react";
import { useNavigate } from "react-router-dom";
import {
  User,
  Bell,
  Lock,
  Moon,
  Save,
  Check,
  ArrowLeft,
  Sparkles,
} from "lucide-react";
<<<<<<< HEAD
import logo from "../../assets/logo.jpeg";
import StudentSidebar from "./StudentSidebar";
=======
>>>>>>> 6d22643 (student frontend development)

interface UserSettings {
  fullName: string;
  email: string;
  bio: string;
  emailNotifications: boolean;
  pushNotifications: boolean;
  aiInsightsAlerts: boolean;
  theme: "dark" | "light" | "system";
  twoFactorAuth: boolean;
}

const DEFAULT_SETTINGS: UserSettings = {
  fullName: "Alex Rivera",
  email: "alex.rivera@learnai.edu",
  bio: "Senior High School Student interested in Physics & Computer Science.",
  emailNotifications: true,
  pushNotifications: true,
  aiInsightsAlerts: true,
  theme: "dark",
  twoFactorAuth: false,
};

const Settings: React.FC = () => {
  const navigate = useNavigate();

<<<<<<< HEAD
  // Load persistent settings from LocalStorage
  const [settings, setSettings] = useState<UserSettings>(() => {
    const saved = localStorage.getItem("student_settings_data");
    return saved ? JSON.parse(saved) : DEFAULT_SETTINGS;
  });

  const [activeTab, setActiveTab] = useState<"profile" | "notifications" | "security" | "appearance">("profile");
  const [savedSuccess, setSavedSuccess] = useState(false);

  // Handle Save
  const handleSaveSettings = (e: React.FormEvent) => {
    e.preventDefault();
    localStorage.setItem("student_settings_data", JSON.stringify(settings));
    setSavedSuccess(true);
    setTimeout(() => setSavedSuccess(false), 3000);
  };

  return (
    <div className="min-h-screen bg-white font-sans text-slate-100 antialiased">
      <div>
        <StudentSidebar />
      </div>

      <div className="ml-60">
        {/* BACKGROUND GLOW */}
        <div className="fixed inset-0 pointer-events-none overflow-hidden">
          <div className="absolute -left-40 -top-40 h-96 w-96 rounded-full bg-purple-600/15 blur-3xl" />
          <div className="absolute right-0 top-1/3 h-96 w-96 rounded-full bg-blue-600/10 blur-3xl" />
        </div>

        <div className="relative mx-auto max-w-5xl px-4 py-8 md:px-8">
          {/* HEADER */}
          <header className="mb-8 flex items-center justify-between border-b border-slate-800 pb-6">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center overflow-hidden rounded-xl ring-2 ring-purple-500/30 shadow-lg shadow-purple-500/10">
                <img src={logo} alt="Brand Logo" className="h-full w-full object-cover" />
              </div>
              <div>
                <h1 className="text-base font-extrabold tracking-tight text-white">
                  LearnAI Studio
                </h1>
                <p className="text-[11px] font-medium text-slate-400">
                  Account & System Preferences
                </p>
              </div>
=======
  const [settings, setSettings] =
    useState<UserSettings>(() => {
      try {
        const saved =
          localStorage.getItem(
            "student_settings_data"
          );

        if (saved) {
          return JSON.parse(saved);
        }
      } catch {
        // Ignore invalid localStorage data
      }

      return DEFAULT_SETTINGS;
    });

  const [activeTab, setActiveTab] =
    useState<
      | "profile"
      | "notifications"
      | "security"
      | "appearance"
    >("profile");

  const [savedSuccess, setSavedSuccess] =
    useState(false);

  const handleSaveSettings = (
    event: React.FormEvent
  ) => {
    event.preventDefault();

    localStorage.setItem(
      "student_settings_data",
      JSON.stringify(settings)
    );

    setSavedSuccess(true);

    setTimeout(() => {
      setSavedSuccess(false);
    }, 3000);
  };

  const updateSetting = <
    K extends keyof UserSettings
  >(
    key: K,
    value: UserSettings[K]
  ) => {
    setSettings((previous) => ({
      ...previous,
      [key]: value,
    }));
  };

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-800 antialiased">

      {/* HEADER */}
      <header className="sticky top-0 z-30 border-b border-slate-200 bg-white/95 px-8 py-4 backdrop-blur-xl">
        <div className="mx-auto flex max-w-5xl items-center justify-between">

          <div>
            <h1 className="text-lg font-extrabold text-slate-800">
              Settings
            </h1>

            <p className="text-xs text-slate-400">
              Account & system preferences
            </p>
          </div>

          <button
            onClick={() =>
              navigate("/profile")
            }
            className="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-xs font-semibold text-slate-600 transition hover:border-blue-200 hover:bg-blue-50 hover:text-blue-600"
          >
            <ArrowLeft size={15} />
            Back to Profile
          </button>

        </div>
      </header>

      {/* MAIN */}
      <main className="mx-auto max-w-5xl p-6 md:p-8">

        {/* PAGE INTRO */}
        <div className="mb-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm md:p-7">

          <div className="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">

            <div>

              <div className="mb-2 inline-flex items-center gap-2 rounded-full bg-blue-50 px-3 py-1.5 text-xs font-semibold text-blue-600">
                <ShieldCheck size={13} />
                Account Preferences
              </div>

              <h2 className="text-2xl font-extrabold tracking-tight text-slate-800">
                Settings
              </h2>

              <p className="mt-1 max-w-xl text-xs leading-5 text-slate-500">
                Manage your personal information,
                notifications, security and
                appearance preferences.
              </p>

>>>>>>> 6d22643 (student frontend development)
            </div>

            {savedSuccess && (
              <div className="flex items-center gap-2 rounded-xl border border-green-200 bg-green-50 px-4 py-2.5 text-xs font-bold text-green-600">
                <Check size={16} />
                Changes Saved
              </div>
            )}

          </div>
        </div>

        {/* SETTINGS */}
        <div className="grid grid-cols-1 gap-6 md:grid-cols-4">

          {/* TABS */}
          <div className="h-fit rounded-2xl border border-slate-200 bg-white p-2 shadow-sm">

            {/* PROFILE */}
            <button
<<<<<<< HEAD
              onClick={() => navigate("/profile")}
              className="flex items-center gap-2 rounded-xl border border-slate-800 bg-slate-800/60 px-4 py-2 text-xs font-semibold text-slate-300 hover:bg-slate-800 hover:text-white transition-all"
            >
              <ArrowLeft size={14} /> Back to Profile
            </button>
          </header>

          {/* PAGE BANNER */}
          <div className="mb-8 rounded-3xl border border-slate-800 bg-gradient-to-r from-slate-900 via-purple-950/30 to-slate-900 p-6 md:p-8 shadow-xl">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <span className="inline-flex items-center gap-1.5 rounded-full border border-purple-500/30 bg-purple-500/10 px-3 py-1 text-xs font-semibold text-purple-300 mb-2">
                  <Sparkles size={12} /> Portal Preferences
                </span>
                <h2 className="text-2xl font-extrabold text-white">Settings</h2>
                <p className="text-xs text-slate-400 mt-1">
                  Manage your personal details, notification alerts, and account security.
                </p>
              </div>

              {savedSuccess && (
                <div className="flex items-center gap-2 rounded-2xl border border-emerald-500/30 bg-emerald-500/10 px-4 py-2 text-xs font-bold text-emerald-400 animate-pulse">
                  <Check size={16} /> Changes Saved!
                </div>
              )}
            </div>
          </div>

          {/* MAIN SETTINGS CONTAINER */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            {/* TABS SIDEBAR */}
            <div className="space-y-1 rounded-2xl border border-slate-800 bg-slate-800/30 p-2 h-fit">
              <button
                onClick={() => setActiveTab("profile")}
                className={`w-full flex items-center gap-3 rounded-xl px-4 py-3 text-xs font-semibold transition-all ${
                  activeTab === "profile"
                    ? "bg-purple-600 text-white shadow-md shadow-purple-600/20"
                    : "text-slate-400 hover:text-white hover:bg-slate-800/50"
                }`}
              >
                <User size={16} /> Profile Details
              </button>

              <button
                onClick={() => setActiveTab("notifications")}
                className={`w-full flex items-center gap-3 rounded-xl px-4 py-3 text-xs font-semibold transition-all ${
                  activeTab === "notifications"
                    ? "bg-purple-600 text-white shadow-md shadow-purple-600/20"
                    : "text-slate-400 hover:text-white hover:bg-slate-800/50"
                }`}
              >
                <Bell size={16} /> Notifications
              </button>

              <button
                onClick={() => setActiveTab("security")}
                className={`w-full flex items-center gap-3 rounded-xl px-4 py-3 text-xs font-semibold transition-all ${
                  activeTab === "security"
                    ? "bg-purple-600 text-white shadow-md shadow-purple-600/20"
                    : "text-slate-400 hover:text-white hover:bg-slate-800/50"
                }`}
              >
                <Lock size={16} /> Security
              </button>

              <button
                onClick={() => setActiveTab("appearance")}
                className={`w-full flex items-center gap-3 rounded-xl px-4 py-3 text-xs font-semibold transition-all ${
                  activeTab === "appearance"
                    ? "bg-purple-600 text-white shadow-md shadow-purple-600/20"
                    : "text-slate-400 hover:text-white hover:bg-slate-800/50"
                }`}
              >
                <Moon size={16} /> Appearance
              </button>
            </div>

            {/* TAB CONTENT PANEL */}
            <div className="md:col-span-3 rounded-3xl border border-slate-800 bg-slate-800/40 p-6 backdrop-blur-md">
              <form onSubmit={handleSaveSettings}>
                {/* PROFILE TAB */}
                {activeTab === "profile" && (
                  <div className="space-y-4">
                    <h3 className="text-base font-bold text-white mb-4 border-b border-slate-800 pb-3">
                      Profile Details
                    </h3>

                    <div>
                      <label className="block text-xs font-semibold text-slate-300 mb-1">
                        Full Name
                      </label>
                      <input
                        type="text"
                        value={settings.fullName}
                        onChange={(e) => setSettings({ ...settings, fullName: e.target.value })}
                        className="w-full rounded-xl border border-slate-800 bg-slate-950 p-3 text-xs text-white outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-semibold text-slate-300 mb-1">
                        Email Address
                      </label>
                      <input
                        type="email"
                        value={settings.email}
                        onChange={(e) => setSettings({ ...settings, email: e.target.value })}
                        className="w-full rounded-xl border border-slate-800 bg-slate-950 p-3 text-xs text-white outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-semibold text-slate-300 mb-1">
                        Student Bio
                      </label>
                      <textarea
                        rows={3}
                        value={settings.bio}
                        onChange={(e) => setSettings({ ...settings, bio: e.target.value })}
                        className="w-full rounded-xl border border-slate-800 bg-slate-950 p-3 text-xs text-white outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20 resize-none"
                      />
=======
              type="button"
              onClick={() =>
                setActiveTab("profile")
              }
              className={`mb-1 flex w-full items-center gap-3 rounded-xl px-4 py-3 text-xs font-semibold transition ${
                activeTab === "profile"
                  ? "bg-blue-600 text-white shadow-sm"
                  : "text-slate-500 hover:bg-slate-50 hover:text-slate-800"
              }`}
            >
              <User size={16} />
              Profile Details
            </button>

            {/* NOTIFICATIONS */}
            <button
              type="button"
              onClick={() =>
                setActiveTab(
                  "notifications"
                )
              }
              className={`mb-1 flex w-full items-center gap-3 rounded-xl px-4 py-3 text-xs font-semibold transition ${
                activeTab === "notifications"
                  ? "bg-blue-600 text-white shadow-sm"
                  : "text-slate-500 hover:bg-slate-50 hover:text-slate-800"
              }`}
            >
              <Bell size={16} />
              Notifications
            </button>

            {/* SECURITY */}
            <button
              type="button"
              onClick={() =>
                setActiveTab("security")
              }
              className={`mb-1 flex w-full items-center gap-3 rounded-xl px-4 py-3 text-xs font-semibold transition ${
                activeTab === "security"
                  ? "bg-blue-600 text-white shadow-sm"
                  : "text-slate-500 hover:bg-slate-50 hover:text-slate-800"
              }`}
            >
              <Lock size={16} />
              Security
            </button>

            {/* APPEARANCE */}
            <button
              type="button"
              onClick={() =>
                setActiveTab("appearance")
              }
              className={`flex w-full items-center gap-3 rounded-xl px-4 py-3 text-xs font-semibold transition ${
                activeTab === "appearance"
                  ? "bg-blue-600 text-white shadow-sm"
                  : "text-slate-500 hover:bg-slate-50 hover:text-slate-800"
              }`}
            >
              <Moon size={16} />
              Appearance
            </button>

          </div>

          {/* CONTENT */}
          <div className="md:col-span-3">

            <div className="rounded-3xl border border-slate-200 bg-white shadow-sm">

              <form
                onSubmit={
                  handleSaveSettings
                }
              >

                {/* PROFILE */}
                {activeTab === "profile" && (
                  <div className="p-6 md:p-8">

                    <div className="mb-7 border-b border-slate-200 pb-5">

                      <p className="text-xs font-bold uppercase tracking-wider text-blue-600">
                        Account
                      </p>

                      <h3 className="mt-1 text-xl font-bold text-slate-800">
                        Profile Details
                      </h3>

                      <p className="mt-1 text-xs text-slate-400">
                        Update your basic account
                        information.
                      </p>

                    </div>

                    <div className="space-y-5">

                      {/* FULL NAME */}
                      <div>

                        <label className="mb-2 block text-xs font-semibold text-slate-600">
                          Full Name
                        </label>

                        <input
                          type="text"
                          value={
                            settings.fullName
                          }
                          onChange={(event) =>
                            updateSetting(
                              "fullName",
                              event.target.value
                            )
                          }
                          className="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-700 outline-none transition placeholder:text-slate-400 focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10"
                        />

                      </div>

                      {/* EMAIL */}
                      <div>

                        <label className="mb-2 block text-xs font-semibold text-slate-600">
                          Email Address
                        </label>

                        <input
                          type="email"
                          value={
                            settings.email
                          }
                          onChange={(event) =>
                            updateSetting(
                              "email",
                              event.target.value
                            )
                          }
                          className="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-700 outline-none transition placeholder:text-slate-400 focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10"
                        />

                      </div>

                      {/* BIO */}
                      <div>

                        <label className="mb-2 block text-xs font-semibold text-slate-600">
                          Student Bio
                        </label>

                        <textarea
                          rows={4}
                          value={
                            settings.bio
                          }
                          onChange={(event) =>
                            updateSetting(
                              "bio",
                              event.target.value
                            )
                          }
                          className="w-full resize-none rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-700 outline-none transition placeholder:text-slate-400 focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10"
                        />

                      </div>

>>>>>>> 6d22643 (student frontend development)
                    </div>
                  </div>
                )}

<<<<<<< HEAD
                {/* NOTIFICATIONS TAB */}
                {activeTab === "notifications" && (
                  <div className="space-y-4">
                    <h3 className="text-base font-bold text-white mb-4 border-b border-slate-800 pb-3">
                      Notification Preferences
                    </h3>

                    <div className="flex items-center justify-between p-3 rounded-2xl border border-slate-800 bg-slate-950/60">
                      <div>
                        <p className="text-xs font-bold text-white">Email Notifications</p>
                        <p className="text-[11px] text-slate-400">Receive assignment updates via email.</p>
                      </div>
                      <input
                        type="checkbox"
                        checked={settings.emailNotifications}
                        onChange={(e) =>
                          setSettings({ ...settings, emailNotifications: e.target.checked })
                        }
                        className="h-4 w-4 rounded accent-purple-600 cursor-pointer"
                      />
                    </div>

                    <div className="flex items-center justify-between p-3 rounded-2xl border border-slate-800 bg-slate-950/60">
                      <div>
                        <p className="text-xs font-bold text-white">In-App Push Notifications</p>
                        <p className="text-[11px] text-slate-400">Get instant alerts for grades and homework.</p>
                      </div>
                      <input
                        type="checkbox"
                        checked={settings.pushNotifications}
                        onChange={(e) =>
                          setSettings({ ...settings, pushNotifications: e.target.checked })
                        }
                        className="h-4 w-4 rounded accent-purple-600 cursor-pointer"
                      />
                    </div>

                    <div className="flex items-center justify-between p-3 rounded-2xl border border-slate-800 bg-slate-950/60">
                      <div>
                        <p className="text-xs font-bold text-white">AI Learning Insights</p>
                        <p className="text-[11px] text-slate-400">Receive personalized study prompts from LearnAI.</p>
                      </div>
                      <input
                        type="checkbox"
                        checked={settings.aiInsightsAlerts}
                        onChange={(e) =>
                          setSettings({ ...settings, aiInsightsAlerts: e.target.checked })
                        }
                        className="h-4 w-4 rounded accent-purple-600 cursor-pointer"
                      />
                    </div>
                  </div>
                )}

                {/* SECURITY TAB */}
                {activeTab === "security" && (
                  <div className="space-y-4">
                    <h3 className="text-base font-bold text-white mb-4 border-b border-slate-800 pb-3">
                      Security & Passwords
                    </h3>

                    <div>
                      <label className="block text-xs font-semibold text-slate-300 mb-1">
                        Current Password
                      </label>
                      <input
                        type="password"
                        placeholder="••••••••"
                        className="w-full rounded-xl border border-slate-800 bg-slate-950 p-3 text-xs text-white outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-semibold text-slate-300 mb-1">
                        New Password
                      </label>
                      <input
                        type="password"
                        placeholder="••••••••"
                        className="w-full rounded-xl border border-slate-800 bg-slate-950 p-3 text-xs text-white outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20"
                      />
                    </div>

                    <div className="flex items-center justify-between p-3 rounded-2xl border border-slate-800 bg-slate-950/60 mt-4">
                      <div>
                        <p className="text-xs font-bold text-white">Two-Factor Authentication (2FA)</p>
                        <p className="text-[11px] text-slate-400">Add an extra layer of security to your account.</p>
                      </div>
                      <input
                        type="checkbox"
                        checked={settings.twoFactorAuth}
                        onChange={(e) =>
                          setSettings({ ...settings, twoFactorAuth: e.target.checked })
                        }
                        className="h-4 w-4 rounded accent-purple-600 cursor-pointer"
                      />
                    </div>
                  </div>
                )}

                {/* APPEARANCE TAB */}
                {activeTab === "appearance" && (
                  <div className="space-y-4">
                    <h3 className="text-base font-bold text-white mb-4 border-b border-slate-800 pb-3">
                      Appearance & Theme
                    </h3>

                    <div className="grid grid-cols-3 gap-3">
                      {(["dark", "light", "system"] as const).map((themeOption) => (
                        <button
                          key={themeOption}
                          type="button"
                          onClick={() => setSettings({ ...settings, theme: themeOption })}
                          className={`flex flex-col items-center gap-2 rounded-2xl border p-4 capitalize text-xs font-bold transition-all ${
                            settings.theme === themeOption
                              ? "border-purple-500 bg-purple-600/20 text-purple-300"
                              : "border-slate-800 bg-slate-950/60 text-slate-400 hover:text-white"
                          }`}
                        >
                          <Moon size={20} />
                          {themeOption}
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                {/* SAVE BUTTON */}
                <div className="mt-6 flex justify-end border-t border-slate-800 pt-4">
                  <button
                    type="submit"
                    className="inline-flex items-center gap-2 rounded-xl bg-purple-600 px-5 py-2.5 text-xs font-semibold text-white shadow-md shadow-purple-600/20 hover:bg-purple-500 transition-all active:scale-95"
                  >
                    <Save size={14} /> Save Preferences
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
=======
                {/* NOTIFICATIONS */}
                {activeTab ===
                  "notifications" && (
                  <div className="p-6 md:p-8">

                    <div className="mb-7 border-b border-slate-200 pb-5">

                      <p className="text-xs font-bold uppercase tracking-wider text-blue-600">
                        Alerts
                      </p>

                      <h3 className="mt-1 text-xl font-bold text-slate-800">
                        Notification Preferences
                      </h3>

                      <p className="mt-1 text-xs text-slate-400">
                        Choose how you want LearnAI
                        to notify you.
                      </p>

                    </div>

                    <div className="space-y-3">

                      {/* EMAIL */}
                      <div className="flex items-center justify-between gap-4 rounded-2xl border border-slate-200 bg-slate-50 p-5">

                        <div>

                          <p className="text-sm font-bold text-slate-800">
                            Email Notifications
                          </p>

                          <p className="mt-1 text-xs leading-5 text-slate-500">
                            Receive assignment and
                            academic updates through
                            email.
                          </p>

                        </div>

                        <button
                          type="button"
                          onClick={() =>
                            updateSetting(
                              "emailNotifications",
                              !settings.emailNotifications
                            )
                          }
                          className={`relative h-6 w-11 shrink-0 rounded-full transition ${
                            settings.emailNotifications
                              ? "bg-blue-600"
                              : "bg-slate-300"
                          }`}
                        >
                          <span
                            className={`absolute top-1 h-4 w-4 rounded-full bg-white shadow-sm transition ${
                              settings.emailNotifications
                                ? "left-6"
                                : "left-1"
                            }`}
                          />
                        </button>

                      </div>

                      {/* PUSH */}
                      <div className="flex items-center justify-between gap-4 rounded-2xl border border-slate-200 bg-slate-50 p-5">

                        <div>

                          <p className="text-sm font-bold text-slate-800">
                            In-App Notifications
                          </p>

                          <p className="mt-1 text-xs leading-5 text-slate-500">
                            Get alerts for grades,
                            assignments and important
                            updates.
                          </p>

                        </div>

                        <button
                          type="button"
                          onClick={() =>
                            updateSetting(
                              "pushNotifications",
                              !settings.pushNotifications
                            )
                          }
                          className={`relative h-6 w-11 shrink-0 rounded-full transition ${
                            settings.pushNotifications
                              ? "bg-blue-600"
                              : "bg-slate-300"
                          }`}
                        >
                          <span
                            className={`absolute top-1 h-4 w-4 rounded-full bg-white shadow-sm transition ${
                              settings.pushNotifications
                                ? "left-6"
                                : "left-1"
                            }`}
                          />
                        </button>

                      </div>

                      {/* AI */}
                      <div className="flex items-center justify-between gap-4 rounded-2xl border border-slate-200 bg-slate-50 p-5">

                        <div>

                          <p className="text-sm font-bold text-slate-800">
                            AI Learning Insights
                          </p>

                          <p className="mt-1 text-xs leading-5 text-slate-500">
                            Receive personalized learning
                            suggestions from LearnAI.
                          </p>

                        </div>

                        <button
                          type="button"
                          onClick={() =>
                            updateSetting(
                              "aiInsightsAlerts",
                              !settings.aiInsightsAlerts
                            )
                          }
                          className={`relative h-6 w-11 shrink-0 rounded-full transition ${
                            settings.aiInsightsAlerts
                              ? "bg-blue-600"
                              : "bg-slate-300"
                          }`}
                        >
                          <span
                            className={`absolute top-1 h-4 w-4 rounded-full bg-white shadow-sm transition ${
                              settings.aiInsightsAlerts
                                ? "left-6"
                                : "left-1"
                            }`}
                          />
                        </button>

                      </div>

                    </div>
                  </div>
                )}

                {/* SECURITY */}
                {activeTab ===
                  "security" && (
                  <div className="p-6 md:p-8">

                    <div className="mb-7 border-b border-slate-200 pb-5">

                      <p className="text-xs font-bold uppercase tracking-wider text-blue-600">
                        Protection
                      </p>

                      <h3 className="mt-1 text-xl font-bold text-slate-800">
                        Security
                      </h3>

                      <p className="mt-1 text-xs text-slate-400">
                        Keep your LearnAI account
                        secure.
                      </p>

                    </div>

                    <div className="space-y-5">

                      {/* CURRENT PASSWORD */}
                      <div>

                        <label className="mb-2 block text-xs font-semibold text-slate-600">
                          Current Password
                        </label>

                        <input
                          type="password"
                          placeholder="Enter current password"
                          className="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-700 outline-none transition placeholder:text-slate-400 focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10"
                        />

                      </div>

                      {/* NEW PASSWORD */}
                      <div>

                        <label className="mb-2 block text-xs font-semibold text-slate-600">
                          New Password
                        </label>

                        <input
                          type="password"
                          placeholder="Enter new password"
                          className="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-700 outline-none transition placeholder:text-slate-400 focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10"
                        />

                      </div>

                      {/* CONFIRM PASSWORD */}
                      <div>

                        <label className="mb-2 block text-xs font-semibold text-slate-600">
                          Confirm New Password
                        </label>

                        <input
                          type="password"
                          placeholder="Confirm new password"
                          className="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-700 outline-none transition placeholder:text-slate-400 focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10"
                        />

                      </div>

                      {/* 2FA */}
                      <div className="flex items-center justify-between gap-4 rounded-2xl border border-slate-200 bg-slate-50 p-5">

                        <div>

                          <p className="text-sm font-bold text-slate-800">
                            Two-Factor Authentication
                          </p>

                          <p className="mt-1 text-xs leading-5 text-slate-500">
                            Add an extra layer of
                            protection to your account.
                          </p>

                        </div>

                        <button
                          type="button"
                          onClick={() =>
                            updateSetting(
                              "twoFactorAuth",
                              !settings.twoFactorAuth
                            )
                          }
                          className={`relative h-6 w-11 shrink-0 rounded-full transition ${
                            settings.twoFactorAuth
                              ? "bg-blue-600"
                              : "bg-slate-300"
                          }`}
                        >
                          <span
                            className={`absolute top-1 h-4 w-4 rounded-full bg-white shadow-sm transition ${
                              settings.twoFactorAuth
                                ? "left-6"
                                : "left-1"
                            }`}
                          />
                        </button>

                      </div>

                    </div>
                  </div>
                )}

                {/* APPEARANCE */}
                {activeTab ===
                  "appearance" && (
                  <div className="p-6 md:p-8">

                    <div className="mb-7 border-b border-slate-200 pb-5">

                      <p className="text-xs font-bold uppercase tracking-wider text-blue-600">
                        Interface
                      </p>

                      <h3 className="mt-1 text-xl font-bold text-slate-800">
                        Appearance
                      </h3>

                      <p className="mt-1 text-xs text-slate-400">
                        Choose how LearnAI should look.
                      </p>

                    </div>

                    <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">

                      {/* LIGHT */}
                      <button
                        type="button"
                        onClick={() =>
                          updateSetting(
                            "theme",
                            "light"
                          )
                        }
                        className={`rounded-2xl border p-5 text-left transition ${
                          settings.theme ===
                          "light"
                            ? "border-blue-500 bg-blue-50 ring-2 ring-blue-500/10"
                            : "border-slate-200 bg-white hover:border-blue-200 hover:bg-slate-50"
                        }`}
                      >

                        <div
                          className={`mb-4 flex h-11 w-11 items-center justify-center rounded-xl ${
                            settings.theme ===
                            "light"
                              ? "bg-blue-600 text-white"
                              : "bg-slate-100 text-slate-500"
                          }`}
                        >
                          <Sun size={20} />
                        </div>

                        <p className="text-sm font-bold text-slate-800">
                          Light
                        </p>

                        <p className="mt-1 text-xs text-slate-500">
                          Clean and bright
                          interface.
                        </p>

                      </button>

                      {/* DARK */}
                      <button
                        type="button"
                        onClick={() =>
                          updateSetting(
                            "theme",
                            "dark"
                          )
                        }
                        className={`rounded-2xl border p-5 text-left transition ${
                          settings.theme ===
                          "dark"
                            ? "border-blue-500 bg-blue-50 ring-2 ring-blue-500/10"
                            : "border-slate-200 bg-white hover:border-blue-200 hover:bg-slate-50"
                        }`}
                      >

                        <div
                          className={`mb-4 flex h-11 w-11 items-center justify-center rounded-xl ${
                            settings.theme ===
                            "dark"
                              ? "bg-blue-600 text-white"
                              : "bg-slate-100 text-slate-500"
                          }`}
                        >
                          <Moon size={20} />
                        </div>

                        <p className="text-sm font-bold text-slate-800">
                          Dark
                        </p>

                        <p className="mt-1 text-xs text-slate-500">
                          Dark interface for
                          low-light use.
                        </p>

                      </button>

                      {/* SYSTEM */}
                      <button
                        type="button"
                        onClick={() =>
                          updateSetting(
                            "theme",
                            "system"
                          )
                        }
                        className={`rounded-2xl border p-5 text-left transition ${
                          settings.theme ===
                          "system"
                            ? "border-blue-500 bg-blue-50 ring-2 ring-blue-500/10"
                            : "border-slate-200 bg-white hover:border-blue-200 hover:bg-slate-50"
                        }`}
                      >

                        <div
                          className={`mb-4 flex h-11 w-11 items-center justify-center rounded-xl ${
                            settings.theme ===
                            "system"
                              ? "bg-blue-600 text-white"
                              : "bg-slate-100 text-slate-500"
                          }`}
                        >
                          <Monitor size={20} />
                        </div>

                        <p className="text-sm font-bold text-slate-800">
                          System
                        </p>

                        <p className="mt-1 text-xs text-slate-500">
                          Follow your device
                          settings.
                        </p>

                      </button>

                    </div>

                    {/* CURRENT THEME */}
                    <div className="mt-6 rounded-2xl border border-slate-200 bg-slate-50 p-5">

                      <p className="text-xs font-semibold text-slate-500">
                        Current theme
                      </p>

                      <p className="mt-1 text-sm font-bold capitalize text-slate-800">
                        {settings.theme}
                      </p>

                    </div>

                  </div>
                )}

                {/* SAVE */}
                <div className="flex justify-end border-t border-slate-200 bg-slate-50 px-6 py-4 md:px-8">

                  <button
                    type="submit"
                    className="inline-flex items-center gap-2 rounded-xl bg-blue-600 px-5 py-3 text-xs font-semibold text-white shadow-sm transition hover:bg-blue-700 active:scale-[0.98]"
                  >
                    <Save size={15} />
                    Save Preferences
                  </button>

                </div>

              </form>

            </div>
          </div>
        </div>
      </main>
>>>>>>> 6d22643 (student frontend development)
    </div>
  );
};

export default Settings;