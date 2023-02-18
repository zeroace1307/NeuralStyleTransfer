import React, { useState } from "react";
import Button from "@material-ui/core/Button";
import { makeStyles } from "@material-ui/core/styles";

function ImageUpload({ displayText, setImage }) {
  const handleUpload = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = () => setImage(reader.result);
    reader.readAsDataURL(file);
  };

  return (
    <div className="container">
      <label htmlFor="image-upload">
        <Button variant="contained" component="label" color="primary">
          {displayText}
          <input
            hidden
            accept="image/*"
            multiple
            type="file"
            onChange={handleUpload}
          />
        </Button>
      </label>
    </div>
  );
}

export default ImageUpload;
