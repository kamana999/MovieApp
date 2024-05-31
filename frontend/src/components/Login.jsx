import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import { Button, Card, CardBody, CardHeader, Form } from "react-bootstrap";
import apiCall from "../utils/fetch";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const [error, setError] = useState("");

  const handleLogin = async () => {
    try {
      const options = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      };
      let data = await apiCall("/api/user/login", options);
      console.log(data);
      if (data.token) {
        localStorage.setItem("token", data.token);
        navigate("/movie_list", { replace: true });
        window.location.reload();
      } else {
        setError(data.message);
      }
    } catch (error) {
      console.error(error);
      setError(error.message);
    }
  };

  return (
    <>
      <Card style={{ width: "30%", margin: "auto", marginTop: "10%" }}>
        <CardHeader>Login Here </CardHeader>
        <CardBody>
          <Form>
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>Enter Your User Name</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicPassword">
              <Form.Label>Password</Form.Label>
              <Form.Control
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </Form.Group>
            <Button variant="primary" onClick={handleLogin}>
              Login
            </Button>
          </Form>
          {error && <div>{error}</div>}
        </CardBody>
      </Card>
    </>
  );
};

export default Login;

// http://localhost:5000/api/user/login 
// http://localhost:5000/api/csv/list 