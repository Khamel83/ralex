#!/bin/bash

# RalexOS Distribution Packager
# Creates a single distributable file with everything needed

# Create a directory for distribution
DIST_DIR="/tmp/ralexos-dist"
mkdir -p "$DIST_DIR"

# Copy all relevant files
cp /home/ubuntu/dev/RalexOS/ralexos-complete.sh "$DIST_DIR/"
cp /home/ubuntu/dev/RalexOS/README.md "$DIST_DIR/"
cp /home/ubuntu/dev/RalexOS/INSTALL.md "$DIST_DIR/"
cp /home/ubuntu/dev/RalexOS/demo.sh "$DIST_DIR/"

# Create a simple installation script
cat > "$DIST_DIR/install.sh" << 'EOF'
#!/bin/bash

echo "RalexOS Installer"
echo "================"

# Make the main script executable
chmod +x ralexos-complete.sh

# Show installation instructions
echo "Setup files copied to current directory."
echo "To install RalexOS:"
echo "1. Edit ralexos-complete.sh and set your configuration values"
echo "2. Run: ./ralexos-complete.sh"
echo "3. Follow the on-screen instructions"

echo
echo "For detailed instructions, see INSTALL.md"
echo "For full documentation, see README.md"
EOF

chmod +x "$DIST_DIR/install.sh"

# Create a simple README for the distribution
cat > "$DIST_DIR/DISTRIBUTION-README.md" << 'EOF'
# RalexOS Distribution Package

This package contains everything you need to set up RalexOS on any machine.

## Contents

1. `ralexos-complete.sh` - The main setup script
2. `README.md` - Full documentation
3. `INSTALL.md` - Quick installation guide
4. `demo.sh` - Demonstration script
5. `install.sh` - Simple installer

## Installation

1. Extract this package to a directory
2. Edit `ralexos-complete.sh` to set your configuration values:
   - OPENROUTER_API_KEY
   - GITHUB_TOKEN
   - GIT_USER_NAME
   - GIT_USER_EMAIL
3. Run the setup: `./ralexos-complete.sh`
4. Follow the on-screen instructions

## Platform Support

This package works on:
- macOS (Intel and Apple Silicon)
- Ubuntu/Debian
- Other Linux distributions
- Raspberry Pi
- VPS servers

## Getting Started

After installation:
1. Restart your shell or source your profile
2. Run `opencode` to start the AI assistant
3. Try the aliases: `ocp`, `ocq`, `ocg`, `ock`, `oy`

## Documentation

See README.md for complete documentation and usage instructions.
EOF

# Create a zip file of the distribution
cd /tmp
zip -r ralexos-dist.zip ralexos-dist

echo "Distribution package created at /tmp/ralexos-dist.zip"
echo "Contents:"
ls -la /tmp/ralexos-dist/

# Clean up
rm -rf /tmp/ralexos-dist