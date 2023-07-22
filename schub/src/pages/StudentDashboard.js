/* eslint-disable react-hooks/exhaustive-deps */
import React, { useContext, useState, useEffect } from 'react';
import { Navigate } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../contexts/AuthContext';
import Button from '../components/Button';
import LoadingPage from '../components/Loading';
import '../styles/dashboard.css';

function StudentDashboard({ loading }) {
  const { isLoggedIn, user } = useContext(AuthContext);
  const [department, setDepartment] = useState(null);
  const [allCourses, setAllCourses] = useState([]);
  const [filteredCourses, setFilteredCourses] = useState([]);
  const [courses, setCourses] = useState([]);
  const [show, setShow] = useState(false);
  const [showTeacher, setShowTeacher] = useState({});

  useEffect(() => {
    if (user) {
      // fetch department of student
      axios
        .get(`http://localhost:5000/api/departments/${user.department_id}`)
        .then((res) => {
          setDepartment(res.data);
        })
        .catch((err) => {
          console.log('Error:', err);
        });

      // fetch courses of student
      axios
        .get(
          `http://localhost:5000/api/departments/${user.department_id}/courses`
        )
        .then((res) => {
          setAllCourses(res.data);
        })
        .catch((err) => {
          console.log('Error:', err);
        });
    }
  }, [user]);

  useEffect(() => {
    if (allCourses.length > 0) {
      const filteredCourses = allCourses.filter(
        (course) => course.level === user.current_level
      );
      setFilteredCourses(filteredCourses);
      setCourses(filteredCourses);
    }
  }, [allCourses]);

  function showTeacherDetails(index) {
    setShowTeacher((prevState) => ({
      ...prevState,
      [index]: !prevState[index],
    }));
  }

  function showAll() {
    if (show) {
      setCourses(filteredCourses);
      setShow(false);
    } else {
      setCourses(allCourses);
      setShow(true);
    }
  }

  return loading ? (
    <LoadingPage />
  ) : isLoggedIn ? (
    user.type === 'Student' ? (
      <section className='dashboard'>
        <h1>Welcome {user.first_name}</h1>
        <div className='logo-student'></div>
        <div className='details'>
          <h3>Profile</h3>
          <p>
            <span>Matric No: </span>
            {user.matric_no}
          </p>
          <p>
            <span>Full Name: </span>
            {user.first_name + ' ' + user.last_name}
          </p>
          <p>
            <span>Email: </span>
            {user.email}
          </p>
          <p>
            <span>Level: </span>
            {user.current_level}
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
                      showTeacherDetails(i);
                    }}
                    className={`para student ${
                      showTeacher[i] ? 'hide' : 'show'
                    }`}
                  >
                    {course.name} ({course.level}L)
                  </p>
                  {showTeacher[i] && (
                    <p className='teacher-details'>Teacher: {course.teacher}</p>
                  )}
                </div>
              ))}
              <Button name='more-courses' onClick={showAll}>
                {show
                  ? 'Show courses for current level'
                  : 'Show courses for all levels'}
              </Button>
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

export default StudentDashboard;
