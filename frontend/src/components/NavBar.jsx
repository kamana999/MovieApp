import { Button, Nav, Navbar } from "react-bootstrap";

const Logout = () => {
  const logout = () => {
    localStorage.removeItem("token");
    window.location.reload();
  };
  return (
    <Button variant="danger" onClick={logout}>
      Logout
    </Button>
  );
};

const NavBar = ({ isLoggedIn }) => {
  isLoggedIn = localStorage.getItem("token") ? true : false;
  return (
    <>
      <Navbar bg="dark" variant="dark" expand="sm" className="mb-3">
        <Nav className="justify-content-end">
          <Nav.Link href="/movie_list">Movie List</Nav.Link>
          <Nav.Link href="/upload">Upload Csv</Nav.Link>
          {isLoggedIn && <Logout/>}
        </Nav>
      </Navbar>
    </>
  );
};

export default NavBar;
