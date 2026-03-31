"""
Xero AI Agent
=============
An interactive agent that connects to your Xero account via MCP
and uses Claude to perform accounting actions.

Setup:
  1. cp .env.example .env  and fill in your credentials
  2. pip install -r requirements.txt
  3. python agent.py

The agent uses xero-mcp (https://github.com/john-zhang-dev/xero-mcp).
On first run it will open a browser for Xero OAuth authentication.
"""

import anyio
import os
import sys

from dotenv import load_dotenv
from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AssistantMessage,
    ResultMessage,
    TextBlock,
)

load_dotenv()

SYSTEM_PROMPT = """You are a helpful Xero accounting assistant. You have access to the
user's Xero account via MCP tools.

You can help with:
- Listing and searching invoices, quotes, and payments
- Managing contacts (customers and suppliers)
- Viewing and creating bank transactions
- Financial reports: balance sheet, profit & loss, trial balance
- Listing accounts, journals, and organisations

Guidelines:
- Always confirm details before creating or modifying records
- Be precise with amounts, dates, and account codes
- When listing items, present them clearly in a table or structured format
- If a request is ambiguous, ask for clarification before proceeding
"""


def build_mcp_config() -> dict:
    env = {}

    client_id = os.getenv("XERO_CLIENT_ID")
    client_secret = os.getenv("XERO_CLIENT_SECRET")
    redirect_uri = os.getenv("XERO_REDIRECT_URI", "http://localhost:5000/callback")

    if not client_id or not client_secret:
        print(
            "Warning: XERO_CLIENT_ID and XERO_CLIENT_SECRET are not set.\n"
            "Copy .env.example to .env and fill in your Xero credentials.\n"
        )
    else:
        env["XERO_CLIENT_ID"] = client_id
        env["XERO_CLIENT_SECRET"] = client_secret
        env["XERO_REDIRECT_URI"] = redirect_uri

    return {
        "command": "npx",
        "args": ["-y", "xero-mcp@latest"],
        "env": env,
    }


async def run_agent(prompt: str) -> None:
    options = ClaudeAgentOptions(
        system_prompt=SYSTEM_PROMPT,
        mcp_servers={"xero": build_mcp_config()},
    )

    print("Agent: ", end="", flush=True)

    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text, end="", flush=True)
        elif isinstance(message, ResultMessage):
            print()  # newline after the response


async def main() -> None:
    print("Xero AI Agent")
    print("=============")
    print("Connected to your Xero account via Claude + MCP.")
    print("Type your request, or 'quit' to exit.\n")
    print("Examples:")
    print("  - List all unpaid invoices")
    print("  - Show me the balance sheet")
    print("  - Create a contact for Acme Corp")
    print("  - What bank transactions were posted last week?\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        await run_agent(user_input)


if __name__ == "__main__":
    anyio.run(main)
