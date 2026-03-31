# Xero AI Agent

An interactive CLI agent that connects to your Xero account using Claude AI and the official [xero-mcp-server](https://github.com/XeroAPI/xero-mcp-server) by Xero. Ask questions about your accounting data in plain English.

## Prerequisites

- Python 3.10+
- Node.js (for `npx` to run the Xero MCP server)
- An [Anthropic API key](https://console.anthropic.com/)
- A Xero account with a **Custom Connection** (see setup below)

## Setup

### 1. Clone and install dependencies

```bash
git clone <your-repo-url>
cd xero
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Create a Xero Custom Connection

The official Xero MCP server uses [Custom Connections](https://developer.xero.com/documentation/guides/oauth2/custom-connections/) rather than standard OAuth. Custom Connections are machine-to-machine credentials that don't require a browser-based auth flow.

1. Go to [developer.xero.com/app/manage](https://developer.xero.com/app/manage) and create a new app
2. Select **Custom Connection** as the integration type
3. Grant the scopes your agent needs (e.g. `accounting.transactions.read`, `accounting.contacts.read`, etc.)
4. Note your **Client ID** and **Client Secret**

### 3. Configure credentials

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
XERO_CLIENT_ID=your_client_id_here
XERO_CLIENT_SECRET=your_client_secret_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### 4. Run the agent

```bash
python agent.py
```

## Usage

```
Xero AI Agent
=============
Connected to your Xero account via Claude + MCP.
Type your request, or 'quit' to exit.

You: List all unpaid invoices
Agent: Here are your unpaid invoices...

You: Show me the balance sheet
Agent: ...

You: quit
```

### Example prompts

| Category | Example |
|---|---|
| Invoices | `List all overdue invoices` |
| Invoices | `Show invoice INV-0042` |
| Contacts | `Find contacts named Acme` |
| Reports | `Show the profit and loss for this month` |
| Reports | `What does the balance sheet look like?` |
| Reports | `Show me the trial balance` |
| Bank | `List bank transactions from last week` |
| Payments | `Show all payments received this quarter` |

## Available Xero tools

The agent has access to the following operations via the official Xero MCP server:

| Tool | Description |
|---|---|
| `list-invoices` | List and filter invoices |
| `list-contacts` | List contacts (customers/suppliers) |
| `list-accounts` | List chart of accounts |
| `list-payments` | List payments |
| `list-bank-transactions` | List bank transactions |
| `list-quotes` | List quotes |
| `list-purchase-orders` | List purchase orders |
| `list-profit-and-loss` | Profit & loss report |
| `list-balance-sheet` | Balance sheet report |
| `list-trial-balance` | Trial balance report |
| `list-organisations` | List connected organisations |

> **Note:** The official Xero MCP server is read-only. It does not support creating or updating records.

## Project structure

```
xero/
├── agent.py          # Main agent — interactive CLI loop
├── requirements.txt  # Python dependencies
├── .env.example      # Credential template
├── .env              # Your credentials (git-ignored)
└── README.md
```

## Notes

- The agent uses `claude-opus-4-6` by default via the Claude Agent SDK.
- Custom Connections authenticate automatically using client credentials — no browser login required.
- For a full list of available scopes, see the [Xero OAuth 2.0 scopes reference](https://developer.xero.com/documentation/guides/oauth2/scopes/).
