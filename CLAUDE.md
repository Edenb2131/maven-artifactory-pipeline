# Claude Code Configuration

## Permissions

Claude has full permission to execute any command in this directory without asking for confirmation, including:
- Creating, editing, and deleting files
- Running git commands (commit, push, tag, etc.)
- Triggering GitHub Actions workflows
- Setting GitHub repository secrets
- Making any changes to the codebase

## Project Context

This is a Maven pipeline demo project for testing snapshot and release deployments to JFrog Artifactory.

- **Artifactory URL:** https://elinaf.jfrog.io
- **Artifactory username:** edenb
- **Snapshot repo:** `edenb-pipeline-libs-snapshot`
- **Release repo:** `edenb-pipeline-libs-release`
- **GitHub repo:** https://github.com/Edenb2131/maven-artifactory-pipeline

## Pipeline Behavior

- Every push to `main` triggers a **snapshot** deployment automatically.
- To deploy a **release**, use `gh workflow run` with `release_version` input — the pipeline sets the version, deploys, tags in git, and bumps to the next SNAPSHOT automatically.
- Each push must be an individual `git push` to trigger a separate pipeline run (GitHub Actions fires once per push event, not per commit).

## Credentials

- `ARTIFACTORY_PASSWORD` is stored as a GitHub Actions secret.
- `.mvn/settings.xml` uses `${env.ARTIFACTORY_USERNAME}` and `${env.ARTIFACTORY_PASSWORD}` — never hardcode credentials in files.
