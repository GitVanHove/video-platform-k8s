import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { FaTrash, FaPlay } from "react-icons/fa"; // Importing icons
import "../styles/HomePage.css"; 

const HomePage = () => {
  const [videos, setVideos] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/videos/1") // Fetch video list
      .then((res) => res.json())
      .then((data) => {
        const formattedVideos = data.videos.map((file) => ({
          id: file.split("_")[0], // Extract ID
          file: file, // Full filename
        }));
        setVideos(formattedVideos);
      })
      .catch((err) => console.error("Error fetching videos:", err));
  }, []);

  const handleDelete = (id) => {
    fetch(`http://127.0.0.1:5000/videos/${id}`, { method: "DELETE" })
      .then(() => setVideos(videos.filter((video) => video.id !== id)))
      .catch((err) => console.error("Error deleting video:", err));
  };

  return (
    <div className="container">
      <h1 className="title">All Videos</h1>
      <Link to="/upload">
        <button className="upload-btn">Upload Video</button>
      </Link>
      <div className="video-list">
        {videos.length > 0 ? (
          videos.map(({ id, file }) => (
            <div key={id} className="video-card">
              <img
                src={`http://127.0.0.1:5000/video/${id}/${file}`}
                alt="Video Thumbnail"
                className="thumbnail"
              />
              <div className="video-info">
                <Link to={`/video/${id}`} className="video-title">
                  {file} {/* Show filename */}
                </Link>
                <div className="actions">
                  <Link to={`/video/${id}`} className="play-btn">
                    <FaPlay />
                  </Link>
                  <button className="delete-btn" onClick={() => handleDelete(id)}>
                    <FaTrash />
                  </button>
                </div>
              </div>
            </div>
          ))
        ) : (
          <p>No videos available.</p>
        )}
      </div>
    </div>
  );
};

export default HomePage;