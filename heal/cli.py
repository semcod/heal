#!/usr/bin/env python3
"""
CLI module for heal package - LLM-powered shell error fixing.
"""

import os
import sys
import subprocess
from pathlib import Path
import click

from dotenv import load_dotenv, set_key
from litellm import completion

CONFIG_DIR = Path.home() / ".heal"
ENV_PATH = CONFIG_DIR / ".env"

# Provider configurations with API key URLs and popular models
PROVIDERS = {
    "openrouter": {
        "name": "OpenRouter",
        "api_key_url": "https://openrouter.ai/keys",
        "base_url": "https://openrouter.ai/api/v1",
        "litellm_prefix": "openrouter/",  # Prefix for litellm
        "models": [
            ("openai/gpt-4o-mini", "GPT-4o Mini (fast, cheap, recommended)"),
            ("openai/gpt-4o", "GPT-4o (most capable)"),
            ("anthropic/claude-3.5-sonnet", "Claude 3.5 Sonnet (excellent reasoning)"),
            ("google/gemini-pro-1.5", "Gemini Pro 1.5 (long context)"),
            ("meta-llama/llama-3.1-70b-instruct", "Llama 3.1 70B (open source)"),
            ("qwen/qwen-2.5-72b-instruct", "Qwen 2.5 72B (multilingual)"),
            ("arcee-ai/trinity-large-preview:free", "Trinity Large (free, fast)"),
        ]
    },
    "openai": {
        "name": "OpenAI",
        "api_key_url": "https://platform.openai.com/api-keys",
        "base_url": None,
        "litellm_prefix": None,  # No prefix needed for OpenAI
        "models": [
            ("gpt-4o-mini", "GPT-4o Mini (fast, cheap, recommended)"),
            ("gpt-4o", "GPT-4o (most capable)"),
            ("gpt-4-turbo", "GPT-4 Turbo (previous generation)"),
            ("gpt-3.5-turbo", "GPT-3.5 Turbo (legacy, cheap)"),
        ]
    },
    "anthropic": {
        "name": "Anthropic",
        "api_key_url": "https://console.anthropic.com/settings/keys",
        "base_url": None,
        "litellm_prefix": None,  # No prefix needed for Anthropic
        "models": [
            ("claude-3-5-sonnet-20241022", "Claude 3.5 Sonnet (recommended)"),
            ("claude-3-opus-20240229", "Claude 3 Opus (most capable)"),
            ("claude-3-haiku-20240307", "Claude 3 Haiku (fast, cheap)"),
        ]
    },
    "google": {
        "name": "Google AI",
        "api_key_url": "https://aistudio.google.com/app/apikey",
        "base_url": None,
        "litellm_prefix": "gemini/",  # Prefix for Google models
        "models": [
            ("gemini-pro", "Gemini Pro (recommended)"),
            ("gemini-pro-vision", "Gemini Pro Vision (multimodal)"),
        ]
    },
}


def get_litellm_model_name(provider, model):
    """Convert model name to litellm format with provider prefix if needed."""
    provider_info = PROVIDERS.get(provider, {})
    prefix = provider_info.get("litellm_prefix")
    
    if prefix:
        # Check if model already has the prefix
        if not model.startswith(prefix):
            return f"{prefix}{model}"
    
    return model


def ensure_config():
    """Ensure configuration exists and prompt for missing values."""
    CONFIG_DIR.mkdir(exist_ok=True)

    if not ENV_PATH.exists():
        ENV_PATH.touch()

    load_dotenv(ENV_PATH)

    provider = os.getenv("HEAL_PROVIDER")
    api_key = os.getenv("HEAL_API_KEY")
    model = os.getenv("HEAL_MODEL")
    base_url = os.getenv("HEAL_BASE_URL")

    # Select provider if not configured
    if not provider:
        click.echo("\n🔧 First-time setup - Let's configure your LLM provider\n")
        click.echo("Available providers:")
        provider_list = list(PROVIDERS.keys())
        for i, prov_key in enumerate(provider_list, 1):
            prov_info = PROVIDERS[prov_key]
            default_marker = " (recommended)" if prov_key == "openrouter" else ""
            click.echo(f"  {i}. {prov_info['name']}{default_marker}")
        
        click.echo("\n💡 Tip: OpenRouter gives you access to all models with one API key")
        
        choice = click.prompt(
            "\nSelect provider",
            type=click.IntRange(1, len(provider_list)),
            default=1
        )
        provider = provider_list[choice - 1]
        set_key(ENV_PATH, "HEAL_PROVIDER", provider)

    provider_info = PROVIDERS.get(provider, PROVIDERS["openrouter"])

    # Get API key if not configured
    if not api_key:
        click.echo(f"\n🔑 Get your {provider_info['name']} API key here:")
        click.echo(f"   {click.style(provider_info['api_key_url'], fg='cyan', underline=True)}")
        click.echo()
        api_key = click.prompt("Enter your API key", type=str).strip()
        set_key(ENV_PATH, "HEAL_API_KEY", api_key)

    # Select model if not configured
    if not model:
        click.echo(f"\n🤖 Select a model from {provider_info['name']}:\n")
        models = provider_info['models']
        for i, (model_id, description) in enumerate(models, 1):
            click.echo(f"  {i}. {model_id}")
            click.echo(f"     {click.style(description, fg='bright_black')}")
        
        click.echo(f"\n  {len(models) + 1}. Custom (enter model name manually)")
        
        choice = click.prompt(
            "\nSelect model",
            type=click.IntRange(1, len(models) + 1),
            default=1
        )
        
        if choice <= len(models):
            model = models[choice - 1][0]
        else:
            model = click.prompt("Enter custom model name", type=str).strip()
        
        set_key(ENV_PATH, "HEAL_MODEL", model)

    # Set base URL for OpenRouter
    if provider == "openrouter" and not base_url:
        base_url = provider_info['base_url']
        set_key(ENV_PATH, "HEAL_BASE_URL", base_url)

    # Load into environment
    os.environ["HEAL_PROVIDER"] = provider
    os.environ["HEAL_API_KEY"] = api_key
    os.environ["HEAL_MODEL"] = model
    if base_url:
        os.environ["HEAL_BASE_URL"] = base_url


def last_shell_command():
    """Get the last shell command from buffer or history."""
    # First try to read from buffer (if heal init was used)
    cmd_file = CONFIG_DIR / "last_command.txt"
    if cmd_file.exists():
        try:
            return cmd_file.read_text().strip()
        except Exception:
            pass
    
    # Fallback to bash history
    try:
        out = subprocess.check_output(
            ["bash", "-lc", "fc -ln -1"],
            stderr=subprocess.DEVNULL,
            text=True
        )
        return out.strip()
    except Exception:
        return ""


def read_stdin():
    """Read from stdin if not a TTY."""
    if sys.stdin.isatty():
        return ""
    return sys.stdin.read()


def get_last_output():
    """Read the last captured output from shell hook."""
    # Try new buffer location first
    output_file = CONFIG_DIR / "last_output.txt"
    if output_file.exists():
        return output_file.read_text()
    
    # Fallback to old location for backwards compatibility
    old_output_file = CONFIG_DIR / "last_output.txt"
    if old_output_file.exists():
        return old_output_file.read_text()
    
    return ""


def call_llm(model, api_key, prompt, raise_on_error=False):
    """Call the LLM with the given prompt."""
    provider = os.getenv("HEAL_PROVIDER", "openrouter")
    base_url = os.getenv("HEAL_BASE_URL")
    
    # Format model name with provider prefix for litellm
    litellm_model = get_litellm_model_name(provider, model)
    
    # Set API key based on provider - litellm checks these env vars
    if provider == "openrouter":
        os.environ["OPENROUTER_API_KEY"] = api_key
        # Also set as generic key for litellm
        os.environ["OPENAI_API_KEY"] = api_key
    elif provider == "anthropic":
        os.environ["ANTHROPIC_API_KEY"] = api_key
    elif provider == "google":
        os.environ["GOOGLE_API_KEY"] = api_key
    else:
        os.environ["OPENAI_API_KEY"] = api_key

    try:
        kwargs = {
            "model": litellm_model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
        }
        
        if base_url:
            kwargs["api_base"] = base_url
        
        # For OpenRouter, also pass api_key explicitly
        if provider == "openrouter":
            kwargs["api_key"] = api_key
        
        resp = completion(**kwargs)
        return resp.choices[0].message.content
    except Exception as e:
        if raise_on_error:
            raise
        return f"Error calling LLM: {e}"


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    """Heal - LLM-powered shell error fixing."""
    if ctx.invoked_subcommand is None:
        ctx.invoke(fix)


@main.command()
@click.option('--model', help='Override the model')
@click.option('--api-key', help='Override the API key')
@click.option('--anonymize', is_flag=True, help='Anonymize sensitive data before sending to LLM')
@click.option('--privacy-check', is_flag=True, help='Check privacy masking availability')
def fix(model, api_key, anonymize, privacy_check):
    """Fix shell errors using LLM."""
    # Check privacy status if requested
    if privacy_check:
        from .privacy import get_privacy_status
        status = get_privacy_status()
        click.echo("\n🔒 Privacy Masking Status\n")
        click.echo(f"Active backends: {', '.join(status['backends'])}\n")
        click.echo("Backend availability:")
        click.echo(f"  {'✓' if True else '✗'} builtin_regex       (always available)")
        click.echo(f"  {'✓' if status['detect_secrets_installed'] else '✗'} detect-secrets      API keys, tokens, private keys")
        click.echo(f"  {'✓' if status['presidio_installed'] else '✗'} presidio-analyzer   Microsoft PII detection")
        click.echo(f"  {'✓' if status['priv_masker_installed'] else '✗'} priv-masker         Polish NLP masking")
        click.echo(f"  {'✓' if status['datafog_installed'] else '✗'} datafog             Lightweight PII detection")
        click.echo(f"  {'✓' if status['faker_installed'] else '✗'} faker               Fake data generation")
        if status['install_instructions']:
            click.echo(f"\n{status['install_instructions']}")
        click.echo()
        return
    
    ensure_config()

    if model:
        os.environ["HEAL_MODEL"] = model
    if api_key:
        os.environ["HEAL_API_KEY"] = api_key

    model = os.environ["HEAL_MODEL"]
    api_key = os.environ["HEAL_API_KEY"]

    last_cmd = last_shell_command()
    error_output = read_stdin() or get_last_output()

    if not error_output:
        click.echo("No error input detected on stdin or from shell hook.")
        click.echo("Tip: run your command like:")
        click.echo("  your_command 2>&1 | heal fix")
        click.echo("  # Or install shell hook with: heal install")
        return

    # Anonymize if requested
    if anonymize:
        from .privacy import anonymize_shell_output, get_privacy_status
        status = get_privacy_status()
        
        if not status['available']:
            click.echo("⚠️  Privacy masking not fully available.")
            click.echo("   Using basic regex-based masking as fallback.")
            if status['install_instructions']:
                click.echo(f"\n   For full privacy protection:\n{status['install_instructions']}\n")
        else:
            click.echo("🔒 Anonymizing sensitive data...\n")
        
        error_output = anonymize_shell_output(
            error_output,
            enable_privacy=True,
            mask_names=True,
            mask_dates=False,  # Keep dates for context
            mask_contacts=True,
            mask_addresses=True,
            mask_ids=True,
        )

    prompt = f"""
You are a CLI assistant that helps fix shell errors and command failures.

The user executed this command:
{last_cmd}

And got this output / error:
{error_output}

The user is currently in this directory: {os.getcwd()}

Your task:
- Explain briefly what went wrong
- Propose concrete shell commands or file edits to fix it
- Be concise and practical
- Focus on the most likely solution

If there's no obvious error, suggest debugging steps.
"""

    response = call_llm(model, api_key, prompt)
    click.echo(response)


@main.command()
def test():
    """Test heal with a simulated error to verify configuration."""
    click.echo("\n🧪 Testing heal configuration...\n")
    
    # Check if configured
    load_dotenv(ENV_PATH)
    provider = os.getenv("HEAL_PROVIDER")
    model = os.getenv("HEAL_MODEL")
    api_key = os.getenv("HEAL_API_KEY")
    
    if not all([provider, model, api_key]):
        click.echo("❌ Heal is not configured yet.")
        click.echo()
        if click.confirm("Would you like to configure it now?", default=True):
            ensure_config()
            click.echo("\n✅ Configuration complete! Running test...\n")
            # Reload config
            load_dotenv(ENV_PATH)
            provider = os.getenv("HEAL_PROVIDER")
            model = os.getenv("HEAL_MODEL")
            api_key = os.getenv("HEAL_API_KEY")
        else:
            click.echo("   Run 'heal config' when ready to set up.\n")
            return
    
    provider_info = PROVIDERS.get(provider, PROVIDERS["openrouter"])
    litellm_model = get_litellm_model_name(provider, model)
    
    click.echo(f"✓ Provider: {provider_info['name']}")
    click.echo(f"✓ Model: {model}")
    if litellm_model != model:
        click.echo(f"  (litellm format: {litellm_model})")
    click.echo(f"✓ API Key: {'*' * 20}{api_key[-4:]}")
    click.echo()
    
    # Simulate a common error
    simulated_command = "python app.py"
    simulated_error = """Traceback (most recent call last):
  File "app.py", line 3, in <module>
    from flask import Flask
ModuleNotFoundError: No module named 'flask'"""
    
    click.echo("📝 Simulating error:")
    click.echo(f"   Command: {simulated_command}")
    click.echo(f"   Error: ModuleNotFoundError: No module named 'flask'")
    click.echo()
    click.echo("🤖 Asking LLM for solution...\n")
    
    # Create test prompt
    prompt = f"""You are a CLI assistant that helps fix shell errors.

The user executed: {simulated_command}

And got this error:
{simulated_error}

Provide a brief, practical solution (2-3 sentences max)."""
    
    try:
        response = call_llm(model, api_key, prompt, raise_on_error=True)
        click.echo("💡 LLM Response:")
        click.echo("─" * 60)
        click.echo(response)
        click.echo("─" * 60)
        click.echo()
        click.echo("✅ Test successful! Heal is working correctly.")
        click.echo("   You can now use: command 2>&1 | heal")
    except Exception as e:
        error_str = str(e)
        click.echo("❌ Test failed!\n")
        click.echo("💡 Error Details:")
        click.echo("─" * 60)
        
        # Check for specific error types
        if "AuthenticationError" in error_str or "401" in error_str:
            click.echo("Authentication failed - your API key appears to be invalid.\n")
            click.echo("Possible causes:")
            click.echo("  • API key is incorrect or expired")
            click.echo("  • API key doesn't have proper permissions")
            click.echo("  • Wrong provider selected for this API key")
            click.echo()
            click.echo("Let's reconfigure your settings step by step:\n")
            
            # Ask what to reconfigure
            click.echo("What would you like to do?")
            click.echo("  1. Change provider and API key")
            click.echo("  2. Just update API key (keep current provider)")
            click.echo("  3. Try a different model (keep provider and key)")
            click.echo("  4. Cancel")
            
            choice = click.prompt("\nSelect option", type=click.IntRange(1, 4), default=1)
            
            if choice == 1:
                # Full reconfiguration
                click.echo("\n🔧 Full reconfiguration\n")
                # Clear everything from env file
                if ENV_PATH.exists():
                    ENV_PATH.unlink()
                # Clear env vars
                for key in ["HEAL_PROVIDER", "HEAL_API_KEY", "HEAL_MODEL", "HEAL_BASE_URL"]:
                    os.environ.pop(key, None)
                ensure_config()
                click.echo("\n✅ Reconfigured! Try running 'heal test' again.")
            elif choice == 2:
                # Just update API key
                click.echo("\n🔑 Update API key\n")
                provider = os.getenv("HEAL_PROVIDER", "openrouter")
                provider_info = PROVIDERS.get(provider, PROVIDERS["openrouter"])
                click.echo(f"Provider: {provider_info['name']}")
                click.echo(f"Get your API key: {click.style(provider_info['api_key_url'], fg='cyan', underline=True)}\n")
                new_api_key = click.prompt("Enter your new API key", type=str).strip()
                set_key(ENV_PATH, "HEAL_API_KEY", new_api_key)
                os.environ["HEAL_API_KEY"] = new_api_key
                click.echo("\n✅ API key updated! Try running 'heal test' again.")
            elif choice == 3:
                # Change model
                click.echo("\n🤖 Select a different model\n")
                provider = os.getenv("HEAL_PROVIDER", "openrouter")
                provider_info = PROVIDERS.get(provider, PROVIDERS["openrouter"])
                models = provider_info['models']
                for i, (model_id, description) in enumerate(models, 1):
                    click.echo(f"  {i}. {model_id}")
                    click.echo(f"     {click.style(description, fg='bright_black')}")
                click.echo(f"\n  {len(models) + 1}. Custom (enter model name manually)")
                
                model_choice = click.prompt("\nSelect model", type=click.IntRange(1, len(models) + 1), default=1)
                if model_choice <= len(models):
                    new_model = models[model_choice - 1][0]
                else:
                    new_model = click.prompt("Enter custom model name", type=str).strip()
                
                set_key(ENV_PATH, "HEAL_MODEL", new_model)
                os.environ["HEAL_MODEL"] = new_model
                click.echo(f"\n✅ Model changed to: {new_model}")
                click.echo("Try running 'heal test' again.")
            else:
                click.echo("\nRun 'heal config' when ready to fix your configuration.")
        elif "rate_limit" in error_str.lower():
            click.echo("Rate limit exceeded - you're making too many requests.\n")
            click.echo("Solutions:")
            click.echo("  • Wait a few minutes and try again")
            click.echo("  • Check your provider's rate limits")
            click.echo("  • Consider upgrading your plan")
        elif "insufficient" in error_str.lower() or "quota" in error_str.lower():
            click.echo("Insufficient credits or quota exceeded.\n")
            click.echo("Solutions:")
            click.echo("  • Add credits to your account")
            click.echo("  • Enable billing if not already enabled")
            click.echo("  • Check your usage limits")
        else:
            click.echo(f"{error_str}\n")
            click.echo("Troubleshooting:")
            click.echo("  1. Verify your API key is valid")
            click.echo("  2. Check you have credits/billing enabled")
            click.echo("  3. Ensure the model name is correct")
            click.echo("  4. Try a different model")
            click.echo()
            if click.confirm("Would you like to reconfigure?", default=False):
                click.echo("\nWhat would you like to do?")
                click.echo("  1. Full reconfiguration (provider, API key, model)")
                click.echo("  2. Just change the model")
                click.echo("  3. Cancel")
                
                choice = click.prompt("\nSelect option", type=click.IntRange(1, 3), default=2)
                
                if choice == 1:
                    # Full reconfiguration
                    if ENV_PATH.exists():
                        ENV_PATH.unlink()
                    for key in ["HEAL_PROVIDER", "HEAL_API_KEY", "HEAL_MODEL", "HEAL_BASE_URL"]:
                        os.environ.pop(key, None)
                    ensure_config()
                    click.echo("\n✅ Reconfigured! Try running 'heal test' again.")
                elif choice == 2:
                    # Just change model
                    provider = os.getenv("HEAL_PROVIDER", "openrouter")
                    provider_info = PROVIDERS.get(provider, PROVIDERS["openrouter"])
                    models = provider_info['models']
                    click.echo(f"\n🤖 Select a different model from {provider_info['name']}:\n")
                    for i, (model_id, description) in enumerate(models, 1):
                        click.echo(f"  {i}. {model_id}")
                        click.echo(f"     {click.style(description, fg='bright_black')}")
                    click.echo(f"\n  {len(models) + 1}. Custom (enter model name manually)")
                    
                    model_choice = click.prompt("\nSelect model", type=click.IntRange(1, len(models) + 1), default=1)
                    if model_choice <= len(models):
                        new_model = models[model_choice - 1][0]
                    else:
                        new_model = click.prompt("Enter custom model name", type=str).strip()
                    
                    set_key(ENV_PATH, "HEAL_MODEL", new_model)
                    os.environ["HEAL_MODEL"] = new_model
                    click.echo(f"\n✅ Model changed to: {new_model}")
                    click.echo("Try running 'heal test' again.")
        
        click.echo("─" * 60)


@main.command()
def init():
    """Initialize bash integration for automatic command capture."""
    shell_hook_path = CONFIG_DIR / "heal.bash"
    bashrc_path = Path.home() / ".bashrc"
    
    # Create improved shell hook with buffer
    hook_content = '''# Heal shell integration for automatic command and output capture
# This captures the last command and its output for easy error fixing

export HEAL_DIR="$HOME/.heal"
mkdir -p "$HEAL_DIR"

# Buffer files
export HEAL_LAST_CMD="$HEAL_DIR/last_command.txt"
export HEAL_LAST_OUT="$HEAL_DIR/last_output.txt"

# Capture command before execution
__heal_preexec() {
    # Save the command that's about to run
    echo "$1" > "$HEAL_LAST_CMD"
    
    # Start capturing output
    exec 3>&1 4>&2
    exec > >(tee "$HEAL_LAST_OUT") 2>&1
}

# Restore output after command execution
__heal_precmd() {
    local exit_code=$?
    
    # Restore normal output
    exec 1>&3 2>&4 2>/dev/null
    exec 3>&- 4>&- 2>/dev/null
    
    # Save exit code for reference
    echo "$exit_code" > "$HEAL_DIR/last_exit_code.txt"
    
    return $exit_code
}

# Set up the hooks
if [[ -n "$BASH_VERSION" ]]; then
    # Bash-specific setup
    trap '__heal_preexec "$BASH_COMMAND"' DEBUG
    PROMPT_COMMAND="__heal_precmd${PROMPT_COMMAND:+; $PROMPT_COMMAND}"
fi

# Helper function to show last command
heal-last() {
    if [[ -f "$HEAL_LAST_CMD" ]]; then
        echo "Last command:"
        cat "$HEAL_LAST_CMD"
    else
        echo "No command captured yet"
    fi
}

# Helper function to show last output
heal-output() {
    if [[ -f "$HEAL_LAST_OUT" ]]; then
        cat "$HEAL_LAST_OUT"
    else
        echo "No output captured yet"
    fi
}
'''
    
    CONFIG_DIR.mkdir(exist_ok=True)
    shell_hook_path.write_text(hook_content)
    
    click.echo("\n✅ Heal bash integration created!\n")
    click.echo(f"📄 Hook file: {shell_hook_path}\n")
    
    # Check if already in bashrc
    source_line = f"source {shell_hook_path}"
    already_installed = False
    
    if bashrc_path.exists():
        bashrc_content = bashrc_path.read_text()
        if str(shell_hook_path) in bashrc_content or "heal.bash" in bashrc_content:
            already_installed = True
    
    if already_installed:
        click.echo("ℹ️  Already installed in ~/.bashrc")
    else:
        click.echo("📝 To activate, add this line to your ~/.bashrc:")
        click.echo(f"   {click.style(source_line, fg='cyan')}")
        click.echo()
        
        if click.confirm("   Add to ~/.bashrc automatically?", default=True):
            try:
                with open(bashrc_path, 'a') as f:
                    f.write(f"\n# Heal - LLM-powered error fixing\n")
                    f.write(f"{source_line}\n")
                click.echo("   ✅ Added to ~/.bashrc")
            except Exception as e:
                click.echo(f"   ❌ Failed to update ~/.bashrc: {e}")
                click.echo(f"   Please add manually: {source_line}")
    
    click.echo()
    click.echo("🔄 To activate now, run:")
    click.echo(f"   source ~/.bashrc")
    click.echo()
    click.echo("📚 Usage after activation:")
    click.echo("   1. Run any command (it will be captured automatically)")
    click.echo("   2. If it fails, just run: heal")
    click.echo("   3. Heal will analyze the error and suggest fixes")
    click.echo()
    click.echo("💡 Helper commands:")
    click.echo("   heal-last    - Show last captured command")
    click.echo("   heal-output  - Show last captured output")


@main.command()
def install():
    """Install shell hook for automatic error capture (legacy, use 'heal init' instead)."""
    click.echo("ℹ️  Note: 'heal install' is deprecated. Use 'heal init' instead.\n")
    
    # Call init instead
    from click.testing import CliRunner
    runner = CliRunner()
    result = runner.invoke(init)
    click.echo(result.output)


@main.command()
def config():
    """Configure or reconfigure heal settings (provider, API key, model)."""
    CONFIG_DIR.mkdir(exist_ok=True)
    
    if not ENV_PATH.exists():
        ENV_PATH.touch()
    
    load_dotenv(ENV_PATH)
    
    click.echo("\n⚙️  Heal Configuration\n")
    
    # Show current configuration
    current_provider = os.getenv("HEAL_PROVIDER")
    current_model = os.getenv("HEAL_MODEL")
    
    if current_provider and current_model:
        click.echo(f"Current settings:")
        click.echo(f"  Provider: {PROVIDERS.get(current_provider, {}).get('name', current_provider)}")
        click.echo(f"  Model: {current_model}")
        click.echo()
        
        if not click.confirm("Do you want to reconfigure?", default=False):
            return
    
    # Clear existing configuration
    for key in ["HEAL_PROVIDER", "HEAL_API_KEY", "HEAL_MODEL", "HEAL_BASE_URL"]:
        if os.getenv(key):
            os.environ.pop(key, None)
    
    # Run configuration
    ensure_config()
    
    click.echo("\n✅ Configuration saved successfully!")
    click.echo(f"   Config file: {ENV_PATH}")


@main.command()
def uninstall():
    """Remove shell hook and configuration."""
    shell_hook_path = CONFIG_DIR / "heal.bash"
    output_file = CONFIG_DIR / "last_output.txt"
    
    if shell_hook_path.exists():
        shell_hook_path.unlink()
        click.echo("Shell hook removed.")
    
    if output_file.exists():
        output_file.unlink()
        click.echo("Output cache cleared.")
    
    click.echo("Remember to remove the source line from your ~/.bashrc")


if __name__ == "__main__":
    main()
