import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
import psycopg2

# Initialize the tokenizer from Hugging Face Transformers library
tokenizer = T5Tokenizer.from_pretrained('t5-small')

# Load the model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = T5ForConditionalGeneration.from_pretrained('cssupport/t5-small-awesome-text-to-sql')
model = model.to(device)
model.eval()

import pandas as pd
import psycopg2

def fetch_data_from_postgres(query):
    try:
        connection = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='Anurag@#',
            host='localhost',
            port='5432'
        )
        cursor = connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        colnames = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(records, columns=colnames)

        # Ensure the expiry date column is in the correct datetime format
        if 'expiry_date' in df.columns:
            df['expiry_date'] = pd.to_datetime(df['expiry_date'], format='%Y-%m-%d')

        # Convert all columns to strings after ensuring expiry_date is datetime
        for col in df.columns:
            df[col] = df[col].apply(lambda x: str(x) if not isinstance(x, str) else x)

        # Convert the DataFrame to a formatted string
        result_string = df.to_string(index=False)  # Set index=False to avoid printing the DataFrame index
        return result_string

    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def generate_sql(input_prompt):
    # Tokenize the input prompt
    inputs = tokenizer(input_prompt, padding=True, truncation=True, return_tensors="pt").to(device)

    # Forward pass
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=512)

    # Decode the output IDs to a string (SQL query in this case)
    generated_sql = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return generated_sql

if __name__ == "__main__":
    # Test the function
    # input_prompt = "tables:\n" + "CREATE TABLE Catalogs (date_of_latest_revision VARCHAR)" + "\n" +"query for: Find the dates on which more than one revisions were made."
    # input_prompt = "tables:\n" + "CREATE TABLE table_22767 ( \"Year\" real, \"World\" real, \"Asia\" text, \"Africa\" text, \"Europe\" text, \"Latin America/Caribbean\" text, \"Northern America\" text, \"Oceania\" text )" + "\n" +"query for:what will the population of Asia be when Latin America/Caribbean is 783 (7.5%)?."
    # input_prompt = "tables:\n" + "CREATE TABLE procedures ( subject_id text, hadm_id text, icd9_code text, short_title text, long_title text ) CREATE TABLE diagnoses ( subject_id text, hadm_id text, icd9_code text, short_title text, long_title text ) CREATE TABLE lab ( subject_id text, hadm_id text, itemid text, charttime text, flag text, value_unit text, label text, fluid text ) CREATE TABLE demographic ( subject_id text, hadm_id text, name text, marital_status text, age text, dob text, gender text, language text, religion text, admission_type text, days_stay text, insurance text, ethnicity text, expire_flag text, admission_location text, discharge_location text, diagnosis text, dod text, dob_year text, dod_year text, admittime text, dischtime text, admityear text ) CREATE TABLE prescriptions ( subject_id text, hadm_id text, icustay_id text, drug_type text, drug text, formulary_drug_cd text, route text, drug_dose text )" + "\n" +"query for:" + "what is the total number of patients who were diagnosed with icd9 code 2254?"
    query = """SELECT 'CREATE TABLE ' || tablename || ' (' || string_agg(column_name || ' ' || 
       CASE 
           WHEN character_maximum_length IS NOT NULL THEN data_type || '(' || character_maximum_length || ')'
           ELSE data_type 
       END || 
       CASE 
           WHEN is_nullable = 'NO' THEN ' NOT NULL' ELSE '' 
       END, ', ') || ');'
FROM (
    SELECT table_name AS tablename, column_name, data_type, character_maximum_length, is_nullable
    FROM information_schema.columns
    WHERE table_name = 'inventory'
    ORDER BY ordinal_position
) AS subquery
GROUP BY tablename"""
    table = fetch_data_from_postgres(query)
    print(f"Table: {table}")
    input_prompt = "tables:\n" + table + "\n" + "query for:" + "Insert Milk in inventory"

    generated_sql = generate_sql(input_prompt)

    print(f"The generated SQL query is: {generated_sql}")
    # OUTPUT: The generated SQL query is: SELECT student_id FROM students WHERE NOT student_id IN (SELECT student_id FROM student_course_attendance)
