import 'date-fns';
import React, { useState } from 'react';
import { Grid, Button } from '@material-ui/core';
import DateFnsUtils from '@date-io/date-fns';
import { MuiPickersUtilsProvider, KeyboardDatePicker } from '@material-ui/pickers';

export default function MaterialUIPickers(props) {
  // The first commit of Material-UI
  const [selectedFromDate, setSelectedFromDate] = useState(0);
  const [selectedToDate, setSelectedToDate] = useState(0);

  const handleFromDateChange = (date) => {
    console.log('this should technically be the from date: ', date);
    setSelectedFromDate(date);
  };
  const handleToDateChange = (date) => {
    console.log('this should technically be the TO date: ', date);
    setSelectedToDate(date);
  };
  const submitDates = () => {
    // eslint-disable-next-line react/prop-types
    props.passDates([selectedFromDate, selectedToDate]);
    // eslint-disable-next-line no-restricted-globals
    event.preventDefault();
  };
  return (
    <MuiPickersUtilsProvider utils={DateFnsUtils}>
      <Grid container>
        <Grid item xs={6} lg={3} md={3} sm={6}>
          <KeyboardDatePicker
            disableToolbar
            variant="inline"
            format="MM/dd/yyyy"
            margin="normal"
            id="date-picker-inline"
            label="From Date"
            value={selectedFromDate}
            onChange={handleFromDateChange}
            KeyboardButtonProps={{
              'aria-label': 'change date',
            }}
          />
        </Grid>
        <Grid item xs={6} lg={3} md={3} sm={6}>
          <KeyboardDatePicker
            disableToolbar
            variant="inline"
            format="MM/dd/yyyy"
            margin="normal"
            id="date-picker-inline"
            label="To Date"
            value={selectedToDate}
            onChange={handleToDateChange}
            KeyboardButtonProps={{
              'aria-label': 'change date',
            }}
          />
        </Grid>
        <Grid item xs={12} lg={3} md={3} sm={12} style={{ marginTop: '28px' }}>
          <Button variant="outlined" color="secondary" onClick={submitDates}>
            Submit
          </Button>
        </Grid>
      </Grid>
    </MuiPickersUtilsProvider>
  );
}
