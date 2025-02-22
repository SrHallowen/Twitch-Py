import sys

# Python version check
if sys.version_info < (3, 12):
    print("Python 3.12 or newer is required!")
    print(f"Current version: {sys.version}")
    print("Download from: https://www.python.org/downloads/")
    sys.exit(1)

import subprocess
import os

def check_command_exists(command):
    """Check if a CLI command exists"""
    try:
        subprocess.run(
            [command, "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", package],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except subprocess.CalledProcessError:
        return False

# Dependency configuration
dependencies = [
    {
        "type": "command",
        "name": "twitch-dl",
        "package": "twitch-dl"
    },
    {
        "type": "python",
        "name": "questionary",
        "package": "questionary"
    }
]

print("🔍 Checking dependencies...")
installed_packages = False

for dep in dependencies:
    if dep["type"] == "command":
        if check_command_exists(dep["name"]):
            print(f"✅ {dep['name']} is available")
        else:
            print(f"📦 Installing {dep['package']}...")
            if install_package(dep["package"]):
                installed_packages = True
                print(f"✅ Successfully installed {dep['package']}")
            else:
                print(f"❌ Failed to install {dep['package']}")
                sys.exit(1)
    elif dep["type"] == "python":
        try:
            __import__(dep["name"])
            print(f"✅ {dep['package']} is installed")
        except ImportError:
            print(f"📦 Installing {dep['package']}...")
            if install_package(dep["package"]):
                installed_packages = True
                print(f"✅ Successfully installed {dep['package']}")
            else:
                print(f"❌ Failed to install {dep['package']}")
                sys.exit(1)

if installed_packages:
    print("🔄 Restarting to apply changes...")
    os.execv(sys.executable, [sys.executable] + sys.argv)

# Main application imports
import questionary

def listChannelVideos(channelName):
    subprocess.run(["twitch-dl", "videos", channelName])

def downloadTwitchVideo(videoId):
    subprocess.run(["twitch-dl", "download", videoId, "--quality", "source"])

if __name__ == "__main__":
    choiceUser = questionary.select(
        "\nSelect the type of media to download",
        choices=["List channel videos", "Download channel video"]
    ).ask()

    if choiceUser == "List channel videos":
        channelName = questionary.text("\nTwitch channel name:").ask()
        listChannelVideos(channelName)
    elif choiceUser == "Download channel video":
        videoId = questionary.text("\nTwitch video ID:").ask()
        downloadTwitchVideo(videoId)