import React from "react";
import Drawer from "../components/drawer/drawer";
import Graph from "../components/graph/graph";
import { makeStyles, Grid } from "@material-ui/core";

// NOTE: look into border-sizing: border-box if the elements are all moved to the right due to the padding that is being used.

const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
    },
    drawer: {
        display: "flex",
        flexDirection: "column",
        height: "100vh",
    },
    padding: {
        padding: "50px",
    },
}));
function Dashboard() {
    const classes = useStyles();
    return (
        <>
            <Grid container className={classes.root} spacing={0}>
                <Grid item xs={2} md={2} lg={2} sm={2} className={classes.drawer}>
                    <Drawer />
                </Grid>
                <Grid item xs={10} md={10} lg={10} sm={10} style={{ padding: "40px", background: "aliceblue" }}>
                    <Graph />
                </Grid>
            </Grid>
        </>
    );
}

export default Dashboard;
