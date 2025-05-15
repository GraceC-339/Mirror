# Mirror Mirror 🪞
Mirror Mirror is an interactive AI-powered web application designed to help users start their day with a positive mindset. It acts as a friendly, supportive, and empathetic companion, providing positive affirmations based on user input and allowing users to take selfies with a timestamp.

## Features
- **Chat with AI**: Interact with an AI chatbot that provides positive affirmations.
- **Take a Selfie**: Capture selfies with a live webcam preview and a countdown timer.
- **Timestamped Photos**: Selfies include the current date in the bottom-right corner.
- **Responsive Design**: A user-friendly interface for seamless interaction.
--- 
## Technologies Used
### Frontend
- React: For building the user interface.
- Axios: For making API requests to the backend.
- CSS: For styling the application.
### Backend
- **FastAPI**: For handling API requests and managing chatbot logic.
- **Python**: For backend development.
--- 
## **Setup Instructions**

### **1. Clone the Repository**
```
git clone https://github.com/GraceC-339/Mirror.git
cd Mirror
```

### **2. Backend Setup**
1. Navigate to the backend directory:
`cd backend`
2. Create a virtual environment:
`python3 -m venv venv`
`source venv/bin/activate`
4. Install dependencies:
`pip install -r requirements.txt`
5. Run the backend server:
`uvicorn main:app --reload`

### **3. Frontend Setup**
1. Navigate to the frontend directory:
`cd ../frontend`
2. Install dependencies:
`npm install`
3. Start the frontend development server:
`npm start`

## Usage
1. Open the application in your browser at http://localhost:3000.
2. Interact with the chatbot by typing messages in the input box.
3. Click the "Take a Selfie" button to open the webcam preview.
4. Wait for the countdown and capture your selfie with a timestamp.
