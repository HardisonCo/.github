# HMS Multi-Cloud Deployment Plan

## Executive Summary

This document outlines a comprehensive plan for deploying HMS system components as Kubernetes nodes across multiple cloud providers, specifically AWS and Azure. The implementation leverages HMS-SYS (based on Cilium networking) and OPS-CLI to create a unified management layer for cross-cloud operations.

## 1. System Architecture Overview

### 1.1 Core Components

- **HMS-SYS**: Core system providing networking, security, and observability using eBPF
- **HMS-OPS**: Operations component based on Cilium for network management
- **OPS-CLI**: Command-line interface for unified deployment and management
- **HMS Components**: Various HMS components to be deployed across clouds

### 1.2 Multi-Cloud Architecture

```
┌──────────────────────────────────────────┐   ┌──────────────────────────────────────────┐
│               AWS Cloud                  │   │              Azure Cloud                 │
│  ┌────────────────────────────────────┐  │   │  ┌────────────────────────────────────┐  │
│  │        Kubernetes Cluster 1        │  │   │  │        Kubernetes Cluster 2        │  │
│  │  ┌──────────┐        ┌──────────┐  │  │   │  │  ┌──────────┐        ┌──────────┐  │  │
│  │  │ HMS-SYS  │◄──────►│ HMS-DEV  │  │  │   │  │  │ HMS-SYS  │◄──────►│ HMS-OPS  │  │  │
│  │  └────┬─────┘        └──────────┘  │  │   │  │  └────┬─────┘        └──────────┘  │  │
│  │       │                            │  │   │  │       │                            │  │
│  │       ▼                            │  │   │  │       ▼                            │  │
│  │  ┌──────────┐        ┌──────────┐  │  │   │  │  ┌──────────┐        ┌──────────┐  │  │
│  │  │ HMS-API  │◄──────►│ HMS-CDF  │  │◄─┼───┼──┼─►│ HMS-NFO  │◄──────►│ HMS-DOC  │  │  │
│  │  └────┬─────┘        └──────────┘  │  │   │  │  └────┬─────┘        └──────────┘  │  │
│  │       │                            │  │   │  │       │                            │  │
│  │       ▼                            │  │   │  │       ▼                            │  │
│  │  ┌──────────┐        ┌──────────┐  │  │   │  │  ┌──────────┐        ┌──────────┐  │  │
│  │  │ HMS-A2A  │◄──────►│ HMS-Other│  │  │   │  │  │ HMS-ETL  │◄──────►│ HMS-Other│  │  │
│  │  └──────────┘        └──────────┘  │  │   │  │  └──────────┘        └──────────┘  │  │
│  │                                    │  │   │  │                                    │  │
│  └────────────────────────────────────┘  │   │  └────────────────────────────────────┘  │
│                                          │   │                                          │
└──────────────────────────────────────────┘   └──────────────────────────────────────────┘
                    ▲                                            ▲
                    │                                            │
                    │                                            │
                    ▼                                            ▼
             ┌─────────────────────────────────────────────────────────┐
             │                    OPS-CLI Interface                     │
             └─────────────────────────────────────────────────────────┘
```

### 1.3 Communication Flows

- **Intra-Cluster**: Normal Kubernetes pod-to-pod communication
- **Cross-Cluster/Same Cloud**: Cilium ClusterMesh for direct connectivity
- **Cross-Cluster/Cross-Cloud**: Secure tunnels using Cilium encryption or Cloud-provider VPC peering

## 2. Implementation Strategy

### 2.1 Preparation Phase

1. **Cluster Setup**
   - Deploy Kubernetes clusters in AWS and Azure
   - Configure identity and access management
   - Establish network connectivity between clusters

2. **HMS-SYS Installation**
   - Deploy HMS-SYS (Cilium) to each cluster with unique cluster IDs
   - Configure cloud-specific integrations
   - Enable ClusterMesh for cross-cluster communication

3. **OPS-CLI Configuration**
   - Set up OPS-CLI with multi-context support
   - Configure credentials for both AWS and Azure
   - Establish central configuration repository

### 2.2 Component Distribution Strategy

**AWS Cluster:**
- HMS-SYS: Core system services
- HMS-API: API gateway for all components
- HMS-DEV: Development tools
- HMS-A2A: Agent-to-agent communication
- HMS-CDF: Component distribution framework

**Azure Cluster:**
- HMS-SYS: Core system services
- HMS-OPS: Operations management
- HMS-NFO: Information services
- HMS-DOC: Documentation services
- HMS-ETL: Data extraction and transformation

### 2.3 Shared Services and State

- **Configuration Management**: Centralized configuration store accessible by all clusters
- **Secrets Management**: Kubernetes secrets, synchronized where needed
- **Service Discovery**: DNS-based with cross-cluster service resolution
- **Data Persistence**: Cloud-native options with cross-region replication

## 3. Technical Implementation

### 3.1 AWS-Specific Configuration

```yaml
# HMS-SYS AWS Cluster Configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: hms-sys-aws-config
  namespace: kube-system
data:
  cluster-id: "aws-1"
  ipam-mode: "eni"
  aws-vpc-id: "${AWS_VPC_ID}"
  aws-prefix-delegation-enabled: "true"
  tunnel-protocol: "geneve"
  encryption-enabled: "true"
  encryption-type: "wireguard"
```

### 3.2 Azure-Specific Configuration

```yaml
# HMS-SYS Azure Cluster Configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: hms-sys-azure-config
  namespace: kube-system
data:
  cluster-id: "azure-1"
  ipam-mode: "azure"
  azure-resource-group: "${AZURE_RESOURCE_GROUP}"
  azure-subscription-id: "${AZURE_SUBSCRIPTION_ID}"
  azure-user-assigned-identity-id: "${AZURE_USER_ASSIGNED_IDENTITY_ID}"
  tunnel-protocol: "geneve"
  encryption-enabled: "true"
  encryption-type: "wireguard"
```

### 3.3 ClusterMesh Configuration

```yaml
# ClusterMesh Configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: clustermesh-config
  namespace: kube-system
data:
  cluster-name: "${CLUSTER_NAME}"
  cluster-id: "${CLUSTER_ID}"
  enable-external-workloads: "true"
  enable-remote-node-identity: "true"
  clustermesh-config-create-secret: "true"
```

### 3.4 Cross-Cloud Network Configuration

**AWS VPC Peering to Azure:**
- Create a VPC peering connection from AWS to Azure
- Configure route tables for cross-cloud traffic
- Set up appropriate security groups

**Azure VNET Peering to AWS:**
- Create a VNET peering connection from Azure to AWS
- Configure route tables for cross-cloud traffic
- Set up appropriate network security groups

## 4. Deployment Workflow

### 4.1 Initial Setup

1. Create Kubernetes clusters in both AWS and Azure
2. Install HMS-SYS (Cilium) with basic configuration
3. Configure networking for cross-cloud communication
4. Set up OPS-CLI with contexts for both clouds

```bash
# Install HMS-SYS on AWS cluster
kubectl config use-context aws-cluster
cilium install --set cluster.id=1 --set ipam.mode=eni

# Install HMS-SYS on Azure cluster  
kubectl config use-context azure-cluster
cilium install --set cluster.id=2 --set ipam.mode=azure
```

### 4.2 Enable ClusterMesh

1. Enable ClusterMesh on both clusters
2. Configure cross-cluster connectivity
3. Verify communication between clusters

```bash
# Enable ClusterMesh on AWS cluster
kubectl config use-context aws-cluster
cilium clustermesh enable

# Enable ClusterMesh on Azure cluster
kubectl config use-context azure-cluster
cilium clustermesh enable

# Connect clusters
cilium clustermesh connect --context aws-cluster --destination-context azure-cluster
```

### 4.3 Deploy HMS Components

1. Deploy core services to both clusters
2. Deploy specific HMS components according to distribution strategy
3. Configure cross-component communication

```bash
# Deploy HMS-API to AWS cluster
kubectl config use-context aws-cluster
kubectl apply -f hms-api-deployment.yaml

# Deploy HMS-NFO to Azure cluster
kubectl config use-context azure-cluster
kubectl apply -f hms-nfo-deployment.yaml
```

## 5. Operational Considerations

### 5.1 Monitoring and Observability

- Deploy Hubble for network visibility across clusters
- Configure centralized logging with cross-cloud aggregation
- Implement distributed tracing for cross-component requests

### 5.2 Disaster Recovery

- Active-active deployment for critical components
- Regular backups of stateful services
- Cross-cloud failover procedures

### 5.3 Security Considerations

- End-to-end encryption for cross-cloud traffic
- Consistent network policies across clusters
- Identity and access management integration

## 6. Implementation Timeline

| Phase | Description | Duration |
|-------|-------------|----------|
| 1 | Preparation & Infrastructure Setup | 2 weeks |
| 2 | HMS-SYS & OPS-CLI Configuration | 1 week |
| 3 | Cross-Cloud Networking | 1 week |
| 4 | Component Deployment - AWS | 1 week |
| 5 | Component Deployment - Azure | 1 week |
| 6 | Testing & Validation | 2 weeks |
| 7 | Documentation & Knowledge Transfer | 1 week |

## 7. Conclusion

This plan provides a comprehensive approach to deploying HMS system components across AWS and Azure clouds using HMS-SYS and OPS-CLI. The implementation leverages Cilium's networking and security capabilities to create a unified operational model that spans multiple cloud providers.

By following this plan, organizations can achieve:

- Unified management of HMS components across cloud environments
- Consistent networking, security, and observability
- Flexible deployment options based on cloud-specific advantages
- Enhanced resiliency through cross-cloud distribution

## Appendix A: Useful OPS-CLI Commands

```bash
# Check status across all clusters
cilium status --context aws-cluster
cilium status --context azure-cluster

# Connectivity testing
cilium connectivity test --context aws-cluster
cilium connectivity test --context azure-cluster

# Cross-cluster connectivity
cilium clustermesh status --context aws-cluster
```

## Appendix B: Troubleshooting

Common issues and resolution steps:

1. **Cross-cluster connectivity issues**
   - Check ClusterMesh status
   - Verify network routes between clusters
   - Ensure correct service CIDR configuration

2. **Cloud-specific integration problems**
   - Validate cloud provider credentials
   - Check resource quotas and limits
   - Verify required cloud permissions

3. **Component deployment failures**
   - Check component logs
   - Validate Kubernetes resources
   - Ensure correct configuration