import os
import tiktoken
import json
from openai import AsyncOpenAI
from .config import logger

GPT_APIKEY = os.getenv("GPT_APIKEY", "")
GPT_MODEL_NAME = os.getenv("GPT_MODEL_NAME", "gpt-3.5-turbo")


# Context and Response Token size can be adjusted according to business requirements 
MAX_CONTEXT_SIZE = 7000 
MAX_RESPONSE_TOKENS = 2000

openAIClient = AsyncOpenAI(
  api_key= GPT_APIKEY,
)

# Code snippet borrowed from : https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken
def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        logger.warning("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
        }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        logger.warning("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        logger.warning("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


async def generate_response(query='', context = ''):
    config = {
        "model": GPT_MODEL_NAME,
        "temperature": 0,
        "response_format": { "type": "json_object" },
        "max_tokens": MAX_RESPONSE_TOKENS
    }

    gpt_response = {
        "status": "",
        "facts": []
    }

    messages = [
            {
                "role": "system",

                "content": "You are a highly skilled AI tasked with analyzing conversations from meeting logs to extract the most current and relevant decisions in json format. Given a question and call logs, your role involves identifying the latest agreed-upon facts from a series of dialogues in the logs. While going through each sentence of the context, if a decision was made and then later changed, only the final version of that decision should be in the answers. If a decision is made and then later decided against, don't record anything about that decision. Final output has to be a json. Your summarized answer is stored in key 'facts' which is an array of strings, each string being a single sentence of your answer. if two sentences are related to the same thing, club them. If no answers are possible for the question-query, simply return empty array of facts'. Sample= {'facts':['The team made decision 1','The team made decison 2']}"                },
            {
                "role": "user",
                "content": "\nQuestion: " + query + "\nContext: \n" + context
            }
    ]
    try :
        num_tokens = num_tokens_from_messages(messages, model=GPT_MODEL_NAME)
        logger.info(f"Number of tokens in LLM prompt: {num_tokens}")
        if num_tokens > MAX_CONTEXT_SIZE - config['max_tokens']: # To control the input text size
            return {
                "status" : "error",
                "facts" : ["Sorry, that's too much text for me to process. Can you reduce the number of attached files and try again?"]
            }
        response = await getLLMResponse(messages, config)
        logger.info(f"GPT Response: {response}")
        
    except Exception as e:
        logger.error(e)
        return {
            "status" : "error",
            "facts" : ["Sorry, I'm having some trouble answering your question. Please contact support"]
        }

    if(response):
        try:
            response = json.loads(response)
            response['status'] = 'success'
            return response
        except:
            return {
            "status" : "error",
            "facts" : ["Sorry, I'm having some trouble answering your question. Please contact support"]
        }

    return {}

async def getLLMResponse(messages, config):
    response = await openAIClient.chat.completions.create(
        model=config['model'],
        temperature=config['temperature'],
        messages=messages,
        response_format={ "type": "json_object" },
        max_tokens=config['max_tokens']
    )
    return response.choices[0].message.content

