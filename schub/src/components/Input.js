import React from 'react';

function Input({ error, ...props }) {
  return (
    <>
      <input
        {...props}
        style={error.active ? { border: '2px solid red' } : {}}
      />
      {error.active && (
        <>
          <br />
          <p style={{ color: 'red', textAlign: 'center', fontSize: '0.8rem' }}>
            {error.message}
          </p>
        </>
      )}
    </>
  );
}

export default Input;
