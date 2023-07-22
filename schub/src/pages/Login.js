import React, { useContext, useState } from 'react';
import { Link, Navigate } from 'react-router-dom';
import { RotatingLines } from 'react-loader-spinner';
import axios from 'axios';
import validator from 'validator';
import { AuthContext } from '../contexts/AuthContext';
import Form from '../components/Form';
import Input from '../components/Input';
import Button from '../components/Button';
import '../styles/login.css';

function Login() {
  // states for logging in
  const [startLogin, setStartLogin] = useState(false);
  const [loggingIn, setLoggingIn] = useState(false);
  const [type, setType] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  // states for handling login errors
  const [error, setError] = useState(false);
  const [emailError, setEmailError] = useState({ active: false });
  const [passwordError, setPasswordError] = useState({ active: false });
  const [loginError, setLoginError] = useState({ active: false });

  // auth context
  const { isLoggedIn, login, user } = useContext(AuthContext);

  function handleLogin(e) {
    e.preventDefault();

    if (email.length === 0) {
      setEmailError({ active: true, message: 'Email cannot be blank' });
      return;
    } else {
      setEmailError({ active: false });
    }

    if (password.length === 0) {
      setPasswordError({ active: true, message: 'Password cannot be blank' });
      return;
    } else {
      setPasswordError({ active: false });
    }

    setLoggingIn(true);

    axios
      .post(
        'http://localhost:5000/auth/login',
        { type, email, password },
        { withCredentials: true }
      )
      .then((res) => {
        const data = res.data;
        setLoggingIn(false);
        login(data.user);
      })
      .catch((err) => {
        if (err.response && err.response.status === 401) {
          setPasswordError({
            active: true,
            message: err.response.data.message,
          });
        } else if (err.response && err.response.status === 404) {
          setEmailError({
            active: true,
            message: err.response.data.message,
          });
        } else {
          setLoginError({
            active: true,
            message: 'An error occured. Please try again.',
          });
        }
        setLoggingIn(false);
      });
  }

  function handleStartLogin(e) {
    if (startLogin) {
      setStartLogin(false);
      setType('');
      setEmail('');
      setPassword('');
      setError(false);
      setEmailError({ active: false });
      setPasswordError({ active: false });
    } else {
      setStartLogin(true);
      setType(e.target.name);
    }
  }

  return isLoggedIn ? (
    <Navigate replace to={`/${user.type.toLowerCase()}-dashboard`} />
  ) : (
    <div className='form-container'>
      {startLogin ? (
        <div className='login-container'>
          <Button
            name={type}
            onClick={handleStartLogin}
            className={`login-${type.toLowerCase()}`}
          >
            {`Login as ${type}`}
          </Button>
          <Form className='login-form' onSubmit={handleLogin}>
            {loginError.active && (
              <p
                style={{
                  color: 'red',
                  textAlign: 'center',
                  fontSize: '0.8rem',
                }}
              >
                {loginError.message}
              </p>
            )}
            <Input
              type='text'
              name='email'
              placeholder='Enter Email'
              value={email}
              onChange={(e) => {
                setEmail(e.target.value);
                if (!validator.isEmail(email)) {
                  setError(true);
                  setEmailError({
                    active: true,
                    message: 'Invalid email address',
                  });
                } else {
                  setError(false);
                  setEmailError({ active: false });
                }
              }}
              error={emailError}
            />
            <br />
            <Input
              type='password'
              name='password'
              placeholder='Enter Password'
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              error={passwordError}
            />
            <br />
            {loggingIn ? (
              <Button className='disabled' disabled>
                Logging in...
                <RotatingLines
                  strokeColor='white'
                  strokeWidth='5'
                  animationDuration='0.75'
                  width='17'
                  visible={true}
                />
              </Button>
            ) : (
              <Input
                type='submit'
                value='Login'
                error={{ active: false }}
                disabled={error}
                id={error ? 'disabled' : ''}
              />
            )}
            <br />
            {type !== 'Admin' && (
              <p>
                Don't have a password yet? If you just registered with the admin
                then
                <Link to='/password-create' state={{ type: type }}>
                  Create a password
                </Link>
              </p>
            )}
            <p>
              <Link to='/password-recovery' state={{ type: type }}>
                Forgot password?
              </Link>
            </p>
          </Form>
        </div>
      ) : (
        <div className='login-container'>
          <Button
            name='Student'
            onClick={handleStartLogin}
            className='login-student'
          >
            Login as Student
          </Button>
          <br />
          <Button
            name='Teacher'
            onClick={handleStartLogin}
            className='login-teacher'
          >
            Login as Teacher
          </Button>
          <br />
          <Button
            name='Admin'
            onClick={handleStartLogin}
            className='login-admin'
          >
            Login as Admin
          </Button>
          <br />
        </div>
      )}
    </div>
  );
}

export default Login;
