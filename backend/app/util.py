import re
import httpx
import os
from .config import logger
from urllib.parse import urlparse
from fastapi import HTTPException

import ipaddress

APP_ENV = os.getenv("APP_ENV", "DEV")


def extract_dialogues(doc):
    # Compile pattern to extract sentences
    pattern = re.compile(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\s*\n(.*?): (.*?)(?=\n\d{2}:\d{2}|\Z)', re.DOTALL)
    matches = pattern.findall(doc)
    relevant_dialogues = [f"{speaker}: {speech_instance}" for speaker, speech_instance in matches]

    return relevant_dialogues

# Fetch content from all the document urls
async def fetch_all_docs(documents):
    doc_content = ''
    try:
        for doc_url in documents:
            document_content = await fetch_document(doc_url)
            doc_content += document_content + '\n'
    except Exception as e:
        logger.error(f"Error processing documents: {e}")
    return doc_content
    
async def fetch_document(url):
    headers = {'Accept': 'application/json', 'User-Agent': 'minute-app'}
    doc_content = ''
    try:
        if APP_ENV == "DEV" or is_safe_url(url):
            async with httpx.AsyncClient(headers=headers) as client:
                response = await client.get(url)
                if response.status_code == 200 and response.headers.get('Content-Type', '').startswith('text/plain'):
                    doc_content = response.text
                else:
                    logger.warning(f"Failed to fetch {url} with status code: {response.status_code}")
        else:
            raise  HTTPException(status_code=403, detail="Foribidden")
    except Exception as e:
        logger.warning(f"Exception occurred when fetching {url}: {e}")
    finally:
        logger.info("HTTP client operation completed.")
        return doc_content
    
def is_safe_url(url):
    try:
        result = urlparse(url)
        hostname = result.hostname

        # Check if the hostname is an IP address
        try:
            ip = ipaddress.ip_address(hostname)
            # Block private and loopback addresses
            if ip.is_private or ip.is_loopback:
                return False
        except ValueError:
            # Hostname is not an IP address, check if it's localhost
            if hostname in ['localhost', '127.0.0.1', '::1']:
                return False

        # Add more conditions to refine what URLs should be considered safe
        return True
    except ValueError:
        return False

    
"""
# TODO: 
Can be adopted to filter dialogues, but would need a model that is fine-tuned 
to business domain to extract good results without losing important context
"""
# import spacy
# nlp = spacy.load('en_core_web_sm')

# def extract_relevant_dialogues(doc, keywords, threshold=0.5):
#     # Compile pattern to extract sentences
#     pattern = re.compile(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\s*\n(.*?): (.*?)(?=\n\d{2}:\d{2}|\Z)', re.DOTALL)

#     matches = pattern.findall(doc)
#     relevant_dialogues = [f"{speaker}: {speech_instance}" for speaker, speech_instance in matches]
#     keyword_doc = nlp(" ".join(keywords))
#     relevant_dialogues = []
#     for speaker, speech_instance in matches:
#         speech_instance_doc = nlp(speech_instance)
#         similarity_score = speech_instance_doc.similarity(keyword_doc)
#         if similarity_score > threshold: 
#             relevant_dialogues.append(speaker + ": " + speech_instance)

#     return relevant_dialogues

# # Basic NLP processing to extract keywords from the question
# def extract_keywords(question):
#     doc = nlp(question)
#     keywords = [token.lemma_ for token in doc if token.pos_ in ['NOUN', 'VERB', 'ADJ']]
#     return keywords