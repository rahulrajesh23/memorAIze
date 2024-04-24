# Fact Extractor Application

## Overview

The Fact Extractor Application is designed to process call transcripts and extract facts relevant to a user-submitted question. It employs advanced document processing techniques to maintain the accuracy and relevance of the facts over a series of documents, considering any modifications or removals that occur in subsequent texts.

## Application Structure

### Input Screen

- **Functionality**: Users can submit a question along with one or more URLs pointing to call log transcripts.
- **Purpose**: To gather information and initiate the process of fact extraction relevant to the question.

### Output Screen

- **Functionality**: Displays a bulleted list of extracted facts.
- **Presentation**: Facts are listed in clear, simple language to ensure easy comprehension.

## Document Processing

- **Sequential Relevance**: The application processes documents in the order they are provided. Facts from later documents can add to, modify, or nullify facts from earlier documents based on the content changes.
- **Optimization**: The system is optimized for accuracy, ensuring that the final list of facts is up-to-date and relevant to the user’s query.

## API Endpoints

### POST `/submit_question_and_documents`

- **Payload**:
  ```json
  {
    "question": "Your question here",
    "documents": ["<URL1>", "<URL2>", "<URL3>"]
  }

### GET `/get_question_and_facts`

- **Response**:
  ```json
  {
    "question": "Your question here",
    "facts": [
      "Fact 1",
      "Fact 2",
      "Fact 3"
    ],
    "status": "done"
  }

## Design Considerations

- **Model Usage**: The application utilizes GPT-4 for processing and extracting facts, leveraging its advanced natural language understanding capabilities.
- **API Key**: Ensure you have your own API key for GPT-4 usage as the application requires it for operation.
- **Idempotence**: Submitting a new question and document URLs resets the application state and starts the fact extraction process anew.

## Getting Started

To run the application:
1. Ensure you have Python 3.x and Flask installed.
2. Clone the repository.
3. Install dependencies using `pip install -r requirements.txt`.
4. Set your API key in the configuration file.
5. Start the server with `python app.py`.

Visit `localhost:5000` in your browser to access the application.

