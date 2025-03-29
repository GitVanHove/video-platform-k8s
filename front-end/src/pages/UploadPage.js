import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/UploadPage.css";

const UploadPage = () => {
  const [file, setFile] = useState(null);
  const navigate = useNavigate();

  const handleUpload = async () => {
    if (!file) return alert("Choose a file first!");

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      alert("Upload successful!");
      navigate("/");
    }
  };

  return (
    <div className="upload-container">
      <h1 className="upload-title">Upload a Video</h1>
      <input type="file" className="upload-input" onChange={(e) => setFile(e.target.files[0])} />
      <button className="upload-btn" onClick={handleUpload}>Upload</button>
    </div>
  );
};

export default UploadPage;