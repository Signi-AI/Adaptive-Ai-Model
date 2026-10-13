import { BarChart3, BookOpen, ClipboardList, LayoutDashboard, Plus, X } from "lucide-react";
import { Link } from "react-router-dom";
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

export default function LearnSidebar({ open, onClose, onNew, recents, onRecent, level }: Props) {
  return (
    <>
      {open && <div className="fixed inset-0 z-20 bg-black/40 md:hidden" onClick={onClose} aria-hidden="true" />}
      <aside
        className={`fixed inset-y-0 left-0 z-30 flex w-64 flex-none flex-col border-r border-learn-line bg-learn-side px-2.5 pt-3.5 transition-transform duration-300 md:static md:translate-x-0 ${open ? "translate-x-0" : "-translate-x-full"}`}
      >
        <div className="flex items-center justify-between px-2.5 pb-4 pt-1.5">
          <div className="flex items-center gap-2.5">
            <img src={logo} alt="" className="h-7 w-7 rounded-lg object-cover" />
            <span className="font-display text-2xl font-medium text-learn-ink">LearnAI</span>
          </div>
          <button type="button" onClick={onClose} className="rounded-lg p-1.5 text-learn-muted hover:bg-learn-hover md:hidden" aria-label="Close menu">
            <X size={18} />
          </button>
        </div>

        <button type="button" onClick={onNew} className={item}>
          <Plus size={18} /> New lesson
        </button>
        <Link to="/student-dashboard" className={item}>
          <LayoutDashboard size={18} /> Dashboard
        </Link>
        <Link to="/subjects" className={item}>
          <BookOpen size={18} /> My subjects
        </Link>
        <Link to="/progress" className={item}>
          <BarChart3 size={18} /> My progress
        </Link>
        <Link to="/assignments" className={item}>
          <ClipboardList size={18} /> Assignments
        </Link>

        {recents.length > 0 && (
          <>
            <div className="px-2.5 pb-1.5 pt-5 text-[13px] font-semibold text-learn-muted">Recent lessons</div>
            {recents.map((r) => (
              <button key={`${r.subject}-${r.lesson}`} type="button" onClick={() => onRecent(r)} className={`${item} font-medium text-learn-muted`}>
                <span className="truncate">{r.lesson}</span>
              </button>
            ))}
          </>
        )}

        <div className="flex-1" />
        <div className="-mx-2.5 flex items-center gap-2.5 border-t border-learn-line px-5 py-3">
          <div className="grid h-8 w-8 place-items-center rounded-full bg-learn-ink text-sm font-semibold text-learn-bg">S</div>
          <div className="leading-tight">
            <div className="text-sm font-semibold text-learn-ink">Student</div>
            <div className="text-xs text-learn-muted">{level || "Class not chosen"}</div>
          </div>
        </div>
      </aside>
    </>
  );
}
