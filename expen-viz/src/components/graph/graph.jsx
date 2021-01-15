/* eslint-disable prefer-destructuring */
import React from 'react';
import Plot from 'react-plotly.js';
import { makeStyles, Grid } from '@material-ui/core';
import Data from '../../hook/get_data';
import DatePicker from '../date_picker/date_picker';

const useStyles = makeStyles(() => ({
  root: {
    flex: 1,
  },
  width: {
    width: '100%',
  },

  background: {
    padding: '20px',
    width: '100%',
    // height: "20rem",
    boxShadow: '0 0 1rem 0 rgba(0, 0, 0, .2)',
    borderRadius: '20px',
    position: 'relative',
    background: '#fff',
    zIndex: 1,
    overflow: 'hidden',
    '&::before': {
      content: '',
      position: 'absolute',
      background: 'inherit',
      zIndex: '-1',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      boxShadow: 'inset 0 0 2000px rgba(255, 255, 255, .5)',
      filter: 'blur(10px)',
      margin: '-20px',
    },
  },
}));

function Graph() {
  const [results, errorMessage] = Data();
  let scatterbarDailySumAndAverage;
  let pieDaysExpenditurePieChart;
  let barDayBasedCategoricalExpenditure;
  let barCategoricalSumExpenditure;
  let pieCategoricalSumExpenditure;

  if (results.length !== 0) {
    // eslint-disable-next-line prefer-destructuring
    scatterbarDailySumAndAverage = results[0];
    pieDaysExpenditurePieChart = results[1];
    barDayBasedCategoricalExpenditure = results[2];
    barCategoricalSumExpenditure = results[3];
    pieCategoricalSumExpenditure = results[4];
  }

  const classes = useStyles();
  const config = { responsive: true };
  // eslint-disable-next-line no-nested-ternary
  return results.length !== 0 ? (
    <Grid container className={classes.root} spacing={3}>
      <Grid item xs={11} md={11} lg={11} sm={11} style={{ margin: '10px 10px 10px 15px' }}>
        <DatePicker />
      </Grid>
      <Grid
        item
        xs={11}
        md={11}
        lg={11}
        sm={11}
        className={classes.background}
        style={{ margin: '10px 10px 10px 15px' }}
      >
        <Plot
          data={scatterbarDailySumAndAverage.data}
          layout={scatterbarDailySumAndAverage.layout}
          config={config}
          className={classes.width}
        />
      </Grid>
      <Grid
        item
        xs={4}
        md={4}
        lg={4}
        sm={4}
        className={classes.background}
        style={{ margin: '10px' }}
      >
        <Plot
          data={pieDaysExpenditurePieChart.data}
          layout={pieDaysExpenditurePieChart.layout}
          config={config}
          className={classes.width}
        />
      </Grid>
      <Grid item xs={7} className={classes.background} style={{ margin: '10px' }}>
        <Plot
          data={barDayBasedCategoricalExpenditure.data}
          layout={barDayBasedCategoricalExpenditure.layout}
          config={config}
          className={classes.width}
        />
      </Grid>
      <Grid item xs={6} className={classes.background} style={{ margin: '10px' }}>
        <Plot
          data={barCategoricalSumExpenditure.data}
          layout={barCategoricalSumExpenditure.layout}
          config={config}
          className={classes.width}
        />
      </Grid>
      <Grid item xs={5} className={classes.background} style={{ margin: '10px' }}>
        <Plot
          data={pieCategoricalSumExpenditure.data}
          layout={pieCategoricalSumExpenditure.layout}
          config={config}
          className={classes.width}
        />
      </Grid>
    </Grid>
  ) : errorMessage !== 0 ? (
    <Grid item xs={12} style={{ margin: '10px' }}>
      <h3>
        There has been an issue. The error is:
        {errorMessage}
      </h3>
    </Grid>
  ) : (
    <Grid item xs={12} style={{ margin: '10px', textAlign: 'center' }}>
      <h3>LOADING</h3>
    </Grid>
  );
}

export default Graph;
