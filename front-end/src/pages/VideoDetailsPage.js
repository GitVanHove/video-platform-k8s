import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "../styles/VideoDetailsPage.css"; 

const VideoDetailsPage = () => {
  const { id, filename } = useParams();  
  const navigate = useNavigate();
  const [media, setMedia] = useState(null);
  const [detectedObjects, setDetectedObjects] = useState(null); // Store detected objects

  const userId = localStorage.getItem("user_id"); 

  useEffect(() => {
    if (!userId) {
      alert("User not logged in!");
      return;
    }
  
    if (id) {
      fetch(`http://127.0.0.1:5000/detail/${userId}/${id}`)
        .then((res) => res.json())
        .then((data) => {
          setMedia(data);
          if (data.json_url) {
            // Fetch the detected objects JSON
            fetch(data.json_url)
              .then((res) => res.json())
              .then((jsonData) => setDetectedObjects(jsonData.objects)) // Store objects array
              .catch((err) => console.error("Error fetching detected objects:", err));
          }
        })
        .catch((err) => console.error("Error fetching media data:", err));
    }
  }, [id, userId]);

  const handleDelete = () => {
    fetch(`http://127.0.0.1:5000/video/${userId}/${id}`, { method: "DELETE" })
      .then(() => navigate("/"))
      .catch((err) => console.error("Error deleting video:", err));
  };

  if (!media) return <p>Loading...</p>; 

  const getMediaType = (id) => {
    if (!id) return null;  
    const ext = id.split('.').pop().toLowerCase(); 
    if (ext === 'mp4' || ext === 'mov') return 'video';
    if (ext === 'gif') return 'image';
    if (ext === 'mp3') return 'audio';
    return null;
  };

  const mediaType = getMediaType(id);

  return (
    <div className="video-details-container">
      <h1 className="media-title">{id}</h1>
      
      <div className="media-player">
        {mediaType === 'video' && (
          <video width="800" controls>
            <source src={media.video_url} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        )}
        {mediaType === 'image' && <img src={media.video_url} alt="GIF" width="800" />}
        {mediaType === 'audio' && (
          <audio controls>
            <source src={media.video_url} type="audio/mp3" />
            Your browser does not support the audio tag.
          </audio>
        )}
        {!mediaType && <p>Unsupported media type.</p>}
      </div>

      {/* Detected Objects Section */}
      <div className="detected-objects">
        <h2>Detected Objects</h2>
        {detectedObjects ? (
          <ul>
            {detectedObjects.map((obj, index) => (
              <li key={index}>
                <strong>{obj.label}</strong> - Confidence: {(obj.confidence * 100).toFixed(2)}% at {obj.timestamp}s
              </li>
            ))}
          </ul>
        ) : (
          <p>Loading detected objects...</p>
        )}
      </div>

      <div className="delete-button">
        <button onClick={handleDelete}>Delete Media</button>
      </div>
    </div>
  );
};

export default VideoDetailsPage;