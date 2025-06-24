
import mysql.connector

def get_patient_full_record(patient_id, db_config):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    def fetch(query):
        cursor.execute(query)
        return cursor.fetchall()

    queries = {
        "core_info": f"SELECT * FROM patient WHERE PatNum = {patient_id}",
        "appointments": f"SELECT * FROM appointment WHERE PatNum = {patient_id}",
        "medications": f"SELECT * FROM medicationpat WHERE PatNum = {patient_id}",
        "allergies": f"SELECT * FROM allergy WHERE PatNum = {patient_id}",
        "conditions": f"SELECT * FROM disease WHERE PatNum = {patient_id}",
        "procedures": f"SELECT * FROM procedurelog WHERE PatNum = {patient_id}",
        "recalls": f"SELECT * FROM recall WHERE PatNum = {patient_id}",
        "notes": f"SELECT * FROM commlog WHERE PatNum = {patient_id}",
        "referrals": f"SELECT * FROM refattach WHERE PatNum = {patient_id}",
        "insurances": f"SELECT * FROM patplan WHERE PatNum = {patient_id}"
    }

    result = {key: fetch(query) for key, query in queries.items()}

    cursor.close()
    connection.close()
    return result
