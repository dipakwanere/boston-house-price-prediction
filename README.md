This is a Boston House Price Prediction with a Linear Regression model. 

### Tools & Software requirement
- **Githubb Account**: [github.com](https://github.com)
- **VS Code IDE**: [code.visualstudio.com](https://code.visualstudio.com/)
- **Heroku**: [heroku.com](https://www.heroku.com/)
- **GitCLI**: [git-scm.com](https://git-scm.com/)

### Virtual environment (venv)
- Create venv (from project root):
```bash
python -m venv venv
```

- Activate venv:
  - PowerShell:
  ```powershell
  .\venv\Scripts\Activate.ps1
  # If blocked, run once in the same session:
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  .\venv\Scripts\Activate.ps1
  ```
  - Command Prompt (CMD):
  ```bat
  venv\Scripts\activate.bat
  ```
  - Git Bash / WSL:
  ```bash
  source venv/Scripts/activate
  ```

- Deactivate venv:
```bash
deactivate
```

### Install dependencies
```bash
pip install -r requirements.txt
```