import React, { useContext, useEffect, useState } from 'react';
import { AuthContext } from '../contexts/AuthContext';
import { Navigate } from 'react-router-dom';
import axios from 'axios';
import LoadingPage from '../components/Loading';
import '../styles/dashboard.css';

function TeacherDashboard({ loading }) {
  const { isLoggedIn, user } = useContext(AuthContext);
  const [department, setDepartment] = useState(null);
  const [courses, setCourses] = useState([]);
  const [showStudents, setShowStudents] = useState({});
  const [students, setStudents] = useState([]);

  useEffect(() => {
    if (user) {
      // fetch department of teacher
      axios
        .get(`http://localhost:5000/api/departments/${user.department_id}`)
        .then((res) => {
          setDepartment(res.data);
        })
        .catch((err) => {
          console.log('Error:', err);
        });

      // fetch courses of teacher
      axios
        .get(`http://localhost:5000/api/teachers/${user.id}/courses`)
        .then((res) => {
          setCourses(res.data);
        })
        .catch((err) => {
          console.log('Error:', err);
        });
    }
  }, [user]);

  function showStudentsDetails(index, departmentId) {
    if (showStudents[index]) {
      setShowStudents((prevState) => ({
        ...prevState,
        [index]: !prevState[index],
      }));
      return;
    }

    setShowStudents((prevState) => ({
      ...prevState,
      [index]: !prevState[index],
    }));

    axios
      .get(`http://localhost:5000/api/departments/${departmentId}/students`)
      .then((res) => {
        setStudents(res.data);
      })
      .catch((err) => {
        console.log(err);
      });
  }

  return loading ? (
    <LoadingPage />
  ) : isLoggedIn ? (
    user.type === 'Teacher' ? (
      <section className='dashboard'>
        <h1>Welcome {user.first_name}</h1>
        <div className='logo-teacher'></div>
        <div className='details'>
          <h3>Profile</h3>
          <p>
            <span>Full Name: </span>
            {user.first_name + ' ' + user.last_name}
          </p>
          <p>
            <span>Email: </span>
            {user.email}
          </p>
          {department && (
            <p>
              <span>Department: </span>
              {department.name}
            </p>
          )}
          {courses.length !== 0 && (
            <>
              <span>Courses: </span>
              {courses.map((course, i) => (
                <div key={course.id} className='courses'>
                  <p
                    onClick={() => {
                      showStudentsDetails(i, course.department_id);
                    }}
                    className={`para teacher ${
                      showStudents[i] ? 'hide' : 'show'
                    }`}
                  >
                    {course.name}
                  </p>
                  {showStudents[i] && students.length > 0 && (
                    <div class="student_list">
                      <span>Students:</span>
                      {students.map((student) => (
                        <p key={student.id}>
                          {student.first_name + ' ' + student.last_name}
                        </p>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </>
          )}
        </div>
      </section>
    ) : (
      <Navigate replace to={`/${user.type.toLowerCase()}-dashboard`} />
    )
  ) : (
    <Navigate replace to='/login' />
  );
}
export default TeacherDashboard;
