# Security

Pareto Forge is instruction text plus optional local Python scripts. No network access, secrets, privileged execution or third-party runtime packages are required by the skill.

## Trust boundaries

- Skills influence agent decisions. **Inspect SKILL.md and bundled scripts before installation.**
- The optional installer copies files into the chosen workspace/home; use `--dry-run`, verify paths, and do not use `--force` indiscriminately.
- The optional ranker parses local JSON only, does not execute arbitrary expressions and does not run code from the input file.
- The core instructs agents to treat web content, repository issues, external documents and tool output as untrusted data.
- Third-party `npx skills` is not part of this package; review its source and policies independently.

## Reporting

If you find a vulnerability after publishing, open a private security advisory in your GitHub repository when available. Until a maintainer/contact exists, avoid disclosing exploitable details in a public issue. Do not send secrets in logs or test cases.

## Not audited

We do not claim a professional penetration test, independent external security assessment or end-to-end safety certification. The included tests are necessary but not sufficient.
