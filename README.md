# Transcript AI

## Overview

Transcript AI is designed to process documents and extract facts relevant to a user-submitted question. It employs advanced document processing techniques to maintain the accuracy and relevance of the facts over a series of documents, giving users only the most most succinct answer in a predictable format.

The next section goes over the Design Decisions and Limitations. This is followed by the Application Structure and finally, the Setup Instructions

## LLM Prompting Designs and Limitations

### Document Retrieval

- **Basic Parsing**: Initial parsing of documents focused on extracting only relevant dialogues to optimize the context sent to the LLM. Unnecessary White spaces are eliminated.
- **Advanced Techniques**: Explored the use of a smaller model (e.g., SpaCy) to extract key keywords from the question and perform similarity matching on individual dialogues. However, this approach sometimes led to the loss of crucial context needed by the LLM to make informed decisions. In a production environment, the smaller model could be fine-tuned to more accurately extract relevant dialogues, considering the specific domain.


### Prompt Construction

- **Structure**: The prompt was structured as `[persona] + [context] + [task] + [suggested_steps] + [format]`.
- **Brevity and Precision**: The goal was to keep the prompt concise, avoiding overfitting to specific test scenarios.
- **Response Format**: Utilized `response_format={"type": "json_object"}` when calling the GPT-4 API to encourage the model to return a stringified JSON object.
- **Token Management**: Configured `max_tokens` to ensure the GPT-4 output was constrained, preventing the model from processing an excessively high number of tokens.
- **Privacy Concerns**: This wasn't implemented. Depending on the business use case, we could add instructions to protect personally identifiable information (PII)..
- **Handling Outliers**: A default response was encoouraged while either the Question or the Context is irrelevant to the other.

### Limitations
- The prompt could fail in several scenarios. The scope of this project was to only extract the final list facts given a context and query. 
- Its performance is not reliable while asking for more nuanced details that occur in the middle of the context.

### Configurations

The `.env` file can be modified to 

- **API Key**: Enter the necessary API key for accessing services.
- **Environment Settings**: Specify the environment setting; based on this, specific loggers are activated to tend to the application's logging needs.


## Application Structure

### User Interface

- **Functionality**: Users can submit a question along with one or more URLs pointing to text documents to extract relevant information
- **Presentation**: The AI backend service returns a list of relevant "facts" that are extracted from the document, presented as a conversation

### API Endpoints

### POST `api/submit_question_and_documents`

- **Payload**:
  ```json
  {
    "question": "<your_question>",
    "documents": ["<url_1>", "<url_2>", "<url_3>, ..."]
  }
  ```
- **Response**:
  ```json
  {
    "status": "<processing/error>"
  }

**Note:** Submitting a new question clears the previous operation, and any following GET operation will only return the response of the last question.

### GET `api/get_question_and_facts`

**Response**
- **Facts still processing**:
  ```json
  {
    "question": "<your_question>",
    "facts": null,
    "status": "processing"
  }
  ```
- **Successfully fetched facts**:
  ```json
  {
    "question": "<your_question>",
    "facts": [
      "Fact 1",
      "Fact 2",
      "Fact 3"
      .
      .
    ],
    "status": "done"
  }
  ```
## Code Setup

This project includes Docker configurations for an integrated execution environment which includes the frontend, backend, and Nginx modules.

### Initial Setup

1. **Fork the Repository**: Start by forking the repo to your GitHub account.
2. **Clone and Navigate**: Clone the forked repository to your local machine and navigate to the root folder of the project.

   ```bash
   git git@github.com:rahulrajesh23/transcript-ai.git project_name
   cd project_name
   ```
3. **Environment Setup**:
   - Set up a Python virtual environment:

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
4. **Create .env file**:
   - Rename the `.env.template` file in the root directory and configure your API Key and other environment variables

5. **Docker Compose**:
   - Modify the `docker-compose.yml` file if necessary.
   - Run the Docker containers:

     ```bash
     docker-compose up -d
     ```

   This command starts the frontend React server, the backend FastAPI server, and configures Nginx to manage ports.

6. **Access the Application**:
   - The application should now be running and accessible via [http://localhost/app](http://localhost/app).

### Alternative Setup: Building Separately

If you prefer to build the frontend and backend separately using Docker, perform the following steps:

- Navigate to the respective directory (`frontend` or `backend`).
- Run the following command in each directory:

  ```bash
  docker-compose up -d
  
  ```
### Manual Build (Without Docker)

For developers preferring to manually set up the project without Docker:

1. **Frontend Setup**:
   - Navigate to the `/frontend` directory.
   - Install dependencies and start the server:

     ```bash
     npm install
     npm start
     ```

   - The frontend service will be available at [http://localhost:3000](http://localhost:3000).

2. **Backend Setup**:
   - Navigate to the `/backend` directory.
   - Install Python dependencies:

     ```bash
     pip install -r requirements.txt
     ```

   - Start the FastAPI server:

     ```bash
     uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
     ```

   - The backend service will be running at [http://localhost:8000](http://localhost:8000).

   - **Note**: If running the backend service manually, update the API paths in the frontend code. The Nginx configuration obfuscates the port number and adds `/api` to the backend APIs. For example, use `http://localhost:8000/api_name`.


