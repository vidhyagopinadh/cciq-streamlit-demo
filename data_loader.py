import pandas as pd
import mysql.connector
from config import DB_CONFIG

def load_data(query):
    conn = mysql.connector.connect(**DB_CONFIG)
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def get_call_data():
    query = """
    SELECT 
        CallRecordId,
        PatientId,
        SourcePhone,
        DestinationPhone,
        CallDateTime,
        CallDuration,
        Direction
    FROM call_record
    WHERE PatientId IS NOT NULL
    """
    return load_data(query)

def get_patient_data():
    query = """
    SELECT 
        PatientId,
        FirstName,
        LastName,
        DaysWithMeasurements,
        MostRecentCall
    FROM patient
    WHERE IsTest = 0
    """
    return load_data(query)

def get_call_entry():
    query = """
    SELECT 
        CallEntryId,
        CallRecordId,
        PatientId,
        Phone,
        CallDateTime,
        CallDuration
    FROM call_entry
    """
    return load_data(query)

def get_patient_answers():
    query = """
    SELECT 
        PatientAnswerId,
        PatientId,
        AnswerDateTime,
        AnswerText,
        Score,
        AssignmentDate,
        MeasurementType,
        Alert
    FROM patient_answer
    """
    return load_data(query)

def get_unified_data():
    query = """
    SELECT 
        cr.CallRecordId,
        cr.PatientId,
        cr.SourcePhone,
        cr.DestinationPhone,
        cr.CallDateTime AS CallStart,
        cr.CallDuration,
        cr.Direction,
        ce.CallEntryId,
        ce.CallDateTime AS PickupTime,
        TIMESTAMPDIFF(SECOND, cr.CallDateTime, ce.CallDateTime) AS LatencySec,
        pa.PatientAnswerId,
        pa.AnswerDateTime,
        pa.Score,
        pa.Alert,
        p.DaysWithMeasurements,
        p.MostRecentCall
    FROM call_record cr
    LEFT JOIN call_entry ce ON cr.CallRecordId = ce.CallRecordId
    LEFT JOIN patient_answer pa ON cr.PatientId = pa.PatientId
    LEFT JOIN patient p ON cr.PatientId = p.PatientId
    WHERE p.IsTest = 0
    """
    return load_data(query)
