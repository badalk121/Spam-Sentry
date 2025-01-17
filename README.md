# SpamSentry 🛡️

A phone number spam detection and contact management system built with Django. Think Truecaller, but your own version! Protect users from spam calls while managing contacts efficiently.

## Features

- 📱 Phone number spam detection
- 👥 Contact management
- 🔒 User authentication with JWT
- 🔍 Search functionality
- ⚡ Performance optimized
- 💾 Caching support

## Prerequisites

Before we dive in, make sure you have:

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, but recommended)
- A text editor (VS Code, PyCharm, or whatever you prefer)
- A terminal/command prompt
- Coffee ☕ (optional, but highly recommended 😉)

## Quick Start

I'll walk you through setting this up on different operating systems. Don't worry, it's easier than it looks!

### Windows Setup

Open Command Prompt or PowerShell (I'd suggest PowerShell)

1. Clone the repo (if you're using Git)

            git clone https://github.com/badalk121/Spam-Sentry
            cd Spam-Sentry

2. Create a virtual environment (keeping things clean!)

            python -m venv venv

3. Activate it (choose one based on your terminal)

   For Command Prompt:

            venv\Scripts\activate

   For PowerShell:

            .\venv\Scripts\Activate.ps1

4. Install requirements

            pip install -r requirements.txt

5. Set up the database

            python manage.py migrate

6. Create your superuser (follow the prompts)

            python manage.py createsuperuser

7. Run the development server

            python manage.py runserver

### macOS/Linux Setup

Open Terminal

1. Clone the repo

            git clone https://github.com/badalk121/Spam-Sentry.git
            cd SpamSentry

2. Create a virtual environment

            python3 -m venv venv

3. Activate it

            source venv/bin/activate

4. Install requirements

            pip install -r requirements.txt

5. Set up the database

            python manage.py migrate

6. Create your superuser

            python manage.py createsuperuser

7. Run the server

            python manage.py runserver

## Using the API

Let's test it out! I recommend using either Postman or cURL.

### Using cURL

1. Register a new user

            curl -X POST [http://localhost:8000/api/users/](http://localhost:8000/api/users/)
            -H "Content-Type: application/json"
            -d '{"username":"testuser","phone_number":"+11234567890","password":"testpass123"}'

3. Get your token

            curl -X POST [http://localhost:8000/api/token/](http://localhost:8000/api/token/)
            -H "Content-Type: application/json"
            -d '{"phone_number":"+11234567890","password":"testpass123"}'

4. Add a contact (don't forget to replace YOUR_TOKEN)

            curl -X POST [http://localhost:8000/api/contacts/](http://localhost:8000/api/contacts/)
            -H "Authorization: Bearer YOUR_TOKEN"
            -H "Content-Type: application/json"
            -d '{"name":"John Doe","phone_number":"+10987654321"}'

5. Report spam

            curl -X POST [http://localhost:8000/api/spam/](http://localhost:8000/api/spam/)
            -H "Authorization: Bearer YOUR_TOKEN"
            -H "Content-Type: application/json"
            -d '{"phone_number":"+10987654321"}'

### Using Postman

1. Import the provided Postman collection (`SpamSentry.postman_collection.json`)
2. Set up your environment variables:
   - `base_url`: `http://localhost:8000`
   - `token`: (you'll get this after login)
3. Try out the endpoints!

## API Endpoints

Here are all the endpoints you can play with:

Auth Endpoints:
POST /api/users/ - Register new user
POST /api/token/ - Get JWT token
POST /api/token/refresh/ - Refresh JWT token

Contact Endpoints:
GET /api/contacts/ - List contacts
POST /api/contacts/ - Create contact
GET /api/contacts/1/ - Get contact details
PUT /api/contacts/1/ - Update contact
DELETE /api/contacts/1/ - Delete contact

Spam Endpoints:
POST /api/spam/ - Report spam
GET /api/spam/check/ - Check number
GET /api/spam/stats/ - Get spam statistics

## Common Issues & their Solutions

### "Port already in use" error

Windows:

      netstat -ano | findstr :8000
      taskkill /PID /F

macOS/Linux:

      lsof -i :8000
      kill -9

### Database issues?

Nuclear option (FatBoy):

      rm db.sqlite3
      python manage.py migrate

### Virtual environment not working?

Windows PowerShell:

      Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

macOS/Linux:

      chmod +x venv/bin/activate

## 🧪 Running Tests

Run all tests

      python manage.py test

Run specific tests

      python manage.py test apps.users
      python manage.py test apps.contacts
      python manage.py test apps.spam

Run with coverage

      coverage run --source='.' manage.py test
      coverage report

## Production Deployment

Want to deploy to production? Here's what you need to change:

1. Update `settings.py`:
   - Set `DEBUG = False`
   - Update `ALLOWED_HOSTS`
   - Configure your production database
   - Set up proper cache backend
2. Use a proper web server:
   - Nginx + Gunicorn is recommended
   - Don't forget SSL certificates!

## Contributing

Found a bug? Want to add a feature? Awesome! Just:

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/badalk121/Spam-Sentry/blob/main/LICENSE) file for details.

## Need Help?

Got questions? Here's how to get help:

1. Check the issues tab
2. Create a new issue
3. Reach out to me at badal.kumar.sde@gmail.com

---

Developed with efforts and lots of ☕.
