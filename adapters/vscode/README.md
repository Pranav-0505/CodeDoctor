# Code Doctor — VS Code Extension Adapter

This adapter connects Visual Studio Code workspace editors to the central **Code Doctor Engine** over REST API.

## Features

* **Real-time Diagnostics**: Publishes Code Doctor syntax, runtime exception, security, and performance warnings directly into the VS Code Problems panel.
* **Code Surgery Integration**: Triggers minimal patch generation and diff preview inside VS Code buffers.
* **Platform Independent Backend**: Communicates asynchronously with `http://127.0.0.1:8000/api/v1`.

## Commands

* `Code Doctor: Diagnose Current File` (`codedoctor.analyzeFile`)
* `Code Doctor: Run Code Surgery & Preview Fix` (`codedoctor.runSurgery`)
