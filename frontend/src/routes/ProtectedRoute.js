import React from "react";
import { Navigate, Outlet } from "react-router-dom";

const PrivateRoute = ({ isLoggedIn, ...rest }) => {
  isLoggedIn = localStorage.getItem("token") ? true : false;
  if (!isLoggedIn) {
    return <Navigate to="/login" />;
  }

  return <Outlet {...rest} />;
};

export default PrivateRoute;
