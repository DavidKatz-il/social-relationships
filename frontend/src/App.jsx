import React, { useContext, useEffect, useState } from "react";
import Header from "./components/Header";
import { UserContext } from "./context/UserContext";
import { Views } from "./components/Views";
import { SignInUp } from "./components/User/SignInUp";

const App = () => {
  const [message, setMessage] = useState("");
  const [token] = useContext(UserContext);

  const getWelcomeMessage = async () => {
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    };
    const response = await fetch("/api", requestOptions);
    const data = await response.json();

    if (!response.ok) console.log("something messed up");
    else setMessage(data.message);
  };

  useEffect(() => { getWelcomeMessage(); }, []);

  return (
    <>
      <Header title={message} />
      <div className="columns">
        <div className="column"></div>
        <div className="column m-5 is-two-thirds"> {!token ? <SignInUp /> : <Views />} </div>
        <div className="column"></div>
      </div>
    </>
  );
};
export default App;