# IgniteVibes — Azure Cosmos DB Demo (Python)

A compact demo of Azure Cosmos DB development. It includes a Python console app for managing “vibes” data and a local Azure Cosmos DB vNext Docker emulator setup.

## Quick start

See `SETUP.md` for full instructions.

```bash
# 1) Start the Azure Cosmos DB Emulator
./start-cosmos-emulator.sh

# 2) Create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows
# source .venv/bin/activate    # Linux/Mac

# 3) Install dependencies
pip install -r requirements.txt

# 4) Run the app
python vibes_manager.py
```

## Features

- Interactive console UI with tables and prompts
- Full CRUD: add, remove, list
- Number-based delete (no UUID copy/paste)
- Local Azure Cosmos DB vNext emulator with helper scripts
- Environment-based config and optional SSL handling
- Data Explorer at `http://localhost:1234`
- Clear error messages and graceful cleanup

## Prerequisites

- Docker Desktop
- Python 3.7+
- WSL2 recommended for Windows

## Installation and setup

1) Clone the repo
```bash
git clone <repository-url>
cd ignitevibes
```

2) Start the emulator
```bash
# With the provided script (Linux/WSL)
./start-cosmos-emulator.sh

# Or manually
docker run --detach --publish 8081:8081 --publish 1234:1234 \
  mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator:vnext-preview \
  --protocol https
```

3) Create a virtual environment and install dependencies
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows
# source .venv/bin/activate    # Linux/Mac

pip install -r requirements.txt
```

4) Configure environment
```bash
copy .env.example .env  # Windows (cmd)
# cp .env.example .env  # Linux/Mac or PowerShell (Copy-Item)
```

5) Run
```bash
python vibes_manager.py
```

## Usage

- Add a vibe: enter title, optional description, and category (defaults to “general”).
- Remove a vibe: choose by number, review details, confirm deletion.
- List vibes: view a table with truncated IDs, titles, categories, and dates.
- Exit: closes resources cleanly.

## Project structure

```
ignitevibes/
├── vibes_manager.py             # Console app
├── start-cosmos-emulator.sh     # Emulator helper
├── .env / .env.example          # Configuration
├── requirements.txt             # Dependencies
├── setup_vibes.sh               # Linux/WSL setup
├── SETUP.md                     # Full setup guide
├── README.md                    # This overview
├── PROJECT_SUMMARY.md           # Deeper breakdown
└── .github/
    └── copilot-instructions.md  # GitHub Copilot context
```

## Configuration

Update `.env` to customize:

| Variable | Description | Default |
|---|---|---|
| `COSMOS_ENDPOINT` | Emulator endpoint | `https://localhost:8081` |
| `COSMOS_KEY` | Account key | emulator default key |
| `COSMOS_DATABASE_NAME` | Database | `vibes` |
| `COSMOS_CONTAINER_NAME` | Container | `items` |
| `DISABLE_SSL_VERIFICATION` | Disable SSL verification for local dev | `true` |

## Architecture and practices

Security
- Environment variables for configuration
- Supports SSL/TLS; local SSL verification can be disabled for the emulator
- No credentials hardcoded

Error handling
- Specific handling for Azure Cosmos DB errors
- Clear, actionable messages
- App continues when individual operations fail

Performance and code quality
- SDK connection management, context managers, and cleanup
- Simple, efficient queries
- Type hints and docstrings
- Console UI built with Rich

## Database schema

```json
{
  "id": "uuid-string",
  "title": "string",
  "description": "string",
  "category": "string",
  "created_at": "ISO-8601-datetime",
  "updated_at": "ISO-8601-datetime",
  "type": "vibe"
}
```

## Troubleshooting

Connection
- Ensure the emulator is running on `8081`
- Verify Data Explorer at `http://localhost:1234`
- Confirm `.env` values

SSL
- For the emulator, set `DISABLE_SSL_VERIFICATION=true`
- For production, install the emulator certificate

Packages
- Use Python 3.7+ and a virtual environment
- Upgrade pip if needed: `python -m pip install --upgrade pip`

## Tools used

- VS Code (preferred IDE)
- Azure Cosmos DB Linux-based emulator - vNext (preview): https://learn.microsoft.com/azure/cosmos-db/emulator-linux
- Azure Databases VS Code Extension: https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-cosmosdb
- GitHub Copilot Chat VS Code extension (natural-language prompts to produce code): https://github.com/microsoft/vscode-copilot-chat

## License

This project is an educational example that demonstrates Azure Cosmos DB best practices.