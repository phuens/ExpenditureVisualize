import 'date-fns';
import React, { useState } from 'react';
import { makeStyles, Grid, Button } from '@material-ui/core';
import DateFnsUtils from '@date-io/date-fns';
import { MuiPickersUtilsProvider, KeyboardDatePicker } from '@material-ui/pickers';
import { Alert, AlertTitle } from '@material-ui/lab';

const useStyles = makeStyles(() => ({
  errorModal: {
    transition: '200ms ease-in all',
  },
}));
export default function MaterialUIPickers(props) {
  const classes = useStyles();
  const [selectedFromDate, setSelectedFromDate] = useState(new Date());
  const [selectedToDate, setSelectedToDate] = useState(new Date());
  const [alertShow, setAlertShow] = useState(false);

  // handle from date change
  const handleFromDateChange = (date) => {
    setSelectedFromDate(date);
  };
  // handle to date change
  const handleToDateChange = (date) => {
    setSelectedToDate(date);
  };

  const submitDates = () => {
    console.log('from date is after to date: ', selectedFromDate > selectedToDate);
    const dateValidate = selectedFromDate < selectedToDate;
    // eslint-disable-next-line no-unused-expressions
    dateValidate ? props.passDates([selectedFromDate, selectedToDate]) : setAlertShow(!alertShow);
    event.preventDefault();
  };
  return (
    <>
      <MuiPickersUtilsProvider utils={DateFnsUtils}>
        <Grid container>
          {/* ------- alert button ------- */}
          {alertShow ? (
            <Grid
              item
              xs={12}
              lg={12}
              md={12}
              sm={12}
              align="center"
              className={classes.errorModal}
            >
              <Grid contianer>
                <Grid item xs={12} lg={4} md={6} sm={12} style={{ textAlign: 'left' }}>
                  <Alert severity="error">
                    <AlertTitle>Error</AlertTitle>
                    From Date cannot be after To Date
                    <br />
                    <Button
                      size="small"
                      variant="contained"
                      color="primary"
                      style={{ marginTop: '30px' }}
                      onClick={() => setAlertShow(!alertShow)}
                    >
                      close
                    </Button>
                  </Alert>
                </Grid>
              </Grid>
            </Grid>
          ) : undefined}
          {/* ------- end of alert button ------- */}
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
    </>
  );
}
