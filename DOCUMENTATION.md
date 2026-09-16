# CIS CLD AI Applications — application documentation

A Streamlit web page that catalogues the 85 AI applications delivered by CIS CLD. Each entry carries a
description, a use-case category, its Infosys Hexagon pillar, the technology stack detected from the app's own
dependency files, its business drivers, and a conservative modelled annual saving.

- **Repository:** https://github.com/ajittgosavii/cicldaiprojects
- **Entry point:** `streamlit_app.py`
- **Runs on:** Streamlit Community Cloud (or locally)
- **Access:** sign-in required

---

## 1. What the page does

Someone opening the page signs in, then sees the whole portfolio as one paginated table, with a bar across the top
showing how the portfolio splits across the six Hexagon pillars. They can filter by pillar or category, sort, and
page through the list. Every application title links to its GitHub repository where one exists
(65 of 85 do; a further 40 repositories are listed as variants of those entries).

**Ordering.** AWS-hosted applications come first, then the Streamlit ones, then the rest. The serial numbers follow
that order, so row 1 is the first AWS-hosted app.

| Hosting | Applications | Position in the list |
|---|---:|---|
| AWS | 21 | listed first |
| Streamlit | 53 | after the AWS apps |
| Other | 11 | last |

---

## 2. Deploying it

1. Go to share.streamlit.io → **Create app**.
2. Repository `ajittgosavii/cicldaiprojects`, branch `main`, main file `streamlit_app.py`.
3. Open **Manage app → Settings → Secrets** and paste the `[auth.users]` block (see below). Until you do, the page
   loads but says sign-in isn't set up, and nobody can get in.

Streamlit is pinned to `1.59.0` in `requirements.txt`. That is deliberate: newer releases lay `st.pills` out on a
single clipped line, which hides some of the pillar filter buttons. Test on a new version before unpinning.

## 3. Running it locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Sign-in reads `.streamlit/secrets.toml`, which git ignores. Create it with the same `[auth.users]` block.

---

## 4. Sign-in

Accounts live in the app's secrets, never in the repository, as salted PBKDF2-SHA256 hashes (240,000 iterations):

```toml
[auth.users]
"cicld-admin" = "pbkdf2_sha256$240000$<salt-hex>$<digest-hex>"
```

Add a colleague by hashing their password and adding a line:

```bash
python -c "import auth; print(auth.hash_password('their-password'))"
```

Behaviour worth knowing:

- A wrong username and a wrong password give the same message, and an unknown username takes the same time as a
  known one, so the form does not reveal which accounts exist.
- Five failed attempts lock sign-in for 60 seconds.
- Sessions are per browser session: refreshing the page signs the viewer out again.
- **The login protects the page, not the data.** The repository is public, so `projects.json` is readable by anyone
  who can see the repo. Make the repository private if the catalogue itself is sensitive.

---

## 5. What each column means

| Column | Meaning |
|---|---|
| S.No | Position in the list; AWS-hosted applications first |
| Application Title | Links to the GitHub repository; other builds of the same app appear beneath as variants |
| Description | Two sentences: what it does, then how it is built |
| Category | The use case or industry, e.g. Cloud Migration, Aviation, Energy & Utilities |
| Infosys Hexagon | One of the six pillars |
| Technology Stack | Read from the app's `requirements.txt`, `pyproject.toml`, `package.json`, Dockerfile or Terraform — not hand-written |
| Business Drivers | Why a business would want it, e.g. Risk reduction, Modernisation |
| Business Benefits (est.) | A one-line benefit, a modelled annual saving, and the basis for it |

### The savings figures are modelled, not measured

No application here reports measured savings, so every figure is an estimate built from a stated assumption, and the
page says so under the table. Two bases are used:

- **Labour:** hours saved per year × a conservative **$75/hr** blended rate.
- **FinOps:** **2–3%** of an assumed **$1M/yr** cloud bill.

Across the portfolio this totals about **$1.65M a year**. Treat it as an order-of-magnitude
indication for a mid-size enterprise, not a result. If you have your own rate or cloud spend, the numbers should be
recalculated before the page is shown to a customer.

---

## 6. The portfolio at a glance

| Infosys Hexagon pillar | Applications | Modelled saving |
|---|---:|---:|
| AI Strategy & Engineering | 21 | ~$435K |
| Data for AI | 17 | ~$292K |
| Process AI | 9 | ~$148K |
| Agentic Legacy Modernization | 23 | ~$464K |
| Physical AI | 1 | ~$22K |
| AI Trust | 14 | ~$289K |

**Largest categories**

| Category | Applications |
|---|---:|
| Security & Compliance | 13 |
| Cloud Migration | 11 |
| Database | 9 |
| Cloud Infrastructure | 5 |
| Database Migration | 5 |
| Software Engineering | 5 |
| FinOps | 5 |
| Kubernetes | 3 |
| End-User Computing | 3 |
| Cloud Operations | 2 |
| Legal | 2 |
| Infrastructure as Code | 2 |

**Most common technologies**

| Technology | Applications |
|---|---:|
| Streamlit | 58 |
| Claude (Anthropic) | 56 |
| Pandas | 53 |
| Plotly | 46 |
| AWS SDK (boto3) | 37 |
| FastAPI | 22 |
| React | 21 |
| OpenAI | 20 |
| Excel export | 19 |
| PostgreSQL | 17 |
| ReportLab (PDF) | 15 |
| Docker | 13 |

---

## 7. Files

| File | Purpose |
|---|---|
| `streamlit_app.py` | The page: app bar, pillar mix bar, filters, table, pagination, footnote |
| `auth.py` | Sign-in gate, password hashing, the logo, and the animated login page |
| `projects.json` | The catalogue — the only file to edit when applications change |
| `requirements.txt` | Pinned Streamlit version |
| `.streamlit/config.toml` | Light theme and brand colours |
| `.streamlit/secrets.toml` | Accounts. Local only, git-ignored, never committed |

### `projects.json` fields

| Field | Notes |
|---|---|
| `sno` | Position, contiguous from 1, AWS-hosted first |
| `title`, `description` | Shown in the table |
| `category`, `hexagon` | Category and pillar; the pillar must be one of the six |
| `stack` | List of technologies, at most 8 shown |
| `drivers` | Business drivers, split on `·` onto separate lines |
| `benefit`, `savings_usd`, `savings_basis` | The benefit line, the modelled figure, and its basis |
| `where` | `GitHub`, `C:\aidemos`, `AWS` — drives the AWS-first ordering |
| `repo`, `variants` | Repository for the title link, and other builds of the same app |

To add or change an application: edit `projects.json`, keep `sno` contiguous with the AWS-hosted rows first, and
push. The page reloads from the file; its cache keys on the file's modification time, so no restart is needed.

---

## 8. Design

- **Type:** IBM Plex Sans, with the condensed cut for headings.
- **Colour:** navy ink on a cool grey-blue canvas, white cards with hairline borders.
- **Pillar colours** were checked with a colour-blindness validator. An earlier palette failed — its green and red
  were nearly identical under deuteranopia — so the six pillars use a tested categorical palette, and every pillar
  label carries its name in text with the colour only as a marker. Colour never carries meaning alone.
- **The login page** animates once on load: the hexagon logo draws itself, a cloud fades in and breathes, and three
  data points rise into it, over drifting colour fields, a sliding hexagon mesh and thin uplink streams. All motion
  stops when the viewer's system asks for reduced motion.
- **Narrow screens:** below about 1100px each application becomes a stacked card with field labels instead of a
  table that scrolls sideways.

---

## 9. Known limitations

- **The catalogue is duplicated.** The ECHO AI Lab portal (`ajittgosavii/projects`) holds its own copy of
  `projects.json`. A change to an application's description must be made in both repositories.
- **Savings are modelled**, as described above.
- **Sign-in does not survive a refresh**, since it is held in the Streamlit session.
- **Streamlit is pinned**; newer versions change how the filter buttons lay out.

---

## Appendix — the 85 applications

| # | Application | Category | Infosys Hexagon | Hosting | Est. saving |
|---:|---|---|---|---|---:|
| 1 | AWS Well-Architected Advisor | Cloud Infrastructure | AI Strategy & Engineering | AWS | ~$22K |
| 2 | Cloud Compliance Canvas | Security & Compliance | AI Trust | AWS | ~$38K |
| 3 | Container Vulnerability Management | Security & Compliance | AI Trust | AWS | ~$22K |
| 4 | CloudMigrate | Database Migration | Agentic Legacy Modernization | AWS | ~$45K |
| 5 | Application Lifecycle Tracker | IT Lifecycle Management | Agentic Legacy Modernization | AWS | ~$9K |
| 6 | Cobalt Migration Platform | Cloud Migration | Agentic Legacy Modernization | AWS | ~$75K |
| 7 | AI Agents Based Application Development Platform | Software Engineering | AI Strategy & Engineering | AWS | ~$22K |
| 8 | Agentic AWS FinOps | FinOps | Data for AI | AWS | ~$30K |
| 9 | Multi-Cloud AI Operations Platform | Cloud Operations | AI Strategy & Engineering | AWS | ~$30K |
| 10 | CIS Cloud Shield | Security & Compliance | AI Trust | AWS | ~$38K |
| 11 | AI Cloud Automation Platform | Cloud Infrastructure | AI Strategy & Engineering | AWS | ~$38K |
| 12 | BI Dashboard Security Center | Security & Compliance | AI Trust | AWS | ~$4K |
| 13 | DB Performance AI Agent | Database | Data for AI | AWS | ~$19K |
| 14 | GovScope | Public Sector | Data for AI | AWS | ~$15K |
| 15 | TGW Atlas | Networking | AI Strategy & Engineering | AWS | ~$15K |
| 16 | AWS Transform Hub | Cloud Migration | Agentic Legacy Modernization | AWS | ~$30K |
| 17 | GCP Cloud Shield | Security & Compliance | AI Trust | AWS | ~$30K |
| 18 | AI Tech Debt Analyzer | Software Engineering | Agentic Legacy Modernization | AWS | ~$22K |
| 19 | SpecCraft | Software Engineering | Agentic Legacy Modernization | AWS | ~$22K |
| 20 | TD2BQ SQL Converter | Data Warehouse Migration | Agentic Legacy Modernization | AWS | ~$45K |
| 21 | KubeOps AI | Kubernetes | AI Strategy & Engineering | AWS | ~$38K |
| 22 | Advanced Multi-Agent Security System | Security & Compliance | AI Trust | Streamlit | ~$11K |
| 23 | AI Code Reviewer | Software Engineering | AI Strategy & Engineering | Streamlit | ~$11K |
| 24 | AI Estimator for LLMs | AI Adoption | AI Strategy & Engineering | Streamlit | ~$6K |
| 25 | AI/ML Observability Platform | MLOps | AI Strategy & Engineering | Streamlit | ~$15K |
| 26 | AeroTrack AI | Aviation | Process AI | Streamlit | ~$30K |
| 27 | AI Database Migration Studio | Database Migration | Agentic Legacy Modernization | Streamlit | ~$15K |
| 28 | AI Decision War Room | Decision Intelligence | Process AI | Streamlit | ~$4K |
| 29 | Secure Enterprise DB Analyzer | Database | Data for AI | Streamlit | ~$11K |
| 30 | AI-Enhanced AWS Compliance Platform | Security & Compliance | AI Trust | Streamlit | ~$22K |
| 31 | Enterprise AWS Cost Management | FinOps | Data for AI | Streamlit | ~$30K |
| 32 | AWS Enterprise Assessment Platform | Cloud Migration | Agentic Legacy Modernization | Streamlit | ~$12K |
| 33 | AWS Guardrails Platform | Security & Compliance | AI Trust | Streamlit | ~$19K |
| 34 | AWS Landing Zone Studio | Cloud Infrastructure | AI Strategy & Engineering | Streamlit | ~$12K |
| 35 | AWS Credential & Backup Governance | Security & Compliance | AI Trust | Streamlit | ~$11K |
| 36 | CloudIDP — Multi-Account Cloud Platform | Cloud Infrastructure | AI Strategy & Engineering | Streamlit | ~$60K |
| 37 | Citrix to AWS EUC Migration Studio | End-User Computing | Agentic Legacy Modernization | Streamlit | ~$15K |
| 38 | Azure CloudOps AI Platform | Cloud Operations | AI Strategy & Engineering | Streamlit | ~$22K |
| 39 | VDI Migration Assessment Tool | End-User Computing | Agentic Legacy Modernization | Streamlit | ~$9K |
| 40 | BOMOCO Cloud Optimizer | Energy & Sustainability | AI Strategy & Engineering | Streamlit | ~$20K |
| 41 | AI Contract Lifecycle Management | Legal | Process AI | Streamlit | ~$30K |
| 42 | Database Metrics Collector | Database | Data for AI | Streamlit | ~$11K |
| 43 | Enterprise Database Migration Analyzer | Database Migration | Agentic Legacy Modernization | Streamlit | ~$15K |
| 44 | vROps-Driven AWS Migration Sizing | Cloud Migration | Agentic Legacy Modernization | Streamlit | ~$15K |
| 45 | EKS Operations Platform | Kubernetes | AI Strategy & Engineering | Streamlit | ~$22K |
| 46 | HOLDPOINT Permit Safety Reviewer | Energy & Utilities | Physical AI | Streamlit | ~$22K |
| 47 | AWS EC2 SQL Server Sizing Calculator | Cloud Migration | Agentic Legacy Modernization | Streamlit | ~$11K |
| 48 | AI Database Management Suite | Database | Data for AI | Streamlit | ~$15K |
| 49 | Regulatory Compliance AI Platform | Legal & Regulatory | Process AI | Streamlit | ~$30K |
| 50 | Cloud Migration Tool Comparator | Cloud Migration | Agentic Legacy Modernization | Streamlit | ~$9K |
| 51 | Oracle to MongoDB Migration Analyzer | Database Migration | Agentic Legacy Modernization | Streamlit | ~$11K |
| 52 | Multi-Cloud FinOps Command Center | FinOps | Data for AI | Streamlit | ~$30K |
| 53 | Multi-Cloud Infrastructure Intelligence | Cloud Infrastructure | AI Strategy & Engineering | Streamlit | ~$38K |
| 54 | Multi-Cloud Security Scanner | Security & Compliance | AI Trust | Streamlit | ~$15K |
| 55 | Multi-DB Schema Documentation Tool | Database | Data for AI | Streamlit | ~$8K |
| 56 | GenAI Database Query Translator | Database | Data for AI | Streamlit | ~$9K |
| 57 | AWS Migration Analyzer | Cloud Migration | Agentic Legacy Modernization | Streamlit | ~$15K |
| 58 | AWS Migration Strategy Platform | Cloud Migration | Agentic Legacy Modernization | Streamlit | ~$19K |
| 59 | CISCLD Ascend | Cloud Migration | Agentic Legacy Modernization | Streamlit | ~$12K |
| 60 | Enterprise Productivity Tracker | Workplace Productivity | Process AI | Streamlit | ~$11K |
| 61 | Enterprise Migration Platform | Cloud Migration | Agentic Legacy Modernization | Streamlit | ~$15K |
| 62 | AWS RDS Migration & Sizing Tool | Database Migration | Agentic Legacy Modernization | Streamlit | ~$11K |
| 63 | Cloud Operations Resource Planning | Workforce Planning | Process AI | Streamlit | ~$4K |
| 64 | ReturnGuard AI | Retail & E-commerce | Process AI | Streamlit | ~$22K |
| 65 | SAP HANA Monitoring Copilot | SAP | Data for AI | Streamlit | ~$15K |
| 66 | SQL Server Scaling Platform | Database | Data for AI | Streamlit | ~$8K |
| 67 | AWS CloudWatch SQL Server Monitor | Database | Data for AI | Streamlit | ~$9K |
| 68 | SQL Server AI Optimizer Suite | Database | Data for AI | Streamlit | ~$11K |
| 69 | TechGuardrails | Security & Compliance | AI Trust | Streamlit | ~$30K |
| 70 | Telecom Churn Predictor | Telecom | Data for AI | Streamlit | ~$11K |
| 71 | Terraform Code Generator | Infrastructure as Code | AI Strategy & Engineering | Streamlit | ~$8K |
| 72 | Terraform to CDK Converter | Infrastructure as Code | Agentic Legacy Modernization | Streamlit | ~$11K |
| 73 | TrustLayer AI | AI Governance | AI Trust | Streamlit | ~$15K |
| 74 | Windows Vulnerability AI Agent | Security & Compliance | AI Trust | Streamlit | ~$30K |
| 75 | AWS WorkSpaces Provisioner | End-User Computing | AI Strategy & Engineering | Other | ~$11K |
| 76 | EKS GitOps Automation | Kubernetes | AI Strategy & Engineering | Other | ~$15K |
| 77 | Multi-Cloud FinOps on GCP | FinOps | Data for AI | Other | ~$30K |
| 78 | Container Vulnerability Demo App | Security & Compliance | AI Trust | Other | ~$3K |
| 79 | Migration Governance Controls | Cloud Migration | Agentic Legacy Modernization | Other | ~$19K |
| 80 | Smart Subscription Manager API | Consumer Finance | Process AI | Other | ~$4K |
| 81 | AWS FinOps Intelligence Platform | FinOps | Data for AI | Other | ~$30K |
| 82 | Agentic Bug Fixer | Software Engineering | AI Strategy & Engineering | Other | ~$15K |
| 83 | AI Digital Twin | Conversational AI | AI Strategy & Engineering | Other | ~$11K |
| 84 | Prelegal Contract Generator | Legal | Process AI | Other | ~$11K |
| 85 | MCP Training Demo | AI Engineering | AI Strategy & Engineering | Other | ~$3K |
