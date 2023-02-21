import logo from "./logo.svg";
import "./App.css";
import exampleImage from "./assets/images/example_output.png";
import lightBulb from "./assets/images/light_bulb.png";
import questionMark from "./assets/images/question_mark.png";
import ImageUpload from "./ImageUpload";
import { createTheme, ThemeProvider } from "@material-ui/core/styles";
import blue from "@material-ui/core/colors/blue";
import React, { useState, useEffect } from "react";
import Button from "@material-ui/core/Button";
import CircularProgress from "@mui/material/CircularProgress";
import { pink } from "@material-ui/core/colors";

const theme = createTheme({
  palette: {
    primary: blue,
    secondary: pink,
  },
});

function arrayBufferToBase64(buffer) {
  let binary = "";
  const bytes = new Uint8Array(buffer);
  const len = bytes.byteLength;
  for (let i = 0; i < len; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary);
}

function App() {
  const url = "http://localhost:5001/image";

  const [contentImage, setContentImage] = useState(null);
  const [styleImage, setStyleImage] = useState(null);
  const [outputImage, setOutputImage] = useState(null);
  // const [outputImage, setOutputImage] = useState(questionMark);
  const [isLoading, setIsLoading] = useState(false);

  const [isGenerateButtonDisabled, setisGenerateButtonDisabled] =
    useState(true);

  var src = questionMark;
  async function sendImageDataToServer(event) {
    const formData = new FormData();
    formData.append("content_image", contentImage);
    formData.append("style_image", styleImage);
    setIsLoading(true);
    try {
      const response = await fetch(url, {
        method: "POST",
        body: formData,
      })
        .then((response) => response.arrayBuffer())
        .then((buffer) => {
          const base64Flag = "data:image/jpeg;base64,";
          const imageStr = arrayBufferToBase64(buffer);
          const imageData = base64Flag + imageStr;
          setIsLoading(false);
          setOutputImage(imageData);
        });

      // if (!response.ok) {
      //   throw new Error(`HTTP error! Status: ${response.status}`);
      // }

      // const responseData = await response.json();
      // return responseData;
      // fetch(url);
    } catch (error) {
      setIsLoading(false);
      console.error("Error:", error);
    }
  }

  useEffect(() => {
    // update count2 when count1 is updated
    if (contentImage && styleImage) {
      setisGenerateButtonDisabled(false);
    }
  }, [contentImage, styleImage]);

  useEffect(() => {
    // update count2 when count1 is updated
    if (isLoading) {
      setOutputImage(null);
    }
  }, [isLoading]);

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
                  height: "50px",
                  flexDirection: "row",
                }}
              >
                <div style={{ flex: 1 }}>
                  <ImageUpload
                    displayText="upload content"
                    setImage={setContentImage}
                  />
                </div>
                <div style={{ flex: 1 }}>
                  <ImageUpload
                    displayText="upload style"
                    setImage={setStyleImage}
                  />
                </div>
              </div>
              <div
                style={{
                  display: "flex",
                  flex: "1",
                  padding: "10px",
                  height: "200px",
                  flexDirection: "row",
                }}
              >
                <div style={{ flex: 1 }}>
                  {contentImage && (
                    <img
                      src={contentImage}
                      alt="uploaded content image"
                      style={{
                        maxWidth: "100%",
                        maxHeight: "100%",
                        objectFit: "contain",
                      }}
                    />
                  )}
                </div>
                <div style={{ flex: 1 }}>
                  {styleImage && (
                    <img
                      src={styleImage}
                      alt="uploaded style image"
                      style={{
                        maxWidth: "100%",
                        maxHeight: "100%",
                        objectFit: "contain",
                      }}
                    />
                  )}
                </div>
              </div>
            </div>
          </div>
          <div
            style={{
              display: "flex",
              flex: 1,
              justifyContent: "center",
              alignItems: "center",
              flexDirection: "column",
            }}
          >
            <div
              style={{
                display: "flex",
                height: "10%",
                justifyContent: "center",
                alignItems: "center",
              }}
            >
              {isLoading ? (
                <CircularProgress />
              ) : (
                <Button
                  variant="contained"
                  component="label"
                  color="secondary"
                  disabled={isGenerateButtonDisabled}
                  onClick={sendImageDataToServer}
                >
                  GENERATE
                </Button>
              )}
            </div>
            <div
              style={{
                display: "flex",
                height: "70%",
                width: "80%",
                justifyContent: "center",
                alignContent: "center",
                border: "5px dashed black",
                borderRadius: "20px",
                marginBottom: "100px",
              }}
            >
              <div
                style={{
                  height: "100%",
                  width: "100%",
                  justifyContent: "center",
                  alignContent: "center",
                  marginTop: "100px",
                  marginBottom: "100px",
                }}
              >
                {outputImage ? (
                  <img
                    src={outputImage}
                    alt="An example image"
                    style={{
                      width: "50%",
                      height: "50%",
                      marginTop: "50px",
                      marginBottom: "50px",
                    }}
                  />
                ) : null}
              </div>
            </div>
          </div>
        </div>
      </div>
    </ThemeProvider>
  );
}

export default App;
