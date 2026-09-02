# DECISION LOG & ARCHITECTURAL REGISTER
## WORKFORCE DYNAMIC LENS – PEOPLE ANALYTICS & HR FINANCIAL OPTIMIZATION PLATFORM

**Document Version:** v0.5.0  
**Target Audience:** People Analytics Leaders, BI Managers, HR Business Partners, Technical Recruiters  
**Project Author:** Emmanuel Rodríguez Mendoza  
**Project:** Workforce Dynamic Lens  
**Date:** August 2026  
**Status:** Fase 2 Completed – Analytics Design & Data Modeling Baseline Established  

---

## 1. Document Purpose

El **Decision Log & Architectural Register (`docs/decisions_log.md`)** centraliza y registra de forma cronológica todas las decisiones estratégicas, técnicas, metodológicas y de negocio adoptadas durante el diseño y desarrollo de la plataforma **Workforce Dynamic Lens**.

Este registro ofrece una vista consolidada de trazabilidad histórica. Permite a los revisores técnicos y reclutadores comprender el **porqué de cada elección**, las alternativas consideradas, el impacto en el proyecto y su alineación con el perfil de **People Analytics / BI Analyst / Data Analyst**.

---

## 2. Decision Governance Framework

Cada decisión registrada en este documento se clasifica dentro de tres dominios estratégicos:

| Dominio | Código | Descripción del Alcance |
| :--- | :--- | :--- |
| **Business & Domain** | `BUS` | Definición del problema de negocio, KPIs de RRHH, monetización en P&L. |
| **Architecture & Data** | `DAT` | Modelado dimensional (Kimball), diccionario de datos, esquema PostgreSQL. |
| **Analytics & Data Tools** | `ENG` | Scripts de Python (generador sintético, ETL, validación de calidad), SQL, Power BI & DAX. |

---

## 3. Master Decision Summary Table

| Decision ID | Date | Version | Category | Decision | Core Justification | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DEC-001** | July 2026 | v0.3.0 | BUS | Focus on HR Domain & Monetization | Diferenciación del perfil alineando datos de RRHH con impacto financiero ($540k USD en P&L). | Approved |
| **DEC-002** | July 2026 | v0.2.0 | DAT | 100% Synthetic Data Generation via Python | Garantizar privacidad (RGPD/PII) sin comprometer el realismo estadístico ni relaciones de negocio. | Approved |
| **DEC-003** | August 2026 | v0.5.0 | DAT | Adopt Kimball Star Schema Architecture | Optimizar el rendimiento OLAP y simplificar la sintaxis de medidas DAX en Power BI. | Approved |
| **DEC-004** | August 2026 | v0.5.0 | DAT | PostgreSQL 16+ as Relational DW Engine | Motor relacional robusto, open-source, con soporte nativo para ANSI SQL y RLS. | Approved |
| **DEC-005** | August 2026 | v0.4.0 | DAT | Data Dictionary & Contract Specification | Establecer `docs/data_dictionary.md` como contrato estricto de calidad antes de codificar en Python/SQL. | Approved |
| **DEC-006** | August 2026 | v0.5.0 | ENG | Python 3.11+ as Core Analytics Stack | Lenguaje estándar unificado para generación sintética, ETL, validaciones de calidad y ML. | Approved |
| **DEC-007** | August 2026 | v0.5.0 | ENG | Multivariate Risk Scoring & Retention Analytics | Modelo analítico explicable para diagnóstico de fuga de talento basado en variables de talento. | Approved |
| **DEC-008** | August 2026 | v0.5.0 | ENG | Power BI as Primary Executive BI Suite | Estándar corporativo global para dashboards interactivos, modelado dimensional y DAX. | Approved |
| **DEC-009** | August 2026 | v0.3.0 | BUS | Configurable Bradford Factor Thresholds | Evitar valores rígidos universales; adaptar alertas a políticas corporativas de ausentismo. | Approved |
| **DEC-010** | August 2026 | v0.5.0 | ENG | Separation of Architecture Docs & Code | Mantener documentación funcional limpia separada del código ejecutable (`sql/`, `python/`). | Approved |

---

## 4. Chronological Decision Registry

### DEC-001: Focus on HR Domain & Financial Monetization (P&L Impact)
* **Date:** July 2026
* **Release Milestone:** v0.3.0
* **Category:** Business & Domain (`BUS`)
* **Decision:** Centrar el portafolio exclusivamente en el dominio de *People Analytics* y monetizar el impacto de la rotación y el ausentismo en el estado de resultados (P&L) de MedTech Global Solutions.
* **Alternatives Considered:** Crear un proyecto genérico de e-commerce, ventas o análisis de churn de clientes B2C.
* **Justification:** Un proyecto de analítica generalista no destaca en procesos de selección competitivos. Demostrar cómo la pérdida de talento en áreas clave frena la productividad y pone en riesgo recursos financieros posiciona al profesional como un consultor estratégico de negocio en RR. HH., no como un simple generador de reportes.
* **Impact:** Fundamentación de `docs/Business_Case.md` ($540,000 USD en ahorros proyectados) y alineación con `docs/business_requirements.md`.

---

### DEC-002: 100% Synthetic Data Generation via Python
* **Date:** July 2026
* **Release Milestone:** v0.2.0 (Planificación) / v0.6.0 (Implementación)
* **Category:** Business & Data Privacy (`DAT`)
* **Decision:** Diseñar un motor generador sintético en Python (`python/data_generation/`) que simule la operación de 4.500 empleados, inyectando programáticamente correlaciones de negocio realistas (ej. brecha salarial → mayor rotación; horas extra → ausentismo por burnout).
* **Alternatives Considered:** Utilizar datasets públicos estáticos de Kaggle (ej. IBM HR Analytics Dataset).
* **Justification:** Los datasets de Kaggle son planos, estáticos y carecen de escala temporal transaccional. Generar datos sintéticos propios permite simular transacciones complejas (`fact_attendance_logs`, `fact_sla_events`) respetando al 100% la privacidad (RGPD / LATAM).
* **Impact:** Autonomía total para definir esquemas relacionales y validar consistencia en la capa de datos.

---

### DEC-003: Adoption of Kimball Star Schema Architecture
* **Date:** August 2026
* **Release Milestone:** v0.5.0
* **Category:** Data Modeling (`DAT`)
* **Decision:** Implementar un Esquema en Estrella (*Star Schema*) compuesto por 3 dimensiones conformadas (`dim_employees`, `dim_departments`, `dim_positions`), 1 dimensión de referencia (`dim_salary_benchmarks`) y 3 tablas de hechos (`fact_attendance_logs`, `fact_terminations`, `fact_sla_events`).
* **Alternatives Considered:** Tercera Forma Normal (3NF), Esquema Copo de Nieve (Snowflake), Data Vault 2.0.
* **Justification:** Un modelo en estrella denormalizado optimiza el rendimiento de lectura OLAP, simplifica las uniones relacionales de `1:N` y evita la sobrecarga computacional en las medidas DAX de Power BI. 3NF habría exigido JOINs complejos en tiempo de ejecución, degradando los paneles ejecutivos.
* **Impact:** Base del documento `04_Data_Model.md` (v0.5.0) y desacoplamiento entre tablas de hechos y dimensiones.

---

### DEC-004: PostgreSQL 16+ as Primary Relational Engine
* **Date:** August 2026
* **Release Milestone:** v0.5.0 (Arquitectura) / v0.6.0 (Despliegue)
* **Category:** Infrastructure & Architecture (`DAT`)
* **Decision:** Seleccionar PostgreSQL 16+ como el motor de base de datos relacional para el almacén de datos analítico.
* **Alternatives Considered:** MySQL, SQLite, DuckDB, Snowflake / BigQuery Cloud DW.
* **Justification:** PostgreSQL es el estándar de la industria para bases de datos relacionales open-source. Ofrece soporte completo para ANSI SQL, funciones de ventana (`WINDOW FUNCTIONS`), particionamiento declarativo, vistas y Seguridad a Nivel de Fila (`RLS`).
* **Impact:** Garantía de que los scripts DDL en `sql/` sean estándar y portables hacia cualquier servicio en la nube (ej. Azure Database for PostgreSQL).

---

### DEC-005: Data Dictionary & Specifications Baseline
* **Date:** August 2026
* **Release Milestone:** v0.4.0
* **Category:** Data Governance (`DAT`)
* **Decision:** Formalizar el documento `docs/data_dictionary.md` como especificación y contrato de datos previo al desarrollo del código en Python o SQL.
* **Alternatives Considered:** Documentar las columnas de la base de datos a posteriori, una vez creada la base de datos.
* **Justification:** En proyectos reales de analítica empresarial, construir bases de datos sin una especificación clara genera deuda técnica y discrepancias entre equipos. Definir propietarios de negocio, frecuencias de refresco, niveles de PII y reglas de validación desde el inicio garantiza trazabilidad auditable.
* **Impact:** Definición estricta de 7 entidades, 87 atributos y matriz de gobernanza PII que sirve como especificación para el script de Python.

---

### DEC-006: Python 3.11+ as Core Data Prep & Ingestion Stack
* **Date:** August 2026
* **Release Milestone:** v0.5.0
* **Category:** Analytics Engineering (`ENG`)
* **Decision:** Utilizar Python 3.11+ junto con `SQLAlchemy`, `Pandas` y `NumPy` para la orquestación del pipeline ETL, la generación sintética y la validación de contratos.
* **Alternatives Considered:** Herramientas de GUI como Pentaho, Talend o scripts puros en Bash/SQL.
* **Justification:** Python otorga flexibilidad total para programar lógica de negocio compleja (ej. cálculo del Factor de Bradford, reconciliación SCD2, reclasificación proxy de salidas) y facilita el control de versiones en Git.
* **Impact:** Unificación del stack de preparación de datos en la carpeta `python/`.

---

### DEC-007: Multivariate Risk Scoring & Retention Analytics
* **Date:** August 2026
* **Release Milestone:** v0.5.0 (Diseño) / v0.7.0 (Lógica Analítica)
* **Category:** People Analytics (`BUS` / `ENG`)
* **Decision:** Implementar un modelo analítico multifactorial de riesgo de rotación y retención, sintetizando el Compa-Ratio frente a mercado, la acumulación de horas extra en 30 días y la severidad de ausentismo (Factor de Bradford).
* **Alternatives Considered:** Modelos predictivos de caja negra sin interpretabilidad directa para RR. HH.
* **Justification:** En People Analytics, los líderes ejecutivos y HRBPs requieren modelos transparentes y explicables basados en evidencia cuantitativa y psicología organizacional. Un score ponderado multifactorial permite aislar con precisión qué colaboradores clave (High Performers) están en riesgo de fuga por descompensación salarial o fatiga operativa, facilitando planes de retención directos y medibles.
* **Impact:** Fundamentación de las vistas analíticas en SQL y del tablero de retención en Power BI.

---

### DEC-008: Power BI as Primary Executive BI Suite
* **Date:** August 2026
* **Release Milestone:** v0.5.0 (Diseño) / v0.8.0 (Dashboards)
* **Category:** Business Intelligence (`ENG`)
* **Decision:** Utilizar Microsoft Power BI Desktop / Service como la suite corporativa para la capa de visualización e historias con datos (*Data Storytelling*).
* **Alternatives Considered:** Tableau, Looker Studio, Dash / Streamlit en Python.
* **Justification:** Power BI domina el mercado corporativo global en departamentos de Recursos Humanos y Finanzas. Su integración con modelos en estrella, lenguaje DAX para métricas dinámicas y capacidades de simulación de escenarios (*What-If Parameters*) son fundamentales para evaluar el ROI de retención.
* **Impact:** Diseño de las tres pantallas ejecutivas (Resumen Ejecutivo, Análisis Diagnóstico de Ausentismo, Riesgo de Rotación y Retención).

---

### DEC-009: Configurable Bradford Factor Thresholds & Proxy Exit Reclassification
* **Date:** August 2026
* **Release Milestone:** v0.3.0 (BRS) & v0.5.0 (KPIs)
* **Category:** Business Logic (`BUS` / `DAT`)
* **Decision:** Definir los umbrales del Factor de Bradford como parámetros de negocio configurables e implementar una regla de reclasificación proxy para corregir motivos de salida genéricos.
* **Alternatives Considered:** Aplicar un umbral rígido universal de 150 puntos sin considerar el contexto organizacional; confiar ciegamente en las respuestas de las entrevistas de salida.
* **Justification:** Ninguna organización opera con umbrales fijos no adaptables. Asimismo, las entrevistas de salida en HRIS suelen ocultar las verdaderas razones de renuncia. Reclasificar entradas genéricas ("Desarrollo Profesional") basándose en datos duros de salario (*Compa-Ratio < 0.85*) o sobrecarga (*Horas Extra > 30h*) aporta realismo de consultoría.
* **Impact:** Mayor precisión analítica en los módulos de ausentismo y rotación voluntaria.

---

### DEC-010: Separation of Architecture Documentation and Executable SQL
* **Date:** August 2026
* **Release Milestone:** v0.5.0
* **Category:** Software Engineering (`ENG`)
* **Decision:** Separar de forma estricta la documentación técnica del modelo de datos (`04_Data_Model.md`) del código ejecutable en base de datos, organizando los scripts DDL en archivos modulares dentro de `sql/`.
* **Alternatives Considered:** Incluir cientos de líneas de código SQL DDL dentro del archivo de documentación Markdown.
* **Justification:** Mezclar documentación con código dificulta la lectura ejecutiva y complica la automatización de scripts. Tener archivos modulares (`sql/ddl_schema.sql`, etc.) refleja las mejores prácticas de organización de proyectos analíticos.
* **Impact:** Estructura de repositorio limpia y ejecutable paso a paso.

---

## 5. Decision Traceability Matrix

| Decision ID | Primary Document Impacted | Code Artifact Impacted | Target Stakeholder Benefit |
| :--- | :--- | :--- | :--- |
| **DEC-001** | `docs/Business_Case.md` | N/A | CFO / CHRO (Clear ROI Monetization) |
| **DEC-002** | `docs/Company_Profile.md` | `python/generate_synthetic_data.py` | CISO / Privacy Lead (100% GDPR Compliant) |
| **DEC-003** | `04_Data_Model.md` | `sql/ddl_schema.sql` | BI Developer (Simple DAX Joins) |
| **DEC-004** | `03_Architecture.md` | `sql/ddl_schema.sql` | Analytics Lead (ANSI SQL Standard) |
| **DEC-005** | `docs/data_dictionary.md` | `python/etl_pipeline.py` | Data Steward (Quality Auditability) |
| **DEC-006** | `03_Architecture.md` | `python/etl_pipeline.py` | Analytics Engineer (Unified Codebase) |
| **DEC-007** | `docs/KPIs_Definition.md` | `python/ml_flight_risk.py` | HRBP (Explainable Flight Risk Drivers) |
| **DEC-008** | `03_Architecture.md` | `powerbi/workforce_dynamic_lens.pbix` | C-Suite (Interactive Decision Panels) |
| **DEC-009** | `docs/business_requirements.md` | `sql/views.sql` | HR Operations (Flexible Policy Rules) |
| **DEC-010** | `04_Data_Model.md` | `sql/*.sql` | Technical Reviewer (Clean Repo Layout) |

---

### Decision: DEC-015 — Termination Reconciliation & is_active Semantics (v0.7.0)

**Date**: 2026-08-14  
**Status**: Approved  
**Context**: Audit revealed that terminated employees were never marked `is_active = FALSE` in dim_employees. The generation pipeline created terminations in fact_terminations but never reconciled employee employment state. This caused 1,200 employees to appear active despite having termination records, and generated 305,483 ghost attendance records after termination dates.

**Decision**:
1. Termination generation reordered to occur BEFORE attendance generation
2. A formal reconciliation step sets `is_active = FALSE` on the current SCD2 row of every terminated employee
3. Attendance generator receives termination dates and excludes post-termination records
4. Historical SCD2 rows retain `is_active = TRUE` (employee was employed during that period)
5. Config key `target_active_headcount` renamed to `total_employee_population` for semantic clarity
6. DatasetValidator and DryRunValidator enhanced with business rule validation gates

**Consequences**:
- Active headcount will be dynamically calculated (~3,300 with current config)
- No ghost attendance records
- All terminated employees correctly reflected as `is_active = FALSE`
- CSV export blocked if critical business rules fail

---

### Decision: DEC-016 — Date Dimension Range & Schema Constraint Alignment (v0.7.0)

**Date**: 2026-08-14  
**Status**: Approved  
**Context**: The initial date dimension (`dim_date`) covered `2020-01-01` to `2030-12-31`. However, historical employee hires start in `2012` and offboardings start in `2013`. When loading `fact_terminations`, 64 offboarding events prior to 2020 were dropped because `termination_date_sk` returned `NULL` in `date_lookup`. Additionally, PostgreSQL schema check constraints `chk_date_sk_format` (`BETWEEN 20200101 AND 20991231`) and `chk_trm_date_min` (`>= '2015-01-01'`) blocked loading full historical records.

**Decision**:
1. Expanded `dim_date` range to `2012-01-01` through `2030-12-31` (6,940 days) across data generation scripts, static CSV exporters, and ETL dimension loaders.
2. Aligned PostgreSQL check constraint `chk_date_sk_format` to `BETWEEN 20100101 AND 20991231`.
3. Aligned PostgreSQL check constraint `chk_trm_date_min` to `CHECK (termination_date >= '2010-01-01')`.
4. Standardized `attendance_id` formatting in `attendance_generator.py` to `ATT_{YYYYMMDD}{counter:06d}` (14 digits) to strictly comply with `chk_att_id_format` (`^ATT_[0-9]{12,16}$`).

**Consequences**:
- 100% of historical termination events (1,200/1,200) are loaded cleanly into PostgreSQL without record dropping.
- Full time-intelligence analytics supported from company inception (2012) through 2030.
- All PostgreSQL schema constraints pass without check violations.