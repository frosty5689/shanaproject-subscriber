# Shana Project Subscriber 🎬

An automated Python script designed to instantly follow all anime titles for any given season on **Shana Project**, with strict user configuration overrides. 

It automatically locks down your seasonal tracking list to custom quality options (**1080p Only (HD)**), bit profile standards (**Prefer 8-bit**), and specified **fansub groups** (via backend dynamic AJAX lookups) without manual web entry.

## ✨ Features

- **Isolated Execution:** Zero pollution of your operating system's global Python configuration.
- **Dynamic Parameterization:** Pass target seasons, target years, and target subbers directly via the CLI terminal.
- **Form Payload Replication:** Accurately replicates browser authentication tokens and header data mappings (`HTTP 302` verification handling).
- **Automated Anti-Bot Throttling:** Built-in sleep pacing preserves backend account session health.

---

## 🛠️ Installation & Setup

### 1. Project Directory Isolation
Clone or move your project components into an isolated local folder path:
```bash
git clone https://github.com/frosty5689/shanaproject-subscriber
cd shanaproject-subscriber
```

### 2. Establish the Virtual Environment (`venv`)

Select your operating system parameters below to generate your secure dependencies layer:

#### 💻 Linux & macOS
```bash
# Initialize isolated directory environment
python3 -m venv venv

# Activate local scope parameters
source venv/bin/activate

# Upgrade pipeline and install required packages
pip install --upgrade pip
pip install -r requirements.txt
```

#### 🪟 Windows (PowerShell)
```powershell
# Initialize isolated directory environment
python -m venv venv

# Activate local scope parameters
.\venv\Scripts\Activate.ps1

# Upgrade pipeline and install required packages
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🔒 Security Configuration (Environment Variables)

To protect your login details from accidentally being hardcoded or leaked into your git commit history, the script reads your Shana Project parameters directly from the native environment space.

Before executing the python process, declare your parameters in your open shell console instance:

### 💻 Linux / macOS Environment Variables
```bash
export SHANAPROJECT_USER="YourActualUsername"
export SHANAPROJECT_PASS="YourSecurePassword"
```

### 🪟 Windows PowerShell Environment Variables
```powershell
$env:SHANAPROJECT_USER="YourActualUsername"
$env:SHANAPROJECT_PASS="YourSecurePassword"
```

---

## 🚀 Execution & Command Syntax

Once your environment variables are set and your `venv` is active, execute the script by formatting your command layout as follows:

```bash
python subscribe_season.py [Season] [Year] [Preferred Subber Name]
```

### Examples:

#### A. Subscribe to a specific season using an explicit Fansub Group (Dynamic Lookup):
```bash
python subscribe_season.py Fall 2026 Erai-raws
```
*(Locks down rulesets targeting `Fall 2026` shows to `Erai-raws` only, forcing 1080p and 8-bit).*

#### B. Track an upcoming season using an alternative Group:
```bash
python subscribe_season.py Winter 2027 SubsPlease
```

#### C. Track an entire season using the "Don't care" Subber Fallback:
If no subber name argument is passed, the automator leaves the subber tag blank (`subber_tag=`), matching Shana Project's internal **"Don't care"** rule tracking structure.
```bash
python subscribe_season.py Fall 2026
```

---

## 🛑 Clean Up & Exit
When your automated bulk-subscription run finishes syncing your profile settings, deactivate your isolated shell context safely:
```bash
deactivate
```
