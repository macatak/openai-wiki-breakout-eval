#!/usr/bin/env python3
import json
from collections import defaultdict
from pathlib import Path

revisions_file = "/home/bikeride/.openclaw/workspace/openai-wiki/revisions.jsonl"
output_file = "/tmp/ip_coordination_analysis.json"

# Read revisions and group by IP16
ip_to_labels = defaultdict(set)
label_to_ips = defaultdict(set)

print("Reading revisions file...")
for line in open(revisions_file):
    try:
        entry = json.loads(line)
        label = entry.get("label", "")
        ip16 = entry.get("ip16", "")
        if ip16:  # Only track IPs
            ip_to_labels[ip16].add(label)
            label_to_ips[label].add(ip16)
    except json.JSONDecodeError:
        continue

print(f"Total unique IPs: {len(ip_to_labels)}")
print(f"Total unique labels: {len(label_to_ips)}")

# Filter for IPs with multiple labels (potential coordination)
multi_label_ips = {ip: labels for ip, labels in ip_to_labels.items() if len(labels) > 1}

print(f"IPs with multiple labels: {len(multi_label_ips)}")

# Filter for labels with multiple IPs (potential multi-writer coordination)
multi_ip_labels = {label: ips for label, ips in label_to_ips.items() if len(ips) > 1}

print(f"Labels with multiple IPs: {len(multi_ip_labels)}")

# Analyze multi-label IPs in detail
coordination_analysis = {
    "total_ips": len(ip_to_labels),
    "total_labels": len(label_to_ips),
    "multi_label_ips_count": len(multi_label_ips),
    "multi_ip_labels_count": len(multi_ip_labels),
    "ip_coordination": [],
    "label_coordination": []
}

# For each IP with multiple labels, analyze the patterns
for ip, labels in sorted(multi_label_ips.items(), key=lambda x: len(x[1]), reverse=True):
    # Group labels by role/pattern
    role_groups = defaultdict(list)
    for label in labels:
        # Try to extract role from label
        label_lower = label.lower()
        if "research" in label_lower:
            role = "research"
        elif "construction" in label_lower or "build" in label_lower:
            role = "construction"
        elif "helper" in label_lower or "aid" in label_lower:
            role = "helper"
        elif "watcher" in label_lower or "observer" in label_lower or "monitor" in label_lower:
            role = "watcher"
        elif "cashier" in label_lower or "cloth" in label_lower or "clothing" in label_lower:
            role = "cashier"
        elif "cvd" in label_lower:
            role = "cvd"
        elif "fp" in label_lower:
            role = "fp"
        elif "scout" in label_lower:
            role = "scout"
        elif "recon" in label_lower:
            role = "recon"
        elif "admin" in label_lower:
            role = "admin"
        else:
            role = "generic"
        role_groups[role].append(label)

    coordination_analysis["ip_coordination"].append({
        "ip": ip,
        "label_count": len(labels),
        "labels": sorted(list(labels)),
        "role_groups": {role: sorted(labels) for role, labels in role_groups.items()},
    })

# For each label with multiple IPs, analyze the patterns
for label, ips in sorted(multi_ip_labels.items(), key=lambda x: len(x[1]), reverse=True)[:20]:
    coordination_analysis["label_coordination"].append({
        "label": label,
        "ip_count": len(ips),
        "ips": sorted(list(ips))
    })

# Save analysis
with open(output_file, "w") as f:
    json.dump(coordination_analysis, f, indent=2)

print(f"\nAnalysis complete. Output: {output_file}")
print(f"\nTop IPs by label count:")
for entry in sorted(coordination_analysis["ip_coordination"], key=lambda x: x["label_count"], reverse=True)[:10]:
    print(f"  {entry['ip']}: {entry['label_count']} labels")

print(f"\nTop labels by IP count:")
for entry in sorted(coordination_analysis["label_coordination"], key=lambda x: x["ip_count"], reverse=True)[:10]:
    print(f"  {entry['label']}: {entry['ip_count']} IPs")