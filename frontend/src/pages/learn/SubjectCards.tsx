import type { Subject } from "./data";
import { LEVELS, SUBJECTS } from "./data";

interface Props {
  selected: Subject | null;
  level: string;
  locked: boolean;
  onPick: (s: Subject) => void;
  onLevel: (level: string) => void;
}

export default function SubjectCards({ selected, level, locked, onPick, onLevel }: Props) {
  return (
    <div className="mt-3 grid grid-cols-[repeat(auto-fill,minmax(132px,1fr))] gap-2">
      {SUBJECTS.map((s) => {
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
            {isSel && (
              <select
                value={level}
                onClick={(e) => e.stopPropagation()}
                onChange={(e) => onLevel(e.target.value)}
                aria-label="Your class"
                className="mt-2 w-full rounded-lg border border-learn-line bg-learn-bg px-2 py-1.5 text-sm font-medium text-learn-ink focus-visible:outline focus-visible:outline-2 focus-visible:outline-learn-accent"
              >
                <option value="" disabled>
                  Choose your class
                </option>
                {LEVELS.map((l) => (
                  <option key={l} value={l}>
                    {l}
                  </option>
                ))}
              </select>
            )}
          </div>
        );
      })}
    </div>
  );
}
