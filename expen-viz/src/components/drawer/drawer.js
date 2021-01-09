import React from "react";
import { makeStyles, withStyles } from "@material-ui/core";

const userStyles = makeStyles({
    drawer: {
        display: "flex",
        flexDirection: "column",
        position: "absolute",
        left: "0%",
        width: "300px",
        height: "100%",
        backgroundColor: "red",
    },
});
export default function Drawer() {
    const classes = userStyles();
    return <div className={classes.drawer}>sdkjhsfhshf</div>;
}

// ONE WAY OF PASSING THE STYLES
// const style = {
//     drawer: {
//         display: "flex",
//         flexDirection: "column",
//         position: "absolute",
//         left: "0%",
//         width: "300px",
//         height: "100%",
//         backgroundColor: "red",
//     },
// };

// const SideMenu = (props) => {
//     const { classes } = props;
//     return <div className={classes.drawer}>sdkjhsfhshf</div>;
// };

// export default withStyles(style)(SideMenu);
