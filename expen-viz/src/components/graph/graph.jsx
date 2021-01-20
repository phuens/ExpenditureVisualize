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
  let scatterbarDailySumAndAverage;
  let pieDaysExpenditurePieChart;
  let barDayBasedCategoricalExpenditure;
  let barCategoricalSumExpenditure;
  let pieCategoricalSumExpenditure;

  const [searchApi, results, errorMessage] = Data();
  console.log(results.length);
  console.log('error message>>>>> ', errorMessage);
  if (results.length === 5) {
    scatterbarDailySumAndAverage = results[0];
    pieDaysExpenditurePieChart = results[1];
    barDayBasedCategoricalExpenditure = results[2];
    barCategoricalSumExpenditure = results[3];
    pieCategoricalSumExpenditure = results[4];
  }

  // TODO: need to parse the date properly. the wrong date is being passed.
  const handleCallback = (childData) => {
    console.log('parsed in handle callback', childData);
    const fromDate = JSON.stringify(childData[0]).slice(1, 11);
    const toDate = JSON.stringify(childData[1]).slice(1, 11);
    console.log('date under the handle call back: ', fromDate, ' - ', toDate);
    searchApi(fromDate, toDate);
  };

  const classes = useStyles();
  const config = { responsive: true };
  // eslint-disable-next-line no-nested-ternary
  return results.length !== 0 ? (
    <Grid container className={classes.root} spacing={3}>
      <Grid item xs={11} md={11} lg={11} sm={11} style={{ margin: '60px 10px 10px 15px' }}>
        <DatePicker passDates={handleCallback} />
      </Grid>
      <Grid
        item
        xs={12}
        md={12}
        lg={11}
        sm={12}
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
        xs={12}
        md={12}
        lg={4}
        sm={12}
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
      <Grid
        item
        xs={12}
        md={12}
        lg={7}
        sm={12}
        className={classes.background}
        style={{ margin: '10px' }}
      >
        <Plot
          data={barDayBasedCategoricalExpenditure.data}
          layout={barDayBasedCategoricalExpenditure.layout}
          config={config}
          className={classes.width}
        />
      </Grid>
      <Grid
        item
        xs={12}
        md={12}
        lg={6}
        sm={12}
        className={classes.background}
        style={{ margin: '10px' }}
      >
        <Plot
          data={barCategoricalSumExpenditure.data}
          layout={barCategoricalSumExpenditure.layout}
          config={config}
          className={classes.width}
        />
      </Grid>
      <Grid
        item
        xs={12}
        md={12}
        lg={5}
        sm={12}
        className={classes.background}
        style={{ margin: '10px' }}
      >
        <Plot
          data={pieCategoricalSumExpenditure.data}
          layout={pieCategoricalSumExpenditure.layout}
          config={config}
          className={classes.width}
        />
      </Grid>
    </Grid>
  ) : (
    <Grid item xs={12} style={{ margin: '10px', textAlign: 'center' }}>
      <h3>LOADING</h3>
    </Grid>
  );
}

export default Graph;
