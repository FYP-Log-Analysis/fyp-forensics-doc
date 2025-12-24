# Normalizer Source

**What's in this folder:**
- `__init__.py` - Makes this folder a Python package
- `normalize.py` - Main script that coordinates the cleaning process
- `application_norm.py` - Cleans Application log files
- `security_norm.py` - Cleans Security log files
- `system_norm.py` - Cleans System log files
- `powershell_norm.py` - Cleans PowerShell log files
- `utils.py` - Helper functions used by the other scripts

**Purpose:** These scripts take different types of Windows logs and clean them up so they all follow the same format. Each script specializes in one type of log (Security, System, Application, PowerShell).