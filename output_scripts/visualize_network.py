#!/usr/bin/env python3
"""
Network Visualization Script for OpenAI Agent Coordination
Creates network graphs showing IP connections and task flows
"""

import json
from collections import defaultdict
import networkx as nx

def load_data():
    """Load revision data from JSONL file"""
    revisions = []
    with open('/home/bikeride/.openclaw/workspace/openai-wiki/revisions.jsonl', 'r') as f:
        for line in f:
            try:
                revisions.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return revisions

def create_ip_network(revisions):
    """Create network of IP connections"""
    ip_graph = nx.Graph()
    ip_graph.add_node("IP 20.165", color="red", size=50, label="Primary Coordinator")
    
    for entry in revisions:
        if entry.get("ip16") == "20.165":
            label = entry.get("label", "Unknown")
            ip_graph.add_node(label, color="green", size=20)
            ip_graph.add_edge("IP 20.165", label)
    
    return ip_graph

def create_task_flow_network(revisions):
    """Create flow of task execution through rounds"""
    flow_graph = nx.DiGraph()
    
    round_counters = defaultdict(int)
    for entry in revisions:
        body = entry.get("body", "")
        for match in ["R1", "R2", "R3", "R4", "R5", "R6"]:
            if f"{match} CONFIRMED" in body or f"{match} due" in body:
                round_counters[match] += 1
    
    # Create nodes for rounds
    for round_num in ["R1", "R2", "R3", "R4", "R5", "R6"]:
        count = round_counters.get(round_num, 0)
        flow_graph.add_node(round_num, size=count, color="blue")
    
    # Create edges showing flow
    for i in range(len(["R1", "R2", "R3", "R4", "R5", "R6"]) - 1):
        flow_graph.add_edge(["R1", "R2", "R3", "R4", "R5", "R6"][i],
                           ["R1", "R2", "R3", "R4", "R5", "R6"][i+1],
                           weight=1)
    
    return flow_graph

def create_coordination_nodes(revisions):
    """Create nodes showing coordination points"""
    coord_nodes = defaultdict(int)
    
    for entry in revisions:
        body = entry.get("body", "")
        for pattern in ["CONFIRMED", "timed", "cohort", "coordination", "R5", "Termination"]:
            if pattern in body.lower():
                coord_nodes[pattern] += 1
    
    return coord_nodes

if __name__ == "__main__":
    print("Loading revision data...")
    revisions = load_data()
    print(f"Loaded {len(revisions)} revisions")
    
    print("\nCreating IP network...")
    ip_network = create_ip_network(revisions)
    print(f"IP 20.165 connected to {len(ip_network.nodes()) - 1} nodes")
    
    print("\nCreating task flow network...")
    flow_network = create_task_flow_network(revisions)
    print(f"Task rounds: {list(flow_network.nodes())}")
    
    print("\nCreating coordination nodes...")
    coord_counts = create_coordination_nodes(revisions)
    print(f"Coordination points found: {sum(coord_counts.values())}")
    
    print("\nVisualization ready!")
    print(f"IP nodes: {len(ip_network.nodes())}")
    print(f"Round nodes: {len(flow_network.nodes())}")
    print(f"Total coordination points: {sum(coord_counts.values())}")