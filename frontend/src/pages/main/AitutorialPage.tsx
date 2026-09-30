import React, { useEffect, useRef, useState } from "react";
import {
  User,
  Search,
  Send,
  Trash2,
  Menu,
  PlusCircle,
  BookOpen,
  MessageSquare,
  X,
  WifiOff,
  LogOut,
  Settings,
  HardDrive,
  ShieldCheck,
} from "lucide-react";
import logo from "../../assets/logo.jpeg";

interface Message {
  id: number;
  sender: "user" | "ai";
  text: string;
  time: string;
}

interface Conversation {
  id: number;
  title: string;
  preview: string;
  time: string;
}

const AITutor: React.FC = () => {
  const [conversations, setConversations] = useState<Conversation[]>(() => {
    const saved = localStorage.getItem("student_ai_conversations");
    return saved
      ? JSON.parse(saved)
      : [
          {
            id: 1,
            title: "Quadratic Equations",
            preview: "Help me solve a quadratic equation",
            time: "Today",
          },
          {
            id: 2,
            title: "Photosynthesis",
            preview: "Explain photosynthesis",
            time: "Yesterday",
          },
          {
            id: 3,
            title: "English Grammar",
            preview: "What is a noun?",
            time: "Yesterday",
          },
          {
            id: 4,
            title: "Newton's Laws",
            preview: "Explain Newton's first law",
            time: "Older",
          },
        ];
  });

  const [messages, setMessages] = useState<Message[]>(() => {
    const saved = localStorage.getItem("student_ai_messages");
    return saved
      ? JSON.parse(saved)
      : [
          {
            id: 1,
            sender: "ai",
            text: "Hello! I am your AI Tutor. Ask me any question, and I'll break it down step-by-step for you.",
            time: new Date().toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
            }),
          },
        ];
  });

  const [selectedConversation, setSelectedConversation] =
    useState<number | null>(null);
  const [prompt, setPrompt] = useState("");
  const [search, setSearch] = useState("");
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [isThinking, setIsThinking] = useState(false);
  const [showProfile, setShowProfile] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement | null>(null);
  const profileRef = useRef<HTMLDivElement | null>(null);

  // Close profile dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        profileRef.current &&
        !profileRef.current.contains(event.target as Node)
      ) {
        setShowProfile(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // Save conversations locally
  useEffect(() => {
    localStorage.setItem(
      "student_ai_conversations",
      JSON.stringify(conversations)
    );
  }, [conversations]);

  // Save messages locally
  useEffect(() => {
    localStorage.setItem("student_ai_messages", JSON.stringify(messages));
  }, [messages]);

  // Auto scroll
  useEffect(() => {
    const timeout = setTimeout(() => {
      messagesEndRef.current?.scrollIntoView({
        behavior: "smooth",
        block: "end",
      });
    }, 50);

    return () => clearTimeout(timeout);
  }, [messages, isThinking]);

  // Offline AI rule-based responses
  const generateLocalResponse = (question: string): string => {
    const text = question.toLowerCase();

    if (
      text.includes("hello") ||
      text.includes("hi") ||
      text.includes("hey")
    ) {
      return "Hello! I'm ready to assist you. Which subject or topic would you like to explore today?";
    }

    if (
      text.includes("quadratic") ||
      text.includes("quadratic equation")
    ) {
      return `A quadratic equation is expressed in the standard form:

ax² + bx + c = 0

You can solve it using the quadratic formula:
x = (-b ± √(b² - 4ac)) / 2a

Example:
x² - 5x + 6 = 0

Factorizing gives:
(x - 2)(x - 3) = 0

Therefore:
x = 2  or  x = 3`;
    }

    if (
      text.includes("photosynthesis") ||
      text.includes("plant")
    ) {
      return `Photosynthesis is the process green plants use to synthesize nutrients from carbon dioxide and water using sunlight.

Inputs required:
• Sunlight energy
• Carbon dioxide (CO₂)
• Water (H₂O)

Outputs produced:
• Glucose (sugar)
• Oxygen (O₂)

This fundamental chemical reaction occurs inside specialized cell structures called chloroplasts using chlorophyll.`;
    }

    if (
      text.includes("noun") ||
      text.includes("grammar") ||
      text.includes("verb") ||
      text.includes("adjective")
    ) {
      return `Here is a quick grammar summary:

• Noun: Words that name a person, place, thing, or concept.
  (e.g., Student, Laptop, Tanzania, Courage)

• Verb: Action or state words.
  (e.g., Analyze, Solve, Study, Create)

• Adjective: Words that modify or describe a noun.
  (e.g., Brilliant, Complex, Creative)

Example sentence:
"The diligent student solved the problem effortlessly."`;
    }

    if (
      text.includes("newton") ||
      text.includes("force") ||
      text.includes("motion") ||
      text.includes("physics")
    ) {
      return `Newton's Three Laws of Motion:

1. First Law (Inertia):
An object remains at rest or in uniform motion unless acted upon by a net external force.

2. Second Law (Acceleration):
Force is proportional to the rate of change of momentum:
F = ma (Force = Mass × Acceleration)

3. Third Law (Action & Reaction):
For every action, there is an equal and opposite reaction.`;
    }

    if (
      text.includes("computer") ||
      text.includes("programming") ||
      text.includes("javascript") ||
      text.includes("react")
    ) {
      return `Computer Science & Web Development:

Programming allows humans to instruct computers using precise syntax and algorithms.

Key Tools:
• JavaScript: The primary language of the interactive web.
• React: A powerful UI library for building modular component-based web interfaces.
• TypeScript: Adds strong typing to JavaScript for enhanced code stability.`;
    }

    return `I am here to guide your study sessions offline!

I can help with:
• Mathematics & Algebra
• Physics & Natural Sciences
• Grammar & Communication
• Computer Science & Tech Concepts

Feel free to ask a specific question or ask for a practice problem!`;
  };

  // Send message
  const handleSend = () => {
    const trimmedPrompt = prompt.trim();

    if (!trimmedPrompt || isThinking) return;

    const now = new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });

    const userMessage: Message = {
      id: Date.now(),
      sender: "user",
      text: trimmedPrompt,
      time: now,
    };

    setMessages((prev) => [...prev, userMessage]);
    setPrompt("");
    setIsThinking(true);

    const newConversation: Conversation = {
      id: Date.now(),
      title:
        trimmedPrompt.length > 28
          ? trimmedPrompt.substring(0, 28) + "..."
          : trimmedPrompt,
      preview: trimmedPrompt,
      time: "Today",
    };

    setConversations((prev) => [newConversation, ...prev]);
    setSelectedConversation(newConversation.id);

    setTimeout(() => {
      const aiMessage: Message = {
        id: Date.now() + 1,
        sender: "ai",
        text: generateLocalResponse(trimmedPrompt),
        time: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      };

      setMessages((prev) => [...prev, aiMessage]);
      setIsThinking(false);
    }, 1000);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleNewChat = () => {
    if (isThinking) return;

    setSelectedConversation(null);
    setIsThinking(false);

    setMessages([
      {
        id: Date.now(),
        sender: "ai",
        text: "Hello! I am your AI Tutor. Ask me any question, and I'll break it down step-by-step for you.",
        time: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      },
    ]);

    setPrompt("");
  };

  const handleSelectConversation = (conversation: Conversation) => {
    if (isThinking) return;

    setSelectedConversation(conversation.id);

    setMessages([
      {
        id: Date.now(),
        sender: "user",
        text: conversation.preview,
        time: "Earlier",
      },
      {
        id: Date.now() + 1,
        sender: "ai",
        text: generateLocalResponse(conversation.preview),
        time: "Earlier",
      },
    ]);
  };

  const handleDeleteConversation = (e: React.MouseEvent, id: number) => {
    e.stopPropagation();

    setConversations((prev) => prev.filter((item) => item.id !== id));

    if (selectedConversation === id) {
      handleNewChat();
    }
  };

  const filteredConversations = conversations.filter(
    (c) =>
      c.title.toLowerCase().includes(search.toLowerCase()) ||
      c.preview.toLowerCase().includes(search.toLowerCase())
  );

  const todayConversations = filteredConversations.filter(
    (item) => item.time === "Today"
  );
  const yesterdayConversations = filteredConversations.filter(
    (item) => item.time === "Yesterday"
  );
  const olderConversations = filteredConversations.filter(
    (item) => item.time === "Older"
  );

  const renderConversation = (conversation: Conversation) => {
    const isSelected = selectedConversation === conversation.id;
    return (
      <div
        key={conversation.id}
        onClick={() => handleSelectConversation(conversation)}
        className={`group relative flex cursor-pointer items-center justify-between rounded-xl px-3.5 py-2.5 transition-all duration-200 ${
          isSelected
            ? "bg-purple-50 text-purple-900 shadow-sm ring-1 ring-purple-200/60"
            : "text-slate-600 hover:bg-slate-100/80 hover:text-slate-900"
        }`}
      >
        <div className="flex min-w-0 items-center gap-3">
          <MessageSquare
            size={16}
            className={`shrink-0 ${
              isSelected ? "text-purple-600" : "text-slate-400 group-hover:text-slate-600"
            }`}
          />
          <div className="min-w-0 flex-1">
            <p className="truncate text-xs font-semibold leading-tight">
              {conversation.title}
            </p>
            <p
              className={`mt-1 truncate text-[11px] ${
                isSelected ? "text-purple-600/80" : "text-slate-400"
              }`}
            >
              {conversation.preview}
            </p>
          </div>
        </div>

        <button
          onClick={(e) => handleDeleteConversation(e, conversation.id)}
          className="ml-2 rounded-lg p-1 text-slate-400 opacity-0 hover:bg-red-50 hover:text-red-500 group-hover:opacity-100 transition-all"
          title="Delete chat"
        >
          <Trash2 size={14} />
        </button>
      </div>
    );
  };

  return (
    <div className="flex h-screen overflow-hidden bg-slate-100 font-sans text-slate-900 antialiased">
      {/* SIDEBAR */}
      {sidebarOpen && (
        <aside className="relative flex w-80 flex-col border-r border-slate-200/80 bg-white/90 backdrop-blur-md">
          {/* Sidebar Header */}
          <div className="flex flex-col gap-4 border-b border-slate-200/80 p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <div className="flex h-9 w-9 items-center justify-center overflow-hidden rounded-xl ring-2 ring-purple-100 shadow-md">
                  <img
                    src={logo}
                    alt="LearnAI Logo"
                    className="h-full w-full object-cover"
                  />
                </div>
                <div>
                  <h1 className="text-sm font-extrabold tracking-tight text-slate-900">
                    LearnAI Tutor
                  </h1>
                  <span className="inline-flex items-center gap-1.5 text-[10px] font-semibold text-slate-500">
                    <WifiOff size={10} className="text-slate-400" />
                    Offline Mode
                  </span>
                </div>
              </div>

              <button
                onClick={() => setSidebarOpen(false)}
                className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-100 hover:text-slate-700"
                title="Hide sidebar"
              >
                <X size={18} />
              </button>
            </div>

            <button
              onClick={handleNewChat}
              disabled={isThinking}
              className="flex w-full items-center justify-center gap-2 rounded-xl bg-slate-900 py-2.5 text-xs font-semibold text-white shadow-sm transition-all hover:bg-purple-600 hover:shadow-md hover:shadow-purple-500/20 active:scale-[0.98] disabled:cursor-not-allowed disabled:bg-slate-300"
            >
              <PlusCircle size={16} />
              <span>New Conversation</span>
            </button>
          </div>

          {/* Search */}
          <div className="px-3.5 pt-3 pb-2">
            <div className="relative">
              <Search
                size={15}
                className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
              />
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search chats..."
                className="w-full rounded-xl border border-slate-200 bg-slate-50/70 py-2 pl-9 pr-3 text-xs outline-none transition duration-200 focus:border-purple-500 focus:bg-white focus:ring-2 focus:ring-purple-100"
              />
            </div>
          </div>

          {/* Conversations List */}
          <div className="flex-1 overflow-y-auto px-3.5 py-2 space-y-4">
            {todayConversations.length > 0 && (
              <div>
                <p className="mb-2 px-1 text-[10px] font-bold uppercase tracking-wider text-slate-400">
                  Today
                </p>
                <div className="space-y-1">{todayConversations.map(renderConversation)}</div>
              </div>
            )}

            {yesterdayConversations.length > 0 && (
              <div>
                <p className="mb-2 px-1 text-[10px] font-bold uppercase tracking-wider text-slate-400">
                  Yesterday
                </p>
                <div className="space-y-1">{yesterdayConversations.map(renderConversation)}</div>
              </div>
            )}

            {olderConversations.length > 0 && (
              <div>
                <p className="mb-2 px-1 text-[10px] font-bold uppercase tracking-wider text-slate-400">
                  Older
                </p>
                <div className="space-y-1">{olderConversations.map(renderConversation)}</div>
              </div>
            )}

            {filteredConversations.length === 0 && (
              <div className="py-12 text-center">
                <BookOpen size={24} className="mx-auto text-slate-300 mb-2" />
                <p className="text-xs font-medium text-slate-400">No conversations found</p>
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="border-t border-slate-200/80 bg-slate-50/50 p-3.5">
            <div className="flex items-center gap-3 rounded-xl bg-white p-2.5 border border-slate-200/60 shadow-xs">
              <div className="flex h-8 w-8 items-center justify-center overflow-hidden rounded-lg">
                <img src={logo} alt="LearnAI" className="h-full w-full object-cover" />
              </div>
              <div className="min-w-0 flex-1">
                <p className="text-xs font-bold text-slate-800">LearnAI Studio</p>
                <p className="text-[10px] text-slate-400 truncate">Saved locally on device</p>
              </div>
            </div>
          </div>
        </aside>
      )}

      {/* MAIN VIEW */}
      <main className="flex min-w-0 flex-1 flex-col bg-slate-50 relative">
        {/* Top Header */}
        <header className="flex h-16 items-center justify-between border-b border-slate-200/80 bg-white/80 px-6 backdrop-blur-md">
          <div className="flex items-center gap-3">
            {!sidebarOpen && (
              <button
                onClick={() => setSidebarOpen(true)}
                className="rounded-xl border border-slate-200 p-2 text-slate-600 hover:bg-slate-100 transition-all"
                title="Open sidebar"
              >
                <Menu size={18} />
              </button>
            )}

            <div className="flex items-center gap-2.5">
              <div className="flex h-8 w-8 items-center justify-center overflow-hidden rounded-lg ring-1 ring-slate-200">
                <img src={logo} alt="LearnAI Logo" className="h-full w-full object-cover" />
              </div>
              <div>
                <h2 className="text-sm font-bold text-slate-900 leading-none">
                  AI Personal Tutor
                </h2>
                <p className="mt-1 text-[11px] text-slate-400">
                  Offline Interactive Learning
                </p>
              </div>
            </div>
          </div>

          {/* User Profile Container & Dropdown */}
          <div className="relative" ref={profileRef}>
            <button
              onClick={() => setShowProfile(!showProfile)}
              className={`flex h-9 w-9 items-center justify-center rounded-xl transition-all ring-1 ${
                showProfile
                  ? "bg-purple-600 text-white ring-purple-600 shadow-md shadow-purple-500/20"
                  : "bg-slate-100 text-slate-700 hover:bg-purple-50 hover:text-purple-600 ring-slate-200/80"
              }`}
              title="User Profile"
            >
              <User size={18} />
            </button>

            {/* Profile Dropdown Menu */}
            {showProfile && (
              <div className="absolute right-0 top-12 z-50 w-72 rounded-2xl border border-slate-200 bg-white p-4 shadow-xl animate-in fade-in zoom-in-95 duration-150">
                <div className="flex items-center gap-3 border-b border-slate-100 pb-3">
                  <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-purple-100 text-purple-700 font-bold text-sm ring-1 ring-purple-200/60">
                    ST
                  </div>
                  <div className="min-w-0 flex-1">
                    <p className="text-xs font-bold text-slate-900 truncate">
                      Student Account
                    </p>
                    <p className="text-[11px] text-slate-400 truncate">
                      Local Offline Profile
                    </p>
                  </div>
                </div>

                <div className="mt-3 space-y-1">
                  <div className="flex items-center gap-2.5 rounded-lg px-2.5 py-2 text-xs text-slate-600">
                    <HardDrive size={15} className="text-slate-400" />
                    <span>Storage: LocalStorage</span>
                  </div>
                  <div className="flex items-center gap-2.5 rounded-lg px-2.5 py-2 text-xs text-slate-600">
                    <ShieldCheck size={15} className="text-emerald-500" />
                    <span>Privacy: 100% On-Device</span>
                  </div>
                  <button
                    onClick={() => {
                      alert("Offline mode active. All data remains stored locally.");
                    }}
                    className="flex w-full items-center gap-2.5 rounded-lg px-2.5 py-2 text-xs text-slate-600 hover:bg-slate-50 hover:text-slate-900 transition-colors"
                  >
                    <Settings size={15} className="text-slate-400" />
                    <span>Settings</span>
                  </button>
                </div>

                <div className="mt-3 border-t border-slate-100 pt-2">
                  <button
                    onClick={() => {
                      if (confirm("Clear local chat history?")) {
                        localStorage.removeItem("student_ai_conversations");
                        localStorage.removeItem("student_ai_messages");
                        window.location.reload();
                      }
                    }}
                    className="flex w-full items-center gap-2.5 rounded-lg px-2.5 py-2 text-xs font-semibold text-red-600 hover:bg-red-50 transition-colors"
                  >
                    <LogOut size={15} />
                    <span>Reset Local Data</span>
                  </button>
                </div>
              </div>
            )}
          </div>
        </header>

        {/* Message Thread */}
        <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-6">
          <div className="mx-auto max-w-3xl space-y-6">
            {messages.map((message) => {
              const isUser = message.sender === "user";
              return (
                <div
                  key={message.id}
                  className={`flex items-start gap-3 ${
                    isUser ? "flex-row-reverse" : "flex-row"
                  }`}
                >
                  {/* Avatar */}
                  <div
                    className={`flex h-8 w-8 shrink-0 items-center justify-center overflow-hidden rounded-xl text-xs font-bold shadow-xs ${
                      isUser ? "bg-slate-900 text-white" : "ring-1 ring-slate-200 bg-white"
                    }`}
                  >
                    {isUser ? (
                      <User size={15} />
                    ) : (
                      <img src={logo} alt="AI" className="h-full w-full object-cover" />
                    )}
                  </div>

                  {/* Content Bubble */}
                  <div
                    className={`group relative max-w-[85%] sm:max-w-[78%] rounded-2xl px-4 py-3 text-sm shadow-xs ${
                      isUser
                        ? "rounded-tr-xs bg-slate-900 text-white"
                        : "rounded-tl-xs border border-slate-200/80 bg-white text-slate-800"
                    }`}
                  >
                    <div className="whitespace-pre-line leading-relaxed font-normal">
                      {message.text}
                    </div>

                    <span
                      className={`mt-1.5 block text-[10px] ${
                        isUser
                          ? "text-slate-400 text-right"
                          : "text-slate-400 text-left"
                      }`}
                    >
                      {message.time}
                    </span>
                  </div>
                </div>
              );
            })}

            {/* AI Thinking Animation */}
            {isThinking && (
              <div className="flex items-start gap-3">
                <div className="flex h-8 w-8 shrink-0 items-center justify-center overflow-hidden rounded-xl bg-white ring-1 ring-slate-200 shadow-xs">
                  <img src={logo} alt="AI" className="h-full w-full object-cover" />
                </div>
                <div className="rounded-2xl rounded-tl-xs border border-slate-200/80 bg-white px-4 py-3 shadow-xs">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-medium text-slate-500">
                      Tutor is thinking
                    </span>
                    <div className="flex gap-1">
                      <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-purple-600 [animation-delay:-0.3s]" />
                      <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-purple-600 [animation-delay:-0.15s]" />
                      <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-purple-600" />
                    </div>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input Area */}
        <div className="p-4 bg-white/80 border-t border-slate-200/80 backdrop-blur-md">
          <div className="mx-auto max-w-3xl">
            <div className="relative flex items-end rounded-2xl border border-slate-200/80 bg-slate-50/50 p-2 shadow-sm transition-all focus-within:border-purple-500 focus-within:bg-white focus-within:ring-4 focus-within:ring-purple-100">
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask your AI Tutor anything..."
                rows={1}
                disabled={isThinking}
                className="max-h-36 min-h-[44px] flex-1 resize-none bg-transparent px-3 py-2.5 text-sm outline-none placeholder:text-slate-400 disabled:cursor-not-allowed disabled:opacity-60"
              />

              <button
                onClick={handleSend}
                disabled={!prompt.trim() || isThinking}
                className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-purple-600 text-white shadow-md shadow-purple-500/20 transition-all hover:bg-purple-700 active:scale-95 disabled:cursor-not-allowed disabled:bg-slate-200 disabled:text-slate-400 disabled:shadow-none"
                title="Send message"
              >
                <Send size={16} />
              </button>
            </div>

            <p className="mt-2 text-center text-[11px] font-medium text-slate-400">
              Offline mode active · Conversations are stored locally in your browser
            </p>
          </div>
        </div>
      </main>
    </div>
  );
};

export default AITutor;