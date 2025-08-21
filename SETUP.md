# 🎵 IgniteVibes - Azure Cosmos DB Demo Application

A complete demonstration of Azure Cosmos DB development featuring:
- **Azure Cosmos DB vNext Docker Emulator** setup and management
- **Python Console Application** for managing "vibes" data
- **Best Practices** implementation for Azure development

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Docker Desktop** - [Download here](https://www.docker.com/products/docker-desktop/)
- **Python 3.7+** - [Download here](https://www.python.org/downloads/)
- **Git** - [Download here](https://git-scm.com/downloads)
- **WSL2** (Windows users) - [Installation guide](https://docs.microsoft.com/en-us/windows/wsl/install)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/jaydestro/ignitevibes.git
cd ignitevibes
```

### 2. Start Azure Cosmos DB Emulator

#### Option A: Using the Provided Script (Recommended)

```bash
# Make the script executable (Linux/WSL)
chmod +x start-cosmos-emulator.sh

# Start the emulator
./start-cosmos-emulator.sh
```

#### Option B: Manual Docker Command

```bash
docker run --detach \
    --name cosmos-emulator-vnext \
    --publish 8081:8081 \
    --publish 1234:1234 \
    mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator:vnext-preview \
    --protocol https
```

### 3. Set Up Python Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Linux/WSL/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Run the Vibes Manager Application

```bash
python vibes_manager.py
```

## 🔧 Detailed Setup Instructions

### Azure Cosmos DB Emulator Setup

The Azure Cosmos DB vNext emulator runs in Docker and provides a local development environment.

#### Connection Information

Once started, the emulator provides:

- **Cosmos DB Endpoint**: `https://localhost:8081`
- **Data Explorer**: `http://localhost:1234`
- **Default Account Key**: `C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==`

#### Emulator Management Commands

```bash
# Start the emulator
./start-cosmos-emulator.sh

# Stop the emulator
./start-cosmos-emulator.sh stop

# Remove the emulator container
./start-cosmos-emulator.sh remove

# Check emulator status
./start-cosmos-emulator.sh status

# View emulator logs
./start-cosmos-emulator.sh logs

# Download SSL certificate (for Java SDK)
./start-cosmos-emulator.sh cert
```

#### Accessing Data Explorer

Open your web browser and navigate to: `http://localhost:1234`

The Data Explorer provides a web interface to:
- Browse databases and containers
- Run queries
- Manage data
- Monitor performance

### Python Application Setup

#### Environment Configuration

The application uses a `.env` file for configuration:

```env
# Cosmos DB Configuration
COSMOS_ENDPOINT=https://localhost:8081
COSMOS_KEY=C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==
COSMOS_DATABASE_NAME=vibes
COSMOS_CONTAINER_NAME=items

# SSL Configuration for local emulator
DISABLE_SSL_VERIFICATION=true
```

#### Dependencies

The application requires these Python packages:

```txt
azure-cosmos>=4.5.1    # Azure Cosmos DB SDK
rich>=13.0.0           # Rich console interface
python-dotenv>=1.0.0   # Environment variable management
```

#### Application Features

The **Vibes Manager** console application provides:

1. **📝 Add New Vibes**: Create vibe items with title, description, and category
2. **🗑️ Remove Vibes**: Delete existing vibes by ID
3. **📋 List All Vibes**: View all vibes in a formatted table
4. **❌ Exit**: Safely close the application

#### Sample Usage

```bash
$ python vibes_manager.py

🎵 Welcome to the Vibes Manager! 🎵

This console application allows you to manage your vibes in Azure Cosmos DB.
You can add new vibes, remove existing ones, and view your entire collection.

🔌 Connecting to Cosmos DB...
✅ Successfully connected to Cosmos DB
📊 Database: vibes
📦 Container: items

==================================================
╭───── Main Menu ──────╮
│                      │
│ 1. 📝 Add a new vibe │
│ 2. 🗑️  Remove a vibe  │
│ 3. 📋 List all vibes │
│ 4. ❌ Exit           │
│                      │
╰──────────────────────╯

What would you like to do? [1/2/3/4] (3):
```

## 📁 Project Structure

```
ignitevibes/
├── 📄 README.md                 # This file
├── 📄 SETUP.md                  # GitHub setup instructions
├── 🐍 vibes_manager.py          # Main Python application
├── 📋 requirements.txt          # Python dependencies
├── ⚙️ .env                      # Environment configuration
├── 🐧 start-cosmos-emulator.sh  # Emulator startup script
├── 🐧 setup_vibes.sh           # Linux/WSL setup script
└── 🗂️ .venv/                   # Python virtual environment
```

## 🛠️ Platform-Specific Instructions

### Windows Users

#### Using PowerShell

```powershell
# Clone repository
git clone https://github.com/jaydestro/ignitevibes.git
cd ignitevibes

# Start Cosmos DB emulator using WSL
wsl bash -c "./start-cosmos-emulator.sh"

# Set up Python environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Run the application
python vibes_manager.py
```

#### Using WSL (Recommended)

```bash
# In WSL terminal
git clone https://github.com/jaydestro/ignitevibes.git
cd ignitevibes

# Start emulator
chmod +x start-cosmos-emulator.sh
./start-cosmos-emulator.sh

# Set up Python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run application
python vibes_manager.py
```

### Linux/macOS Users

```bash
# Clone repository
git clone https://github.com/jaydestro/ignitevibes.git
cd ignitevibes

# Use the automated setup script
chmod +x setup_vibes.sh
./setup_vibes.sh
```

## 🔍 Troubleshooting

### Common Issues and Solutions

#### Cosmos DB Emulator Won't Start

**Problem**: Container fails to start or stops unexpectedly

**Solutions**:
1. Check if Docker is running: `docker info`
2. Ensure ports 8081 and 1234 are available
3. Remove existing container: `./start-cosmos-emulator.sh remove`
4. Pull latest image: `docker pull mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator:vnext-preview`

#### Connection Refused Errors

**Problem**: Python app can't connect to Cosmos DB

**Solutions**:
1. Verify emulator is running: `docker ps`
2. Check Data Explorer: `http://localhost:1234`
3. Confirm environment variables in `.env` file
4. Wait 1-2 minutes for emulator to fully start

#### SSL/Certificate Issues

**Problem**: SSL verification errors

**Solutions**:
1. Ensure `DISABLE_SSL_VERIFICATION=true` in `.env`
2. For production, download certificate: `./start-cosmos-emulator.sh cert`
3. For Java SDK, import certificate to keystore

#### Python Package Installation Issues

**Problem**: pip install fails

**Solutions**:
1. Upgrade pip: `python -m pip install --upgrade pip`
2. Use virtual environment: `python -m venv .venv`
3. Check Python version: `python --version` (requires 3.7+)

### Verification Steps

#### 1. Verify Emulator Status

```bash
# Check container status
docker ps --filter name=cosmos-emulator-vnext

# Test Data Explorer
curl -s http://localhost:1234 | grep -q "Cosmos" && echo "✅ Data Explorer OK" || echo "❌ Data Explorer Failed"

# Test Cosmos endpoint (may take time to start)
curl -k -s https://localhost:8081/_explorer/emulator.pem > /dev/null && echo "✅ Cosmos Endpoint OK" || echo "⏳ Cosmos Endpoint Starting"
```

#### 2. Verify Python Environment

```bash
# Check Python version
python --version

# Check installed packages
pip list | grep -E "(azure-cosmos|rich|python-dotenv)"

# Test import
python -c "from azure.cosmos import CosmosClient; print('✅ Azure Cosmos SDK OK')"
```

## 📊 Features and Capabilities

### Azure Cosmos DB Emulator Features

- **NoSQL API Support**: Full compatibility with Azure Cosmos DB NoSQL API
- **Local Development**: No Azure subscription required
- **Data Explorer**: Web-based interface for data management
- **HTTPS Support**: SSL/TLS encryption for secure connections
- **Docker-based**: Consistent environment across platforms

### Python Application Features

- **Interactive Console**: Rich-formatted user interface
- **CRUD Operations**: Complete Create, Read, Update, Delete functionality
- **Error Handling**: Comprehensive error handling and user feedback
- **Configuration Management**: Environment-based configuration
- **Type Safety**: Full type hints for maintainability
- **Best Practices**: Following Azure SDK best practices

### Database Schema

Vibe items are stored with the following structure:

```json
{
  "id": "uuid-string",
  "title": "My Awesome Vibe",
  "description": "A detailed description of the vibe",
  "category": "music",
  "created_at": "2025-08-21T21:22:00.000Z",
  "updated_at": "2025-08-21T21:22:00.000Z",
  "type": "vibe"
}
```

## 🔒 Security Considerations

### Local Development

- Uses emulator's default key (safe for local development)
- SSL verification disabled for local emulator
- No sensitive data in source code

### Production Deployment

For production use:
1. Use Azure Cosmos DB service (not emulator)
2. Store credentials in Azure Key Vault
3. Enable SSL verification
4. Use Managed Identity when possible
5. Implement proper RBAC

## 📚 Additional Resources

### Documentation

- [Azure Cosmos DB Documentation](https://docs.microsoft.com/en-us/azure/cosmos-db/)
- [Azure Cosmos DB Python SDK](https://docs.microsoft.com/en-us/azure/cosmos-db/sql/sql-api-python-application)
- [Azure Cosmos DB Emulator](https://docs.microsoft.com/en-us/azure/cosmos-db/emulator-linux)
- [Rich Python Library](https://rich.readthedocs.io/)

### Azure Best Practices

- [Azure Cosmos DB Best Practices](https://docs.microsoft.com/en-us/azure/cosmos-db/sql/best-practice-python)
- [Azure SDK for Python Guidelines](https://azure.github.io/azure-sdk/python_introduction.html)
- [Azure Security Best Practices](https://docs.microsoft.com/en-us/azure/security/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is provided as an educational example demonstrating Azure Cosmos DB development best practices.

## 🎯 Next Steps

After successfully running the application, consider:

1. **Extend the Application**: Add search, categories, or import/export features
2. **Deploy to Azure**: Move from emulator to Azure Cosmos DB service
3. **Add Tests**: Implement unit and integration tests
4. **CI/CD Pipeline**: Set up GitHub Actions for automated testing
5. **Web Interface**: Create a web frontend using Flask or FastAPI
6. **Mobile App**: Build a mobile client using Azure SDKs

---

**Happy coding! 🚀**

For questions or issues, please open a GitHub issue or contact the maintainers.
