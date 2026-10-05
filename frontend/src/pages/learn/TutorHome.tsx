import { useCallback, useEffect, useRef, useState } from "react";
import type { CSSProperties, FC, FormEvent, KeyboardEvent, ReactNode } from "react";
import { ArrowUp, Menu, Moon, Sun } from "lucide-react";
import AiMessage from "./AiMessage";
import LearnSidebar from "./LearnSidebar";
import type { RecentLesson } from "./LearnSidebar";
import SubjectBackground from "./SubjectBackground";
import SubjectCards from "./SubjectCards";
import { SUBJECTS, lessonText } from "./data";
import type { Subject } from "./data";

type Extra = "subjects" | "topics" | "lesson";

type Msg =
  | { id: number; role: "user"; text: string }
  | { id: number; role: "ai"; paragraphs: string[]; extra?: Extra; subject?: string; showActions?: boolean };

const WELCOME = ["I'm your AI teacher. We will be together on your learning journey, one step at a time.", "Which subject do you want to learn today?"];
const RECENT_KEY = "learn_recent";

function loadRecents(): RecentLesson[] {
  try {
    const raw = localStorage.getItem(RECENT_KEY);
    return raw ? (JSON.parse(raw) as RecentLesson[]) : [];
  } catch {
    return [];
  }
}

const pill =
  "rounded-full border border-learn-line bg-learn-panel px-3.5 py-1.5 text-sm font-medium text-learn-ink transition-colors hover:border-learn-accent hover:bg-learn-hover focus-visible:outline focus-visible:outline-2 focus-visible:outline-learn-accent";

export interface TutorHomeProps {
  children?: ReactNode;
}

export const TutorHome: FC<TutorHomeProps> = () => {
  const [dark, setDark] = useState(() => window.matchMedia("(prefers-color-scheme: dark)").matches);
  const [subject, setSubject] = useState<Subject | null>(null);
  const [level, setLevel] = useState("");
  const [busy, setBusy] = useState(true);
  const [menu, setMenu] = useState(false);
  const [draft, setDraft] = useState("");
  const [recents, setRecents] = useState<RecentLesson[]>(loadRecents);

  const idRef = useRef(1);
  const askedRef = useRef(new Set<string>());
  const chatRef = useRef<HTMLDivElement>(null);
  const nextId = () => idRef.current++;

  const [messages, setMessages] = useState<Msg[]>(() => [{ id: nextId(), role: "ai", paragraphs: WELCOME, extra: "subjects" }]);

  const scrollEnd = useCallback(() => {
    const el = chatRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, []);

  useEffect(scrollEnd, [messages, scrollEnd]);

  const push = (...added: Msg[]) => {
    if (added.some((m) => m.role === "ai")) setBusy(true);
    setMessages((prev) => [...prev, ...added]);
  };

  const showTopics = (s: Subject, lv: string, withUser: boolean) => {
    const list: Msg[] = [];
    if (withUser) list.push({ id: nextId(), role: "user", text: `${s.name}, ${lv}` });
    list.push({
      id: nextId(),
      role: "ai",
      paragraphs: [`Here is what we will cover in ${s.name} for ${lv}. Pick the lesson you want to start with.`],
      extra: "topics",
      subject: s.key,
    });
    push(...list);
  };

  const pickSubject = (s: Subject) => {
    if (busy) return;
    setSubject(s);
    if (!askedRef.current.has(s.key)) {
      askedRef.current.add(s.key);
      push({ id: nextId(), role: "ai", paragraphs: [`${s.name} it is. Now choose your class in the small menu on the card.`] });
    }
  };

  const pickLevel = (lv: string) => {
    if (busy || !subject) return;
    setLevel(lv);
    showTopics(subject, lv, true);
  };

  const teach = (s: Subject, topic: string, lesson: string, lv: string, withUser = true) => {
    if (busy) return;
    const entry: RecentLesson = { subject: s.key, topic, lesson };
    const nextRecents = [entry, ...recents.filter((r) => !(r.subject === s.key && r.lesson === lesson))].slice(0, 5);
    setRecents(nextRecents);
    try {
      localStorage.setItem(RECENT_KEY, JSON.stringify(nextRecents));
    } catch {
      return;
    }
    const list: Msg[] = [];
    if (withUser) list.push({ id: nextId(), role: "user", text: lesson });
    list.push({ id: nextId(), role: "ai", paragraphs: lessonText(s, topic, lesson, lv), extra: "lesson", subject: s.key, showActions: true });
    push(...list);
  };

  const openRecent = (r: RecentLesson) => {
    const s = SUBJECTS.find((x) => x.key === r.subject);
    if (!s || busy) return;
    const lv = level || "Form 2";
    setSubject(s);
    setLevel(lv);
    setMenu(false);
    teach(s, r.topic, r.lesson, lv);
  };

  const followUp = (label: string, reply: string) => {
    if (busy) return;
    push({ id: nextId(), role: "user", text: label }, { id: nextId(), role: "ai", paragraphs: [reply], showActions: true });
  };

  const newLesson = () => {
    window.speechSynthesis?.cancel();
    askedRef.current.clear();
    setSubject(null);
    setLevel("");
    setMenu(false);
    setBusy(true);
    setMessages([{ id: nextId(), role: "ai", paragraphs: WELCOME, extra: "subjects" }]);
  };

  const submit = (e: FormEvent) => {
    e.preventDefault();
    const text = draft.trim();
    if (!text || busy) return;
    setDraft("");
    const reply = subject
      ? "Good question. This is where the AI engine will answer. For now this screen only shows the interface."
      : "Let us pick a subject first so I can teach you at the right level. Choose one of the cards above.";
    push({ id: nextId(), role: "user", text }, { id: nextId(), role: "ai", paragraphs: [reply], showActions: true });
  };

  const onKey = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      e.currentTarget.form?.requestSubmit();
    }
  };

  const topicsShown = messages.some((m) => m.role === "ai" && m.extra === "topics");

  const renderExtra = (m: Extract<Msg, { role: "ai" }>): ReactNode => {
    if (m.extra === "subjects") {
      return <SubjectCards selected={subject} level={level} locked={topicsShown} onPick={pickSubject} onLevel={pickLevel} />;
    }
    const s = SUBJECTS.find((x) => x.key === m.subject);
    if (!s) return null;
    if (m.extra === "topics") {
      return (
        <div className="mt-2">
          {s.topics.map((t) => (
            <div key={t.title} className="mt-3.5">
              <h4 className="mb-1.5 text-[15px] font-semibold text-learn-ink">{t.title}</h4>
              <div className="flex flex-wrap gap-2">
                {t.lessons.map((l) => (
                  <button key={l} type="button" className={pill} onClick={() => teach(s, t.title, l, level)}>
                    {l}
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>
      );
    }
    if (m.extra === "lesson") {
      return (
        <div>
          <div className="my-3.5 border-l-[3px] border-learn-accent py-0.5 pl-3.5 font-medium text-learn-muted">
            Check yourself: can you explain this lesson in your own words?
          </div>
          <div className="flex flex-wrap gap-2">
            <button type="button" className={pill} onClick={() => followUp("Explain it simpler", "Imagine you are teaching a younger friend. Start with one small example from daily life, then build up from there.")}>
              Explain it simpler
            </button>
            <button type="button" className={pill} onClick={() => followUp("Give me an example", "Try this: take a real situation, like sharing mangoes among friends, and see how this lesson describes it.")}>
              Give me an example
            </button>
            <button type="button" className={pill} onClick={() => !busy && showTopics(s, level || "Form 2", false)}>
              Choose another topic
            </button>
          </div>
        </div>
      );
    }
    return null;
  };

  const themeStyle = { "--l-accent": subject?.color ?? "#7c3aed" } as CSSProperties;

  return (
    <div style={themeStyle} className={`learn ${dark ? "learn-dark" : ""} flex h-screen overflow-hidden bg-learn-bg font-body text-base leading-relaxed text-learn-ink transition-colors duration-500`}>
      <LearnSidebar open={menu} onClose={() => setMenu(false)} onNew={newLesson} recents={recents} onRecent={openRecent} level={level} />

      <div className="relative flex min-w-0 flex-1 flex-col">
        <SubjectBackground subject={subject} />

        <div className="relative z-10 flex min-h-[52px] items-center gap-2.5 px-4 py-2.5">
          <button type="button" onClick={() => setMenu(true)} className="grid h-9 w-9 place-items-center rounded-lg hover:bg-learn-hover md:hidden" aria-label="Open menu">
            <Menu size={20} />
          </button>
          <div className="flex-1 truncate font-semibold text-learn-muted">{subject?.name ?? "New lesson"}</div>
          <button type="button" onClick={() => setDark((d) => !d)} className="grid h-9 w-9 place-items-center rounded-lg hover:bg-learn-hover" aria-label="Switch light or dark theme">
            {dark ? <Sun size={18} /> : <Moon size={18} />}
          </button>
        </div>

        <div ref={chatRef} className="relative z-10 flex-1 overflow-y-auto" aria-live="polite">
          <div className="mx-auto max-w-[720px] px-5 pb-6 pt-3">
            <h1 className="mb-2 mt-9 font-display text-[30px] font-medium leading-tight md:text-[38px]">Welcome, Student</h1>
            {messages.map((m) =>
              m.role === "user" ? (
                <div key={m.id} className="my-6 flex justify-end">
                  <div className="max-w-[85%] rounded-2xl bg-learn-user px-4 py-2.5">{m.text}</div>
                </div>
              ) : (
                <AiMessage key={m.id} paragraphs={m.paragraphs} showActions={m.showActions} onStart={() => setBusy(true)} onDone={() => setBusy(false)} onTick={scrollEnd}>
                  {renderExtra(m)}
                </AiMessage>
              ),
            )}
          </div>
        </div>

        <form onSubmit={submit} className="relative z-10 px-5 pb-4" autoComplete="off">
          <div className="mx-auto flex max-w-[720px] items-end gap-2.5 rounded-3xl border border-learn-line bg-learn-panel py-3 pl-5 pr-3 shadow-sm focus-within:border-learn-accent">
            <textarea
              rows={1}
              value={draft}
              onChange={(e) => setDraft(e.target.value)}
              onKeyDown={onKey}
              placeholder="Ask your AI teacher anything"
              aria-label="Ask your AI teacher"
              className="max-h-36 min-w-0 flex-1 resize-none border-0 bg-transparent py-1.5 text-learn-ink outline-none placeholder:text-learn-muted"
            />
            <button type="submit" disabled={!draft.trim() || busy} aria-label="Send" className="grid h-9 w-9 flex-none place-items-center rounded-full bg-learn-accent text-white transition-opacity disabled:cursor-not-allowed disabled:opacity-35">
              <ArrowUp size={18} />
            </button>
          </div>
          <p className="mt-2 text-center text-xs text-learn-muted">Your AI teacher can make mistakes. Check important facts with your textbook.</p>
        </form>
      </div>
    </div>
  );
};

export default TutorHome;