import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  CheckCircle2,
  Clock,
  FileText,
  Send,
  X,
  Sparkles,
  ArrowLeft,
  ChevronRight,
  Filter,
} from "lucide-react";
import StudentSidebar from "./StudentSidebar";

interface Assignment {
  id: string;
  title: string;
  subject: string;
  dueDate: string;
  status: "pending" | "submitted" | "graded";
  description: string;
  grade?: string;
  feedback?: string;
  submittedAt?: string;
  answer?: string;
}

const INITIAL_ASSIGNMENTS: Assignment[] = [
  {
    id: "assign-1",
    title: "Kinematics & Newton's Laws Problem Set",
    subject: "Physics",
    dueDate: "2026-10-05",
    status: "pending",
    description:
      "Solve questions 1 through 10 in Chapter 3. Show all mathematical step-by-step derivations for force vector calculations.",
  },
  {
    id: "assign-2",
    title: "Quadratic Equations & Polynomial Graphs",
    subject: "Mathematics",
    dueDate: "2026-09-28",
    status: "graded",
    grade: "92/100",
    feedback:
      "Excellent work on completing the square! Watch out for minor sign errors in Q4.",
    description:
      "Complete exercises 4B and 4C on factoring higher-degree polynomials.",
    submittedAt: "2026-09-27",
    answer:
      "I completed exercises 4B and 4C and showed the required steps for each polynomial.",
  },
  {
    id: "assign-3",
    title: "Cellular Respiration Synthesis Essay",
    subject: "Biology",
    dueDate: "2026-10-02",
    status: "submitted",
    description:
      "Write a 500-word essay comparing aerobic and anaerobic respiration processes in eukaryotic cells.",
    submittedAt: "2026-09-29",
    answer:
      "Aerobic respiration uses oxygen to release energy from glucose, while anaerobic respiration occurs without oxygen...",
  },
  {
    id: "assign-4",
    title: "Stoichiometry & Chemical Equations",
    subject: "Chemistry",
    dueDate: "2026-10-08",
    status: "pending",
    description:
      "Balance the given 15 chemical equations and calculate molar ratios.",
  },
];

const Assignments: React.FC = () => {
  const navigate = useNavigate();

  const [assignments, setAssignments] = useState<Assignment[]>(() => {
    try {
      const saved = localStorage.getItem("student_assignments_data");

      if (saved) {
        return JSON.parse(saved);
      }

      return INITIAL_ASSIGNMENTS;
    } catch {
      return INITIAL_ASSIGNMENTS;
    }
  });

  useEffect(() => {
    localStorage.setItem(
      "student_assignments_data",
      JSON.stringify(assignments)
    );
  }, [assignments]);

  const [filter, setFilter] = useState<
    "all" | "pending" | "submitted" | "graded"
  >("all");

  const [activeAssignment, setActiveAssignment] =
    useState<Assignment | null>(null);

  const [submissionText, setSubmissionText] = useState("");

  const filteredAssignments = assignments.filter((item) => {
    if (filter === "all") {
      return true;
    }

    return item.status === filter;
  });

  const pendingCount = assignments.filter(
    (assignment) => assignment.status === "pending"
  ).length;

  const submittedCount = assignments.filter(
    (assignment) => assignment.status === "submitted"
  ).length;

  const gradedCount = assignments.filter(
    (assignment) => assignment.status === "graded"
  ).length;

  const openAssignment = (assignment: Assignment) => {
    setActiveAssignment(assignment);
    setSubmissionText(assignment.answer || "");
  };

  const closeAssignment = () => {
    setActiveAssignment(null);
    setSubmissionText("");
  };

  const handleSubmitAssignment = () => {
    if (!activeAssignment) return;

    if (!submissionText.trim()) {
      return;
    }

    const updatedAssignments = assignments.map((assignment) => {
      if (assignment.id === activeAssignment.id) {
        return {
          ...assignment,
          status: "submitted" as const,
          answer: submissionText.trim(),
          submittedAt: new Date().toISOString().split("T")[0],
        };
      }

      return assignment;
    });

    setAssignments(updatedAssignments);

    const updatedAssignment = updatedAssignments.find(
      (assignment) => assignment.id === activeAssignment.id
    );

    if (updatedAssignment) {
      setActiveAssignment(updatedAssignment);
    }

    setSubmissionText("");
  };

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-800 antialiased">
      <StudentSidebar />

      <div className="ml-60">
        {/* HEADER */}
        <header className="sticky top-0 z-30 border-b border-slate-200 bg-white/95 px-8 py-5 backdrop-blur-xl">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold tracking-tight text-slate-800">
                Assignments
              </h1>

              <p className="mt-1 text-sm text-slate-500">
                View, complete and submit your assignments.
              </p>
            </div>

            <button
              onClick={() => navigate("/profile")}
              className="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-slate-600 transition hover:border-slate-300 hover:bg-slate-50 hover:text-slate-800"
            >
              <ArrowLeft size={16} />
              Back to Profile
            </button>
          </div>
        </header>

        <main className="mx-auto max-w-6xl space-y-8 p-8">
          {/* PAGE BANNER */}
          <section className="rounded-2xl bg-slate-300 p-7 shadow-sm">
            <div className="flex flex-col justify-between gap-6 md:flex-row md:items-center">
              <div>
                <div className="mb-2 inline-flex items-center gap-2 rounded-full bg-white/60 px-3 py-1 text-xs font-semibold text-slate-700">
                  <FileText size={13} />
                  Homework Tracker
                </div>

                <h2 className="text-2xl font-bold text-slate-900">
                  Course Assignments
                </h2>

                <p className="mt-2 max-w-xl text-sm leading-6 text-slate-600">
                  Complete your assignments directly on this page and submit
                  your answers for review.
                </p>
              </div>

              {/* SUMMARY */}
              <div className="grid grid-cols-3 gap-3">
                <div className="min-w-[90px] rounded-xl bg-white/60 px-4 py-3 text-center">
                  <Clock
                    size={17}
                    className="mx-auto mb-1 text-amber-600"
                  />

                  <p className="text-[11px] font-semibold uppercase text-slate-500">
                    Pending
                  </p>

                  <p className="mt-1 text-xl font-bold text-slate-900">
                    {pendingCount}
                  </p>
                </div>

                <div className="min-w-[90px] rounded-xl bg-white/60 px-4 py-3 text-center">
                  <CheckCircle2
                    size={17}
                    className="mx-auto mb-1 text-blue-600"
                  />

                  <p className="text-[11px] font-semibold uppercase text-slate-500">
                    Submitted
                  </p>

                  <p className="mt-1 text-xl font-bold text-slate-900">
                    {submittedCount}
                  </p>
                </div>

                <div className="min-w-[90px] rounded-xl bg-white/60 px-4 py-3 text-center">
                  <Sparkles
                    size={17}
                    className="mx-auto mb-1 text-green-600"
                  />

                  <p className="text-[11px] font-semibold uppercase text-slate-500">
                    Graded
                  </p>

                  <p className="mt-1 text-xl font-bold text-slate-900">
                    {gradedCount}
                  </p>
                </div>
              </div>
            </div>
          </section>

          {/* FILTER */}
          <section className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
            <div className="flex w-fit items-center gap-1 rounded-xl border border-slate-200 bg-white p-1 shadow-sm">
              {(["all", "pending", "submitted", "graded"] as const).map(
                (tab) => (
                  <button
                    key={tab}
                    onClick={() => setFilter(tab)}
                    className={`rounded-lg px-4 py-2 text-xs font-semibold capitalize transition ${
                      filter === tab
                        ? "bg-slate-800 text-white"
                        : "text-slate-500 hover:bg-slate-100 hover:text-slate-800"
                    }`}
                  >
                    {tab}
                  </button>
                )
              )}
            </div>

            <div className="flex items-center gap-1 text-xs text-slate-500">
              <Filter size={14} />

              Showing {filteredAssignments.length} assignment
              {filteredAssignments.length !== 1 ? "s" : ""}
            </div>
          </section>

          {/* ASSIGNMENTS */}
          <section className="space-y-4">
            {filteredAssignments.length === 0 ? (
              <div className="rounded-2xl border border-slate-200 bg-white p-12 text-center shadow-sm">
                <FileText
                  size={36}
                  className="mx-auto mb-3 text-slate-300"
                />

                <h3 className="text-sm font-bold text-slate-700">
                  No assignments found
                </h3>

                <p className="mt-1 text-xs text-slate-500">
                  There are no assignments in this category.
                </p>
              </div>
            ) : (
              filteredAssignments.map((assignment) => (
                <article
                  key={assignment.id}
                  className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm transition hover:border-slate-300 hover:shadow-md"
                >
                  <div className="flex flex-col justify-between gap-5 lg:flex-row">
                    {/* ASSIGNMENT INFORMATION */}
                    <div className="min-w-0 flex-1">
                      <div className="mb-3 flex flex-wrap items-center gap-2">
                        <span className="rounded-lg bg-blue-50 px-3 py-1 text-[11px] font-bold text-blue-700">
                          {assignment.subject}
                        </span>

                        {assignment.status === "pending" && (
                          <span className="inline-flex items-center gap-1 rounded-full bg-amber-50 px-3 py-1 text-[10px] font-bold text-amber-700">
                            <Clock size={11} />
                            Pending
                          </span>
                        )}

                        {assignment.status === "submitted" && (
                          <span className="inline-flex items-center gap-1 rounded-full bg-blue-50 px-3 py-1 text-[10px] font-bold text-blue-700">
                            <CheckCircle2 size={11} />
                            Submitted
                          </span>
                        )}

                        {assignment.status === "graded" && (
                          <span className="inline-flex items-center gap-1 rounded-full bg-green-50 px-3 py-1 text-[10px] font-bold text-green-700">
                            <CheckCircle2 size={11} />
                            Graded
                          </span>
                        )}
                      </div>

                      <h2 className="text-lg font-bold text-slate-800">
                        {assignment.title}
                      </h2>

                      <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-500">
                        {assignment.description}
                      </p>

                      {/* GRADE */}
                      {assignment.status === "graded" &&
                        assignment.grade && (
                          <div className="mt-4 inline-flex items-center gap-2 rounded-xl bg-green-50 px-4 py-2.5">
                            <CheckCircle2
                              size={17}
                              className="text-green-600"
                            />

                            <div>
                              <p className="text-[10px] font-semibold uppercase text-green-700">
                                Grade
                              </p>

                              <p className="text-sm font-bold text-green-800">
                                {assignment.grade}
                              </p>
                            </div>
                          </div>
                        )}

                      {/* FEEDBACK */}
                      {assignment.feedback && (
                        <div className="mt-4 rounded-xl border border-green-100 bg-green-50 p-4">
                          <p className="text-xs font-bold text-green-800">
                            Teacher Feedback
                          </p>

                          <p className="mt-1 text-sm leading-6 text-green-700">
                            {assignment.feedback}
                          </p>
                        </div>
                      )}

                      {/* SUBMITTED DATE */}
                      {assignment.submittedAt && (
                        <p className="mt-4 text-xs text-slate-400">
                          Submitted on:{" "}
                          <span className="font-semibold text-slate-600">
                            {assignment.submittedAt}
                          </span>
                        </p>
                      )}
                    </div>

                    {/* ACTION AREA */}
                    <div className="flex shrink-0 flex-col items-start justify-between gap-4 lg:items-end">
                      <div className="text-left lg:text-right">
                        <p className="text-[11px] text-slate-400">
                          Due Date
                        </p>

                        <p className="mt-1 text-sm font-bold text-slate-700">
                          {assignment.dueDate}
                        </p>
                      </div>

                      {assignment.status === "pending" ? (
                        <button
                          onClick={() => openAssignment(assignment)}
                          className="inline-flex items-center gap-2 rounded-xl bg-blue-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-blue-700 active:scale-[0.98]"
                        >
                          Do Assignment
                          <ChevronRight size={16} />
                        </button>
                      ) : (
                        <button
                          onClick={() => openAssignment(assignment)}
                          className="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-slate-700 transition hover:border-slate-300 hover:bg-slate-50"
                        >
                          View Assignment
                          <ChevronRight size={16} />
                        </button>
                      )}
                    </div>
                  </div>
                </article>
              ))
            )}
          </section>
        </main>

        {/* ASSIGNMENT MODAL */}
        {activeAssignment && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/60 px-4 py-6 backdrop-blur-sm">
            <div className="flex max-h-[90vh] w-full max-w-2xl flex-col overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-2xl">
              {/* MODAL HEADER */}
              <div className="flex items-start justify-between border-b border-slate-200 px-6 py-5">
                <div className="min-w-0 pr-4">
                  <span className="text-xs font-bold uppercase tracking-wide text-blue-600">
                    {activeAssignment.subject}
                  </span>

                  <h2 className="mt-1 text-xl font-bold text-slate-800">
                    {activeAssignment.title}
                  </h2>
                </div>

                <button
                  onClick={closeAssignment}
                  className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl border border-slate-200 text-slate-400 transition hover:bg-slate-100 hover:text-slate-700"
                >
                  <X size={18} />
                </button>
              </div>

              {/* MODAL CONTENT */}
              <div className="overflow-y-auto px-6 py-6">
                <div className="space-y-6">
                  {/* INSTRUCTIONS */}
                  <div>
                    <h3 className="mb-2 text-sm font-bold text-slate-800">
                      Assignment Instructions
                    </h3>

                    <div className="rounded-xl border border-slate-200 bg-slate-50 p-4">
                      <p className="text-sm leading-6 text-slate-600">
                        {activeAssignment.description}
                      </p>
                    </div>
                  </div>

                  {/* DUE DATE */}
                  <div className="flex items-center justify-between rounded-xl border border-slate-200 bg-white p-4">
                    <div>
                      <p className="text-xs text-slate-400">
                        Due Date
                      </p>

                      <p className="mt-1 text-sm font-bold text-slate-700">
                        {activeAssignment.dueDate}
                      </p>
                    </div>

                    <div>
                      <p className="text-xs text-slate-400">
                        Status
                      </p>

                      <p
                        className={`mt-1 text-sm font-bold capitalize ${
                          activeAssignment.status === "pending"
                            ? "text-amber-600"
                            : activeAssignment.status === "submitted"
                            ? "text-blue-600"
                            : "text-green-600"
                        }`}
                      >
                        {activeAssignment.status}
                      </p>
                    </div>
                  </div>

                  {/* STUDENT ANSWER */}
                  {activeAssignment.status === "pending" ? (
                    <div>
                      <label className="mb-2 block text-sm font-bold text-slate-800">
                        Your Answer
                      </label>

                      <p className="mb-3 text-xs leading-5 text-slate-500">
                        Write your complete answer below. Make sure you
                        answer all parts of the assignment before submitting.
                      </p>

                      <textarea
                        rows={12}
                        value={submissionText}
                        onChange={(event) =>
                          setSubmissionText(event.target.value)
                        }
                        placeholder="Write your answer here..."
                        className="w-full resize-none rounded-xl border border-slate-200 bg-white p-4 text-sm leading-6 text-slate-700 outline-none transition placeholder:text-slate-400 focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10"
                      />

                      <div className="mt-2 flex justify-between text-xs">
                        <span className="text-slate-400">
                          Type your answer directly here.
                        </span>

                        <span
                          className={
                            submissionText.trim().length > 0
                              ? "font-medium text-slate-500"
                              : "text-slate-400"
                          }
                        >
                          {submissionText.length} characters
                        </span>
                      </div>
                    </div>
                  ) : (
                    <div>
                      <h3 className="mb-2 text-sm font-bold text-slate-800">
                        Your Submitted Answer
                      </h3>

                      <div className="rounded-xl border border-slate-200 bg-slate-50 p-5">
                        {activeAssignment.answer ? (
                          <p className="whitespace-pre-wrap text-sm leading-7 text-slate-600">
                            {activeAssignment.answer}
                          </p>
                        ) : (
                          <p className="text-sm italic text-slate-400">
                            No answer was recorded.
                          </p>
                        )}
                      </div>
                    </div>
                  )}

                  {/* GRADED INFORMATION */}
                  {activeAssignment.status === "graded" && (
                    <div className="space-y-4">
                      {activeAssignment.grade && (
                        <div className="rounded-xl border border-green-200 bg-green-50 p-5">
                          <p className="text-xs font-bold uppercase tracking-wide text-green-700">
                            Grade Received
                          </p>

                          <p className="mt-1 text-2xl font-extrabold text-green-800">
                            {activeAssignment.grade}
                          </p>
                        </div>
                      )}

                      {activeAssignment.feedback && (
                        <div className="rounded-xl border border-green-200 bg-green-50 p-5">
                          <p className="text-xs font-bold text-green-800">
                            Teacher Feedback
                          </p>

                          <p className="mt-2 text-sm leading-6 text-green-700">
                            {activeAssignment.feedback}
                          </p>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>

              {/* MODAL FOOTER */}
              <div className="flex gap-3 border-t border-slate-200 bg-slate-50 px-6 py-4">
                <button
                  onClick={closeAssignment}
                  className="flex-1 rounded-xl border border-slate-200 bg-white py-3 text-sm font-semibold text-slate-600 transition hover:bg-slate-100"
                >
                  Close
                </button>

                {activeAssignment.status === "pending" && (
                  <button
                    onClick={handleSubmitAssignment}
                    disabled={!submissionText.trim()}
                    className="inline-flex flex-1 items-center justify-center gap-2 rounded-xl bg-blue-600 py-3 text-sm font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-300"
                  >
                    <Send size={16} />
                    Submit Assignment
                  </button>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Assignments;