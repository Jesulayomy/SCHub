#!/usr/bin/env bash

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to check if a command was successful
check_status() {
    if [ $? -eq 0 ]; then
        print_message "$GREEN" "✓ Success: $1"
    else
        print_message "$RED" "✗ Error: $1"
        exit 1
    fi
}

# Function to check Python installation
check_python() {
    print_message "$YELLOW" "Checking Python installation..."

    # Check if running on Windows
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        # Check for Python in Windows
        if ! command -v python.exe &> /dev/null && ! command -v python3.exe &> /dev/null; then
            print_message "$RED" "Python is not installed or not in PATH!"
            print_message "$YELLOW" "Please install Python 3.x using one of these methods:"
            echo "1. Download from official website: https://www.python.org/downloads/"
            echo "2. Install from Microsoft Store"
            echo "3. Use Windows Package Manager (if available):"
            echo "   winget install Python.Python.3.10"
            echo
            echo "Important: During installation:"
            echo "- Check 'Add Python to PATH'"
            echo "- Check 'Install pip'"
            exit 1
        fi
    else
        # Check for Python in Unix-like systems
        if ! command -v python3 &> /dev/null; then
            print_message "$RED" "Python is not installed!"
            print_message "$YELLOW" "Please install Python 3.x using your package manager:"
            echo "For Ubuntu/Debian:"
            echo "sudo apt update && sudo apt install python3 python3-pip python3-venv"
            echo
            echo "For Fedora:"
            echo "sudo dnf install python3 python3-pip"
            echo
            echo "For macOS:"
            echo "brew install python3"
            exit 1
        fi
    fi

    # Check Python version
    local python_cmd
    if command -v python3 &> /dev/null; then
        python_cmd="python3"
    elif command -v python &> /dev/null; then
        python_cmd="python"
    else
        print_message "$RED" "No Python command found!"
        exit 1
    fi

    local version
    version=$($python_cmd -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    print_message "$GREEN" "Found Python version $version"
}

# Function to install MySQL if it's not found
# Function to install MySQL if it's not found
install_mysql() {
    print_message "$YELLOW" "Checking if MySQL is installed..."

    # Check if MySQL is already installed
    if ! command -v mysql &> /dev/null; then
        print_message "$RED" "MySQL is not installed. Attempting to install MySQL..."

        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # For Ubuntu/Debian
            if command -v apt-get &> /dev/null; then
                sudo apt update && sudo apt install mysql-server mysql-client -y
            # For Fedora
            elif command -v dnf &> /dev/null; then
                sudo dnf install mysql mysql-server -y
            else
                print_message "$YELLOW" "Could not determine Linux package manager. Please install MySQL manually."
                print_message "$YELLOW" "Visit: https://dev.mysql.com/downloads/mysql/"
                exit 1
            fi

        elif [[ "$OSTYPE" == "darwin"* ]]; then
            # For macOS
            if command -v brew &> /dev/null; then
                brew install mysql
            else
                print_message "$RED" "Homebrew not found. Install Homebrew or MySQL manually."
                print_message "$YELLOW" "Visit: https://dev.mysql.com/downloads/mysql/"
                exit 1
            fi

        elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
            # For Windows
            print_message "$RED" "Automatic installation of MySQL on Windows is unsupported."
            print_message "$YELLOW" "Please install MySQL manually from: https://dev.mysql.com/downloads/installer/"

            exit 1
        else
            print_message "$RED" "Unsupported OS. Please install MySQL manually."
            print_message "$YELLOW" "Visit: https://dev.mysql.com/downloads/mysql/"
            exit 1
        fi

        print_message "$GREEN" "MySQL installation completed."

        # Start MySQL service if installed on Linux or macOS
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            sudo systemctl start mysql
            sudo systemctl enable mysql
        elif [[ "$OSTYPE" == "darwin"* ]]; then
            brew services start mysql
        fi
    else
        print_message "$GREEN" "MySQL is already installed."
    fi
}


# Function to prompt for user input with a default value
prompt_with_default() {
    local prompt=$1
    local default=$2
    read -p "$prompt [$default]: " value
    echo "${value:-$default}"
}

# Function to setup virtual environment
setup_venv() {
    print_message "$YELLOW" "Setting up Python virtual environment..."

    local python_cmd
    if command -v python3 &> /dev/null; then
        python_cmd="python3"
    else
        python_cmd="python"
    fi

    # Create virtual environment
    $python_cmd -m venv .venv || {
        print_message "$RED" "Failed to create virtual environment. Installing venv..."
        if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
            $python_cmd -m pip install virtualenv
            $python_cmd -m virtualenv .venv
        else
            sudo apt-get install python3-venv -y
            $python_cmd -m venv .venv
        fi
    }

    # Activate virtual environment based on OS
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        source .venv/Scripts/activate
    else
        source .venv/bin/activate
    fi

    check_status "Virtual environment creation"
}

# Function to install Python dependencies
install_python_deps() {
    print_message "$YELLOW" "Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r configurations/requirements.txt
    check_status "Python dependencies installation"
}

# Function to setup pre-commit hooks
setup_precommit() {
    print_message "$YELLOW" "Setting up pre-commit hooks..."
    pre-commit install
    check_status "Pre-commit hooks setup"
}

# Function to configure environment variables
configure_env() {
    print_message "$YELLOW" "Configuring environment variables..."

    if [ ! -f ".env" ]; then
        cp configurations/environment .env

        # Prompt for database configuration
        DB_DEV_PASSWORD=$(prompt_with_default "Enter development database password" "schub_dev_pwd")
        DB_TEST_PASSWORD=$(prompt_with_default "Enter test database password" "schub_test_pwd")
        SECRET_KEY=$(openssl rand -hex 32)
        HOST=$(prompt_with_default "Enter host" "127.0.0.1:8000")

        # Update .env file
        sed -i "s/{PASSWORD}/$DB_DEV_PASSWORD/g" .env
        sed -i "s/{TEST_PASSWORD}/$DB_TEST_PASSWORD/g" .env
        sed -i "s/{SECRET_KEY}/$SECRET_KEY/g" .env
        sed -i "s/{HOST}/$HOST/g" .env

        check_status "Environment configuration"
    else
        print_message "$YELLOW" ".env file already exists. Skipping configuration."
    fi
}

# Function to setup MySQL databases
setup_mysql() {
    print_message "$YELLOW" "Setting up MySQL databases..."

    read -sp "Enter MySQL root password: " MYSQL_ROOT_PASSWORD
    echo

    # Setup development database
    mysql -u root -p"$MYSQL_ROOT_PASSWORD" < data/setup_dev_db.sql
    check_status "Development database setup"

    # Setup test database
    mysql -u root -p"$MYSQL_ROOT_PASSWORD" < data/setup_test_db.sql
    check_status "Test database setup"
}

# Function to install Node.js dependencies
install_node_deps() {
    print_message "$YELLOW" "Installing Node.js dependencies..."
    cd schub
    npm install
    check_status "Node.js dependencies installation"
    cd ..
}

# Function to generate and import data
generate_data() {
    print_message "$YELLOW" "Generating and importing data..."
    cd data/
    python3 generate_dump.py
    check_status "Data generation"

    read -sp "Enter MySQL root password to import data: " MYSQL_ROOT_PASSWORD
    echo
    mysql -u root -p"$MYSQL_ROOT_PASSWORD" < dump.sql
    check_status "Data import"
    cd ..
}

# Function to reset development database
reset_dev_db() {
    print_message "$YELLOW" "Resetting development database..."
    read -sp "Enter MySQL root password: " MYSQL_ROOT_PASSWORD
    echo

    # Drop and recreate development database
    mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "DROP DATABASE IF EXISTS schub;"
    mysql -u root -p"$MYSQL_ROOT_PASSWORD" < data/setup_dev_db.sql
    check_status "Development database reset"

    # Regenerate and import fresh data
    cd data/
    python3 generate_dump.py
    mysql -u root -p"$MYSQL_ROOT_PASSWORD" < dump.sql
    check_status "Development data import"
    cd ..
}

# Function to reset test database
reset_test_db() {
    print_message "$YELLOW" "Resetting test database..."
    read -sp "Enter MySQL root password: " MYSQL_ROOT_PASSWORD
    echo

    # Drop and recreate test database
    mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "DROP DATABASE IF EXISTS schub_test_db;"
    mysql -u root -p"$MYSQL_ROOT_PASSWORD" < data/setup_test_db.sql
    check_status "Test database reset"
}

# Function to handle database operations
database_operations() {
    while true; do
        echo
        print_message "$GREEN" "Database Operations Menu:"
        echo "1. Reset development database"
        echo "2. Reset test database"
        echo "3. Reset both databases"
        echo "4. Return to main menu"
        echo
        read -p "Select an option (1-4): " db_choice

        case $db_choice in
            1)
                reset_dev_db
                ;;
            2)
                reset_test_db
                ;;
            3)
                reset_dev_db
                reset_test_db
                ;;
            4)
                return
                ;;
            *)
                print_message "$RED" "Invalid option"
                ;;
        esac
    done
}

# Main installation function
main_installation() {
    print_message "$GREEN" "Starting SCHub installation..."

    # Check Python installation first
    check_python

    # Check and install MySQL if necessary
    install_mysql

    # Clone repository if not already in SCHub directory
    if [[ ! -d ".git" ]]; then
        print_message "$YELLOW" "Cloning SCHub repository..."
        git clone https://github.com/Jesulayomy/SCHub.git
        cd SCHub
        check_status "Repository clone"
    fi

    # Execute installation steps
    setup_venv
    install_python_deps
    setup_precommit
    configure_env
    setup_mysql
    install_node_deps
    generate_data

    print_message "$GREEN" "Installation completed successfully!"
    print_message "$YELLOW" "To start the application:"
    echo "1. Activate virtual environment:"
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        echo "   source .venv/Scripts/activate"
    else
        echo "   source .venv/bin/activate"
    fi
    echo "2. Start Flask server: python3 -m api.app"
    echo "3. In another terminal, start React frontend: cd schub && npm start"
}

# Main menu function
main_menu() {
    while true; do
        echo
        print_message "$GREEN" "SCHub Installation and Management Menu:"
        echo "1. Full installation"
        echo "2. Database operations"
        echo "3. Exit"
        echo
        read -p "Select an option (1-3): " choice

        case $choice in
            1)
                main_installation
                ;;
            2)
                database_operations
                ;;
            3)
                print_message "$GREEN" "Goodbye!"
                exit 0
                ;;
            *)
                print_message "$RED" "Invalid option"
                ;;
        esac
    done
}

# Execute main menu
main_menu
