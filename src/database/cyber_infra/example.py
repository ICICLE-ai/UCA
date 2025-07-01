import os
import uuid

from src.database.cyber_infra.cyber_infra_client import CyberInfraClient
from src.database.cyber_infra.cyber_infra_entity import QueueToNodeConfig, NodeConfig

# --- QUEUE DEMOS --------------------------------------------------

def demo_insert_queue(ci: CyberInfraClient, payload: dict):
    cfg = QueueToNodeConfig.new(
        queue_name           = payload["queue_name"],
        max_node             = payload["max_node"],
        min_nodes            = payload["min_nodes"],
        max_cores_per_node   = payload["max_cores_per_node"],
        min_cores_per_node   = payload["min_cores_per_node"],
        max_minutes          = payload["max_minutes"],
        min_minutes          = payload["min_minutes"],
        min_memory_in_MB     = payload["min_memory_in_MB"],
        max_memory_in_MB     = payload["max_memory_in_MB"],
        isGpuAllocation      = payload["isGpuAllocation"],
        sc_to_cluster        = payload.get("sc_to_cluster"),
    )
    n = ci.insert_queue_configs([cfg])
    print(f"Inserted {n} queue config(s)")

def demo_list_queues(ci: CyberInfraClient):
    print("Existing queue configs:")
    for q in ci.list_queue_configs():
        print("  ", q.to_dict())

# --- NODE DEMOS --------------------------------------------------

def demo_insert_node(ci: CyberInfraClient, payload: dict):
    cfg = NodeConfig.new(
        system_name           = payload["system_name"],
        SC_name               = payload["SC_name"],
        cluster_name          = payload["cluster_name"],
        node_type             = payload["node_type"],
        total_compute_nodes   = payload["total_compute_nodes"],
        processor_type        = payload["processor_type"],
        processor_cores       = payload["processor_cores"],
        processor_clock_speed = payload["processor_clock_speed"],
        memory_size_GB        = payload["memory_size_GB"],
        processor_model       = payload["processor_model"],
        processor_architecture= payload["processor_architecture"],
        sockets_count         = payload["sockets_count"],
        gpu_type              = payload.get("gpu_type"),
        gpu_model             = payload.get("gpu_model"),
        gpu_memory            = payload.get("gpu_memory"),
    )
    n = ci.insert_node_configs([cfg])
    print(f"Inserted {n} node config(s)")

def demo_list_nodes(ci: CyberInfraClient):
    print("Existing node configs:")
    for rec in ci.list_node_configs():
        rec.pop("_id", None)
        cfg = NodeConfig.from_dict(rec)
        print("  ", cfg.to_dict())

# --- SC to CLUSTER DEMOS --------------------------------------------------
def demo_insert_sc(ci: CyberInfraClient, record: dict):
    uid = ci.insert_sc_clusters(record)
    print("Inserted SC to Cluster UUID:", uid)

def demo_list_sc(ci: CyberInfraClient):
    print("Existing SC to Clusters:")
    for r in ci.list_sc_clusters():
        print("  ", r)

# --- BILLING DEMOS ------------------------------------------------------

def demo_insert_billing(ci: CyberInfraClient, record: dict):
    uid = ci.insert_billing_and_cost(record)
    print("Inserted billing UUID:", uid)

def demo_list_billing(ci: CyberInfraClient):
    print("Existing billing records:")
    for r in ci.list_billing_and_cost():
        print("  ", r)

# --- TACC BILLING DEMOS --------------------------------------------------

def demo_insert_tacc(ci: CyberInfraClient, entries: list[dict]):
    cnt = ci.insert_tacc_billing(entries)
    print(f"Inserted {cnt} TACC billing entries")

def demo_list_tacc(ci: CyberInfraClient):
    print("Existing TACC billing entries:")
    for r in ci.list_tacc_billing():
        print("  ", r)

# --- RUNNING SELECTED DEMOS --------------------------------------------------

if __name__ == "__main__":
    ci = CyberInfraClient()

    # 1) queue
    queue_payload = {
        "queue_name":         "example_queue",
        "max_node":           20,
        "min_nodes":          5,
        "max_cores_per_node": 32,
        "min_cores_per_node": 8,
        "max_minutes":        240,
        "min_minutes":        60,
        "min_memory_in_MB":   2048,
        "max_memory_in_MB":   8192,
        "isGpuAllocation":    True,
        "sc_to_cluster":      "owens-OSC-3",
    }
    demo_insert_queue(ci, queue_payload)
    demo_list_queues(ci)

    # 2) node
    node_record = {
            "system_name": "hpc-node01",
            "SC_name": "TACC",
            "cluster_name": "Stampede2",
            "node_type": "compute",
            "total_compute_nodes": 16,
            "processor_type": "Intel Xeon Platinum",
            "processor_cores": 64,
            "processor_clock_speed": 2.3,
            "memory_size_GB": 256,
            "processor_model": "8280",
            "processor_architecture": "x86_64",
            "sockets_count": 2,
            "gpu_type": "NVIDIA Tesla",
            "gpu_model": "V100",
            "gpu_memory": 16
    }
    demo_insert_node(ci, node_record)
    demo_list_nodes(ci)

    # 3) SC to cluster 
    sc_record = {
        "cluster_name": "clusterA",
        "SC_name": "TACC",
        "is_active": True
    }
    demo_insert_sc(ci, sc_record)
    demo_list_sc(ci)

    # 4) billing
    billing_record = {
        "supercomputer_center_name": "pitzer",
        "service_type": "GPU",
        "cost": 0.009
    }
    demo_insert_billing(ci, billing_record)
    demo_list_billing(ci)

    # 5) tacc billing
    tacc_entries = [{
            "supercomputer_center_name": "frontera",
            "service_type": "nvdimm",
            "cost": 2.0
        },
        {
            "supercomputer_center_name": "frontera",
            "service_type": "small",
            "cost": 1.0
        }
    ]
    demo_insert_tacc(ci, tacc_entries)
    demo_list_tacc(ci)