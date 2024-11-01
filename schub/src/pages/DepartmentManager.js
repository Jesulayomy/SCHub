import { useEffect, useState, useContext } from 'react';
import { Link, Navigate } from 'react-router-dom';
// import axios from 'axios';
import api from '../contexts/api';
import { AuthContext } from '../contexts/AuthContext';
import UpdateForm from '../components/UpdateForm';
import Input from '../components/Input';
import Button from '../components/Button';
import DisplayTable from '../components/DisplayTable';
import '../styles/manage.css';
import LoadingPage from '../components/Loading';

function DepartmentManager({ loading }) {
  // auth context values
  const { isLoggedIn, user } = useContext(AuthContext);

  const [allDepartments, setAllDepartments] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [nextPage, setNextPage] = useState(1);
  const [hasPages, setHasPages] = useState(false);

  const [updating, setUpdating] = useState(false);
  const [updateDepartment, setUpdateDepartment] = useState({
    id: '',
    name: '',
  });
  const [updateSucess, setUpdateSucess] = useState(false);

  const [searching, setSearching] = useState(false);
  const [searchingValue, setSearchingValue] = useState('');
  const [searchedValue, setSearchedValue] = useState('');

  useEffect(() => {
    // fetch all departments
    api
      .get('departments/', { withCredentials: true })
      .then((res) => {
        if (res.data.next) {
          setHasPages(true);
          setNextPage(nextPage + 1);
          console.log('Has more pages');
          console.log('Next page:', nextPage);
        }
        setAllDepartments(res.data.departments);
        setDepartments(res.data.departments);
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
    setDepartments(
      allDepartments.filter((department) => {
        return department.name
          .toLowerCase()
          .includes(searchingValue.toLowerCase());
      })
    );
    setSearchedValue(searchingValue);
  }

  function loadMore() {
    setHasPages(false);
    console.log('Loading more departments');
    console.log('Getting page:', nextPage);
    api
      .get(`departments/?page=${nextPage}`, { withCredentials: true })
      .then((res) => {
        setDepartments([...departments, ...res.data.departments]);
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

  function handleUpdate(id, name, department) {
    setUpdating(true);
    setUpdateDepartment({ id: id, name: name, department: department });
  }

  function showAll() {
    setDepartments(allDepartments);
    setSearching(false);
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
            type='department'
            name={updateDepartment.name}
            id={updateDepartment.id}
            setUpdating={setUpdating}
            setUpdate={setUpdateDepartment}
            setUpdateSucess={setUpdateSucess}
          />
        ) : (
          <>
            <h1>Departments</h1>
            <Link to='/admin-dashboard/departments/new'>
              Register New Department
            </Link>
            <div className='search'>
              <Input
                type='text'
                name='search'
                placeholder='Search department by name'
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
                <Button name='search-departments' onClick={handleSearch}>
                  Search
                </Button>
              )}
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
              type='department'
              data={departments}
              setData={setDepartments}
              allData={allDepartments}
              setAllData={setAllDepartments}
              handleUpdate={handleUpdate}
              searching={searching}
              searchedValue={searchedValue}
            />
            {/* {hasPages ? (
              <Button name='load-more' onClick={loadMore}>
                Load More
              </Button>
            ) : (
              <></>
            )} */}
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

export default DepartmentManager;
