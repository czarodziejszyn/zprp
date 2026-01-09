# Uruchomienie

Opcja prosta (Makefile):
```bash
cd frontend
make run     # uruchomienie aplikacji
make test    # uruchomienie testów e2e
```

Opcja ręczna (bez Makefile):
```bash
cd frontend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
