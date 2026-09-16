# CIS CLD AI Applications

A paginated Streamlit page cataloguing the AI applications delivered by CIS CLD. AWS-hosted applications are listed first, then the Streamlit ones.

Each entry has a serial number, a title, a two-line description, a Category (use case or industry), its Infosys Hexagon pillar (AI Strategy & Engineering, Data for AI, Process AI, Agentic Legacy Modernization, Physical AI, AI Trust), the Technology Stack detected from the app's dependency files, Business Drivers, and Business Benefits with a conservative estimated annual saving.

Savings are modelled, not measured: labour savings = hours saved per year × $75/hr blended rate; FinOps savings = 2–3% of an assumed $1M/yr cloud bill. Each row shows its basis.

Full documentation: [DOCUMENTATION.md](DOCUMENTATION.md) — what the page shows, how it is deployed and secured, the savings method, the data model, and the full list of applications.

## Run locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy on Streamlit Community Cloud

New app → repository `ajittgosavii/cicldaiprojects`, branch `main`, main file `streamlit_app.py`. Then add the sign-in account under Manage app → Settings → Secrets.

## Sign-in

Accounts live in the app's secrets (`.streamlit/secrets.toml` locally, which is gitignored), as salted PBKDF2 hashes:

```toml
[auth.users]
"cicld-admin" = "pbkdf2_sha256$240000$<salt>$<digest>"
```

Add a user by hashing their password: `python -c "import auth; print(auth.hash_password('their-password'))"`. The login protects the page, not the repo: `projects.json` is readable by anyone who can see this repository.

## Updating the list

All entries are in `projects.json` (`sno`, `title`, `description`, `category`, `hexagon`, `stack`, `drivers`, `benefit`, `savings_usd`, `savings_basis`, `where`, `repo`, `variants`). Edit that file and push; the page reloads from it. Keep `sno` contiguous, with the AWS-hosted rows first.
