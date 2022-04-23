import React from "react";
import Register from "./Register";
import Login from "./Login";

export const SignInUp = () => {
    return <div className="columns">
        <Register /> <Login />
    </div>
}