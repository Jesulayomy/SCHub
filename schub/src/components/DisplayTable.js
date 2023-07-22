import { useState } from 'react';
import { TailSpin } from 'react-loader-spinner';
import axios from 'axios';
import Button from './Button';
import '../styles/table.css';

function DisplayTable({
  type,
  data,
  setData,
  allData,
  setAllData,
  handleUpdate,
  searching,
  searchedValue,
}) {
  const [deleting, setDeleting] = useState(false);
  const [deleteId, setDeleteId] = useState('');

  function handleDelete(e) {
    setDeleting(true);
    setDeleteId(e.target.name);
  }

  function doDelete(e) {
    const id = deleteId;
    setAllData(allData.filter((dt) => dt.id !== id));
    if (type !== 'student') {
      setData(data.filter((dt) => dt.id !== id));
    }
    axios
      .delete(`http://localhost:5000/api/${type}s/${id}`, {
        withCredentials: true,
      })
      .then((res) => {
        // console.log(res.data);
      })
      .catch((err) => console.log('Error:', err));
    backFromDelete();
  }

  function backFromDelete() {
    setDeleting(false);
    setDeleteId('');
  }

  return data.length === 0 ? (
    <div className='loading'>
      {searching ? (
        <p>No results found for {searchedValue}</p>
      ) : (
        <>
          <TailSpin
            height='80'
            width='50'
            color='#4fa94d'
            ariaLabel='tail-spin-loading'
            radius='1'
            wrapperStyle={{}}
            wrapperClass=''
            visible={true}
          />
          <h4>Loading {type}s data</h4>
        </>
      )}
    </div>
  ) : (
    <div className='table-div'>
      <table>
        <thead>
          <tr>
            <th>
              {type === 'student' || type === 'teacher' ? 'Full Name' : 'Name'}
            </th>
            {type === 'student' && <th>Matric No</th>}
            {(type === 'student' || type === 'teacher') && <th>Email</th>}
            {type !== 'department' && <th>Department</th>}
            {(type === 'student' || type === 'course') && <th>Level</th>}
            {type === 'course' && <th>Teacher</th>}
            <th colSpan={2}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {data.map((dt) => {
            return (
              <tr key={dt.id}>
                <td>
                  {type === 'student' || type === 'teacher'
                    ? dt.first_name + ' ' + dt.last_name
                    : dt.name}
                </td>
                {type === 'student' && <td>{dt.matric_no}</td>}
                {(type === 'student' || type === 'teacher') && (
                  <td>{dt.email}</td>
                )}
                {type !== 'department' && <td>{dt.department}</td>}
                {type === 'student' && <td>{dt.current_level}</td>}
                {type === 'course' && <td>{dt.level}</td>}
                {type === 'course' && <td>{dt.teacher}</td>}
                <td>
                  <Button
                    name={dt.id}
                    onClick={() =>
                      handleUpdate(
                        dt.id,
                        type === 'student' || type === 'teacher'
                          ? `${dt.first_name} ${dt.last_name}`
                          : dt.name,
                        type === 'course' && dt.department
                      )
                    }
                    className='update'
                  >
                    Update
                  </Button>
                </td>
                <td>
                  {type !== 'department' &&
                    (deleting && deleteId === dt.id ? (
                      <div className='deleting'>
                        <p>
                          Confirm?
                        </p>
                        <Button
                          name='back'
                          onClick={backFromDelete}
                          className='back'
                        >
                          No&nbsp;
                        </Button>
                        <Button
                          name='delete'
                          onClick={doDelete}
                          className='delete'
                        >
                          Yes&nbsp;
                        </Button>
                      </div>
                    ) : (
                      <Button
                        name={dt.id}
                        onClick={handleDelete}
                        className='delete'
                      >
                        Delete
                      </Button>
                    ))}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export default DisplayTable;
