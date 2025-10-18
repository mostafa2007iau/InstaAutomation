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
    -   Update your system:
        ```bash
        sudo apt update && sudo apt upgrade -y
        ```
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
    -   Add `pyenv` to your shell's startup file (e.g., `.bashrc` or `.zshrc`):
        ```bash
        echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
        echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
        echo 'eval "$(pyenv init -)"' >> ~/.bashrc
        ```
    -   Reload your shell: `exec "$SHELL"`
    -   Install Python 3.10 (or a recent version):
        ```bash
        pyenv install 3.10.12
        pyenv global 3.10.12
        ```
-   **Install `nvm` for Node.js version management:**
    ```bash
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
    ```
    -   Reload your shell: `exec "$SHELL"`
    -   Install the latest LTS version of Node.js:
        ```bash
        nvm install --lts
        ```

**3. Clone & Setup the Project**

-   **Clone the repository:**
    ```bash
    git clone <YOUR_REPOSITORY_URL>
    cd <YOUR_PROJECT_DIRECTORY>
    ```

**4. Backend Setup (Django)**

-   **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
-   **Install Redis (for Celery):**
    ```bash
    sudo apt install -y redis-server
    sudo systemctl enable redis-server.service
    ```
-   **Create an environment file:** Create a file named `.env` in the project root and add your OpenAI API key:
    ```
    OPENAI_API_KEY=your_openai_api_key_here
    ```
-   **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
-   **Run database migrations:**
    ```bash
    python manage.py migrate
    ```
-   **For development, run the services:**
    -   Django server: `python manage.py runserver`
    -   Celery worker (in a new terminal): `celery -A core worker -l info`
    -   Celery beat (in another new terminal): `celery -A core beat -l info`

**5. Frontend Setup (React)**

-   Navigate to the `frontend` directory: `cd frontend`
-   **Install dependencies:**
    ```bash
    npm install
    ```
-   **For development, run the dev server:** `npm run dev`
-   **For production, build the static files:**
    ```bash
    npm run build
    ```
    The production-ready files will be in the `frontend/dist` directory.

**6. Production Deployment (Recommended)**

For a production environment, you should not use the development servers. Instead:
-   **Backend:** Use **Gunicorn** as an application server and **Nginx** as a reverse proxy.
-   **Frontend:** Serve the static files from the `frontend/dist` directory using Nginx.
-   **Celery:** Run the Celery worker and beat processes as background services using a process manager like **Systemd**.

Setting up Gunicorn, Nginx, and Systemd is a more advanced topic beyond this guide, but it is the standard way to deploy Django and React applications reliably.

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

-   **نوع سرور:** یک سرور مجازی (VPS) با حداقل ۱ هسته پردازشی، ۱ گیگابایت رم و ۲۵ گیگابایت حافظه توصیه می‌شود. شرکت‌هایی مانند DigitalOcean، Linode یا Vultr گزینه‌های مناسبی هستند.
-   **تنظیمات اولیه سرور:**
    -   از طریق SSH به سرور خود متصل شوید: `ssh root@YOUR_SERVER_IP`
    -   سیستم خود را به‌روزرسانی کنید:
        ```bash
        sudo apt update && sudo apt upgrade -y
        ```
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
    -   `pyenv` را به فایل استارتاپ شل خود اضافه کنید (مانند `.bashrc` یا `.zshrc`):
        ```bash
        echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
        echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
        echo 'eval "$(pyenv init -)"' >> ~/.bashrc
        ```
    -   شل خود را دوباره بارگذاری کنید: `exec "$SHELL"`
    -   پایتون نسخه ۳.۱۰ (یا یک نسخه جدید) را نصب کنید:
        ```bash
        pyenv install 3.10.12
        pyenv global 3.10.12
        ```
-   **نصب `nvm` برای مدیریت نسخه‌های Node.js:**
    ```bash
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
    ```
    -   شل خود را دوباره بارگذاری کنید: `exec "$SHELL"`
    -   آخرین نسخه LTS از Node.js را نصب کنید:
        ```bash
        nvm install --lts
        ```

**۳. کلون و راه‌اندازی پروژه**

-   **کلون کردن ریپازیتوری:**
    ```bash
    git clone <YOUR_REPOSITORY_URL>
    cd <YOUR_PROJECT_DIRECTORY>
    ```

**۴. راه‌اندازی بک‌اند (Django)**

-   **ایجاد و فعال‌سازی یک محیط مجازی:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
-   **نصب Redis (برای Celery):**
    ```bash
    sudo apt install -y redis-server
    sudo systemctl enable redis-server.service
    ```
-   **ایجاد فایل محیطی:** یک فایل به نام `.env` در پوشه اصلی پروژه ایجاد کرده و کلید API خود را در آن قرار دهید:
    ```
    OPENAI_API_KEY=your_openai_api_key_here
    ```
-   **نصب نیازمندی‌های پایتون:**
    ```bash
    pip install -r requirements.txt
    ```
-   **اجرای مایگریشن‌های پایگاه داده:**
    ```bash
    python manage.py migrate
    ```
-   **برای محیط توسعه، سرویس‌ها را اجرا کنید:**
    -   سرور جنگو: `python manage.py runserver`
    -   ورکر Celery (در یک ترمینال جدید): `celery -A core worker -l info`
    -   زمان‌بند Celery (در یک ترمینال دیگر): `celery -A core beat -l info`

**۵. راه‌اندازی فرانت‌اند (React)**

-   به پوشه `frontend` بروید: `cd frontend`
-   **نصب نیازمندی‌ها:**
    ```bash
    npm install
    ```
-   **برای محیط توسعه، سرور را اجرا کنید:** `npm run dev`
-   **برای محیط عملیاتی، فایل‌های استاتیک را بسازید:**
    ```bash
    npm run build
    ```
    فایل‌های آماده برای استقرار در پوشه `frontend/dist` قرار خواهند گرفت.

**۶. استقرار در محیط عملیاتی (توصیه‌شده)**

برای یک محیط عملیاتی، نباید از سرورهای توسعه استفاده کنید. به جای آن:
-   **بک‌اند:** از **Gunicorn** به عنوان وب سرور برنامه و از **Nginx** به عنوان پراکسی معکوس استفاده کنید.
-   **فرانت‌اند:** فایل‌های استاتیک ساخته شده در پوشه `frontend/dist` را با استفاده از Nginx سرو کنید.
-   **Celery:** پردازه‌های ورکر و بیت Celery را به عنوان سرویس‌های پس‌زمینه با استفاده از یک مدیر پردازش مانند **Systemd** اجرا کنید.

راه‌اندازی Gunicorn، Nginx و Systemd یک موضوع پیشرفته‌تر است که خارج از این راهنماست، اما این روش استاندارد برای استقرار قابل اعتماد برنامه‌های Django و React است.