# AI Logistics Copilot

**AI evaluation work sample:** [reproducible findings, response rubric and conversational test designs](docs/ai-evaluation/README.md). The portfolio separates observed code behaviour from unexecuted model tests and discloses AI assistance.

Prototipo de portfolio de Jan Millan para analizar inventario, revisar riesgos y apoyar decisiones de reposición con Python, pandas y Streamlit. Parte de necesidades operativas reales y utiliza los datos de muestra incluidos en el repositorio.

## Qué se puede revisar

- Dashboard con valor de inventario, health score, productos críticos y estado operativo.
- Seis páginas: Risk Engine, Demand Forecast, Executive Summary, Purchase Planner, Inventory Health y PDF Report.
- Muestra de 50 productos en seis categorías, cruzada con ventas diarias.
- Cálculo de cobertura y simulación del efecto de una compra sobre stock, cobertura y valor.
- Generación del informe PDF ejecutivo en memoria, sin depender de una carpeta reports.
- Código de integración generativa opcional con Gemini; desactivado por defecto.

## Datos y métricas de la muestra

Comprobación offline del 12 de octubre de 2026: 6 productos con cobertura inferior a 7 días, 16 entre 7 y 21 días, y 28 con 21 días o más. El health score ponderado es 72/100. Estas cifras describen la muestra y las reglas del prototipo; no son resultados de un cliente ni métricas de ahorro.

La estimación de cobertura utiliza stock / ventas diarias. No es un modelo de Machine Learning ni contempla estacionalidad. El score pondera productos saludables con 100, productos en revisión con 50 y críticos con 0.

## Ejecutar localmente

Desde la carpeta raíz del proyecto, con un entorno virtual de Python activado:

```powershell
python --version
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

La aplicación abre con datos de muestra sin necesitar credenciales de IA. Las dos cargas CSV de la página principal esperan las columnas de data/inventory.csv y data/sales_history.csv. Las páginas secundarias utilizan los archivos de muestra del repositorio.

## IA y privacidad

La integración generativa requiere revisar proveedor, modelo y credenciales antes de activarla. Para una demostración sin llamadas externas, mantener GEMINI_FREE_ENABLED=false. El nombre de una opción o modelo no garantiza por sí mismo que una cuenta esté libre de facturación.

No subir datos personales, datos de clientes ni credenciales a GitHub. El prototipo no incorpora autenticación ni aislamiento entre organizaciones. No se presenta como implementación de RAG, agentes autónomos o servicio listo para producción.

## Validación realizada

- Sintaxis de los archivos Python revisados.
- Cruce uno a uno de los 50 productos de muestra.
- Cálculos de cobertura, ventas iguales a cero y score de salud.
- Coherencia del score del resumen con el dashboard.
- Exportación con ReportLab: PDF válido en memoria con los indicadores de la muestra. Los controles de Streamlit se simularon en esta prueba; falta la comprobación completa en navegador y la validación de la API generativa.

## Tecnologías

Python, pandas, Streamlit, Plotly, ReportLab y SDK de Google Gen AI.

## Autor

Jan Millan · [Perfil de GitHub](https://github.com/JanMillFar)

