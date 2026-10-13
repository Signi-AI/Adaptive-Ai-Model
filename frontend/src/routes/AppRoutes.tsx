import { Route, Routes } from "react-router-dom";

import HomePage from "../pages/main/HomePage";
import Profile from "../pages/main/ProfilePage";
import Dashboard from "../pages/main/Dashbord";
import Register from "../pages/main/Register";
import Login from "../pages/main/LoginPage";
<<<<<<< HEAD
import StudentDashboard from "../pages/main/StudentDashboard";
=======

>>>>>>> 6d22643 (student frontend development)
import StudentLayout from "../pages/main/Studentlayout";

import AitutorialPage from "../pages/main/AitutorialPage";
import SubjectsPage from "../pages/main/SubjectsPage";
import Myprogress from "../pages/main/Myprogress";
import AssignmentPage from "../pages/main/AssignmentPage";
import Notifications from "../pages/components/Notification";
import Setting from "../pages/main/Setting";
import SubjectDetailsPage from "../pages/main/SubjectDetailsPage";
import TeacherDashboard from "../pages/main/TeacherDashboard";

import TutorHome from "../pages/learn/TutorHome";

const AppRoutes = () => {
  return (
<<<<<<< HEAD
    <div>
        <Routes>
          <Route path="/" element ={<Dashboard/>}/>
          <Route path="/teacher" element={<TeacherDashboard/>}/>

          <Route path="/materials"element={<LearningMaterialsPage/>}/>
          <Route path="/subjects/physics" element ={<SubjectDetailsPage/>}/>
          <Route path="/settings" element={<Setting/>}/>
          <Route path="/student-dashboard" element ={<StudentDashboard/>}/>
          <Route path="/notifications" element={<Notifications/>}/>
          <Route path="/assignments" element={<AssignmentPage/>}/>
          <Route path="progress" element ={<Myprogress/>}/>
          <Route path="/student/ai-tutor" element ={<AitutorialPage/>}/>
          <Route path="/subjects" element ={<SubjectsPage/>}/>
          <Route path="/ studentlayout" element ={<StudentLayout/>}/>
          <Route path="/ai-tutor" element ={<AitutorialPage/>}/>
          <Route path="/learn" element={<TutorHome/>}/>
          <Route path="/login" element = {<Login/>}/>
          <Route path="/register" element={<Register/>}/>
            <Route path="/homepage" element = {<HomePage/>}/>
            <Route path="/profile" element ={<Profile/>}/>
        </Routes>
=======
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
>>>>>>> 6d22643 (student frontend development)

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