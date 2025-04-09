from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import config.config as config
import re

OPENAI_API_KEY = config.OPENAI_API_KEY
llm = ChatOpenAI(model_name="gpt-4o-mini",openai_api_key=OPENAI_API_KEY,
    verbose=True, temperature=0.4)

def strip_code_fence(text: str) -> str:
    """Remove ```html ... ``` or ``` ... ``` from the response"""
    # Match content inside triple backticks
    match = re.match(r"```(?:html)?\s*(.*?)\s*```", text, re.DOTALL)
    return match.group(1) if match else text

def format_response_to_html(backend_response: str) -> str:
    system_msg = SystemMessage(
    content=(
        """
        You are a web assistant that transforms text into clean, styled HTML web page. 
        add good stylish professional css
        If the response is plain text, format it in a styled div. 
        If it requires user selection, create appropriate HTML forms like checkboxes, dropdowns, or buttons. text input is not prefered 
        Include minimal styling inline or with a <style> block. 
        Add a <script> that listens to form or button clicks and uses `window.parent.postMessage(...)` 
        to send a message of the format: { type: 'proceed', data: '...user input summary...' }.
        Add <scripts> tag only if user input is required for plain info <script> tag is not required 
        Example: If the user selects an account from a dropdown, send `data: 'proceed with account 12345'`. 
        For checkboxes, send something like `data: 'proceed with these transaction IDs: T1, T2'`.
        """
      )
    )
    human_msg = HumanMessage(content=f"Convert the following response into user-friendly HTML:\n\n{backend_response}")
    
    response = llm([system_msg, human_msg])
    cleaned_html = strip_code_fence(response.content)
    return cleaned_html
