# Terraform Enterprise State Recovery Lab

[![State Lab CI](https://github.com/alexcgodwin/terraform-enterprise-state-recovery-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/alexcgodwin/terraform-enterprise-state-recovery-lab/actions/workflows/ci.yml)

Demonstrates recovery of Terraform state bindings under change control, with isolated, executable state-move, state-detach, and drift-plan exercises plus an import scenario. No AWS credentials or cloud resources are required for the automated labs.

## Engineering scope

| Workflow | Executable evidence | Required operator control |
| --- | --- | --- |
| `terraform state mv` | Disposable local state, no-recreate plan | Exclusive lock, coordinated config update |
| `terraform state rm` | Dry-run, detach and state inspection | Backup and ownership transfer review |
| `terraform import` | Existing random ID import contract | Match live attributes and verify plan |
| Drift diagnosis | `-detailed-exitcode` 2 in local lab | Distinguish config change from external drift |
| Backend migrations | S3 versioning / native locking runbook | Encrypt, backup, test and compare lineage |
| Stale lock recovery | Decision and escalation runbook | Never force-unlock an active writer |

## Run the labs

Prerequisites: Terraform >= 1.6, Python >= 3.10.

```bash
python -m unittest discover -s tests -v
python scripts/recovery_lab.py move
python scripts/recovery_lab.py detach
python scripts/recovery_lab.py drift
python scripts/import_lab.py
```

Each script creates and cleans up its own temporary local Terraform directory. Real state is not touched. The `import` exercise uses a disposable local workspace and the logical random provider; you can also run the import manually using the [state recovery guide](docs/STATE_RECOVERY.md).

## Decisions and recovery documentation

Read [State Recovery](docs/STATE_RECOVERY.md) and [Runbooks](docs/RUNBOOKS.md) before using similar commands against a real backend. Terraform state is sensitive and this repository deliberately does not include production state samples, credentials, or a destructive automation pipeline.

**Status:** Validated learning and operational reference. It is not evidence of a live production state incident or employer-specific implementation.
