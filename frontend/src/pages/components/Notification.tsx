import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Bell,
  CheckCheck,
  Trash2,
  BookOpen,
  Award,
  Clock,
  ArrowLeft,
  ChevronRight,
  Filter,
  Sparkles,
  Target,
  GraduationCap,
} from "lucide-react";
import StudentSidebar from "../main/StudentSidebar";

interface NotificationItem {
  id: string;
  title: string;
  message: string;
  timestamp: string;
  type: "assignment" | "grade" | "reminder" | "system" | "achievement";
  read: boolean;
  link?: string;
}

const INITIAL_NOTIFICATIONS: NotificationItem[] = [
  {
    id: "notif-1",
    title: "Assignment Graded",
    message:
      "Your Mathematics assignment, Quadratic Equations & Polynomial Graphs, has been graded. You scored 92/100.",
    timestamp: "10 minutes ago",
    type: "grade",
    read: false,
    link: "/assignments",
  },
  {
    id: "notif-2",
    title: "New Assignment",
    message:
      "A new Physics assignment has been posted: Kinematics & Newton's Laws Problem Set. Due on October 5, 2026.",
    timestamp: "1 hour ago",
    type: "assignment",
    read: false,
    link: "/assignments",
  },
  {
    id: "notif-3",
    title: "Assignment Due Soon",
    message:
      "Your Chemistry assignment, Stoichiometry & Chemical Equations, is due on October 8, 2026.",
    timestamp: "2 hours ago",
    type: "reminder",
    read: false,
    link: "/assignments",
  },
  {
    id: "notif-4",
    title: "Keep Learning",
    message:
      "You are making good progress in Mathematics. Continue your current lesson to maintain your learning streak.",
    timestamp: "3 hours ago",
    type: "reminder",
    read: true,
    link: "/learn",
  },
  {
    id: "notif-5",
    title: "AI Tutor Recommendation",
    message:
      "Your recent Physics progress shows that you may benefit from reviewing Force and Motion.",
    timestamp: "5 hours ago",
    type: "system",
    read: true,
    link: "/learn",
  },
  {
    id: "notif-6",
    title: "Learning Achievement",
    message:
      "Great job! You have completed 75% of your Mathematics learning progress.",
    timestamp: "Yesterday",
    type: "achievement",
    read: true,
    link: "/subjects",
  },
  {
    id: "notif-7",
    title: "Assignment Submitted",
    message:
      "Your Biology Cellular Respiration Synthesis Essay was successfully submitted.",
    timestamp: "Yesterday",
    type: "assignment",
    read: true,
    link: "/assignments",
  },
  {
    id: "notif-8",
    title: "Learning Reminder",
    message:
      "You have not completed a learning session today. Spend a few minutes reviewing your subjects.",
    timestamp: "Yesterday",
    type: "reminder",
    read: true,
    link: "/learn",
  },
];

const Notifications: React.FC = () => {
  const navigate = useNavigate();

  const [notifications, setNotifications] = useState<NotificationItem[]>(() => {
    try {
      const saved = localStorage.getItem("student_notifications_data");

      if (saved) {
        return JSON.parse(saved);
      }

      return INITIAL_NOTIFICATIONS;
    } catch {
      return INITIAL_NOTIFICATIONS;
    }
  });

  useEffect(() => {
    localStorage.setItem(
      "student_notifications_data",
      JSON.stringify(notifications)
    );
  }, [notifications]);

  const [filter, setFilter] = useState<
    "all" | "unread" | "assignment" | "learning"
  >("all");

  const unreadCount = notifications.filter(
    (notification) => !notification.read
  ).length;

  const markAsRead = (id: string) => {
    setNotifications((previous) =>
      previous.map((notification) =>
        notification.id === id
          ? { ...notification, read: true }
          : notification
      )
    );
  };

  const markAllAsRead = () => {
    setNotifications((previous) =>
      previous.map((notification) => ({
        ...notification,
        read: true,
      }))
    );
  };

  const deleteNotification = (
    id: string,
    event: React.MouseEvent<HTMLButtonElement>
  ) => {
    event.stopPropagation();

    setNotifications((previous) =>
      previous.filter((notification) => notification.id !== id)
    );
  };

  const clearAllNotifications = () => {
    setNotifications([]);
  };

  const handleNotificationClick = (notification: NotificationItem) => {
    markAsRead(notification.id);

    if (notification.link) {
      navigate(notification.link);
    }
  };

  const filteredNotifications = notifications.filter((notification) => {
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
  });

  const getNotificationIcon = (
    type: NotificationItem["type"]
  ) => {
    switch (type) {
      case "grade":
        return (
          <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-green-50 text-green-600">
            <Award size={20} />
          </div>
        );

      case "assignment":
        return (
          <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-blue-50 text-blue-600">
            <BookOpen size={20} />
          </div>
        );

      case "reminder":
        return (
          <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-amber-50 text-amber-600">
            <Clock size={20} />
          </div>
        );

      case "achievement":
        return (
          <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-blue-50 text-blue-600">
            <Target size={20} />
          </div>
        );

      case "system":
      default:
        return (
          <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-slate-100 text-slate-600">
            <Sparkles size={20} />
          </div>
        );
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-800">
      <StudentSidebar />

      <div className="ml-60">
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

        <main className="mx-auto max-w-5xl space-y-7 p-8">
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
                    Important updates about assignments, grades, progress,
                    and your learning activities.
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

          <section className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
            <div className="flex w-fit flex-wrap items-center gap-1 rounded-xl border border-slate-200 bg-white p-1.5 shadow-sm">
              {(
                ["all", "unread", "assignment", "learning"] as const
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
              {filteredNotifications.length !== 1 ? "s" : ""}
            </div>
          </section>

          <section className="space-y-3">
            {filteredNotifications.length === 0 ? (
              <div className="rounded-2xl border border-slate-200 bg-white p-14 text-center shadow-sm">
                <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-slate-100">
                  <Bell size={25} className="text-slate-400" />
                </div>

                <h3 className="mt-4 text-base font-bold text-slate-700">
                  All caught up!
                </h3>

                <p className="mx-auto mt-1 max-w-sm text-sm text-slate-500">
                  You don't have any notifications matching the selected
                  filter.
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
                    {getNotificationIcon(notification.type)}

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
                        {notification.type === "assignment" && (
                          <span className="rounded-full bg-blue-50 px-2.5 py-1 text-[10px] font-semibold text-blue-700">
                            Assignment
                          </span>
                        )}

                        {notification.type === "grade" && (
                          <span className="rounded-full bg-green-50 px-2.5 py-1 text-[10px] font-semibold text-green-700">
                            Grade
                          </span>
                        )}

                        {notification.type === "reminder" && (
                          <span className="rounded-full bg-amber-50 px-2.5 py-1 text-[10px] font-semibold text-amber-700">
                            Reminder
                          </span>
                        )}

                        {notification.type === "achievement" && (
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
                        deleteNotification(notification.id, event)
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
                  Check your notifications regularly so you don't miss new
                  assignments, grades, deadlines, or learning recommendations.
                </p>

                <button
                  onClick={() => navigate("/learn")}
                  className="mt-3 inline-flex items-center gap-1 text-sm font-semibold text-blue-600 transition hover:text-blue-700"
                >
                  Continue Learning
                  <ChevronRight size={15} />
                </button>
              </div>
            </div>
          </section>
        </main>
      </div>
    </div>
  );
};

export default Notifications;