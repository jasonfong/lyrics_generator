# Lyrics Generator

Song Lyrics Generator

# Local Testing

Install Python virtual environment:
```
python3 -m venv venv 
source venv/bin/activate
pip install -U -r dev-requirements.txt
```

Run local Flask server:
```
python main.py
```

Browse to test form:
http://localhost:8080/web/submit_line

# Deploying to Google App Engine

```
gcloud app deploy
```

# Updating Python Package Pins

```
pip-compile requirements.in
pip-compile dev-requirements.in
```
