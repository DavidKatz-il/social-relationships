import React from "react";

export const ErrorMessage = ({ message }) => (
  <p className="has-text-weight-bold has-text-danger" style={{ textAlign: "center" }}>{message}</p>
);