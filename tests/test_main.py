"""
Tests for heal.main module.
"""

from heal.main import hello, get_version, ShellHealer


def test_hello():
    """Test hello function."""
    result = hello()
    assert isinstance(result, str)
    assert "heal package" in result
    assert "LLM-powered" in result


def test_get_version():
    """Test get_version function."""
    from heal import __version__

    result = get_version()
    assert isinstance(result, str)
    # Compare against the package's own version source; a hardcoded literal
    # breaks on every automated release bump.
    assert result == __version__
    assert result.count(".") == 2


def test_shell_healer_init():
    """Test ShellHealer initialization."""
    healer = ShellHealer()
    assert healer.name == "ShellHealer"

    healer_custom = ShellHealer("CustomHealer")
    assert healer_custom.name == "CustomHealer"


def test_shell_healer_heal():
    """Test ShellHealer heal method."""
    healer = ShellHealer()
    command = "make dev"
    error = "Error: file not found"

    result = healer.heal(command, error)
    assert isinstance(result, str)
    assert command in result
    assert error[:100] in result


def test_shell_healer_str():
    """Test ShellHealer string representation."""
    healer = ShellHealer("TestHealer")
    result = str(healer)
    assert result == "ShellHealer(TestHealer)"
