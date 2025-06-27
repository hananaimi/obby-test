➜ helm install mimir grafana/mimir-distributed -f mimir-values.yaml -n mimir


W0626 14:45:31.149083  167268 warnings.go:70] metadata.name: this is used in Pod names and hostnames, which can result in surprising behavior; a DNS label is recommended: [must not contain dots]
NAME: mimir
LAST DEPLOYED: Thu Jun 26 14:45:25 2025
NAMESPACE: mimir
STATUS: deployed
REVISION: 1
NOTES:
Welcome to Grafana Mimir!
Remote write endpoints for Prometheus or Grafana Agent:
Ingress is not enabled, see the gateway.ingress values.
From inside the cluster:
  http://mimir-gateway.mimir.svc:80/api/v1/push

Read address, Grafana data source (Prometheus) URL:
Ingress is not enabled, see the gateway.ingress values.
From inside the cluster:
  http://mimir-gateway.mimir.svc:80/prometheus

**IMPORTANT**: Always consult CHANGELOG.md file at https://github.com/grafana/mimir/blob/main/operations/helm/charts/mimir-distributed/CHANGELOG.md and the deprecation list there to learn about breaking changes that require action during upgrade.
