import React from 'react';
import ReactDOM from 'react-dom/client';
import { AuthProvider } from './contexts/AuthContext';
import App from './components/App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  // Wrapping the app with AuthProvider for authentication context 
  <React.StrictMode>
    <AuthProvider>
      <App />
    </AuthProvider>
  </React.StrictMode>
);
