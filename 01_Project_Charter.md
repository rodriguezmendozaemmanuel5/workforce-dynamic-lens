# Project Charter

## Project Information

| Item | Description |
|------|-------------|
| Project Name | Workforce Dynamic Lens |
| Version | 0.2.0 |
| Date | 07-20-2026 |
| Project Lead | Emmanuel Rodríguez Mendoza |
| Professional Role | People Analytics / HR Data Analyst |
| Business Area | Human Resources / People Analytics |
| Industry | Health Technology (MedTech) |
| Company | MedTech Global Solutions |
| Project Type | People Analytics & HR Data Analytics Solution |

---

# 1. Executive Summary

## Background

MedTech Global Solutions, una empresa multinacional especializada en dispositivos médicos y servicios de telemedicina B2B con 4.500 colaboradores, ha identificado un incremento sostenido en la rotación voluntaria (*turnover*) y el ausentismo laboral dentro de áreas estratégicas de la organización (I+D y Soporte Clínico).

Aunque la empresa dispone de múltiples fuentes de información relacionadas con Recursos Humanos (HRIS, marcajes de asistencia, bandas salariales), actualmente no existe un modelo analítico centralizado que permita transformar estos datos en indicadores confiables y accionables para apoyar la toma de decisiones.

Como consecuencia, la dirección ejecutiva carece de visibilidad sobre el impacto financiero de la pérdida de talento en el estado de resultados (P&L) y no cuenta con herramientas analíticas para identificar factores de riesgo de salida y optimizar la retención de colaboradores clave.

---

## Business Need

La organización necesita una solución analítica que permita:

- Centralizar, preparar y validar información de RR. HH.
- Medir y estandarizar indicadores estratégicos de People Analytics.
- Cuantificar el costo económico del ausentismo y la rotación voluntaria.
- Evaluar la competitividad salarial (*Compa-Ratio*) y su impacto en la retención.
- Identificar perfiles y patrones de riesgo de salida de talento crítico.
- Apoyar decisiones estratégicas mediante dashboards interactivos en Power BI.

---

# 2. Problem Statement

Actualmente la empresa enfrenta:

- Incremento del ausentismo no programado y sobrecarga de horas extra.
- Aumento de la rotación voluntaria en roles de alta especialización.
- Pérdida de talento crítico (*High Performers*).
- Ausencia de métricas consolidadas y catálogos estandarizados de KPIs.
- Dificultad para estimar el impacto financiero integral de vacantes y penalizaciones de SLA.
- Falta de análisis diagnóstico y visualización ejecutiva para fundamentar planes de retención.

Si la situación continúa, la organización proyecta una reducción aproximada del 12% en la velocidad de entrega de proyectos estratégicos y un incremento significativo de costos asociados a contratación, liquidaciones y penalizaciones contractuales.

---

# 3. Business Objectives

El proyecto busca:

- Construir un modelo analítico dimensional en PostgreSQL optimizado para People Analytics.
- Identificar factores y patrones asociados a la rotación voluntaria y al ausentismo.
- Cuantificar el impacto financiero total de la pérdida de talento y la falta de capacidad operativa.
- Analizar la equidad y competitividad salarial mediante *Compa-Ratio*.
- Modelar indicadores multifactoriales de riesgo de fuga (*Flight Risk*).
- Desarrollar dashboards ejecutivos interactivos en Power BI con simulador financiero *What-If*.
- Facilitar la toma de decisiones estratégicas basadas en evidencia y datos duros de RR. HH.

---

# 4. Scope

## Included

- Generación y validación de datos sintéticos con distribuciones realistas de RR. HH.
- Base de datos relacional y modelo dimensional en estrella en PostgreSQL 16+.
- Limpieza, estandarización y pipeline ETL en Python (Pandas, SQLAlchemy).
- Análisis exploratorio de datos (EDA) y diagnóstico multivariado de factores de talento.
- Consultas analíticas, vistas y agregaciones en SQL.
- Modelado semántico, medidas DAX avanzadas y suite de dashboards en Power BI.
- Documentación técnica, de requerimientos y catálogo de KPIs.
- Presentación ejecutiva y reporte de hallazgos para Alta Dirección.

## Excluded

- Integración directa con APIs de producción de sistemas HRIS comerciales.
- Despliegue en infraestructura cloud de pago empresarial.
- Módulos transaccionales de nómina en tiempo real.
- Datos reales de empleados (preservación total de privacidad).

---

# 5. Stakeholders

| Stakeholder | Rol | Interés |
|-------------|------|----------|
| CHRO | Sponsor Ejecutivo | Alto |
| CFO | Sponsor Financiero | Alto |
| VP Operations | Sponsor Operativo | Alto |
| HR Business Partners (HRBPs) | Usuario principal | Alto |
| People Analytics / Data Analytics Team | Desarrollo y Análisis | Alto |
| IT & Data Governance | Soporte técnico | Medio |

---

# 6. Success Criteria

El proyecto será considerado exitoso si:

- Se identifican con claridad los principales factores y departamentos asociados a la rotación.
- Se cuantifica con rigor el impacto financiero (costos directos de rotación y costos de vacancia).
- Se construye un modelo dimensional en estrella eficiente en PostgreSQL.
- Se implementan dashboards ejecutivos en Power BI con interactividad y medidas DAX dinámicas.
- La documentación analítica, el diccionario de datos y el catálogo de KPIs son completos y trazables.
- El proyecto demuestra competencias sólidas de People Analytics y Data Analytics defendibles en entrevistas técnicas.

---

# 7. Risks

| Riesgo | Impacto | Mitigación |
|---------|----------|------------|
| Dataset poco representativo | Alto | Generación sintética en Python basada en evidencia de RR. HH. y psicología organizacional |
| Inconsistencia en métricas de RR. HH. | Alto | Catálogo estandarizado de KPIs y Data Contract con reglas de validación |
| Fórmulas DAX o consultas SQL lentas | Medio | Modelo en estrella denormalizado con índices optimizados en PostgreSQL |
| Dificultad de adopción ejecutiva | Medio | Diseño de dashboards orientados a decisiones con storytelling financiero |

---

# 8. Deliverables

- Dataset sintético estructurado y validado.
- Scripts SQL de esquema, restricciones, índices y vistas analíticas.
- Scripts de preparación y pipeline ETL en Python.
- Notebooks de análisis exploratorio (EDA) de rotación y ausentismo.
- Archivo Power BI (`.pbix`) con suite de tableros ejecutivos y simulador What-If.
- Reporte ejecutivo de insights y presentación para directivos.
- Documentación técnica y funcional completa en Markdown.
- Repositorio GitHub con estándar profesional.

---

# 9. Assumptions

Se asume que:

- Los datos sintéticos representan adecuadamente los comportamientos y dinámicas organizacionales.
- Los parámetros financieros (costo de vacancia 1.5x, penalizaciones de SLA) son aproximaciones válidas sustentadas en la literatura.
- Las variables seleccionadas reflejan dimensiones reales de compensación, desempeño y ciclo laboral.

---

# 10. Constraints

- Proyecto de portafolio profesional e investigación aplicada.
- Datos simulados para garantizar cumplimiento de normativas de privacidad (RGPD / LATAM).
- Entorno de ejecución local reproducible.

---

# 11. Expected Business Value

La solución permitirá:

- Reducir la incertidumbre en la toma de decisiones de talento humano.
- Priorizar acciones e intervenciones de retención en talento crítico.
- Visibilizar y cuantificar pérdidas económicas por rotación y ausentismo en el P&L.
- Evaluar escenarios presupuestarios de nivelación salarial mediante simulación interactiva.
- Evidenciar el valor estratégico de People Analytics como socio de negocio.