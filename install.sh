#!/bin/bash

# =================================================================
#
# Instagram Automation Bot - Smart Installation Script
#
# This script automates the full deployment of the application
# on a fresh Ubuntu server. It is designed to be idempotent and
# resilient to common errors.
#
# =================================================================

# --- Script Configuration & Colors ---
C_RESET=$(tput sgr0)
C_RED=$(tput setaf 1)
C_GREEN=$(tput setaf 2)
C_YELLOW=$(tput setaf 3)
C_BLUE=$(tput setaf 4)
C_CYAN=$(tput setaf 6)

# --- Logging Functions ---
log_info() { echo -e "\n${C_BLUE}INFO:${C_RESET} $1"; }
log_success() { echo -e "${C_GREEN}SUCCESS:${C_RESET} $1"; }
log_warning() { echo -e "${C_YELLOW}WARNING:${C_RESET} $1"; }
log_error() { echo -e "${C_RED}ERROR:${C_RESET} $1"; exit 1; }
log_progress() {
    local percent=$1
    local message=$2
    printf "\r${C_CYAN}PROGRESS: [%-50s] %d%% - %s${C_RESET}" $(printf '#%.0s' {1..$((percent/2))}) $percent "$message"
}

# --- Utility Functions ---
check_if_installed() {
    command -v "$1" &> /dev/null
}

check_port_availability() {
    if ss -tuln | grep -q ":$1 "; then return 1; else return 0; fi
}

prompt_for_reconfirmation() {
    read -p "${C_YELLOW}WARNING:${C_RESET} $1 is already configured. Do you want to re-run this step? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then return 0; else return 1; fi
}

# --- Core Installation Functions ---

get_user_input() {
    log_info "Gathering required information..."

    read -p "Enter your server's public IP address or domain name: " -r SERVER_IP
    [ -z "$SERVER_IP" ] && log_error "Server IP/domain cannot be empty."

    read -p "Enter the username that will run the application (e.g., 'ubuntu'): " -r APP_USER
    [ -z "$APP_USER" ] && log_error "Application user cannot be empty."

    read -s -p "Enter your OpenAI API Key: " -r OPENAI_API_KEY
    echo
    [ -z "$OPENAI_API_KEY" ] && log_error "OpenAI API Key cannot be empty."

    read -p "Enter the desired Python version (e.g., 3.10.12) [default: 3.10.12]: " -r PYTHON_VERSION
    PYTHON_VERSION=${PYTHON_VERSION:-"3.10.12"}

    read -p "Enter the desired port for Nginx (frontend) [default: 80]: " -r NGINX_PORT
    NGINX_PORT=${NGINX_PORT:-"80"}

    log_success "All required information has been gathered."
}

update_or_clone_project() {
    log_info "Cloning or updating the project repository..."
    INSTALL_DIR="/srv/instagram_bot"
    if [ -d "$INSTALL_DIR" ]; then
        log_warning "Project directory already exists at $INSTALL_DIR."
        if prompt_for_reconfirmation "Update the existing project with 'git pull'?"; then
            cd "$INSTALL_DIR" || log_error "Could not change to project directory."
            git pull || log_error "Git pull failed."
            log_success "Project updated successfully."
        fi
    else
        sudo git clone https://github.com/your_username/your_repo_name.git "$INSTALL_DIR" || log_error "Git clone failed."
        sudo chown -R "$APP_USER":"$APP_USER" "$INSTALL_DIR"
        log_success "Project cloned successfully into $INSTALL_DIR."
    fi
    cd "$INSTALL_DIR" || log_error "Could not change to project directory."
}

install_system_dependencies() {
    log_info "Updating package list and installing system dependencies..."
    sudo apt-get update -y
    sudo apt-get install -y git build-essential libssl-dev zlib1g-dev libbz2-dev \
        libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
        xz-utils tk-dev libffi-dev liblzma-dev python3-openssl nginx redis-server
    log_success "System dependencies installed."
}

setup_python_environment() {
    log_info "Setting up Python environment..."
    if ! check_if_installed "pyenv"; then
        curl https://pyenv.run | bash
        echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
        echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
        echo 'eval "$(pyenv init -)"' >> ~/.bashrc
        export PYENV_ROOT="$HOME/.pyenv"
        export PATH="$PYENV_ROOT/bin:$PATH"
        eval "$(pyenv init -)"
    fi
    pyenv install -s "$PYTHON_VERSION" || log_error "Failed to install Python $PYTHON_VERSION"
    pyenv global "$PYTHON_VERSION"
    log_success "Python environment is ready."
}

setup_nodejs_environment() {
    log_info "Setting up Node.js environment..."
    if ! check_if_installed "nvm"; then
        curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
        export NVM_DIR="$HOME/.nvm"
        [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    fi
    nvm install --lts
    log_success "Node.js environment is ready."
}

setup_backend() {
    log_info "Setting up Django backend..."
    python -m venv venv || log_error "Failed to create virtual environment."
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt || log_error "Failed to install python packages."
    pip install gunicorn

    echo "OPENAI_API_KEY=${OPENAI_API_KEY}" > .env

    python manage.py migrate || log_error "Django migrations failed."
    python manage.py collectstatic --noinput

    deactivate
    log_success "Backend setup complete."
}

setup_frontend() {
    log_info "Building React frontend..."
    cd frontend || log_error "Could not find frontend directory."
    npm install || log_error "npm install failed."
    npm run build || log_error "npm run build failed."
    cd ..
    log_success "Frontend build complete."
}

create_systemd_services() {
    log_info "Creating Systemd services..."
    # Gunicorn Service
    cat > /tmp/gunicorn.service << EOL
[Unit]
Description=gunicorn daemon for instagram bot
After=network.target

[Service]
User=$APP_USER
Group=www-data
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/venv/bin/gunicorn --workers 3 --bind unix:$INSTALL_DIR/gunicorn.sock core.wsgi:application

[Install]
WantedBy=multi-user.target
EOL
    sudo mv /tmp/gunicorn.service /etc/systemd/system/

    # Celery Worker Service
    cat > /tmp/celery_worker.service << EOL
[Unit]
Description=Celery Worker for instagram bot
After=network.target

[Service]
User=$APP_USER
Group=www-data
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/venv/bin/celery -A core worker -l info

[Install]
WantedBy=multi-user.target
EOL
    sudo mv /tmp/celery_worker.service /etc/systemd/system/

    # Celery Beat Service
    cat > /tmp/celery_beat.service << EOL
[Unit]
Description=Celery Beat for instagram bot
After=network.target

[Service]
User=$APP_USER
Group=www-data
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/venv/bin/celery -A core beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

[Install]
WantedBy=multi-user.target
EOL
    sudo mv /tmp/celery_beat.service /etc/systemd/system/

    sudo systemctl daemon-reload
    sudo systemctl start gunicorn celery_worker celery_beat
    sudo systemctl enable gunicorn celery_worker celery_beat
    log_success "Systemd services created and started."
}

configure_nginx() {
    log_info "Configuring Nginx..."
    cat > /tmp/instagram_bot << EOL
server {
    listen $NGINX_PORT;
    server_name $SERVER_IP;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root $INSTALL_DIR;
    }
    location / {
        root $INSTALL_DIR/frontend/dist;
        try_files \$uri /index.html;
    }
    location /api/ {
        include proxy_params;
        proxy_pass http://unix:$INSTALL_DIR/gunicorn.sock;
    }
}
EOL
    sudo mv /tmp/instagram_bot /etc/nginx/sites-available/
    sudo ln -sf /etc/nginx/sites-available/instagram_bot /etc/nginx/sites-enabled/
    sudo nginx -t || log_error "Nginx configuration test failed."
    sudo systemctl restart nginx
    log_success "Nginx configured successfully."
}

run_api_tests() {
    log_info "Running API health checks..."
    chmod +x test_api.sh
    ./test_api.sh "http://$SERVER_IP:$NGINX_PORT"
}

# --- Main Execution Logic ---
main() {
    log_info "Starting Instagram Bot Installation..."

    get_user_input
    log_progress 10 "Input gathered."

    update_or_clone_project
    log_progress 20 "Project repository is ready."

    install_system_dependencies
    log_progress 30 "System dependencies installed."

    setup_python_environment
    log_progress 40 "Python environment is ready."

    setup_nodejs_environment
    log_progress 50 "Node.js environment is ready."

    setup_backend
    log_progress 60 "Backend setup complete."

    setup_frontend
    log_progress 70 "Frontend build complete."

    create_systemd_services
    log_progress 80 "Systemd services created."

    configure_nginx
    log_progress 90 "Nginx configured."

    run_api_tests
    log_progress 100 "Final checks complete."

    echo
    log_success "Installation complete! The application should be accessible at http://${SERVER_IP}:${NGINX_PORT}"
}

# Kick off the script
main