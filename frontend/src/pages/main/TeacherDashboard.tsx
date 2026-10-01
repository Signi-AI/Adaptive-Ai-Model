import React, { useState } from "react";
import { 
  Users, 
  BookOpen, 
  Plus, 
  Search, 
  MessageSquare, 
  Send, 
  FilePlus, 
  X,
  BarChart2
} from "lucide-react";

interface Student {
  id: string;
  name: string;
  email: string;
  course: string;
  progress: number;
  status: "Active" | "Pending" | "Completed";
  comments: string[];
}

interface Assignment {
  id: string;
  title: string;
  course: string;
  dueDate: string;
}

const mockStudents: Student[] = [
  { id: "1", name: "Neema Joseph", email: "neema@example.com", course: "Mathematics 101", progress: 85, status: "Active", comments: ["Great progress on algebra!"] },
  { id: "2", name: "Gracious Kimaro", email: "gracious@example.com", course: "Physics & Circuits", progress: 62, status: "Active", comments: [] },
  { id: "3", name: "Daniel Mtaki", email: "daniel@example.com", course: "Mathematics 101", progress: 100, status: "Completed", comments: ["Passed with flying colors."] },
  { id: "4", name: "Amani Said", email: "amani@example.com", course: "Python Basics", progress: 40, status: "Pending", comments: [] },
];

const mockAssignments: Assignment[] = [
  { id: "1", title: "Algebra Quiz #3", course: "Mathematics 101", dueDate: "2026-10-02" },
  { id: "2", title: "Circuit Simulation Lab", course: "Physics & Circuits", dueDate: "2026-10-05" },
];

const TeacherDashboard: React.FC = () => {
  const [students, setStudents] = useState<Student[]>(mockStudents);
  const [assignments, setAssignments] = useState<Assignment[]>(mockAssignments);
  const [searchTerm, setSearchTerm] = useState("");

  // Modal & Selection States
  const [selectedStudent, setSelectedStudent] = useState<Student | null>(null);
  const [commentText, setCommentText] = useState("");
  const [isAssignmentModalOpen, setIsAssignmentModalOpen] = useState(false);
  const [newAssignment, setNewAssignment] = useState({ title: "", course: "Mathematics 101", dueDate: "" });

  // Handle Comment Submission
  const handleAddComment = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedStudent || !commentText.trim()) return;

    setStudents((prev) =>
      prev.map((s) =>
        s.id === selectedStudent.id
          ? { ...s, comments: [...s.comments, commentText] }
          : s
      )
    );

    setSelectedStudent((prev) =>
      prev ? { ...prev, comments: [...prev.comments, commentText] } : null
    );
    setCommentText("");
  };

  // Handle Creating Assignment
  const handleCreateAssignment = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newAssignment.title || !newAssignment.dueDate) return;

    const created: Assignment = {
      id: Date.now().toString(),
      ...newAssignment
    };

    setAssignments([created, ...assignments]);
    setIsAssignmentModalOpen(false);
    setNewAssignment({ title: "", course: "Mathematics 101", dueDate: "" });
  };

  const filteredStudents = students.filter(
    (student) =>
      student.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      student.course.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gray-50/50 p-6 md:p-8">
      {/* Header */}
      <div className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 md:text-3xl">Teacher Dashboard</h1>
          <p className="mt-1 text-sm text-gray-500">
            Post assignments, give feedback, and monitor student progress.
          </p>
        </div>

        <button
          onClick={() => setIsAssignmentModalOpen(true)}
          className="flex items-center gap-2 rounded-xl bg-purple-600 px-4 py-2.5 text-sm font-semibold text-white shadow-md shadow-purple-200 transition-all hover:bg-purple-700 active:scale-95"
        >
          <Plus className="h-4 w-4" /> Create Assignment
        </button>
      </div>

      {/* Metrics */}
      <div className="mb-8 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <div className="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-gray-400">Total Students</span>
            <div className="rounded-xl bg-purple-50 p-2.5 text-purple-600"><Users className="h-5 w-5" /></div>
          </div>
          <p className="mt-4 text-2xl font-extrabold text-gray-900">{students.length}</p>
        </div>

        <div className="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-gray-400">Active Assignments</span>
            <div className="rounded-xl bg-blue-50 p-2.5 text-blue-600"><BookOpen className="h-5 w-5" /></div>
          </div>
          <p className="mt-4 text-2xl font-extrabold text-gray-900">{assignments.length}</p>
        </div>

        <div className="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-gray-400">Avg. Completion</span>
            <div className="rounded-xl bg-emerald-50 p-2.5 text-emerald-600"><BarChart2 className="h-5 w-5" /></div>
          </div>
          <p className="mt-4 text-2xl font-extrabold text-gray-900">72%</p>
        </div>

        <div className="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-gray-400">Feedback Sent</span>
            <div className="rounded-xl bg-amber-50 p-2.5 text-amber-600"><MessageSquare className="h-5 w-5" /></div>
          </div>
          <p className="mt-4 text-2xl font-extrabold text-gray-900">
            {students.reduce((acc, s) => acc + s.comments.length, 0)}
          </p>
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
        {/* Student Table */}
        <div className="rounded-2xl border border-gray-100 bg-white p-6 shadow-sm lg:col-span-2">
          <div className="mb-5 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <h2 className="text-lg font-bold text-gray-900">Student Progress & Feedback</h2>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
              <input
                type="text"
                placeholder="Search..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full rounded-xl border border-gray-200 bg-gray-50/50 py-2 pl-9 pr-4 text-xs font-medium outline-none focus:bg-white focus:border-purple-600 sm:w-60"
              />
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead>
                <tr className="border-b border-gray-100 text-xs font-semibold uppercase text-gray-400">
                  <th className="pb-3">Student</th>
                  <th className="pb-3">Course</th>
                  <th className="pb-3">Progress</th>
                  <th className="pb-3 text-right">Feedback</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {filteredStudents.map((student) => (
                  <tr key={student.id} className="hover:bg-gray-50/50">
                    <td className="py-4 font-semibold text-gray-900">{student.name}</td>
                    <td className="py-4 text-xs text-gray-600">{student.course}</td>
                    <td className="py-4">
                      <div className="w-28">
                        <span className="text-xs font-semibold text-gray-600">{student.progress}%</span>
                        <div className="h-1.5 w-full rounded-full bg-gray-100 mt-1">
                          <div className="h-1.5 rounded-full bg-purple-600" style={{ width: `${student.progress}%` }} />
                        </div>
                      </div>
                    </td>
                    <td className="py-4 text-right">
                      <button
                        onClick={() => setSelectedStudent(student)}
                        className="inline-flex items-center gap-1.5 rounded-lg border border-purple-200 bg-purple-50 px-3 py-1.5 text-xs font-semibold text-purple-700 hover:bg-purple-100"
                      >
                        <MessageSquare className="h-3.5 w-3.5" />
                        Comment ({student.comments.length})
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Posted Assignments List */}
        <div className="rounded-2xl border border-gray-100 bg-white p-6 shadow-sm">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-lg font-bold text-gray-900">Active Assignments</h2>
            <FilePlus className="h-5 w-5 text-purple-600" />
          </div>
          <div className="space-y-3">
            {assignments.map((assignment) => (
              <div key={assignment.id} className="rounded-xl border border-gray-100 bg-gray-50/50 p-3.5">
                <p className="text-xs font-bold text-gray-900">{assignment.title}</p>
                <div className="mt-1 flex items-center justify-between text-[11px] text-gray-500">
                  <span>{assignment.course}</span>
                  <span className="font-medium text-purple-600">Due: {assignment.dueDate}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Comment Drawer / Modal */}
      {selectedStudent && (
        <div className="fixed inset-0 z-50 flex items-center justify-end bg-black/40 backdrop-blur-sm">
          <div className="h-full w-full max-w-md bg-white p-6 shadow-2xl flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between border-b pb-4">
                <div>
                  <h3 className="font-bold text-gray-900">{selectedStudent.name}</h3>
                  <p className="text-xs text-gray-500">{selectedStudent.course}</p>
                </div>
                <button onClick={() => setSelectedStudent(null)} className="text-gray-400 hover:text-gray-600">
                  <X className="h-5 w-5" />
                </button>
              </div>

              <div className="mt-6 space-y-3 max-h-[60vh] overflow-y-auto">
                <p className="text-xs font-bold uppercase text-gray-400">Previous Comments</p>
                {selectedStudent.comments.length === 0 ? (
                  <p className="text-xs text-gray-400 italic">No feedback provided yet.</p>
                ) : (
                  selectedStudent.comments.map((comment, i) => (
                    <div key={i} className="rounded-xl bg-purple-50/60 p-3 text-xs text-purple-900">
                      {comment}
                    </div>
                  ))
                )}
              </div>
            </div>

            <form onSubmit={handleAddComment} className="mt-4 flex gap-2 border-t pt-4">
              <input
                type="text"
                placeholder="Write feedback or comment..."
                value={commentText}
                onChange={(e) => setCommentText(e.target.value)}
                className="flex-1 rounded-xl border border-gray-200 px-3 py-2 text-xs outline-none focus:border-purple-600"
              />
              <button
                type="submit"
                className="rounded-xl bg-purple-600 px-3 py-2 text-white hover:bg-purple-700"
              >
                <Send className="h-4 w-4" />
              </button>
            </form>
          </div>
        </div>
      )}

      {/* Create Assignment Modal */}
      {isAssignmentModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm">
          <div className="w-full max-w-md rounded-2xl bg-white p-6 shadow-xl">
            <div className="flex items-center justify-between border-b pb-3">
              <h3 className="font-bold text-gray-900">Create New Assignment</h3>
              <button onClick={() => setIsAssignmentModalOpen(false)} className="text-gray-400 hover:text-gray-600">
                <X className="h-5 w-5" />
              </button>
            </div>

            <form onSubmit={handleCreateAssignment} className="mt-4 space-y-4">
              <div>
                <label className="text-xs font-bold text-gray-700">Assignment Title</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Node Analysis Homework"
                  value={newAssignment.title}
                  onChange={(e) => setNewAssignment({ ...newAssignment, title: e.target.value })}
                  className="mt-1 w-full rounded-xl border border-gray-200 p-2.5 text-xs outline-none focus:border-purple-600"
                />
              </div>

              <div>
                <label className="text-xs font-bold text-gray-700">Course</label>
                <select
                  value={newAssignment.course}
                  onChange={(e) => setNewAssignment({ ...newAssignment, course: e.target.value })}
                  className="mt-1 w-full rounded-xl border border-gray-200 p-2.5 text-xs outline-none focus:border-purple-600"
                >
                  <option>Mathematics 101</option>
                  <option>Physics & Circuits</option>
                  <option>Python Basics</option>
                </select>
              </div>

              <div>
                <label className="text-xs font-bold text-gray-700">Due Date</label>
                <input
                  type="date"
                  required
                  value={newAssignment.dueDate}
                  onChange={(e) => setNewAssignment({ ...newAssignment, dueDate: e.target.value })}
                  className="mt-1 w-full rounded-xl border border-gray-200 p-2.5 text-xs outline-none focus:border-purple-600"
                />
              </div>

              <div className="flex justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setIsAssignmentModalOpen(false)}
                  className="rounded-xl border border-gray-200 px-4 py-2 text-xs font-semibold text-gray-600 hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="rounded-xl bg-purple-600 px-4 py-2 text-xs font-semibold text-white hover:bg-purple-700"
                >
                  Post Assignment
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default TeacherDashboard;