# Advance Steganography Application

This is an advance steganography application. You can sent messages securely.

## How to run in your machine

### Requirements

- Python 3
- Pip
- Venv (pip install virtualenv)
- Redis

### Installation

1. Clone The Repo

```bash
git clone https://github.com/sandippakhanna/steganography_chat_application.git
```

2. Go the folder

```bash
cd steganography_chat_application
```

3. Activate the venv

```bash
# create venv
python -m venv venv

# activate venv
venv\Scripts\activate
```

4. Install all dependency

```bash
pip install -r requirements.txt
```

5. Run Redis Server

```bash
redis-server
```

6. Migrate and Run the server

```bash
# migration
python manage.py migrate

# run the server
python manage.py runserver
```

7. Now open http://localhost:8000 in your browser.
