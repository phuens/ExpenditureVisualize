import React from "react";
import Drawer from "../components/drawer/drawer";
import Navbar from "../components/navbar/navbar";
import { makeStyles } from "@material-ui/core";

// NOTE: look into border-sizing: border-box if the elements are all moved to the right due to the padding that is being used.

const useStyles = makeStyles({
    appMain: {
        paddingLeft: "300px",
        width: "100%",
    },
});
function Dashboard() {
    const classes = useStyles();
    return (
        <>
            <Drawer />
            <div className={classes.appMain}>this is where the graphs content will be.</div>
        </>
    );
}

export default Dashboard;
