import React, { createContext, useEffect, useState } from "react";
import * as g from "../Global";

export const UserContext = createContext();

export const UserProvider = (props) => {
  const [token, setToken] = useState(localStorage.getItem("socialRelationshipsToken"));

  useEffect(() => {
    const fetchUser = async () => {
      await g.fetchData("GET", "application/json", token, "user", undefined, "", undefined,
        () => localStorage.setItem("socialRelationshipsToken", token), undefined, setToken);
    };
    fetchUser();
  }, [token]);

  return <UserContext.Provider value={[token, setToken]}>{props.children}</UserContext.Provider>
};