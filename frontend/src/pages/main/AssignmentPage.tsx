import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  CheckCircle2,
  Clock,
  FileText,
  UploadCloud,
  Send,
  X,
  Sparkles,
  ArrowLeft,
  ChevronRight,
  Filter,
} from "lucide-react";
import logo from "../../assets/logo.jpeg";
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
    feedback: "Excellent work on completing the square! Watch out for minor sign errors in Q4.",
    description: "Complete exercises 4B and 4C on factoring higher-degree polynomials.",
    submittedAt: "2026-09-27",
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
  },
  {
    id: "assign-4",
    title: "Stoichiometry & Chemical Equations",
    subject: "Chemistry",
    dueDate: "2026-10-08",
    status: "pending",
    description: "Balance the given 15 chemical equations and calculate molar ratios.",
  },
];

const Assignments: React.FC = () => {
  const navigate = useNavigate();

  // Persist assignments in LocalStorage
  const [assignments, setAssignments] = useState<Assignment[]>(() => {
    const saved = localStorage.getItem("student_assignments_data");
    return saved ? JSON.parse(saved) : INITIAL_ASSIGNMENTS;
  });

  useEffect(() => {
    localStorage.setItem("student_assignments_data", JSON.stringify(assignments));
  }, [assignments]);

  // Filter state
  const [filter, setFilter] = useState<"all" | "pending" | "submitted" | "graded">("all");

  // Modal / Submission drawer state
  const [activeAssignment, setActiveAssignment] = useState<Assignment | null>(null);
  const [submissionText, setSubmissionText] = useState("");
  const [attachedFile, setAttachedFile] = useState<File | null>(null);

  // Filter logic
  const filteredAssignments = assignments.filter((item) => {
    if (filter === "all") return true;
    return item.status === filter;
  });

  // Calculate summary counts
  const pendingCount = assignments.filter((a) => a.status === "pending").length;
  const submittedCount = assignments.filter((a) => a.status === "submitted").length;
  const gradedCount = assignments.filter((a) => a.status === "graded").length;

  // Handle Submission
  const handleSubmitAssignment = () => {
    if (!activeAssignment) return;

    const updated = assignments.map((item) => {
      if (item.id === activeAssignment.id) {
        return {
          ...item,
          status: "submitted" as const,
          submittedAt: new Date().toISOString().split("T")[0],
        };
      }
      return item;
    });

    setAssignments(updated);
    setActiveAssignment(null);
    setSubmissionText("");
    setAttachedFile(null);
  };

  return (
    <div className="min-h-screen bg-white font-sans text-slate-100 antialiased">
      <div>
        <StudentSidebar />
      </div>

      <div className="ml-60">
        {/* BACKGROUND AMBIENT GLOW */}
        <div className="fixed inset-0 pointer-events-none overflow-hidden">
          <div className="absolute -left-40 -top-40 h-96 w-96 rounded-full bg-purple-600/15 blur-3xl" />
          <div className="absolute right-0 top-1/3 h-96 w-96 rounded-full bg-blue-600/10 blur-3xl" />
        </div>

        <div className="relative mx-auto max-w-6xl px-4 py-8 md:px-8">
          {/* HEADER */}
          <header className="mb-8 flex items-center justify-between border-b border-slate-800 pb-6">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center overflow-hidden rounded-xl ring-2 ring-purple-500/30 shadow-lg shadow-purple-500/10">
                <img src={logo} alt="Brand Logo" className="h-full w-full object-cover" />
              </div>
              <div>
                <h1 className="text-base font-extrabold tracking-tight text-white">
                  LearnAI Studio
                </h1>
                <p className="text-[11px] font-medium text-slate-400">
                  Student Assignments & Homework Portal
                </p>
              </div>
            </div>

            <button
              onClick={() => navigate("/profile")}
              className="flex items-center gap-2 rounded-xl border border-slate-800 bg-slate-800/60 px-4 py-2 text-xs font-semibold text-slate-300 hover:bg-slate-800 hover:text-white transition-all"
            >
              <ArrowLeft size={14} /> Back to Profile
            </button>
          </header>

          {/* PAGE BANNER */}
          <div className="mb-8 rounded-3xl border border-slate-800 bg-gradient-to-r from-slate-900 via-purple-950/30 to-slate-900 p-6 md:p-8 shadow-xl">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <span className="inline-flex items-center gap-1.5 rounded-full border border-purple-500/30 bg-purple-500/10 px-3 py-1 text-xs font-semibold text-purple-300 mb-2">
                  <Sparkles size={12} /> Homework Tracker
                </span>
                <h2 className="text-2xl font-extrabold text-white">Course Assignments</h2>
                <p className="text-xs text-slate-400 mt-1">
                  Track, complete, and submit your academic tasks across all subjects.
                </p>
              </div>

              {/* STAT SUMMARY BADGES */}
              <div className="flex items-center gap-2 sm:gap-3">
                <div className="rounded-2xl border border-amber-500/20 bg-amber-500/10 px-4 py-2.5 text-center">
                  <p className="text-[10px] font-bold text-amber-400 uppercase">Pending</p>
                  <p className="text-lg font-extrabold text-white">{pendingCount}</p>
                </div>
                <div className="rounded-2xl border border-blue-500/20 bg-blue-500/10 px-4 py-2.5 text-center">
                  <p className="text-[10px] font-bold text-blue-400 uppercase">Submitted</p>
                  <p className="text-lg font-extrabold text-white">{submittedCount}</p>
                </div>
                <div className="rounded-2xl border border-emerald-500/20 bg-emerald-500/10 px-4 py-2.5 text-center">
                  <p className="text-[10px] font-bold text-emerald-400 uppercase">Graded</p>
                  <p className="text-lg font-extrabold text-white">{gradedCount}</p>
                </div>
              </div>
            </div>
          </div>

          {/* FILTER TABS */}
          <div className="mb-6 flex items-center justify-between">
            <div className="flex items-center gap-1 rounded-2xl border border-slate-800 bg-slate-900/80 p-1.5">
              {(["all", "pending", "submitted", "graded"] as const).map((tab) => (
                <button
                  key={tab}
                  onClick={() => setFilter(tab)}
                  className={`rounded-xl px-4 py-2 text-xs font-semibold capitalize transition-all ${
                    filter === tab
                      ? "bg-purple-600 text-white shadow-md shadow-purple-600/20"
                      : "text-slate-400 hover:text-white"
                  }`}
                >
                  {tab}
                </button>
              ))}
            </div>

            <span className="text-xs text-slate-400 flex items-center gap-1">
              <Filter size={13} /> Showing {filteredAssignments.length} item(s)
            </span>
          </div>

          {/* ASSIGNMENTS LIST */}
          <div className="space-y-4">
            {filteredAssignments.length === 0 ? (
              <div className="rounded-3xl border border-slate-800 bg-slate-800/40 p-12 text-center">
                <FileText className="mx-auto text-slate-500 mb-3" size={32} />
                <p className="text-sm font-semibold text-slate-300">No assignments found</p>
                <p className="text-xs text-slate-500 mt-1">There are no tasks in this view.</p>
              </div>
            ) : (
              filteredAssignments.map((assignment) => (
                <div
                  key={assignment.id}
                  className="rounded-2xl border border-slate-800 bg-slate-800/40 p-5 backdrop-blur-md transition-all hover:border-purple-500/40 hover:bg-slate-800/70"
                >
                  <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-2.5 mb-1.5">
                        <span className="rounded-md border border-purple-500/20 bg-purple-500/10 px-2.5 py-0.5 text-[10px] font-bold text-purple-300">
                          {assignment.subject}
                        </span>

                        {/* STATUS BADGES */}
                        {assignment.status === "pending" && (
                          <span className="inline-flex items-center gap-1 rounded-full bg-amber-500/10 px-2.5 py-0.5 text-[10px] font-bold text-amber-400 border border-amber-500/20">
                            <Clock size={10} /> Pending
                          </span>
                        )}
                        {assignment.status === "submitted" && (
                          <span className="inline-flex items-center gap-1 rounded-full bg-blue-500/10 px-2.5 py-0.5 text-[10px] font-bold text-blue-400 border border-blue-500/20">
                            <CheckCircle2 size={10} /> Submitted
                          </span>
                        )}
                        {assignment.status === "graded" && (
                          <span className="inline-flex items-center gap-1 rounded-full bg-emerald-500/10 px-2.5 py-0.5 text-[10px] font-bold text-emerald-400 border border-emerald-500/20">
                            <Sparkles size={10} /> Graded ({assignment.grade})
                          </span>
                        )}
                      </div>

                      <h3 className="text-base font-bold text-white">{assignment.title}</h3>
                      <p className="mt-1 text-xs text-slate-300 leading-relaxed">
                        {assignment.description}
                      </p>

                      {/* FEEDBACK (IF GRADED) */}
                      {assignment.feedback && (
                        <div className="mt-3 rounded-xl border border-emerald-500/20 bg-emerald-950/20 p-3 text-xs text-emerald-300">
                          <span className="font-bold">Teacher Feedback:</span>{" "}
                          {assignment.feedback}
                        </div>
                      )}
                    </div>

                    {/* DATES AND ACTION BUTTON */}
                    <div className="flex flex-col sm:flex-row md:flex-col items-start md:items-end justify-between gap-3 shrink-0">
                      <div className="text-left md:text-right text-[11px] text-slate-400">
                        <p>Due Date: <span className="font-semibold text-slate-200">{assignment.dueDate}</span></p>
                        {assignment.submittedAt && (
                          <p className="text-[10px] text-slate-500">Submitted: {assignment.submittedAt}</p>
                        )}
                      </div>

                      {assignment.status === "pending" ? (
                        <button
                          onClick={() => setActiveAssignment(assignment)}
                          className="inline-flex items-center gap-1.5 rounded-xl bg-purple-600 px-4 py-2 text-xs font-semibold text-white shadow-md shadow-purple-600/20 hover:bg-purple-500 transition-all active:scale-95"
                        >
                          <span>Submit Work</span>
                          <ChevronRight size={14} />
                        </button>
                      ) : (
                        <button
                          onClick={() => setActiveAssignment(assignment)}
                          className="inline-flex items-center gap-1.5 rounded-xl border border-slate-700 bg-slate-900/80 px-4 py-2 text-xs font-semibold text-slate-300 hover:text-white transition-all"
                        >
                          <span>View Details</span>
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* SUBMISSION MODAL / DRAWER */}
        {activeAssignment && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 px-4 backdrop-blur-md">
            <div className="w-full max-w-lg rounded-3xl border border-slate-800 bg-slate-900 p-6 md:p-8 text-white shadow-2xl">
              <div className="mb-4 flex items-center justify-between border-b border-slate-800 pb-4">
                <div>
                  <span className="text-[10px] font-bold uppercase tracking-wider text-purple-400">
                    {activeAssignment.subject}
                  </span>
                  <h3 className="text-lg font-bold">{activeAssignment.title}</h3>
                </div>
                <button
                  onClick={() => setActiveAssignment(null)}
                  className="rounded-xl border border-slate-800 p-1.5 text-slate-400 hover:text-white"
                >
                  <X size={18} />
                </button>
              </div>

              <div className="space-y-4">
                <div>
                  <p className="text-xs text-slate-400 mb-1">Instructions:</p>
                  <p className="text-xs text-slate-200 rounded-xl bg-slate-950 p-3 border border-slate-800">
                    {activeAssignment.description}
                  </p>
                </div>

                {activeAssignment.status === "pending" ? (
                  <>
                    <div>
                      <label className="mb-1.5 block text-xs font-semibold text-slate-300">
                        Written Submission / Answer
                      </label>
                      <textarea
                        rows={4}
                        placeholder="Type your response or answers here..."
                        value={submissionText}
                        onChange={(e) => setSubmissionText(e.target.value)}
                        className="w-full rounded-xl border border-slate-800 bg-slate-950 p-3 text-xs text-white outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20 resize-none"
                      />
                    </div>

                    <div>
                      <label className="mb-1.5 block text-xs font-semibold text-slate-300">
                        Attach File (Optional)
                      </label>
                      <label className="flex cursor-pointer items-center justify-center gap-2 rounded-xl border border-dashed border-slate-700 bg-slate-950/50 p-4 text-xs text-slate-400 hover:border-purple-500 hover:text-purple-400 transition-all">
                        <UploadCloud size={18} />
                        <span>
                          {attachedFile ? attachedFile.name : "Click to upload document or image"}
                        </span>
                        <input
                          type="file"
                          onChange={(e) => setAttachedFile(e.target.files?.[0] || null)}
                          className="hidden"
                        />
                      </label>
                    </div>
                  </>
                ) : (
                  <div className="rounded-xl bg-slate-950/60 p-4 border border-slate-800 space-y-2">
                    <p className="text-xs font-semibold text-slate-300">
                      Submission Status:{" "}
                      <span className="text-purple-400 capitalize">{activeAssignment.status}</span>
                    </p>
                    {activeAssignment.grade && (
                      <p className="text-xs font-semibold text-emerald-400">
                        Grade Received: {activeAssignment.grade}
                      </p>
                    )}
                    {activeAssignment.feedback && (
                      <p className="text-xs text-slate-300">
                        <span className="font-bold">Feedback:</span> {activeAssignment.feedback}
                      </p>
                    )}
                  </div>
                )}
              </div>

              {/* MODAL ACTIONS */}
              <div className="mt-6 flex gap-3">
                <button
                  onClick={() => setActiveAssignment(null)}
                  className="flex-1 rounded-xl border border-slate-800 bg-slate-800/50 py-2.5 text-xs font-semibold text-slate-300 hover:bg-slate-800"
                >
                  Close
                </button>

                {activeAssignment.status === "pending" && (
                  <button
                    onClick={handleSubmitAssignment}
                    className="flex-1 inline-flex items-center justify-center gap-2 rounded-xl bg-purple-600 py-2.5 text-xs font-semibold text-white shadow-md shadow-purple-600/20 hover:bg-purple-500 transition-all"
                  >
                    <Send size={14} /> Submit Assignment
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