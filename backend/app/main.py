import asyncio
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from .models import QuestionAndDocumentsRequest, GetQuestionAndFactsResponse
from .config import logger, executor
from .util import extract_dialogues, fetch_all_docs
from .gptclient import generate_response

app = FastAPI()
app.mount("/files", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Variables / State
# TODO: Move to Session Store
current_task: Optional[asyncio.Task] = None # Reference to the current processing task
processing_data = {}

# Lock to synchronize access to processing_data
lock = asyncio.Lock()

@app.on_event("startup")
def on_startup():
    # Initialize resources
    pass

@app.on_event("shutdown")
def on_shutdown():
    # Close the executor
    executor.shutdown(wait=True)
    logger.info("Executor has been shut down")

@app.post("/submit_question_and_documents")
async def submit_question_and_documents(request: QuestionAndDocumentsRequest):
    global current_task
    
    # Killing previous generate process if new we get a new question
    if current_task and not current_task.done():
        logger.info("Current task running, attempting to cancel...")
        current_task.cancel()
        try:
            await current_task  # Wait for the task to actually cancel
            logger.info("Current task was successfully cancelled.")
        except asyncio.CancelledError:
            logger.info("Successfully caught cancellation of the task.")
        except Exception as e:
            logger.error(f"Error during task cancellation: {e}")
    

    processing_data["question"] = request.question
    processing_data["facts"] = None
    processing_data["status"] = "processing"

    # Start a new task
    current_task = asyncio.create_task(process_documents(request))
    logger.info("Started new task for processing documents")

    return {"status": "processing"}

@app.get("/get_question_and_facts", response_model=GetQuestionAndFactsResponse)
async def get_question_and_facts():
    logger.info("Inside GET function")
    if not processing_data or (processing_data and not processing_data["question"]) :
        raise HTTPException(status_code=404, detail="No active or recent task data found")
    if processing_data and processing_data["facts"] is None:
        processing_data["status"] = "processing"  

    print(processing_data)      
    return processing_data


# Async function
async def process_documents(request: QuestionAndDocumentsRequest):
    facts = []
    relevant_info_string = ''
    doc_content = ''
    async with lock:
        try:
            loop = asyncio.get_running_loop()

            # TODO: Get keywords from the question to extract only relevant dialogues for cost optimzation
            # keywords = await loop.run_in_executor(executor, extract_keywords, request.question)

            try:
                # Extracting all text from the documents
                doc_content = await fetch_all_docs(request.documents)
                if (doc_content):
                    logger.info("Attempting to extract relevant dialogues")

                    rel_info = await loop.run_in_executor(executor, extract_dialogues, doc_content)
                    relevant_info_string += "".join(rel_info)

                    logger.info(f"Relevant dialogues extracted:\n {relevant_info_string}", )
            except Exception as e:
                logger.error(e)
                processing_data["status"] = "error"

            gpt_response = await generate_response(query=request.question, context=relevant_info_string)
            logger.info(f"GPT response processed.\n {gpt_response}")

            #  Adding extra checks due to unpredictability of LLM
            if "facts" in gpt_response and isinstance(gpt_response['facts'], list) and len(gpt_response["facts"]) >0 and not(len(gpt_response["facts"]) == 1 and gpt_response["facts"][0].strip() == ""):
                facts = gpt_response["facts"]
            else:
                facts = ["I'm sorry, I'm unable to answer your question. Can you please try again?"]

            processing_data["facts"] = facts
            processing_data["status"] = "done"

            logger.info(processing_data["facts"])

        except asyncio.CancelledError:
            logger.info("Document processing was cancelled.")
            processing_data["status"] = "cancelled"
            raise
        except Exception as e:
            processing_data["status"] = "error"
            logger.error(f"Error processing documents: {e}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



