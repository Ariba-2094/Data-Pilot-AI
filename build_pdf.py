from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from pathlib import Path


OUT=Path('outputs/DataPilot_AI_Project_and_Architecture.pdf')
W,H=595.28,841.89
navy=HexColor('#102C42'); teal=HexColor('#007F86'); ink=HexColor('#263D4D'); muted=HexColor('#5D7280'); pale=HexColor('#EDF5F7')
c=canvas.Canvas(str(OUT),pagesize=(W,H))
c.setTitle('DataPilot AI | Project Blueprint & System Architecture')
c.setAuthor('DataPilot AI Project Documentation')
styles={
 'body':ParagraphStyle('body',fontName='Helvetica',fontSize=10.3,leading=15.1,textColor=ink,spaceAfter=8),
 'small':ParagraphStyle('small',fontName='Helvetica',fontSize=8.5,leading=12,textColor=muted),
 'heading':ParagraphStyle('heading',fontName='Helvetica-Bold',fontSize=14,leading=18,textColor=navy),
 'box':ParagraphStyle('box',fontName='Helvetica',fontSize=9,leading=12,textColor=ink),
}
page=0; y=0
def para(text,style='body',x=44,width=507):
 global y
 p=Paragraph(text,styles[style]); _,h=p.wrap(width,700); p.drawOn(c,x,y-h); y-=h+9
 if y<53: raise RuntimeError(f'Overflow page {page}: {y}')
def section(title,text):
 global y
 y-=7; para(title,'heading'); para(text)
def bullet(title,text): para('<b>'+title+'</b> '+text)
def start(kicker,title,sub):
 global page,y
 if page:c.showPage()
 page+=1
 c.setFillColor(teal);c.rect(0,H-9,W,9,fill=1,stroke=0)
 c.setFont('Helvetica-Bold',9);c.drawString(44, H-43,'DATAPILOT AI  /  '+kicker.upper())
 c.setFillColor(navy);c.setFont('Helvetica-Bold',25);c.drawString(44,H-82,title)
 y=H-102;para(sub,'small');y-=13
 c.setStrokeColor(HexColor('#D7E3E8'));c.line(44,41,W-44,41)
 c.setFillColor(muted);c.setFont('Helvetica',8);c.drawString(44,27,'PROJECT BLUEPRINT  |  Proposed design  |  September 2026');c.drawRightString(W-44,27,f'{page:02d}')
def note(text):
 global y
 p=Paragraph(text,styles['box']);_,h=p.wrap(481,700)
 c.setFillColor(pale);c.roundRect(44,y-h-23,507,h+23,6,fill=1,stroke=0)
 p.drawOn(c,57,y-h-11);y-=h+37
def table(rows,widths):
 global y
 for i,row in enumerate(rows):
  ps=[Paragraph(t,styles['box']) for t in row]
  hs=[p.wrap(w-18,600)[1] for p,w in zip(ps,widths)];rh=max(hs)+18
  c.setFillColor(pale if i%2==0 else HexColor('#F8FAFB'));c.rect(44,y-rh,sum(widths),rh,fill=1,stroke=0)
  x=44
  for p,w,h in zip(ps,widths,hs):p.drawOn(c,x+9,y-9-h);x+=w
  y-=rh
 y-=12

start('Concept & scope','From dataset to decisions','A complete AI Data Analyst platform with automatically generated interactive dashboards.')
para('DataPilot AI lets a user upload a tabular dataset, understand its quality, explore patterns, train predictive models, explain predictions, and ask questions in natural language - inside one analysis workspace.')
note('<b>Core promise</b><br/>Upload CSV or Excel &gt; inspect and validate &gt; generate a filterable dashboard &gt; explore evidence &gt; optionally train and explain models &gt; export reproducible results.')
section('The problem it solves','Analysts often move between spreadsheets, notebooks, visualization tools, and model scripts. This fragments the analysis and makes results hard to reproduce. DataPilot AI connects these steps around a versioned dataset and a shared analysis context.')
section('Project objectives','Reduce the effort needed to start an analysis; make data quality visible before decisions; generate useful charts from column types; support hands-on exploration; compare reliable classification and regression baselines; and explain conclusions with traceable evidence.')
section('Who it serves','Students and analysts can investigate new datasets quickly. Business users can explore segments through filters and plain-language questions. Interviewers can inspect a complete product spanning data science, ML, GenAI, backend engineering, and deployment.')
section('Scope and honest positioning','The initial release handles one tabular dataset per workspace. Modeling is optional and requires a suitable target. Multi-table joins, forecasting, streaming, and autonomous business decisions are later extensions. This document describes a proposed implementation, not completed features or measured performance.')
table([['<b>Explore</b>','<b>Predict</b>','<b>Explain</b>'],['Quality, statistics, linked charts and filters','Classification, regression and validated model comparison','Feature attribution, grounded insights and ask-your-data']],[169,169,169])

start('User journey','End-to-end workflow','Each stage produces an inspectable artifact; users can explore without training a model.')
for title,text in [
('01  Upload and validate','Accept CSV/XLSX, select the Excel sheet, check file size and format, and inspect parsing errors. Assign an owner and dataset ID; retain the original file.'),
('02  Detect and confirm schema','Infer numerical, categorical, datetime, boolean, text and identifier roles. Let users correct ambiguous dates, numeric category codes, units and target semantics.'),
('03  Profile and prepare','Compute missingness, duplicates, distributions and suspicious values. Preview proposed cleaning changes and save an approved, versioned transformation recipe.'),
('04  Generate the dashboard','Use schema, cardinality and profiling results to choose KPIs, compatible charts and filters. Save a declarative dashboard specification users can customize.'),
('05  Explore and ask questions','Apply shared filters, click chart marks, inspect descriptive statistics, and ask questions. Display the active scope and contributing row count with every answer.'),
('06  Train and evaluate (optional)','Choose a target and task, confirm a data split, compare baselines and candidate models with cross-validation, then evaluate the selected pipeline on a held-out test set.'),
('07  Explain and predict','Inspect global feature importance and local explanations. Submit new rows through the same fitted preprocessing pipeline and show validation errors clearly.'),
('08  Save and export','Save dashboard layout and filter state. Export filtered data, charts, analysis reports and a model card containing dataset, recipe, split and model versions.')]:bullet(title,text)
note('<b>Example journey:</b> A churn dataset yields region and contract filters, tenure ranges and a churn KPI. Selecting a region updates the cohort. Training a churn model is a separate, explicit experiment tied to a recorded dataset version.')

start('Architecture','System architecture','A modular application with a separate worker process keeps long-running analysis off the web request path.')
def box(x,top,w,h,title,body):
 c.setFillColor(pale);c.setStrokeColor(HexColor('#B4D1D7'));c.roundRect(x,top-h,w,h,6,fill=1,stroke=1)
 p=Paragraph('<b>'+title+'</b><br/>'+body,styles['box']);_,ph=p.wrap(w-18,h);p.drawOn(c,x+9,top-10-ph)
def arrow(x1,y1,x2,y2):
 c.setStrokeColor(teal);c.setLineWidth(1.3);c.line(x1,y1,x2,y2)
 import math
 a=math.atan2(y2-y1,x2-x1)
 for d in [-.5,.5]:c.line(x2,y2,x2-6*math.cos(a+d),y2-6*math.sin(a+d))
box(44,684,507,58,'Browser | React + TypeScript + Plotly','Upload • generated dashboard • shared filter state • experiments • chat')
arrow(297,626,297,601)
box(44,601,507,61,'API | FastAPI','Authentication + ownership checks • dataset and dashboard APIs • query validation • job status')
arrow(120,540,120,514);arrow(297,540,297,514);arrow(473,540,473,514)
box(44,514,153,81,'Analytics service','Schema + quality + EDA<br/>Dashboard specifications<br/>DuckDB aggregate queries')
box(221,514,153,81,'Job queue + workers','Redis + Celery<br/>Preparation + ML + SHAP<br/>Reports and artifacts')
box(398,514,153,81,'AI gateway','Question &gt; query plan<br/>Evidence &gt; narrative<br/>External LLM API')
arrow(120,433,120,399);arrow(280,433,260,399);arrow(315,433,390,399)
box(44,399,242,83,'PostgreSQL | application state','Users + dataset metadata + recipes<br/>Dashboard specs + saved filters<br/>Job state + experiment metrics')
box(309,399,242,83,'Object storage | versioned artifacts','Original files + curated Parquet<br/>Fitted pipelines + explanations<br/>Reports + filtered exports')
y=289
para('<b>Flow:</b> the browser sends authenticated requests. The API runs bounded queries or queues expensive jobs. Workers read the relevant dataset version, write results to storage, and update job state. The browser retrieves results through the API.','body')
para('<b>Diagram convention:</b> arrows indicate the main request and persistence direction. Services may use both stores through authorized access. The AI gateway receives schema and scoped evidence through the API; it has no direct database credentials.','small')
section('Design boundaries','Keep modules in one backend codebase initially, with API and workers deployed as separate processes. Store tenant ownership on every resource. Use dataset version + filter hash + chart specification as the aggregate-cache key so stale or cross-user results cannot leak.')

start('Dashboard generation','Generate charts from the data','The output is a configurable dashboard specification, not a fixed page built for one sample CSV.')
section('A deterministic generation engine','Profile column roles, missingness, unique counts and valid ranges. Apply compatibility rules, rank useful chart candidates, suppress identifiers and near-unique categories, and build a compact default layout. Let users override chart type, axes, group-by and aggregation. An LLM may suggest titles, but validated rules decide what can execute.')
table([['<b>Detected structure</b>','<b>Default visualization</b>','<b>Guardrail</b>'],['Numeric feature','Histogram and box plot','Show binning and units; flag skew'],['Categorical feature','Count or percentage bars','Top-N + Other; searchable filter'],['Date + numeric metric','Trend with time grouping','Distinguish totals from averages'],['Two numeric features','Scatter plot; optional trend','Sample large plots and label it'],['Numeric feature set','Correlation heatmap','Exclude IDs; show pairwise counts'],['Confirmed target','Class balance or target distribution','Do not infer meaning from type alone']],[133,184,190])
section('What the specification stores','Each chart records a stable ID, chart type, dataset version, fields, aggregation, sort, limit, filter bindings and layout. The server validates fields and aggregations against the schema. Store the target choice, display labels and units alongside the specification.')
section('Dashboard sections','Overview KPIs; Data Quality; Exploratory Analysis; Target Analysis; ML Evaluation; Explainability; and AI Insights. Hide ML panels until an experiment exists. Label model metrics with their evaluation split and version so they are not confused with live exploration KPIs.')
note('<b>Keep it usable:</b> start with a small set of useful charts, provide an Add chart action, virtualize long tables, and show empty states when a dataset lacks compatible fields. A table containing only IDs should not produce misleading analytics.')

start('Interactions','Filters and cross-filtering','One explicit filter state drives charts, KPI cards, tables, exports and scoped AI answers.')
table([['<b>Control</b>','<b>Behavior</b>'],['Categorical selectors','Searchable dropdowns and multi-select; explicit missing-value option'],['Numeric and date ranges','Range slider plus editable bounds; date range with declared timezone'],['Chart configuration','X/Y fields, group-by, aggregation, chart type and target selector'],['Chart interactions','Click category or select points/range; hover details, zoom, pan, legend toggles'],['Scope controls','Visible filter chips, selected-row count, remove-one and Reset all']],[153,354])
section('The cross-filtering contract','A chart click becomes a predicate such as region IN [South]. The browser merges it into shared state, sends a revisioned aggregate request, and redraws all bound charts and KPIs from the same result scope. Use OR within a field and AND across fields. Stable row IDs support point selections; numeric selections use explicit intervals.')
section('Avoid confusing behavior','Clicking the same selected category toggles it off. Reset clears filters and selections. Zoom and legend visibility remain visual changes unless explicitly offered as filters. Choose and document whether a source chart retains context; for the first release, all charts show the filtered cohort and selected chips remain visible.')
note('<b>Illustrative interaction:</b> Region = South AND Contract = Monthly AND Tenure between 0 and 12 months. The churn KPI becomes churned customers / customers with a known churn label in that cohort. Revenue and tenure plots, the data table, and filtered CSV use those same predicates. No example result is claimed here.')
section('Consistency and performance','Debounce rapid control changes, cancel obsolete requests, and discard responses with an old filter revision. Execute aggregates server-side, return binned data, and paginate rows. Show whether results are exact or sampled. Preserve filter state in saved views; return a clear zero-row state instead of stale charts.')
para('<b>Model distinction:</b> exploratory filtering does not retrain models. A user can evaluate a frozen model on a labeled cohort or explicitly create a new training experiment; both actions must record their scope.','small')

start('Analysis engine','Data quality, EDA and statistics','Preserve raw data, expose assumptions and make every transformation reproducible.')
section('Data quality before cleaning','Report shape, types, missing values by column, exact duplicates, parsing failures, constant fields, invalid domain values and likely identifiers. Use IQR-based or domain-specific rules to flag possible outliers; do not automatically delete unusual but valid observations. If a health score is included, publish its formula and show the component checks.')
section('A versioned preparation recipe','Offer type conversion, whitespace/category normalization, duplicate handling and missing-value policies with an affected-row preview. Retain source lineage and allow a new dataset version to be created. Distinguish deterministic corrections from learned transformations: imputation statistics, scaling and encodings used by ML are fitted only within training folds.')
section('Exploratory analysis','Display counts, means, medians, standard deviations, quantiles and missingness with denominators. Compare segments using consistent bins and units. Show distributions, category frequencies, trends, pairwise plots and correlations. Flag unequal group sizes, high cardinality and possible target leakage rather than silently hiding them.')
table([['<b>Question</b>','<b>Candidate method and interpretation</b>'],['How strongly do numeric values move together?','Pearson for linear relationships; Spearman for monotonic rank relationships. Neither establishes causation.'],['Do groups differ on a numeric outcome?','Welch t-test for two independent groups when appropriate; use robust/nonparametric alternatives after checking assumptions.'],['Are two categories associated?','Chi-square when expected counts support it; use an appropriate exact method for sparse small tables.'],['How uncertain is an estimate?','Confidence intervals with a suitable sampling method; effect sizes and sample counts alongside p-values.']],[193,314])
para('Treat automatically proposed tests as exploratory. Check independence, missingness and sampling assumptions, address multiple comparisons, and avoid presenting statistical significance as practical importance. Time-dependent data requires a suitable analysis design.','small')

start('Machine learning','Classification and regression','The user confirms the target and task; numeric labels can still represent classes.')
section('Build an experiment, not just a model','Record dataset/recipe versions, target, excluded identifiers, feature set, task, random seed, split policy, metric and resource budget. Reject missing targets for supervised fitting and report excluded rows. Review fields that would not be available at prediction time.')
section('Split before learning from the data','Reserve a held-out test set before fitting any learned preprocessing. Use stratification for suitable classification data, group splits for repeated entities, and chronological splits for time-dependent observations. Fit imputation, encoding, scaling and optional feature selection inside each cross-validation training fold [1].')
table([['<b>Stage</b>','<b>Classification</b>','<b>Regression</b>'],['Baseline','Majority/stratified dummy classifier','Mean/median dummy regressor'],['Candidates','Logistic regression, random forest, gradient boosting','Ridge regression, random forest, gradient boosting'],['Primary metric','Choose macro-F1, recall or PR-AUC based on the task','Choose MAE or RMSE based on error cost'],['Diagnostics','Confusion matrix; precision/recall; ROC and PR curves where valid','Residual plots; error distribution; MAE, RMSE and R-squared'],['Selection','Cross-validation metric and variability, training cost and interpretability','Same policy; compare against the baseline']],[93,207,207])
section('Selection and final evaluation','Tune a limited search space on training data only. Handle class weighting or resampling inside training folds. Select thresholds on validation data, then evaluate the frozen selection once on the test set. Present cross-validation variability separately from final test performance; do not promise that every dataset supports useful prediction.')
section('Serve the complete fitted pipeline','Persist preprocessing and estimator together with the expected schema and model card. Validate new inputs, handle unseen categories deliberately and report drift indicators. Never load user-supplied serialized model objects. Dashboard cohort metrics must retain model and evaluation-version labels.')

start('Explainability & narrative','Explain results with evidence','Keep model behavior, statistical association and causal claims clearly separated.')
section('Global and local explanations','Use held-out permutation importance to assess predictive dependence, with caution for correlated features. Add SHAP summary and individual prediction views using an explainer appropriate to the fitted model [4]. Retain the background-data choice, feature mapping and output scale; explain whether contributions refer to a score, log-odds or prediction value.')
section('What the user sees','A global view ranks influential features across a named evaluation sample. A local view shows the baseline output and contributions for one prediction. One-hot features can be grouped for readability with documented aggregation. Label sampled explanations and keep expensive explanation jobs bounded and asynchronous.')
note('<b>Interpretation:</b> a feature increasing a model score describes that model on the chosen reference context. It does not prove that changing the feature will change the real-world outcome. Correlated features can share or redistribute attribution.')
section('Grounded AI insights','Compute structured evidence first: metric ID, value, denominator, unit, cohort, dataset version and relevant comparison. Send this compact evidence to the language model with a request to explain only supported observations. Attach each narrative statement to the calculation or chart that supports it.')
section('A reliable insight pipeline','Aggregate &gt; detect candidate findings &gt; check minimum sample sizes and missingness &gt; generate a concise explanation &gt; validate numerical references &gt; display evidence links. Cache by dataset version and filter state. Invalidate insight text when filters change, and offer a deterministic summary if generation fails.')
section('Examples of useful insights','Highlight concentrated missingness, unusual group distributions, a trend within a declared period, or a model outperforming its baseline on a named metric. Say that an observation needs investigation when confounding, small samples or weak evidence limit the conclusion. Never invent a business explanation for a correlation.')

start('Natural-language analysis','Ask your data','A question becomes a validated analytical operation with a visible scope and reproducible answer.')
note('<b>Example question:</b> "What is the average monthly charge by contract type for the selected region?"<br/>Show the region filter, average definition, valid-value count, resulting table/chart and query details with the answer.')
for title,text in [
('1. Resolve context','Read the authorized dataset version, confirmed schema, metric definitions and current dashboard filters. Ask a clarification when "best", "revenue" or a time period is ambiguous.'),
('2. Plan the operation','Have the LLM emit a typed query plan: fields, aggregation, grouping, ordering and additional predicates. Prefer a bounded semantic plan that the server compiles to SQL.'),
('3. Validate and constrain','Allow only known fields and approved aggregate operations. Apply ownership checks independently of the model; parameterize values and allowlist identifiers. Reject joins and unsupported operations in the first release.'),
('4. Execute safely','Run an authorized read-only analytical query in an isolated DuckDB environment [3]. Disable external file/network access and extension loading for the query path; enforce time, memory and result-size limits. A SELECT-only check alone is insufficient.'),
('5. Explain the evidence','Return the calculated values, supporting chart/table, sample size, missing-value handling and filters. The LLM summarizes this result and cannot manufacture missing calculations.'),
('6. Continue or save','A follow-up such as "only monthly contracts" extends the declared context. Save an answer as a dashboard chart only after specification validation. Log query metadata and redact sensitive values.')]:bullet(title,text)
para('<b>Trust boundary:</b> uploaded cells and column names are data, never instructions. Do not execute generated Python or arbitrary SQL. Send only necessary schema and aggregates to the LLM; exclude sensitive raw rows by default. If the provider is unavailable, dashboards and deterministic analytics should continue to work.','small')

start('Implementation & deployment','A practical deployment stack','Suggested engineering choices for this design; pin and test compatible dependency versions during implementation.')
table([['<b>Layer</b>','<b>Choice</b>','<b>Responsibility</b>'],['Interface','React + TypeScript + Plotly','Reusable chart renderer, filter store, event-driven interactions [2]'],['API','FastAPI + validation models','Auth, resource ownership, bounded query and job APIs'],['Analytics','pandas + DuckDB + Parquet','File preparation, profiling and aggregate queries'],['ML / XAI','scikit-learn + SHAP','Fitted pipelines, evaluation and explanations'],['Background work','Celery + Redis','Analysis/training queue, retries and resource isolation'],['Persistence','PostgreSQL + S3-compatible storage','Application metadata plus files and model artifacts'],['AI integration','Provider-neutral LLM adapter','Validated question plans and grounded narrative'],['Delivery','Docker + CI + HTTPS ingress','Reproducible builds, tests, deployment and health checks']],[87,171,249])
section('Deploy a complete first release','Use a static frontend host or reverse proxy, an API container, a worker container, managed PostgreSQL and Redis, and private object storage. Keep compute and storage in compatible regions. Maintain staging and production settings; inject secrets at runtime and use short-lived signed links for authorized file downloads.')
section('Request and job lifecycle','An upload creates a dataset record; a profiling request returns a job ID. The UI polls job status or receives server-sent events. Use queued/running/succeeded/failed/cancelled states, bounded retries and idempotency keys. Write artifacts atomically before publishing successful job completion.')
section('Operations and cost control','Set upload, row, training-time and LLM-token budgets. Monitor job duration, queue depth, query latency, errors and provider usage without logging sensitive rows. Back up metadata, apply artifact retention policies, and support deletion across raw files, derived versions and caches. Scale workers separately only when measurements justify it.')

start('Delivery & verification','Build plan and acceptance criteria','Deliver the complete vertical workflow in stages, with measurable checks at each milestone.')
table([['<b>Milestone</b>','<b>Deliverable and exit criterion</b>'],['1. Data foundation','Authenticated upload, schema confirmation, immutable original and quality report. Malformed files return actionable errors.'],['2. Interactive analytics','Generated dashboard, categorical/numeric/date filters, cross-filtering and export. Charts and KPIs agree with reference queries.'],['3. Predictive analysis','Classification and regression pipelines, baseline comparison and saved experiments. Verify preprocessing fits only training folds.'],['4. Explanations and AI','Local/global explanations, evidence-linked insights and bounded ask-your-data. Unsupported questions fail clearly.'],['5. Deployment and polish','Deployed demo, CI, error states, quotas, docs and model cards. Validate ownership isolation and recovery from worker/provider failures.']],[116,391])
section('Meaningful tests','Use fixtures with missing labels, rare categories, dates, duplicate records and zero-row filter results. Test filter combination semantics, chart-to-filter mapping, stale-response handling and equality of exported row counts. Check that a user cannot read another user\'s dataset, artifacts, jobs or cached results.')
section('Evaluate the AI component','Create a fixed question set with expected plans and numerical answers. Measure valid-plan rate, numerical correctness, scope adherence, clarification quality and refusal of unsupported operations. Include misleading column names and instruction-like cell values to test the trust boundary.')
section('Measure performance honestly','Benchmark a declared dataset size, column mix and deployment configuration. Record upload-to-dashboard time, p50/p95 filter-query latency, training duration and cost per AI answer. Set targets after initial measurement, then publish observed numbers with their conditions; no speed or accuracy claim is assumed in this blueprint.')
note('<b>Definition of done:</b> a new dataset can be uploaded, explored with synchronized filters, queried in plain language, used in an appropriate validated ML experiment, explained, and exported from the deployed application with traceable versions and clear failure states.')

styles['body'].fontSize=9.5
styles['body'].leading=13
start('Interview & resume','Present the project confidently','Explain the engineering decisions and demonstrate evidence rather than listing libraries.')
section('A concise project pitch','"DataPilot AI is a tabular analysis platform that generates interactive dashboards from uploaded datasets. Users explore linked charts and filters, train classification or regression pipelines, inspect model explanations, and ask data questions. Its key design is a shared, versioned analysis context that keeps charts, exports and AI answers consistent."')
section('A five-minute demonstration','Upload a dataset and explain one quality issue. Show that the dashboard is generated from schema. Apply two filters and click a chart to update KPIs and exports. Ask a question about the filtered cohort and inspect its evidence. Finally, compare a model with its baseline and explain one prediction using the saved experiment.')
section('Questions worth preparing for','<b>Why not let the LLM compute everything?</b> Deterministic calculations are testable; the LLM interprets validated evidence.<br/><b>How is leakage prevented?</b> Split first and fit learned preprocessing within training folds.<br/><b>How does cross-filtering work?</b> Chart events update a central predicate state; the server recomputes scoped aggregates.<br/><b>Why separate workers?</b> Training and reports should not block ordinary exploration.<br/><b>What are the limits?</b> Dataset semantics, small samples, causal ambiguity and unmeasured production scale remain explicit.')
section('Resume bullet templates - use after implementation','• Built a dataset-driven analytics platform with generated dashboards, synchronized filters and reproducible exports.<br/>• Implemented classification/regression pipelines with training-only preprocessing, baseline comparison and held-out evaluation.<br/>• Added evidence-grounded natural-language analysis and model explanations; measured [verified metric] on [declared benchmark].')
para('Replace placeholders with verified results and describe only features actually delivered. Keep a README, architecture diagram, deployed demo, evaluation report and one reproducible sample workflow as supporting evidence.','small')

section('Technical references','Official documentation used to ground key implementation choices. The architecture and build plan are proposed design decisions.')
for txt,url in [('[1] scikit-learn: common pitfalls and data leakage','https://scikit-learn.org/1.8/common_pitfalls.html'),('[2] Plotly: JavaScript chart events','https://plotly.com/javascript/plotlyjs-events/'),('[3] DuckDB: SELECT statement','https://duckdb.org/docs/current/sql/statements/select'),('[4] SHAP: API and explainer reference','https://shap.readthedocs.io/en/stable/api.html')]:para(f'<link href="{url}" color="#007F86">{txt}</link>','small')
c.save()
print(f'Created {page} pages: {OUT}')




