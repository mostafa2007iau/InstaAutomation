import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';

const App = () => {
    const isAuthenticated = !!localStorage.getItem('accessToken');

    return (
        <Router>
            <div className="App">
                <Routes>
                    <Route path="/login" element={<LoginPage />} />
                    <Route
                        path="/dashboard"
                        element={isAuthenticated ? <DashboardPage /> : <Navigate to="/login" />}
                    />
                    <Route
                        path="/"
                        element={<Navigate to={isAuthenticated ? "/dashboard" : "/login"} />}
                    />
                </Routes>
            </div>
        </Router>
    );
};

export default App;