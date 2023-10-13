import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import '../css/chat_interface.css'; // Import your CSS for the chat interface

function ChatInterface() {
  const [inputText, setInputText] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [isChatOpen, setIsChatOpen] = useState(false);
  const chatHistoryRef = useRef(null);

  const addMessageToChat = (role, content) => {
    setChatHistory((prevHistory) => [...prevHistory, { role, content }]);
  };

  const handleInputChange = (event) => {
    setInputText(event.target.value);
  };

  const handleSendMessage = () => {
    if (inputText.trim() === '') return;

    // Add user message to chat history
    addMessageToChat('user', inputText);

    // Prepare the request payload
    const payload = {
      role: 'user',
      content: inputText,
    };

    // Make a POST request to your local Flask server
    axios.post('http://127.0.0.1:5000/call_external_api', payload, {
      headers: {
        'Content-Type': 'application/json',
        'Input-Text': inputText,
      },
    })
      .then((response) => {
        // Handle the API response
        if (response.data && response.data.response) {
          const apiResponse = response.data.response;
          const content = apiResponse.openAIResponse.choices[0].message.content;

          // Add bot response to chat history
          addMessageToChat('bot', content);
        }
      })
      .catch((error) => {
        console.error('API call error:', error);
      });

    // Clear the input field
    setInputText('');
  };

  const handleEnterKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleSendMessage();
    }
  };

  // Use useEffect to scroll to the bottom of the chat history when it updates
  useEffect(() => {
    if (chatHistoryRef.current) {
      chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
    }
  }, [chatHistory]);

  return (
    <div className="chat-interface">
      {isChatOpen ? (
        <div>
          <div className="chat-history" ref={chatHistoryRef}>
            {chatHistory.map((message, index) => (
              <div key={index} className={`chat-message ${message.role}`}>
                {message.content}
              </div>
            ))}
          </div>
          <div className="chat-input">
            <input
              type="text"
              className="input-text"
              value={inputText}
              onChange={handleInputChange}
              placeholder="Type a message to chat with the assistant..."
              onKeyPress={handleEnterKeyPress} // Handle Enter key press
            />
            <button className="send-button" onClick={handleSendMessage}>
              Send
            </button>
          </div>
        </div>
      ) : (
        <div className="chat-start">
          <strong>
            <div className="assistant-text">Do you want to chat with the Assistant? Click below to start.</div>
          </strong>
          <button className="chat-start-button" onClick={() => setIsChatOpen(true)}>
            Start Chat
          </button>
        </div>
      )}
    </div>
  );
}

export default ChatInterface;
