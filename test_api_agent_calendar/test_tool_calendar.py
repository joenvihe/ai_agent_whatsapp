# Example: Configuring Google Calendar Tools
from google.adk.tools.google_api_tool import calendar_tool_set
# --- Cargar .env (recomendado para client_id y client_secret) ---
from dotenv import load_dotenv
import os

load_dotenv()
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]

client_id = CLIENT_ID
client_secret = CLIENT_SECRET

calendar_tools = calendar_tool_set.get_tools()
for tool in calendar_tools:
    # Use the specific configure method for this tool type
    print(tool)
    tool.configure_auth(client_id=client_id, client_secret=client_secret)

# agent = LlmAgent(..., tools=calendar_tools)