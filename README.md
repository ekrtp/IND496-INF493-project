quickstart:
```bash
python -m venv .venv
```
(for windows - powershell)
```bash
.\.venv\Scripts\Activate.ps1
```

(for mac)
```bash
source .venv/bin/activate
```

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

(auto)
```bash
.\start.ps1
```

(manuel)
Terminal 1 (Backend):
```bash
# Windows PowerShell
\.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# macOS / Linux (zsh/bash)
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Terminal 2 (Streamlit UI):
```bash
# Windows PowerShell
\.\.venv\Scripts\Activate.ps1
streamlit run streamlit_app.py

# macOS / Linux (zsh/bash)
source .venv/bin/activate
streamlit run streamlit_app.py
```
---

python version: 3.10.3