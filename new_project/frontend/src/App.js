import React from 'react';
import { ThemeProvider } from '@mui/material/styles';
import theme from './theme';

function App() {
  return (
    <ThemeProvider theme={theme}>
      {/* Your app components here */}
    </ThemeProvider>
  );
}

export default App;