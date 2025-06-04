import subprocess

def run_powershell():
    while True:
        try:
            user_input = input("Fixr (PowerShell)> ")
            if user_input.strip().lower() in ("exit", "quit"):
                break

            result = subprocess.run(
                ["powershell", "-Command", user_input],
                capture_output=True,
                text=True
            )

            if result.stdout:
                print(result.stdout.strip())
            if result.stderr:
                print("[stderr]", result.stderr.strip())

        except KeyboardInterrupt:
            print("\nExiting Fixr Shell.")
            break

if __name__ == "__main__":
    run_powershell()
