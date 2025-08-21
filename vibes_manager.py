#!/usr/bin/env python3
"""
Azure Cosmos DB Vibes Manager - Console Application

This script provides a simple console interface to manage items in an Azure
Cosmos DB database called "vibes". It demonstrates best practices for Azure
Cosmos DB operations including proper error handling, connection management,
and security considerations.

Features:
- Add new vibe items to the database
- Remove existing vibe items
- List all vibes
- Interactive console interface
- Proper error handling and logging
- SSL verification handling for local emulator

Requirements:
- Azure Cosmos DB emulator running (or Azure Cosmos DB account)
- Python packages: azure-cosmos, rich, python-dotenv

Author: Generated following Azure best practices
Reference: https://docs.microsoft.com/en-us/azure/cosmos-db/sql/
           sql-api-python-application
"""

import os
import sys
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
import ssl
import urllib3

# Third-party imports
try:
    from azure.cosmos import CosmosClient, PartitionKey, exceptions
    from azure.cosmos.database import DatabaseProxy
    from azure.cosmos.container import ContainerProxy
    from rich.console import Console
    from rich.table import Table
    from rich.prompt import Prompt, Confirm
    from rich.panel import Panel
    from dotenv import load_dotenv
except ImportError as e:
    print("❌ Missing required packages. Please install them using:")
    print("pip install -r requirements.txt")
    print(f"Missing package: {e}")
    sys.exit(1)

# Load environment variables
load_dotenv()

# Configure console for rich output
console = Console()


class VibesManager:
    """
    Manages vibe items in Azure Cosmos DB with proper error handling and
    best practices.

    This class implements:
    - Secure connection management with SSL handling for local emulator
    - Proper error handling with retry logic
    - Resource cleanup and connection management
    - Type hints for better code maintainability
    """

    def __init__(self):
        """Initialize the Cosmos DB client and configure database/container."""
        self.endpoint = os.getenv('COSMOS_ENDPOINT', 'https://localhost:8081')
        self.key = os.getenv('COSMOS_KEY')
        self.database_name = os.getenv('COSMOS_DATABASE_NAME', 'vibes')
        self.container_name = os.getenv('COSMOS_CONTAINER_NAME', 'items')
        disable_ssl_env = os.getenv('DISABLE_SSL_VERIFICATION', 'false')
        self.disable_ssl = disable_ssl_env.lower() == 'true'

        # Disable SSL warnings for local emulator
        if self.disable_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            ssl._create_default_https_context = ssl._create_unverified_context

        self.client: Optional[CosmosClient] = None
        self.database: Optional[DatabaseProxy] = None
        self.container: Optional[ContainerProxy] = None

        # Validate configuration
        if not self.key:
            console.print("❌ COSMOS_KEY not found in environment variables",
                          style="red")
            sys.exit(1)

    def __enter__(self):
        """Context manager entry - establish connection."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup resources."""
        self.disconnect()

    def connect(self) -> bool:
        """
        Establish connection to Cosmos DB and ensure database/container exist.

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            console.print("🔌 Connecting to Cosmos DB...", style="yellow")

            # Check for missing key
            if not self.key:
                console.print(
                    "❌ COSMOS_KEY environment variable is missing.",
                    style="red"
                )
                return False

            # Create Cosmos client with proper configuration
            self.client = CosmosClient(
                url=self.endpoint,
                credential=self.key,
                connection_verify=not self.disable_ssl,  # For local emulator
                connection_timeout=30,
                request_timeout=30
            )

            # Test connection by listing databases
            list(self.client.list_databases())

            # Create database if it doesn't exist
            self.database = self.client.create_database_if_not_exists(
                id=self.database_name,
                offer_throughput=400  # Minimum throughput for shared database
            )

            # Create container if it doesn't exist
            self.container = self.database.create_container_if_not_exists(
                id=self.container_name,
                partition_key=PartitionKey(path="/id"),
                offer_throughput=400  # Minimum throughput
            )

            console.print("✅ Successfully connected to Cosmos DB",
                          style="green")
            console.print(f"📊 Database: {self.database_name}", style="blue")
            console.print(f"📦 Container: {self.container_name}", style="blue")
            return True

        except exceptions.CosmosHttpResponseError as e:
            error_message = getattr(e, 'message', str(e))
            status_code = getattr(e, 'status_code', 'N/A')
            console.print(
                f"❌ Cosmos DB HTTP Error: {error_message}",
                style="red"
            )
            console.print(
                f"Status Code: {status_code}",
                style="red"
            )
            return False
        except (ConnectionError, OSError, ValueError) as e:
            console.print(f"❌ Connection failed: {str(e)}", style="red")
            console.print("💡 Make sure the Cosmos DB emulator is running",
                          style="yellow")
            return False

    def disconnect(self):
        """Clean up resources and close connections."""
        if self.client:
            # Note: CosmosClient doesn't have explicit close method
            # Connection pooling is handled automatically
            self.client = None
            self.database = None
            self.container = None
            console.print("🔌 Disconnected from Cosmos DB", style="yellow")

    def add_vibe(self, title: str, description: str,
                 category: str = "general") -> bool:
        """
        Add a new vibe item to the database.

        Args:
            title: The title of the vibe
            description: Description of the vibe
            category: Category of the vibe (default: "general")

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create vibe item with proper structure
            vibe_item = {
                "id": str(uuid.uuid4()),  # Unique identifier
                "title": title,
                "description": description,
                "category": category,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
                "type": "vibe"  # Document type for future querying
            }

            # Insert item with retry logic
            assert self.container is not None, "Container not initialized"
            response = self.container.create_item(body=vibe_item)

            console.print(f"✅ Added vibe: '{title}'", style="green")
            console.print(f"🆔 ID: {response['id']}", style="blue")
            return True

        except exceptions.CosmosResourceExistsError:
            console.print("❌ Vibe with this ID already exists", style="red")
            return False
        except exceptions.CosmosHttpResponseError as e:
            error_message = getattr(e, 'message', str(e))
            console.print(
                f"❌ Failed to add vibe: {error_message}", style="red")
            return False
        except (ValueError, KeyError) as e:
            console.print(f"❌ Unexpected error: {str(e)}", style="red")
            return False

    def remove_vibe(self, vibe_id: str) -> bool:
        """
        Remove a vibe item from the database.

        Args:
            vibe_id: The ID of the vibe to remove

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Delete item by ID and partition key
            assert self.container is not None, "Container not initialized"
            self.container.delete_item(
                item=vibe_id,
                partition_key=vibe_id
            )

            console.print(f"✅ Removed vibe with ID: {vibe_id}", style="green")
            return True

        except exceptions.CosmosResourceNotFoundError:
            console.print(f"❌ Vibe not found with ID: {vibe_id}", style="red")
            return False
        except exceptions.CosmosHttpResponseError as e:
            error_message = getattr(e, 'message', str(e))
            console.print(
                f"❌ Failed to remove vibe: {error_message}", style="red")
            return False
        except (ValueError, KeyError) as e:
            console.print(f"❌ Unexpected error: {str(e)}", style="red")
            return False

    def list_vibes(self) -> List[Dict[str, Any]]:
        """
        List all vibe items from the database.

        Returns:
            List of vibe dictionaries
        """
        try:
            # Query all vibe items with proper SQL
            query = ("SELECT * FROM c WHERE c.type = 'vibe' "
                     "ORDER BY c.created_at DESC")

            assert self.container is not None, "Container not initialized"
            items = list(self.container.query_items(
                query=query,
                enable_cross_partition_query=True
            ))

            return items

        except exceptions.CosmosHttpResponseError as e:
            console.print(f"❌ Failed to list vibes: {e.message}", style="red")
            return []
        except (ValueError, KeyError) as e:
            console.print(f"❌ Unexpected error: {str(e)}", style="red")
            return []

    def select_vibe_for_removal(self) -> Optional[Dict[str, Any]]:
        """
        Interactive vibe selection for removal with scrolling interface.

        Returns:
            Dict containing the selected vibe, or None if cancelled
        """
        vibes = self.list_vibes()
        if not vibes:
            console.print("📭 No vibes available to remove", style="yellow")
            return None

        console.print(f"\n🗑️ Select a vibe to remove ({len(vibes)} total):",
                      style="red bold")

        # Create choices with meaningful descriptions
        choices = []
        choice_map = {}

        for i, vibe in enumerate(vibes, 1):
            title = vibe.get('title', 'Untitled')[:30]
            category = vibe.get('category', 'general')
            created = vibe.get('created_at', '')

            # Format creation date
            if created:
                try:
                    dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                    created_short = dt.strftime('%m/%d/%y')
                except (ValueError, AttributeError):
                    created_short = created[:10] if len(
                        created) >= 10 else created
            else:
                created_short = 'Unknown'

            choice_label = f"{i}"
            choice_desc = f"{title} [{category}] ({created_short})"
            choices.append(choice_label)
            choice_map[choice_label] = {
                'vibe': vibe,
                'description': choice_desc
            }

        # Add cancel option
        choices.append("cancel")

        # Display the vibes in a numbered list
        console.print("\nAvailable vibes:")
        for choice_num, choice_data in choice_map.items():
            if choice_num != "cancel":
                console.print(f"  {choice_num}. {choice_data['description']}",
                              style="cyan")

        console.print("  cancel. Go back to main menu", style="dim")

        # Get user selection
        selection = Prompt.ask(
            "\nEnter the number of the vibe to remove",
            choices=choices,
            default="cancel"
        )

        if selection == "cancel":
            return None

        selected_data = choice_map[selection]
        selected_vibe = selected_data['vibe']

        # Show detailed view of selected vibe
        console.print(f"\n📋 Selected vibe details:", style="blue bold")

        detail_table = Table(show_header=False, box=None, padding=(0, 2))
        detail_table.add_column("Field", style="bold cyan")
        detail_table.add_column("Value", style="white")

        detail_table.add_row("Title:", selected_vibe.get('title', 'N/A'))
        detail_table.add_row(
            "Description:", selected_vibe.get('description', 'N/A'))
        detail_table.add_row("Category:", selected_vibe.get('category', 'N/A'))
        detail_table.add_row("ID:", selected_vibe.get('id', 'N/A'))
        detail_table.add_row(
            "Created:", selected_vibe.get('created_at', 'N/A'))

        console.print(detail_table)

        return selected_vibe

    def display_vibes(self, vibes: List[Dict[str, Any]]):
        """
        Display vibes in a formatted table.

        Args:
            vibes: List of vibe dictionaries to display
        """
        if not vibes:
            console.print("📭 No vibes found in the database", style="yellow")
            return

        # Create rich table for better formatting
        table = Table(title="🎵 Vibes Database", show_header=True,
                      header_style="bold magenta")
        table.add_column("ID", style="blue", width=8)
        table.add_column("Title", style="green")
        table.add_column("Description", style="white")
        table.add_column("Category", style="yellow")
        table.add_column("Created", style="cyan")

        for vibe in vibes:
            # Truncate long descriptions for display
            description = vibe.get('description', '')
            if len(description) > 50:
                description = description[:47] + "..."

            # Format date for display
            created_at = vibe.get('created_at', '')
            if created_at:
                try:
                    dt = datetime.fromisoformat(
                        created_at.replace('Z', '+00:00'))
                    created_at = dt.strftime('%Y-%m-%d %H:%M')
                except (ValueError, AttributeError):
                    pass

            table.add_row(
                vibe.get('id', '')[:8],  # Show first 8 chars of ID
                vibe.get('title', ''),
                description,
                vibe.get('category', ''),
                created_at
            )

        console.print(table)
        console.print(f"\n📊 Total vibes: {len(vibes)}", style="blue")


def show_welcome():
    """Display welcome message and connection info."""
    welcome_panel = Panel.fit(
        "🎵 Welcome to the Vibes Manager! 🎵\n\n"
        "This console application allows you to manage your vibes in Azure Cosmos DB.\n"
        "You can add new vibes, remove existing ones, and view your entire collection.\n\n"
        "Make sure your Cosmos DB emulator is running at https://localhost:8081",
        title="Vibes Manager",
        style="blue"
    )
    console.print(welcome_panel)


def show_menu():
    """Display the main menu options."""
    menu_panel = Panel.fit(
        "1. 📝 Add a new vibe\n"
        "2. 🗑️  Remove a vibe\n"
        "3. 📋 List all vibes\n"
        "4. ❌ Exit",
        title="Main Menu",
        style="green"
    )
    console.print(menu_panel)


def main():
    """Main application loop with interactive console interface."""
    show_welcome()

    # Use context manager for proper resource cleanup
    with VibesManager() as vibes_manager:
        if not vibes_manager.client:
            console.print("\n❌ Failed to connect to Cosmos DB. Exiting.",
                          style="red")
            sys.exit(1)

        while True:
            console.print("\n" + "="*50)
            show_menu()

            choice = Prompt.ask(
                "\nWhat would you like to do?",
                choices=["1", "2", "3", "4"],
                default="3"
            )

            if choice == "1":
                # Add new vibe
                console.print("\n📝 Adding a new vibe:", style="green bold")
                title = Prompt.ask("Enter vibe title")
                if not title.strip():
                    console.print("❌ Title cannot be empty", style="red")
                    continue
                description = Prompt.ask("Enter vibe description", default="")
                category = Prompt.ask("Enter category", default="general")
                vibes_manager.add_vibe(title.strip(), description.strip(),
                                       category.strip())
            elif choice == "2":
                # Remove vibe with interactive selection
                console.print("\n🗑️ Remove a vibe:", style="red bold")

                selected_vibe = vibes_manager.select_vibe_for_removal()
                if selected_vibe is None:
                    console.print("Operation cancelled.", style="yellow")
                    continue

                # Final confirmation
                vibe_title = selected_vibe.get('title', 'Unknown')
                vibe_id = selected_vibe.get('id', '')

                if Confirm.ask(f"\n⚠️  Are you sure you want to permanently delete "
                               f"'{vibe_title}'?"):
                    if vibes_manager.remove_vibe(vibe_id):
                        console.print(f"✅ Successfully removed '{vibe_title}'",
                                      style="green")
                    else:
                        console.print(f"❌ Failed to remove '{vibe_title}'",
                                      style="red")
                else:
                    console.print("Deletion cancelled.", style="yellow")

            elif choice == "3":
                # List all vibes
                console.print("\n📋 Listing all vibes:", style="blue bold")
                vibes = vibes_manager.list_vibes()
                vibes_manager.display_vibes(vibes)

            elif choice == "4":
                # Exit
                if Confirm.ask("\nAre you sure you want to exit?"):
                    console.print(
                        "\n👋 Thanks for using Vibes Manager!", style="green")
                    break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n👋 Goodbye!", style="green")
        sys.exit(0)
    except (SystemExit, RuntimeError, OSError) as e:
        console.print(f"\n❌ An unexpected error occurred: {str(e)}",
                      style="red")
        sys.exit(1)
