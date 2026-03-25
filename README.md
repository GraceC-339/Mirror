# Mirror Mirror 🪞

Mirror Mirror is an interactive AI-powered web application designed to help users start their day with a positive mindset. It acts as a friendly, supportive, and empathetic companion, providing positive affirmations based on user input and allowing users to take selfies with a timestamp.

**Current Status**: This is a **quick development prototype** built for rapid iteration and learning. See [Future Roadmap](#future-roadmap) for production-readiness improvements.

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

### **2. Backend Setup** (requires Python 3.12+):
`python3 -m venv .venv`
`source .venv/bin/activate`
3. Install dependencies:
`pip install -r requirements.txt`
4. Create a `.env` file in `backend/` with your Azure OpenAI credentials:
```
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=you-project-name
AZURE_OPENAI_API_VERSION=
```
5. Run the backend server:
`python -m . Install dependencies:
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

---

## Usage
1. Open the application in your browser at http://localhost:3000.
2. Interact with the chatbot by typing messages in the input box.
3. Click the "Take a Selfie" button to open the webcam preview.
4. Wait for the countdown and capture your selfie with a timestamp.

---

## Future Roadmap

### Phase 1: Production Readiness (High Priority)
- [ ] **Per-Session State**: Implement session-scoped conversation state using Redis or database
- [ ] **Persistent Database**: Move to PostgreSQL/MongoDB for conversation history and metadata
- [ ] **Structured Logging**: Add proper logging framework (Python logging module) for debugging and monitoring
- [ ] **Cloud Storage**: Migrate selfies to S3/Azure Blob Storage for scalability
- [ ] **Error Handling**: Implement custom exception handlers and meaningful error responses

### Phase 2: Feature Enhancement (Medium Priority)
- [ ] **User Authentication**: Add user accounts and sign-in flow
- [ ] **Response Models**: Strict Pydantic response types for API documentation
- [ ] **API Documentation**: Auto-generated Swagger UI customization and schema validation
- [ ] **Conversation Analytics**: Track sentiment, user engagement, and affirmation effectiveness
- [ ] **Selfie Gallery**: User history of selfies with date filters

### Phase 3: Scalability & Operations (Medium Priority)
- [ ] **Containerization**: Docker image with multi-stage builds
- [ ] **Container Orchestration**: Kubernetes deployment manifests
- [ ] **Dependency Injection**: FastAPI Depends() for cleaner code organization
- [ ] **Unit & Integration Tests**: Comprehensive test coverage with pytest
- [ ] **CI/CD Pipeline**: GitHub Actions for automated testing and deployment

### Phase 4: Advanced Features (Lower Priority)
- [ ] **Notification System**: Reminders and scheduled affirmations
- [ ] **Social Sharing**: Share selfies and affirmations (privacy-respecting)
- [ ] **Mobile App**: Native mobile clients for iOS/Android
- [ ] **Accessibility**: WCAG 2.1 compliance for inclusive design

