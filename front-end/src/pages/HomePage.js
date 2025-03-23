import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

const HomePage = () => {
  const [videos, setVideos] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/videos") // Change to your actual API
      .then((res) => res.json())
      .then((data) => setVideos(data));
  }, []);

  return (
    <div>
      <h1>All Videos</h1>
      <Link to="/upload"><button>Upload Video</button></Link>
      <ul>
        {videos.map((video) => (
          <li key={video.id}>
            <Link to={`/video/${video.id}`}>{video.title}</Link>
            <button onClick={() => handleDelete(video.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );

  function handleDelete(id) {
    fetch(`http://localhost:5000/videos/${id}`, { method: "DELETE" })
      .then(() => setVideos(videos.filter((video) => video.id !== id)));
  }
};

export default HomePage;