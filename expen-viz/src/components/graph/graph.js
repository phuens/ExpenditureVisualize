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
    let scatterbarDailySumAndAverage;
    let pieDaysExpenditurePieChart;
    let barDayBasedCategoricalExpenditure;
    let barCategoricalSumExpenditure;
    let pieCategoricalSumExpenditure;

    if (results.length !== 0) {
        scatterbarDailySumAndAverage = results[0];
        pieDaysExpenditurePieChart = results[1];
        barDayBasedCategoricalExpenditure = results[2];
        barCategoricalSumExpenditure = results[3];
        pieCategoricalSumExpenditure = results[4];
    }

    const classes = useStyles();
    return results.length !== 0 ? (
        <>
            <Grid container className={classes.background}>
                <Plot data={scatterbarDailySumAndAverage.data} layout={scatterbarDailySumAndAverage.layout} className={classes.width} />
            </Grid>
            <Grid container className={classes.background}>
                <Plot data={pieDaysExpenditurePieChart.data} layout={pieDaysExpenditurePieChart.layout} className={classes.width} />
            </Grid>
            <Grid container className={classes.background}>
                <Plot data={barDayBasedCategoricalExpenditure.data} layout={barDayBasedCategoricalExpenditure.layout} className={classes.width} />
            </Grid>
            <Grid container className={classes.background}>
                <Plot data={barCategoricalSumExpenditure.data} layout={barCategoricalSumExpenditure.layout} className={classes.width} />
            </Grid>
            <Grid container className={classes.background}>
                <Plot data={pieCategoricalSumExpenditure.data} layout={pieCategoricalSumExpenditure.layout} className={classes.width} />
            </Grid>
        </>
    ) : (
        "LOADING"
    );
}

export default Graph;
