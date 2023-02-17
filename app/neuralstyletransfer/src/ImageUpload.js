import React, { useState } from "react";
import Button from "@material-ui/core/Button";
import { makeStyles } from "@material-ui/core/styles";

function ImageUpload(props) {
  const [image, setImage] = useState(null);

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = () => {
      setImage(reader.result);
    };
    reader.readAsDataURL(file);
  };

  return (
    <div className="container">
      <Button
        variant="contained"
        component="label"
        onChange={props.onChange}
        color="primary"
      >
        {props.displayText}
        {/* <input hidden accept="image/*" multiple type="file" /> */}
      </Button>
      {image && <img src={image} alt="Uploaded" />}
    </div>
  );
}

export default ImageUpload;
