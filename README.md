# Instagram Comment Automation Bot

This project is a web application that allows you to automatically reply to comments on your Instagram posts based on keywords. It features a Django backend and a React frontend.

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

### Setup and Installation

**1. Backend Setup (Django)**

-   **Prerequisites:** Python 3.8+, Pip, and Redis.
-   Navigate to the project root directory.
-   **Create an environment file:** Create a file named `.env` in the root directory and add your OpenAI API key:
    ```
    OPENAI_API_KEY=your_openai_api_key_here
    ```
-   **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
-   **Run database migrations:**
    ```bash
    python manage.py migrate
    ```
-   **Start the Django development server:**
    ```bash
    python manage.py runserver
    ```
-   **Start the Celery worker (in a new terminal):**
    ```bash
    celery -A core worker -l info
    ```
-   **Start the Celery beat scheduler (in a new terminal):**
    ```bash
    celery -A core beat -l info
    ```

**2. Frontend Setup (React)**

-   **Prerequisites:** Node.js and npm.
-   Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
-   **Install dependencies:**
    ```bash
    npm install
    ```
-   **Start the React development server:**
    ```bash
    npm run dev
    ```

### How to Use

1.  Open your browser and navigate to `http://localhost:5173` (or the port your React app is running on).
2.  Register a new account or log in.
3.  From the dashboard, click "Add New Account" to connect your first Instagram account. You can add more accounts later.
4.  Select an account from the dropdown to view its posts.
5.  Click "Manage Bot" on any post to open the rule manager.
6.  Click "Create New Rule" and configure your settings:
    -   Add keywords to trigger the bot.
    -   Check "Send as Comment" and/or "Send as Direct Message" and provide reply texts.
    -   Alternatively, check "Generate reply with AI" for smart responses.
7.  The bot will now automatically process comments based on your active rules.

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

### نصب و راه‌اندازی

**۱. راه‌اندازی بک‌اند (Django)**

-   **پیش‌نیازها:** پایتون نسخه ۳.۸ به بالا، Pip و Redis.
-   به پوشه اصلی پروژه بروید.
-   **ایجاد فایل محیطی:** یک فایل به نام `.env` در پوشه اصلی پروژه ایجاد کرده و کلید API خود را در آن قرار دهید:
    ```
    OPENAI_API_KEY=your_openai_api_key_here
    ```
-   **نصب نیازمندی‌ها:**
    ```bash
    pip install -r requirements.txt
    ```
-   **اجرای مایگریشن‌های پایگاه داده:**
    ```bash
    python manage.py migrate
    ```
-   **اجرای سرور جنگو:**
    ```bash
    python manage.py runserver
    ```
-   **اجرای ورکر Celery (در یک ترمینال جدید):**
    ```bash
    celery -A core worker -l info
    ```
-   **اجرای زمان‌بند Celery (در یک ترمینال جدید):**
    ```bash
    celery -A core beat -l info
    ```

**۲. راه‌اندازی فرانت‌اند (React)**

-   **پیش‌نیازها:** Node.js و npm.
-   به پوشه `frontend` بروید:
    ```bash
    cd frontend
    ```
-   **نصب نیازمندی‌ها:**
    ```bash
    npm install
    ```
-   **اجرای سرور React:**
    ```bash
    npm run dev
    ```

### نحوه استفاده

۱. مرورگر خود را باز کرده و به آدرس `http://localhost:5173` (یا پورتی که برنامه React شما روی آن اجرا می‌شود) بروید.
۲. یک حساب کاربری جدید بسازید یا وارد شوید.
۳. از داشبورد، روی «افزودن اکانت جدید» کلیک کنید تا اولین حساب اینستاگرام خود را متصل کنید. می‌توانید بعداً اکانت‌های بیشتری اضافه کنید.
۴. از منوی کشویی یک اکانت را انتخاب کنید تا پست‌های آن را ببینید.
۵. روی «مدیریت ربات» در هر پست کلیک کنید تا مدیریت قوانین باز شود.
۶. روی «ایجاد قانون جدید» کلیک کرده و تنظیمات خود را پیکربندی کنید:
    -   کلمات کلیدی را برای فعال کردن ربات اضافه کنید.
    -   گزینه «ارسال به صورت کامنت» و/یا «ارسال به صورت دایرکت» را علامت بزنید و متن‌های پاسخ را ارائه دهید.
    -   به عنوان جایگزین، برای پاسخ‌های هوشمند، گزینه «ایجاد پاسخ توسط هوش مصنوعی» را علامت بزنید.
۷. ربات به طور خودکار کامنت‌ها را بر اساس قوانین فعال شما پردازش خواهد کرد.