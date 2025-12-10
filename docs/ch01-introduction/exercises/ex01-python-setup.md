---
exercise_id: ex01-01-python-setup
chapter: ch01-introduction
title: "Python and PyBullet Environment Setup"
learning_outcome: "Install and verify Python 3.9+, PyBullet, and essential robotics libraries"
difficulty: beginner
estimated_time: "30-45 minutes"
prerequisites:
  - "Basic familiarity with command line/terminal"
  - "Administrator/sudo access to install software"
tools:
  - Python 3.9+
  - pip (Python package manager)
  - PyBullet
  - NumPy
  - Matplotlib
---

# Exercise: Python and PyBullet Environment Setup

## Overview

In this exercise, you'll set up your Python development environment for robotics simulation. You'll install Python 3.9 or higher, the PyBullet physics simulator, and essential scientific computing libraries (NumPy, Matplotlib, SciPy). Finally, you'll verify your installation by running a test script that checks all dependencies.

**What you'll build**: A working Python environment with all packages required for this textbook's exercises

**Why it matters**: Every chapter includes hands-on code exercises using PyBullet for robot simulation. Setting up your environment correctly ensures smooth progress through the textbook.

**Real-world application**: Professional robotics engineers use Python extensively for rapid prototyping, simulation, and algorithm development before deploying to real hardware. PyBullet is used by leading research labs (Google DeepMind, OpenAI, CMU) for robot learning experiments.

---

## Setup Instructions

### System Requirements

- **Operating System**: Windows 10/11, Ubuntu 20.04+, or macOS 11+
- **Python**: 3.9, 3.10, or 3.11 (Python 3.12+ may have compatibility issues with some packages)
- **RAM**: 4GB minimum (8GB recommended for complex simulations)
- **Disk Space**: 2GB for Python, packages, and dependencies
- **Graphics**: OpenGL-capable GPU for PyBullet GUI (optional but recommended)

---

### Installation

#### **Windows**

**Step 1: Install Python**

Download Python from [https://www.python.org/downloads/](https://www.python.org/downloads/)

- Choose Python 3.11.x (latest 3.11 release)
- **Important**: Check "Add Python to PATH" during installation
- Verify installation:

```bash
python --version
# Expected output: Python 3.11.x
```

**Step 2: Upgrade pip**

```bash
python -m pip install --upgrade pip
```

**Step 3: Install Required Packages**

```bash
pip install numpy==1.24.0 matplotlib==3.7.0 scipy==1.10.0 pybullet==3.2.5
```

Installation will take 2-5 minutes depending on your internet speed.

---

#### **Linux (Ubuntu/Debian)**

**Step 1: Install Python and pip**

```bash
sudo apt update
sudo apt install python3.9 python3-pip python3.9-venv
```

**Step 2: Create Virtual Environment (Recommended)**

```bash
python3.9 -m venv ~/robotics-env
source ~/robotics-env/bin/activate
```

**Step 3: Install Required Packages**

```bash
pip install numpy==1.24.0 matplotlib==3.7.0 scipy==1.10.0 pybullet==3.2.5
```

---

#### **macOS**

**Step 1: Install Homebrew (if not already installed)**

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Step 2: Install Python**

```bash
brew install python@3.11
```

**Step 3: Install Required Packages**

```bash
pip3 install numpy==1.24.0 matplotlib==3.7.0 scipy==1.10.0 pybullet==3.2.5
```

---

### Verify Installation

**Step 1: Create Test Script**

Create a file named `verify_environment.py` with the following content:

```python
"""
Environment Verification Script for Physical AI Textbook
Tests all required package installations
"""

import sys

def check_python_version():
    """Verify Python version is 3.9+"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")

    if version.major == 3 and version.minor >= 9:
        print("✓ Python version check passed\n")
        return True
    else:
        print("✗ Python 3.9+ required\n")
        return False

def check_package(package_name):
    """Try importing a package and report result"""
    try:
        module = __import__(package_name)
        version = getattr(module, '__version__', 'unknown')
        print(f"✓ {package_name:15s} version {version}")
        return True
    except ImportError:
        print(f"✗ {package_name:15s} NOT INSTALLED")
        return False

def main():
    """Run all verification checks"""
    print("=" * 60)
    print("Physical AI Textbook - Environment Verification")
    print("=" * 60)
    print()

    # Check Python version
    python_ok = check_python_version()

    # Check required packages
    print("Checking required packages:")
    packages = ['numpy', 'matplotlib', 'scipy', 'pybullet']
    results = {pkg: check_package(pkg) for pkg in packages}
    print()

    # Summary
    all_ok = python_ok and all(results.values())
    print("=" * 60)
    if all_ok:
        print("✓ SUCCESS: Environment setup complete!")
        print("You're ready to begin the exercises.")
    else:
        print("✗ FAILURE: Some requirements missing")
        print("Re-run installation commands above")
    print("=" * 60)

    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
```

**Step 2: Run Test Script**

```bash
python verify_environment.py
```

**Expected Output:**

```
============================================================
Physical AI Textbook - Environment Verification
============================================================

Python version: 3.11.5
✓ Python version check passed

Checking required packages:
✓ numpy           version 1.24.0
✓ matplotlib      version 3.7.0
✓ scipy           version 1.10.0
✓ pybullet        version 325

============================================================
✓ SUCCESS: Environment setup complete!
You're ready to begin the exercises.
============================================================
```

---

### Troubleshooting Setup

**Issue 1: "python: command not found"**
- **Windows**: Python not added to PATH during installation. Reinstall Python with "Add to PATH" checked.
- **Linux/macOS**: Try `python3` instead of `python`

**Issue 2: "ModuleNotFoundError: No module named 'numpy'"**
- **Solution**: Ensure pip installed packages to correct Python version:
  ```bash
  python -m pip install numpy  # Use same python command you run scripts with
  ```

**Issue 3: "Permission denied" when installing packages**
- **Windows**: Run Command Prompt as Administrator
- **Linux/macOS**: Use `pip install --user` flag or create virtual environment

**Issue 4: PyBullet GUI not opening**
- **Check**: Graphics drivers are up to date
- **Test**: Try headless mode in Python:
  ```python
  import pybullet as p
  p.connect(p.DIRECT)  # Headless mode (no GUI)
  print("PyBullet connected successfully!")
  ```
- **Windows**: May need Visual C++ Redistributable: https://aka.ms/vs/17/release/vc_redist.x64.exe

**Issue 5: Import errors with numpy on Windows**
- **Solution**: Install Microsoft Visual C++ Build Tools
- **Link**: https://visualstudio.microsoft.com/visual-cpp-build-tools/

---

## Problem Statement

**Task**: Install Python 3.9+, PyBullet, and all required packages; verify installation with test script

**Success Criteria**:
- [x] Python 3.9 or higher installed and accessible from command line
- [x] All packages (numpy, matplotlib, scipy, pybullet) installed without errors
- [x] Verification script outputs "SUCCESS" message
- [x] Can import all packages in Python interpreter without errors

**Deliverable**: Screenshot or copy-paste of successful verification script output

---

## Step-by-Step Instructions

### Part 1: Installation (20 minutes)

1. **Download and Install Python**
   - Go to python.org and download Python 3.11.x
   - Run installer (check "Add to PATH" on Windows)
   - Verify: `python --version`

2. **Upgrade pip**
   - Run: `python -m pip install --upgrade pip`
   - Verify: `pip --version` (should be 23.0+)

3. **Install Packages**
   - Run: `pip install numpy matplotlib scipy pybullet`
   - Wait for downloads to complete (2-5 minutes)

### Part 2: Verification (10 minutes)

1. **Create Test Script**
   - Copy the `verify_environment.py` code above into a new file
   - Save in a folder like `~/robotics-exercises/`

2. **Run Verification**
   - Navigate to folder: `cd ~/robotics-exercises/`
   - Run: `python verify_environment.py`
   - Check output for "SUCCESS" message

3. **Test PyBullet GUI**
   - Create a file `test_pybullet.py`:
   ```python
   import pybullet as p
   import time

   # Connect to PyBullet with GUI
   p.connect(p.GUI)
   print("PyBullet GUI opened successfully!")
   print("Close the window to exit.")

   # Keep GUI open for 5 seconds
   time.sleep(5)
   p.disconnect()
   ```
   - Run: `python test_pybullet.py`
   - A 3D visualization window should open

### Part 3: Documentation (5 minutes)

1. **Take Screenshot**
   - Capture successful verification output
   - Capture PyBullet GUI window (optional)

2. **Note Your Configuration**
   - Operating System: _______________
   - Python Version: _______________
   - Any issues encountered: _______________

---

## Expected Output

After completing this exercise, you should have:

1. **Working Python installation** (3.9+)
2. **All required packages installed**: numpy, matplotlib, scipy, pybullet
3. **Successful verification script output**
4. **PyBullet GUI functional** (or headless mode working)

**Save your verification output**—you'll need a working environment for all subsequent exercises!

---

## Extensions (Optional)

If you finish early or want to explore further:

1. **Virtual Environment Setup**
   - Create an isolated environment for this textbook:
   ```bash
   python -m venv physical-ai-env
   source physical-ai-env/bin/activate  # Linux/macOS
   physical-ai-env\Scripts\activate     # Windows
   ```
   - Reinstall packages in virtual environment

2. **Jupyter Notebook Installation**
   - Install Jupyter for interactive development:
   ```bash
   pip install jupyter
   jupyter notebook
   ```
   - Useful for experimenting with code snippets

3. **IDE Setup**
   - Install Visual Studio Code: https://code.visualstudio.com/
   - Install Python extension for syntax highlighting and debugging
   - Configure Python interpreter in VS Code

4. **Test Additional Packages**
   - Install optional packages for later chapters:
   ```bash
   pip install opencv-python scikit-learn pandas
   ```

---

## Rubric

**Assessment Criteria** (Total: 10 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Python 3.9+ installed | 2 | Correct version accessible from command line |
| Packages installed | 3 | All 4 packages (numpy, matplotlib, scipy, pybullet) installed |
| Verification script runs | 2 | Script executes without errors |
| Verification passes | 2 | Script outputs "SUCCESS" message |
| Documentation | 1 | Screenshot or output copy provided |

**Passing Grade**: 7/10 or higher

---

## Next Exercise

Once your environment is set up, proceed to **[Exercise 2: First Robot Simulation](ex02-first-simulation.md)** where you'll load a humanoid robot model and explore joint control in PyBullet.

---

## Need Help?

- **Textbook**: Review Chapter 1 Code Examples for additional context
- **PyBullet Documentation**: https://docs.google.com/document/d/10sXEhzFRSnvFcl3XxNGhnD4N2SedqwdAvK3dsihxVUA/
- **Stack Overflow**: Search for "[pybullet] installation" for common issues
- **Appendix**: See Appendix A (coming soon) for detailed platform-specific troubleshooting
