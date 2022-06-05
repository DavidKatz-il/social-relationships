/*import React, { createContext, useEffect, useState } from "react";

export const InfoContext = createContext();

export const InfoProvider = (props) => {
    const [token,] = useContext(UserContext);
    const [pageTitle, setPageTitle] = useState("Page");
    const [pageInfo, setPageInfo] = useState("some info about the page");

    useEffect(() => {
        const fetchUser = async () => {
            const requestOptions = {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: "Bearer " + token,
                },
            };
            const response = await fetch("/api/users/user", requestOptions);
            if (!response.ok) setToken(null);
            localStorage.setItem("socialRelationshipsToken", token);
        };
        fetchUser();
    }, [token]);

    return <InfoContext.Provider value={[token, setToken]}>{props.children}</InfoContext.Provider>
};*/