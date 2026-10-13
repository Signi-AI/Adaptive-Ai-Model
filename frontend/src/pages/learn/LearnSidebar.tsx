import {
  BarChart3,
  BookOpen,
  ClipboardList,
  LayoutDashboard,
  Plus,
  X,
  User,
  Settings,
  LogOut,
  Bell,
} from "lucide-react";

import {
  Link,
  useLocation,
  useNavigate,
} from "react-router-dom";

import logo from "../../assets/logo.jpeg";

export interface RecentLesson {
  subject: string;
  topic: string;
  lesson: string;
}

interface Props {
  open: boolean;
  onClose: () => void;
  onNew: () => void;
  recents: RecentLesson[];
  onRecent: (r: RecentLesson) => void;
  level: string;
}

const item =
  "flex w-full items-center gap-2.5 rounded-xl px-2.5 py-2 text-left text-[15px] font-medium text-learn-ink transition-colors hover:bg-learn-hover focus-visible:outline focus-visible:outline-2 focus-visible:outline-learn-accent";

const activeItem =
  "bg-learn-hover text-learn-accent";

export default function LearnSidebar({
  open,
  onClose,
  onNew,
  recents,
  onRecent,
  level,
}: Props) {
  const location = useLocation();
  const navigate = useNavigate();

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("accessToken");
    localStorage.removeItem("user");
    localStorage.removeItem("student");
    localStorage.removeItem("currentUser");

    onClose();

    navigate("/login");
  };

  return (
    <>
      {/* =========================
          MOBILE OVERLAY
      ========================== */}
      {open && (
        <div
          className="fixed inset-0 z-40 bg-black/40 backdrop-blur-[1px] md:hidden"
          onClick={onClose}
          aria-hidden="true"
        />
      )}

      {/* =========================
          SIDEBAR
      ========================== */}
      <aside
        className={`
          fixed inset-y-0 left-0 z-50
          flex w-64 flex-col
          border-r border-learn-line
          bg-learn-side
          px-2.5 pt-3.5
          shadow-xl
          transition-transform duration-300 ease-in-out

          ${
            open
              ? "translate-x-0"
              : "-translate-x-full"
          }

          md:static
          md:z-auto
          md:translate-x-0
          md:shadow-none
        `}
      >
        {/* =========================
            LOGO
        ========================== */}
        <div className="flex items-center justify-between px-2.5 pb-4 pt-1.5">
          <div className="flex items-center gap-2.5">
            <img
              src={logo}
              alt="LearnAI Logo"
              className="h-7 w-7 rounded-lg object-cover"
            />

            <span className="font-display text-2xl font-medium text-learn-ink">
              LearnAI
            </span>
          </div>

          {/* Mobile close button */}
          <button
            type="button"
            onClick={onClose}
            className="rounded-lg p-1.5 text-learn-muted transition hover:bg-learn-hover md:hidden"
            aria-label="Close sidebar"
          >
            <X size={19} />
          </button>
        </div>

        {/* =========================
            NEW LESSON
        ========================== */}
        <button
          type="button"
          onClick={onNew}
          className={item}
        >
          <Plus size={18} />
          <span>New lesson</span>
        </button>

        {/* =========================
            DASHBOARD
        ========================== */}
        <Link
          to="/student-dashboard"
          onClick={onClose}
          className={`${item} ${
            isActive("/student-dashboard")
              ? activeItem
              : ""
          }`}
        >
          <LayoutDashboard size={18} />
          <span>Dashboard</span>
        </Link>

        {/* =========================
            SUBJECTS
        ========================== */}
        <Link
          to="/subjects"
          onClick={onClose}
          className={`${item} ${
            isActive("/subjects")
              ? activeItem
              : ""
          }`}
        >
          <BookOpen size={18} />
          <span>My subjects</span>
        </Link>

        {/* =========================
            PROGRESS
        ========================== */}
        <Link
          to="/progress"
          onClick={onClose}
          className={`${item} ${
            isActive("/progress")
              ? activeItem
              : ""
          }`}
        >
          <BarChart3 size={18} />
          <span>My progress</span>
        </Link>

        {/* =========================
            ASSIGNMENTS
        ========================== */}
        <Link
          to="/assignments"
          onClick={onClose}
          className={`${item} ${
            isActive("/assignments")
              ? activeItem
              : ""
          }`}
        >
          <ClipboardList size={18} />
          <span>Assignments</span>
        </Link>

        {/* =========================
            NOTIFICATIONS
        ========================== */}
        <Link
          to="/notifications"
          onClick={onClose}
          className={`${item} ${
            isActive("/notifications")
              ? activeItem
              : ""
          }`}
        >
          <Bell size={18} />
          <span>Notifications</span>
        </Link>

        {/* =========================
            RECENT LESSONS
        ========================== */}
        {recents.length > 0 && (
          <>
            <div className="px-2.5 pb-1.5 pt-5 text-[13px] font-semibold text-learn-muted">
              Recent lessons
            </div>

            <div className="min-h-0 overflow-y-auto">
              {recents.map((r) => (
                <button
                  key={`${r.subject}-${r.lesson}`}
                  type="button"
                  onClick={() => onRecent(r)}
                  className={`${item} font-medium text-learn-muted`}
                >
                  <span className="truncate">
                    {r.lesson}
                  </span>
                </button>
              ))}
            </div>
          </>
        )}

        {/* =========================
            SPACER
        ========================== */}
        <div className="flex-1" />

        {/* =========================
            PROFILE
        ========================== */}
        <Link
          to="/profile"
          onClick={onClose}
          className={`${item} ${
            isActive("/profile")
              ? activeItem
              : ""
          }`}
        >
          <User size={18} />
          <span>Profile</span>
        </Link>

        {/* =========================
            SETTINGS
        ========================== */}
        <Link
          to="/settings"
          onClick={onClose}
          className={`${item} ${
            isActive("/settings")
              ? activeItem
              : ""
          }`}
        >
          <Settings size={18} />
          <span>Settings</span>
        </Link>

        {/* =========================
            LOGOUT
        ========================== */}
        <button
          type="button"
          onClick={handleLogout}
          className={`${item} mb-2 text-red-600 hover:bg-red-50 hover:text-red-700`}
        >
          <LogOut size={18} />
          <span>Logout</span>
        </button>

        {/* =========================
            STUDENT
        ========================== */}
        <div className="-mx-2.5 flex items-center gap-2.5 border-t border-learn-line px-5 py-3">
          <div className="grid h-8 w-8 flex-none place-items-center rounded-full bg-learn-ink text-sm font-semibold text-learn-bg">
            S
          </div>

          <div className="min-w-0 leading-tight">
            <div className="truncate text-sm font-semibold text-learn-ink">
              Student
            </div>

            <div className="truncate text-xs text-learn-muted">
              {level || "Class not chosen"}
            </div>
          </div>
        </div>
      </aside>
    </>
  );
}