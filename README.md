# Ralex - The "Always-Working" Wrapper for Claude Code

**A smart, reliable wrapper for the `claude-code` CLI that automatically falls back to a free model when you hit your usage limit.**

This script lets you use the official, interactive `claude-code` terminal application exactly as you normally would. When you exit a session, Ralex checks for a "usage limit" error. If it finds one, it will notify you and you can then re-run your prompt with the fallback model.

---

## The Problem We're Solving

You're in the middle of a coding session, relying on the fantastic interactive environment of `claude-code`. Suddenly, you hit your usage limit and get an error. Your flow is broken. You have to stop what you're doing and wait hours for your limit to reset.

## The Ralex Solution

With Ralex, this never happens. You use `ralex` instead of `claude-code`.

1.  **Normal Usage:** The `claude-code` interactive environment launches perfectly. You use it as you always do.
2.  **The Magic:** When you exit, Ralex inspects the session's output.
3.  **Seamless Fallback:** If it detects a "usage limit" error, it will notify you. You can then re-enter your last prompt to continue with the fallback model.

---

## How It *Actually* Works (The Technical Details)

It's important to understand how this works correctly, as previous versions of this script got it wrong.

-   **`claude-code` is an Application:** The `claude-code` command is not a simple script that prints text. It's a full-screen, interactive terminal application that takes over the display.
-   **The Wrong Way (What We Don't Do):** You cannot simply "pipe" or "redirect" the output of an interactive application like this. Trying to do so breaks the application and prevents it from ever launching.
-   **The Right Way (How Ralex Works):** Ralex uses the standard Unix `script` command. This command is designed specifically to capture the full output of an interactive terminal session.
    1.  `script -q -c "claude-code"` launches `claude-code` and transparently records everything that happens on the screen to a temporary file.
    2.  You interact with `claude-code` normally.
    3.  When you exit, Ralex opens the temporary log file.
    4.  It searches the log for the specific "usage limit" text.
    5.  If found, it will print a message informing you that the limit has been reached.

This approach respects the integrity of the `claude-code` application while still allowing us to inspect the results after it closes.

---

## Quick Start

### 1. Clone and Setup
```bash
git clone https://github.com/Khamel83/ralex.git
cd ralex

# Get your OpenRouter API key from https://openrouter.ai/
# It's free to sign up and use free models.
echo "OPENROUTER_API_KEY=your-key-here" > .env
```

### 2. Make the Script Executable
```bash
# This only needs to be done once.
chmod +x ralex-claude-code.sh
```

### 3. Create a Convenient Alias (Recommended)
To avoid typing the full path to the script every time, add an alias to your shell's startup file (`~/.zshrc`, `~/.bashrc`, or `~/.config/fish/config.fish`).

**Important:** You must replace `/path/to/your/ralex` with the actual, absolute path to where you cloned the repository.

```bash
# Add this line to your shell config file:
alias ralex='/path/to/your/ralex/ralex-claude-code.sh'

# Then, reload your shell or run:
source ~/.zshrc # Or your respective config file
```

### 4. Your New Daily Workflow
Instead of running `claude-code`, you now run `ralex`.

```bash
# This will launch the interactive claude-code session.
ralex

# If you hit your usage limit, upon exiting, Ralex will
# notify you. You can then re-enter your last prompt to
# continue with the fallback model.
```

---

## Project Structure

```
ralex/
├── README.md              # This file: The clear, correct documentation.
├── ralex-claude-code.sh   # The new, interactive-aware Ralex script.
├── .gitignore             # Protects your .env file.
└── .env.example           # An example of the .env file.
```
The old, incorrect script has been moved to the `archive/incorrect-simple-script` branch for historical purposes.
