# Terraform state incident response and ownership

## Before any state mutation

1. Open a change record, identify resource ID and owning workspace.
2. Freeze competing plans and applies in CI. Check drift and policy exceptions.
3. Verify the backend, region, credentials, and current state lineage and serial.
4. Create an encrypted, access-controlled state backup and document retention.
5. Use `terraform state list`, `state show`, `plan -refresh-only` and provider console to reconcile remote objects.
6. Run the state operation with locking **enabled** and `-lock-timeout=5m` where supported.
7. Verify `terraform plan -detailed-exitcode`, state mappings, provider IDs, and drift after the change.
8. Publish a redacted change/evidence summary, not state or secrets.

## Moving without recreating

For a resource rename, prefer a declarative `moved` block under version control. In exceptional coordinated refactors, `terraform state mv OLD NEW` moves a binding. Update configuration in the same maintenance window so another apply cannot destroy/recreate it. The automated `move` exercise does this in a temporary local state directory.

## Detaching without deleting

`terraform state rm -dry-run ADDRESS` previews what will be forgotten. A subsequent `state rm` only deletes Terraform's *tracking record*, not the real cloud object. If the resource block remains in configuration, the next plan will propose to create the object again, possibly causing collisions. This is why detaching in live environments requires a configuration, migration, or ownership plan.

## Importing a pre-existing object

Example with a known value supplied by the random provider (`labs/import`):

```sh
cd labs/import
terraform init
terraform import random_id.existing p-9hUg
terraform state show random_id.existing
terraform plan -detailed-exitcode
```

The imported `random_id` requires its `byte_length` and any keepers/prefix to match the actual object or the plan can propose replacement. Do not apply blindly. For real AWS resources, verify the provider's documented ID shape and build a matching resource declaration, then import to exactly one state address. `import` does not create the remote object.

## Diagnosing drift

`terraform plan -refresh-only` checks remote changes via provider APIs; `terraform plan -detailed-exitcode` communicates intended changes (0 no changes, 2 changes, 1 error). The local `drift` lab simulates a configuration mismatch; **it is not evidence of real external drift**.

## Lock recovery

Never use `-lock=false` to bypass an active writer. Identify the workspace, lock ID, and live process; verify a genuine stale lock; get operator approval; then use `terraform force-unlock LOCK_ID` only if ownership is established. A force-unlock does not fix an interrupted apply. Reconcile drift afterward.

## Backend migration

For S3, configure encryption, restrictive IAM, bucket versioning, audit logging and native `use_lockfile = true` before using `terraform init -migrate-state`. Separate each environment by state key. Backup first; migrate through reviewed changes; compare state lineage, serial, and resource addresses before/after; do not commit `.tfstate` or backend credentials.

See HashiCorp's Terraform CLI state and import documentation for flags specific to your backend and version.
