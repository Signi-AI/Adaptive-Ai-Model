import React from "react";
import { NavLink } from "react-router-dom";

const AppSidebar: React.FC = () => {
  const navItems = [
    {
      name: "Home",
      path: "/learning",
      icon: "⌂",
    },
    {
      name: "Learn",
      path: "/subjects",
      icon: "📚",
    },
    {
      name: "Assignments",
      path: "/assignments",
      icon: "📝",
    },
    {
      name: "AI Tutor",
      path: "/ai-tutor",
      icon: "🤖",
    },
    {
      name: "Profile",
      path: "/profile",
      icon: "👤",
    },
  ];

  return (
    <aside className="hidden h-screen w-64 shrink-0 border-r border-gray-200 bg-white lg:flex lg:flex-col">

      {/* Logo */}
      <div className="flex h-20 items-center border-b border-gray-100 px-6">
        <NavLink to="/learning" className="flex items-center gap-3">

          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-black text-lg font-bold text-white">
            A
          </div>

          <div>
            <p className="text-base font-bold text-black">
              AdaptiveLearn
            </p>

            <p className="text-[9px] font-medium uppercase tracking-widest text-gray-400">
              Learn Smarter
            </p>
          </div>

        </NavLink>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-6">

        <p className="mb-3 px-3 text-[10px] font-semibold uppercase tracking-widest text-gray-400">
          Menu
        </p>

        <div className="space-y-1">

          {navItems.map((item) => (
            <NavLink
              key={item.name}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-xl px-3 py-3 text-sm font-medium transition ${
                  isActive
                    ? "bg-black text-white"
                    : "text-gray-600 hover:bg-gray-100 hover:text-black"
                }`
              }
            >
              <span className="flex h-8 w-8 items-center justify-center rounded-lg text-base">
                {item.icon}
              </span>

              <span>{item.name}</span>
            </NavLink>
          ))}

        </div>
      </nav>

      {/* Offline Status */}
      <div className="border-t border-gray-100 p-4">

        <div className="rounded-2xl bg-gray-50 p-4">

          <div className="flex items-center gap-2">

            <span className="h-2.5 w-2.5 rounded-full bg-green-500" />

            <span className="text-xs font-semibold text-gray-700">
              Offline Ready
            </span>

          </div>

          <p className="mt-2 text-xs leading-5 text-gray-400">
            Your lessons and progress are available offline.
          </p>

        </div>

      </div>
    </aside>
  );
};

export default AppSidebar;