import React from "react";

const ErrorMessage = ({ message }) => (
  <p className="has-text-weight-bold has-text-danger" style={{ textAlign: "center" }}>{message}</p>
);
export default ErrorMessage;