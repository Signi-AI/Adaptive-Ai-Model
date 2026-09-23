import React, { useState } from "react";
import { Link } from "react-router-dom";

type Notification = {
  id: number;
  title: string;
  message: string;
  time: string;
  type: "Assignment" | "Learning" | "System";
  read: boolean;
};

const Notifications: React.FC = () => {
  const [notifications, setNotifications] = useState<Notification[]>([
    {
      id: 1,
      title: "New Assignment",
      message:
        "Your Mathematics assignment on Algebra is now available.",
      time: "10 minutes ago",
      type: "Assignment",
      read: false,
    },
    {
      id: 2,
      title: "Assignment Reminder",
      message:
        "Your Biology assignment is due soon. Make sure you complete it on time.",
      time: "1 hour ago",
      type: "Assignment",
      read: false,
    },
    {
      id: 3,
      title: "Learning Progress",
      message:
        "You have completed 68% of your learning goals. Keep going!",
      time: "Yesterday",
      type: "Learning",
      read: true,
    },
    {
      id: 4,
      title: "AI Tutor Available",
      message:
        "You can now continue your personalized learning session with the AI Tutor.",
      time: "Yesterday",
      type: "Learning",
      read: true,
    },
    {
      id: 5,
      title: "System Update",
      message:
        "Your student learning dashboard has been updated successfully.",
      time: "2 days ago",
      type: "System",
      read: true,
    },
  ]);

  const unreadCount = notifications.filter(
    (notification) => !notification.read
  ).length;

  const markAsRead = (id: number) => {
    setNotifications((current) =>
      current.map((notification) =>
        notification.id === id
          ? { ...notification, read: true }
          : notification
      )
    );
  };

  const markAllAsRead = () => {
    setNotifications((current) =>
      current.map((notification) => ({
        ...notification,
        read: true,
      }))
    );
  };

  const deleteNotification = (id: number) => {
    setNotifications((current) =>
      current.filter((notification) => notification.id !== id)
    );
  };

  return (
    <div className="min-h-screen bg-gray-50">

      {/* Header */}
      <header className="sticky top-0 z-30 border-b border-gray-200 bg-white px-8 py-6">
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">

          <div>
            <h1 className="text-2xl font-bold text-black">
              Notifications
            </h1>

            <p className="mt-1 text-sm text-gray-500">
              Stay updated with your learning activities
            </p>
          </div>

          {unreadCount > 0 && (
            <button
              type="button"
              onClick={markAllAsRead}
              className="w-fit rounded-lg bg-black px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-gray-800"
            >
              Mark All as Read
            </button>
          )}

        </div>
      </header>

      {/* Main Content */}
      <main className="space-y-8 p-8">

        {/* Notification Summary */}
        <section className="rounded-2xl bg-black p-8 text-white">

          <h2 className="text-2xl font-bold">
            Your Notifications
          </h2>

          <p className="mt-3 max-w-2xl text-sm leading-6 text-gray-300">
            Important updates about assignments, learning progress,
            and your student account will appear here.
          </p>

          <div className="mt-7 grid grid-cols-1 gap-4 sm:grid-cols-3">

            <div className="rounded-xl bg-gray-900 p-5">
              <p className="text-sm text-gray-400">
                Total Notifications
              </p>

              <p className="mt-2 text-3xl font-bold">
                {notifications.length}
              </p>
            </div>

            <div className="rounded-xl bg-gray-900 p-5">
              <p className="text-sm text-gray-400">
                Unread
              </p>

              <p className="mt-2 text-3xl font-bold">
                {unreadCount}
              </p>
            </div>

            <div className="rounded-xl bg-gray-900 p-5">
              <p className="text-sm text-gray-400">
                Read
              </p>

              <p className="mt-2 text-3xl font-bold">
                {notifications.length - unreadCount}
              </p>
            </div>

          </div>

        </section>

        {/* Notifications List */}
        <section className="rounded-2xl border border-gray-200 bg-white p-7">

          <div>
            <h2 className="text-xl font-bold text-black">
              Recent Notifications
            </h2>

            <p className="mt-1 text-sm text-gray-500">
              Your latest learning and account updates.
            </p>
          </div>

          <div className="mt-6 space-y-4">

            {notifications.length === 0 ? (
              <div className="rounded-xl border border-gray-200 bg-gray-50 p-10 text-center">
                <h3 className="text-lg font-semibold text-black">
                  No Notifications
                </h3>

                <p className="mt-2 text-sm text-gray-500">
                  You don't have any notifications at the moment.
                </p>
              </div>
            ) : (
              notifications.map((notification) => (
                <div
                  key={notification.id}
                  className={`rounded-xl border p-6 transition ${
                    notification.read
                      ? "border-gray-200 bg-white"
                      : "border-slate-300 bg-slate-300/30"
                  }`}
                >

                  <div className="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between">

                    {/* Notification Content */}
                    <div className="flex-1">

                      <div className="flex flex-wrap items-center gap-3">

                        <h3 className="text-lg font-bold text-black">
                          {notification.title}
                        </h3>

                        {!notification.read && (
                          <span className="rounded-full bg-black px-3 py-1 text-xs font-semibold text-white">
                            New
                          </span>
                        )}

                      </div>

                      <p className="mt-2 text-sm leading-6 text-gray-600">
                        {notification.message}
                      </p>

                      <div className="mt-4 flex flex-wrap items-center gap-3">

                        <span className="rounded-full bg-slate-300 px-3 py-1 text-xs font-semibold text-black">
                          {notification.type}
                        </span>

                        <span className="text-xs text-gray-400">
                          {notification.time}
                        </span>

                      </div>

                    </div>

                    {/* Actions */}
                    <div className="flex flex-wrap gap-2">

                      {!notification.read && (
                        <button
                          type="button"
                          onClick={() =>
                            markAsRead(notification.id)
                          }
                          className="rounded-lg bg-black px-4 py-2 text-xs font-semibold text-white transition hover:bg-gray-800"
                        >
                          Mark as Read
                        </button>
                      )}

                      <button
                        type="button"
                        onClick={() =>
                          deleteNotification(notification.id)
                        }
                        className="rounded-lg border border-gray-300 px-4 py-2 text-xs font-semibold text-black transition hover:bg-gray-100"
                      >
                        Delete
                      </button>

                    </div>

                  </div>

                </div>
              ))
            )}

          </div>

        </section>

        {/* Learning Section */}
        <section className="rounded-2xl border border-slate-300 bg-slate-300 p-7">

          <h2 className="text-xl font-bold text-black">
            Continue Learning
          </h2>

          <p className="mt-2 max-w-2xl text-sm leading-6 text-black">
            Check your assignments and continue learning with your
            personalized AI Tutor.
          </p>

          <div className="mt-5 flex flex-wrap gap-3">

            <Link
              to="/student/assignments"
              className="rounded-xl bg-black px-6 py-3 text-sm font-semibold text-white transition hover:bg-gray-800"
            >
              View Assignments
            </Link>

            <Link
              to="/student/ai-tutor"
              className="rounded-xl border border-black px-6 py-3 text-sm font-semibold text-black transition hover:bg-gray-200"
            >
              Ask AI Tutor
            </Link>

          </div>

        </section>

      </main>
    </div>
  );
};

export default Notifications;