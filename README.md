# AllStar-Tail-Tone-Fix

A simple Python-based automation tool to adjust timing and telemetry settings for AllStarLink (ASL) nodes. This script eliminates the manual searching and editing of `rpt.conf` by programmatically inserting wait times and updating telemetry delay values.

## 🛠 Features
- **Automatic Backup**: Creates a `.bak` copy of your `rpt.conf` before making any changes.
- **Automated Insertion**: Finds the `startup_macro` and inserts `wait_time` and `hangtime` settings.
- **Telemetry Update**: Specifically targets the `[wait-times_hd]` stanza to update `telemwait`, `idwait`, and `unkeywait` from 100ms to 500ms.
- **Safety First**: Includes root privilege checks and regex-based matching to handle comments and whitespace.

## 📋 Prerequisites
- An active AllStarLink node (ASL 1.x, 2.x, or 3.0).
- Python 3.x installed.
- Sudo/Root access to the `/etc/asterisk/` directory.

## 🚀 Usage

1. **Clone the repository:**
   ```bash
   wget https://github.com/fahadmieaji/AllStar-Tail-Tone-Fix/raw/refs/heads/main/asl_tail_tone_fix.py
   ```

2. **Run the script with sudo:**
   ```bash
   sudo python3 asl_tail_tone_fix.py
   ```

3. **Follow the prompt:**
   The script will confirm each change. At the end, you will be asked if you'd like to reboot to apply the changes immediately.

## ⚙️ What the script modifies
The script automates the following manual steps in `/etc/asterisk/rpt.conf`:

- **Inserts under `;startup_macro = *8132000`:**
  ```ini
  wait_time = wait-times_hd
  hangtime = 100
  ```

- **Updates in `[wait-times_hd]`:**
  Changes the following values from **100** to **500**:
  - `telemwait`
  - `idwait`
  - `unkeywait`

## ⚠️ Disclaimer
*Always verify your configuration manually if you have highly customized `rpt.conf` files. While this script creates backups, it is your responsibility to ensure your node is operating within your local coordination guidelines.*

## 🤝 Contributing
Feel free to fork this project, submit pull requests, or report issues!
