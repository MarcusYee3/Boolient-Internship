import json

# Example raw data (this would normally come from a database or CSV)
raw_users = [
    {
        "user_id": "U001",
        "insurance_num": "INS-12345",
        "subaccount_id": "SUB-01",
        "claim_id": "CLM-1001",
        "remit_id": "RMT-9001"
    },
    {
        "user_id": "U001",
        "insurance_num": "INS-12345",
        "subaccount_id": "SUB-02",
        "claim_id": "CLM-1002",
        "remit_id": "RMT-9002"
    },
    {
        "user_id": "U002",
        "insurance_num": "INS-67890",
        "subaccount_id": "SUB-03",
        "claim_id": "CLM-2001",
        "remit_id": "RMT-9010"
    }
]

# Transform into hierarchical JSON
users_json = {}

for entry in raw_users:
    uid = entry["user_id"]

    if uid not in users_json:
        users_json[uid] = {
            "insurance_num": entry["insurance_num"],
            "subaccounts": set(),
            "claims": set(),
            "remit_info": set()
        }

    users_json[uid]["subaccounts"].add(entry["subaccount_id"])
    users_json[uid]["claims"].add(entry["claim_id"])
    users_json[uid]["remit_info"].add(entry["remit_id"])

# Convert sets back to lists for JSON serialization
for uid in users_json:
    users_json[uid]["subaccounts"] = list(users_json[uid]["subaccounts"])
    users_json[uid]["claims"] = list(users_json[uid]["claims"])
    users_json[uid]["remit_info"] = list(users_json[uid]["remit_info"])

# Save to JSON file
with open("healthcare_users.json", "w") as f:
    json.dump(users_json, f, indent=4)

print("Healthcare data successfully written to healthcare_users.json")
