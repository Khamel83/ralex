#!/bin/bash

# RalexOS Installation Instructions
# Copy and paste this to get started quickly

# 1. Download the complete setup script
curl -O https://raw.githubusercontent.com/yourusername/ralexos/main/ralexos-complete.sh

# 2. Make it executable
chmod +x ralexos-complete.sh

# 3. Edit the configuration values at the top of the script
#    Update these variables:
#    - OPENROUTER_API_KEY
#    - GITHUB_TOKEN
#    - GIT_USER_NAME
#    - GIT_USER_EMAIL

# 4. Run the setup
./ralexos-complete.sh

# 5. Restart your shell or source your profile
# source ~/.bashrc
# source ~/.zshrc

# 6. Start using OpenCode
# opencode

# Quick aliases available after setup:
# ocp  - Force Claude Pro model
# ocq  - Use Qwen3 Coder (free)
# ocg  - Use Gemini Flash
# ock  - Use Kimi K2 (free)
# oy   - Run one-shot command

echo "Installation instructions saved. Run 'cat INSTALL.md' to see them again."