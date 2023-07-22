import { useState, useEffect } from 'react';
import { useLocation, Navigate } from 'react-router-dom';
import { RotatingLines } from 'react-loader-spinner';
import validator from 'validator';
import Input from '../components/Input';
import Button from '../components/Button';
import Form from '../components/Form';
import axios from 'axios';
import '../styles/create.css';

function RecoverPassword() {
  const location = useLocation();
  const { type } = location.state;

  const [email, setEmail] = useState('');
  const [user, setUser] = useState({});
  const [recoveryAnswer, setRecoveryAnswer] = useState('');
  const [verified, setVerified] = useState(false);
  const [password, setPassword] = useState('');
  const [verify, setVerify] = useState('');

  const [error, setError] = useState(false);
  const [emailError, setEmailError] = useState({ active: false });
  const [fetchError, setFetchError] = useState({ active: false });
  const [recoveryError, setRecoveryError] = useState({ active: false });
  const [recoveryAnswerError, setRecoveryAnswerError] = useState('');
  const [passwordError, setPasswordError] = useState({ active: false });
  const [verifyError, setVerifyError] = useState({ active: false });

  const [creating, setCreating] = useState(false);
  const [confirming, setConfirming] = useState(false);
  const [verifying, setVerifying] = useState(false);

  const [createSuccess, setCreateSuccess] = useState(false);
  const [createError, setCreateError] = useState(false);
  const [sec, setSec] = useState(5);
  const [redirect, setRedirect] = useState(false);

  useEffect(() => {
    if (createSuccess && sec > 0) {
      const timer = setTimeout(() => setSec(sec - 1), 1000);
      return () => clearTimeout(timer);
    } else if (sec === 0) {
      setRedirect(true);
    }
  }, [createSuccess, sec]);

  function getUser() {
    setFetchError({ active: false });

    if (email.length === 0) {
      setEmailError({ active: true, message: 'Email cannot be blank' });
      return;
    } else {
      setEmailError({ active: false });
    }

    setConfirming(true);

    axios
      .get(`http://localhost:5000/api/${type.toLowerCase()}s`, {
        params: { email: email },
      })
      .then((res) => {
        setConfirming(false);
        if (!res.data.password) {
          setFetchError({
            active: true,
            message: `Password not created for ${email}.`,
          });
        } else {
          setUser(res.data);
        }
      })
      .catch((err) => {
        setConfirming(false);
        if (err.response && err.response.status === 404) {
          setFetchError({ active: true, message: `${type} not found` });
        } else {
          setFetchError({
            active: true,
            message: 'An error occured. Please try again',
          });
        }
      });
  }

  function toReset() {
    setRecoveryError({ active: false });

    if (recoveryAnswer.length === 0) {
      setRecoveryAnswerError({
        active: true,
        message: 'Answer cannot be blank',
      });
      return;
    } else {
      setRecoveryAnswerError({ active: false });
    }

    setVerifying(true);

    axios
      .post(`http://localhost:5000/auth/verify-recovery/${user.id}`, {
        answer: recoveryAnswer,
      })
      .then((res) => {
        setVerifying(false);
        if (res.data.verified) {
          setVerified(true);
        } else {
          setRecoveryAnswerError({
            active: true,
            message: 'Incorrect answer. Try again',
          });
        }
      })
      .catch((err) => {
        setVerifying(false);
        setRecoveryError({
          active: true,
          message: 'An error occured. Please try again',
        });
      });
  }

  function resetPassword(e) {
    e.preventDefault();
    setCreateError({ active: false });

    if (password.length === 0) {
      setPasswordError({ active: true, message: 'Password cannot be blank' });
      return;
    } else {
      setPasswordError({ active: false });
    }

    if (verify !== password) {
      setVerifyError({ active: true, message: 'Passwords do not match' });
      return;
    } else {
      setVerifyError({ active: false });
    }

    setCreating(true);

    axios
      .put(`http://localhost:5000/api/${type.toLowerCase()}s/${user.id}`, {
        password: password,
      })
      .then((res) => {
        setCreating(false);
        setCreateSuccess(true);
      })
      .catch((err) => {
        setCreating(false);
        setCreateError({
          active: true,
          message: 'An error occured. Please try again',
        });
      });
  }

  return redirect ? (
    <Navigate to='/login' />
  ) : Object.keys(user).length === 0 ? (
    <Form className='create reset'>
      {fetchError.active && (
        <p style={{ color: 'red', textAlign: 'center', fontSize: '0.8rem' }}>
          {fetchError.message}
        </p>
      )}
      <p>Enter email to proceed</p>
      <Input
        type='email'
        name='email'
        placeholder='Enter email address'
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
      {confirming ? (
        <Button className='disabled' disabled>
          Confirming...
          <RotatingLines
            strokeColor='white'
            strokeWidth='5'
            animationDuration='0.75'
            width='17'
            visible={true}
          />
        </Button>
      ) : (
        <Button disabled={error} onClick={getUser}>
          Confirm
        </Button>
      )}
    </Form>
  ) : verified ? (
    <Form onSubmit={resetPassword} className='create reset'>
      {createSuccess && (
        <p style={{ color: 'green', textAlign: 'center', fontSize: '1rem' }}>
          Password reset successful. Redirecting to login in {sec} seconds.
        </p>
      )}
      {createError.active && (
        <p style={{ color: 'red', textAlign: 'center', fontSize: '0.8rem' }}>
          {createError.message}
        </p>
      )}
      <p>Create a new password</p>
      <Input
        type='password'
        name='password'
        placeholder='Create a password'
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        error={passwordError}
      />
      <br />
      <Input
        type='password'
        name='verify'
        placeholder='Verify password'
        value={verify}
        onChange={(e) => setVerify(e.target.value)}
        error={verifyError}
      />
      <br />
      {creating ? (
        <Button className='disabled' disabled>
          Resetting password...
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
          value='Create password'
          error={{ active: false }}
          disabled={error}
          id={error ? 'disabled' : ''}
        />
      )}
    </Form>
  ) : (
    <Form className='create reset'>
      {recoveryError.active && (
        <p style={{ color: 'red', textAlign: 'center', fontSize: '0.8rem' }}>
          {recoveryError.message}
        </p>
      )}
      <h3>Answer the recovery question to proceed to password reset</h3>
      <p>
        <span>Question:</span>
        {user.recovery_question}
      </p>
      <Input
        type='text'
        name='answer'
        placeholder='Enter answer'
        value={recoveryAnswer}
        onChange={(e) => setRecoveryAnswer(e.target.value)}
        error={recoveryAnswerError}
      />
      <br />
      {verifying ? (
        <Button className='disabled' disabled>
          Checking answer...
          <RotatingLines
            strokeColor='white'
            strokeWidth='5'
            animationDuration='0.75'
            width='17'
            visible={true}
          />
        </Button>
      ) : (
        <Button onClick={toReset}>Verify</Button>
      )}
    </Form>
  );
}

export default RecoverPassword;
