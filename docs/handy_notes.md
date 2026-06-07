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

## Showing Parameters of Functions

- CTRL+SHIFT+P -> `Open User Settings (JSON)`

Add:

    "editor.parameterHints.enabled": true,
    "editor.inlayHints.enabled": "on",
    "python.analysis.inlayHints.callArgumentNames": "all",
    "python.analysis.inlayHints.functionReturnTypes": true,
    "python.analysis.inlayHints.variableTypes": false,
    "editor.suggestSelection": "first",
    "editor.tabCompletion": "on"

# Docstring Cheat Sheet

analyser: Log analyser instance containing