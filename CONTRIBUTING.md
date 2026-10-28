# Engineering contribution rules

1. Open an issue specifying the failure mode and acceptance criteria.
2. Commit on a branch and request peer review for changes affecting state, public module inputs, pipelines, or security controls.
3. Provide a reproducible failure case and automated regression tests.
4. Prefer local or mocked tests; production Terraform apply is never run by repository CI.
5. Treat state, plan artifacts and provider credentials as sensitive. Never commit them.
6. Record interface-breaking changes in a release note and migration guide.
7. Keep runbook guidance explicit about locking, backups, authorization, blast radius and rollback.

The repository is an engineering lab, not evidence of a past employer deployment.
