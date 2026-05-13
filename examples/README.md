# Heal Examples

This directory contains real-world error examples and how `heal` helps fix them.

### [Python Errors](python_errors.md)
Common Python development errors:
- ModuleNotFoundError
- Circular imports
- IndentationError
- Virtual environment issues
- Permission errors
- Syntax errors

### [Docker Errors](docker_errors.md)
Docker and container-related errors:
- Port already in use
- Dockerfile COPY failures
- Permission denied in containers
- Network errors
- Image not found
- Out of disk space
- Container exits immediately

### [Node.js Errors](nodejs_errors.md)
Node.js and npm errors:
- Module not found
- Peer dependency conflicts
- Port already in use
- 404 package not found
- Build errors
- Syntax errors
- Permission errors (EACCES)
- Memory heap errors

### [Git Errors](git_errors.md)
Git version control errors:
- Merge conflicts
- Push rejected (non-fast-forward)
- Authentication failures
- Detached HEAD state
- Uncommitted changes blocking pull
- Large file errors
- Rebase conflicts
- Branch already exists

## How to Use These Examples

Each example shows:
1. **The Error** - What you see in your terminal
2. **Using heal** - How to pipe the error to heal
3. **Expected Solution** - What heal should suggest

# Simulate an error and fix it
python non_existent_script.py 2>&1 | heal

# Or after running a failing command
your_failing_command
heal
```

## Contributing Examples

Have a common error that should be documented? Please contribute!

1. Fork the repository
2. Add your example to the appropriate file
3. Follow the existing format
4. Submit a pull request

### Error
\`\`\`bash
$ command that fails
error output here
\`\`\`

### Using heal
\`\`\`bash
$ command that fails 2>&1 | heal
\`\`\`

### Expected Solution
\`\`\`
Explanation of what went wrong

**Solution:**
1. Step-by-step fix
   \`\`\`bash
   commands to run
   \`\`\`
\`\`\`
```

## Additional Resources

- [Main README](../README.md) - Installation and quick start
- [CHANGELOG](../CHANGELOG.md) - Version history
- [TODO](../TODO.md) - Planned features
