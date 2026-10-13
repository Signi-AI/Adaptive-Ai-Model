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
<<<<<<< HEAD
import logo from "../../assets/logo.jpeg";
import StudentSidebar from "../main/StudentSidebar";
=======
>>>>>>> 6d22643 (student frontend development)

interface NotificationItem {
  id: string;
  title: string;
  message: string;
  timestamp: string;
<<<<<<< HEAD
  type: "assignment" | "grade" | "reminder" | "system";
=======
  type:
    | "assignment"
    | "grade"
    | "reminder"
    | "system"
    | "achievement";
>>>>>>> 6d22643 (student frontend development)
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

<<<<<<< HEAD
  // LocalStorage Persistence
  const [notifications, setNotifications] = useState<NotificationItem[]>(() => {
    const saved = localStorage.getItem("student_notifications_data");
    return saved ? JSON.parse(saved) : INITIAL_NOTIFICATIONS;
=======
  const [notifications, setNotifications] = useState<
    NotificationItem[]
  >(() => {
    try {
      const saved = localStorage.getItem(
        "student_notifications_data"
      );

      if (saved) {
        return JSON.parse(saved);
      }

      return INITIAL_NOTIFICATIONS;
    } catch {
      return INITIAL_NOTIFICATIONS;
    }
>>>>>>> 6d22643 (student frontend development)
  });

  const [filter, setFilter] = useState<
    "all" | "unread" | "assignment" | "learning"
  >("all");

  useEffect(() => {
    localStorage.setItem("student_notifications_data", JSON.stringify(notifications));
  }, [notifications]);

<<<<<<< HEAD
  // Filter state
  const [filter, setFilter] = useState<"all" | "unread" | "assignment" | "system">("all");

  // Calculations
  const unreadCount = notifications.filter((n) => !n.read).length;
=======
  const unreadCount = notifications.filter(
    (notification) => !notification.read
  ).length;
>>>>>>> 6d22643 (student frontend development)

  // Actions
  const markAsRead = (id: string) => {
<<<<<<< HEAD
    setNotifications((prev) =>
      prev.map((n) => (n.id === id ? { ...n, read: true } : n))
=======
    setNotifications((previous) =>
      previous.map((notification) =>
        notification.id === id
          ? {
              ...notification,
              read: true,
            }
          : notification
      )
>>>>>>> 6d22643 (student frontend development)
    );
  };

  const markAllAsRead = () => {
    setNotifications((prev) => prev.map((n) => ({ ...n, read: true })));
  };

<<<<<<< HEAD
  const deleteNotification = (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setNotifications((prev) => prev.filter((n) => n.id !== id));
=======
  const deleteNotification = (
    id: string,
    event: React.MouseEvent<HTMLButtonElement>
  ) => {
    event.stopPropagation();

    setNotifications((previous) =>
      previous.filter(
        (notification) => notification.id !== id
      )
    );
>>>>>>> 6d22643 (student frontend development)
  };

  const clearAllNotifications = () => {
    setNotifications([]);
  };

<<<<<<< HEAD
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
=======
  const handleNotificationClick = (
    notification: NotificationItem
  ) => {
    markAsRead(notification.id);

    if (notification.link) {
      navigate(notification.link);
    }
  };

  const filteredNotifications = notifications.filter(
    (notification) => {
      if (filter === "unread") {
        return !notification.read;
      }

      if (filter === "assignment") {
        return (
          notification.type === "assignment" ||
          notification.type === "grade"
        );
      }

      if (filter === "learning") {
        return (
          notification.type === "reminder" ||
          notification.type === "system" ||
          notification.type === "achievement"
        );
      }

      return true;
    }
  );
>>>>>>> 6d22643 (student frontend development)

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
<<<<<<< HEAD
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
=======
    <div className="min-h-screen bg-slate-50 font-sans text-slate-800">
      {/* =========================
          HEADER
      ========================== */}
      <header className="sticky top-0 z-30 border-b border-slate-200 bg-white/95 px-8 py-5 backdrop-blur-xl">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-slate-800">
              Notifications
            </h1>

            <p className="mt-1 text-sm text-slate-500">
              Stay updated with your learning activities.
            </p>
          </div>

          <button
            onClick={() => navigate("/profile")}
            className="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-slate-600 transition hover:bg-slate-50 hover:text-slate-800"
          >
            <ArrowLeft size={16} />
            Back to Profile
          </button>
        </div>
      </header>

      {/* =========================
          MAIN CONTENT
      ========================== */}
      <main className="mx-auto max-w-5xl space-y-7 p-8">
        {/* =========================
            NOTIFICATION SUMMARY
        ========================== */}
        <section className="rounded-2xl bg-slate-300 p-7 shadow-sm">
          <div className="flex flex-col justify-between gap-6 md:flex-row md:items-center">
            <div className="flex items-center gap-4">
              <div className="relative flex h-14 w-14 items-center justify-center rounded-2xl bg-white/60 text-slate-800">
                <Bell size={25} />

                {unreadCount > 0 && (
                  <span className="absolute -right-1 -top-1 flex h-6 min-w-6 items-center justify-center rounded-full bg-blue-600 px-1.5 text-[10px] font-bold text-white ring-2 ring-slate-300">
                    {unreadCount}
                  </span>
                )}
              </div>

              <div>
                <h2 className="text-2xl font-bold text-slate-900">
                  Your Notifications
                </h2>

                <p className="mt-1 max-w-xl text-sm text-slate-600">
                  Important updates about assignments, grades,
                  progress, and your learning activities.
                </p>
              </div>
            </div>

            <div className="flex flex-wrap gap-2">
              {unreadCount > 0 && (
                <button
                  onClick={markAllAsRead}
                  className="inline-flex items-center gap-2 rounded-xl bg-white/70 px-4 py-2.5 text-xs font-semibold text-slate-700 transition hover:bg-white"
                >
                  <CheckCheck size={15} />
                  Mark all as read
                </button>
              )}

              {notifications.length > 0 && (
                <button
                  onClick={clearAllNotifications}
                  className="inline-flex items-center gap-2 rounded-xl bg-white/50 px-4 py-2.5 text-xs font-semibold text-slate-600 transition hover:bg-white hover:text-red-600"
                >
                  <Trash2 size={15} />
                  Clear all
                </button>
              )}
            </div>
          </div>

          {/* =========================
              STATISTICS
          ========================== */}
          <div className="mt-7 grid grid-cols-1 gap-3 sm:grid-cols-3">
            <div className="rounded-xl bg-white/50 p-4">
              <p className="text-xs font-medium text-slate-500">
                Total Notifications
              </p>

              <p className="mt-1 text-2xl font-bold text-slate-900">
                {notifications.length}
              </p>
            </div>

            <div className="rounded-xl bg-white/50 p-4">
              <p className="text-xs font-medium text-slate-500">
                Unread
              </p>

              <p className="mt-1 text-2xl font-bold text-blue-700">
                {unreadCount}
              </p>
            </div>

            <div className="rounded-xl bg-white/50 p-4">
              <p className="text-xs font-medium text-slate-500">
                Assignment Updates
              </p>

              <p className="mt-1 text-2xl font-bold text-slate-900">
                {
                  notifications.filter(
                    (notification) =>
                      notification.type === "assignment" ||
                      notification.type === "grade"
                  ).length
                }
              </p>
            </div>
          </div>
        </section>

        {/* =========================
            FILTERS
        ========================== */}
        <section className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
          <div className="flex w-fit flex-wrap items-center gap-1 rounded-xl border border-slate-200 bg-white p-1.5 shadow-sm">
            {(
              [
                "all",
                "unread",
                "assignment",
                "learning",
              ] as const
            ).map((tab) => (
              <button
                key={tab}
                onClick={() => setFilter(tab)}
                className={`rounded-lg px-4 py-2 text-xs font-semibold capitalize transition ${
                  filter === tab
                    ? "bg-slate-800 text-white"
                    : "text-slate-500 hover:bg-slate-100 hover:text-slate-800"
                }`}
              >
                {tab === "assignment"
                  ? "Assignments"
                  : tab === "learning"
                  ? "Learning"
                  : tab}
              </button>
            ))}
          </div>

          <div className="flex items-center gap-2 text-xs text-slate-500">
            <Filter size={14} />
            Showing {filteredNotifications.length} notification
            {filteredNotifications.length !== 1
              ? "s"
              : ""}
          </div>
        </section>

        {/* =========================
            NOTIFICATION LIST
        ========================== */}
        <section className="space-y-3">
          {filteredNotifications.length === 0 ? (
            <div className="rounded-2xl border border-slate-200 bg-white p-14 text-center shadow-sm">
              <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-slate-100">
                <Bell
                  size={25}
                  className="text-slate-400"
                />
              </div>

              <h3 className="mt-4 text-base font-bold text-slate-700">
                All caught up!
              </h3>

              <p className="mx-auto mt-1 max-w-sm text-sm text-slate-500">
                You don't have any notifications matching
                the selected filter.
              </p>
            </div>
          ) : (
            filteredNotifications.map((notification) => (
              <article
                key={notification.id}
                onClick={() =>
                  handleNotificationClick(notification)
                }
                className={`group cursor-pointer rounded-2xl border bg-white p-5 shadow-sm transition hover:-translate-y-[1px] hover:shadow-md ${
                  !notification.read
                    ? "border-blue-200 bg-blue-50/30"
                    : "border-slate-200"
                }`}
              >
                <div className="flex items-start gap-4">
                  {getNotificationIcon(
                    notification.type
                  )}

                  <div className="min-w-0 flex-1">
                    <div className="flex flex-col gap-1 sm:flex-row sm:items-start sm:justify-between">
                      <div className="flex items-center gap-2">
                        <h3 className="text-sm font-bold text-slate-800">
                          {notification.title}
                        </h3>

                        {!notification.read && (
                          <span className="h-2 w-2 shrink-0 rounded-full bg-blue-600" />
                        )}
                      </div>

                      <span className="shrink-0 text-[11px] text-slate-400">
                        {notification.timestamp}
                      </span>
                    </div>

                    <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-500">
                      {notification.message}
                    </p>

                    <div className="mt-3 flex items-center gap-2">
                      {notification.type ===
                        "assignment" && (
                        <span className="rounded-full bg-blue-50 px-2.5 py-1 text-[10px] font-semibold text-blue-700">
                          Assignment
                        </span>
                      )}

                      {notification.type === "grade" && (
                        <span className="rounded-full bg-green-50 px-2.5 py-1 text-[10px] font-semibold text-green-700">
                          Grade
                        </span>
                      )}

                      {notification.type ===
                        "reminder" && (
                        <span className="rounded-full bg-amber-50 px-2.5 py-1 text-[10px] font-semibold text-amber-700">
                          Reminder
                        </span>
                      )}

                      {notification.type ===
                        "achievement" && (
                        <span className="rounded-full bg-blue-50 px-2.5 py-1 text-[10px] font-semibold text-blue-700">
                          Achievement
                        </span>
                      )}

                      {notification.type === "system" && (
                        <span className="rounded-full bg-slate-100 px-2.5 py-1 text-[10px] font-semibold text-slate-600">
                          AI Tutor
                        </span>
                      )}

                      {notification.link && (
                        <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-blue-600 opacity-0 transition group-hover:opacity-100">
                          View
                          <ChevronRight size={13} />
                        </span>
                      )}
                    </div>
                  </div>

                  <button
                    onClick={(event) =>
                      deleteNotification(
                        notification.id,
                        event
                      )
                    }
                    className="shrink-0 rounded-lg p-2 text-slate-300 opacity-0 transition hover:bg-red-50 hover:text-red-500 group-hover:opacity-100"
                    title="Delete notification"
                  >
                    <Trash2 size={15} />
                  </button>
                </div>
              </article>
            ))
          )}
        </section>

        {/* =========================
            LEARNING REMINDER
        ========================== */}
        <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex items-start gap-4">
            <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-blue-50 text-blue-600">
              <GraduationCap size={21} />
            </div>

            <div>
              <h3 className="text-sm font-bold text-slate-800">
                Stay consistent with your learning
              </h3>

              <p className="mt-1 text-sm leading-6 text-slate-500">
                Check your notifications regularly so you
                don't miss new assignments, grades, deadlines,
                or learning recommendations.
              </p>

              <button
                onClick={() => navigate("/tutorhome")}
                className="mt-3 inline-flex items-center gap-1 text-sm font-semibold text-blue-600 transition hover:text-blue-700"
              >
                Continue Learning
                <ChevronRight size={15} />
              </button>
            </div>
          </div>
        </section>
      </main>
>>>>>>> 6d22643 (student frontend development)
    </div>
  );
};

export default Notifications;