# Instagram Comment Automation Bot

This project is a web application that allows you to automatically reply to comments on your Instagram posts based on keywords. It features a Django backend, a React frontend, multi-account support, and AI-powered smart replies.

---

## English

### Features

-   **User Authentication:** Secure user registration and login using JWT.
-   **Flexible Instagram Login:** Connect your accounts using traditional username/password or by providing session details for enhanced security.
-   **Proxy Support:** Configure a unique proxy for each connected Instagram account to minimize the risk of blocks and improve connection stability.
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

**1. Server Preparation & Initial Setup**

-   **Server Type:** A Virtual Private Server (VPS) with at least 1 CPU core, 1 GB of RAM, and 25 GB of storage is recommended.
-   **Connect & Update:** Connect via SSH (`ssh root@YOUR_SERVER_IP`) and update your system: `sudo apt update && sudo apt upgrade -y`
-   **Install Essentials:**
    ```bash
    sudo apt install -y git build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python3-openssl nginx
    ```

**2. Install Python & Node.js**

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

**3. Clone & Setup the Project**

-   Clone the repository: `git clone <YOUR_REPOSITORY_URL>`
-   Navigate into the project: `cd <YOUR_PROJECT_DIRECTORY>`

**4. Backend Production Setup (Gunicorn & Systemd)**

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
        ExecStart=<path_to_project>/venv/bin/gunicorn \
            --access-logfile - \
            --workers 3 \
            --bind unix:<path_to_project>/gunicorn.sock \
            core.wsgi:application

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

**5. Frontend Production Setup (Nginx)**

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

### How to Use

1.  Open your browser and navigate to your server's IP or domain.
2.  Register a new account or log in.
3.  From the dashboard, click "Add New Account". You will have two options:
    -   **Login with Password:** Enter your Instagram username and password.
    -   **Login with Session:** A more secure method. Enter your `sessionid`, `csrftoken`, and `ds_user_id` values, which you can find in your browser's cookies for instagram.com.
    -   **Proxy (Optional):** For either method, you can provide a proxy URL (e.g., `http://user:pass@host:port`) to enhance security.
4.  Once connected, your account will appear in the dropdown. You can add more accounts.
5.  Select an account from the dropdown to view its posts.
6.  Click "Manage Bot" on any post to open the rule manager.
7.  Click "Create New Rule" and configure your settings.
8.  The bot will now automatically process comments based on your active rules, using the proxy you provided for that account if any.

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

### امکانات

-   **احراز هویت کاربران:** ثبت‌نام و ورود امن کاربران با استفاده از JWT.
-   **ورود انعطاف‌پذیر به اینستاگرام:** اکانت‌های خود را با استفاده از نام کاربری/رمز عبور یا از طریق جزئیات نشست (Session) برای امنیت بیشتر متصل کنید.
-   **پشتیبانی از پراکسی:** برای هر اکانت اینستاگرام یک پراکسی منحصربه‌فرد تنظیم کنید تا ریسک بلاک شدن به حداقل برسد و پایداری اتصال افزایش یابد.
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

**۱. آماده‌سازی سرور و نصب ابزارهای اولیه**

-   **نوع سرور:** یک سرور مجازی (VPS) با حداقل ۱ هسته پردازشی، ۱ گیگابایت رم و ۲۵ گیگابایت حافظه توصیه می‌شود.
-   **اتصال و به‌روزرسانی:** با دستور `ssh root@YOUR_SERVER_IP` به سرور متصل شده و آن را آپدیت کنید: `sudo apt update && sudo apt upgrade -y`
-   **نصب ابزارهای ضروری:**
    ```bash
    sudo apt install -y git build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python3-openssl nginx
    ```

**۲. نصب پایتون و Node.js**

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

**۳. کلون و راه‌اندازی پروژه**

-   **کلون کردن ریپازیتوری:** `git clone <YOUR_REPOSITORY_URL>`
-   **ورود به پوشه پروژه:** `cd <YOUR_PROJECT_DIRECTORY>`

**۴. راه‌اندازی بک‌اند در محیط عملیاتی (Gunicorn & Systemd)**

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
        ExecStart=<path_to_project>/venv/bin/gunicorn \
            --access-logfile - \
            --workers 3 \
            --bind unix:<path_to_project>/gunicorn.sock \
            core.wsgi:application

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

**۵. راه‌اندازی فرانت‌اند در محیط عملیاتی (Nginx)**

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

### نحوه استفاده

۱. مرورگر خود را باز کرده و به آدرس IP یا دامنه سرور خود بروید.
۲. یک حساب کاربری جدید بسازید یا وارد شوید.
۳. از داشبورد، روی «افزودن اکانت جدید» کلیک کنید. شما دو گزینه خواهید داشت:
    -   **ورود با رمز عبور:** نام کاربری و رمز عبور اینستاگرام خود را وارد کنید.
    -   **ورود با نشست (Session):** یک روش امن‌تر. مقادیر `sessionid`، `csrftoken` و `ds_user_id` را که می‌توانید از کوکی‌های مرورگر خود در سایت instagram.com پیدا کنید، وارد نمایید.
    -   **پراکسی (اختیاری):** برای هر دو روش، می‌توانید یک آدرس پراکسی (مانند `http://user:pass@host:port`) برای افزایش امنیت ارائه دهید.
۴. پس از اتصال، اکانت شما در منوی کشویی ظاهر می‌شود. می‌توانید اکانت‌های بیشتری اضافه کنید.
۵. از منوی کشویی یک اکانت را انتخاب کنید تا پست‌های آن را ببینید.
۶. روی «مدیریت ربات» در هر پست کلیک کنید تا مدیریت قوانین باز شود.
۷. روی «ایجاد قانون جدید» کلیک کرده و تنظیمات خود را پیکربندی کنید.
۸. ربات به طور خودکار کامنت‌ها را بر اساس قوانین فعال شما پردازش خواهد کرد و در صورت وجود، از پراکسی که برای آن اکانت ارائه داده‌اید استفاده می‌کند.

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