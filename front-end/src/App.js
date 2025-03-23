import HomePage from "./pages/HomePage";
import UploadPage from "./pages/UploadPage";
import VideoDetailsPage from "./pages/VideoDetailsPage";
import LoginPage from "./pages/LoginPage";
import Navbar from "./components/Navbar";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import './App.css';

function App() {
  return (
    <Router>
      <Navbar />
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/upload" element={<UploadPage />} />
      <Route path="/video/:id" element={<VideoDetailsPage />} />
      <Route path="/login" element={<LoginPage />} />
    </Routes>
  </Router>
  );
}

export default App;
