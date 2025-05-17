# HMS Cross-Cloud Network Architecture

## Overview

This document details the network architecture design for enabling secure and efficient communication between HMS components deployed across multiple cloud environments (AWS and Azure). The architecture leverages HMS-SYS (based on Cilium) capabilities to create a unified networking layer that spans cloud boundaries.

## Design Principles

1. **Security First**: All cross-cloud traffic must be encrypted and authenticated
2. **Operational Simplicity**: Unified management model across environments
3. **Performance Optimization**: Minimize latency for cross-cloud communication
4. **Resiliency**: No single point of failure for cross-cloud connectivity
5. **Observability**: Comprehensive visibility into cross-cloud traffic patterns

## Network Architecture Components

### 1. Core Network Components

#### 1.1 Kubernetes Networking Layer (HMS-SYS/Cilium)

Cilium provides the foundation for our cross-cloud networking with:
- eBPF-based dataplane for efficient traffic handling
- Identity-based security decoupled from network addressing
- Support for multiple networking modes (direct routing/overlay)
- Built-in load balancing capabilities

#### 1.2 Cross-Cluster Mesh (ClusterMesh)

ClusterMesh enables multi-cluster communication with:
- Service discovery across clusters
- Identity propagation between clusters
- Network policy enforcement spanning clusters
- Load balancing for services across clusters

#### 1.3 Encryption Layer

For securing cross-cloud traffic:
- WireGuard for transparent encryption
- IPsec for compatibility with existing VPN infrastructure
- TLS for application-level encryption

#### 1.4 Service Discovery

For locating services across clouds:
- DNS-based discovery with cross-cluster resolution
- Service identity propagation across clusters
- Endpoint health monitoring across boundaries

### 2. Cloud-Specific Integration Components

#### 2.1 AWS Integration

- **VPC**: Primary network container for AWS resources
- **Elastic Network Interfaces (ENI)**: For native AWS networking
- **AWS Transit Gateway**: For connecting to Azure (if using AWS-to-Azure direct connectivity)
- **Route53**: For DNS resolution across clouds
- **Network Load Balancers**: For externally exposed services

#### 2.2 Azure Integration

- **VNET**: Primary network container for Azure resources
- **Azure CNI**: For native Azure networking
- **Azure Virtual Network Gateway**: For connecting to AWS (if using Azure-to-AWS direct connectivity)
- **Azure DNS**: For DNS resolution across clouds
- **Azure Load Balancer**: For externally exposed services

## Network Architecture Diagrams

### High-Level Network Overview

```
┌──────────────────────────────────────────────────────┐   ┌──────────────────────────────────────────────────────┐
│                     AWS Cloud                         │   │                    Azure Cloud                        │
│                                                       │   │                                                       │
│  ┌───────────────────┐         ┌───────────────────┐  │   │  ┌───────────────────┐         ┌───────────────────┐  │
│  │      VPC          │         │  Transit Gateway  │  │   │  │      VNET         │         │  Virtual Network  │  │
│  │                   │         │                   │  │   │  │                   │         │     Gateway       │  │
│  │  ┌─────────────┐  │         │  ┌─────────────┐  │  │   │  │  ┌─────────────┐  │         │  ┌─────────────┐  │  │
│  │  │ K8s Cluster │  │◄────────┼─►│  AWS-Azure  │  │◄─┼───┼─►│  Azure-AWS   │◄─┼─────────►│ K8s Cluster  │  │  │
│  │  │             │  │         │  │ Connection  │  │  │   │  │ Connection    │  │         │             │  │  │
│  │  └─────────────┘  │         │  └─────────────┘  │  │   │  └─────────────┘  │         │  └─────────────┘  │  │
│  │                   │         │                   │  │   │                   │         │                   │  │
│  └───────────────────┘         └───────────────────┘  │   │  └───────────────────┘         └───────────────────┘  │
│                                                       │   │                                                       │
│                     ▲                                 │   │                     ▲                                 │
│                     │                                 │   │                     │                                 │
│                     ▼                                 │   │                     ▼                                 │
│  ┌───────────────────────────────────────────────┐   │   │  ┌───────────────────────────────────────────────┐   │
│  │             AWS Cilium Operator               │   │   │  │            Azure Cilium Operator              │   │
│  └───────────────────────────────────────────────┘   │   │  └───────────────────────────────────────────────┘   │
│                                                       │   │                                                       │
└──────────────────────────────────────────────────────┘   └──────────────────────────────────────────────────────┘
                              ▲                                                   ▲
                              │                                                   │
                              │               ClusterMesh Communication           │
                              └───────────────────────────────────────────────────┘
```

### Detailed Network Flow

```
┌────────────────────────────────────────────────────────────┐   ┌────────────────────────────────────────────────────────────┐
│                        AWS Cluster                          │   │                       Azure Cluster                         │
│                                                             │   │                                                             │
│  ┌─────────────┐         ┌─────────────┐    ┌─────────────┐ │   │ ┌─────────────┐         ┌─────────────┐    ┌─────────────┐ │
│  │  HMS-API    │◄───────►│  HMS-SYS    │◄───┤ kube-proxy  │ │   │ │  HMS-NFO    │◄───────►│  HMS-SYS    │◄───┤ kube-proxy  │ │
│  │  POD        │         │  DAEMON     │    │ (optional)  │ │   │ │  POD        │         │  DAEMON     │    │ (optional)  │ │
│  └──────┬──────┘         └──────┬──────┘    └─────────────┘ │   │ └──────┬──────┘         └──────┬──────┘    └─────────────┘ │
│         │                       │                            │   │        │                       │                            │
│         ▼                       ▼                            │   │        ▼                       ▼                            │
│  ┌─────────────┐         ┌─────────────┐                     │   │ ┌─────────────┐         ┌─────────────┐                     │
│  │  veth pair  │         │  ENI        │                     │   │ │  veth pair  │         │  Azure CNI  │                     │
│  └──────┬──────┘         └──────┬──────┘                     │   │ └──────┬──────┘         └──────┬──────┘                     │
│         │                       │                            │   │        │                       │                            │
│         ▼                       ▼                            │   │        ▼                       ▼                            │
│  ┌───────────────────────────────────────────────────────┐  │   │ ┌───────────────────────────────────────────────────────┐  │
│  │                 eBPF Programs (datapath)              │  │   │ │                eBPF Programs (datapath)               │  │
│  └──────┬──────────────────────────────────┬─────────────┘  │   │ └──────┬──────────────────────────────────┬─────────────┘  │
│         │                                   │                │   │        │                                   │                │
│         ▼                                   ▼                │   │        ▼                                   ▼                │
│  ┌─────────────┐                    ┌─────────────┐          │   │ ┌─────────────┐                    ┌─────────────┐          │
│  │ Encryption  │                    │    VPC      │          │   │ │ Encryption  │                    │    VNET     │          │
│  │ (WireGuard) │                    │   Routes    │          │   │ │ (WireGuard) │                    │   Routes    │          │
│  └──────┬──────┘                    └──────┬──────┘          │   │ └──────┬──────┘                    └──────┬──────┘          │
│         │                                  │                 │   │        │                                  │                 │
│         └────────────┬────────────────────┘                 │   │        └────────────┬────────────────────┘                 │
│                      │                                       │   │                     │                                       │
│                      ▼                                       │   │                     ▼                                       │
│          ┌──────────────────────────┐                        │   │         ┌──────────────────────────┐                        │
│          │     AWS Internet GW      │                        │   │         │    Azure Internet GW     │                        │
│          │     or Transit GW        │                        │   │         │    or Network Gateway    │                        │
│          └──────────┬───────────────┘                        │   │         └──────────┬───────────────┘                        │
│                     │                                        │   │                    │                                        │
└─────────────────────┼────────────────────────────────────────┘   └────────────────────┼─────────────────────────────────────────┘
                      │                                                                 │
                      │                    Internet / Direct Connect                    │
                      └────────────────────────────────────────────────────────────────┘
```

## Network Implementation Options

### Option 1: Cilium ClusterMesh with VPC/VNET Peering

**Components:**
- Cilium installed in both AWS and Azure clusters
- ClusterMesh enabled for cross-cluster communication
- VPC Peering or Transit Gateway between AWS and Azure

**Advantages:**
- Direct connectivity between clusters
- Unified security model across clouds
- Simplified service discovery

**Considerations:**
- Requires compatible CIDRs across clouds
- May incur higher data transfer costs
- Limited by VPC peering constraints

**Sample Configuration:**
```yaml
# ClusterMesh configuration (AWS cluster)
apiVersion: v1
kind: ConfigMap
metadata:
  name: cilium-config
  namespace: kube-system
data:
  cluster-name: "aws-cluster"
  cluster-id: "1"
  enable-clustermesh: "true"
  ipv4-native-routing-cidr: "10.0.0.0/8"
  tunnel-protocol: "disabled"  # Use direct routing with VPC peering
```

### Option 2: Cilium with Encrypted Overlay

**Components:**
- Cilium installed in both AWS and Azure clusters
- WireGuard encryption for cross-cluster traffic
- Overlay networking mode (VXLAN, Geneve)

**Advantages:**
- No need for VPC peering
- Works with overlapping CIDRs
- Consistent encryption model

**Considerations:**
- Slightly higher overhead due to encryption and encapsulation
- Requires UDP port 51871 (WireGuard) to be open

**Sample Configuration:**
```yaml
# Encrypted overlay configuration (AWS cluster)
apiVersion: v1
kind: ConfigMap
metadata:
  name: cilium-config
  namespace: kube-system
data:
  cluster-name: "aws-cluster"
  cluster-id: "1"
  enable-clustermesh: "true"
  tunnel-protocol: "geneve"
  enable-encryption: "true"
  encryption-type: "wireguard"
```

### Option 3: Service Mesh with Gateway

**Components:**
- Cilium for intra-cluster networking
- Service mesh gateway (Istio, Linkerd) at cluster boundaries
- Load balancers exposed through cloud providers

**Advantages:**
- Fine-grained traffic control
- Advanced traffic management capabilities
- Can work with restrictive network environments

**Considerations:**
- More complex to set up and manage
- Additional hop for cross-cluster traffic
- Higher resource consumption

**Sample Configuration:**
```yaml
# Example Istio Gateway configuration
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: cross-cloud-gateway
  namespace: istio-system
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 443
      name: https
      protocol: HTTPS
    hosts:
    - "*.cloud.hms-system.internal"
    tls:
      mode: MUTUAL
```

## CIDR Allocation Plan

To ensure non-overlapping address spaces across clusters:

| Cloud | Cluster | Pod CIDR | Service CIDR |
|-------|---------|----------|-------------|
| AWS | Primary | 10.0.0.0/16 | 10.100.0.0/16 |
| Azure | Primary | 10.1.0.0/16 | 10.101.0.0/16 |
| AWS | DR | 10.2.0.0/16 | 10.102.0.0/16 |
| Azure | DR | 10.3.0.0/16 | 10.103.0.0/16 |

## Network Policy Model

HMS components require consistent network policies across clusters:

### Default Deny Policy
```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: default-deny
spec:
  endpointSelector:
    matchLabels: {}
  ingress:
  - {}
  egress:
  - {}
```

### HMS API Communication Policy
```yaml
apiVersion: cilium.io/v2
kind: CiliumClusterwideNetworkPolicy
metadata:
  name: allow-hms-api-access
spec:
  endpointSelector:
    matchLabels:
      app: hms-api
  ingress:
  - fromEndpoints:
    - matchLabels:
        io.kubernetes.pod.namespace: kube-system
        k8s-app: kube-dns
    toPorts:
    - ports:
      - port: "53"
        protocol: UDP
  - fromEndpoints:
    - matchLabels:
        app: hms-sys
    toPorts:
    - ports:
      - port: "8080"
        protocol: TCP
  egress:
  - toEndpoints:
    - matchLabels:
        app: hms-sys
    toPorts:
    - ports:
      - port: "8080"
        protocol: TCP
```

## DNS Configuration

To enable service discovery across clusters:

1. **CoreDNS Custom Configuration:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns-custom
  namespace: kube-system
data:
  cross-cloud.server: |
    azure-cluster.svc.cluster.local:53 {
        forward . <azure-dns-service-ip>
    }
    aws-cluster.svc.cluster.local:53 {
        forward . <aws-dns-service-ip>
    }
```

2. **External DNS Integration:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: external-dns
spec:
  template:
    spec:
      containers:
      - name: external-dns
        args:
        - --source=service
        - --source=ingress
        - --domain-filter=hms-system.internal
        - --provider=aws
        # When running in AWS
        - --aws-zone-type=private
        # When running in Azure
        - --azure-resource-group=<resource-group>
```

## Security Considerations

### 1. Encryption

All cross-cloud traffic must be encrypted using:
- WireGuard/IPsec for network-level encryption
- TLS for application-level encryption
- mTLS for service-to-service authentication

### 2. Identity Management

Consistent identity across clouds:
- Kubernetes service accounts with OIDC integration
- Cloud IAM integration with limited permissions
- Identity propagation via ClusterMesh

### 3. Network Isolation

Proper segmentation within and across clouds:
- Strict network policies for all components
- Ingress/egress gateway controls
- Cloud-native security groups as an additional layer

## Performance Optimizations

To minimize latency and maximize throughput for cross-cloud communication:

1. **Pod placement strategy:**
   - Co-locate frequently communicating services in the same cluster
   - Deploy read replicas across clouds for data-heavy services

2. **Network optimizations:**
   - Use direct routing where possible instead of tunneling
   - Enable TCP BBR congestion control
   - Configure appropriate MTU settings to avoid fragmentation

3. **Load distribution:**
   - Implement regional affinity for requests
   - Use Horizontal Pod Autoscaler (HPA) with custom metrics for scaling based on network latency

## Monitoring and Observability

To ensure visibility into cross-cloud network traffic:

1. **Hubble deployment:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: cilium-config
  namespace: kube-system
data:
  enable-hubble: "true"
  hubble-socket-path: "/var/run/cilium/hubble.sock"
  hubble-metrics-server: ":9091"
  hubble-metrics: "drop,tcp,flow,port-distribution,icmp,http"
```

2. **Grafana dashboards:**
   - Cross-cloud latency monitoring
   - Inter-service communication graphs
   - Traffic flow visualization

3. **Alerting rules:**
   - High cross-cloud latency detection
   - Connection drops between clouds
   - Encryption failures

## Conclusion

This network architecture design provides a robust foundation for deploying HMS components across AWS and Azure clouds. By leveraging Cilium's capabilities with proper cloud-specific integrations, we can achieve a unified networking model that ensures secure, observable, and performant communication across cloud boundaries.

The implementation allows for flexible deployment options while maintaining consistent security and operational models, making it easier to manage HMS components regardless of their cloud location.