import React, { useState, useEffect, useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { RotatingLines } from 'react-loader-spinner';
import axios from 'axios';
import validator from 'validator';
import Form from '../components/Form';
import Input from '../components/Input';
import Button from '../components/Button';
import { AuthContext } from '../contexts/AuthContext';
import '../styles/create.css';

function CreateNew({ type }) {
  const { isLoggedIn, user } = useContext(AuthContext);

  const [departments, setDepartments] = useState([]);
  const [fName, setFName] = useState('');
  const [lName, setLName] = useState('');
  const [name, setName] = useState('');
  const [teachers, setTeachers] = useState([]);
  const [teacherId, setTeacherId] = useState('None');
  const [email, setEmail] = useState('');
  const [age, setAge] = useState('');
  const [level, setLevel] = useState('None');
  const [matricNo, setMatricNo] = useState('');
  const [departmentId, setDepartmentId] = useState('None');

  const [creating, setCreating] = useState(false);

  // states for handling errors
  const [error, setError] = useState(false);
  const [postError, setPostError] = useState({ active: false });
  const [fNameError, setFNameError] = useState({ active: false });
  const [lNameError, setLNameError] = useState({ active: false });
  const [nameError, setNameError] = useState({ active: false });
  const [emailError, setEmailError] = useState({ active: false });
  const [ageError, setAgeError] = useState({ active: false });
  const [matricError, setMatricError] = useState({ active: false });
  const [levelError, setLevelError] = useState({ active: false });
  const [departmentError, setDepartmentError] = useState({ active: false });
  const [departmentFetchError, setDepartmentFetchError] = useState({
    active: false,
  });
  const [teacherError, setTeacherError] = useState({ active: false });
  const [teacherFetchError, setTeacherFetchError] = useState({
    active: false,
  });

  // success state
  const [createSuccess, setCreateSuccess] = useState(false);

  useEffect(() => {
    if (type !== 'department') {
      // fetch departments
      axios
        .get('http://localhost:5000/api/departments')
        .then((res) => {
          setDepartments(res.data);
        })
        .catch((err) => {
          setDepartmentFetchError({
            active: true,
            error:
              'An error occured while fetching department details, Please try again',
          });
        });
    }
  }, [type]);

  function createNew(e) {
    e.preventDefault();
    setPostError({ active: false });
    setCreateSuccess(false);

    const data = {};

    // Error checking for empty fields
    if (type === 'student' || type === 'teacher') {
      if (fName.length === 0) {
        setFNameError({ active: true, message: 'First name cannot be blank' });
        return;
      } else {
        setFNameError({ active: false });
        data.first_name = fName;
      }

      if (lName.length === 0) {
        setLNameError({ active: true, message: 'Last name cannot be blank' });
        return;
      } else {
        setLNameError({ active: false });
        data.last_name = lName;
      }

      if (email.length === 0) {
        setEmailError({ active: true, message: 'Email cannot be blank' });
        return;
      } else {
        setEmailError({ active: false });
        data.email = email;
      }
    }

    if (type === 'student') {
      if (age.length === 0) {
        setAgeError({ active: true, message: 'Age cannot be blank' });
        return;
      } else {
        setAgeError({ active: false });
        data.age = age;
      }

      if (matricNo.length === 0) {
        setMatricError({ active: true, message: 'Matric no cannot be blank' });
        return;
      } else {
        setMatricError({ active: false });
        data.matric_no = matricNo;
      }

      if (level === 'None') {
        setLevelError({ active: true, message: 'Please select a level' });
        return;
      } else {
        setLevelError({ active: false });
        data.start_level = level;
        data.current_level = level;
      }
    }

    if (type === 'course' || type === 'department') {
      if (name.length === 0) {
        setNameError({ active: true, message: 'Name cannot be blank' });
        return;
      } else {
        setNameError({ active: false });
        data.name = name;
      }
    }

    if (type !== 'department') {
      if (departmentId === 'None') {
        setDepartmentError({
          active: true,
          message: 'Please select a department',
        });
        return;
      } else {
        setDepartmentError({ active: false });
        data.department_id = departmentId;
      }
    }

    if (type === 'course') {
      if (teacherId === 'None') {
        setTeacherError({ active: true, message: 'Please select a teacher' });
        return;
      } else {
        setTeacherError({ active: false });
        data.teacher_id = teacherId;
      }

      if (level === 'None') {
        setLevelError({ active: true, message: 'Please select a level' });
        return;
      } else {
        setLevelError({ active: false });
        data.level = level;
      }
    }

    setCreating(true);

    axios
      .post(`http://localhost:5000/api/${type}s`, data, {
        withCredentials: true,
      })
      .then((res) => {
        setCreating(false);
        setCreateSuccess(true);
        clearForm();
      })
      .catch((err) => {
        setCreating(false);
        setPostError({
          active: true,
          message: 'An error occured. Please try again',
        });
      });
  }

  function clearForm() {
    setFName('');
    setLName('');
    setEmail('');
    setName('');
    setAge('');
    setLevel('None');
    setMatricNo('');
    setDepartmentId('None');
    setTeachers([]);
    setTeacherId('');
  }

  function handleDepartmentChange(e) {
    const id = e.target.options[e.target.selectedIndex].getAttribute('id');
    setDepartmentId(id);

    if (type === 'course') {
      // fetch teachers
      axios
        .get('http://localhost:5000/api/teachers')
        .then((res) => {
          const allTeachers = res.data;
          setTeachers(
            allTeachers.filter((teacher) => teacher.department_id === id)
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
  }

  return isLoggedIn ? (
    user.type === 'Admin' ? (
      <div>
        <Form onSubmit={createNew} className='create'>
          <h3>Register new {type}</h3>
          {postError.active && (
            <p
              style={{ color: 'red', textAlign: 'center', fontSize: '0.8rem' }}
            >
              {postError.message}
            </p>
          )}
          {createSuccess && (
            <p
              style={{ color: 'green', textAlign: 'center', fontSize: '1rem' }}
            >
              New {type} registered successfully.
            </p>
          )}
          {(type === 'student' || type === 'teacher') && (
            <>
              <Input
                type='text'
                name='fName'
                placeholder='Enter first name'
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
                placeholder='Enter last name'
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
                placeholder='Enter email'
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
          {(type === 'course' || type === 'department') && (
            <>
              <Input
                type='text'
                name='name'
                placeholder='Enter name'
                value={name}
                onChange={(e) => setName(e.target.value)}
                error={nameError}
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
                error={ageError}
              />
              <br />
              <Input
                type='text'
                name='matricNo'
                placeholder='Enter matric number'
                value={matricNo}
                onChange={(e) => setMatricNo(e.target.value)}
                error={matricError}
              />
              <br />
            </>
          )}
          {departmentFetchError.active && (
            <p
              style={{ color: 'red', textAlign: 'center', fontSize: '0.8rem' }}
            >
              {departmentFetchError.message}
            </p>
          )}
          {departments.length > 0 && (
            <>
              <p>Choose department:</p>
              <select onChange={handleDepartmentChange}>
                <option id='None'>None</option>
                {departments.map((department) => (
                  <option key={department.id} id={department.id}>
                    {department.name}
                  </option>
                ))}
              </select>
              {departmentError.active && (
                <>
                  <br />
                  <p
                    style={{
                      color: 'red',
                      textAlign: 'center',
                      fontSize: '0.8rem',
                    }}
                  >
                    {departmentError.message}
                  </p>
                </>
              )}
              <br />
            </>
          )}
          {(type === 'student' || type === 'course') && (
            <>
              <p>Level</p>
              <select value={level} onChange={(e) => setLevel(e.target.value)}>
                <option>None</option>
                <option>100</option>
                <option>200</option>
                <option>300</option>
                <option>400</option>
              </select>
              {levelError.active && (
                <>
                  <br />
                  <p
                    style={{
                      color: 'red',
                      textAlign: 'center',
                      fontSize: '0.8rem',
                    }}
                  >
                    {levelError.message}
                  </p>
                </>
              )}
              <br />
            </>
          )}
          {teacherFetchError.active && (
            <p
              style={{ color: 'red', textAlign: 'center', fontSize: '0.8rem' }}
            >
              {teacherFetchError.message}
            </p>
          )}
          {teachers.length !== 0 && (
            <>
              <p className='change'>Select Teacher</p>
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
              {teacherError.active && (
                <>
                  <br />
                  <p
                    style={{
                      color: 'red',
                      textAlign: 'center',
                      fontSize: '0.8rem',
                    }}
                  >
                    {teacherError.message}
                  </p>
                </>
              )}
              <br />
            </>
          )}
          {creating ? (
            <Button className='disabled' disabled>
              Creating {type}...
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
              name='create'
              value='Register'
              error={{ active: false }}
              disabled={error}
              id={error ? 'disabled' : ''}
            />
          )}
        </Form>
      </div>
    ) : (
      <Navigate replace to={`/${user.type.toLowerCase()}-dashboard`} />
    )
  ) : (
    <Navigate replace to='/login' />
  );
}

export default CreateNew;
