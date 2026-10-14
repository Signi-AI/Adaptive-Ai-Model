import {

  useCallback,

  useEffect,

  useRef,

  useState,

} from "react";

import type {

  CSSProperties,

  FC,

  FormEvent,

  KeyboardEvent,

  ReactNode,

  MouseEvent,

} from "react";

import {

  ArrowUp,

  History,

  Menu,

  Moon,

  Plus,

  Pencil,

  Search,

  Sparkles,

  Sun,

  Trash2,

  X,

} from "lucide-react";

import AiMessage from "./AiMessage";

import type { RecentLesson } from "./LearnSidebar";

import SubjectBackground from "./SubjectBackground";

import SubjectCards from "./SubjectCards";

import {

  SUBJECTS,

  lessonText,

} from "./data";

import type { Subject } from "./data";

import { useStudentLayout } from "../main/Studentlayout";

type Extra =

  | "subjects"

  | "topics"

  | "lesson";

type Msg =

  | {

      id: number;

      role: "user";

      text: string;

    }

  | {

      id: number;

      role: "ai";

      paragraphs: string[];

      extra?: Extra;

      subject?: string;

      showActions?: boolean;

    };

export interface ChatSession {

  id: string;

  title: string;

  timestamp: number;

  subjectKey: string | null;

  level: string;

  messages: Msg[];

}

const WELCOME = [

  "I'm your AI teacher. We will be together on your learning journey, one step at a time.",

  "Which subject do you want to learn today?",

];

const RECENT_KEY = "learn_recent";

const SESSIONS_KEY = "learn_chat_sessions";

function loadRecents(): RecentLesson[] {

  try {

    const raw = localStorage.getItem(RECENT_KEY);

    return raw ? (JSON.parse(raw) as RecentLesson[]) : [];

  } catch {

    return [];

  }

}

function loadSessions(): ChatSession[] {

  try {

    const raw = localStorage.getItem(SESSIONS_KEY);

    return raw ? (JSON.parse(raw) as ChatSession[]) : [];

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

  const { openMenu } = useStudentLayout();

  const [dark, setDark] = useState(() =>

    window.matchMedia("(prefers-color-scheme: dark)").matches

  );

  const [subject, setSubject] = useState<Subject | null>(null);

  const [level, setLevel] = useState(

    () => localStorage.getItem("studentLevel") || ""

  );

  const [busy, setBusy] = useState(false);

  const [draft, setDraft] = useState("");

  const [recents, setRecents] = useState<RecentLesson[]>(loadRecents);

  // Chat History & Search State

  const [sessions, setSessions] = useState<ChatSession[]>(loadSessions);

  const [currentSessionId, setCurrentSessionId] = useState<string>(() => Date.now().toString());

  const [searchQuery, setSearchQuery] = useState("");

  const [showHistory, setShowHistory] = useState(false);

  const idRef = useRef(1);

  const askedRef = useRef(new Set<string>());

  const chatRef = useRef<HTMLDivElement>(null);

  const nextId = () => idRef.current++;

  const [messages, setMessages] = useState<Msg[]>([

    {

      id: nextId(),

      role: "ai",

      paragraphs: WELCOME,

      extra: "subjects",

    },

  ]);

  /*

   * Keep history sessions updated in local storage.

   */

  useEffect(() => {

    if (messages.length <= 1 && messages[0]?.role === "ai" && messages[0].extra === "subjects") return;

    setSessions((prev) => {

      const existingIdx = prev.findIndex((s) => s.id === currentSessionId);

      const title =

        messages.find((m) => m.role === "user")?.text.slice(0, 30) ||

        (subject ? `${subject.name} Chat` : "New Chat");

      const currentSession: ChatSession = {

        id: currentSessionId,

        title,

        timestamp: existingIdx >= 0 ? prev[existingIdx].timestamp : Date.now(),

        subjectKey: subject?.key || null,

        level,

        messages,

      };

      let updated: ChatSession[];

      if (existingIdx >= 0) {

        updated = [...prev];

        updated[existingIdx] = currentSession;

      } else {

        updated = [currentSession, ...prev];

      }

      try {

        localStorage.setItem(SESSIONS_KEY, JSON.stringify(updated));

      } catch {

        // Handle storage quota limits gracefully

      }

      return updated;

    });

  }, [messages, subject, level, currentSessionId]);

  /*

   * Keep recent lessons synchronized.

   */

  useEffect(() => {

    const updateRecents = () => setRecents(loadRecents());

    window.addEventListener("learn-recents-updated", updateRecents);

    return () => window.removeEventListener("learn-recents-updated", updateRecents);

  }, []);

  /*

   * Scroll chat to bottom.

   */

  const scrollEnd = useCallback(() => {

    const el = chatRef.current;

    if (el) {

      el.scrollTop = el.scrollHeight;

    }

  }, []);

  useEffect(() => {

    scrollEnd();

  }, [messages, scrollEnd]);

  /*

   * Add messages.

   */

  const push = (...added: Msg[]) => {

    if (added.some((m) => m.role === "ai")) {

      setBusy(true);

    }

    setMessages((prev) => [...prev, ...added]);

  };

  /*

   * Start a brand new session.

   */

  const startNewChat = () => {

    window.speechSynthesis?.cancel();

    askedRef.current.clear();

    setSubject(null);

    setLevel("");

    setBusy(false);

    setCurrentSessionId(Date.now().toString());

    setMessages([

      {

        id: nextId(),

        role: "ai",

        paragraphs: WELCOME,

        extra: "subjects",

      },

    ]);

  };

  /*

   * Load an existing session.

   */

  const loadSession = (session: ChatSession) => {

    setCurrentSessionId(session.id);

    setMessages(session.messages);

    const sub = SUBJECTS.find((s) => s.key === session.subjectKey) || null;

    setSubject(sub);

    setLevel(session.level);

    setShowHistory(false);

  };

  /*

   * Delete a session.

   */

  const deleteSession = (id: string, e: MouseEvent<HTMLButtonElement>) => {

    e.stopPropagation();

    const updated = sessions.filter((s) => s.id !== id);

    setSessions(updated);

    try {

      localStorage.setItem(SESSIONS_KEY, JSON.stringify(updated));

    } catch {}

    if (id === currentSessionId) {

      startNewChat();

    }

  };

  const renameSession = (id: string, e: MouseEvent<HTMLButtonElement>) => {
    e.stopPropagation();
    const session = sessions.find((item) => item.id === id);
    if (!session) return;
    const nextTitle = window.prompt("Rename this chat", session.title)?.trim();
    if (!nextTitle) return;
    const updated = sessions.map((item) =>
      item.id === id ? { ...item, title: nextTitle, timestamp: Date.now() } : item
    );
    setSessions(updated);
    try {
      localStorage.setItem(SESSIONS_KEY, JSON.stringify(updated));
    } catch {
      // Keep the current session usable if storage is unavailable.
    }
  };

  /*

   * Show topics.

   */

  const showTopics = (s: Subject, lv: string, withUser: boolean) => {

    const list: Msg[] = [];

    if (withUser) {

      list.push({

        id: nextId(),

        role: "user",

        text: `${s.name}, ${lv}`,

      });

    }

    list.push({

      id: nextId(),

      role: "ai",

      paragraphs: [

        `Here is what we will cover in ${s.name} for ${lv}. Pick the lesson you want to start with.`,

      ],

      extra: "topics",

      subject: s.key,

    });

    push(...list);

  };

  /*

   * Pick subject.

   */

  const pickSubject = (s: Subject) => {

    if (busy) return;

    setSubject(s);

    if (!askedRef.current.has(s.key)) {

      askedRef.current.add(s.key);

      push({

        id: nextId(),

        role: "ai",

        paragraphs: [

          `${s.name} it is. Now choose your class in the small menu on the card.`,

        ],

      });

    }

  };

  /*

   * Pick class.

   */

  const pickLevel = (lv: string) => {

    if (busy || !subject) return;

    setLevel(lv);

    localStorage.setItem("studentLevel", lv);

    window.dispatchEvent(new Event("student-level-updated"));

    showTopics(subject, lv, true);

  };

  /*

   * Teach lesson.

   */

  const teach = (

    s: Subject,

    topic: string,

    lesson: string,

    lv: string,

    withUser = true

  ) => {

    if (busy) return;

    const entry: RecentLesson = { subject: s.key, topic, lesson };

    const nextRecents = [

      entry,

      ...recents.filter((r) => !(r.subject === s.key && r.lesson === lesson)),

    ].slice(0, 5);

    setRecents(nextRecents);

    try {

      localStorage.setItem(RECENT_KEY, JSON.stringify(nextRecents));

      window.dispatchEvent(new Event("learn-recents-updated"));

    } catch {}

    const list: Msg[] = [];

    if (withUser) {

      list.push({

        id: nextId(),

        role: "user",

        text: lesson,

      });

    }

    list.push({

      id: nextId(),

      role: "ai",

      paragraphs: lessonText(s, topic, lesson, lv),

      extra: "lesson",

      subject: s.key,

      showActions: true,

    });

    push(...list);

  };

  /*

   * Follow-up.

   */

  const followUp = (label: string, reply: string) => {

    if (busy) return;

    push(

      { id: nextId(), role: "user", text: label },

      { id: nextId(), role: "ai", paragraphs: [reply], showActions: true }

    );

  };

  /*

   * Submit user message.

   */

  const submit = (e: FormEvent) => {

    e.preventDefault();

    const text = draft.trim();

    if (!text || busy) return;

    setDraft("");

    const reply = subject

      ? `Good question regarding ${subject.name}. This is where the AI answer will be dynamically generated.`

      : "Let us pick a subject first so I can teach you at the right level. Choose one of the cards above.";

    push(

      { id: nextId(), role: "user", text },

      { id: nextId(), role: "ai", paragraphs: [reply], showActions: true }

    );

  };

  /*

   * Enter key trigger.

   */

  const onKey = (e: KeyboardEvent<HTMLTextAreaElement>) => {

    if (e.key === "Enter" && !e.shiftKey) {

      e.preventDefault();

      e.currentTarget.form?.requestSubmit();

    }

  };

  const topicsShown = messages.some(

    (m) => m.role === "ai" && m.extra === "topics"

  );

  const filteredSessions = sessions.filter((s) =>

    s.title.toLowerCase().includes(searchQuery.toLowerCase()) ||

    s.messages.some(

      (m) => m.role === "user" && m.text.toLowerCase().includes(searchQuery.toLowerCase())

    )

  );

  const renderExtra = (m: Extract<Msg, { role: "ai" }>): ReactNode => {

    if (m.extra === "subjects") {

      return (

        <SubjectCards

          selected={subject}

          level={level}

          locked={topicsShown}

          onPick={pickSubject}

          onLevel={pickLevel}

        />

      );

    }

    const s = SUBJECTS.find((x) => x.key === m.subject);

    if (!s) return null;

    if (m.extra === "topics") {

      return (

        <div className="mt-2">

          {s.topics.map((t) => (

            <div key={t.title} className="mt-3.5">

              <h4 className="mb-1.5 text-[15px] font-semibold text-learn-ink">

                {t.title}

              </h4>

              <div className="flex flex-wrap gap-2">

                {t.lessons.map((l) => (

                  <button

                    key={l}

                    type="button"

                    className={pill}

                    onClick={() => teach(s, t.title, l, level || "Form 2")}

                  >

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

            <button

              type="button"

              className={pill}

              onClick={() =>

                followUp(

                  "Explain it simpler",

                  "Imagine you are teaching a younger friend. Start with one small example from daily life, then build up from there."

                )

              }

            >

              Explain it simpler

            </button>

            <button

              type="button"

              className={pill}

              onClick={() =>

                followUp(

                  "Give me an example",

                  "Try this: take a real situation, like sharing mangoes among friends, and see how this lesson describes it."

                )

              }

            >

              Give me an example

            </button>

            <button

              type="button"

              className={pill}

              onClick={() =>

                !busy && showTopics(s, level || "Form 2", false)

              }

            >

              Choose another topic

            </button>

          </div>

        </div>

      );

    }

    return null;

  };

  const themeStyle = {

    "--l-accent": subject?.color ?? "#7c3aed",

  } as CSSProperties;

  return (

    <div

      style={themeStyle}

      className={`learn ${

        dark ? "learn-dark" : ""

      } relative flex h-full min-w-0 flex-row overflow-hidden bg-learn-bg font-body text-base leading-relaxed text-learn-ink transition-colors duration-500`}

    >

      <SubjectBackground subject={subject} />

      {/* LEFT CHAT SIDEBAR */}
      <aside
        className={`${showHistory ? "flex" : "hidden"} relative z-20 h-full w-[285px] max-w-[85vw] shrink-0 flex-col border-r border-learn-line bg-learn-panel/95 p-3 shadow-xl backdrop-blur`}
        aria-label="Chat history sidebar"
      >
        <div className="mb-3 flex items-center gap-2 px-1">
          <div className="grid h-9 w-9 place-items-center rounded-xl bg-learn-accent text-white">
            <Sparkles size={18} />
          </div>
          <div className="min-w-0 flex-1">
            <p className="truncate text-sm font-semibold text-learn-ink">AI Tutor</p>
            <p className="text-xs text-learn-muted">Your learning space</p>
          </div>
          <button type="button" onClick={() => setShowHistory(false)} className="rounded-lg p-1.5 hover:bg-learn-hover md:hidden" aria-label="Close sidebar">
            <X size={17} />
          </button>
        </div>

        <button
          type="button"
          onClick={() => { startNewChat(); setShowHistory(false); }}
          className="mb-3 flex w-full items-center justify-center gap-2 rounded-xl border border-learn-line px-3 py-2.5 text-sm font-semibold text-learn-ink transition-colors hover:border-learn-accent hover:bg-learn-hover"
        >
          <Plus size={17} /> New chat
        </button>

        <div className="relative mb-3">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-learn-muted" />
          <input
            type="search"
            placeholder="Search chats..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full rounded-xl border border-learn-line bg-learn-bg py-2 pl-9 pr-3 text-sm text-learn-ink outline-none focus:border-learn-accent"
            aria-label="Search chat history"
          />
        </div>

        <div className="mb-2 px-2 text-xs font-semibold uppercase tracking-wider text-learn-muted">Recent chats</div>
        <div className="min-h-0 flex-1 space-y-1 overflow-y-auto">
          {filteredSessions.length === 0 ? (
            <div className="rounded-xl px-3 py-6 text-center text-sm text-learn-muted">
              {searchQuery ? "No chats match your search." : "Your conversations will appear here."}
            </div>
          ) : (
            filteredSessions.map((session) => (
              <div
                key={session.id}
                className={`group flex items-center gap-1 rounded-xl p-2 transition-colors ${session.id === currentSessionId ? "bg-learn-hover text-learn-accent" : "text-learn-ink hover:bg-learn-hover"}`}
              >
                <button type="button" onClick={() => { loadSession(session); setShowHistory(false); }} className="min-w-0 flex-1 px-1 py-1 text-left" title={session.title}>
                  <span className="block truncate text-sm font-medium">{session.title}</span>
                  <span className="mt-0.5 block text-[11px] text-learn-muted">{new Date(session.timestamp).toLocaleDateString()}</span>
                </button>
                <button type="button" onClick={(e) => renameSession(session.id, e)} className="rounded-md p-1.5 text-learn-muted opacity-70 hover:bg-learn-bg hover:text-learn-accent" aria-label={`Rename ${session.title}`} title="Rename chat">
                  <Pencil size={14} />
                </button>
                <button type="button" onClick={(e) => deleteSession(session.id, e)} className="rounded-md p-1.5 text-learn-muted opacity-70 hover:bg-red-50 hover:text-red-500" aria-label={`Delete ${session.title}`} title="Delete chat">
                  <Trash2 size={14} />
                </button>
              </div>
            ))
          )}
        </div>

        <div className="mt-3 border-t border-learn-line px-2 pt-3 text-xs text-learn-muted">
          Chat history is saved on this device.
        </div>
      </aside>

      {/* MAIN CHAT AREA */}
      <div className="relative flex min-w-0 flex-1 flex-col overflow-hidden">
        {/* TOP BAR */}
        <div className="relative z-10 flex min-h-[52px] items-center gap-2.5 border-b border-learn-line/60 px-4 py-2.5">
          <button type="button" onClick={() => setShowHistory((v) => !v)} className="grid h-9 w-9 flex-none place-items-center rounded-lg hover:bg-learn-hover" aria-label={showHistory ? "Close sidebar" : "Open sidebar"} title={showHistory ? "Close sidebar" : "Open sidebar"}>
            {showHistory ? <X size={20} /> : <Menu size={20} />}
          </button>
          <div className="flex-1 truncate font-semibold text-learn-muted">{subject?.name ?? "New lesson"}</div>
          <button type="button" onClick={startNewChat} className="flex h-9 items-center gap-1.5 rounded-lg px-2.5 text-sm font-medium hover:bg-learn-hover" title="New chat">
            <Plus size={18} /><span className="hidden sm:inline">New chat</span>
          </button>
          <button type="button" onClick={() => setDark((d) => !d)} className="grid h-9 w-9 flex-none place-items-center rounded-lg hover:bg-learn-hover" aria-label="Switch light or dark theme">
            {dark ? <Sun size={18} /> : <Moon size={18} />}
          </button>
        </div>

      {/* CHAT DISPLAY */}

      <div

        ref={chatRef}

        className="relative z-10 flex-1 overflow-y-auto"

        aria-live="polite"

      >

        <div className="mx-auto max-w-[720px] px-5 pb-6 pt-3">

          <h1 className="mb-2 mt-9 font-display text-[30px] font-medium leading-tight md:text-[38px]">

            Welcome, Student

          </h1>

          {messages.map((m) =>

            m.role === "user" ? (

              <div key={m.id} className="my-6 flex justify-end">

                <div className="max-w-[85%] rounded-2xl bg-learn-user px-4 py-2.5">

                  {m.text}

                </div>

              </div>

            ) : (

              <AiMessage

                key={m.id}

                paragraphs={m.paragraphs}

                showActions={m.showActions}

                onStart={() => setBusy(true)}

                onDone={() => setBusy(false)}

                onTick={scrollEnd}

              >

                {renderExtra(m)}

              </AiMessage>

            )

          )}

        </div>

      </div>

      {/* INPUT FORM */}

      <form

        onSubmit={submit}

        className="relative z-10 px-5 pb-4"

        autoComplete="off"

      >

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

          <button

            type="submit"

            disabled={!draft.trim() || busy}

            aria-label="Send"

            className="grid h-9 w-9 flex-none place-items-center rounded-full bg-learn-accent text-white transition-opacity disabled:cursor-not-allowed disabled:opacity-35"

          >

            <ArrowUp size={18} />

          </button>

        </div>

        <p className="mt-2 text-center text-xs text-learn-muted">

          Your AI teacher can make mistakes. Check important facts with your textbook.

        </p>

      </form>

      </div>

    </div>

  );

};

export default TutorHome;