Declarative Automation Bundles are Databricks' infrastructure-as-code format for packaging data, analytics, and ML projects as source-controlled bundles. They define jobs, pipelines, notebooks, Python code, tests, model-serving resources, permissions, and deployment targets so teams can validate, deploy, and run Databricks workloads through CI/CD.

## Source

- [[raw/clippings/What are Declarative Automation Bundles.md|raw/clippings/What are Declarative Automation Bundles.md]]

## What a Bundle Contains

A bundle is an end-to-end project definition. It can include:

- Workspace and cloud configuration
- Source files such as notebooks and Python modules
- Lakeflow Jobs
- Lakeflow Spark Declarative Pipelines
- Dashboards
- Model Serving endpoints
- MLflow Experiments
- Registered models
- Unit and integration tests
- Environment targets and deployment metadata

The key idea is that Databricks resources become versioned source files rather than click-built workspace state.

## When to Use Bundles

Bundles fit projects where reproducibility, collaboration, and CI/CD matter:

| Scenario | Why bundles help |
|---|---|
| Team-based data or ML projects | Organize notebooks, jobs, pipelines, and tests in one source-controlled unit |
| MLOps stacks | Deploy training, batch inference, model registry, and serving resources consistently |
| Regulated work | Preserve history of code and infrastructure changes |
| Standard project templates | Encode team defaults for permissions, service principals, and CI/CD |
| Multi-environment deployment | Promote the same project across dev, staging, and production |

For quick one-off notebooks, bundles may be unnecessary overhead. For production ML and analytics, they bring Databricks closer to normal software engineering practice.

## Lifecycle

The core bundle loop is:

```bash
databricks bundle init
databricks bundle validate
databricks bundle deploy
databricks bundle run
```

The CLI reads YAML configuration, resolves targets, uploads source files, creates or updates Databricks resources, and runs the declared workflows.

## Bundle vs Ad Hoc Workspace Work

| Ad hoc workspace work | Bundle-based work |
|---|---|
| Resources created manually | Resources declared in source |
| Harder to review changes | Changes reviewed in pull requests |
| Environment drift is common | Targets make environment differences explicit |
| CI/CD is bolted on later | CI/CD is part of the project shape |
| Project structure varies by user | Templates can standardize structure |

Bundles are essentially an IaC layer for Databricks project assets.

## Related Topics

- [[mlops]] - production ML deployment, monitoring, and release patterns
- [[system-design]] - source-controlled infrastructure and deployment topology
- [[ai-coding]] - code review, CI, and disciplined automation
- [[docling]] - document processing pipelines that can feed data and ML systems
- [[hugging-face]] - model ecosystem often used alongside Databricks ML workflows
