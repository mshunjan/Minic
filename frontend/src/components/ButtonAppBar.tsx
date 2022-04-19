import { AppBar, CardActionArea, Tooltip, Typography } from '@mui/material';
import StackedBarChartIcon from '@mui/icons-material/StackedBarChart';
export default function ButtonAppBar() {

  return (
    <Tooltip title='Go Home'>
      <AppBar position="static" onClick={() => window.location.reload()}>
        <CardActionArea>
          <Typography variant="h2" flexGrow={1}>
            <StackedBarChartIcon />
            MINIC
          </Typography>
        </CardActionArea>
      </AppBar>
    </Tooltip>
  );
}
