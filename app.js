const state = { rows: [], columns: [], filters: {}, sourceName: "" };
const $ = (id) => document.getElementById(id);
const palette = ["#007f86", "#f5b942", "#e46c53", "#5669c8", "#779d3f", "#a85f93"];

function parseCSV(text) {
  const lines = text.replace(/^\uFEFF/, "").split(/\r?\n/).filter((line) => line.trim());
  if (lines.length < 2) throw new Error("Upload a CSV with a header row and at least one data row.");
  const readLine = (line) => { const out=[]; let value="", quoted=false; for(let i=0;i<line.length;i++){const ch=line[i]; if(ch==='"'){if(quoted&&line[i+1]==='"'){value+='"';i++;}else quoted=!quoted;}else if(ch===','&&!quoted){out.push(value.trim());value="";}else value+=ch;}out.push(value.trim());return out; };
  const headers = readLine(lines[0]).map((h, i) => h || `Column ${i + 1}`);
  return lines.slice(1).map((line) => { const values = readLine(line); return Object.fromEntries(headers.map((h, i) => [h, values[i] ?? ""])); });
}

function inferColumns(rows) {
  return Object.keys(rows[0]).map((name) => {
    const values = rows.map(r => r[name]).filter(v => v !== "");
    const numeric = values.length && values.filter(v => Number.isFinite(Number(v))).length / values.length > .88;
    const date = !numeric && values.length && values.filter(v => !Number.isNaN(Date.parse(v))).length / values.length > .88;
    const unique = new Set(values).size;
    const looksLikeIdentifier = /(^id$|_id$|\bid\b|identifier|customer.?number)/i.test(name) && unique / Math.max(values.length, 1) > .85;
    return { name, type: looksLikeIdentifier ? "identifier" : numeric ? "number" : date ? "date" : "category", unique, missing: rows.length - values.length, values };
  });
}
function num(value) { return Number(value); }
function visibleRows() { return state.rows.filter(row => Object.entries(state.filters).every(([key, filter]) => {
  if (filter.kind === "categories") return !filter.values.length || filter.values.includes(row[key]);
  if (filter.kind === "range") { const value = num(row[key]); return Number.isFinite(value) && value >= filter.min && value <= filter.max; }
  if (filter.kind === "date-range") { const value = Date.parse(row[key]); return Number.isFinite(value) && value >= filter.low && value <= filter.high; }
  return true;
})); }
function displayName(name) { return name.replace(/[_-]/g, " ").replace(/\b\w/g, l => l.toUpperCase()); }
function numberFormat(n) { return new Intl.NumberFormat().format(n); }

function profileUI() {
  const missing = state.columns.reduce((sum, col) => sum + col.missing, 0);
  $("columns-kpi").textContent = state.columns.length;
  $("missing-kpi").textContent = numberFormat(missing);
  $("numeric-kpi").textContent = state.columns.filter(c => c.type === "number").length;
  $("schema-list").innerHTML = state.columns.map(c => `<div class="schema-item"><span>${displayName(c.name)}</span><span class="schema-type">${c.type}</span></div>`).join("");
}
function buildFilters() {
  const categorical = state.columns.filter(c => c.type === "category" && c.unique > 1 && c.unique <= 16).slice(0, 3);
  const numeric = state.columns.filter(c => c.type === "number").slice(0, 2);
  const dates = state.columns.filter(c => c.type === "date").slice(0, 1);
  categorical.forEach(c => state.filters[c.name] = { kind: "categories", values: [] });
  numeric.forEach(c => { const nums = c.values.map(num).filter(Number.isFinite); state.filters[c.name] = { kind: "range", min: Math.min(...nums), max: Math.max(...nums), low: Math.min(...nums), high: Math.max(...nums) }; });
  dates.forEach(c => { const values = c.values.map(value => Date.parse(value)).filter(Number.isFinite); state.filters[c.name] = { kind: "date-range", min: Math.min(...values), max: Math.max(...values), low: Math.min(...values), high: Math.max(...values) }; });
  const toDateInput = (value) => new Date(value).toISOString().slice(0, 10);
  $("filter-controls").innerHTML = [...categorical.map(c => `<div class="filter-group"><label for="filter-${c.name}">${displayName(c.name)}</label><select id="filter-${c.name}" multiple size="${Math.min(5, c.unique)}">${[...new Set(c.values)].sort().map(v=>`<option value="${escapeHTML(v)}">${escapeHTML(v)}</option>`).join("")}</select></div>`), ...numeric.map(c => `<div class="filter-group"><span class="filter-label">${displayName(c.name)}</span><input id="filter-${c.name}" type="range" min="${state.filters[c.name].min}" max="${state.filters[c.name].max}" value="${state.filters[c.name].high}" step="any"><div class="range-labels"><span>${state.filters[c.name].low}</span><span id="value-${c.name}">${state.filters[c.name].high}</span></div></div>`), ...dates.map(c => `<div class="filter-group"><span class="filter-label">${displayName(c.name)}</span><label class="range-labels" for="filter-${c.name}"><span>From</span><span>To</span></label><input id="filter-${c.name}" type="date" min="${toDateInput(state.filters[c.name].min)}" max="${toDateInput(state.filters[c.name].max)}" value="${toDateInput(state.filters[c.name].low)}"><input id="filter-${c.name}-end" type="date" min="${toDateInput(state.filters[c.name].min)}" max="${toDateInput(state.filters[c.name].max)}" value="${toDateInput(state.filters[c.name].high)}"></div>`)].join("");
  categorical.forEach(c => $("filter-"+c.name).addEventListener("change", e => { state.filters[c.name].values=[...e.target.selectedOptions].map(o=>o.value); render(); }));
  numeric.forEach(c => $("filter-"+c.name).addEventListener("input", e => { state.filters[c.name].high=num(e.target.value); $("value-"+c.name).textContent=e.target.value; render(); }));
  dates.forEach(c => { $("filter-"+c.name).addEventListener("change", e => { state.filters[c.name].low=Date.parse(e.target.value); render(); }); $("filter-"+c.name+"-end").addEventListener("change", e => { state.filters[c.name].high=Date.parse(e.target.value); render(); }); });
}
function escapeHTML(value) { return String(value).replace(/[&<>'"]/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;","'":"&#39;",'"':"&quot;"}[char])); }
function drawCharts(rows) {
  const numbers = state.columns.filter(c=>c.type === "number");
  const categories = state.columns.filter(c=>c.type === "category" && c.unique > 1 && c.unique <= 30);
  const primaryNumber = numbers[0], secondaryNumber = numbers[1] || numbers[0], primaryCategory = categories[0];
  const empty = rows.length === 0;
  if (primaryNumber) { $("distribution-title").textContent=`Distribution of ${displayName(primaryNumber.name)}`; Plotly.react("distribution-chart", [{x:rows.map(r=>num(r[primaryNumber.name])).filter(Number.isFinite), type:"histogram", marker:{color:palette[0]}, hovertemplate:"Value: %{x}<br>Count: %{y}<extra></extra>"}], {margin:{l:44,r:14,t:10,b:43},paper_bgcolor:"white",plot_bgcolor:"white",xaxis:{title:displayName(primaryNumber.name),gridcolor:"#edf1f2"},yaxis:{title:"Rows",gridcolor:"#edf1f2"},annotations:empty?[{text:"No rows match these filters",showarrow:false}]:[]},{responsive:true,displayModeBar:false}); }
  else { Plotly.purge("distribution-chart"); $("distribution-chart").innerHTML="<p class='scope'>No numeric field available.</p>"; }
  if (primaryCategory) { const counts={}; rows.forEach(r=>{const v=r[primaryCategory.name]||"Missing";counts[v]=(counts[v]||0)+1}); const labels=Object.keys(counts).sort((a,b)=>counts[b]-counts[a]).slice(0,10); $("category-title").textContent=`${displayName(primaryCategory.name)} breakdown`; Plotly.react("category-chart",[{x:labels,y:labels.map(k=>counts[k]),type:"bar",marker:{color:labels.map((_,i)=>palette[i%palette.length])},customdata:labels,hovertemplate:"%{x}: %{y} rows<extra></extra>"}],{margin:{l:44,r:14,t:10,b:75},paper_bgcolor:"white",plot_bgcolor:"white",xaxis:{tickangle:-28},yaxis:{title:"Rows",gridcolor:"#edf1f2"},annotations:empty?[{text:"No rows match these filters",showarrow:false}]:[]},{responsive:true,displayModeBar:false}); $("category-chart").on("plotly_click", event => { const value=event.points[0].customdata; const f=state.filters[primaryCategory.name] || {kind:"categories",values:[]}; f.values=f.values.includes(value)?f.values.filter(v=>v!==value):[...f.values,value]; state.filters[primaryCategory.name]=f; const select=$("filter-"+primaryCategory.name); if(select) [...select.options].forEach(o=>o.selected=f.values.includes(o.value)); render(); }); }
  else { Plotly.purge("category-chart"); $("category-chart").innerHTML="<p class='scope'>No category field available.</p>"; }
  if (primaryNumber && secondaryNumber && primaryNumber.name !== secondaryNumber.name) { $("trend-title").textContent=`${displayName(primaryNumber.name)} and ${displayName(secondaryNumber.name)}`; Plotly.react("relationship-chart",[{x:rows.map(r=>num(r[primaryNumber.name])),y:rows.map(r=>num(r[secondaryNumber.name])),mode:"markers",type:"scatter",marker:{color:palette[0],size:8,opacity:.67},hovertemplate:`${displayName(primaryNumber.name)}: %{x}<br>${displayName(secondaryNumber.name)}: %{y}<extra></extra>`}],{margin:{l:56,r:14,t:10,b:44},paper_bgcolor:"white",plot_bgcolor:"white",xaxis:{title:displayName(primaryNumber.name),gridcolor:"#edf1f2"},yaxis:{title:displayName(secondaryNumber.name),gridcolor:"#edf1f2"},annotations:empty?[{text:"No rows match these filters",showarrow:false}]:[]},{responsive:true,displayModeBar:false}); } else { $("trend-title").textContent="Relationship"; Plotly.purge("relationship-chart"); $("relationship-chart").innerHTML="<p class='scope'>Upload a dataset with at least two numeric fields to create a relationship chart.</p>"; }
}
function renderTable(rows) { const cols=state.columns.slice(0,8).map(c=>c.name); $("data-head").innerHTML=`<tr>${cols.map(c=>`<th>${escapeHTML(displayName(c))}</th>`).join("")}</tr>`; $("data-body").innerHTML=rows.slice(0,100).map(r=>`<tr>${cols.map(c=>`<td>${escapeHTML(r[c] || "-")}</td>`).join("")}</tr>`).join(""); $("table-count").textContent=`Showing ${Math.min(100,rows.length)} of ${numberFormat(rows.length)} rows`; }
function render() { const rows=visibleRows(); $("rows-kpi").textContent=numberFormat(rows.length); const active=Object.entries(state.filters).filter(([,f])=>f.kind==="categories"?f.values.length:f.kind==="range"?f.high!==f.max:f.low!==f.min||f.high!==f.max); $("scope-text").textContent=active.length?`${numberFormat(rows.length)} rows · ${active.length} active filter${active.length>1?"s":""}`:`All ${numberFormat(rows.length)} rows`; drawCharts(rows);renderTable(rows); }
function openDataset(rows,name) { state.rows=rows;state.columns=inferColumns(rows);state.filters={};state.sourceName=name.replace(/\.csv$/i,""); $("dataset-name").textContent=state.sourceName;$("dataset-label").textContent=`${numberFormat(rows.length)} ROWS · ${state.columns.length} FIELDS`;$("welcome").classList.add("hidden");$("workspace").classList.remove("hidden");profileUI();buildFilters();render(); }
$("csv-upload").addEventListener("change", async e=>{const file=e.target.files[0];if(!file)return;try{openDataset(parseCSV(await file.text()),file.name);$("upload-error").textContent="";}catch(err){$("upload-error").textContent=err.message;}});
$("load-sample").addEventListener("click",async()=>{const response=await fetch("sample-data/customer_churn_sample.csv");openDataset(parseCSV(await response.text()),"Customer Churn Sample");});
$("new-dataset").addEventListener("click",()=>$("csv-upload").click());
$("reset-filters").addEventListener("click",()=>{Object.values(state.filters).forEach(f=>{if(f.kind==="categories")f.values=[];else { f.low=f.min; f.high=f.max; }});buildFilters();render();});
