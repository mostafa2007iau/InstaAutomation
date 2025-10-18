# Instagram Comment Automation Bot

This project is a web application that allows you to automatically reply to comments on your Instagram posts based on keywords. It features a Django backend, a React frontend, multi-account support, and AI-powered smart replies.

---

## English

### Features

-   **User Authentication:** Secure user registration and login using JWT.
-   **Multi-Account Support:** Connect and manage multiple Instagram accounts under a single user.
-   **Post Management:** View your recent Instagram posts for each connected account.
-   **Advanced Automation Rules:**
    -   Define multiple rules for each post.
    -   Trigger responses based on keywords.
    -   Choose to reply via comment, direct message, or both.
    -   Set custom reply texts for comments and DMs.
-   **AI-Powered Smart Replies:** Optionally, use AI (powered by OpenAI's GPT models) to generate context-aware, human-like replies.
-   **Task Management:** Create, edit, delete, and pause your automation rules.
-   **Activity Logs:** View a detailed log of all actions performed by the bot for each rule.
-   **Rate Limiting:** Smart delays are built-in to prevent your account from being blocked by Instagram.

### Full Deployment Guide (from Scratch)

This guide provides a detailed walkthrough for deploying the application on a fresh **Ubuntu 22.04 server**.

**1. Server Preparation**

-   **Server Type:** A Virtual Private Server (VPS) with at least 1 CPU core, 1 GB of RAM, and 25 GB of storage is recommended. Providers like DigitalOcean, Linode, or Vultr are good options.
-   **Initial Server Setup:**
    -   Connect to your server via SSH: `ssh root@YOUR_SERVER_IP`
    -   Update your system: `sudo apt update && sudo apt upgrade -y`
    -   Install essential build tools and Git:
        ```bash
        sudo apt install -y git build-essential libssl-dev zlib1g-dev libbz2-dev \
        libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
        xz-utils tk-dev libffi-dev liblzma-dev python3-openssl
        ```

**2. Install Python & Node.js**

-   **Install `pyenv` for Python version management:**
    ```bash
    curl https://pyenv.run | bash
    ```
    -   Add `pyenv` to your shell's startup file (e.g., `.bashrc`):
        ```bash
        echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
        echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
        echo 'eval "$(pyenv init -)"' >> ~/.bashrc
        ```
    -   Reload your shell: `exec "$SHELL"`
    -   Install Python 3.10: `pyenv install 3.10.12 && pyenv global 3.10.12`
-   **Install `nvm` for Node.js version management:**
    ```bash
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
    ```
    -   Reload your shell: `exec "$SHELL"`
    -   Install Node.js LTS: `nvm install --lts`

**3. Clone & Setup the Project**

-   Clone the repository: `git clone <YOUR_REPOSITORY_URL>`
-   Navigate into the project: `cd <YOUR_PROJECT_DIRECTORY>`

**4. Backend Setup (Django)**

-   **Create virtual environment:** `python -m venv venv && source venv/bin/activate`
-   **Install Redis:** `sudo apt install -y redis-server && sudo systemctl enable redis-server.service`
    *(Note: The app is configured to use Redis on port `6380`. If you need to change this, edit `redis.conf` and the URL in `core/settings.py`.)*
-   **Create `.env` file:** Create a `.env` file in the project root:
    ```
    OPENAI_API_KEY=your_openai_api_key_here
    ```
-   **Install dependencies:** `pip install -r requirements.txt`
-   **Run database migrations:** `python manage.py migrate`
-   **Run Development Server:** `python manage.py runserver 8001`
    *(For production, use Gunicorn and run Celery processes as background services with Systemd.)*

**5. Frontend Production Deployment with Nginx**

This section details how to serve the React frontend and proxy API requests to the Django backend using Nginx.

-   **Navigate to the frontend directory and build the project:**
    ```bash
    cd frontend
    npm install
    npm run build
    cd ..
    ```
-   **Install Nginx:**
    ```bash
    sudo apt install -y nginx
    ```
-   **Create an Nginx configuration file:**
    ```bash
    sudo nano /etc/nginx/sites-available/instagram_bot
    ```
-   **Paste the following configuration** into the file. Replace `your_domain_or_server_ip` with your server's public IP address or your domain name.
    ```nginx
    server {
        listen 80;
        server_name your_domain_or_server_ip;

        # Serve React App
        location / {
            root /path/to/your_project/frontend/dist;
            try_files $uri /index.html;
        }

        # Proxy API requests to the Django backend
        location /api/ {
            proxy_pass http://127.0.0.1:8001;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
    ```
    *Important: Make sure to replace `/path/to/your_project/` with the actual absolute path to your project directory on the server.*
-   **Enable the site and test the configuration:**
    ```bash
    sudo ln -s /etc/nginx/sites-available/instagram_bot /etc/nginx/sites-enabled/
    sudo nginx -t
    ```
-   **If the test is successful, restart Nginx:**
    ```bash
    sudo systemctl restart nginx
    ```
-   **Adjust the Firewall:**
    ```bash
    sudo ufw allow 'Nginx Full'
    ```

Your application should now be accessible at `http://your_domain_or_server_ip`.

---

## فارسی

### امکانات

-   **احراز هویت کاربران:** ثبت‌نام و ورود امن کاربران با استفاده از JWT.
-   **پشتیبانی از چند اکانت:** چندین حساب اینستاگرام را تحت یک کاربر واحد متصل و مدیریت کنید.
-   **مدیریت پست‌ها:** پست‌های اخیر هر حساب متصل شده را مشاهده کنید.
-   **قوانین اتوماسیون پیشرفته:**
    -   برای هر پست چندین قانون مختلف تعریف کنید.
    -   پاسخ‌ها را بر اساس کلمات کلیدی فعال کنید.
    -   انتخاب کنید که پاسخ از طریق کامنت، دایرکت یا هر دو ارسال شود.
    -   متن‌های پاسخ سفارشی برای کامنت و دایرکت تنظیم کنید.
-   **پاسخ‌های هوشمند با هوش مصنوعی:** به صورت اختیاری، از هوش مصنوعی (مدل‌های GPT) برای تولید پاسخ‌های هوشمند و انسانی استفاده کنید.
-   **مدیریت تسک‌ها:** قوانین اتوماسیون خود را ایجاد، ویرایش، حذف و یا متوقف کنید.
-   **گزارش عملکرد:** گزارش دقیقی از تمام اقدامات انجام شده توسط ربات برای هر قانون را مشاهده کنید.
-   **رعایت محدودیت‌ها:** تأخیرهای هوشمند برای جلوگیری از بلاک شدن حساب شما توسط اینستاگرام در سیستم تعبیه شده است.

### راهنمای کامل استقرار (از صفر)

این راهنما یک توضیح قدم به قدم برای استقرار برنامه روی یک سرور **اوبونتو نسخه ۲۲.۰۴** ارائه می‌دهد.

**۱. آماده‌سازی سرور**

-   **نوع سرور:** یک سرور مجازی (VPS) با حداقل ۱ هسته پردازشی، ۱ گیگابایت رم و ۲۵ گیگابایت حافظه توصیه می‌شود.
-   **تنظیمات اولیه سرور:**
    -   از طریق SSH به سرور خود متصل شوید: `ssh root@YOUR_SERVER_IP`
    -   سیستم خود را به‌روزرسانی کنید: `sudo apt update && sudo apt upgrade -y`
    -   ابزارهای ضروری و گیت را نصب کنید:
        ```bash
        sudo apt install -y git build-essential libssl-dev zlib1g-dev libbz2-dev \
        libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
        xz-utils tk-dev libffi-dev liblzma-dev python3-openssl
        ```

**۲. نصب پایتون و Node.js**

-   **نصب `pyenv` برای مدیریت نسخه‌های پایتون:**
    ```bash
    curl https://pyenv.run | bash
    ```
    -   `pyenv` را به فایل استارتاپ شل خود اضافه کنید (مانند `.bashrc`):
        ```bash
        echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
        echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
        echo 'eval "$(pyenv init -)"' >> ~/.bashrc
        ```
    -   شل خود را دوباره بارگذاری کنید: `exec "$SHELL"`
    -   پایتون نسخه ۳.۱۰ را نصب کنید: `pyenv install 3.10.12 && pyenv global 3.10.12`
-   **نصب `nvm` برای مدیریت نسخه‌های Node.js:**
    ```bash
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
    ```
    -   شل خود را دوباره بارگذاری کنید: `exec "$SHELL"`
    -   آخرین نسخه LTS از Node.js را نصب کنید: `nvm install --lts`

**۳. کلون و راه‌اندازی پروژه**

-   **کلون کردن ریپازیتوری:** `git clone <YOUR_REPOSITORY_URL>`
-   **ورود به پوشه پروژه:** `cd <YOUR_PROJECT_DIRECTORY>`

**۴. راه‌اندازی بک‌اند (Django)**

-   **ایجاد محیط مجازی:** `python -m venv venv && source venv/bin/activate`
-   **نصب Redis:** `sudo apt install -y redis-server && sudo systemctl enable redis-server.service`
    *(توجه: برنامه برای استفاده از Redis روی پورت `6380` پیکربندی شده است. اگر نیاز به تغییر دارید، فایل `redis.conf` و آدرس در `core/settings.py` را ویرایش کنید.)*
-   **ایجاد فایل `.env`:** یک فایل `.env` در ریشه پروژه بسازید:
    ```
    OPENAI_API_KEY=your_openai_api_key_here
    ```
-   **نصب نیازمندی‌ها:** `pip install -r requirements.txt`
-   **اجرای مایگریشن‌ها:** `python manage.py migrate`
-   **اجرای سرور توسعه:** `python manage.py runserver 8001`
    *(برای محیط عملیاتی، از Gunicorn استفاده کرده و پردازه‌های Celery را با Systemd به عنوان سرویس پس‌زمینه اجرا کنید.)*

**۵. استقرار فرانت‌اند در محیط عملیاتی با Nginx**

این بخش نحوه سرو کردن فرانت‌اند React و هدایت درخواست‌های API به بک‌اند جنگو را با استفاده از Nginx توضیح می‌دهد.

-   **به پوشه فرانت‌اند رفته و پروژه را بیلد کنید:**
    ```bash
    cd frontend
    npm install
    npm run build
    cd ..
    ```
-   **نصب Nginx:**
    ```bash
    sudo apt install -y nginx
    ```
-   **ایجاد فایل پیکربندی برای Nginx:**
    ```bash
    sudo nano /etc/nginx/sites-available/instagram_bot
    ```
-   **پیکربندی زیر را در فایل کپی کنید.** حتماً `your_domain_or_server_ip` را با آدرس IP عمومی سرور یا دامنه خود جایگزین کنید.
    ```nginx
    server {
        listen 80;
        server_name your_domain_or_server_ip;

        # سرو کردن برنامه React
        location / {
            root /path/to/your_project/frontend/dist;
            try_files $uri /index.html;
        }

        # پراکسی کردن درخواست‌های API به بک‌اند جنگو
        location /api/ {
            proxy_pass http://127.0.0.1:8001;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
    ```
    *مهم: حتماً `/path/to/your_project/` را با مسیر مطلق واقعی پروژه خود روی سرور جایگزین کنید.*
-   **فعال‌سازی سایت و تست پیکربندی:**
    ```bash
    sudo ln -s /etc/nginx/sites-available/instagram_bot /etc/nginx/sites-enabled/
    sudo nginx -t
    ```
-   **اگر تست موفقیت‌آمیز بود، Nginx را ری‌استارت کنید:**
    ```bash
    sudo systemctl restart nginx
    ```
-   **تنظیم فایروال:**
    ```bash
    sudo ufw allow 'Nginx Full'
    ```

اکنون برنامه شما باید از طریق آدرس `http://your_domain_or_server_ip` قابل دسترس باشد.