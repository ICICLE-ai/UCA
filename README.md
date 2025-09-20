# UCA

1. implement UCA for smart scheduler (which integrates Time Estimator and REFDNN internally) and CKN (via Illuvatar). The CKN integration might depend on the Illuvatar release.

1. implement the UCA for model commons.

1. implement the narrow waist model using Kafka to enable inter-component communication. This enables Smart Scheduler+CKN communication and Smart Schedluer+TimeEsitmator/REFDNN.


---
## Rules Engine Component
```
src/
└── database/
    └── rules_engine/
        ├── api.py           # FastAPI app (endpoints, Tapis validation)
        ├── rules_engine_client.py  # Mongo CRUD client 
        └── config.py        # Loads config.yaml at startup
├── config.yaml              # Runtime config
├── requirements.txt
└── Dockerfile
```

---

## Configuration

All runtime config comes from `config.yaml` (mounted into the container or used locally).

**Example `config.yaml`:**
```yaml
# MongoDB creds
mongo_uri: "mongodb+srv://<USER>:<PASS>@<CLUSTER>/"
rules_db:  "IMT_Rules_engine_database"

# Tapis
tapis_url: "https://tacc.tapis.io"
```

Note: At the moment, MongoDB Atlas is hosted under Gautam’s (molakalmuru.1@osu.edu)personal account (Contact him for adding the tester to the ongoing project). This setup can be reused for development and testing, but for long-term stability we should transition to an ICICLE-managed MongoDB service (e.g., Atlas under the org account, or Mongo pods in Kubernetes).

---
**Side note on base URL:**

The **BASE_URL** depends on where the API is hosted.

* **Temporary tunnel for local testing:** an `ngrok` URL (This should be replaced once a stable setup is available). Check below for reference to use ngrok.
* **VM or container on a server:** `http://<server-ip-or-domain>:8081`

> In production or shared environment, we need to replace this with an **ICICLE-managed domain** (if available) so users have a stable endpoint or any other approach.


---
### Running with Docker

**Build the image:**

```bash
docker build -t uca-rules-api .
```

**Run the container (mount your config):**
```bash
docker run --rm -p 8081:8081 -v "$PWD/config.yaml:/app/config.yaml:ro" uca-rules-api
```
---
### Using ngrok to Expose the Rules Engine

If you’re running the API locally (e.g., via Docker), you can use **ngrok** to create a temporary public URL for testing.

1. Install ngrok

   Install via package manager:
     ```bash
     brew install ngrok               # macOS
     sudo apt install ngrok           # Ubuntu/Debian
     ```

2. Authenticate (one-time setup)

   After creating a free ngrok account, copy your auth token from the dashboard and run:
   ```bash
   ngrok config add-authtoken <YOUR_AUTH_TOKEN>
   ```

3. Run your Rules Engine locally

    For example:

    ```bash
    docker run --rm -p 8081:8081 -v "$PWD/config.yaml:/app/config.yaml:ro" uca-rules-api
    ```

4. Expose with ngrok

    In another terminal:
    ```bash
    ngrok http 8081
    ```

5.	Use the public URL

    ngrok will show output like:
    ```bash
    Forwarding  https://xyz123.ngrok-free.app -> http://localhost:8081
    ```

    Copy the https://...ngrok-free.app URL and use it as your **BASE_URL** in Colab.

    **Note**: ngrok URLs change every time you restart it (unless you have a paid plan with reserved domains).
For production, we should use a stable domain or server IP instead of ngrok.

---

## Final Thoughts

For a hands-on walkthrough of how to interact with the Rules Engine (create, list, update, delete rules), please refer to the notebook under `rules_engine` folder:  
**`Rules_Engine_Notebook.ipynb`**

### TODO / Next Steps
- **MongoDB**: Currently the deployment uses Mongo Atlas under Gautam’s account. This works for testing, but eventually we need to migrate to ICICLE-managed MongoDB servers for production stability or other viable approach.
- **Domain name / Base URL**: For now, we rely on `ngrok` or direct VM IPs for accessing the API. Long term, we should register and expose the Rules Engine under an official ICICLE domain or other viable approach.

This repo should be seen as the first working version.