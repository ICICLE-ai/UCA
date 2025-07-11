# This is a sample example production level test case
import os

from .rules_engine_client import RuleEngineClient


def main():
    client = RuleEngineClient(
        tapis_url = os.getenv("TAPIS_BASE_URL"),
        tapis_user= os.getenv("TAPIS_USER"),
        tapis_pass= os.getenv("TAPIS_PASS"),
        mongo_uri = os.getenv("MONGO_URI")
    )
    print("Connected to MongoDB & TAPIS")
    rule_json = {
      "CI": "OSC",
      "Type": "data",
      "Active_From": "2024-05-06T12:00:00",
      "Active_To": None,
      "Services": [
        "data-label",
        "model-train"
      ],
      "Data_Rules": [
        {
          "Folder_Path": "/fs/ess/PAS2271/Gautam/Animal_Ecology/output/old/visualized_images",
          "Type": "count",
          "Count": 10000,
          "Apps": [
            "<TAPIS_APP_ID_1>",
            "<TAPIS_APP_ID_2>"
          ],
          "Sample_Images": True,
          "Wait_Manual": True
        }
      ],
      "Model_Rules": []
    }

    rule_uuid = client.create_rule(rule_json)
    print(f"New Rule created with UUID: {rule_uuid}")

    fetched = client.list_rules({"Rule_UUID": rule_uuid})
    print("Fetched rule:", fetched)

if __name__ == "__main__":
    main()