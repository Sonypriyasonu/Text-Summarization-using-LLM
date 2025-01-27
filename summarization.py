import os
import logging
import re
from better_profanity import profanity
from prompts import prompt_templates
from dotenv import load_dotenv
from langsmith import traceable
from langchain.callbacks.tracers import LangChainTracer
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env file
load_dotenv()

# Set environment variables directly from the .env file
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
langchain_tracing = os.getenv('LANGCHAIN_TRACING_V2')
langchain_api_key = os.getenv('LANGCHAIN_API_KEY')

if langchain_tracing:
    os.environ['LANGCHAIN_TRACING_V2'] = langchain_tracing

if langchain_api_key:
    os.environ['LANGCHAIN_API_KEY'] = langchain_api_key
    
# Configure logging
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
tracer = LangChainTracer()

class TextSummarizer:
    def __init__(self):
        # Initialize with the API keys from environment variables
        self.langchain_api_key = langchain_api_key
        #self.google_api_key = GOOGLE_API_KEY
        #genai.configure(api_key=self.google_api_key)  # Configure Google API Key

    # Function to calculate token count (approximation based on word count)
    @staticmethod
    def count_tokens(text):
        return len(text.split())  # A rough estimate: count words

    # Function to generate the summary from text
    @traceable(tracer)
    def generate_summary(self, text, prompt_template, detail_level=None, audience=None):
        self.google_api_key = GOOGLE_API_KEY
        if audience:  
            prompt = prompt_template.format(text=text, audience=audience, level=detail_level)
        elif detail_level:
            prompt = prompt_template.format(text=text, level=detail_level)
        else:
            prompt = prompt_template.format(text=text)

        # Initialize the model and generate content
        model = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", google_api_key=self.google_api_key,temperature=1)
        response = model.invoke(prompt)
        print(response)
        # Count tokens in both prompt and response
        prompt_tokens = self.count_tokens(prompt)
        response_tokens = self.count_tokens(response.content)
        total_tokens = prompt_tokens + response_tokens
             
        # Log the prompt, response, and token usage
        logger.info(f"Prompt: {prompt}")
        logger.info(f"Response: {response.content}")
        logger.info(f"Prompt tokens: {prompt_tokens}")
        logger.info(f"Response tokens: {response_tokens}")
        logger.info(f"Total tokens used: {total_tokens}")

        # Return the response text and token usage
        return response.content, prompt_tokens, response_tokens, total_tokens

    # Function to check for profanity
    @staticmethod
    def contains_profanity(text):
        return profanity.contains_profanity(text)  # Returns True if profanity detected

    # Function to detect PII (Personally Identifiable Information) like emails, phone numbers, SSNs, etc.
    @staticmethod
    def contains_confidential_info(text):
        # Regex patterns to detect different types of confidential information
        
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
        phone_pattern = r'\+?\d[\d -]{8,15}\d'
        ssn_pattern = r'\b\d{3}-\d{2}-\d{4}\b'
        credit_card_pattern = r'\b(?:\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}|\d{4}[-\s]?\d{6}[-\s]?\d{5})\b'
        address_pattern = r'\d{1,5} [A-Za-z0-9 ]+ (Ave|St|Rd|Blvd|Ln|Dr|Ct|Pl|Way|Terrace|Circle|Square)\b'
        bank_account_pattern = r'\b\d{9,18}\b'
        dob_pattern = r'(\d{2}[-/]\d{2}[-/]\d{4}|\d{4}[-/]\d{2}[-/]\d{2})'
        url_pattern = r'https?://[^\s/$.?#].[^\s]*'
        key_pattern =  r'([a-zA-Z0-9_]+_?key)\s*=\s*["\']?[a-zA-Z0-9\-_]{16,64}["\']?'

        patterns = [
            email_pattern, phone_pattern, ssn_pattern, credit_card_pattern,
            address_pattern, bank_account_pattern, dob_pattern, url_pattern,re.compile(key_pattern, re.IGNORECASE)
        ]
        
        # Check for matches using the patterns
        for pattern in patterns:
            if re.search(pattern, text):
                return True  # Return True if any sensitive data is found
        
        return False

