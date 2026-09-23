import React, { useState } from "react";

const AITutorial: React.FC = () => {
  const [message, setMessage] = useState("");

  const [messages, setMessages] = useState<
    {
      sender: "student" | "ai";
      text: string;
    }[]
  >([
    {
      sender: "ai",
      text: "Hello! I am your AI Tutor. What would you like to learn today?",
    },
  ]);

  const handleSend = () => {
    if (!message.trim()) return;

    const studentMessage = message.trim();

    setMessages((previousMessages) => [
      ...previousMessages,
      {
        sender: "student",
        text: studentMessage,
      },
      {
        sender: "ai",
        text: "I received your question. I will help you understand it step by step.",
      },
    ]);

    setMessage("");
  };

  const handleTopicClick = (topic: string) => {
    setMessages((previousMessages) => [
      ...previousMessages,
      {
        sender: "student",
        text: `I want to learn ${topic}.`,
      },
      {
        sender: "ai",
        text: `Great. Let's learn ${topic} step by step. Ask me any question about this topic.`,
      },
    ]);
  };

  return (
    <div className="min-h-screen bg-gray-50">

      {/* Top Header */}
      <header className="sticky top-0 z-30 border-b border-gray-200 bg-slate-300 px-8 py-6">

        <div>
          <h1 className="text-2xl font-bold text-black">
            AI Tutorial
          </h1>

          <p className="mt-1 text-sm text-black">
            Learn with your personal AI tutor
          </p>
        </div>

      </header>

      {/* Main Content */}
      <div className="space-y-6 p-8">

        {/* Introduction */}
        <section className="rounded-2xl bg-slate-300 p-8 text-white">

          <h2 className="text-2xl font-bold">
            Welcome to your AI Tutor
          </h2>

          <p className="mt-3 max-w-3xl text-sm leading-6 text-gray-300">
            Your AI Tutor helps you understand difficult topics,
            practice questions, and learn at your own pace.
            You can choose a subject below or ask your own question.
          </p>

          <div className="mt-6 flex flex-wrap gap-4">

            <div className="rounded-xl bg-white/10 px-5 py-4">
              <p className="text-xs text-gray-400">
                Education Level
              </p>

              <p className="mt-1 font-semibold">
                Form 2
              </p>
            </div>

            <div className="rounded-xl bg-white/10 px-5 py-4">
              <p className="text-xs text-gray-400">
                Learning Mode
              </p>

              <p className="mt-1 font-semibold">
                Personalized
              </p>
            </div>

          </div>

        </section>

        {/* Subject Selection */}
        <section className="rounded-2xl border border-gray-200 bg-white p-7">

          <div>
            <h2 className="text-xl font-bold text-gray-100">
              Choose a Subject
            </h2>

            <p className="mt-1 text-sm text-gray-500">
              Select a subject to start your tutorial.
            </p>
          </div>

          <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">

            {/* Mathematics */}
            <button
              type="button"
              onClick={() => handleTopicClick("Mathematics")}
              className="rounded-xl border border-gray-200 p-5 text-left transition hover:border-purple-500 hover:bg-purple-50"
            >
              <h3 className="font-bold text-gray-900">
                Mathematics
              </h3>

              <p className="mt-2 text-sm text-gray-500">
                Algebra, equations and geometry
              </p>
            </button>

            {/* Biology */}
            <button
              type="button"
              onClick={() => handleTopicClick("Biology")}
              className="rounded-xl border border-gray-200 p-5 text-left transition hover:border-purple-500 hover:bg-purple-50"
            >
              <h3 className="font-bold text-gray-900">
                Biology
              </h3>

              <p className="mt-2 text-sm text-gray-500">
                Living things and human biology
              </p>
            </button>

            {/* Physics */}
            <button
              type="button"
              onClick={() => handleTopicClick("Physics")}
              className="rounded-xl border border-gray-200 p-5 text-left transition hover:border-purple-500 hover:bg-purple-50"
            >
              <h3 className="font-bold text-gray-900">
                Physics
              </h3>

              <p className="mt-2 text-sm text-gray-500">
                Force, motion and energy
              </p>
            </button>

            {/* Chemistry */}
            <button
              type="button"
              onClick={() => handleTopicClick("Chemistry")}
              className="rounded-xl border border-gray-200 p-5 text-left transition hover:border-purple-500 hover:bg-purple-50"
            >
              <h3 className="font-bold text-gray-900">
                Chemistry
              </h3>

              <p className="mt-2 text-sm text-gray-500">
                Matter and chemical reactions
              </p>
            </button>

          </div>

        </section>

        {/* Tutorial Area */}
        <section className="rounded-2xl border border-gray-200 bg-white">

          {/* Tutorial Header */}
          <div className="border-b border-gray-200 p-6">

            <h2 className="text-xl font-bold text-gray-900">
              Ask Your AI Tutor
            </h2>

            <p className="mt-1 text-sm text-gray-500">
              Ask questions and receive step-by-step explanations.
            </p>

          </div>

          {/* Messages */}
          <div className="min-h-[400px] space-y-5 overflow-y-auto p-6">

            {messages.map((chat, index) => (
              <div
                key={index}
                className={`flex ${
                  chat.sender === "student"
                    ? "justify-end"
                    : "justify-start"
                }`}
              >

                <div
                  className={`max-w-2xl rounded-2xl px-5 py-4 ${
                    chat.sender === "student"
                      ? "bg-purple-200 text-white"
                      : "bg-gray-100 text-gray-800"
                  }`}
                >
                  <p className="text-sm leading-6">
                    {chat.text}
                  </p>
                </div>

              </div>
            ))}

          </div>

          {/* Input Area */}
          <div className="border-t border-gray-200 p-5">

            <div className="flex flex-col gap-3 sm:flex-row">

              <input
                type="text"
                value={message}
                onChange={(event) => setMessage(event.target.value)}
                onKeyDown={(event) => {
                  if (event.key === "Enter") {
                    handleSend();
                  }
                }}
                placeholder="Ask your question..."
                className="flex-1 rounded-xl border border-gray-300 px-4 py-3 text-sm text-gray-900 outline-none transition focus:border-purple-500 focus:ring-2 focus:ring-purple-100"
              />

              <button
                type="button"
                onClick={handleSend}
                className="rounded-xl bg-slate-400 px-7 py-3 text-sm font-semibold text-white transition hover:bg-slate-300"
              >
                Send
              </button>

            </div>

          </div>

        </section>

        {/* Learning Features */}
        <section className="grid grid-cols-1 gap-6 md:grid-cols-3">

          <div className="rounded-2xl border border-gray-200 bg-white p-6">

            <h3 className="font-bold text-gray-900">
              Step-by-Step Learning
            </h3>

            <p className="mt-2 text-sm leading-6 text-gray-500">
              The tutor explains difficult concepts in simple steps
              instead of giving only the final answer.
            </p>

          </div>

          <div className="rounded-2xl border border-gray-200 bg-white p-6">

            <h3 className="font-bold text-gray-900">
              Practice Questions
            </h3>

            <p className="mt-2 text-sm leading-6 text-gray-500">
              Practice questions can be generated according to
              your subject and education level.
            </p>

          </div>

          <div className="rounded-2xl border border-gray-200 bg-white p-6">

            <h3 className="font-bold text-gray-900">
              Personalized Help
            </h3>

            <p className="mt-2 text-sm leading-6 text-gray-500">
              The tutor can provide explanations based on your
              learning progress and areas that need improvement.
            </p>

          </div>

        </section>

      </div>

    </div>
  );
};

export default AITutorial;