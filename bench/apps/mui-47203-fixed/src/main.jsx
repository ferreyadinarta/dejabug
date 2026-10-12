// The "Checkboxes" Autocomplete demo from the MUI docs, standalone.
import { createRoot } from 'react-dom/client';
import { ThemeProvider, createTheme, CssBaseline, Box } from '@mui/material';
import Checkbox from '@mui/material/Checkbox';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import CheckBoxOutlineBlankIcon from '@mui/icons-material/CheckBoxOutlineBlank';
import CheckBoxIcon from '@mui/icons-material/CheckBox';

const films = ['The Shawshank Redemption', 'The Godfather', 'The Godfather: Part II', 'The Dark Knight',
  '12 Angry Men', "Schindler's List", 'Pulp Fiction', 'The Lord of the Rings: The Return of the King',
  'The Good, the Bad and the Ugly', 'Fight Club', 'The Lord of the Rings: The Fellowship of the Ring',
  'Star Wars: Episode V - The Empire Strikes Back', 'Forrest Gump', 'Inception',
  'The Lord of the Rings: The Two Towers', "One Flew Over the Cuckoo's Nest", 'Goodfellas', 'The Matrix',
  'Seven Samurai', 'Star Wars: Episode IV - A New Hope', 'City of God', 'Se7en', 'The Silence of the Lambs',
  "It's a Wonderful Life", 'Life Is Beautiful', 'The Usual Suspects', 'Léon: The Professional',
  'Spirited Away', 'Saving Private Ryan', 'Once Upon a Time in the West'].map((title) => ({ title }));

function App() {
  return (
    <Box sx={{ p: 4 }}>
      <Autocomplete
        multiple
        id="checkboxes-tags-demo"
        options={films}
        disableCloseOnSelect
        getOptionLabel={(o) => o.title}
        renderOption={(props, option, { selected }) => {
          const { key, ...rest } = props;
          return (
            <li key={key} {...rest}>
              <Checkbox icon={<CheckBoxOutlineBlankIcon fontSize="small" />}
                checkedIcon={<CheckBoxIcon fontSize="small" />} style={{ marginRight: 8 }} checked={selected} />
              {option.title}
            </li>
          );
        }}
        style={{ width: 500 }}
        renderInput={(params) => <TextField {...params} label="Checkboxes" placeholder="Favorites" />}
      />
    </Box>
  );
}

createRoot(document.getElementById('root')).render(
  <ThemeProvider theme={createTheme({ palette: { mode: 'dark' } })}><CssBaseline /><App /></ThemeProvider>,
);
