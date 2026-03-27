# Commit Message Template

Use this template for writing clear, descriptive commit messages.

## Format

```
<type>: <short summary (50 chars or less)>

<detailed description (wrap at 72 chars)>

Why:
- Explain the motivation for the change
- What problem does it solve?

What:
- List the main changes made
- Be specific about files/components affected

Impact:
- What areas are affected?
- Any breaking changes?
- Performance implications?

Related: #<issue-number> (if applicable)
```

## Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, no logic change)
- **refactor**: Code refactoring (no functional change)
- **test**: Adding or updating tests
- **chore**: Maintenance tasks (dependencies, build, etc.)
- **perf**: Performance improvements
- **ci**: CI/CD changes

## Examples

### Good Commit Message

```
refactor: Remove emoji characters from CI workflow for compatibility

Replace emoji characters (❌, ✅, ⚠️) with text prefixes [ERROR], 
[SUCCESS], [WARNING] in GitHub Actions workflow to ensure consistent 
output across different terminal environments and CI systems.

Why:
- Some CI environments don't render emojis correctly
- Text prefixes are more universally compatible
- Improves log parsing and grep-ability

What:
- Updated all echo statements in .github/workflows/validate.yml
- Standardized error/success/warning message format
- Added consistent [PREFIX] pattern throughout

Impact:
- CI output more readable in all environments
- No functional changes to validation logic
- Easier to parse logs programmatically

Related: #123
```

### Bad Commit Message

```
changes on deployment
```

**Problems:**
-  Too vague - what changes?
-  No explanation of why
-  No context about impact
-  Doesn't mention 1,302 lines deleted

## Setup

To use this template automatically:

```bash
git config commit.template .github/COMMIT_TEMPLATE.md
```

## Tips

1. **First line**: Imperative mood ("Add feature" not "Added feature")
2. **Body**: Explain the "why" not just the "what"
3. **Be specific**: Mention file names, functions, or components
4. **Break it down**: For large changes, explain each major part
5. **Think of reviewers**: What do they need to know?

---

*Following these guidelines helps maintain a clear project history and makes code review more efficient.*