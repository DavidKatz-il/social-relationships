import React, { useContext, useEffect, useState } from "react";
import { ErrorMessage } from "../Info/ErrorMessage";
import { UserContext } from "../../context/UserContext";
import * as g from "../../Global";
import { ReportModal } from "./ReportModal";

export const ReportsTable = () => {
    const [reports, setReports] = useState(null);
    const [activeTab, setActiveTab] = useState("");
    const [activeID, setActiveID] = useState(0);
    const [token] = useContext(UserContext);
    const [errorMessage, setErrorMessage] = useState("");
    const [loaded, setLoaded] = useState(false);

    async function handleCreate() {
        setLoaded(false);
        await g.fetchData("POST", "application/json", token, "reports", setErrorMessage,
            "Something went wrong. Couldn't create reports");
        getReportsData();
    }

    async function getReportsData() {
        setLoaded(false);
        await g.fetchData("GET", "application/json", token, "reports_info", setErrorMessage,
            "Something went wrong. Couldn't get reports", setReports);
        setLoaded(true);
    }

    useEffect(() => {
        if (!(reports && reports.length)) getReportsData();
    }, []);

    function setActiveReport(name, id) {
        setActiveID(id);
        setActiveTab(name);
    }

    return <>
        <aside className="menu" style={{ padding: 25, float: "right" }}>
            <ul className="menu-list">
                <li>
                    <button className="button is-fullwidth is-primary" onClick={handleCreate}>
                        <b>{(reports && reports.length) ? "Renew " : "Create "}Reports</b>
                    </button>
                </li>
            </ul>
            <p className="menu-label"><b>Reports</b></p>
            <ul className="menu-list">
                {reports && reports.map(r => {
                    return <li><a className={activeTab === r.name ? "is-active" : ""} onClick={() => setActiveReport(r.name, r.id)} >{r.name}</a></li>
                })}
            </ul>
        </aside>
        <section className="container">
            <br /><ErrorMessage message={errorMessage} /><br />
            {(loaded && reports.length && activeID > 0) ? <ReportModal ID={activeID} />

                :
                <>
                    {(loaded && reports.length) ?
                        <p style={{ textAlign: "center" }}><b>Select A Report</b></p>
                        :
                        <div>
                            <p style={{ textAlign: "center" }}><br />Loading your reports</p>
                            <progress className="progress is-small is-primary" max="100">99%</progress>
                        </div>}
                </>
            }
        </section>
    </>
}