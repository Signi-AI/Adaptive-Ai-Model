import React, { useEffect, useRef, useState } from "react";
import {
  User,
  Search,
  Send,
  Trash2,
  Menu,
} from "lucide-react";

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
            text: "Hello! I am your AI Tutor. Ask me a question and I will help you learn.",
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

  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  // Save conversations
  useEffect(() => {
    localStorage.setItem(
      "student_ai_conversations",
      JSON.stringify(conversations)
    );
  }, [conversations]);

  // Save messages
  useEffect(() => {
    localStorage.setItem(
      "student_ai_messages",
      JSON.stringify(messages)
    );
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

  // AI response
  const generateLocalResponse = (question: string): string => {
    const text = question.toLowerCase();

    if (
      text.includes("hello") ||
      text.includes("hi") ||
      text.includes("hey")
    ) {
      return "Hello! I am ready to help you learn. What would you like to study?";
    }

    if (
      text.includes("quadratic") ||
      text.includes("quadratic equation")
    ) {
      return `A quadratic equation is usually written as:

ax² + bx + c = 0

You can solve it using the quadratic formula:

x = (-b ± √(b² - 4ac)) / 2a

For example:

x² - 5x + 6 = 0

Factorizing gives:

(x - 2)(x - 3) = 0

Therefore:

x = 2 or x = 3.`;
    }

    if (
      text.includes("photosynthesis") ||
      text.includes("plant")
    ) {
      return `Photosynthesis is the process by which green plants make their own food.

Plants use:

• Sunlight
• Carbon dioxide
• Water

They produce:

• Glucose
• Oxygen

The process mainly takes place in the leaves inside structures called chloroplasts.`;
    }

    if (
      text.includes("noun") ||
      text.includes("grammar") ||
      text.includes("verb") ||
      text.includes("adjective")
    ) {
      return `In English grammar:

A noun is a word that names a person, place, thing, or idea.

Examples:
• Teacher
• Tanzania
• Book
• Education

A verb describes an action or state.

Examples:
• Run
• Eat
• Study
• Is

An adjective describes a noun.

Example:

"The intelligent student studied."

Here, "intelligent" is the adjective.`;
    }

    if (
      text.includes("newton") ||
      text.includes("force") ||
      text.includes("motion") ||
      text.includes("physics")
    ) {
      return `Newton's three laws of motion are:

1. First Law

An object remains at rest or in uniform motion unless acted upon by an external force.

2. Second Law

Force is related to mass and acceleration:

F = ma

3. Third Law

For every action, there is an equal and opposite reaction.`;
    }

    if (
      text.includes("computer") ||
      text.includes("programming") ||
      text.includes("javascript") ||
      text.includes("react") ||
      text.includes("network")
    ) {
      return `Computer science involves studying computers, software, data, and networks.

Programming means giving instructions to a computer using a programming language.

For example, JavaScript can be used to create interactive web applications.

React is a JavaScript library commonly used to build user interfaces.`;
    }

    if (
      text.includes("math") ||
      text.includes("mathematics") ||
      text.includes("calculate") ||
      text.includes("algebra")
    ) {
      return `Mathematics is the study of numbers, quantities, structures, patterns, and relationships.

I can help you with topics such as:

• Algebra
• Geometry
• Trigonometry
• Statistics
• Equations
• Fractions
• Calculus

Send me a specific problem and I will explain it step by step.`;
    }

    if (
      text.includes("help") ||
      text.includes("what can you do")
    ) {
      return `I can help you study different subjects.

You can ask me about:

• Mathematics
• Physics
• Biology
• English
• Computer Science
• General academic questions

Ask your question and I will explain it in a simple way.`;
    }

    return `I’m here to help you learn.

You can ask me questions about:

• Mathematics
• Physics
• Biology
• English
• Computer Science
• General academic questions

Ask your question and I will explain it step by step.`;
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

    // Create conversation
    const newConversation: Conversation = {
      id: Date.now(),
      title:
        trimmedPrompt.length > 35
          ? trimmedPrompt.substring(0, 35) + "..."
          : trimmedPrompt,
      preview: trimmedPrompt,
      time: "Today",
    };

    setConversations((prev) => [
      newConversation,
      ...prev,
    ]);

    setSelectedConversation(newConversation.id);

    // AI thinking time
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
    }, 1500);
  };

  // Enter to send
  const handleKeyDown = (
    e: React.KeyboardEvent<HTMLTextAreaElement>
  ) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // New conversation
  const handleNewChat = () => {
    if (isThinking) return;

    setSelectedConversation(null);
    setIsThinking(false);

    setMessages([
      {
        id: Date.now(),
        sender: "ai",
        text: "Hello! I am your AI Tutor. Ask me a question and I will help you learn.",
        time: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      },
    ]);

    setPrompt("");
  };

  // Select conversation
  const handleSelectConversation = (
    conversation: Conversation
  ) => {
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
        text: generateLocalResponse(
          conversation.preview
        ),
        time: "Earlier",
      },
    ]);
  };

  // Delete conversation
  const handleDeleteConversation = (
    e: React.MouseEvent,
    id: number
  ) => {
    e.stopPropagation();

    setConversations((prev) =>
      prev.filter(
        (conversation) => conversation.id !== id
      )
    );

    if (selectedConversation === id) {
      handleNewChat();
    }
  };

  // Search conversations
  const filteredConversations =
    conversations.filter(
      (conversation) =>
        conversation.title
          .toLowerCase()
          .includes(search.toLowerCase()) ||
        conversation.preview
          .toLowerCase()
          .includes(search.toLowerCase())
    );

  const todayConversations =
    filteredConversations.filter(
      (item) => item.time === "Today"
    );

  const yesterdayConversations =
    filteredConversations.filter(
      (item) => item.time === "Yesterday"
    );

  const olderConversations =
    filteredConversations.filter(
      (item) => item.time === "Older"
    );

  const renderConversation = (
    conversation: Conversation
  ) => (
    <div
      key={conversation.id}
      onClick={() =>
        handleSelectConversation(conversation)
      }
      className={`group cursor-pointer rounded-lg border p-3 transition ${
        selectedConversation === conversation.id
          ? "border-slate-900 bg-slate-100"
          : "border-transparent hover:border-slate-300 hover:bg-slate-50"
      }`}
    >
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0 flex-1">
          <p className="truncate text-sm font-semibold text-slate-900">
            {conversation.title}
          </p>

          <p className="mt-1 line-clamp-2 text-xs text-slate-500">
            {conversation.preview}
          </p>
        </div>

        <button
          onClick={(e) =>
            handleDeleteConversation(
              e,
              conversation.id
            )
          }
          className="rounded-md p-1.5 text-slate-400 opacity-0 transition hover:bg-slate-200 hover:text-black group-hover:opacity-100"
          title="Delete conversation"
        >
          <Trash2 size={16} />
        </button>
      </div>
    </div>
  );

  return (
    <div className="flex h-screen overflow-hidden bg-white text-slate-900">
      {/* SIDEBAR */}
      {sidebarOpen && (
        <aside className="flex w-80 flex-col border-r border-slate-200 bg-white">
          {/* Sidebar Header */}
          <div className="border-b border-slate-200 p-4">
            <div className="flex items-center justify-between">
              <h1 className="text-lg font-bold">
                AI Tutor
              </h1>

              <button
                onClick={() =>
                  setSidebarOpen(false)
                }
                className="rounded-lg p-2 text-slate-600 hover:bg-slate-100 hover:text-black"
                title="Close menu"
              >
                <Menu size={20} />
              </button>
            </div>

            <button
              onClick={handleNewChat}
              disabled={isThinking}
              className="mt-4 w-full rounded-lg bg-black px-4 py-2.5 text-sm font-medium text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-300"
            >
              New Conversation
            </button>
          </div>

          {/* Search */}
          <div className="border-b border-slate-200 p-4">
            <div className="relative">
              <Search
                size={17}
                className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
              />

              <input
                type="text"
                value={search}
                onChange={(e) =>
                  setSearch(e.target.value)
                }
                placeholder="Search conversations..."
                className="w-full rounded-lg border border-slate-300 bg-white py-2.5 pl-10 pr-3 text-sm outline-none transition focus:border-black"
              />
            </div>
          </div>

          {/* Conversations */}
          <div className="flex-1 overflow-y-auto p-4">
            {todayConversations.length > 0 && (
              <div className="mb-6">
                <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-400">
                  Today
                </p>

                <div className="space-y-2">
                  {todayConversations.map(
                    renderConversation
                  )}
                </div>
              </div>
            )}

            {yesterdayConversations.length > 0 && (
              <div className="mb-6">
                <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-400">
                  Yesterday
                </p>

                <div className="space-y-2">
                  {yesterdayConversations.map(
                    renderConversation
                  )}
                </div>
              </div>
            )}

            {olderConversations.length > 0 && (
              <div>
                <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-400">
                  Older
                </p>

                <div className="space-y-2">
                  {olderConversations.map(
                    renderConversation
                  )}
                </div>
              </div>
            )}

            {filteredConversations.length === 0 && (
              <div className="py-10 text-center text-sm text-slate-400">
                No conversations found.
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="border-t border-slate-200 p-4">
            <p className="text-xs text-slate-500">
              AI Tutor
            </p>

            <p className="mt-1 text-xs text-slate-400">
              Your conversations are saved locally.
            </p>
          </div>
        </aside>
      )}

      {/* MAIN */}
      <main className="flex min-w-0 flex-1 flex-col">
        {/* Header */}
        <header className="flex h-16 items-center justify-between border-b border-slate-200 bg-white px-4 md:px-6">
          <div className="flex items-center gap-3">
            {!sidebarOpen && (
              <button
                onClick={() =>
                  setSidebarOpen(true)
                }
                className="rounded-lg p-2 text-slate-600 hover:bg-slate-100 hover:text-black"
                title="Open menu"
              >
                <Menu size={21} />
              </button>
            )}

            <div>
              <h2 className="text-base font-semibold">
                AI Tutor
              </h2>

              <p className="text-xs text-slate-400">
                Learning Assistant
              </p>
            </div>
          </div>

          {/* User */}
          <button
            className="flex h-9 w-9 items-center justify-center rounded-full bg-slate-100 text-slate-700 hover:bg-slate-200"
            title="User profile"
          >
            <User size={18} />
          </button>
        </header>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto bg-slate-50">
          <div className="mx-auto w-full max-w-4xl px-4 py-6 md:px-6">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`mb-6 flex ${
                  message.sender === "user"
                    ? "justify-end"
                    : "justify-start"
                }`}
              >
                <div className="max-w-[85%] md:max-w-[75%]">
                  <div
                    className={`rounded-2xl px-4 py-3 text-sm leading-6 whitespace-pre-line ${
                      message.sender === "user"
                        ? "bg-black text-white"
                        : "border border-slate-200 bg-white text-slate-800"
                    }`}
                  >
                    {message.text}
                  </div>

                  <p
                    className={`mt-1 px-1 text-[11px] text-slate-400 ${
                      message.sender === "user"
                        ? "text-right"
                        : "text-left"
                    }`}
                  >
                    {message.time}
                  </p>
                </div>
              </div>
            ))}

            {/* AI Thinking */}
            {isThinking && (
              <div className="mb-6 flex justify-start">
                <div className="rounded-2xl border border-slate-200 bg-white px-4 py-3">
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-slate-500">
                      AI is thinking
                    </span>

                    <span className="flex gap-1">
                      <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-slate-500 [animation-delay:-0.3s]" />
                      <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-slate-500 [animation-delay:-0.15s]" />
                      <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-slate-500" />
                    </span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input */}
        <div className="border-t border-slate-200 bg-white p-4">
          <div className="mx-auto max-w-4xl">
            <div className="flex items-end gap-2 rounded-xl border border-slate-300 bg-white p-2 focus-within:border-black">
              <textarea
                value={prompt}
                onChange={(e) =>
                  setPrompt(e.target.value)
                }
                onKeyDown={handleKeyDown}
                placeholder="Ask your AI Tutor..."
                rows={1}
                disabled={isThinking}
                className="max-h-32 min-h-[42px] flex-1 resize-none bg-transparent px-2 py-2 text-sm outline-none disabled:cursor-not-allowed disabled:opacity-60"
              />

              <button
                onClick={handleSend}
                disabled={!prompt.trim() || isThinking}
                className="flex h-10 w-10 items-center justify-center rounded-lg bg-black text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-300"
                title="Send message"
              >
                <Send size={18} />
              </button>
            </div>

            <p className="mt-2 text-center text-xs text-slate-400">
              Press Enter to send · Shift + Enter for a new line
            </p>
          </div>
        </div>
      </main>
    </div>
  );
};

export default AITutor;