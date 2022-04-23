/*import React, { ReactElement, useState } from "react";
import { TabType } from "./MyTab";

export const MyTabs: React.FC<{ children: ReactElement[] }> = props => {
    const [selectedTab, setSelectedTab] = useState(0)

    return <>
        <div style={{ display: 'flex', gap: 1 }}>
            {props.children.map((item, i) => {
                var tt = item.props as TabType
                var bkclr = "Green"// tt.style?.backgroundColor || "var(--secondary)"
                var topmrg = selectedTab === i ? 0 : 4
                var bordrwdt = (selectedTab === i ? 5 : 1) + "px 1px " + (selectedTab == i ? 0 : 1) + "px 1px"

                return <div
                    onClick={() => setSelectedTab(i)}
                    style={{
                        flexGrow: 1,
                        backgroundColor: bkclr,
                        padding: 8,
                        fontWeight: 'bold',
                        cursor: 'pointer',
                        borderColor: "var(--primary)",
                        borderRadius: "10px 10px 0px 0px",
                        borderWidth: bordrwdt,
                        borderStyle: "solid",
                        marginTop: topmrg
                    }}>{tt.title}</div>
            }
            )}
        </div>
        <div className="divcontent" style={{
            padding: 5,
            borderColor: "var(--primary)",
            borderStyle: "solid",
            borderWidth: "0px 1px 1px 1px",
            height: "100%"
        }}>{props.children.map((x, i) => <div
            className="divcontentinternal"
            style={{ height: "100%", display: i == selectedTab ? "block" : "none" }}
        >{x}</div>)}
        </div>
    </>
}*/