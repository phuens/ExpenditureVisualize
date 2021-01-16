import React from 'react';
import { Grid, makeStyles } from '@material-ui/core';
import ListItem from '@material-ui/core/ListItem';
import ExpandLess from '@material-ui/icons/ExpandLess';
import ExpandMore from '@material-ui/icons/ExpandMore';
import ListItemText from '@material-ui/core/ListItemText';
import List from '@material-ui/core/List';
import Collapse from '@material-ui/core/Collapse';
import Divider from '@material-ui/core/Divider';
import SummaryData from '../../hook/get_summary';
import Portrait from '../../asset/images/phuntsho.png';

const useStyles = makeStyles((theme) => ({
  root: {
    width: '100%',
    maxWidth: 360,
    backgroundColor: theme.palette.background.paper,
  },
  nested: {
    paddingLeft: theme.spacing(4),
  },
}));

export default function Drawer() {
  const [results, errorMessage] = SummaryData();
  const [open, setOpen] = React.useState(true);
  const [openExp, setOpenExp] = React.useState(true);
  const classes = useStyles();
  const handleClick = () => {
    setOpen(!open);
  };
  const handleClickOpen = () => {
    setOpenExp(!openExp);
  };
  if (results.length === 0) {
    return errorMessage;
  }

  return (
    <Grid container spacing={2} style={{ marginTop: '50px' }}>
      <Grid item xs={12} md={12} lg={12} sm={12}>
        <Grid item xs={6} md={6} lg={6} sm={6} style={{ marginLeft: '70px', marginBottom: '50px' }}>
          <img src={Portrait} alt="self portrait" style={{ width: '100%', borderRadius: '50%' }} />
        </Grid>
      </Grid>

      <Grid item xs={12} md={12} lg={12} sm={12}>
        <ListItem button>
          <ListItemText>
            <b style={{ color: '#4050b5b8' }}>Total Expenditure:</b>
            <span style={{ float: 'right' }}>{results[0]}</span>
          </ListItemText>
        </ListItem>
        <Divider />

        <ListItem button>
          <ListItemText>
            <b style={{ color: '#4050b5b8' }}>Total Earning:</b>
            <span style={{ float: 'right' }}>{results[1]}</span>
          </ListItemText>
        </ListItem>
        <Divider />

        <ListItem button onClick={handleClick}>
          <ListItemText>
            <b style={{ color: '#4050b5b8' }}>Largest Expenditure</b>
          </ListItemText>
          {open ? <ExpandLess /> : <ExpandMore />}
        </ListItem>
        <Collapse in={open} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            <ListItem button className={classes.nested}>
              <ListItemText>
                <i>Amount: </i>
                <span style={{ float: 'right' }}>{results[2]}</span>
              </ListItemText>
            </ListItem>
          </List>
          {/* <List component="div" disablePadding>
            <ListItem button className={classes.nested}>
              <ListItemText>
                <i>Category:</i>
                {results[3]}
              </ListItemText>
            </ListItem>
          </List> */}
          <List component="div" disablePadding>
            <ListItem button className={classes.nested}>
              <ListItemText>
                <i>Item:</i>
                <span style={{ float: 'right' }}>{results[4]}</span>
              </ListItemText>
            </ListItem>
          </List>
        </Collapse>
        <Divider />

        <ListItem button onClick={handleClickOpen}>
          <ListItemText>
            <b style={{ color: '#4050b5b8' }}>Most Expensive Month Month</b>
          </ListItemText>
          {openExp ? <ExpandLess /> : <ExpandMore />}
        </ListItem>
        <Collapse in={openExp} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            <ListItem button className={classes.nested}>
              <ListItemText>
                <i>Month: </i>
                <span style={{ float: 'right' }}>{results[5]}</span>
              </ListItemText>
            </ListItem>
          </List>
          <List component="div" disablePadding>
            <ListItem button className={classes.nested}>
              <ListItemText>
                <i>Amount:</i>
                <span style={{ float: 'right' }}>{results[6]}</span>
              </ListItemText>
            </ListItem>
          </List>
        </Collapse>
      </Grid>
    </Grid>
  );
}
