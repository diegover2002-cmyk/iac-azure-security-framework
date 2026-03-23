# Service Catalog Maturity Roadmap

This document tracks the current maturity of deployable Azure service baselines in this repository.

## Maturity Levels

- `Golden Reference`: Deep service baseline with strong control detail and reusable patterns for future authoring.
- `Strong Baseline`: Good service coverage and useful control mappings, but not yet as rich as the golden references.
- `Expanded Baseline`: Useful and consistent baseline documentation is present, but deeper control detail and examples are still needed.

## Golden Reference

- Azure Storage Account
- Azure Key Vault
- Azure Virtual Network
- Azure App Service
- Azure Kubernetes Service

## Strong Baseline

- Azure SQL Database
- Azure Cosmos DB
- Azure API Management
- Azure Functions
- Azure Backup
- Azure Firewall
- Azure Front Door
- Azure Container Registry
- Azure Service Bus
- Azure Event Hubs
- Azure Monitor
- Azure Application Gateway
- Azure App Configuration
- Azure Cache for Redis
- Azure Logic Apps
- Azure Private Link
- Azure Event Grid

## Expanded Baseline

- Azure Bastion
- Azure Container Apps
- Azure Container Instances
- Azure Data Factory
- Azure Data Share
- Azure DNS
- Azure Load Balancer
- Azure Public IP
- Azure Web Application Firewall

## Next Priorities

1. Promote networking and edge services to strong baseline status.
2. Promote messaging and integration services to strong baseline status.
3. Deepen observability and supply-chain services.
4. Add reusable validation mapping guidance where Checkov coverage is partial or custom.

## Recommended Promotion Order

1. Azure DNS
2. Azure Web Application Firewall
3. Azure Data Factory
4. Azure Container Apps
5. Azure Bastion
6. Azure Load Balancer
7. Azure Public IP
8. Azure Application Gateway validation coverage review
