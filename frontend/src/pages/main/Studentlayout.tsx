import React, {
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";
import { Outlet, useLocation, useNavigate } from "react-router-dom";

import LearnSidebar from "../learn/LearnSidebar";
import type { RecentLesson } from "../learn/LearnSidebar";

interface StudentLayoutContextType {
  openMenu: () => void;
  closeMenu: () => void;
}

const StudentLayoutContext =
  createContext<StudentLayoutContextType | null>(null);

export const useStudentLayout = () => {
  const context = useContext(StudentLayoutContext);

  if (!context) {
    throw new Error(
      "useStudentLayout must be used inside StudentLayout"
    );
  }

  return context;
};

const RECENT_KEY = "learn_recent";
const LEVEL_KEY = "studentLevel";

const loadRecents = (): RecentLesson[] => {
  try {
    const saved = localStorage.getItem(RECENT_KEY);

    if (!saved) {
      return [];
    }

    return JSON.parse(saved) as RecentLesson[];
  } catch {
    return [];
  }
};

const StudentLayout: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const [menu, setMenu] = useState(false);

  const [recents, setRecents] =
    useState<RecentLesson[]>(loadRecents);

  const [level, setLevel] = useState(
    () => localStorage.getItem(LEVEL_KEY) || ""
  );

  const openMenu = () => {
    setMenu(true);
  };

  const closeMenu = () => {
    setMenu(false);
  };

  /*
   * Close mobile sidebar whenever the page changes
   */
  useEffect(() => {
    setMenu(false);
  }, [location.pathname]);

  /*
   * Keep sidebar data updated
   */
  useEffect(() => {
    const updateRecents = () => {
      setRecents(loadRecents());
    };

    const updateLevel = () => {
      setLevel(localStorage.getItem(LEVEL_KEY) || "");
    };

    window.addEventListener(
      "learn-recents-updated",
      updateRecents
    );

    window.addEventListener(
      "student-level-updated",
      updateLevel
    );

    window.addEventListener("storage", updateRecents);
    window.addEventListener("storage", updateLevel);

    return () => {
      window.removeEventListener(
        "learn-recents-updated",
        updateRecents
      );

      window.removeEventListener(
        "student-level-updated",
        updateLevel
      );

      window.removeEventListener("storage", updateRecents);
      window.removeEventListener("storage", updateLevel);
    };
  }, []);

  const handleNewLesson = () => {
    setMenu(false);
    navigate("/tutorhome");
  };

  const handleRecentLesson = (recent: RecentLesson) => {
    setMenu(false);

    localStorage.setItem(
      "selectedRecentLesson",
      JSON.stringify(recent)
    );

    navigate("/tutorhome");
  };

  return (
    <StudentLayoutContext.Provider
      value={{
        openMenu,
        closeMenu,
      }}
    >
      <div className="flex h-screen w-full overflow-hidden bg-slate-50">
        {/* ONE STUDENT SIDEBAR */}
        <LearnSidebar
          open={menu}
          onClose={closeMenu}
          onNew={handleNewLesson}
          recents={recents}
          onRecent={handleRecentLesson}
          level={level}
        />

        {/* PAGE CONTENT */}
        <main className="min-w-0 flex-1 overflow-y-auto">
          <Outlet />
        </main>
      </div>
    </StudentLayoutContext.Provider>
  );
};

export default StudentLayout;