import { useEffect, useState, useContext } from 'react';
import { Link, Navigate } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../contexts/AuthContext';
import UpdateForm from '../components/UpdateForm';
import Input from '../components/Input';
import Button from '../components/Button';
import DisplayTable from '../components/DisplayTable';
import '../styles/manage.css';
import LoadingPage from '../components/Loading';

function TeacherManager({ loading }) {
  // auth context values
  const { isLoggedIn, user } = useContext(AuthContext);

  const [allTeachers, setAllTeachers] = useState([]);
  const [teachers, setTeachers] = useState([]);
  const [departments, setDepartments] = useState([]);

  const [updating, setUpdating] = useState(false);
  const [updateTeacher, setUpdateTeacher] = useState({ id: '', name: '' });
  const [updateSucess, setUpdateSucess] = useState(false);

  const [searching, setSearching] = useState(false);
  const [searchingValue, setSearchingValue] = useState('');
  const [searchedValue, setSearchedValue] = useState('');

  useEffect(() => {
    // fetch all teachers
    axios
      .get('http://localhost:5000/api/teachers', { withCredentials: true })
      .then((res) => {
        setAllTeachers(res.data);
        setTeachers(res.data);
      })
      .catch((err) => {
        console.log('Error:', err);
      });

    // fetch all departments
    axios
      .get('http://localhost:5000/api/departments', { withCredentials: true })
      .then((res) => {
        setDepartments(res.data);
      })
      .catch((err) => {
        console.log('Error:', err);
      });
  }, []);

  function handleSearch() {
    if (searchingValue.length === 0) {
      return;
    }
    setSearching(true);
    setTeachers(
      allTeachers.filter((teacher) => {
        const fullName = teacher.first_name + ' ' + teacher.last_name;
        return fullName.toLowerCase().includes(searchingValue.toLowerCase());
      })
    );
    setSearchedValue(searchingValue);
  }

  function handleFilter(e) {
    setSearching(false);
    setSearchedValue('');
    setSearchingValue('');

    const value = e.target.value;
    if (value === 'By Department') {
      showAll();
      return;
    }
    setTeachers(allTeachers.filter((teacher) => teacher.department === value));
  }

  function handleUpdate(id, name) {
    setUpdating(true);
    setUpdateTeacher({ id: id, name: name });
  }

  function showAll() {
    setTeachers(allTeachers);
    setSearching(false);
    setSearchedValue('');
    setSearchingValue('');
  }

  return loading ? (
    <LoadingPage />
  ) : isLoggedIn ? (
    user.type === 'Admin' ? (
      <section className='manage'>
        {updating ? (
          <UpdateForm
            type='teacher'
            name={updateTeacher.name}
            id={updateTeacher.id}
            setUpdating={setUpdating}
            setUpdate={setUpdateTeacher}
            setUpdateSucess={setUpdateSucess}
          />
        ) : (
          <>
            <h1>Teachers</h1>
            <Link to='/admin-dashboard/teachers/new'>Register New Teacher</Link>
            <div className='search'>
              <Input
                type='text'
                name='search'
                placeholder='Search teacher by name'
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
                <Button name='search-teachers' onClick={handleSearch}>
                  Search
                </Button>
              )}
            </div>
            <div className='filter'>
              <h3>Filter</h3>
              <div className='filters'>
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
              type='teacher'
              data={teachers}
              setData={setTeachers}
              allData={allTeachers}
              setAllData={setAllTeachers}
              handleUpdate={handleUpdate}
              searching={searching}
              searchedValue={searchedValue}
            />
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

export default TeacherManager;
