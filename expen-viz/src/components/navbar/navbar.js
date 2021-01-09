import React from "react";
import { AppBar, Toolbar, Grid } from "@material-ui/core";
function navbar(props) {
    return (
        <AppBar position='static'>
            <Toolbar>
                <Grid container>{/* <Grid item sm={2} xs={4} styles={}></Grid>
                    <Grid item sm={2} xs={4}></Grid> */}</Grid>
            </Toolbar>
        </AppBar>
    );
}

export default navbar;
