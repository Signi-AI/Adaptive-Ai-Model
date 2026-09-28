import React from "react";
import { NavLink } from "react-router-dom";

const MobileNavigation: React.FC = () => {
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
      name: "Tasks",
      path: "/assignments",
      icon: "📝",
    },
    {
      name: "AI",
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
    <nav className="fixed bottom-0 left-0 right-0 z-50 border-t border-gray-200 bg-white px-2 pb-safe lg:hidden">

      <div className="mx-auto flex max-w-lg items-center justify-around">

        {navItems.map((item) => (
          <NavLink
            key={item.name}
            to={item.path}
            className={({ isActive }) =>
              `flex min-w-[60px] flex-col items-center gap-1 px-2 py-3 text-[10px] font-medium transition ${
                isActive
                  ? "text-black"
                  : "text-gray-400"
              }`
            }
          >
            {({ isActive }) => (
              <>
                <span
                  className={`flex h-8 w-8 items-center justify-center rounded-xl text-base ${
                    isActive ? "bg-gray-100" : ""
                  }`}
                >
                  {item.icon}
                </span>

                <span>{item.name}</span>
              </>
            )}
          </NavLink>
        ))}

      </div>
    </nav>
  );
};

export default MobileNavigation;