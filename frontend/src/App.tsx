import './App.css'
import Home from './pages/Home'
import Background from './components/Background/'
import { createTheme, ThemeProvider, CssBaseline, GlobalStyles } from '@mui/material'
import { indigo } from '@mui/material/colors';
import { QueryClient, QueryClientProvider } from 'react-query';
function App() {
  const theme = createTheme({
    typography: {
      fontFamily: 'Montserrat',
      fontSize: 18,
    },
    palette: {
      primary: indigo,
      background: {
        default: indigo[800],
        paper: indigo[200]
      }
    }
  })
  const queryClient = new QueryClient();

  return (
    <div className="App" style={{ width: '100vw', height: "100vh" }}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <GlobalStyles
          styles={{
            body: { backgroundColor: indigo[300] },
          }}
        />
        <QueryClientProvider client={queryClient}>
          <Home />
        </QueryClientProvider>

      </ThemeProvider>
    </div>
  )
}

export default App
