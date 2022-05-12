/*import React, { useState } from "react";
import { ImagesTable } from "./Image/ImagesTable";
import { StudentsTable } from "./Student/StudentsTable";
import { ReportsTable } from "./Report/ReportsTable";

export const Views = () => {
    const [selectedTab, setSelectedTab] = useState(0);

    return <>
        <div className="tabs is-centered is-large is-toggle is-toggle-rounded is-fullwidth">
            <ul>
                <li onClick={() => setSelectedTab(0)}
                    className={selectedTab === 0 ? "is-active" : ""}><a>Students</a></li>
                <li onClick={() => setSelectedTab(1)}
                    className={selectedTab === 1 ? "is-active" : ""}><a>Images</a></li>
                <li onClick={() => setSelectedTab(2)}
                    className={selectedTab === 2 ? "is-active" : ""}><a>Reports</a></li>
                {/*<li onClick={() => setSelectedTab(3)}
                    className={selectedTab === 3 ? "is-active" : ""}><a>Documents</a></li>*}
            </ul>
        </div >
        <div>{selectedTab === 0 ? <StudentsTable /> : <></>}</div>
        <div>{selectedTab === 1 ? <ImagesTable /> : <></>}</div>
        <div>{selectedTab === 2 ? <ReportsTable /> : <></>}</div>
        {/*<div>{selectedTab === 3 ? <Login /> : <></>}</div>*}
    </>
}*/