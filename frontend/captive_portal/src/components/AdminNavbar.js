import React from 'react';
import { Navbar, Nav, Container } from 'react-bootstrap';

const AdminNavbar = () => {
  return (
    <div >
      <Navbar bg='dark' variant='dark' expand='lg' sticky='top'>
        <Container>
          <Navbar.Brand href='/'>Techpoint</Navbar.Brand>
          <Navbar.Toggle aria-controls='basic-navbar-nav' />
          <Navbar.Collapse id='basic-navbar-nav'>
            <Nav className='me-auto'>
              <Nav.Link href='/admin'>Home</Nav.Link>
              <Nav.Link href='/admin/notifications/all'>Notifications</Nav.Link>
              <Nav.Link href='/admin/search'>Search</Nav.Link>
              <Nav.Link href='/admin/generateotp'>Generate OTP</Nav.Link>
              <Nav.Link href='/admin/signup'>Sign Up</Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </div>
  );
};

export default AdminNavbar;