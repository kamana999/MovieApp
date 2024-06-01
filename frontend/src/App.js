import './App.css';
import {BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import Login from './components/Login';
import MoviesList from './components/MoviesList';
import UploadCsv from './components/UploadCsv';
import NavBar from './components/NavBar';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container } from 'react-bootstrap';
import PrivateRoutes from './routes/ProtectedRoute';


const App = () => {
  const isLoggedIn = localStorage.getItem("token") ? true : false;
  return (
    <>
    <NavBar />
    <Container >
        <BrowserRouter>
        <Routes>
          <Route path="/" element={isLoggedIn ? <Navigate to="/movie_list" /> : <Navigate to="/login" />} />
            <Route path="/login" element={<Login />} />
            <Route element={<PrivateRoutes />}>
                <Route element={<MoviesList/>} path="/movie_list" exact/>
                <Route element={<UploadCsv/>} path="/upload"/>
            </Route>
        </Routes>
        </BrowserRouter>
      </Container>

    </>
  );
};

export default App;
