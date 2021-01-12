import "date-fns";
import React, { useState } from "react";
import Grid from "@material-ui/core/Grid";
import DateFnsUtils from "@date-io/date-fns";
import { MuiPickersUtilsProvider, KeyboardDatePicker } from "@material-ui/pickers";

export default function MaterialUIPickers() {
    // The first commit of Material-UI
    const [selectedFromDate, setSelectedFromDate] = useState(new Date());
    const [selectedToDate, setSelectedToDate] = useState(new Date());

    const handleFromDateChange = (date) => {
        setSelectedFromDate(date);
    };
    const handleToDateChange = (date) => {
        setSelectedToDate(date);
    };

    return (
        <MuiPickersUtilsProvider utils={DateFnsUtils}>
            <Grid container>
                <Grid item xs={3}>
                    <KeyboardDatePicker
                        disableToolbar
                        variant='inline'
                        format='MM/dd/yyyy'
                        margin='normal'
                        id='date-picker-inline'
                        label='From Date'
                        value={selectedFromDate}
                        onChange={handleFromDateChange}
                        KeyboardButtonProps={{
                            "aria-label": "change date",
                        }}
                    />
                </Grid>
                <Grid item xs={3}>
                    <KeyboardDatePicker
                        disableToolbar
                        variant='inline'
                        format='MM/dd/yyyy'
                        margin='normal'
                        id='date-picker-inline'
                        label='To Date'
                        value={selectedToDate}
                        onChange={handleToDateChange}
                        KeyboardButtonProps={{
                            "aria-label": "change date",
                        }}
                    />
                </Grid>
            </Grid>
        </MuiPickersUtilsProvider>
    );
}
