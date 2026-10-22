import type { Subject } from "./data";
import { SUBJECTS } from "./data";

interface Props {
  selected: Subject | null;
  locked: boolean;
  onPick: (s: Subject) => void;
  availableNames?: string[];
}

export default function SubjectCards({ selected, locked, onPick, availableNames }: Props) {
  const visibleSubjects = availableNames?.length
    ? SUBJECTS.filter((subject) => availableNames.some((name) => name.trim().toLowerCase() === subject.name.trim().toLowerCase()))
    : SUBJECTS;

  return (
    <div className="mt-3 grid grid-cols-[repeat(auto-fill,minmax(132px,1fr))] gap-2">
      {visibleSubjects.map((s) => {
        const isSel = selected?.key === s.key;
        const dim = locked && !isSel;
        return (
          <div
            key={s.key}
            role="button"
            tabIndex={dim ? -1 : 0}
            onClick={() => !dim && onPick(s)}
            onKeyDown={(e) => {
              if ((e.key === "Enter" || e.key === " ") && e.target === e.currentTarget) {
                e.preventDefault();
                onPick(s);
              }
            }}
            style={{ borderColor: isSel ? s.color : undefined, boxShadow: isSel ? `0 0 0 2px color-mix(in srgb, ${s.color} 28%, transparent)` : undefined }}
            className={`cursor-pointer rounded-xl border border-learn-line bg-learn-panel px-3 py-2.5 transition-all focus-visible:outline focus-visible:outline-2 focus-visible:outline-learn-accent ${dim ? "pointer-events-none opacity-45" : "hover:border-learn-accent"}`}
          >
            <div className="flex items-center gap-2.5">
              <div
                className="grid h-7 w-7 flex-none place-items-center rounded-lg text-[13px] font-bold"
                style={{ color: s.color, background: `color-mix(in srgb, ${s.color} 18%, transparent)` }}
              >
                {s.icon}
              </div>
              <b className="text-[15px] font-semibold text-learn-ink">{s.name}</b>
            </div>
          </div>
        );
      })}
    </div>
  );
}
