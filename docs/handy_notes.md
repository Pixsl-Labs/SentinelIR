# Useful VSCode Extensions

- indent-rainbow
- autoDocstrings
- Mermaid Diagram Manager

## autoDocstrings Configurations

- CTRL+SHIFT+P -> `Open User Settings (JSON)`

Add:

    "autoDocstring.docstringFormat": "google",
    "autoDocstring.customTemplatePath": ".vscode/docstring.mustache",
    "autoDocstring.generateDocstringOnEnter": true,
    "autoDocstring.guessTypes": true,
    "autoDocstring.quoteStyle": "\"\"\"",
    "autoDocstring.startOnNewLine": true

# Docstring Cheat Sheet

analyser: Log analyser instance containing