# 🎵 IgniteVibes - Azure Cosmos DB Demo Application

A complete demonstration of Azure Cosmos DB development featuring a Python console application for managing "vibes" data, with Azure Cosmos DB vNext Docker emulator setup and best practices implementation.

## 🚀 Quick Start

**For complete setup instructions, see [SETUP.md](./SETUP.md)**

```bash
# 1. Start Cosmos DB Emulator
./start-cosmos-emulator.sh

# 2. Set up Python environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows
# source .venv/bin/activate    # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python vibes_manager.py
```

## 🎯 Key Features

- **🎵 Interactive Console**: Rich-formatted user interface with colorful tables and panels
- **🗃️ Full CRUD Operations**: Add, remove, and list vibes with comprehensive validation
- **� Smart Delete Interface**: Select vibes by number instead of copying UUIDs
- **�🐳 Docker Emulator**: Azure Cosmos DB vNext emulator with automated setup scripts
- **🔒 Security Best Practices**: Environment-based configuration and SSL support
- **📊 Data Explorer**: Web interface for database management at http://localhost:1234
- **🛡️ Robust Error Handling**: Comprehensive error handling with user-friendly feedback
- **⚡ Context Management**: Proper resource cleanup and connection management
- **🎨 Rich UI Components**: Beautiful tables, panels, and interactive prompts

## 📋 Prerequisites

- Docker Desktop
- Python 3.7 or later
- WSL2 (Windows users recommended)

## �️ Installation & Setup

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd ignitevibes
```

### 2. Start Cosmos DB Emulator
```bash
# Using the provided script (Linux/WSL)
./start-cosmos-emulator.sh

# Or manually with Docker
docker run --detach --publish 8081:8081 --publish 1234:1234 \
  mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator:vnext-preview \
  --protocol https
```

### 3. Set Up Python Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1  # Windows PowerShell
# source .venv/bin/activate     # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure Environment
Copy the example environment file and adjust if needed:
```bash
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac
```

### 5. Run the Application
```bash
python vibes_manager.py
```

## 🎮 Application Usage

The application provides an interactive menu with enhanced user experience:

### 1. 📝 Add a New Vibe

- Enter a title for your vibe
- Add a description (optional)
- Specify a category (defaults to "general")
- Automatic UUID generation and timestamp tracking

### 2. 🗑️ Remove a Vibe (Enhanced Interface)

- **Numbered Selection**: View all vibes with simple numbers (1, 2, 3...)
- **Detailed Preview**: See full vibe details before deletion
- **Interactive Scrolling**: Easy navigation through your vibe collection
- **Confirmation Dialog**: Double-check before permanent deletion
- **No More UUID Copying**: User-friendly alternative to copying long IDs

Example deletion flow:
```
🗑️ Select a vibe to remove (12 total):

Available vibes:
  1. Coffee Time [general] (01/15/25)
  2. Beach Sunset [nature] (01/14/25)
  3. Coding Flow [productivity] (01/13/25)
  ...
  cancel. Go back to main menu

Enter the number of the vibe to remove: 2

� Selected vibe details:
Title:       Beach Sunset
Description: Relaxing evening by the ocean
Category:    nature
ID:          a1b2c3d4-e5f6-7890-abcd-ef1234567890
Created:     2025-01-14T18:30:00.123456

⚠️ Are you sure you want to permanently delete 'Beach Sunset'? (y/N):
```

### 3. 📋 List All Vibes

- View all vibes in a beautifully formatted table
- Shows ID (truncated), title, description, category, and creation date
- Automatic description truncation for readability
- Total count display

### 4. ❌ Exit

- Graceful application termination
- Automatic resource cleanup

## 📁 Project Structure

```
ignitevibes/
├── 🐍 vibes_manager.py          # Main Python console application
├── 🐳 start-cosmos-emulator.sh  # Cosmos DB emulator management script
├── ⚙️  .env                     # Environment configuration
├── ⚙️  .env.example             # Environment configuration template
├── 📋 requirements.txt          # Python dependencies
├── 🐧 setup_vibes.sh           # Linux/WSL setup automation
├── 📚 SETUP.md                 # Complete GitHub setup instructions
├── 📖 README.md                # This file (project overview)
├── 📊 PROJECT_SUMMARY.md       # Detailed project breakdown
└── .github/
    └── 📝 copilot-instructions.md  # GitHub Copilot context
```

## ✨ Recent Enhancements

### Enhanced Delete Interface (v2.0)
- **User-Friendly Selection**: No more copying UUIDs! Select vibes by simple numbers (1, 2, 3...)
- **Interactive Preview**: See full vibe details before confirming deletion
- **Improved UX**: Scroll through your vibes with ease and confidence
- **Smart Formatting**: Dates, categories, and descriptions beautifully formatted
- **Safety First**: Double confirmation prevents accidental deletions

### Improved Error Handling
- **Comprehensive Exception Handling**: Specific handling for Azure Cosmos DB errors
- **User-Friendly Messages**: Clear, actionable error messages with helpful suggestions
- **Graceful Degradation**: Application continues running even when individual operations fail
- **Connection Validation**: Automatic retry logic and connection health checks

### Enhanced Console Interface
- **Rich UI Components**: Beautiful tables, panels, and interactive prompts
- **Color-Coded Output**: Status indicators with colors and emojis for better visibility
- **Responsive Design**: Adapts to terminal width and content length
- **Professional Formatting**: Consistent styling throughout the application

## 🔧 Configuration Options

You can customize the application by modifying the `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `COSMOS_ENDPOINT` | Cosmos DB endpoint URL | `https://localhost:8081` |
| `COSMOS_KEY` | Account key for authentication | (emulator default key) |
| `COSMOS_DATABASE_NAME` | Database name | `vibes` |
| `COSMOS_CONTAINER_NAME` | Container name | `items` |
| `DISABLE_SSL_VERIFICATION` | Disable SSL for local emulator | `true` |

## 🏗️ Architecture & Best Practices

This application follows Azure best practices:

### Security
- ✅ Uses environment variables for configuration
- ✅ Supports SSL/TLS connections
- ✅ Handles SSL verification for local development
- ✅ No hardcoded credentials in source code

### Error Handling
- ✅ Comprehensive exception handling
- ✅ Specific Cosmos DB error handling
- ✅ User-friendly error messages
- ✅ Graceful degradation

### Performance
- ✅ Connection pooling (handled by SDK)
- ✅ Proper resource cleanup
- ✅ Context manager pattern
- ✅ Efficient querying with SQL

### Code Quality
- ✅ Type hints for better maintainability
- ✅ Docstrings for all functions and classes
- ✅ Separation of concerns
- ✅ Rich console interface for better UX

## 🗃️ Database Schema

Vibe items are stored with the following structure:

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

## 🚨 Troubleshooting

### Connection Issues
- Ensure Cosmos DB emulator is running on port 8081
- Check if the Data Explorer is accessible at http://localhost:1234
- Verify the `.env` file has correct connection details

### SSL Certificate Issues
- For local emulator, ensure `DISABLE_SSL_VERIFICATION=true`
- For production, download and install the emulator certificate

### Package Installation Issues
- Make sure you're using Python 3.7 or later
- Try upgrading pip: `python -m pip install --upgrade pip`
- Use a virtual environment to avoid conflicts

## 📖 References

- [Azure Cosmos DB Python SDK Documentation](https://docs.microsoft.com/en-us/azure/cosmos-db/sql/sql-api-python-application)
- [Azure Cosmos DB Emulator](https://docs.microsoft.com/en-us/azure/cosmos-db/emulator-linux)
- [Rich Python Library](https://rich.readthedocs.io/)

## 🤝 Contributing & Extending

This is a demonstration application showcasing Azure Cosmos DB best practices. Feel free to extend it with additional features:

### Suggested Enhancements
- **Search Functionality**: Add text search across vibe titles and descriptions
- **Bulk Operations**: Implement bulk delete or bulk import capabilities
- **Category Management**: Create a category management system with predefined options
- **Data Export/Import**: Add JSON/CSV export and import functionality
- **Vibe Analytics**: Display statistics about your vibe collection
- **Backup/Restore**: Implement backup and restore functionality
- **Web Interface**: Create a web-based interface using Flask or FastAPI
- **Mobile App**: Build a mobile companion app
- **Advanced Filtering**: Add date range, category, and keyword filtering
- **Tagging System**: Implement a flexible tagging system for vibes

### Development Best Practices
- Follow the existing code patterns and type hints
- Maintain comprehensive error handling
- Use the Rich library for consistent UI formatting
- Add proper docstrings for new functions
- Test with both the local emulator and Azure Cosmos DB
- Update this README when adding new features

### Testing Your Changes
```bash
# Lint your Python code
python -m py_compile vibes_manager.py

# Test with the emulator
./start-cosmos-emulator.sh
python vibes_manager.py

# Test error handling
# (Stop the emulator and test connection failures)
```

## 📄 License

This project is provided as an educational example following Azure best practices.
