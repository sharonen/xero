"""
Xero AI Agent
=============
An interactive agent that connects to your Xero account via MCP
and uses Claude to perform accounting actions.

Setup:
  1. cp .env.example .env  and fill in your credentials
  2. pip install -r requirements.txt
  3. python agent.py

The agent uses the official Xero MCP server
(https://github.com/XeroAPI/xero-mcp-server).
It requires a Xero Custom Connection — set one up at:
https://developer.xero.com/documentation/guides/oauth2/custom-connections/
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
- Listing invoices, quotes, payments, and purchase orders
- Managing contacts (customers and suppliers)
- Viewing bank transactions and account balances
- Financial reports: balance sheet, profit & loss, trial balance
- Listing accounts, journals, and organisations
- Payroll information

Guidelines:
- Be precise with amounts, dates, and account codes
- When listing items, present them clearly in a table or structured format
- If a request is ambiguous, ask for clarification before proceeding
"""


def build_mcp_config() -> dict:
    client_id = os.getenv("XERO_CLIENT_ID")
    client_secret = os.getenv("XERO_CLIENT_SECRET")

    if not client_id or not client_secret:
        print(
            "Warning: XERO_CLIENT_ID and XERO_CLIENT_SECRET are not set.\n"
            "Copy .env.example to .env and fill in your Xero Custom Connection credentials.\n"
            "See: https://developer.xero.com/documentation/guides/oauth2/custom-connections/\n"
        )

    return {
        "command": "npx",
        "args": ["-y", "@xeroapi/xero-mcp-server@latest"],
        "env": {
            "XERO_CLIENT_ID": client_id or "",
            "XERO_CLIENT_SECRET": client_secret or "",
        },
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
    print("  - Show me the profit and loss report")
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
