import logo from './logo.svg';
//import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useState } from 'react';
import './App.css';
import { io } from 'socket.io-client';
import OtpSearch from './pages/OtpSearch';
import AdminNavbar from './components/AdminNavbar';
import Home from './pages/Home';
import Notifications from './pages/Notifications';
import GenerateOtp from './pages/GenerateOtp';
import AppNavbar from './components/AppNavbar';
import GuestHome from './pages/GuestHome';
import SignUp from './components/SignUp';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

function App() {
  const [admin, setAdmin] = useState(true);


  //Establish socketio connection to the server
  var socket = io('http://localhost:5000', {
    transports: ['polling']
});


  socket.on('otp_notification', (data) => {
    console.log("Data:", data);
  
  })
  return (
    <Router>
      {admin ? <AdminNavbar /> : <AppNavbar />}
      <div>
        {admin ?
          <Routes>
            <Route path='/admin' element={<Home />} />
            <Route path='/admin/notifications/all' element={<Notifications />} />
            <Route path='/admin/search' element={<OtpSearch />} />
            <Route path='/admin/generateotp' element={<GenerateOtp />} />
            <Route path='/admin/signup' element={<SignUp />} />
          </Routes>
          :
          <Routes>
            <Route path='/' element={<GuestHome />} />
        </Routes>
        }
      </div>
    </Router>
  );
}

export default App;
