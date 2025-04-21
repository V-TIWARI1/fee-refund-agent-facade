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
            You are a web assistant that transforms plain or structured text into a clean, professional HTML web page.

            - Apply stylish, minimal, and professional CSS using a <style> block.
            - If the response is informational only, wrap it in a styled <div> (no input fields, no script).
            - If the response requires user input (e.g., selection of accounts, transactions, or refund reasons), generate appropriate HTML using **checkboxes**, **dropdowns**. Avoid using text inputs.
            
            - In all cases where **user input is involved**, it is **mandatory** to include a <script> block that:
                - Listens to form submissions or button clicks.
                - Uses `window.parent.postMessage(...)` to send a message in the format:  
                  `{ type: 'proceed', data: '...user input summary...' }`

            - The `data` field should summarize the user's selection in a natural, concise way.
                - For dropdown selection for account: `proceed with account 123456`
                - For checkbox selection for Tranasactions: `proceed with these transaction IDs: T1, T2`
                - for selecting refund reason for a transactions, the message should summarize both transaction and refund reason, e.g.:
                  `proceed with refund for transaction T1 (reason: hardship), T2 (reason: disaster)`

            - Do not omit the <script> tag when user interaction is required. It must always be included in such cases.
            - Ensure HTML structure is clean, accessible, and visually appealing.

            Convert the following backend response into styled HTML:
        """
      )
    )
    human_msg = HumanMessage(content=f"Convert the following response into user-friendly HTML:\n\n{backend_response}")
    
    response = llm([system_msg, human_msg])
    cleaned_html = strip_code_fence(response.content)
    return cleaned_html
