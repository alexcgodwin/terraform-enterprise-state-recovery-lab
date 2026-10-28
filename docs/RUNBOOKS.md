# State incident scenarios

| Symptom | Initial checks | Safe next step | Anti-pattern |
| --- | --- | --- | --- |
| Plan wants to recreate renamed resource | State address vs config, moved blocks | Coordinate refactor, `moved` or reviewed `state mv` | Apply before mapping update |
| Existing resource should be adopted | Provider ID, current owner, config parity | Plan `import` and re-plan | Duplicate management of one object |
| Ownership transferred to another system | State reference, config removal, backups | `state rm -dry-run`, approved detach | Assume remote object was deleted |
| Lock held too long | CI jobs, backend lease, lock ID | Confirm stale lock and obtain approval | `-lock=false` |
| Resource changed out of band | Refresh, CloudTrail, Terraform config | Reconcile intentional/unintended drift | `apply` to erase unexplained drift |
| State migration | Backend versioning / IAM / lineage | Backup, `init -migrate-state`, verify | Copy raw state over current state |

Run `python scripts/recovery_lab.py move`, `detach`, or `drift` to reproduce three zero-cloud scenarios. The import lab is manual to teach ID verification and plan review.
