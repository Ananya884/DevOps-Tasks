# Task 03: Jenkins CI Pipeline with Slack Failure Alerts

A declarative Jenkins pipeline that clones this repo, builds the API Docker
image, and posts a Slack message when any stage fails.

## Pipeline stages

1. **Clone**: `checkout scm` pulls the repo from GitHub.
2. **Build image**: `docker build -t task03-api:<build number> api`.
3. **Verify**: lists the built image.
4. **Simulated failure** (optional): runs only when the `FORCE_FAIL`
   parameter is ticked, so the alert path can be tested on demand.

A `post { failure { ... } }` block sends the Slack notification.

## Setup

- Jenkins LTS on Ubuntu (EC2 t3.small, 2 GB RAM plus 2 GB swap), OpenJDK 21
- The `jenkins` user is in the `docker` group so builds can run Docker
- Pipeline job uses "Pipeline script from SCM", branch `*/main`,
  script path `jenkins-ci/Jenkinsfile`
- Slack incoming webhook stored as a Jenkins **Secret text** credential
  (`slack-webhook`). It is never written in the Jenkinsfile or the repo,
  and Jenkins masks it in build logs.

## Testing the alert

Run "Build with Parameters" with `FORCE_FAIL` ticked. The build fails on
purpose and `Build FAILED: <job> #<n> - <url>` arrives in Slack.

## Problems met and fixes

- **Build waited forever for an executor:** Jenkins took the built-in node
  offline because /tmp (a 953 MB tmpfs) was under its 1 GiB free-space
  threshold. Fixed by enlarging /tmp and lowering the threshold.
- **Jenkins unreachable after a few hours:** my public IP had changed, so the
  security group rules (restricted to my IP) dropped traffic. Updated the rules.

