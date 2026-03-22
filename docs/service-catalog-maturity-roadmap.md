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

## Expanded Baseline

- Azure Application Gateway
- Azure Bastion
- Azure App Configuration
- Azure Cache for Redis
- Azure Container Apps
- Azure Container Instances
- Azure Data Factory
- Azure Data Share
- Azure DNS
- Azure Event Grid
- Azure Load Balancer
- Azure Logic Apps
- Azure Private Link
- Azure Public IP
- Azure Web Application Firewall

## Next Priorities

1. Promote networking and edge services to strong baseline status.
2. Promote messaging and integration services to strong baseline status.
3. Deepen observability and supply-chain services.
4. Add reusable validation mapping guidance where Checkov coverage is partial or custom.

## Recommended Promotion Order

1. Azure Application Gateway
2. Azure App Configuration
3. Azure Cache for Redis
4. Azure Logic Apps
5. Azure Private Link
6. Azure Event Grid
7. Azure DNS
8. Azure Web Application Firewall
