// Select inside an always-open Dialog (as in the issue's StackBlitz demo).
import * as React from 'react';
import { createRoot } from 'react-dom/client';
import { CssBaseline, Dialog, DialogContent, FormControl, InputLabel, Select, MenuItem } from '@mui/material';

function Demo() {
  const [age, setAge] = React.useState('10');
  return (
    <Dialog open>
      <DialogContent>
        <FormControl sx={{ minWidth: 150 }}>
          <InputLabel id="age-label">Age</InputLabel>
          <Select labelId="age-label" id="age-select" value={age} label="Age" onChange={(e) => setAge(e.target.value)}>
            {[10, 20, 30, 40, 50, 60, 70, 80, 90, 100].map((n) => (
              <MenuItem key={n} value={String(n)}>{n}</MenuItem>
            ))}
          </Select>
        </FormControl>
      </DialogContent>
    </Dialog>
  );
}

createRoot(document.getElementById('root')).render(<><CssBaseline /><Demo /></>);
