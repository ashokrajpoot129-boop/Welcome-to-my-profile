# NT Django contact page

## Run locally (Windows PowerShell)

Start MySQL. Create the database once if it does not already exist:

```powershell
mysql -u root -p -e "CREATE DATABASE email CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

Set the MySQL connection variables in the PowerShell window you'll use to run Django:

```powershell
$env:DB_NAME = "email"
$env:DB_USER = "root"
$env:DB_PASSWORD = "your-mysql-password"
$env:DB_HOST = "127.0.0.1"
$env:DB_PORT = "3306"
```

Then install dependencies and run Django:

```powershell
cd C:\Users\HP\Desktop\NT
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

`migrate` creates the `contact_contactmessage` table automatically. To inspect its columns and saved submissions in MySQL:

```sql
USE email;
SHOW TABLES;
DESCRIBE contact_contactmessage;
SELECT id, name, email, mobile_number, message, created_at
FROM contact_contactmessage
ORDER BY created_at DESC;
```

Open http://127.0.0.1:8000/.

Copy `.env.example` to `.env` and update its values; Django loads `.env` automatically. Without SMTP credentials, submitted mail is printed in the terminal for local testing. For real delivery, set the mail variables in `.env` or in PowerShell before starting the server. For Gmail, use a Google App Password, not your regular account password:

```powershell
$env:EMAIL_HOST_USER = "your-gmail-address@gmail.com"
$env:EMAIL_HOST_PASSWORD = "your-16-character-app-password"
$env:DEFAULT_FROM_EMAIL = "your-gmail-address@gmail.com"
$env:CONTACT_NOTIFY_EMAIL = "ashokrajpoot129@gmail.com"
python manage.py runserver
```

When someone submits the contact form, `ashokrajpoot129@gmail.com` receives their name, email address, mobile number, and message. The submitter also receives a confirmation at the email address they entered. Each valid submission is stored in the `contact_contactmessage` table and is available in Django admin. Keep database and SMTP credentials private and do not commit them.