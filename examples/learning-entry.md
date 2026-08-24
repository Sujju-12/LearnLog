---
id: 2026-08-24-kubernetes-services
title: Kubernetes Services
date: 2026-08-24
visibility: private
summary: ClusterIP, NodePort, and LoadBalancer services, including how kube-proxy forwards traffic.
topics:
  - kubernetes
  - networking
skills:
  - clusterip
  - nodeport
  - loadbalancer
learning_type:
  - documentation
  - hands-on
  - ai-assisted
status: captured
tags:
  - eks
  - kube-proxy
resources:
  - provider: IBM
    type: article
    title: Kubernetes Networking
    url: ""
    notes: Overview of cluster networking and service types.
  - provider: OpenAI
    type: ai_conversation
    title: Understanding kube-proxy
    url: ""
    notes: Clarified iptables vs IPVS modes.
  - provider: AWS
    type: documentation
    title: Amazon EKS Networking
    url: ""
related_projects: []
related_achievements: []
---

# Kubernetes Services

## What I learned

Kubernetes Services give pods a stable virtual IP and DNS name. ClusterIP stays
inside the cluster. NodePort exposes a high port on every node. LoadBalancer
asks the cloud provider for an external address.

## Understanding

kube-proxy programs forwarding rules so traffic to a Service IP reaches a
healthy endpoint. The Service is not a process that sits in the data path; it
is an API object plus those rules.

## Key concepts

- ClusterIP, NodePort, LoadBalancer, ExternalName
- Endpoints / EndpointSlices
- kube-proxy modes (iptables, IPVS, nftables)

## Hands-on work

- Created a Deployment and ClusterIP Service in a local cluster
- Inspected `kubectl get endpoints` after scaling replicas

## Knowledge gaps

- How AWS NLB target-type IP interacts with kube-proxy on EKS

## Next steps

- Read AWS load balancer controller docs
- Capture a follow-up entry on Ingress vs Gateway API
