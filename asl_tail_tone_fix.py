import os
import shutil
import sys
import re

# Configuration paths
CONFIG_PATH = "/etc/asterisk/rpt.conf"
BACKUP_PATH = "/etc/asterisk/rpt.conf.bak"

def update_allstar_config():
    # 1. Root check
    if os.name != 'nt' and os.geteuid() != 0:
        print("Error: This script must be run with sudo.")
        return

    # 2. Create backup
    try:
        shutil.copyfile(CONFIG_PATH, BACKUP_PATH)
        print(f"Backup created at {BACKUP_PATH}")
    except FileNotFoundError:
        print(f"Error: {CONFIG_PATH} not found.")
        return

    # 3. Read configuration
    with open(CONFIG_PATH, "r") as f:
        lines = f.readlines()

    new_content = []
    startup_macro_found = False
    in_wait_times_stanza = False
    
    # Target values to update in [wait-times_hd]
    telemetry_updates = {
        "telemwait": "500",
        "idwait": "500",
        "unkeywait": "500"
    }

    # 4. Process file
    for line in lines:
        stripped = line.strip()

        # Step A: Find startup macro and insert wait/hang settings
        if ";startup_macro = *8132000" in stripped:
            startup_macro_found = True
            new_content.append(line)
            new_content.append("wait_time = wait-times_hd\n")
            new_content.append("hangtime = 100\n")
            print("Inserted wait_time and hangtime settings.")
            continue

        # Step B: Enter [wait-times_hd] stanza
        if stripped == "[wait-times_hd]":
            in_wait_times_stanza = True
            new_content.append(line)
            continue

        # Step C: Update telemetry values inside the stanza
        if in_wait_times_stanza:
            # Check if we've left the stanza
            if stripped.startswith("[") and stripped.endswith("]"):
                in_wait_times_stanza = False
            else:
                updated = False
                for key, val in telemetry_updates.items():
                    # Look for key = 100 (handling spaces and comments)
                    pattern = rf"^({key}\s*=\s*)100(\s*(;.*)?)$"
                    if re.match(pattern, stripped):
                        new_content.append(re.sub(pattern, rf"\g<1>{val}\g<2>", line))
                        print(f"Updated {key} to {val}.")
                        updated = True
                        break
                if updated:
                    continue

        new_content.append(line)

    # 5. Save and Reboot
    if startup_macro_found:
        with open(CONFIG_PATH, "w") as f:
            f.writelines(new_content)
        print("Configuration updated successfully.")
        
        choice = input("Reboot now to apply changes? (y/n): ").lower()
        if choice == 'y':
            os.system("sudo reboot")
    else:
        print("Error: Could not find the line ';startup_macro = *8132000'.")

if __name__ == "__main__":
    update_allstar_config()
