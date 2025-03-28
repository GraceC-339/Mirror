import React, { useState, useRef } from "react";
import axios from "axios";

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [showVideoModal, setShowVideoModal] = useState(false);
  const [countdown, setCountdown] = useState(null); // State for countdown
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  const sendMessage = async () => {
    if (input.trim() === "") return;

    const userMessage = { user_text: input };
    setMessages([...messages, { sender: "user", text: input }]);
    setInput("");

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/generate-affirmation",
        userMessage
      );
      const botMessage = response.data.message || response.data.affirmation;
      setMessages([
        ...messages,
        { sender: "user", text: input },
        { sender: "bot", text: botMessage },
      ]);
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  const takeSelfie = async () => {
    try {
      console.log("Accessing webcam...");
      // Access the webcam
      const stream = await navigator.mediaDevices.getUserMedia({
        video: true,
      });
      console.log("Webcam accessed successfully");

      // Show the video modal first
      setShowVideoModal(true);

      // Wait for the modal to render
      setTimeout(() => {
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          videoRef.current.play(); // Start playing the video
        } else {
          console.error("Video element not found");
        }

        // Start the countdown
        let countdownValue = 5;
        setCountdown(countdownValue);
        const countdownInterval = setInterval(() => {
          countdownValue -= 1;
          setCountdown(countdownValue);

          if (countdownValue === 0) {
            clearInterval(countdownInterval);

            // Capture the photo
            const canvas = canvasRef.current;
            const video = videoRef.current;

            if (canvas && video) {
              canvas.width = video.videoWidth;
              canvas.height = video.videoHeight;
              const context = canvas.getContext("2d");
              context.drawImage(video, 0, 0, canvas.width, canvas.height);

              // Add the date to the bottom-right corner
              const date = new Date().toLocaleDateString();
              context.font = "20px Arial";
              context.fillStyle = "white";
              context.textAlign = "right";
              context.fillText(date, canvas.width - 10, canvas.height - 10); // 10px padding from the edges
            } else {
              console.error("Canvas or video element not found");
            }

            // Stop the webcam stream
            stream.getTracks().forEach((track) => track.stop());
            setShowVideoModal(false); // Hide the video modal
            setCountdown(null); // Reset the countdown

            // Convert the photo to a Blob and send it to the backend
            canvas.toBlob(async (blob) => {
              const formData = new FormData();
              formData.append("photo", blob, "selfie.png");

              try {
                const response = await axios.post(
                  "http://127.0.0.1:8000/take-selfie",
                  formData,
                  {
                    headers: { "Content-Type": "multipart/form-data" },
                  }
                );
                console.log("Selfie saved:", response.data);
                setMessages([
                  ...messages,
                  { sender: "bot", text: "Selfie saved successfully!" },
                ]);
              } catch (error) {
                console.error("Error saving selfie:", error);
              }
            });
          }
        }, 1000); // Update countdown every second
      }, 100); // Delay to ensure the modal and video element are rendered
    } catch (error) {
      console.error("Error accessing webcam:", error);
    }
  };

  return (
    <div className="chat-container">
      <h1>Mirror Mirror🪞</h1>
      <p>Say Hi to Mirror Mirror🪞 and take a selfie today</p>
      <div className="chat-box">
        {messages.map((msg, index) => (
          <div key={index} className={`chat-message-container ${msg.sender}`}>
            {/* Avatar */}
            <div className="avatar">
              {msg.sender === "user" ? (
                <img
                  src="/test2.png" // Replace with the actual path to the user avatar
                  alt="User Avatar"
                />
              ) : (
                <img
                  src="/test1.png" // Replace with the actual path to the AI avatar
                  alt="AI Avatar"
                />
              )}
            </div>
            {/* Message */}
            <div className={`chat-message ${msg.sender}`}>{msg.text}</div>
          </div>
        ))}
      </div>

      <div className="chat-input">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Say hi to Mirror, Mirror..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
      <div className="take-selfie">
        <button onClick={takeSelfie}>Take a Selfie</button>
      </div>
      {/* Modal for video preview */}
      {showVideoModal && (
        <div className="video-modal">
          <div className="video-container">
            <video ref={videoRef} autoPlay></video>
            {countdown !== null && <div className="countdown">{countdown}</div>}
          </div>
        </div>
      )}
      <canvas
        ref={canvasRef}
        width="640"
        height="480"
        style={{ display: "none" }}
      ></canvas>
    </div>
  );
};

export default Chat;
