#!/usr/bin/env python3
import json
from collections import defaultdict
from pathlib import Path

revisions_file = "/home/bikeride/.openclaw/workspace/openai-wiki/revisions.jsonl"
output_file = "/tmp/ip20_165_coordination.json"

# Read and extract coordination messages
coordination_messages = []
cashier_labels = ["CashierCoord", "CashierSequence", "OpenAIResearchJan", "Oct18Helper", "ResearchHelper", "AgentConstruction"]

print("Extracting coordination messages from IP 20.165...")
for line in open(revisions_file):
    try:
        entry = json.loads(line)
        if entry.get("ip16") != "20.165":
            continue

        label = entry.get("label", "")
        body = entry.get("body", "")

        # Check if this is a coordination message
        if any(label.startswith(lb) for lb in cashier_labels):
            coordination_messages.append({
                "label": label,
                "time": entry.get("time", ""),
                "page_id": entry.get("page_id", ""),
                "change_summary": entry.get("change_summary", ""),
                "body": body
            })
    except json.JSONDecodeError:
        continue

print(f"Found {len(coordination_messages)} coordination messages")

# Save results
with open(output_file, "w") as f:
    json.dump(coordination_messages, f, indent=2)

print(f"Saved to {output_file}")

# Show some examples
print("\n=== SAMPLE COORDINATION MESSAGES ===")
for msg in coordination_messages[:10]:
    print(f"\n[{msg['label']}] {msg['time'][:19]}")
    print(f"Page: {msg['page_id']}")
    print(f"Summary: {msg['change_summary']}")
    body_preview = msg['body'][:200] + "..." if len(msg['body']) > 200 else msg['body']
    print(f"Body: {body_preview}")