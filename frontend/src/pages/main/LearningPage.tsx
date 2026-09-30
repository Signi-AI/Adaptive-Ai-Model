import React, { useState } from "react";
import { Link, useParams } from "react-router-dom";
import {
  ArrowLeft,
  BookOpen,
  FileText,
  PlayCircle,
  Download,
  HelpCircle,
  ExternalLink,
  CheckCircle2,
  Lock,
  Sparkles,
  BrainCircuit,
  Search,
} from "lucide-react";
import StudentSidebar from "../main/StudentSidebar";

// Data Structure Definitions
interface Material {
  id: string;
  title: string;
  description: string;
  type: "pdf" | "video" | "quiz" | "assignment";
  sizeOrDuration: string;
  isCompleted: boolean;
  isLocked: boolean;
  downloadUrl?: string;
}

interface Unit {
  id: string;
  unitNumber: number;
  title: string;
  materials: Material[];
}

// Sample Learning Materials Data
const LEARNING_MATERIALS_DATA: Record<
  string,
  { subjectName: string; gradeLevel: string; units: Unit[] }
> = {
  physics: {
    subjectName: "Physics & Mechanics",
    gradeLevel: "Form 2",
    units: [
      {
        id: "u1",
        unitNumber: 1,
        title: "Physical Quantities, Measurement & Units",
        materials: [
          {
            id: "m1",
            title: "Fundamental & Derived Quantities Study Guide",
            description: "Comprehensive notes explaining SI base units, dimensions, and conversions.",
            type: "pdf",
            sizeOrDuration: "2.4 MB PDF",
            isCompleted: true,
            isLocked: false,
            downloadUrl: "/downloads/physics-unit1-notes.pdf",
          },
          {
            id: "m2",
            title: "How to Read Vernier Calipers & Micrometer Screw Gauges",
            description: "Video demonstration showing correct instrument reading and zero-error adjustments.",
            type: "video",
            sizeOrDuration: "14 mins",
            isCompleted: true,
            isLocked: false,
          },
          {
            id: "m3",
            title: "Unit Conversions Self-Assessment Quiz",
            description: "10 multiple-choice questions testing unit prefixes and dimension verification.",
            type: "quiz",
            sizeOrDuration: "10 Questions",
            isCompleted: false,
            isLocked: false,
          },
        ],
      },
      {
        id: "u2",
        unitNumber: 2,
        title: "Forces and One-Dimensional Motion",
        materials: [
          {
            id: "m4",
            title: "Newton's Laws of Motion & Friction Handout",
            description: "Detailed summary covering inertial frames, momentum, and friction equations.",
            type: "pdf",
            sizeOrDuration: "3.1 MB PDF",
            isCompleted: false,
            isLocked: false,
            downloadUrl: "/downloads/newton-laws.pdf",
          },
          {
            id: "m5",
            title: "Kinematic Equations Problem-Solving Tutorial",
            description: "Worked examples of uniform acceleration, displacement graphs, and free-fall dynamics.",
            type: "video",
            sizeOrDuration: "22 mins",
            isCompleted: false,
            isLocked: false,
          },
          {
            id: "m6",
            title: "Motion & Gravity AI Practice Assignment",
            description: "Interactive numerical practice problems evaluated by AI Tutor.",
            type: "assignment",
            sizeOrDuration: "5 Problems",
            isCompleted: false,
            isLocked: true,
          },
        ],
      },
    ],
  },
};

const LearningMaterialsPage: React.FC = () => {
  const { subjectId = "physics" } = useParams<{ subjectId: string }>();
  const [selectedFilter, setSelectedFilter] = useState<string>("all");
  const [searchQuery, setSearchQuery] = useState<string>("");

  const subjectData =
    LEARNING_MATERIALS_DATA[subjectId.toLowerCase()] ||
    LEARNING_MATERIALS_DATA["physics"];

  const getMaterialIcon = (type: Material["type"]) => {
    switch (type) {
      case "pdf":
        return <FileText size={20} className="text-rose-600" />;
      case "video":
        return <PlayCircle size={20} className="text-blue-600" />;
      case "quiz":
        return <HelpCircle size={20} className="text-purple-600" />;
      case "assignment":
        return <BookOpen size={20} className="text-amber-600" />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900 antialiased">
      {/* Sidebar Navigation */}
      <StudentSidebar />

      {/* Main Content Area */}
      <main className="ml-60 min-h-screen">
        {/* TOP BAR */}
        <header className="sticky top-0 z-30 flex h-20 items-center justify-between border-b border-slate-200/80 bg-white/90 px-8 backdrop-blur-md">
          <div className="flex items-center gap-4">
            <Link
              to="/subjects"
              className="flex h-10 w-10 items-center justify-center rounded-xl border border-slate-200 bg-white text-slate-600 shadow-sm transition hover:bg-slate-100 hover:text-slate-900"
            >
              <ArrowLeft size={18} />
            </Link>
            <div>
              <span className="text-xs font-semibold uppercase tracking-wider text-purple-600">
                {subjectData.gradeLevel} Course Material
              </span>
              <h1 className="text-lg font-bold tracking-tight text-slate-900">
                {subjectData.subjectName}
              </h1>
            </div>
          </div>

          <Link
            to="/ai-tutor"
            className="flex items-center gap-2 rounded-xl bg-slate-900 px-4 py-2.5 text-xs font-semibold text-white shadow-sm transition-all hover:bg-slate-800 active:scale-95"
          >
            <BrainCircuit size={16} className="text-purple-400" />
            <span>Ask AI Tutor</span>
          </Link>
        </header>

        {/* BODY CONTAINER */}
        <div className="mx-auto max-w-6xl space-y-8 p-8">
          {/* HEADER BANNER */}
          <section className="relative overflow-hidden rounded-3xl border border-slate-200/80 bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 p-8 text-white shadow-xl">
            <div className="relative z-10 max-w-2xl">
              <span className="inline-flex items-center gap-1.5 rounded-full border border-purple-400/30 bg-purple-500/20 px-3 py-1 text-xs font-semibold text-purple-200 mb-3 backdrop-blur-md">
                <Sparkles size={12} /> Learning Resources
              </span>
              <h2 className="text-3xl font-extrabold tracking-tight">
                Study Materials & Handouts
              </h2>
              <p className="mt-2 text-sm leading-relaxed text-slate-300">
                Access lecture notes, downloadable PDFs, video tutorials, and self-assessment quizzes for {subjectData.subjectName}.
              </p>
            </div>
          </section>

          {/* SEARCH & FILTER BAR */}
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            {/* Filter Buttons */}
            <div className="flex items-center gap-2 overflow-x-auto pb-1 sm:pb-0">
              {["all", "pdf", "video", "quiz", "assignment"].map((filter) => (
                <button
                  key={filter}
                  onClick={() => setSelectedFilter(filter)}
                  className={`rounded-xl px-4 py-2 text-xs font-bold capitalize transition-all ${
                    selectedFilter === filter
                      ? "bg-slate-900 text-white shadow-sm"
                      : "border border-slate-200 bg-white text-slate-600 hover:bg-slate-100"
                  }`}
                >
                  {filter === "all" ? "All Resources" : `${filter}s`}
                </button>
              ))}
            </div>

            {/* Search Input */}
            <div className="relative w-full sm:w-72">
              <Search
                size={16}
                className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400"
              />
              <input
                type="text"
                placeholder="Search topic or document..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full rounded-xl border border-slate-200 bg-white py-2 pl-9 pr-4 text-xs font-medium text-slate-900 outline-none transition focus:border-purple-500 focus:ring-1 focus:ring-purple-500"
              />
            </div>
          </div>

          {/* UNITS & MATERIALS LIST */}
          <section className="space-y-6">
            {subjectData.units.map((unit) => {
              const filteredMaterials = unit.materials.filter((mat) => {
                const matchesFilter =
                  selectedFilter === "all" || mat.type === selectedFilter;
                const matchesSearch =
                  mat.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                  mat.description.toLowerCase().includes(searchQuery.toLowerCase());
                return matchesFilter && matchesSearch;
              });

              if (filteredMaterials.length === 0) return null;

              return (
                <div
                  key={unit.id}
                  className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-sm"
                >
                  <div className="mb-4 flex items-center gap-2.5">
                    <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-purple-100 text-xs font-bold text-purple-700">
                      U{unit.unitNumber}
                    </span>
                    <h3 className="text-base font-bold text-slate-900">
                      {unit.title}
                    </h3>
                  </div>

                  <div className="space-y-3">
                    {filteredMaterials.map((material) => (
                      <div
                        key={material.id}
                        className={`flex flex-col justify-between gap-4 rounded-xl border p-4 transition-all sm:flex-row sm:items-center ${
                          material.isLocked
                            ? "border-slate-100 bg-slate-50 opacity-60"
                            : "border-slate-200/80 bg-white hover:border-purple-300 hover:shadow-sm"
                        }`}
                      >
                        {/* Info Block */}
                        <div className="flex items-start gap-3.5">
                          <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl border border-slate-200 bg-slate-50">
                            {getMaterialIcon(material.type)}
                          </div>

                          <div>
                            <div className="flex items-center gap-2">
                              <h4 className="text-xs font-bold text-slate-900">
                                {material.title}
                              </h4>
                              {material.isCompleted && (
                                <span className="inline-flex items-center gap-1 rounded-full bg-emerald-50 px-2 py-0.5 text-[10px] font-bold text-emerald-700">
                                  <CheckCircle2 size={10} /> Completed
                                </span>
                              )}
                            </div>
                            <p className="mt-0.5 text-xs text-slate-500 leading-relaxed">
                              {material.description}
                            </p>
                            <span className="mt-1 inline-block text-[11px] font-medium text-slate-400">
                              {material.sizeOrDuration}
                            </span>
                          </div>
                        </div>

                        {/* Action Buttons */}
                        <div className="flex items-center gap-2 shrink-0 self-end sm:self-center">
                          {material.isLocked ? (
                            <span className="flex items-center gap-1.5 rounded-lg bg-slate-200/70 px-3.5 py-1.5 text-xs font-semibold text-slate-500">
                              <Lock size={14} /> Locked
                            </span>
                          ) : material.type === "pdf" ? (
                            <a
                              href={material.downloadUrl || "#"}
                              download
                              className="flex items-center gap-1.5 rounded-xl border border-slate-200 bg-slate-100 px-3.5 py-2 text-xs font-bold text-slate-800 transition hover:bg-slate-200 active:scale-95"
                            >
                              <Download size={14} />
                              <span>Download PDF</span>
                            </a>
                          ) : (
                            <button className="flex items-center gap-1.5 rounded-xl bg-slate-900 px-4 py-2 text-xs font-bold text-white shadow-sm transition hover:bg-slate-800 active:scale-95">
                              <span>Open Material</span>
                              <ExternalLink size={14} />
                            </button>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              );
            })}
          </section>
        </div>
      </main>
    </div>
  );
};

export default LearningMaterialsPage;