# Instagram Comment Automation Bot

This project is a web application that allows you to automatically reply to comments on your Instagram posts based on keywords. It features a Django backend, a React frontend, multi-account support, and AI-powered smart replies.

---

## Installation

There are two ways to install and deploy this application:

1.  **Automated Installation (Recommended):** Use the smart installation script to handle everything automatically. This is the best option for most users.
2.  **Manual Installation (Advanced):** Follow the step-by-step guide if you want full control over the installation process.

### Automated Installation (Recommended)

This script will ask for necessary inputs, check for existing dependencies, set up the entire environment, and deploy the application.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your_username/your_repo_name.git
    cd your_repo_name
    ```
2.  **Make the script executable:**
    ```bash
    chmod +x install.sh
    ```
3.  **Run the script:**
    ```bash
    ./install.sh
    ```
    Follow the on-screen prompts to provide your server IP, a user for the application, your OpenAI key, and other settings. The script will handle the rest.

---

### Manual Installation Guide (Advanced)

This guide provides a detailed walkthrough for deploying the application on a fresh **Ubuntu 22.04 server**.

#### 1. Server Preparation & Initial Setup

-   **Server Type:** A Virtual Private Server (VPS) with at least 1 CPU core, 1 GB of RAM, and 25 GB of storage is recommended.
-   **Connect & Update:** Connect via SSH (`ssh root@YOUR_SERVER_IP`) and update your system: `sudo apt update && sudo apt upgrade -y`
-   **Install Essentials:**
    ```bash
    sudo apt install -y git build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python3-openssl nginx
    ```

#### 2. Install Python & Node.js

-   **Install `pyenv` for Python:**
    ```bash
    curl https://pyenv.run | bash
    # Add to shell config (e.g., .bashrc)
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc
    exec "$SHELL" # Reload shell
    pyenv install 3.10.12 && pyenv global 3.10.12
    ```
-   **Install `nvm` for Node.js:**
    ```bash
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
    exec "$SHELL" # Reload shell
    nvm install --lts
    ```

#### 3. Clone & Setup the Project

-   **Clone the repository:** `git clone <YOUR_REPOSITORY_URL>`
-   **Navigate into the project:** `cd <YOUR_PROJECT_DIRECTORY>`

#### 4. Backend Production Setup (Gunicorn & Systemd)

-   **Create virtual environment:** `python -m venv venv && source venv/bin/activate`
-   **Install Redis:** `sudo apt install -y redis-server && sudo systemctl enable redis-server.service`
-   **Create `.env` file:** Create a `.env` file in the project root with `OPENAI_API_KEY=your_key`.
-   **Install dependencies:** `pip install -r requirements.txt` and `pip install gunicorn`.
-   **Run migrations & collect static files:** `python manage.py migrate` and `python manage.py collectstatic`.
-   **Create Gunicorn Systemd Service:**
    -   `sudo nano /etc/systemd/system/gunicorn.service`
    -   Paste the following, replacing `<user>` and `<path_to_project>`:
        ```ini
        [Unit]
        Description=gunicorn daemon
        After=network.target

        [Service]
        User=<user>
        Group=www-data
        WorkingDirectory=<path_to_project>
        ExecStart=<path_to_project>/venv/bin/gunicorn --workers 3 --bind unix:<path_to_project>/gunicorn.sock core.wsgi:application

        [Install]
        WantedBy=multi-user.target
        ```
-   **Create Celery Worker Systemd Service:**
    -   `sudo nano /etc/systemd/system/celery_worker.service`
    -   Paste the following, replacing `<user>` and `<path_to_project>`:
        ```ini
        [Unit]
        Description=Celery Worker Service
        After=network.target

        [Service]
        User=<user>
        Group=www-data
        WorkingDirectory=<path_to_project>
        ExecStart=<path_to_project>/venv/bin/celery -A core worker -l info

        [Install]
        WantedBy=multi-user.target
        ```
-   **Create Celery Beat Systemd Service:**
    -   `sudo nano /etc/systemd/system/celery_beat.service`
    -   Paste the following, replacing `<user>` and `<path_to_project>`:
        ```ini
        [Unit]
        Description=Celery Beat Service
        After=network.target

        [Service]
        User=<user>
        Group=www-data
        WorkingDirectory=<path_to_project>
        ExecStart=<path_to_project>/venv/bin/celery -A core beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

        [Install]
        WantedBy=multi-user.target
        ```
-   **Start and Enable Services:**
    ```bash
    sudo systemctl start gunicorn celery_worker celery_beat
    sudo systemctl enable gunicorn celery_worker celery_beat
    ```

#### 5. Frontend Production Setup (Nginx)

-   **Build the project:** `cd frontend && npm install && npm run build && cd ..`
-   **Configure Nginx:**
    -   `sudo nano /etc/nginx/sites-available/instagram_bot`
    -   Paste the following, replacing `your_domain_or_ip` and `<path_to_project>`:
        ```nginx
        server {
            listen 80;
            server_name your_domain_or_ip; # e.g., example.com or your server's IP

            # Path for Django static files
            location /static/ {
                root <path_to_project>; # e.g., /home/user/instagram_bot
            }

            # Path for React frontend build
            location / {
                root <path_to_project>/frontend/dist;
                try_files $uri /index.html;
            }

            # Proxy API requests to the Gunicorn socket
            location /api/ {
                include proxy_params;
                proxy_pass http://unix:<path_to_project>/gunicorn.sock;
            }
        }
        ```
-   **Enable the site:** `sudo ln -s /etc/nginx/sites-available/instagram_bot /etc/nginx/sites-enabled/`
-   **Test and restart Nginx:** `sudo nginx -t && sudo systemctl restart nginx`
-   **Adjust Firewall:** `sudo ufw allow 'Nginx Full'`

Your application is now live and running with a production-ready setup.

### Cross-Platform Application (.NET MAUI)

For developers interested in building a native cross-platform (iOS, Android, Windows, macOS) application, a complete architectural blueprint is available. This document provides a detailed technical guide, including project structure, recommended libraries, and code samples.

**[View the .NET MAUI Architectural Blueprint](./MAUI_ARCHITECTURE.md)**

### Troubleshooting

-   **500 Internal Server Error:** This is a generic server-side error. The most common causes are:
    1.  **Incorrect Paths:** The paths in your Nginx or Systemd service files (`<path_to_project>`) do not match the actual absolute path of your project directory. Double-check all paths.
    2.  **Permissions Issues:** Nginx (running as `www-data`) or your Gunicorn user may not have permission to read or execute files in your project directory.
        -   Check Nginx error logs for "permission denied" errors: `sudo tail -f /var/log/nginx/error.log`
        -   Ensure your user is in the `www-data` group: `sudo usermod -aG www-data <your_user>`
        -   Set appropriate permissions: `sudo chmod -R 775 <path_to_project>`
    3.  **Gunicorn Socket Not Found:** The Nginx proxy cannot connect to the Gunicorn socket. Check the Gunicorn service status: `sudo systemctl status gunicorn`. Make sure it's active and running without errors.

-   **API requests are failing:** If the frontend loads but API calls fail, check the Nginx access and error logs. Also, ensure the Gunicorn service is running correctly and that the API proxy in your Nginx config is pointing to the correct socket or address.

---

## فارسی

### راهنمای نصب

برای نصب و استقرار این برنامه دو روش وجود دارد:

1.  **نصب خودکار (روش پیشنهادی):** از اسکریپت هوشمند نصب استفاده کنید تا همه چیز به صورت خودکار انجام شود. این بهترین گزینه برای اکثر کاربران است.
2.  **نصب دستی (برای متخصصان):** اگر می‌خواهید کنترل کاملی بر فرآیند نصب داشته باشید، راهنمای قدم به قدم را دنبال کنید.

### نصب خودکار (روش پیشنهادی)

این اسکریپت ورودی‌های لازم را از شما می‌پرسد، نیازمندی‌های موجود را بررسی می‌کند، کل محیط را راه‌اندازی کرده و برنامه را مستقر می‌کند.

1.  **کلون کردن ریپازیتوری:**
    ```bash
    git clone https://github.com/your_username/your_repo_name.git
    cd your_repo_name
    ```
2.  **قابل اجرا کردن اسکریپت:**
    ```bash
    chmod +x install.sh
    ```
3.  **اجرای اسکریپت:**
    ```bash
    ./install.sh
    ```
    دستورالعمل‌های روی صفحه را دنبال کنید تا IP سرور، کاربر برنامه، کلید OpenAI و سایر تنظیمات را ارائه دهید. اسکریپت بقیه کارها را انجام خواهد داد.

---

### راهنمای نصب دستی (برای متخصصان)

این راهنما یک توضیح قدم به قدم برای استقرار برنامه روی یک سرور **اوبونتو نسخه ۲۲.۰۴** ارائه می‌دهد.

#### ۱. آماده‌سازی سرور و نصب ابزارهای اولیه

-   **نوع سرور:** یک سرور مجازی (VPS) با حداقل ۱ هسته پردازشی، ۱ گیگابایت رم و ۲۵ گیگابایت حافظه توصیه می‌شود.
-   **اتصال و به‌روزرسانی:** با دستور `ssh root@YOUR_SERVER_IP` به سرور متصل شده و آن را آپدیت کنید: `sudo apt update && sudo apt upgrade -y`
-   **نصب ابزارهای ضروری:**
    ```bash
    sudo apt install -y git build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python3-openssl nginx
    ```

#### ۲. نصب پایتون و Node.js

-   **نصب `pyenv` برای پایتون:**
    ```bash
    curl https://pyenv.run | bash
    # افزودن به فایل کانفیگ شل (مانند .bashrc)
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc
    exec "$SHELL" # بارگذاری مجدد شل
    pyenv install 3.10.12 && pyenv global 3.10.12
    ```
-   **نصب `nvm` برای Node.js:**
    ```bash
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
    exec "$SHELL" # بارگذاری مجدد شل
    nvm install --lts
    ```

#### ۳. کلون و راه‌اندازی پروژه

-   **کلون کردن ریپازیتوری:** `git clone <YOUR_REPOSITORY_URL>`
-   **ورود به پوشه پروژه:** `cd <YOUR_PROJECT_DIRECTORY>`

#### ۴. راه‌اندازی بک‌اند در محیط عملیاتی (Gunicorn & Systemd)

-   **ایجاد محیط مجازی:** `python -m venv venv && source venv/bin/activate`
-   **نصب Redis:** `sudo apt install -y redis-server && sudo systemctl enable redis-server.service`
-   **ایجاد فایل `.env`:** یک فایل `.env` در ریشه پروژه با محتوای `OPENAI_API_KEY=your_key` بسازید.
-   **نصب نیازمندی‌ها:** `pip install -r requirements.txt` و سپس `pip install gunicorn`.
-   **اجرای مایگریشن و جمع‌آوری فایل‌های استاتیک:** `python manage.py migrate` و `python manage.py collectstatic`.
-   **ایجاد سرویس Systemd برای Gunicorn:**
    -   `sudo nano /etc/systemd/system/gunicorn.service`
    -   محتوای زیر را کپی کرده و `<user>` و `<path_to_project>` را جایگزین کنید:
        ```ini
        [Unit]
        Description=gunicorn daemon
        After=network.target

        [Service]
        User=<user>
        Group=www-data
        WorkingDirectory=<path_to_project>
        ExecStart=<path_to_project>/venv/bin/gunicorn --workers 3 --bind unix:<path_to_project>/gunicorn.sock core.wsgi:application

        [Install]
        WantedBy=multi-user.target
        ```
-   **ایجاد سرویس Systemd برای Celery Worker:**
    -   `sudo nano /etc/systemd/system/celery_worker.service`
    -   محتوای زیر را کپی کرده و `<user>` و `<path_to_project>` را جایگزین کنید:
        ```ini
        [Unit]
        Description=Celery Worker Service
        After=network.target

        [Service]
        User=<user>
        Group=www-data
        WorkingDirectory=<path_to_project>
        ExecStart=<path_to_project>/venv/bin/celery -A core worker -l info

        [Install]
        WantedBy=multi-user.target
        ```
-   **ایجاد سرویس Systemd برای Celery Beat:**
    -   `sudo nano /etc/systemd/system/celery_beat.service`
    -   محتوای زیر را کپی کرده و `<user>` و `<path_to_project>` را جایگزین کنید:
        ```ini
        [Unit]
        Description=Celery Beat Service
        After=network.target

        [Service]
        User=<user>
        Group=www-data
        WorkingDirectory=<path_to_project>
        ExecStart=<path_to_project>/venv/bin/celery -A core beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

        [Install]
        WantedBy=multi-user.target
        ```
-   **شروع و فعال‌سازی سرویس‌ها:**
    ```bash
    sudo systemctl start gunicorn celery_worker celery_beat
    sudo systemctl enable gunicorn celery_worker celery_beat
    ```

#### ۵. راه‌اندازی فرانت‌اند در محیط عملیاتی (Nginx)

-   **بیلد کردن پروژه:** `cd frontend && npm install && npm run build && cd ..`
-   **پیکربندی Nginx:**
    -   `sudo nano /etc/nginx/sites-available/instagram_bot`
    -   محتوای زیر را کپی کرده و `your_domain_or_ip` و `<path_to_project>` را جایگزین کنید:
        ```nginx
        server {
            listen 80;
            server_name your_domain_or_ip; # برای مثال: example.com یا IP سرور شما

            # مسیر فایل‌های استاتیک جنگو
            location /static/ {
                root <path_to_project>; # برای مثال: /home/user/instagram_bot
            }

            # مسیر فایل‌های بیلد شده فرانت‌اند React
            location / {
                root <path_to_project>/frontend/dist;
                try_files $uri /index.html;
            }

            # پراکسی کردن درخواست‌های API به سوکت Gunicorn
            location /api/ {
                include proxy_params;
                proxy_pass http://unix:<path_to_project>/gunicorn.sock;
            }
        }
        ```
-   **فعال‌سازی سایت:** `sudo ln -s /etc/nginx/sites-available/instagram_bot /etc/nginx/sites-enabled/`
-   **تست و ری‌استارت Nginx:** `sudo nginx -t && sudo systemctl restart nginx`
-   **تنظیم فایروال:** `sudo ufw allow 'Nginx Full'`

اکنون برنامه شما به صورت کامل و پایدار روی سرور در حال اجرا است.

### اپلیکیشن چند پلتفرمی (.NET MAUI)

برای توسعه‌دهندگانی که علاقه‌مند به ساخت یک اپلیکیشن نیتیو چند پلتفرمی (iOS، اندروید، ویندوز، macOS) هستند، یک بلوپرینت معماری کامل آماده شده است. این سند یک راهنمای فنی دقیق شامل ساختار پروژه، کتابخانه‌های پیشنهادی و نمونه کدها را ارائه می‌دهد.

**[مشاهده بلوپرینت معماری .NET MAUI](./MAUI_ARCHITECTURE.md)**

### عیب‌یابی (Troubleshooting)

-   **خطای 500 Internal Server Error:** این یک خطای عمومی سمت سرور است. دلایل رایج آن عبارتند از:
    1.  **مسیرهای نادرست:** مسیرهای (`<path_to_project>`) در فایل‌های سرویس Nginx یا Systemd با مسیر مطلق واقعی پروژه شما مطابقت ندارند. تمام مسیرها را دوباره بررسی کنید.
    2.  **مشکلات سطح دسترسی (Permissions):** کاربر Nginx (`www-data`) یا کاربر Gunicorn شما ممکن است اجازه خواندن یا اجرای فایل‌های پروژه را نداشته باشد.
        -   برای خطاهای "permission denied"، لاگ خطای Nginx را بررسی کنید: `sudo tail -f /var/log/nginx/error.log`
        -   مطمئن شوید کاربر شما عضو گروه `www-data` است: `sudo usermod -aG www-data <your_user>`
        -   سطوح دسترسی مناسب را تنظیم کنید: `sudo chmod -R 775 <path_to_project>`
    3.  **پیدا نشدن سوکت Gunicorn:** پراکسی Nginx نمی‌تواند به سوکت Gunicorn متصل شود. وضعیت سرویس Gunicorn را بررسی کنید: `sudo systemctl status gunicorn`. مطمئن شوید که سرویس فعال و بدون خطا در حال اجراست.

-   **درخواست‌های API با شکست مواجه می‌شوند:** اگر فرانت‌اند بارگذاری می‌شود اما فراخوانی‌های API با خطا مواجه می‌شوند، لاگ‌های دسترسی و خطای Nginx را بررسی کنید. همچنین، مطمئن شوید که سرویس Gunicorn به درستی در حال اجراست و پراکسی API در کانفیگ Nginx شما به سوکت یا آدرس صحیح اشاره می‌کند.