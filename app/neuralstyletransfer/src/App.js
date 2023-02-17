import logo from "./logo.svg";
import "./App.css";
import exampleImage from "./assets/images/example_output.png";
import ImageUpload from "./ImageUpload";
import { createMuiTheme, ThemeProvider } from "@material-ui/core/styles";
import blue from "@material-ui/core/colors/blue";

const theme = createMuiTheme({
  palette: {
    primary: blue,
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <div className="App" style={{ height: "100%" }}>
        <div
          style={{
            flex: 1,
            display: "flex",
            flexDirection: "row",
            height: "100%",
          }}
        >
          <div
            style={{
              flex: 1,
              display: "flex",
              flexDirection: "column",
            }}
          >
            <div display="flex" style={{ flex: "2", width: "100%" }}>
              <h1 className="title">Neural Style Transfer</h1>
              <div justify-content="center" align-items="center">
                <img
                  src={exampleImage}
                  alt="An example image"
                  style={{ width: "60%", height: "10%" }}
                />
              </div>

              <div
                style={{
                  display: "flex",
                  flex: "1",
                  padding: "20px",
                  height: "100px",
                  flexDirection: "row",
                }}
              >
                <div style={{ flex: 1 }}>
                  <ImageUpload displayText="upload content" />
                </div>
                <div style={{ flex: 1 }}>
                  <ImageUpload displayText="upload style" />
                </div>
              </div>
              <div
                style={{
                  display: "flex",
                  flex: "1",
                  alignItems: "flex-start",
                  padding: "20px",
                  height: "100px",
                }}
              >
                <div style={{ flex: 1 }}>
                  <ImageUpload displayText="upload style" />
                </div>
                <div style={{ flex: 1 }}>
                  <ImageUpload displayText="upload style" />
                </div>
              </div>
            </div>
          </div>
          <div style={{ flex: 1 }}>
            <img src={logo} className="App-logo" alt="logo" />
            <p>
              Edit <code>src/App.js</code> and save to reload.
            </p>
            <a
              className="App-link"
              href="https://reactjs.org"
              target="_blank"
              rel="noopener noreferrer"
            >
              Learn React
            </a>
          </div>
        </div>
      </div>
    </ThemeProvider>
  );
}

export default App;
