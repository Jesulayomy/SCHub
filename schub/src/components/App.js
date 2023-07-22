/* eslint-disable react-hooks/exhaustive-deps */
import { useContext, useEffect, useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../contexts/AuthContext';
import Layout from '../pages/Layout';
import Home from '../pages/Home';
import Login from '../pages/Login';
import AdminDashboard from '../pages/AdminDashboard';
import StudentDashboard from '../pages/StudentDashboard';
import TeacherDashboard from '../pages/TeacherDashboard';
import NotFound from '../pages/NotFound';
import StudentManager from '../pages/StudentManager';
import TeacherManager from '../pages/TeacherManager';
import CourseManager from '../pages/CourseManager';
import DepartmentManager from '../pages/DepartmentManager';
import CreateNew from '../pages/Create';
import CreatePassword from '../pages/CreatePassword';
import RecoverPassword from '../pages/RecoverPassword';

function App() {
  const [isLoading, setIsLoading] = useState(true);
  const { login } = useContext(AuthContext);

  // Fetches Authentication status and logs user in
  useEffect(() => {
    axios
      .get('http://localhost:5000/auth/auth_status', { withCredentials: true })
      .then((res) => {
        setIsLoading(false);
        const data = res.data;
        if (data.authenticated) {
          // User is Authenticated, login user
          login(data.user);
        }
      })
      .catch((err) => {
        console.log('Error:', err);
      });
  }, []);

  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Layout />}>
          <Route index element={<Home />} />
          <Route path='login' element={<Login />} />
          <Route path='password-create' element={<CreatePassword />} />
          <Route path='password-recovery' element={<RecoverPassword />} />
          <Route
            path='student-dashboard'
            element={<StudentDashboard loading={isLoading} />}
          />
          <Route
            path='teacher-dashboard'
            element={<TeacherDashboard loading={isLoading} />}
          />
          <Route
            path='admin-dashboard'
            element={<AdminDashboard loading={isLoading} />}
          />
          <Route
            path='admin-dashboard/students'
            element={<StudentManager loading={isLoading} />}
          />
          <Route
            path='admin-dashboard/students/new'
            element={<CreateNew type='student' />}
          />
          <Route
            path='admin-dashboard/teachers'
            element={<TeacherManager loading={isLoading} />}
          />
          <Route
            path='admin-dashboard/teachers/new'
            element={<CreateNew type='teacher' />}
          />
          <Route
            path='admin-dashboard/courses'
            element={<CourseManager loading={isLoading} />}
          />
          <Route
            path='admin-dashboard/courses/new'
            element={<CreateNew type='course' />}
          />
          <Route
            path='admin-dashboard/departments'
            element={<DepartmentManager loading={isLoading} />}
          />
          <Route
            path='admin-dashboard/departments/new'
            element={<CreateNew type='department' />}
          />
          <Route path='*' element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
