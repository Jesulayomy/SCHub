import React, { createContext, useState } from 'react';

const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  // State variables for authentication
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);

  // Handles user login
  const login = (userData) => {
    setIsLoggedIn(true);
    setUser(userData);
  };

  // Handles User Logout
  const logout = () => {
    setIsLoggedIn(false);
    setUser(null);
  };

  const authContextValue = {
    isLoggedIn,
    user,
    login,
    logout
  };

  return (
    // Provides Authentication to the child components (App)
    <AuthContext.Provider value={authContextValue}>
      {children}
    </AuthContext.Provider>
  );
};

export { AuthContext, AuthProvider };
