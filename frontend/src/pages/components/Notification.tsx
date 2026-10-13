import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  Bell,
  CheckCheck,
  Trash2,
  BookOpen,
  Award,
  Clock,
  ArrowLeft,
  Info,
  ChevronRight,
  Filter,
} from "lucide-react";
import logo from "../../assets/logo.jpeg";
import StudentSidebar from "../main/StudentSidebar";

interface NotificationItem {
  id: string;
  title: string;
  message: string;
  timestamp: string;
  type: "assignment" | "grade" | "reminder" | "system";
  read: boolean;
  link?: string;
}

const INITIAL_NOTIFICATIONS: NotificationItem[] = [
  {
    id: "notif-1",
    title: "Assignment Graded",
    message: "Your 'Quadratic Equations & Polynomial Graphs' assignment has been graded. Score: 92/100.",
    timestamp: "10 minutes ago",
    type: "grade",
    read: false,
    link: "/assignments",
  },
  {
    id: "notif-2",
    title: "New Assignment Posted",
    message: "Physics Teacher posted: 'Kinematics & Newton's Laws Problem Set'. Due in 5 days.",
    timestamp: "1 hour ago",
    type: "assignment",
    read: false,
    link: "/assignments",
  },
  {
    id: "notif-3",
    title: "AI Study Recommendation",
    message: "Your Physics score is currently at 52%. Consider starting a focused review session.",
    timestamp: "3 hours ago",
    type: "reminder",
    read: true,
    link: "/subjects/physics",
  },
  {
    id: "notif-4",
    title: "Platform System Update",
    message: "LearnAI Studio Portal v2.4 successfully updated with new interactive subject tracking.",
    timestamp: "1 day ago",
    type: "system",
    read: true,
  },
];

const Notifications: React.FC = () => {
  const navigate = useNavigate();

  // LocalStorage Persistence
  const [notifications, setNotifications] = useState<NotificationItem[]>(() => {
    const saved = localStorage.getItem("student_notifications_data");
    return saved ? JSON.parse(saved) : INITIAL_NOTIFICATIONS;
  });

  useEffect(() => {
    localStorage.setItem("student_notifications_data", JSON.stringify(notifications));
  }, [notifications]);

  // Filter state
  const [filter, setFilter] = useState<"all" | "unread" | "assignment" | "system">("all");

  // Calculations
  const unreadCount = notifications.filter((n) => !n.read).length;

  // Actions
  const markAsRead = (id: string) => {
    setNotifications((prev) =>
      prev.map((n) => (n.id === id ? { ...n, read: true } : n))
    );
  };

  const markAllAsRead = () => {
    setNotifications((prev) => prev.map((n) => ({ ...n, read: true })));
  };

  const deleteNotification = (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setNotifications((prev) => prev.filter((n) => n.id !== id));
  };

  const clearAllNotifications = () => {
    setNotifications([]);
  };

  const handleNotificationClick = (notif: NotificationItem) => {
    markAsRead(notif.id);
    if (notif.link) {
      navigate(notif.link);
    }
  };

  // Filter logic
  const filteredNotifications = notifications.filter((n) => {
    if (filter === "unread") return !n.read;
    if (filter === "assignment") return n.type === "assignment" || n.type === "grade";
    if (filter === "system") return n.type === "system" || n.type === "reminder";
    return true;
  });

  // Icon Helper
  const getNotificationIcon = (type: NotificationItem["type"]) => {
    switch (type) {
      case "grade":
        return (
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            <Award size={18} />
          </div>
        );
      case "assignment":
        return (
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-purple-500/10 text-purple-400 border border-purple-500/20">
            <BookOpen size={18} />
          </div>
        );
      case "reminder":
        return (
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-amber-500/10 text-amber-400 border border-amber-500/20">
            <Clock size={18} />
          </div>
        );
      case "system":
      default:
        return (
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-blue-500/10 text-blue-400 border border-blue-500/20">
            <Info size={18} />
          </div>
        );
    }
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
                  Student Activity & Alerts
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
              <div className="flex items-center gap-4">
                <div className="relative flex h-12 w-12 items-center justify-center rounded-2xl bg-purple-600/20 text-purple-400 border border-purple-500/30">
                  <Bell size={22} />
                  {unreadCount > 0 && (
                    <span className="absolute -top-1 -right-1 flex h-5 w-5 items-center justify-center rounded-full bg-purple-500 text-[10px] font-extrabold text-white ring-2 ring-slate-900">
                      {unreadCount}
                    </span>
                  )}
                </div>
                <div>
                  <h2 className="text-2xl font-extrabold text-white">Notifications</h2>
                  <p className="text-xs text-slate-400 mt-0.5">
                    Stay updated with assignment alerts, grades, and AI insights.
                  </p>
                </div>
              </div>

              {/* ACTION BUTTONS */}
              <div className="flex items-center gap-2">
                {unreadCount > 0 && (
                  <button
                    onClick={markAllAsRead}
                    className="inline-flex items-center gap-1.5 rounded-xl border border-purple-500/30 bg-purple-500/10 px-3.5 py-2 text-xs font-semibold text-purple-300 hover:bg-purple-500/20 transition-all"
                  >
                    <CheckCheck size={14} /> Mark all read
                  </button>
                )}
                {notifications.length > 0 && (
                  <button
                    onClick={clearAllNotifications}
                    className="inline-flex items-center gap-1.5 rounded-xl border border-slate-800 bg-slate-800/60 px-3.5 py-2 text-xs font-semibold text-slate-400 hover:text-rose-400 hover:border-rose-500/30 transition-all"
                  >
                    <Trash2 size={14} /> Clear all
                  </button>
                )}
              </div>
            </div>
          </div>

          {/* FILTER TABS */}
          <div className="mb-6 flex items-center justify-between">
            <div className="flex items-center gap-1 rounded-2xl border border-slate-800 bg-slate-900/80 p-1.5">
              {(["all", "unread", "assignment", "system"] as const).map((tab) => (
                <button
                  key={tab}
                  onClick={() => setFilter(tab)}
                  className={`rounded-xl px-4 py-2 text-xs font-semibold capitalize transition-all ${
                    filter === tab
                      ? "bg-purple-600 text-white shadow-md shadow-purple-600/20"
                      : "text-slate-400 hover:text-white"
                  }`}
                >
                  {tab}
                </button>
              ))}
            </div>

            <span className="text-xs text-slate-400 flex items-center gap-1">
              <Filter size={13} /> {filteredNotifications.length} Alert(s)
            </span>
          </div>

          {/* NOTIFICATION LIST */}
          <div className="space-y-3">
            {filteredNotifications.length === 0 ? (
              <div className="rounded-3xl border border-slate-800 bg-slate-800/40 p-12 text-center">
                <Bell className="mx-auto text-slate-600 mb-3" size={32} />
                <p className="text-sm font-semibold text-slate-300">All caught up!</p>
                <p className="text-xs text-slate-500 mt-1">
                  You have no notifications matching this filter.
                </p>
              </div>
            ) : (
              filteredNotifications.map((notif) => (
                <div
                  key={notif.id}
                  onClick={() => handleNotificationClick(notif)}
                  className={`group relative cursor-pointer rounded-2xl border p-4 transition-all ${
                    !notif.read
                      ? "border-purple-500/40 bg-purple-950/20 hover:bg-purple-950/30"
                      : "border-slate-800 bg-slate-800/40 hover:bg-slate-800/70"
                  }`}
                >
                  <div className="flex items-start gap-4">
                    {getNotificationIcon(notif.type)}

                    <div className="flex-1">
                      <div className="flex items-center justify-between gap-2">
                        <div className="flex items-center gap-2">
                          <h4 className="text-sm font-bold text-white">{notif.title}</h4>
                          {!notif.read && (
                            <span className="h-2 w-2 rounded-full bg-purple-500 shadow-sm shadow-purple-500" />
                          )}
                        </div>
                        <span className="text-[11px] text-slate-500">{notif.timestamp}</span>
                      </div>

                      <p className="mt-1 text-xs text-slate-300 leading-relaxed">
                        {notif.message}
                      </p>
                    </div>

                    <div className="flex items-center gap-2 shrink-0">
                      <button
                        onClick={(e) => deleteNotification(notif.id, e)}
                        className="opacity-0 group-hover:opacity-100 p-1.5 text-slate-500 hover:text-rose-400 rounded-lg hover:bg-slate-800 transition-all"
                        title="Delete notification"
                      >
                        <Trash2 size={14} />
                      </button>

                      {notif.link && (
                        <ChevronRight size={16} className="text-slate-500 group-hover:text-purple-400 transition-all" />
                      )}
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Notifications;