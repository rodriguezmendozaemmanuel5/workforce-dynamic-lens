# Changelog

All notable changes to this project will be documented in this file.

This project follows the **Keep a Changelog** format and **Semantic Versioning (SemVer)**.

## [v1.0.0] — 2026-09-02

### Added
- **Official Portfolio Release:** Publicación oficial y empaquetado del repositorio con arquitectura end-to-end completa.
- **Auditoría de Paridad QA Certificada:** Validación cruzada al 100% entre PostgreSQL (Kimball DWH) y medidas DAX en Power BI.
- **Assets Visuales:** Integración de capturas de alta resolución en `powerbi/Images/` correspondientes a las 3 vistas del dashboard.
- **Documentación de Entrevista STAR:** Publicación de `docs/interview_notes.md` con narrativas de impacto de $6.44M USD en P&L.

---

## [v0.9.0] — 2026-08-26
### 🛡️ Quality Assurance, Testing & Performance Optimization
- **E2E Consistency & Audit**: Conducted full cross-validation between PostgreSQL DW tables (`dim_employees`, `fact_terminations`, `fact_attendance_logs`, `fact_sla_events`), SQL analytical views (`sql/analytics/13_views.sql`), DAX measures in Power BI (`.pbix`), and documentation contracts (`KPIs_Definition.md`, `Business_Insights.md`).
- **Data Integrity & Traceability**: Audited all 7 business rule validation tests in `sql/analytics/14_validation_queries.sql` with 0 constraint or orphan record violations.
- **DAX & Model Optimization**: Verified display folders, explicit measure references, formatting, and performance across all 3 interactive dashboard screens.
- **Documentation & Positioning Alignment**: Realigned entire repository narrative strictly to **People Analytics, HR Data Analytics & Business Intelligence**, enhancing `README.md`, `docs/Business_Insights.md`, and `docs/interview_notes.md` (STAR method guide).

---

## [v0.8.0] — 2026-08-20
### 📊 Business Intelligence Suite & Executive Storytelling
- **Power BI Executive Model (`.pbix`)**: Completed semantic dimensional model connecting to PostgreSQL `people_analytics` star schema (`dim_employees`, `dim_departments`, `dim_positions`, `dim_date`, `dim_salary_benchmarks`, `fact_attendance_logs`, `fact_terminations`, `fact_sla_events`).
- **Interactive Executive Dashboards (3 Views)**:
  - *Screen 1 - Executive HR Overview & Demographics*: Macro-level headcount tracking (3,300 active / 1,200 historical exits), geographic distribution across 5 countries, gender equity and annualized turnover trends.
  - *Screen 2 - Absenteeism Diagnostic & SLA Impact*: Deep-dive analysis on rolling 12-month Bradford Factor ($S^2 \times D$), overtime accumulation correlation, and $1.3M+ in SLA breach penalty exposure across hospital support contracts.
  - *Screen 3 - Flight Risk & Retention Center*: Multi-factor flight risk scoring engine synthesizing Compa-Ratio gap, Bradford absenteeism and overtime trends to prioritize High Performers retention.
- **DAX Measures Group**: Engineered dynamic measures organized in display folders (Headcount, Turnover, Absenteeism, Financial Cost, Flight Risk, What-If Simulation).
- **Business Insights Report (`docs/Business_Insights.md`)**: Certified official business findings quantifying the **$6.44M USD mitigable P&L exposure**, identifying departmental bottlenecks in R&D and Clinical Support, and defining a 3-pillar action plan with a 535% ROI ($455k net benefit, 2.8 months payback).

---

## [v0.7.0] — 2026-08-14
### 🔴 Critical Fixes & System Reconciliation
- **Termination Reconciliation**: Implemented formal reconciliation between `fact_terminations` and `dim_employees`. Terminated employees are now correctly marked `is_active = FALSE` on their current SCD2 row (R01, R04, R06, R07).
- **Generation Pipeline Reordering**: Reordered generation pipeline: Dimensions → Employees → Terminations → Reconciliation → Attendance → SLA Events → Date Dimension → Validator Gate → CSV Export.
- **Ghost Attendance Eliminated**: Vectorized `attendance_generator.py` with per-employee active date bounds `[max(start_date, hire_date), min(end_date, termination_date)]`, eliminating 305,483 ghost attendance records post-offboarding (R11/R15).
- **Date Dimension Expansion**: Expanded `dim_date` range to `2012-01-01` – `2030-12-31` (6,940 days) across generators, ETL, and SQL schemas to cover all employee hire and termination dates (2012–2025).
- **PostgreSQL Schema Constraint Alignment**:
  - Updated `chk_date_sk_format` in `11_constraints.sql` to `BETWEEN 20100101 AND 20991231`.
  - Updated `chk_trm_date_min` in `11_constraints.sql` to `CHECK (termination_date >= '2010-01-01')`.
  - Aligned `chk_att_id_format` pattern to `^ATT_[0-9]{12,16}$` (`ATT_{YYYYMMDD}{counter:06d}`).

### 🟡 High Severity Fixes & Analytics Alignment
- **View Updates**:
  - `sql/analytics/15_view_monthly_headcount_snapshot.sql`: Added `LEFT JOIN fact_terminations` to exclude offboarded employees from post-termination monthly active headcount snapshots.
  - `sql/analytics/13_views.sql`: Enforced `e.is_current_row = TRUE` across analytical views to prevent historical SCD2 duplication (R13).
- **Validation SQL Suite**: Added Test Suite 5 in `sql/analytics/14_validation_queries.sql` with 7 business rule consistency queries. **ALL 7 CHECKS RETURNED 0 VIOLATIONS ON LIVE POSTGRESQL**.
- **KPI Catalog Contract**: Updated `docs/KPIs_Definition.md` removing hardcoded `4500.0` denominators, enforcing `employee_sk` joins, and adding `is_current_row = TRUE` filters.

### 🟢 End-to-End Validation & Final Metrics
- **Synthetic Dataset**:
  - `dim_employees`: 4,933 rows (4,500 total unique employees, 3,300 active current, 1,200 inactive current, 433 historical SCD2 rows).
  - `fact_terminations`: 1,200 offboarding events (100% loaded into PostgreSQL).
  - `fact_attendance_logs`: 1,513,306 rows (0 ghost attendance records).
  - `fact_sla_events`: 40 breach records.
  - `dim_date`: 6,940 rows.
- **ETL Execution**: 100% successful dry-run and full PostgreSQL database load (`python -m python.etl.pipeline --execute` completed in 328.9s with 0 errors).
- **PostgreSQL Database State**: All foreign keys, unique constraints, and business rules pass with 100% clean integrity.

### 📝 Documentation
- Updated `docs/decisions_log.md` with DEC-015 (Termination Reconciliation) and DEC-016 (Date Range & Constraint Alignment).
- Updated `CHANGELOG.md` with v0.7.0 final execution baseline.

---

## [v0.6.0] — 2026-08-11

### Added
- **Pipeline ETL & Generador Sintético:** Script de ingesta masiva en Python para poblar 4,500 colaboradores y 1.5M+ registros de asistencia.
- **Motor de Validación de Integridad:** Reglas de validación relacional, checks de unicidad y control de tipos de ausencia.
- **Infraestructura PostgreSQL:** Creación automatizada de esquemas, índices B-Tree y restricciones DDL en `people_analytics`.

---

## [v0.5.0] — 2026-08-08

### Added

#### Analytics Design, Architecture & Planning

- Created **KPIs_Definition.md** as the official KPI Catalog & Metrics Definition Contract.
  - Defined 8 KPI specifications across HR, Financial, Operational and Diagnostic categories.
  - Documented SQL (PostgreSQL) and DAX (Power BI) calculation logic for each KPI.
  - Established KPI governance framework, lifecycle states and validation workflow.
  - Added dashboard mapping matrix linking KPIs to executive dashboard screens.
- Created **03_Architecture.md** as the Technical Architecture Document for the analytics platform.
  - Defined end-to-end data flow: Source Systems → PostgreSQL Data Warehouse → Power BI.
  - Documented star schema architecture, naming conventions and indexing strategy.
  - Specified ETL pipeline design using Python (SQLAlchemy, Pandas).
  - Defined analytical SQL views and metrics layer.
  - Documented data quality validation layer, PII anonymization strategy and security design.
- Created **04_Data_Model.md** as the dimensional model specification.
  - Defined Kimball Star Schema with 4 dimension tables and 3 fact tables.
  - Documented surrogate key strategy and SCD Type 2 for salary and department history tracking.
  - Defined all table relationships, primary keys and foreign keys.
- Created **02_Roadmap.md** as the Project Roadmap & Development Plan.
  - Documented 7 development phases from Business Understanding to Portfolio Release.
  - Established release milestones aligned with CHANGELOG.md.
- Created **05_Tasks.md** as the Project Tasks & Development Backlog.
  - Defined 28 tasks across all development phases with dependencies and status tracking.
- Created **docs/decisions_log.md** as the Decision Log & Analytical Design Register.
  - Documented key decisions covering business context, data modeling and analytics stack choices.
- Created **docs/Glossary.md** as the Business & Technical Glossary.
  - Defined terminology bridging the HR domain and data analytics discipline.
- Created **docs/interview_notes.md** as the Interview Preparation & Technical Defense Guide.
  - Documented elevator pitches, technical rationale and key talking points for interviews.

### Improved

- Strengthened traceability between KPIs, Business Rules and Functional Requirements.
- Aligned architecture design with Data Dictionary specifications from v0.4.0.
- Standardized document structure across all v0.5.0 deliverables.

---

## [v0.4.0] — 2026-08-04

### Added

#### Data Contract & Specifications

- Created **data_dictionary.md** as the official Data Contract for the Workforce Dynamic Lens platform.
- Defined seven analytical entities:
  - dim_employees
  - dim_departments
  - dim_positions
  - dim_salary_benchmarks
  - fact_attendance_logs
  - fact_terminations
  - fact_sla_events
- Documented complete metadata for every entity, including:
  - Business Owner
  - Technical Owner
  - Refresh Frequency
  - Data Retention Policy
  - GDPR Classification
  - Source Systems
  - Estimated Volume
- Documented every column with:
  - Data Type
  - Business Description
  - Validation Rules
  - PII Classification
  - Business Rule Mapping
  - Functional Requirement Mapping
- Added Data Governance principles.
- Added Data Quality validation framework.
- Added Data Privacy and GDPR classification matrix.
- Added executable SQL validation examples.
- Added complete Business Rules Mapping Matrix.
- Added Source Systems Architecture & Data Lineage.
- Added ETL refresh strategy.

### Improved

- Increased traceability between business rules, functional requirements and analytical datasets.
- Standardized naming conventions across all entities.
- Improved documentation consistency with the Business Case and Business Requirements documents.

---

## [v0.3.0] — 2026-07-29

### Added

#### Business Analysis

- Created **Business_Case.md**.
- Created **business_requirements.md**.
- Defined 31 Business Questions.
- Defined 42 Functional Requirements.
- Defined 32 Business Rules.
- Built the complete Business Requirements Specification (BRS).
- Added complete traceability between Business Questions, Business Rules and Functional Requirements.

#### Executive Documentation

- Formalized financial justification for the Workforce Dynamic Lens initiative.
- Documented ROI, Payback Period and Cost of Inaction.
- Defined strategic objectives for HR, Operations and Finance.
- Added project assumptions, implementation risks and expected benefits.

### Improved

- Improved consistency between Project Charter, Company Profile and Business Case.
- Standardized documentation style across the project.
- Strengthened business-to-technical traceability.

---

## [v0.2.0] — 2026-07-20

### Added

#### Business Foundation

- Created Project_Charter.md.
- Created Company_Profile.md.
- Defined business scope.
- Identified stakeholders.
- Established project objectives.
- Defined organizational context.
- Established governance structure.

---

## [v0.1.0] — 2026-07-15

### Added

#### Project Initialization

- Repository created.
- Initial folder structure established.
- README.md created.
- Documentation strategy defined.
- Semantic Versioning adopted.
- Keep a Changelog format adopted.

---

## [Upcoming Enhancements] — Post-v1.0.0
- Integración de pipeline CI/CD con GitHub Actions para ejecución automática de pruebas unitarias (`pytest`).
- Conexión del modelo predictivo XGBoost como API REST contenerizada en Docker.