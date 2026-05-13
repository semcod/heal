"""
Tests for heal.cli module.
"""

import os
from unittest.mock import patch
from click.testing import CliRunner
from heal.cli import main, last_shell_command, read_stdin


def test_main_help():
    """Test main help command."""
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Heal - LLM-powered shell error fixing." in result.output


def test_fix_command_no_input():
    """Test fix command with no input."""
    runner = CliRunner()
    with patch("heal.cli.ensure_config"), patch(
        "heal.cli.last_shell_command", return_value=""
    ), patch("heal.cli.read_stdin", return_value=""), patch(
        "heal.cli.get_last_output", return_value=""
    ), patch.dict(
        os.environ, {"HEAL_MODEL": "gpt-5.4-mini", "HEAL_API_KEY": "test-key"}
    ):
        result = runner.invoke(main, ["fix"])
        assert result.exit_code == 0
        assert "No error input detected" in result.output


@patch("heal.cli.ensure_config")
@patch("heal.cli.last_shell_command")
@patch("heal.cli.read_stdin")
@patch("heal.cli.call_llm")
def test_fix_command_with_input(mock_llm, mock_stdin, mock_cmd, mock_config):
    """Test fix command with input."""
    mock_config.return_value = None
    mock_cmd.return_value = "make dev"
    mock_stdin.return_value = "Error: file not found"
    mock_llm.return_value = "Try running: make clean && make dev"

    runner = CliRunner()
    with patch.dict(
        os.environ, {"HEAL_MODEL": "gpt-5.4-mini", "HEAL_API_KEY": "test-key"}
    ):
        result = runner.invoke(main, ["fix"])

    assert result.exit_code == 0
    assert "Try running: make clean && make dev" in result.output


def test_install_command():
    """Test install command (now redirects to init)."""
    runner = CliRunner()
    with patch("heal.cli.CONFIG_DIR") as mock_config_dir:
        mock_config_dir.__str__ = lambda: "/home/user/.heal"
        mock_config_dir.exists.return_value = True

        result = runner.invoke(main, ["install"], input="n\n")
        assert result.exit_code == 0
        assert (
            "deprecated" in result.output.lower()
            or "Heal bash integration created" in result.output
        )


def test_uninstall_command():
    """Test uninstall command."""
    runner = CliRunner()
    with patch("heal.cli.CONFIG_DIR") as mock_config_dir:
        mock_config_dir.__str__ = lambda: "/home/user/.heal"

        result = runner.invoke(main, ["uninstall"])
        assert result.exit_code == 0
        assert "Remember to remove the source line" in result.output


def test_last_shell_command():
    """Test last_shell_command function."""
    result = last_shell_command()
    assert isinstance(result, str)


def test_read_stdin():
    """Test read_stdin function."""
    with patch("sys.stdin.isatty", return_value=True):
        result = read_stdin()
        assert isinstance(result, str)
        assert result == ""
