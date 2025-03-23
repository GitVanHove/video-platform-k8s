import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

const VideoDetailsPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [video, setVideo] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:5000/videos/${id}`)
      .then((res) => res.json())
      .then((data) => setVideo(data));
  }, [id]);

  if (!video) return <p>Loading...</p>;

  return (
    <div>
      <h1>{video.title}</h1>
      <video width="600" controls>
        <source src={`http://localhost:5000/${video.filename}`} type="video/mp4" />
      </video>
      <p>Description: {video.description}</p>
      <button onClick={handleDelete}>Delete Video</button>
    </div>
  );

  function handleDelete() {
    fetch(`http://localhost:5000/videos/${id}`, { method: "DELETE" })
      .then(() => navigate("/"));
  }
};

export default VideoDetailsPage;