from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

documentation = """
ChronicCareIQ Dashboard — Technical Documentation

1. Project Overview
The ChronicCareIQ dashboard consolidates multiple healthcare data tables into a unified dataframe and provides four analytic modules aligned with project documentation:
- 2.1 Engagement Metrics
- 2.2 Care Access Latency
- 2.3 Clinician Workload
- 2.4 Care Outreach Patterns

2. Data Pipeline
Unified Query: Joins call_record, call_entry, patient_answer, and patient.
Key Columns: PatientId, CallRecordId, CallStart, PickupTime, LatencySec, Score, Alert, DaysWithMeasurements, DestinationPhone.
Output: df_unified → single source of truth for all modules.

3. Module Summary Table
Module | Inputs | Outputs | Visualizations
---------------------------------------------------------------
2.1 Engagement Metrics | CallRecordId, Score, DaysWithMeasurements | TotalCalls, AnsweredCalls, CallSuccessRate, EngagementScore, ClusterLabel | Scatter plot, Pie chart, Weekly trend line
2.2 Care Access Latency | CallStart, PickupTime, DestinationPhone | LatencySec, AlertType, Clinician summary (AvgLatencySec, breaches) | Histogram, Bar chart per clinician, Weekly trend line
2.3 Clinician Workload | CallDuration, DestinationPhone | TotalCalls, TotalDuration, AvgCallDuration, PredictedDuration | Bar chart, Scatter plot with regression, Weekly workload trend
2.4 Care Outreach Patterns | CallStart, Direction, CallDuration | AvgDuration, CallVolume by hour/direction, Weekly call volume | Heatmap, Bar chart, Weekly trend line

4. Unified Data View
Displays raw joined dataframe.
Provides summary statistics, latency distribution, and engagement scatter plots.

5. Improvements
- Refactored fragmented scripts → unified dataframe.
- Fixed KeyErrors with explicit column aliasing.
- Ensured calculations match ChronicCareIQ documentation.
- Added trend lines, SLA thresholds, cluster labels, and improved visuals.

6. Next Steps
- Add consistent color palette (red/yellow/green).
- Add filters (clinician, patient, date range).
- Export summary reports (PDF/Excel).
- Benchmark against clinical outcomes.

Architecture Diagram (Conceptual):
Database (MySQL: call_record, call_entry, patient_answer, patient)
   ↓
data_loader.py (Unified Query)
   ↓
df_unified (single source of truth)
   ↓
Modules: Engagement (2.1), Latency (2.2), Workload (2.3), Outreach (2.4)
   ↓
Visualizations: Scatter, Pie, Histogram, Bar, Heatmap, Trend lines
"""

pdf.multi_cell(0, 10, documentation)
pdf.output("ChronicCareIQ_Dashboard_Documentation.pdf")
print("PDF generated: ChronicCareIQ_Dashboard_Documentation.pdf")
