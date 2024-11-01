import { useEffect, useState, useContext } from 'react';
import { Link, Navigate } from 'react-router-dom';
import axios from 'axios';
import api from '../contexts/api';
import { AuthContext } from '../contexts/AuthContext';
import UpdateForm from '../components/UpdateForm';
import Input from '../components/Input';
import Button from '../components/Button';
import DisplayTable from '../components/DisplayTable';
import '../styles/manage.css';
import LoadingPage from '../components/Loading';

function CourseManager({ loading }) {
  // auth context values
  const { isLoggedIn, user } = useContext(AuthContext);

  const [allCourses, setAllCourses] = useState([]);
  const [courses, setCourses] = useState([]);
  const [departments, setDepartments] = useState([]);

  const [filteringLevel, setFilteringLevel] = useState({
    active: false,
    value: '',
  });
  const [filteringDepartment, setFilteringDepartment] = useState({
    active: false,
    value: '',
  });

  const [updating, setUpdating] = useState(false);
  const [updateCourse, setUpdateCourse] = useState({
    id: '',
    name: '',
    department: '',
  });
  const [nextPage, setNextPage] = useState(1);
  const [hasPages, setHasPages] = useState(false);
  const [updateSucess, setUpdateSucess] = useState(false);

  const [searching, setSearching] = useState(false);
  const [searchingValue, setSearchingValue] = useState('');
  const [searchedValue, setSearchedValue] = useState('');

  useEffect(() => {
    // fetch all courses
    api
      .get('courses/', { withCredentials: true })
      .then((res) => {
        if (res.data.next) {
          setHasPages(true);
          setNextPage(nextPage + 1);
          console.log('Has more pages');
          console.log('Next page:', nextPage);
        }
        setAllCourses(res.data.courses);
        setCourses(res.data.courses);
      })
      .catch((err) => {
        console.log('Error:', err);
      });

    // fetch all departments
    api
      .get('departments/', { withCredentials: true })
      .then((res) => {
        setDepartments(res.data.departments);
      })
      .catch((err) => {
        console.log('Error:', err);
      });
  }, []);

  function loadMore() {
    setHasPages(false);
    console.log('Loading more courses');
    console.log('Getting page:', nextPage);
    api
      .get(`courses/?page=${nextPage}`, { withCredentials: true })
      .then((res) => {
        setCourses([...courses, ...res.data.courses]);
        if (res.data.next) {
          setNextPage(nextPage + 1);
          setHasPages(true);
          console.log('Has more pages');
          console.log('Next page:', nextPage);
        }
      })
      .catch((err) => {
        console.log('Error:', err);
      });
  }

  useEffect(() => {
    if (hasPages) {
      loadMore();
    }
  }, [hasPages]);

  function handleSearch() {
    if (searchingValue.length === 0) {
      return;
    }
    setSearching(true);
    setCourses(
      allCourses.filter((course) => {
        return course.name.toLowerCase().includes(searchingValue.toLowerCase());
      })
    );
    setSearchedValue(searchingValue);
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
          setCourses(
            allCourses.filter(
              (course) => course.department === filteringDepartment.value
            )
          );
          setFilteringLevel({ active: false, value: '' });
          return;
        }
        setCourses(
          allCourses.filter(
            (course) =>
              // course.level === value &&
              course.department === filteringDepartment.value
          )
        );
      } else {
        if (value === 'By Level') {
          showAll();
          return;
        }
        setCourses(allCourses.filter((course) => course.level === value));
      }
      setFilteringLevel({ active: true, value: value });
    } else {
      if (filteringLevel.active) {
        if (value === 'By Department') {
          setCourses(
            allCourses.filter((course) => course.level === filteringLevel.value)
          );
          setFilteringDepartment({ active: false, value: '' });
          return;
        }
        setCourses(
          allCourses.filter(
            (course) =>
              course.department === value // &&
              // course.level === filteringLevel.value
          )
        );
      } else {
        if (value === 'By Department') {
          showAll();
          return;
        }
        setCourses(allCourses.filter((course) => course.department === value));
      }
      setFilteringDepartment({ active: true, value: value });
    }
  }

  function handleUpdate(id, name, department) {
    setUpdating(true);
    setUpdateCourse({ id: id, name: name, department: department });
  }

  function showAll() {
    setCourses(allCourses);
    setSearching(false);
    setFilteringLevel({ active: false, value: '' });
    setFilteringDepartment({ active: false, value: '' });
    setSearchedValue('');
    setSearchingValue('');
  }

  return loading ? (
    <LoadingPage />
  ) : isLoggedIn ? (
    // user.type === 'Admin' ? (
      <section className='manage'>
        {updating ? (
          <UpdateForm
            type='course'
            name={updateCourse.name}
            id={updateCourse.id}
            department={updateCourse.department}
            setUpdating={setUpdating}
            setUpdate={setUpdateCourse}
            setUpdateSucess={setUpdateSucess}
          />
        ) : (
          <>
            <h1>Courses</h1>
            <Link to='/admin-dashboard/courses/new'>Register New Course</Link>
            <div className='search'>
              <Input
                type='text'
                name='search'
                placeholder='Search course by name'
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
                <Button name='search-courses' onClick={handleSearch}>
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
              type='course'
              data={courses}
              replaceData={departments}
              setData={setCourses}
              allData={allCourses}
              setAllData={setAllCourses}
              handleUpdate={handleUpdate}
              searching={searching}
              searchedValue={searchedValue}
            />
          </>
        )}
      </section>
    // ) : (
    //   // user.type.toLowerCase()
    //   <Navigate replace to={`/${"admin"}-dashboard`} />
    // )
  ) : (
    <Navigate replace to='/login' />
  );
}

export default CourseManager;
