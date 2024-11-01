import { useState, useEffect, useContext } from 'react';
import { Link, Navigate } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../contexts/AuthContext';
import UpdateForm from '../components/UpdateForm';
import DisplayTable from '../components/DisplayTable';
import Input from '../components/Input';
import Button from '../components/Button';
import LoadingPage from '../components/Loading';
import '../styles/manage.css';

function StudentManager({ loading }) {
  // auth context values
  const { isLoggedIn, user } = useContext(AuthContext);

  // states for initial students and department render
  const [allStudents, setAllStudents] = useState([]);
  const [students, setStudents] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [numberShown, setNumberShown] = useState(100);
  const [nextPage, setNextPage] = useState(1);

  // states for students search functionality
  const [searching, setSearching] = useState(false);
  const [searchingValue, setSearchingValue] = useState('');
  const [searchedValue, setSearchedValue] = useState('');

  // states for students filter functionality
  const [filteringLevel, setFilteringLevel] = useState({
    active: false,
    value: '',
  });
  const [filteringDepartment, setFilteringDepartment] = useState({
    active: false,
    value: '',
  });

  // states for student update functionality
  const [updating, setUpdating] = useState(false);
  const [updateStudent, setUpdateStudent] = useState({ id: '', name: '' });
  const [updateSucess, setUpdateSucess] = useState(false);

  useEffect(() => {
    // fetch all students
    axios
      .get('students/', { withCredentials: true })
      .then((res) => {
        setAllStudents(res.data.students);
      })
      .catch((err) => {
        console.log('Error:', err);
      });

    // fetch all departments
    axios
      .get('departments/', { withCredentials: true })
      .then((res) => {
        setDepartments(res.data.departments);
      })
      .catch((err) => {
        console.log('Error:', err);
      });
  }, []);

  useEffect(() => {
    // to only display the first 100 students on load
    if (allStudents.length > 0) {
      const filteredStudents = allStudents.filter((student, i) => i < 100);
      setStudents(filteredStudents);
    }
  }, [allStudents]);

  function viewMore() {
    setStudents(allStudents.filter((student, i) => i < 100 + numberShown));
    setNumberShown(numberShown + 100);
  }

  function handleFilter(e) {
    setSearching(false);
    setSearchedValue('');
    setSearchingValue('');

    let value;
    if (e.target.name === 'filter-level' && e.target.value !== 'By Level')
      value = Number(e.target.value);
    else value = e.target.value;

    if (e.target.name === 'filter-level') {
      if (filteringDepartment.active) {
        if (value === 'By Level') {
          setStudents(
            allStudents.filter(
              (student) => student.department === filteringDepartment.value
            )
          );
          setFilteringLevel({ active: false, value: '' });
          return;
        }
        setStudents(
          allStudents.filter(
            (student) =>
              student.current_level === value &&
              student.department === filteringDepartment.value
          )
        );
      } else {
        if (value === 'By Level') {
          showAll();
          return;
        }
        setStudents(
          allStudents.filter((student) => student.current_level === value)
        );
      }
      setFilteringLevel({ active: true, value: value });
    } else {
      if (filteringLevel.active) {
        if (value === 'By Department') {
          setStudents(
            allStudents.filter(
              (student) => student.current_level === filteringLevel.value
            )
          );
          setFilteringDepartment({ active: false, value: '' });
          return;
        }
        setStudents(
          allStudents.filter(
            (student) =>
              student.department === value &&
              student.current_level === filteringLevel.value
          )
        );
      } else {
        if (value === 'By Department') {
          showAll();
          return;
        }
        setStudents(
          allStudents.filter((student) => student.department === value)
        );
      }
      setFilteringDepartment({ active: true, value: value });
    }
  }

  function handleSearch() {
    setSearching(true);
    setStudents(
      allStudents.filter((student) => {
        const fullName = student.user.first_name + ' ' + student.user.last_name;
        return (
          fullName.toLowerCase().includes(searchingValue.toLowerCase()) ||
          student.matric_no.toLowerCase().includes(searchingValue.toLowerCase())
        );
      })
    );
    setSearchedValue(searchingValue);
  }

  function showAll() {
    setStudents(allStudents.filter((student, i) => i < 100));
    setNumberShown(100);
    setFilteringLevel({ active: false, value: '' });
    setFilteringDepartment({ active: false, value: '' });
    setSearching(false);
    setSearchedValue('');
    setSearchingValue('');
  }

  function handleUpdate(id, name) {
    setUpdating(true);
    setUpdateStudent({ id: id, name: name });
  }

  return loading ? (
    <LoadingPage />
  ) : isLoggedIn ? (
    user.type === 'Admin' ? (
      <section className='manage'>
        {updating ? (
          <UpdateForm
            type='student'
            name={updateStudent.name}
            id={updateStudent.id}
            setUpdating={setUpdating}
            setUpdate={setUpdateStudent}
            setUpdateSucess={setUpdateSucess}
          />
        ) : (
          <>
            <h1>Students</h1>
            <Link to='/admin-dashboard/students/new'>Register New Student</Link>
            <div className='search'>
              <Input
                type='text'
                name='search'
                placeholder='Search student by name or matric number'
                value={searchingValue}
                onChange={(e) => {
                  setSearchingValue(e.target.value);
                }}
                error={{ active: false }}
              />
              {searching ? (
                <Button
                  style={{
                    backgroundColor: 'red',
                    border: 'none',
                  }}
                  name='show'
                  onClick={showAll}
                >
                  Cancel
                </Button>
              ) : (
                <Button name='search-students' onClick={handleSearch}>
                  Search
                </Button>
              )}
            </div>
            <div className='filter'>
              <h3>Filter</h3>
              <div className='filters'>
                <div className='level'>
                  <select name='filter-level' onChange={handleFilter}>
                    <option>By Level</option>
                    <option>100</option>
                    <option>200</option>
                    <option>300</option>
                    <option>400</option>
                  </select>
                </div>
                <div className='department'>
                  <select name='filter-departments' onChange={handleFilter}>
                    <option>By Department</option>
                    {departments.map((department) => (
                      <option key={department.id}>{department.name}</option>
                    ))}
                  </select>
                </div>
              </div>
            </div>
            {searching && <p>Showing search results for {searchedValue}</p>}
            {updateSucess && (
              <p
                style={{
                  color: 'green',
                  textAlign: 'center',
                  fontSize: '1rem',
                }}
              >
                Updated {updateSucess.name}.
              </p>
            )}
            <DisplayTable
              type='student'
              data={students}
              allData={allStudents}
              setAllData={setAllStudents}
              handleUpdate={handleUpdate}
              searching={searching}
              searchedValue={searchedValue}
            />
            {students.length < allStudents.length &&
              !filteringDepartment.active &&
              !filteringLevel.active &&
              !searching && (
                <Button className='more' name='view' onClick={viewMore}>
                  View More
                </Button>
              )}
          </>
        )}
      </section>
    ) : (
      <Navigate replace to={`/${user.type.toLowerCase()}-dashboard`} />
    )
  ) : (
    <Navigate replace to='/login' />
  );
}

export default StudentManager;
