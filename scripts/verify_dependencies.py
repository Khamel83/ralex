import subprocess

def check_gh_cli():
    try:
        subprocess.run(["gh", "--version"], check=True, capture_output=True)
        print("✅ GitHub CLI is installed.")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ GitHub CLI is not installed. Please install it to continue.")
        return False

if __name__ == "__main__":
    check_gh_cli()
