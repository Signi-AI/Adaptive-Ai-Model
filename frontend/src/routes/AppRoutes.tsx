import { Route, Routes } from "react-router-dom";

import HomePage from "../pages/main/HomePage";
import Profile from "../pages/main/ProfilePage";
import Dashboard from "../pages/main/Dashbord";
import Register from "../pages/main/Register";
import Login from "../pages/main/LoginPage";

import StudentLayout from "../pages/main/Studentlayout";

import AitutorialPage from "../pages/main/AitutorialPage";
import Myprogress from "../pages/main/Myprogress";
import AssignmentPage from "../pages/main/AssignmentPage";
import Notifications from "../pages/components/Notification";
import Setting from "../pages/main/Setting";
import SubjectDetailsPage from "../pages/main/SubjectDetailsPage";
import TeacherDashboard from "../pages/main/TeacherDashboard";

import TutorHome from "../pages/learn/TutorHome";
import MySubjects from "../pages/main/SubjectsPage";
import StudentDashboard from "../pages/main/StudentDashboard";

const AppRoutes = () => {
  return (
    <Routes>
      {/* MAIN PAGES */}
      <Route
        path="/"
        element={<Dashboard />}
      />

      <Route
        path="/homepage"
        element={<HomePage />}
      />

      <Route
        path="/login"
        element={<Login />}
      />

      <Route
        path="/register"
        element={<Register />}
      />

      {/* TEACHER */}
      <Route
        path="/teacher"
        element={<TeacherDashboard />}
      />

      <Route
        path="/materials"
        element={<TeacherDashboard />}
      />

      {/* ============================= */}
      {/* STUDENT LAYOUT */}
      {/* ============================= */}

      <Route element={<StudentLayout />}>

        {/* STUDENT DASHBOARD */}
        <Route
          path="/student-dashboard"
          element={<StudentDashboard />}
        />

        {/* SUBJECTS */}
        <Route
          path="/subjects"
          element={<MySubjects />}
        />

        {/* PHYSICS */}
        <Route
          path="/subjects/physics"
          element={<SubjectDetailsPage />}
        />

        {/* AI TUTOR */}
        <Route
          path="/tutorhome"
          element={<TutorHome />}
        />

        <Route
          path="/ai-tutor"
          element={<TutorHome />}
        />

        <Route
          path="/student/ai-tutor"
          element={<AitutorialPage />}
        />

        {/* PROGRESS */}
        <Route
          path="/progress"
          element={<Myprogress />}
        />

        {/* ASSIGNMENTS */}
        <Route
          path="/assignments"
          element={<AssignmentPage />}
        />

        {/* NOTIFICATIONS */}
        <Route
          path="/notifications"
          element={<Notifications />}
        />

        {/* SETTINGS */}
        <Route
          path="/settings"
          element={<Setting />}
        />

        {/* PROFILE */}
        <Route
          path="/profile"
          element={<Profile />}
        />

      </Route>
    </Routes>
  );
};

export default AppRoutes;