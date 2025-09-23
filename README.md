# UCA

1. implement UCA for smart scheduler (which integrates Time Estimator and REFDNN internally) and CKN (via Illuvatar). The CKN integration might depend on the Illuvatar release.

1. implement the UCA for model commons.

1. implement the narrow waist model using Kafka to enable inter-component communication. This enables Smart Scheduler+CKN communication and Smart Schedluer+TimeEsitmator/REFDNN.


---
## Rules Engine Component

This repository provides a lightweight Python package for interacting with the UCA Rules Engine API.
It acts as a middleware layer between end-users (e.g., Jupyter notebooks, apps) and the Rules Engine Admin service.

```
src/
└── database/
    └── rules_engine/
        ├── rules_engine.py        # Client wrapper (CRUD ops, health check)
        ├── config.py              # Loads config.yaml
        └── __init__.py
├── config.yaml                    # Admin domain configuration to establish communication
├── pyproject.toml                 # Packaging metadata
├── requirements.txt
```
---
## Installation

Clone the repo and install in editable mode (for development):
``` bash
git clone https://github.com/ICICLE-ai/UCA.git
cd UCA
pip install -e .
```

Or install directly from GitHub (specific branch):

```bash
pip install git+https://github.com/ICICLE-ai/UCA.git
```
---
## Configuration

All runtime configuration comes from a config.yaml file at the repo root.
This file must define the base URL of the Rules Engine Admin service.

**Example `config.yaml`:** (works only with jupyter notebook)
```yaml
base_url: "http://127.0.0.1:8081"
```
Refer at the end to run local jupyter notebook. 

If you are testing remotely, replace with the ngrok URL or server IP:
```bash
base_url: "https://xyz123.ngrok-free.app"
```
---
## Development Notes
 
	•	The client only depends on the Rules Engine Admin API being available.
	•	Ensure your config.yaml contains the correct base_url.
	•	A valid Tapis access token is required to call any function.


### Jupyter use
```bash
pip install jupyterlab
jupyter lab
```
---

## Checkout rules_engine_notebook.ipynb in ```UCA/examples/rule_engine_notebook.ipynb``` for reference.