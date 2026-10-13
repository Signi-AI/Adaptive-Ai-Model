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
import logo from "../../assets/logo.jpeg";
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
            </div>

            <button
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
                    </div>
                  </div>
                )}

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
    </div>
  );
};

export default Settings;