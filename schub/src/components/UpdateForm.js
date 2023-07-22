import { useEffect, useState } from 'react';
import { RotatingLines } from 'react-loader-spinner';
import axios from 'axios';
import validator from 'validator';
import Form from './Form';
import Input from './Input';
import Button from './Button';
import '../styles/updateform.css';

function UpdateForm({
  type,
  name,
  id,
  department,
  setUpdating,
  setUpdate,
  setUpdateSucess,
}) {
  const [fName, setFName] = useState('');
  const [lName, setLName] = useState('');
  const [cName, setCName] = useState('');
  const [teachers, setTeachers] = useState([]);
  const [teacherId, setTeacherId] = useState('None');
  const [email, setEmail] = useState('');
  const [age, setAge] = useState('');

  // states for error handling
  const [error, setError] = useState(false);
  const [anyError, setAnyError] = useState({ active: false, message: 'true' });
  const [fNameError, setFNameError] = useState({ active: false });
  const [lNameError, setLNameError] = useState({ active: false });
  const [emailError, setEmailError] = useState({ active: false });
  const [teacherFetchError, setTeacherFetchError] = useState({ active: false });

  const [doingUpdate, setDoingUpdate] = useState(false);

  useEffect(() => {
    if (type === 'course') {
      axios
        .get('http://localhost:5000/api/teachers')
        .then((res) => {
          const allTeachers = res.data;
          setTeachers(
            allTeachers.filter((teacher) => teacher.department === department)
          );
        })
        .catch((err) => {
          setTeacherFetchError({
            active: true,
            message:
              'An error occured while fetching teacher details. Please try again',
          });
        });
    }
  }, [type, department]);

  function doUpdate(e) {
    e.preventDefault();
    const data = {};

    if (type === 'student') {
      if (
        fName.length === 0 &&
        lName.length === 0 &&
        email.length === 0 &&
        age.length === 0
      ) {
        setAnyError({ active: true, message: 'All fields cannot be blank' });
        return;
      } else {
        setAnyError({ active: false });
        if (fName) data.first_name = fName;
        if (lName) data.last_name = lName;
        if (email) data.email = email;
        if (age) data.age = age;
      }
    }

    if (type === 'teacher') {
      if (fName.length === 0 && lName.length === 0 && email.length === 0) {
        setAnyError({ active: true, message: 'All fields cannot be blank' });
        return;
      } else {
        setAnyError({ active: false });
        if (fName) data.first_name = fName;
        if (lName) data.last_name = lName;
        if (email) data.email = email;
      }
    }

    if (type === 'course') {
      if (cName.length === 0 && teacherId === 'None') {
        setAnyError({ active: true, message: 'All fields cannot be blank' });
        return;
      } else {
        setAnyError({ active: false });
        if (cName) data.name = cName;
        if (teacherId) data.teacher_id = teacherId;
      }
    }

    if (type === 'department') {
      if (cName.length === 0) {
        setAnyError({ active: true, message: 'Field cannot be blank' });
        return;
      } else {
        setAnyError({ active: false });
        data.name = cName;
      }
    }

    setDoingUpdate(true);

    axios
      .put(`http://localhost:5000/api/${type}s/${id}`, data, {
        withCredentials: true,
      })
      .then((res) => {
        setDoingUpdate(false);
        setUpdateSucess({ done: true, name: name });
        backFromUpdate();
      })
      .catch((err) => {
        setAnyError({
          active: true,
          message: 'An error occured. Please try again',
        });
      });
  }

  function backFromUpdate() {
    setUpdating(false);
    if (type === 'course') setUpdate({ id: '', name: '', department: '' });
    else setUpdate({ id: '', name: '' });
    setFName('');
    setLName('');
    setCName('');
    setTeacherId('');
    setEmail('');
    setAge('');
  }

  return (
    <Form className='update' onSubmit={doUpdate}>
      <h3>Updating {name}</h3>
      <p>Only fill the details you want to update</p>
      {anyError.active && (
        <p style={{ color: 'red', textAlign: 'center', fontSize: '0.8rem' }}>
          {anyError.message}
        </p>
      )}
      {(type === 'student' || type === 'teacher') && (
        <>
          <Input
            type='text'
            name='fName'
            placeholder='First name'
            value={fName}
            onChange={(e) => {
              setFName(e.target.value);
              if (!validator.isAlpha(fName)) {
                setError(true);
                setFNameError({
                  active: true,
                  message: 'First name must contain only letters',
                });
              } else {
                setError(false);
                setFNameError({ active: false });
              }
            }}
            error={fNameError}
          />
          <br />
          <Input
            type='text'
            name='lName'
            placeholder='Last name'
            value={lName}
            onChange={(e) => {
              setLName(e.target.value);
              if (!validator.isAlpha(lName)) {
                setError(true);
                setLNameError({
                  active: true,
                  message: 'Last name must contain only letters',
                });
              } else {
                setError(false);
                setLNameError({ active: false });
              }
            }}
            error={lNameError}
          />
          <br />
          <Input
            type='email'
            name='email'
            placeholder='Email address'
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
        </>
      )}
      {type === 'student' && (
        <>
          <Input
            type='number'
            name='age'
            placeholder='Enter age'
            value={age}
            onChange={(e) => setAge(e.target.value)}
            error={{ active: false }}
          />
          <br />
        </>
      )}
      {(type === 'course' || type === 'department') && (
        <>
          <Input
            type='text'
            name='cName'
            placeholder={`Enter ${type} name`}
            value={cName}
            onChange={(e) => setCName(e.target.value)}
            error={{ active: false }}
          />
          <br />
          {teacherFetchError.active && (
            <p
              style={{ color: 'red', textAlign: 'center', fontSize: '0.8rem' }}
            >
              {teacherFetchError.message}
            </p>
          )}
          {teachers.length !== 0 && (
            <>
              <p className='change'>Change Teacher</p>
              <select
                onChange={(e) => {
                  setTeacherId(
                    e.target.options[e.target.selectedIndex].getAttribute(
                      'name'
                    )
                  );
                }}
              >
                <option name='None'>None</option>
                {teachers.map((teacher) => (
                  <option key={teacher.id} name={teacher.id}>
                    {teacher.first_name + ' ' + teacher.last_name}
                  </option>
                ))}
              </select>
              <br />
            </>
          )}
        </>
      )}
      <Button name='back' onClick={backFromUpdate}>
        Go back
      </Button>
      {doingUpdate ? (
        <Button className='disabled' disabled>
          Updating...
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
          name='Update'
          value='Update'
          error={{ active: false }}
          disabled={error}
          id={error ? 'disabled' : ''}
        />
      )}
    </Form>
  );
}

export default UpdateForm;
