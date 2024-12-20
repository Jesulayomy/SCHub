import React, { useContext } from 'react';
import { Link, Navigate } from 'react-router-dom';
import { AuthContext } from '../contexts/AuthContext';
import LoadingPage from '../components/Loading';
import '../styles/admin.css';

function AdminDashboard({ loading }) {
  const { isLoggedIn, user } = useContext(AuthContext);

  return loading ? (
    <LoadingPage />
  ) : isLoggedIn ? (
    // user.type === 'Admin' ? (
      <section className='admin-dashboard'>
        <h1>Welcome {user.first_name}</h1>
        <p>What would you like to do today?</p>
        <Link to='/admin-dashboard/students'>Manage Students</Link>
        <br />
        <Link to='/admin-dashboard/teachers'>Manage Teachers</Link>
        <br />
        <Link to='/admin-dashboard/courses'>Manage Courses</Link>
        <br />
        <Link to='/admin-dashboard/departments'>Manage Departments</Link>
        <br />
      </section>
    // ) : (
    //   <Navigate replace to={`/${user.type.toLowerCase()}-dashboard`} />
    // )
  ) : (
    <Navigate replace to='/login' />
  );
}
export default AdminDashboard;
