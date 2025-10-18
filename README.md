# Instagram Comment Automation Bot

This project is a web application that allows you to automatically reply to comments on your Instagram posts based on keywords. It features a Django backend and a React frontend.

---

## English

### Features

-   **User Authentication:** Secure user registration and login using JWT.
-   **Instagram Integration:** Connect your Instagram account securely. Your password is never stored.
-   **Post Management:** View your recent Instagram posts directly in the dashboard.
-   **Custom Automation Rules:** For any post, you can define rules that trigger automated responses.
-   **Keyword-Based Triggers:** Rules are triggered when specific keywords are found in comments.
-   **Multiple Reply Types:** Choose to reply with a public comment or a direct message (DM functionality is currently limited).
-   **Task Management:** Create, edit, delete, and pause your automation rules.
-   **Activity Logs:** View a detailed log of all actions performed by the bot.
-   **Rate Limiting:** Smart delays are built-in to prevent your account from being blocked by Instagram.

### Setup and Installation

**1. Backend Setup (Django)**

-   **Prerequisites:** Python 3.8+, Pip, and Redis.
-   Navigate to the project root directory.
-   **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: A `requirements.txt` file should be generated from the installed packages. For now, you can install them manually as done in the agent's history)*
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
2.  Register a new account or log in if you already have one.
3.  On the dashboard, you will be prompted to connect your Instagram account. Enter your Instagram username and password.
4.  Once connected, click the "Fetch Posts" button to see your recent posts.
5.  Click the "Manage Bot" button on any post to open the rule manager.
6.  Create new rules by specifying keywords, the reply text, and the reply type.
7.  The bot will now automatically check for new comments and reply based on your rules.

---

## فارسی

### امکانات

-   **احراز هویت کاربران:** ثبت‌نام و ورود امن کاربران با استفاده از JWT.
-   **اتصال به اینستاگرام:** حساب اینستاگرام خود را به صورت امن متصل کنید. رمز عبور شما هرگز ذخیره نمی‌شود.
-   **مدیریت پست‌ها:** پست‌های اخیر اینستاگرام خود را مستقیماً در داشبورد مشاهده کنید.
-   **قوانین اتوماسیون سفارشی:** برای هر پست، می‌توانید قوانینی برای پاسخ‌های خودکار تعریف کنید.
-   **فعال‌سازی بر اساس کلمات کلیدی:** قوانین زمانی فعال می‌شوند که کلمات کلیدی مشخصی در کامنت‌ها پیدا شوند.
-   **انواع پاسخ:** می‌توانید انتخاب کنید که پاسخ به صورت یک کامنت عمومی یا یک پیام دایرکت باشد (قابلیت دایرکت در حال حاضر محدود است).
-   **مدیریت تسک‌ها:** قوانین اتوماسیون خود را ایجاد، ویرایش، حذف و یا متوقف کنید.
-   **گزارش عملکرد:** گزارش دقیقی از تمام اقدامات انجام شده توسط ربات را مشاهده کنید.
-   **رعایت محدودیت‌ها:** تأخیرهای هوشمند برای جلوگیری از بلاک شدن حساب شما توسط اینستاگرام در سیستم تعبیه شده است.

### نصب و راه‌اندازی

**۱. راه‌اندازی بک‌اند (Django)**

-   **پیش‌نیازها:** پایتون نسخه ۳.۸ به بالا، Pip و Redis.
-   به پوشه اصلی پروژه بروید.
-   **نصب نیازمندی‌ها:**
    ```bash
    pip install -r requirements.txt
    ```
    *(توجه: فایل `requirements.txt` باید از پکیج‌های نصب شده ساخته شود. در حال حاضر، می‌توانید آن‌ها را به صورت دستی نصب کنید.)*
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
۲. یک حساب کاربری جدید بسازید یا اگر از قبل حساب دارید وارد شوید.
۳. در داشبورد، از شما خواسته می‌شود که به حساب اینستاگرام خود متصل شوید. نام کاربری و رمز عبور اینستاگرام خود را وارد کنید.
۴. پس از اتصال، روی دکمه «دریافت پست‌ها» کلیک کنید تا پست‌های اخیر شما نمایش داده شود.
۵. روی دکمه «مدیریت ربات» در هر پست کلیک کنید تا مدیریت قوانین باز شود.
۶. با مشخص کردن کلمات کلیدی، متن پاسخ و نوع پاسخ، قوانین جدیدی ایجاد کنید.
۷. ربات به طور خودکار کامنت‌های جدید را بررسی کرده و بر اساس قوانین شما پاسخ خواهد داد.