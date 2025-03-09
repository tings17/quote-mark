import { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { isAuthenticated } from './api'
import AuthForm from './components/auth/AuthForm'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import ProtectedRoute from './components/common/ProtectedRoute'
import Navbar from './components/common/Navbar'
import NewAnnotationPage from './pages/NewAnnotationPage'
import BookForm from './components/books/BookForm'
import AnnotationPage from './pages/AnnotationPage'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import BookPage from './pages/BookPage'
import AnnotationForm from './components/annotations/AnnotationForm'
import ScrollToTop from './components/common/ScrollToTop'


function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(isAuthenticated());

  useEffect(() => {
    const handleAuthChange = () => setIsLoggedIn(isAuthenticated)

    window.addEventListener("auth-change", handleAuthChange);

    return () => window.removeEventListener("auth-change", handleAuthChange);
  }, []);

  return (
    <BrowserRouter>
      {isLoggedIn && <Navbar />}
      <ScrollToTop />

      <div className='app-container'>
        <Routes>
          {/* Auth routes*/}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          {/* Protected routes */}
          <Route path="/books" element={
            <ProtectedRoute>
              <BookPage />
            </ProtectedRoute>
          } />

          <Route path="/books/new/" element={
            <ProtectedRoute>
              <BookForm />
            </ProtectedRoute>
          } />

          <Route path="/books/:bookId/new/" element={
            <ProtectedRoute>
              <NewAnnotationPage />
            </ProtectedRoute>
          } />

          <Route path="/books/:bookId/annotations/" element={
            <ProtectedRoute>
              <AnnotationPage />
            </ProtectedRoute>
          } />

          <Route path="/annotations/all/" element={
            <ProtectedRoute>
              <AnnotationPage />
            </ProtectedRoute>
          } />

          {/* Default route */}
          <Route
          path="/"
          element={<Navigate to={isLoggedIn ? "/books" : "/login"} replace />}
          />

          {/* Catch all for unknown routes */}
          <Route
          path="*"
          element={<Navigate to={isLoggedIn ? "/books" : "/login"} replace />}
          />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
