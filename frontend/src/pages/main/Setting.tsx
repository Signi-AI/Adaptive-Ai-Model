import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  User,
  Bell,
  Lock,
  Moon,
  Sun,
  Monitor,
  Save,
  Check,
  ArrowLeft,
  ShieldCheck,
} from "lucide-react";
import StudentSidebar from "./StudentSidebar";

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
  fullName: "Comfotha Mwansasule",
  email: "student@learnai.edu",
  bio: "Student using LearnAI to improve learning and academic performance.",
  emailNotifications: true,
  pushNotifications: true,
  aiInsightsAlerts: true,
  theme: "light",
  twoFactorAuth: false,
};

const Settings: React.FC = () => {
  const navigate = useNavigate();

  const [settings, setSettings] = useState<UserSettings>(() => {
    try {
      const saved = localStorage.getItem("student_settings_data");

      if (saved) {
        return JSON.parse(saved);
      }
    } catch {
      // Ignore invalid localStorage data
    }

    return DEFAULT_SETTINGS;
  });

  const [activeTab, setActiveTab] = useState<
    "profile" | "notifications" | "security" | "appearance"
  >("profile");

  const [savedSuccess, setSavedSuccess] = useState(false);

  const handleSaveSettings = (event: React.FormEvent) => {
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

  const updateSetting = <K extends keyof UserSettings>(
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
      <StudentSidebar />

      <div className="ml-60">
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
              onClick={() => navigate("/profile")}
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
                  Manage your personal information, notifications,
                  security and appearance preferences.
                </p>
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
                type="button"
                onClick={() => setActiveTab("profile")}
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
                onClick={() => setActiveTab("notifications")}
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
                onClick={() => setActiveTab("security")}
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
                onClick={() => setActiveTab("appearance")}
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
                <form onSubmit={handleSaveSettings}>
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
                          Update your basic account information.
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
                            value={settings.fullName}
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
                            value={settings.email}
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
                            value={settings.bio}
                            onChange={(event) =>
                              updateSetting(
                                "bio",
                                event.target.value
                              )
                            }
                            className="w-full resize-none rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-700 outline-none transition placeholder:text-slate-400 focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10"
                          />
                        </div>
                      </div>
                    </div>
                  )}

                  {/* NOTIFICATIONS */}
                  {activeTab === "notifications" && (
                    <div className="p-6 md:p-8">
                      <div className="mb-7 border-b border-slate-200 pb-5">
                        <p className="text-xs font-bold uppercase tracking-wider text-blue-600">
                          Alerts
                        </p>

                        <h3 className="mt-1 text-xl font-bold text-slate-800">
                          Notification Preferences
                        </h3>

                        <p className="mt-1 text-xs text-slate-400">
                          Choose how you want LearnAI to notify you.
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
                              Receive assignment and academic updates
                              through email.
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
                              Get alerts for grades, assignments and
                              important updates.
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
                              Receive personalized learning suggestions
                              from LearnAI.
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
                  {activeTab === "security" && (
                    <div className="p-6 md:p-8">
                      <div className="mb-7 border-b border-slate-200 pb-5">
                        <p className="text-xs font-bold uppercase tracking-wider text-blue-600">
                          Protection
                        </p>

                        <h3 className="mt-1 text-xl font-bold text-slate-800">
                          Security
                        </h3>

                        <p className="mt-1 text-xs text-slate-400">
                          Keep your LearnAI account secure.
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
                              Add an extra layer of protection to your
                              account.
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
                  {activeTab === "appearance" && (
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
                            updateSetting("theme", "light")
                          }
                          className={`rounded-2xl border p-5 text-left transition ${
                            settings.theme === "light"
                              ? "border-blue-500 bg-blue-50 ring-2 ring-blue-500/10"
                              : "border-slate-200 bg-white hover:border-blue-200 hover:bg-slate-50"
                          }`}
                        >
                          <div
                            className={`mb-4 flex h-11 w-11 items-center justify-center rounded-xl ${
                              settings.theme === "light"
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
                            Clean and bright interface.
                          </p>
                        </button>

                        {/* DARK */}
                        <button
                          type="button"
                          onClick={() =>
                            updateSetting("theme", "dark")
                          }
                          className={`rounded-2xl border p-5 text-left transition ${
                            settings.theme === "dark"
                              ? "border-blue-500 bg-blue-50 ring-2 ring-blue-500/10"
                              : "border-slate-200 bg-white hover:border-blue-200 hover:bg-slate-50"
                          }`}
                        >
                          <div
                            className={`mb-4 flex h-11 w-11 items-center justify-center rounded-xl ${
                              settings.theme === "dark"
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
                            Dark interface for low-light use.
                          </p>
                        </button>

                        {/* SYSTEM */}
                        <button
                          type="button"
                          onClick={() =>
                            updateSetting("theme", "system")
                          }
                          className={`rounded-2xl border p-5 text-left transition ${
                            settings.theme === "system"
                              ? "border-blue-500 bg-blue-50 ring-2 ring-blue-500/10"
                              : "border-slate-200 bg-white hover:border-blue-200 hover:bg-slate-50"
                          }`}
                        >
                          <div
                            className={`mb-4 flex h-11 w-11 items-center justify-center rounded-xl ${
                              settings.theme === "system"
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
                            Follow your device settings.
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
      </div>
    </div>
  );
};

export default Settings;