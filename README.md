# Xero AI Agent

An interactive CLI agent that connects to your Xero account using Claude AI and the [xero-mcp](https://github.com/john-zhang-dev/xero-mcp) MCP server. Ask questions and perform accounting actions in plain English.

## Prerequisites

- Python 3.10+
- Node.js (for `npx` to run the Xero MCP server)
- An [Anthropic API key](https://console.anthropic.com/)
- A Xero account with API access

## Setup

### 1. Clone and install dependencies

```bash
git clone <your-repo-url>
cd xero
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Create a Xero app

1. Go to [developer.xero.com/app/manage](https://developer.xero.com/app/manage) and create a new app
2. Set the **Redirect URI** to `http://localhost:5000/callback`
3. Note your **Client ID** and **Client Secret**

### 3. Configure credentials

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
XERO_CLIENT_ID=your_client_id_here
XERO_CLIENT_SECRET=your_client_secret_here
XERO_REDIRECT_URI=http://localhost:5000/callback
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### 4. Run the agent

```bash
python agent.py
```

On first run, a browser window will open for Xero OAuth authentication. After authorising, the agent starts an interactive session.

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
| Contacts | `Create a contact for Acme Corp, email hello@acme.com` |
| Reports | `Show the profit and loss for this month` |
| Reports | `What does the balance sheet look like?` |
| Bank | `List bank transactions from last week` |
| Payments | `Show all payments received this quarter` |

## Available Xero tools

The agent has access to the following Xero operations via MCP:

| Tool | Description |
|---|---|
| `authenticate` | Initiate Xero OAuth flow |
| `list_invoices` | List and filter invoices |
| `get_invoice` | Fetch a single invoice by ID |
| `update_invoice` | Update an existing invoice |
| `list_contacts` | List contacts (customers/suppliers) |
| `create_contacts` | Create new contacts |
| `list_accounts` | List chart of accounts |
| `list_bank_transactions` | List bank transactions |
| `create_bank_transactions` | Create bank transactions |
| `update_bank_transaction` | Update a bank transaction |
| `list_payments` | List payments |
| `list_quotes` | List quotes |
| `list_journals` | List journal entries |
| `list_organisations` | List connected organisations |
| `get_balance_sheet` | Fetch the balance sheet report |
| `list_profit_and_loss` (via official server) | P&L report |

## Project structure

```
xero/
├── agent.py          # Main agent — interactive CLI loop
├── requirements.txt  # Python dependencies
├── .env.example      # Credential template
├── .env              # Your credentials (git-ignored)
└── README.md
```

## MCP server options

This project uses [`xero-mcp`](https://github.com/john-zhang-dev/xero-mcp) which supports both read and write operations via standard Xero OAuth.

If you only need **read access**, you can switch to the official [`@xeroapi/xero-mcp-server`](https://github.com/XeroAPI/xero-mcp-server) which uses Xero Custom Connections (no redirect URI required). Update the `build_mcp_config()` function in `agent.py`:

```python
return {
    "command": "npx",
    "args": ["-y", "@xeroapi/xero-mcp-server@latest"],
    "env": {
        "XERO_CLIENT_ID": client_id,
        "XERO_CLIENT_SECRET": client_secret,
    },
}
```

## Notes

- For Xero apps created after 2 March 2026, use `xero-mcp@beta` instead of `xero-mcp@latest` (due to Xero's granular scope migration). The two tags will merge by end of April 2026.
- The agent uses `claude-opus-4-6` by default via the Claude Agent SDK.
- OAuth tokens are cached locally by `xero-mcp` so you won't need to re-authenticate on every run.
