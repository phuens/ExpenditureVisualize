import React, { useState } from "react";
import { makeStyles, Grid } from "@material-ui/core";
import Data from "../../hook/get_data";
import Plot from "react-plotly.js";

const useStyles = makeStyles((theme) => ({
    width: {
        width: "100%",
    },
    background: {
        padding: "20px",
        width: "100%",
        // height: "20rem",
        boxShadow: "0 0 1rem 0 rgba(0, 0, 0, .2)",
        borderRadius: "20px",
        position: "relative",
        zIndex: 1,
        background: "#FFF",
        overflow: "hidden",
        "&::before": {
            content: "",
            position: "absolute",
            background: "inherit",
            zIndex: "-1",
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            boxShadow: "inset 0 0 2000px rgba(255, 255, 255, .5)",
            filter: "blur(10px)",
            margin: "-20px",
        },
    },
}));

function Graph(props) {
    const [results, errorMessage] = Data();
    const classes = useStyles();
    return (
        <Grid container className={classes.background}>
            <Plot data={results.data} layout={results.layout} className={classes.width} />
        </Grid>
    );
}

export default Graph;
