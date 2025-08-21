# GitHub Copilot Instructions for IgniteVibes

This file provides context and instructions for GitHub Copilot to better assist with the IgniteVibes project - an Azure Cosmos DB demonstration application.

## Project Overview

**IgniteVibes** is a comprehensive Azure Cosmos DB demo application featuring:
- Azure Cosmos DB vNext Docker emulator setup and management
- Python console application for enhanced CRUD operations on "vibes" data
- Interactive numbered selection interface for user-friendly vibe management
- Rich console UI with colorful tables, panels, and interactive prompts
- Best practices implementation for Azure development

## Project Structure

```
ignitevibes/
├── 🐍 vibes_manager.py          # Main Python console application
├── 🐳 start-cosmos-emulator.sh  # Cosmos DB emulator management script
├── ⚙️  .env                     # Environment configuration
├── ⚙️  .env.example             # Environment configuration template
├── 📋 requirements.txt          # Python dependencies
├── 🐧 setup_vibes.sh           # Linux/WSL setup automation
├── 📚 SETUP.md                 # Complete GitHub setup instructions
├── 📖 README.md                # Quick start guide
├── 📊 PROJECT_SUMMARY.md       # Detailed project breakdown
└── .github/
    └── 📝 copilot-instructions.md  # GitHub Copilot context
```

## Technology Stack

### Core Technologies
- **Azure Cosmos DB**: NoSQL document database (vNext emulator)
- **Python 3.7+**: Main application language
- **Docker**: Container runtime for emulator
- **Bash**: Shell scripting for automation

### Python Libraries
- **azure-cosmos**: Official Azure Cosmos DB SDK
- **rich**: Console formatting and UI library
- **python-dotenv**: Environment variable management

### Development Tools
- **WSL2**: Windows Subsystem for Linux (Windows users)
- **Virtual Environment**: Python package isolation

## Key Components

### 1. Azure Cosmos DB Emulator (`start-cosmos-emulator.sh`)
- **Purpose**: Automated Docker-based Cosmos DB emulator management
- **Features**: Start, stop, status, logs, certificate management
- **Configuration**: HTTPS protocol, ports 8081 (Cosmos) and 1234 (Data Explorer)
- **Commands**: 
  - `./start-cosmos-emulator.sh` - Start emulator
  - `./start-cosmos-emulator.sh stop` - Stop emulator
  - `./start-cosmos-emulator.sh status` - Check status

### 2. Python Console Application (`vibes_manager.py`)
- **Purpose**: Interactive CRUD operations for "vibes" data
- **Architecture**: Context manager pattern, rich UI, comprehensive error handling
- **Database**: Uses "vibes" database with "items" container
- **Features**: Add vibes, remove vibes with numbered selection, list vibes, interactive menus
- **User Experience**: Rich console formatting with tables, panels, and smart selection interfaces
- **Enhanced Delete**: Number-based vibe selection instead of UUID copying
- **Error Handling**: Comprehensive exception handling with user-friendly messages

### 3. Configuration (`.env`)
- **Cosmos Endpoint**: `https://localhost:8081`
- **Database Name**: `vibes`
- **Container Name**: `items`
- **SSL Verification**: Disabled for local emulator

## Recent Enhancements (v2.0)

### Enhanced Delete Interface
- **Interactive Number Selection**: Users can select vibes by simple numbers (1, 2, 3...) instead of copying UUIDs
- **Detailed Preview**: Shows complete vibe details before deletion confirmation
- **Smart Formatting**: Displays creation dates, categories, and descriptions in user-friendly format
- **Safe Deletion**: Double confirmation prevents accidental deletions
- **Method**: `select_vibe_for_removal()` provides the enhanced interface

### Rich Console UI Improvements
- **Colorful Tables**: Beautiful formatting with the Rich library
- **Interactive Prompts**: User-friendly input with validation
- **Status Indicators**: Emoji and color-coded feedback for operations
- **Professional Layout**: Consistent styling throughout the application

### Error Handling Enhancements
- **Azure-Specific Exceptions**: Proper handling of `CosmosHttpResponseError` and related exceptions
- **Connection Validation**: Automatic retry logic and health checks
- **User-Friendly Messages**: Clear, actionable error messages with helpful suggestions
- **Graceful Degradation**: Application continues running even when individual operations fail

## Coding Patterns and Best Practices

### Python Code Style
- **Type Hints**: All functions and methods use type annotations
- **Error Handling**: Comprehensive exception handling with user-friendly messages
- **Documentation**: Docstrings for all classes and methods
- **Context Managers**: Proper resource cleanup and connection management
- **Environment Configuration**: No hardcoded credentials

### Azure Best Practices
- **Security**: Environment-based configuration, no hardcoded secrets
- **Connection Management**: Proper SDK usage with connection pooling
- **Error Handling**: Azure-specific exception handling
- **SSL/TLS**: HTTPS enabled for SDK compatibility

### Shell Script Patterns
- **Error Handling**: `set -e` for immediate exit on errors
- **User Feedback**: Colored output with emoji indicators
- **Validation**: Pre-flight checks for Docker, container status
- **Modularity**: Function-based organization

## Database Schema

### Vibe Document Structure
```json
{
  "id": "uuid-string",           // Partition key
  "title": "string",             // Vibe title
  "description": "string",       // Detailed description
  "category": "string",          // Classification
  "created_at": "ISO-8601",      // Creation timestamp
  "updated_at": "ISO-8601",      // Last modification
  "type": "vibe"                 // Document type identifier
}
```

## Common Development Tasks

### Adding New Features to Python App
1. Extend `VibesManager` class with new methods
2. Add corresponding menu options in `main()` function
3. Implement rich console formatting for new features
4. Add proper error handling and validation
5. Update docstrings and type hints
6. Follow the numbered selection pattern for user interactions
7. Use Rich library components for consistent UI styling

### Enhancing User Interface
1. Use Rich library for tables, panels, and prompts
2. Implement numbered selection for user choices
3. Add detailed preview before destructive operations
4. Provide clear confirmation dialogs
5. Use emoji and color coding for status indicators
6. Ensure consistent formatting across all interfaces

### Modifying Emulator Configuration
1. Update variables at top of `start-cosmos-emulator.sh`
2. Modify Docker run command parameters
3. Update connection info display function
4. Test with both Windows and Linux environments

### Database Operations
- Use parameterized queries for security
- Implement proper partition key usage (`/id`)
- Handle `CosmosResourceNotFoundError` for missing items
- Use `create_item()`, `delete_item()`, `query_items()` SDK methods

## Environment-Specific Considerations

### Windows Users
- Use WSL2 for bash script execution
- PowerShell for Python virtual environment activation
- Docker Desktop required for container support

### Linux/macOS Users
- Native bash script support
- Standard Python virtual environment workflow
- Docker Engine or Docker Desktop

## Testing and Validation

### Cosmos DB Emulator Health Checks
```bash
# Check container status
docker ps --filter name=cosmos-emulator-vnext

# Test Data Explorer
curl -s http://localhost:1234 | grep -q "Cosmos"

# Test Cosmos endpoint
curl -k -s https://localhost:8081/_explorer/emulator.pem
```

### Python Application Testing
```python
# Import validation
python -c "from azure.cosmos import CosmosClient; print('SDK OK')"

# Environment validation
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('COSMOS_ENDPOINT'))"

# Syntax validation
python -m py_compile vibes_manager.py

# Interactive testing of enhanced features
python vibes_manager.py
# Test: Add multiple vibes, then use numbered deletion interface
```

### Testing Enhanced Features
```bash
# Test numbered selection interface
# 1. Add several test vibes
# 2. Use option 2 (Remove a vibe)
# 3. Verify numbered list displays correctly
# 4. Test selection by number and preview functionality
# 5. Test cancellation and confirmation flows
```

## Common Issues and Solutions

### Container Permission Issues
- **Problem**: Bind mount permissions on Windows
- **Solution**: Remove persistent storage, use ephemeral containers
- **Code Pattern**: Docker run without `--mount` flag

### SSL Certificate Problems
- **Problem**: SDK SSL verification failures
- **Solution**: Set `DISABLE_SSL_VERIFICATION=true` for emulator
- **Code Pattern**: `connection_verify=not self.disable_ssl` in CosmosClient

### Python Package Conflicts
- **Problem**: Version conflicts or missing packages
- **Solution**: Use virtual environment and pinned versions
- **Code Pattern**: `requirements.txt` with version constraints

## Extension Patterns

### Adding New Document Types
1. Create new document schema with `type` field
2. Add type-specific CRUD operations
3. Update query filters to include document type
4. Extend console menu with new options

### Adding Web Interface
1. Use Flask/FastAPI framework
2. Reuse `VibesManager` class for database operations
3. Convert rich console output to HTML templates
4. Maintain same error handling patterns

### CI/CD Integration
1. Use GitHub Actions for automated testing
2. Start emulator as service container
3. Run Python tests against emulator
4. Generate coverage reports

## Helpful Copilot Prompts

When working on this project, these prompts will be effective:

### Current Functionality
- "Enhance the numbered selection interface for vibe deletion"
- "Add error handling for Azure Cosmos DB operations"
- "Improve the rich console formatting and UI components"
- "Add input validation for vibe creation and editing"
- "Implement bulk operations for vibe management"

### New Feature Development
- "Create a new vibe category management feature"
- "Add search functionality to the vibes application"
- "Implement data export functionality for vibes"
- "Add pagination for large vibe collections"
- "Create a vibe analytics dashboard"
- "Implement vibe tagging system"
- "Add backup and restore functionality"

### Infrastructure and Setup
- "Add logging to the emulator startup script"
- "Create unit tests for the VibesManager class"
- "Implement CI/CD pipeline for automated testing"
- "Add Docker Compose for easier development setup"
- "Create deployment scripts for Azure production environment"

### Code Quality and Maintenance
- "Refactor the console interface for better modularity"
- "Add comprehensive type hints and documentation"
- "Implement configuration validation and environment checks"
- "Create helper utilities for common database operations"

## Code Quality Standards

### Python Standards
- Follow PEP 8 style guidelines
- Use type hints for all function parameters and returns
- Include comprehensive docstrings
- Handle all possible exceptions
- Use context managers for resource management

### Shell Script Standards
- Use `shellcheck` for linting
- Include error handling with proper exit codes
- Provide colored, user-friendly output
- Support both interactive and non-interactive modes
- Include help documentation

### Documentation Standards
- Update README.md for user-facing changes
- Update SETUP.md for installation procedure changes
- Include inline comments for complex logic
- Maintain up-to-date docstrings
- Document configuration options and environment variables

This project demonstrates enterprise-grade Azure development patterns and can serve as a template for similar Azure Cosmos DB applications.
