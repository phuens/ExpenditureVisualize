import React from 'react';
import { Grid } from '@material-ui/core';
import Divider from '@material-ui/core/Divider';
import SummaryData from '../../hook/get_summary';
import Portrait from '../../asset/images/phuntsho.png';

export default function Drawer() {
  const [results, errorMessage] = SummaryData();
  if (results.length === 0) {
    return errorMessage;
  }
  return (
    <Grid container spacing={2}>
      <Grid item xs={12} md={12} lg={12} sm={12}>
        <img src={Portrait} alt="self portrait" style={{ width: '50%', borderRadius: '50%' }} />
      </Grid>
      <Grid item xs={11} md={11} lg={11} sm={11}>
        Total Expenditure:
        {results[0]}
        <Divider />
      </Grid>
      <Grid item xs={11} md={11} lg={11} sm={11}>
        Total Earning:
        {results[1]}
        <Divider />
      </Grid>
      <Grid item xs={11} md={11} lg={11} sm={11}>
        Largest Expenditure:
        <br />
        Amount:
        {results[2]}
      </Grid>
      <Grid item xs={11} md={11} lg={11} sm={11}>
        Category:
        {results[3]}
      </Grid>
      <Grid item xs={11} md={11} lg={11} sm={11}>
        Item:
        {results[4]}
        <Divider />
      </Grid>
      <Grid item xs={11} md={11} lg={11} sm={11}>
        Most Expensive Month Month:
        {results[5]}
        <br />
        Total Expenditure:
        {results[6]}
      </Grid>
    </Grid>
  );
}
