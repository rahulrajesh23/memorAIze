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
