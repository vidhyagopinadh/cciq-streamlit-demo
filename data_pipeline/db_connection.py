import mysql.connector
import pandas as pd

def get_connection():
    return mysql.connector.connect(
        host="10.10.12.78",
        user="remote_al_ml_user",
        password="K8#mP2v$9XzQ_5nR",
        database="ai_ml_db"
    )

def fetch_engagement_data():
    conn = get_connection()
    query = """
    SELECT 
    p.PatientId,
    COUNT(cr.CallRecordId) AS TotalCalls,
    SUM(CASE WHEN pa.AnswerText IS NOT NULL THEN 1 ELSE 0 END) AS AnsweredQuestions,
    AVG(cr.CallDuration) AS AvgCallDuration,
    -- Engagement Score: 40% calls + 60% answers
    ((COUNT(cr.CallRecordId) * 0.4) + (SUM(CASE WHEN pa.AnswerText IS NOT NULL THEN 1 ELSE 0 END) * 0.6)) AS WeightedEngagementScore
FROM patient p
LEFT JOIN call_record cr 
    ON p.PatientId = cr.PatientId
LEFT JOIN patient_answer pa 
    ON p.PatientId = pa.PatientId
WHERE p.IsTest = 0
GROUP BY p.PatientId;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df
