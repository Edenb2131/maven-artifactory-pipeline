# Maven Artifactory Pipeline

A demo Maven project for testing **snapshot** and **release** deployments to [JFrog Artifactory](https://elinaf.jfrog.io).

---

## Project Structure

```
├── pom.xml                                   # Maven project definition & distributionManagement
├── .mvn/settings.xml                         # Artifactory server credentials & mirror config
├── .github/workflows/maven-artifactory.yml  # GitHub Actions CI/CD pipeline
└── src/
    ├── main/java/io/jfrog/example/Calculator.java
    └── test/java/io/jfrog/example/CalculatorTest.java
```

---

## Artifactory Repositories

| Type     | Repository Name                    | URL |
|----------|------------------------------------|-----|
| Release  | `edenb-pipeline-libs-release`      | `https://elinaf.jfrog.io/artifactory/edenb-pipeline-libs-release` |
| Snapshot | `edenb-pipeline-libs-snapshot`     | `https://elinaf.jfrog.io/artifactory/edenb-pipeline-libs-snapshot` |

---

## Pipeline Overview

The pipeline is defined in [`.github/workflows/maven-artifactory.yml`](.github/workflows/maven-artifactory.yml) and consists of three jobs:

### 1. Build & Test
- **Triggers:** every push to `main`, every pull request targeting `main`
- Runs `mvn clean verify` — compiles, runs unit tests, and produces the JAR
- Uploads Surefire test reports as a build artifact

### 2. Deploy Snapshot
- **Triggers:** push to `main` (when no `release_version` input is provided)
- Verifies the `pom.xml` version ends in `-SNAPSHOT`
- Runs `mvn deploy` → artifact lands in `edenb-pipeline-libs-snapshot`
- Each run produces a unique timestamped snapshot (e.g., `1.0.0-20260315.120000-1`)

### 3. Deploy Release
- **Triggers:** manual `workflow_dispatch` with a `release_version` input (e.g., `1.2.0`)
- Sets the version in `pom.xml`, deploys to `edenb-pipeline-libs-release`
- Creates a git tag `v<version>` and commits it back to `main`
- Automatically bumps `pom.xml` to the next `-SNAPSHOT` version

---

## How to Trigger a Snapshot Deployment

Push any commit to `main`. The pipeline will automatically build, test, and deploy a new snapshot to Artifactory.

```bash
git commit -m "your change" && git push origin main
```

---

## How to Trigger a Release Deployment

1. Go to **Actions → Maven Artifactory Pipeline → Run workflow**
2. Enter the `release_version` (e.g., `1.0.0`)
3. Click **Run workflow**

The pipeline will:
- Set `pom.xml` version to `1.0.0`
- Deploy to `edenb-pipeline-libs-release`
- Tag the commit as `v1.0.0`
- Bump `pom.xml` to `1.0.1-SNAPSHOT` and push

---

## Required GitHub Secret

| Secret Name           | Description                              |
|-----------------------|------------------------------------------|
| `ARTIFACTORY_PASSWORD` | Artifactory API key or user password for `edenb` |

Set via: **Settings → Secrets and variables → Actions → New repository secret**

---

## Snapshot History

| Run | Commit | Deployed Version | Artifactory Timestamp |
|-----|--------|------------------|-----------------------|
| #1  | Initial pipeline setup | `1.0.0-SNAPSHOT` | triggered on push |
| #2  | Add README documentation | `1.0.0-SNAPSHOT` | triggered on push |
| #3  | Add snapshot run notes | `1.0.0-SNAPSHOT` | triggered on push |

Each snapshot is stored with a unique build timestamp in Artifactory under `edenb-pipeline-libs-snapshot/io/jfrog/example/maven-artifactory-pipeline/1.0.0-SNAPSHOT/`.

---

## Local Development

```bash
# Build and test locally
mvn clean verify

# Deploy snapshot locally (requires Artifactory credentials in env)
export ARTIFACTORY_USERNAME=edenb
export ARTIFACTORY_PASSWORD=<your-token>
mvn deploy --settings .mvn/settings.xml
```
