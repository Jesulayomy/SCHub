import { useContext, useState } from 'react';
import axios from 'axios';
import { Outlet, Link, useLocation } from 'react-router-dom';
import { AuthContext } from '../contexts/AuthContext';
import Button from '../components/Button';
import '../styles/layout.css';

function Layout() {
  const { isLoggedIn, logout, user } = useContext(AuthContext);
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const location = useLocation();

  function handleLogout() {
    axios
      .get('http://localhost:5000/auth/logout', { withCredentials: true })
      .then((res) => {
        logout();
        if (location.pathname !== '/') setIsLoggingIn(true);
      })
      .catch((err) => {
        console.log('Error:', err);
      });
  }

  if (isLoggedIn && isLoggingIn) setIsLoggingIn(false);

  return (
    <>
      <header >
        <Link to='/' className='head' onClick={() => setIsLoggingIn(false)}>
          SCHub
        </Link>
        {!isLoggingIn &&
          (isLoggedIn ? (
            <div className='sign-div'>
              {/* user.type.toLowerCase() */}
              <Link
                to={`/${"admin"}-dashboard`}
                className='sign dash'
              >
                Dashboard
              </Link>
              <Button onClick={handleLogout} className='sign'>
                Logout
              </Button>
            </div>
          ) : (
            <Link
              to='/login'
              className='sign'
              id='homepage_login'
              onClick={() => setIsLoggingIn(true)}
            >
              Login
            </Link>
          ))}
      </header>
      <Outlet />
    </>
  );
}

export default Layout;
