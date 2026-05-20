# executor.py
import os
import subprocess

def execute_command(cmd):
    """
    Execute the parsed Gemini JSON command.
    """
    if not cmd:
        print("⚠️ No command to execute.")
        return

    action = cmd.get("action")
    filename = cmd.get("filename", "")
    content = cmd.get("content", "")
    new_name = cmd.get("new_name", "")

    try:
        if action == "create_file":
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ File created: {filename}")

        elif action == "edit_file":
            if os.path.exists(filename):
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"✅ File edited: {filename}")
            else:
                print(f"⚠️ File does not exist: {filename}")

        elif action == "append_file":
            if os.path.exists(filename):
                with open(filename, "a", encoding="utf-8") as f:
                    f.write(content)
                print(f"✅ Content appended to file: {filename}")
            else:
                print(f"⚠️ File does not exist: {filename}")

        elif action == "delete_file":
            if os.path.exists(filename):
                os.remove(filename)
                print(f"✅ File deleted: {filename}")
            else:
                print(f"⚠️ File does not exist: {filename}")

        elif action == "rename_file":
            if os.path.exists(filename):
                os.rename(filename, new_name)
                print(f"✅ File renamed: {filename} → {new_name}")
            else:
                print(f"⚠️ File does not exist: {filename}")

        elif action == "run_script":
            if os.path.exists(filename):
                result = subprocess.run(["python", filename], capture_output=True, text=True)
                print(f"🖥️ Script output:\n{result.stdout}")
            else:
                print(f"⚠️ File does not exist: {filename}")

        else:
            print(f"⚠️ Unknown action: {action}")

    except Exception as e:
        print(f"⚠️ Error executing command: {e}")