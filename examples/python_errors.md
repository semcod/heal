# Python Error Examples

This document shows real-world Python errors and how `heal` helps fix them.

### Error
```bash
$ python app.py
Traceback (most recent call last):
  File "app.py", line 3, in <module>
    from flask import Flask
ModuleNotFoundError: No module named 'flask'
```

### Using heal
```bash
$ python app.py 2>&1 | heal
```

### Expected Solution
```
The error indicates that the Flask module is not installed in your Python environment.

**Solution:**
1. Install Flask using pip:
   ```bash
   pip install flask
   ```

2. If you're using a virtual environment, make sure it's activated:
   ```bash
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate  # Windows
   ```

3. If you have a requirements.txt, install all dependencies:
   ```bash
   pip install -r requirements.txt
   ```
```

### Error
```bash
$ python main.py
Traceback (most recent call last):
  File "main.py", line 1, in <module>
    from models import User
  File "/app/models.py", line 2, in <module>
    from main import db
ImportError: cannot import name 'db' from partially initialized module 'main'
```

### Using heal
```bash
$ python main.py 2>&1 | heal
```

### Expected Solution
```
You have a circular import issue. The file `main.py` imports from `models.py`, 
and `models.py` tries to import from `main.py`, creating a circular dependency.

**Solution:**
1. Move the `db` initialization to a separate file (e.g., `database.py`):
   ```python
   # database.py
   from flask_sqlalchemy import SQLAlchemy
   db = SQLAlchemy()
   ```

2. Import `db` from `database.py` in both files:
   ```python
   # main.py
   from database import db
   
   # models.py
   from database import db
   ```

3. Or use lazy imports by moving the import inside a function.
```

### Error
```bash
$ python script.py
  File "script.py", line 8
    return result
    ^
IndentationError: unexpected indent
```

### Using heal
```bash
$ python script.py 2>&1 | heal
```

### Expected Solution
```
Python detected an unexpected indentation on line 8. This usually happens when:
- You mixed tabs and spaces
- You have inconsistent indentation levels

**Solution:**
1. Check line 8 and ensure it's properly indented
2. Use consistent indentation (4 spaces is Python standard)
3. Configure your editor to show whitespace characters
4. Run a linter to fix indentation:
   ```bash
   autopep8 --in-place script.py
   # or
   black script.py
   ```
```

### Error
```bash
$ python manage.py runserver
/usr/bin/python3: No module named django
```

### Using heal
```bash
$ python manage.py runserver 2>&1 | heal
```

### Expected Solution
```
Django is not found in your system Python. You likely need to activate your 
virtual environment where Django is installed.

**Solution:**
1. Activate your virtual environment:
   ```bash
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate  # Windows
   ```

2. Verify Django is installed:
   ```bash
   pip list | grep -i django
   ```

3. If not installed, install it:
   ```bash
   pip install django
   ```

4. Alternative: Use the virtual environment's Python directly:
   ```bash
   ./venv/bin/python manage.py runserver
   ```
```

### Error
```bash
$ python setup.py install
error: could not create '/usr/local/lib/python3.9/site-packages': Permission denied
```

### Using heal
```bash
$ python setup.py install 2>&1 | heal
```

### Expected Solution
```
You're trying to install a package to a system directory without proper permissions.

**Solution (choose one):**

1. **Recommended**: Install in user space:
   ```bash
   pip install --user .
   ```

2. Use a virtual environment (best practice):
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install .
   ```

3. Use sudo (not recommended):
   ```bash
   sudo python setup.py install
   ```

4. Use pip instead of setup.py (modern approach):
   ```bash
   pip install .
   ```
```

### Error
```bash
$ python app.py
  File "app.py", line 15
    if x = 5:
         ^
SyntaxError: invalid syntax
```

### Using heal
```bash
$ python app.py 2>&1 | heal
```

### Expected Solution
```
You're using the assignment operator `=` instead of the comparison operator `==` 
in an if statement.

**Solution:**
Change line 15 from:
```python
if x = 5:
```

To:
```python
if x == 5:
```

**Explanation:**
- `=` is for assignment (setting a value)
- `==` is for comparison (checking equality)
- Use `=` when you want to assign: `x = 5`
- Use `==` when you want to compare: `if x == 5:`
```
