import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/UploadPage.css";

const UploadPage = () => {
  const [file, setFile] = useState(null);
  const navigate = useNavigate();

  const handleUpload = async () => {
    if (!file) return alert("Choose a file first!");

    const formData = new FormData();
    formData.append("video", file); // Key must match Flask ("video")

    const userId = 1; // Replace with the actual user ID
    const response = await fetch(`http://127.0.0.1:5000/upload/${userId}`, {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      alert("Upload successful!");
      navigate("/");
    } else {
      const errorData = await response.json();
      alert(`Upload failed: ${errorData.error}`);
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