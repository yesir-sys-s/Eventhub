# Setup Instructions for EventHub

## 1. Install Homebrew
Open Terminal and run:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

## 2. Install Python
```bash
brew install python
```

## 3. Verify Python installation
```bash
python3 --version
```

## 4. Create and activate virtual environment
```bash
# Navigate to your project directory
cd /Users/oliverreyes/Downloads/Eventhub

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

## 5. Install dependencies
Once your virtual environment is activated:
```bash
pip install -r requirements.txt
```

## 6. Run migrations
```bash
python manage.py migrate
```

## 7. Create superuser (optional)
```bash
python manage.py createsuperuser
```

## 8. Run development server
```bash
python manage.py runserver
```

The site should now be accessible at http://127.0.0.1:8000/
