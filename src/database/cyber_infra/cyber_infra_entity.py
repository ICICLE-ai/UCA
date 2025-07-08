from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Optional
import uuid

@dataclass
class QueueToNodeConfig:
    UUID:               str
    queue_name:         str
    max_node:           int
    min_nodes:          int
    max_cores_per_node: int
    min_cores_per_node: int
    max_minutes:        int
    min_minutes:        int
    min_memory_in_MB:   int
    max_memory_in_MB:   int
    isGpuAllocation:    bool
    sc_to_cluster:      Optional[str] = None

    @staticmethod
    def new(
        queue_name: str,
        max_node: int = 0,
        min_nodes: int = 0,
        max_cores_per_node: int = 0,
        min_cores_per_node: int = 0,
        max_minutes: int = 0,
        min_minutes: int = 0,
        min_memory_in_MB: int = 0,
        max_memory_in_MB: int = 0,
        isGpuAllocation: bool = False,
        sc_to_cluster: Optional[str] = None,
    ) -> QueueToNodeConfig:
        return QueueToNodeConfig(
            UUID=str(uuid.uuid4()),
            queue_name=queue_name,
            max_node=max_node,
            min_nodes=min_nodes,
            max_cores_per_node=max_cores_per_node,
            min_cores_per_node=min_cores_per_node,
            max_minutes=max_minutes,
            min_minutes=min_minutes,
            min_memory_in_MB=min_memory_in_MB,
            max_memory_in_MB=max_memory_in_MB,
            isGpuAllocation=isGpuAllocation,
            sc_to_cluster=sc_to_cluster,
        )

    @staticmethod
    def from_dict(d: dict) -> QueueToNodeConfig:
        return QueueToNodeConfig(**d)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class NodeConfig:
    UUID:                   str
    system_name:            str
    SC_name:                str
    cluster_name:           str
    node_type:              str
    total_compute_nodes:    int
    processor_type:         str
    processor_cores:        int
    processor_clock_speed:  float
    memory_size_GB:         int
    processor_model:        str
    processor_architecture: str
    sockets_count:          int
    gpu_type:               Optional[str] = None
    gpu_model:              Optional[str] = None
    gpu_memory:             Optional[int] = None

    @staticmethod
    def new(
        system_name: str,
        SC_name: str,
        cluster_name: str,
        node_type: str,
        total_compute_nodes: int,
        processor_type: str,
        processor_cores: int,
        processor_clock_speed: float,
        memory_size_GB: int,
        processor_model: str,
        processor_architecture: str,
        sockets_count: int,
        gpu_type: Optional[str] = None,
        gpu_model: Optional[str] = None,
        gpu_memory: Optional[int] = None,
    ) -> NodeConfig:
        return NodeConfig(
            UUID=str(uuid.uuid4()),
            system_name=system_name,
            SC_name=SC_name,
            cluster_name=cluster_name,
            node_type=node_type,
            total_compute_nodes=total_compute_nodes,
            processor_type=processor_type,
            processor_cores=processor_cores,
            processor_clock_speed=processor_clock_speed,
            memory_size_GB=memory_size_GB,
            processor_model=processor_model,
            processor_architecture=processor_architecture,
            sockets_count=sockets_count,
            gpu_type=gpu_type,
            gpu_model=gpu_model,
            gpu_memory=gpu_memory,
        )

    @staticmethod
    def from_dict(d: dict) -> NodeConfig:
        return NodeConfig(**d)

    def to_dict(self) -> dict:
        return asdict(self)