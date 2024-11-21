import logo from './logo.svg';
//import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import { io } from 'socket.io-client';
import OtpSearch from './pages/OtpSearch';
import AppNavbar from './components/Navbar';
import Home from './pages/Home';
import Notifications from './pages/Notifications';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

function App() {


  //Establish socketio connection to the server
  var socket = io('http://localhost:5000', {
    transports: ['polling']
});


  socket.on('otp_notification', (data) => {
    console.log("Data:", data);
  
  })
  return (
    <Router>
      <AppNavbar />
      <div>
        <Routes>
          <Route path='/' element={<Home />} />
          <Route path='/notifications/all' element={<Notifications />} />
          <Route path='/search' element={<OtpSearch />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
