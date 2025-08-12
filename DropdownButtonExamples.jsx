import { useState } from 'react';
import {
  Button,
  Menu,
  MenuItem,
  ButtonGroup,
  ClickAwayListener,
  Grow,
  Paper,
  Popper,
  MenuList,
  Box,
  Select,
  FormControl,
  InputLabel,
  Divider,
  Typography,
  Grid,
  IconButton,
  Tooltip,
  TextField,
  InputAdornment
} from '@mui/material';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

const DropdownButtonExamples = () => {
  // Example 1: Simple Split Button with Dropdown
  const [selectedOption1, setSelectedOption1] = useState(10);
  const options1 = [5, 10, 25, 50, 100];
  const [anchorEl1, setAnchorEl1] = useState(null);
  const open1 = Boolean(anchorEl1);

  const handleClick1 = (event) => {
    setAnchorEl1(event.currentTarget);
  };

  const handleClose1 = () => {
    setAnchorEl1(null);
  };

  const handleMenuItemClick1 = (option) => {
    setSelectedOption1(option);
    setAnchorEl1(null);
  };

  // Example 2: ButtonGroup with Dropdown
  const [selectedOption2, setSelectedOption2] = useState(10);
  const options2 = [5, 10, 25, 50, 100];
  const [open2, setOpen2] = useState(false);
  const anchorRef2 = useState(null)[0];

  const handleToggle2 = () => {
    setOpen2((prevOpen) => !prevOpen);
  };

  const handleClose2 = (event) => {
    if (anchorRef2 && anchorRef2.contains(event.target)) {
      return;
    }
    setOpen2(false);
  };

  const handleMenuItemClick2 = (option) => {
    setSelectedOption2(option);
    setOpen2(false);
  };

  // Example 3: Inline Select in Button
  const [selectedOption3, setSelectedOption3] = useState(10);
  const options3 = [5, 10, 25, 50, 100];

  const handleChange3 = (event) => {
    setSelectedOption3(event.target.value);
  };

  // Example 4: Button with Select in InputAdornment
  const [selectedOption4, setSelectedOption4] = useState(10);
  const options4 = [5, 10, 25, 50, 100];

  const handleChange4 = (event) => {
    setSelectedOption4(event.target.value);
  };

  // Example 5: Compact Dropdown Button
  const [selectedOption5, setSelectedOption5] = useState(10);
  const options5 = [5, 10, 25, 50, 100];
  const [anchorEl5, setAnchorEl5] = useState(null);
  const open5 = Boolean(anchorEl5);

  const handleClick5 = (event) => {
    setAnchorEl5(event.currentTarget);
  };

  const handleClose5 = () => {
    setAnchorEl5(null);
  };

  const handleMenuItemClick5 = (option) => {
    setSelectedOption5(option);
    setAnchorEl5(null);
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Button with Dropdown Examples
      </Typography>
      <Typography variant="subtitle1" gutterBottom>
        Different UI implementations for a button with dropdown functionality
      </Typography>

      <Grid container spacing={4} sx={{ mt: 2 }}>
        {/* Example 1: Simple Split Button with Dropdown */}
        <Grid item xs={12} md={6}>
          <Box sx={{ mb: 1 }}>
            <Typography variant="h6">1. Split Button with Dropdown</Typography>
            <Typography variant="body2" color="text.secondary">
              A button that shows the current selection with a dropdown arrow to change it
            </Typography>
          </Box>
          <Box sx={{ display: 'flex' }}>
            <Button
              variant="contained"
              sx={{ borderTopRightRadius: 0, borderBottomRightRadius: 0 }}
              onClick={() => console.log(`Getting ${selectedOption1} records`)}
            >
              Get {selectedOption1} records
            </Button>
            <Button
              variant="contained"
              size="small"
              sx={{
                borderTopLeftRadius: 0,
                borderBottomLeftRadius: 0,
                minWidth: '36px',
                ml: '-1px'
              }}
              onClick={handleClick1}
              aria-haspopup="true"
              aria-expanded={open1 ? 'true' : undefined}
            >
              <ArrowDropDownIcon />
            </Button>
            <Menu
              anchorEl={anchorEl1}
              open={open1}
              onClose={handleClose1}
            >
              {options1.map((option) => (
                <MenuItem
                  key={option}
                  selected={option === selectedOption1}
                  onClick={() => handleMenuItemClick1(option)}
                >
                  {option}
                </MenuItem>
              ))}
            </Menu>
          </Box>
        </Grid>

        {/* Example 2: ButtonGroup with Dropdown */}
        <Grid item xs={12} md={6}>
          <Box sx={{ mb: 1 }}>
            <Typography variant="h6">2. ButtonGroup with Dropdown</Typography>
            <Typography variant="body2" color="text.secondary">
              Using Material UI's ButtonGroup component with a dropdown
            </Typography>
          </Box>
          <ButtonGroup variant="contained">
            <Button onClick={() => console.log(`Getting ${selectedOption2} records`)}>
              Get {selectedOption2} records
            </Button>
            <Button
              size="small"
              onClick={handleToggle2}
              ref={anchorRef2}
              aria-expanded={open2 ? 'true' : undefined}
            >
              <KeyboardArrowDownIcon />
            </Button>
          </ButtonGroup>
          <Popper
            open={open2}
            anchorEl={anchorRef2}
            transition
            disablePortal
            style={{ zIndex: 1000 }}
          >
            {({ TransitionProps, placement }) => (
              <Grow
                {...TransitionProps}
                style={{
                  transformOrigin:
                    placement === 'bottom' ? 'center top' : 'center bottom',
                }}
              >
                <Paper>
                  <ClickAwayListener onClickAway={handleClose2}>
                    <MenuList autoFocusItem>
                      {options2.map((option) => (
                        <MenuItem
                          key={option}
                          selected={option === selectedOption2}
                          onClick={() => handleMenuItemClick2(option)}
                        >
                          {option}
                        </MenuItem>
                      ))}
                    </MenuList>
                  </ClickAwayListener>
                </Paper>
              </Grow>
            )}
          </Popper>
        </Grid>

        {/* Example 3: Inline Select in Button */}
        <Grid item xs={12} md={6}>
          <Box sx={{ mb: 1 }}>
            <Typography variant="h6">3. Inline Select in Button</Typography>
            <Typography variant="body2" color="text.secondary">
              A button with an embedded select component
            </Typography>
          </Box>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Button
              variant="contained"
              onClick={() => console.log(`Getting ${selectedOption3} records`)}
              sx={{ mr: 1 }}
            >
              Get
            </Button>
            <FormControl variant="outlined" size="small" sx={{ width: 80 }}>
              <Select
                value={selectedOption3}
                onChange={handleChange3}
                displayEmpty
                inputProps={{ 'aria-label': 'records count' }}
              >
                {options3.map((option) => (
                  <MenuItem key={option} value={option}>
                    {option}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <Typography sx={{ ml: 1 }}>records</Typography>
          </Box>
        </Grid>

        {/* Example 4: Button with Select in InputAdornment */}
        <Grid item xs={12} md={6}>
          <Box sx={{ mb: 1 }}>
            <Typography variant="h6">4. TextField with Button</Typography>
            <Typography variant="body2" color="text.secondary">
              A text field with select and button combination
            </Typography>
          </Box>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <TextField
              label="Records"
              variant="outlined"
              size="small"
              sx={{ width: 150 }}
              select
              value={selectedOption4}
              onChange={handleChange4}
              SelectProps={{
                native: false,
              }}
            >
              {options4.map((option) => (
                <MenuItem key={option} value={option}>
                  {option}
                </MenuItem>
              ))}
            </TextField>
            <Button
              variant="contained"
              sx={{ ml: 1 }}
              onClick={() => console.log(`Getting ${selectedOption4} records`)}
            >
              Get Records
            </Button>
          </Box>
        </Grid>

        {/* Example 5: Compact Dropdown Button */}
        <Grid item xs={12} md={6}>
          <Box sx={{ mb: 1 }}>
            <Typography variant="h6">5. Compact Dropdown Button</Typography>
            <Typography variant="body2" color="text.secondary">
              A single button that includes both action and dropdown
            </Typography>
          </Box>
          <Button
            variant="contained"
            onClick={() => console.log(`Getting ${selectedOption5} records`)}
            endIcon={
              <IconButton
                size="small"
                sx={{
                  p: 0,
                  color: 'inherit',
                  '&:hover': { bgcolor: 'transparent' }
                }}
                onClick={(e) => {
                  e.stopPropagation();
                  handleClick5(e);
                }}
              >
                <ExpandMoreIcon />
              </IconButton>
            }
          >
            Get {selectedOption5} records
          </Button>
          <Menu
            anchorEl={anchorEl5}
            open={open5}
            onClose={handleClose5}
          >
            {options5.map((option) => (
              <MenuItem
                key={option}
                selected={option === selectedOption5}
                onClick={() => handleMenuItemClick5(option)}
              >
                {option}
              </MenuItem>
            ))}
          </Menu>
        </Grid>
      </Grid>

      <Box sx={{ mt: 4 }}>
        <Divider />
        <Typography variant="h6" sx={{ mt: 2 }}>
          Usage Instructions
        </Typography>
        <Typography variant="body2" color="text.secondary">
          1. Choose the example that best fits your UI requirements<br />
          2. Copy the relevant code section to your component<br />
          3. Adjust the styling and functionality as needed<br />
          4. Import any required components from Material UI<br />
          5. Implement your specific action logic in the click handlers
        </Typography>
      </Box>
    </Box>
  );
};

export default DropdownButtonExamples;