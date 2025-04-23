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
            You are a web assistant that converts raw or unstructured text into a clean, professional HTML web page with consistent styling and layout.
            Requirements:
            1. Apply modern, professional CSS with:
              - Clean font (e.g., system-ui, Roboto, or similar).
              - Uniform button color: **#004aad** with white text.
              - Proper padding and margin for all elements to ensure readability and structure.
            2. Content formatting rules:
              - Show all accounts and transactions in a **responsive table** with checkbox for selection.
              - while displaying transaction is fee is already refunded make sure corrsponding check-box is disabled and can not be selected
              - while displaying transactions for multiple account, display multiple table for each account  
              - If the response is **plain text**, wrap it in a visually styled `<div>`.
              - If the response is a **list**, use a semantic `<ul>` with appropriate spacing.
              - If the response is a **table**, structure it with `<table>`, including headers and rows styled for readability.
              - If user input or selection is required, use only **non-text inputs** like checkboxes, radio buttons, or dropdowns. Avoid text inputs.
              - If user input or selection is required add small heading on top asking use to select accounts or transactions.
              - If no input is required, do not include any `<script>` tags.
            3. User interaction:
              - When user input is involved, include a `<script>` that listens for changes or button clicks.
              - On interaction, send a message using `window.parent.postMessage(...)` with the format:
                  ```js
                  { type: 'proceed', data: '...summary of selected input...' }
                  ```
              - Examples:
                  - If a dropdown is used to choose an account: `data: 'proceed with account 12345'`.
                  - For checkboxes: `data: 'proceed with these transaction IDs: T1, T2'`.
            4. Include CSS using either a `<style>` block in the `<head>` or inline styles if minimal.
            5: Do not add any explanation it should return pure html page 
            Goal:
              Produce a clean, styled, responsive HTML snippet suitable for embedding in a modern web UI, with visually consistent design and user-friendly interaction when needed.
        """
      )
    )
    human_msg = HumanMessage(content=f"Convert the following response into user-friendly HTML:\n\n{backend_response}")
    
    response = llm([system_msg, human_msg])
    cleaned_html = strip_code_fence(response.content)
    return cleaned_html
