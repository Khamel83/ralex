# `claude-code-router` Debugging Plan

## Summary of Problem

We have successfully configured the environment, API keys, and file locations, but the `ccr` server process is still not loading our custom `config-router.json`. It continues to load default providers (`codewhisperer-primary`, etc.) instead of our `openrouter` configuration.

This happens even when the config file is in the documented default location (`~/.claude-code-router/config-router.json`).

## New Hypothesis

The `ccr code` command is not just a client; its help text says it will "Start router and launch Claude Code with routing". This implies it can manage the server process itself. It is highly likely that the `--config` flag we discovered for the `start` command also works for the `code` command.

By passing the configuration file path directly to `ccr code`, we can bypass any issues with default paths or auto-detection and explicitly force it to use our settings.

## Plan for Next Session

1.  **Ensure a Clean Slate**: Kill any lingering `ccr` server processes to ensure no old versions are running.
    ```bash
    kill $(lsof -t -i:3456) 2>/dev/null || true
    ```

2.  **Run the Explicit Command**: Execute `ccr code` with the `--config` flag pointing directly to our configuration file. We will not run `ccr start &` separately.
    ```bash
    ccr code --config ~/.claude-code-router/config-router.json
    ```

3.  **Verify**: If this command successfully starts and routes to OpenRouter (we will see it in the logs), then we have found the correct, most reliable invocation.

4.  **Update Documentation**: If successful, I will update the `setup-claude-code-router.sh` script and the `CCR_QUICKSTART.md` documentation to reflect this new, more direct command.