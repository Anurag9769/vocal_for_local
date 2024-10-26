from flask import Flask, request, render_template, send_from_directory,jsonify
import os
from transformers import TapasTokenizer, TapasForQuestionAnswering
import pandas as pd
import psycopg2
import speech_recognition as sr
# from googletrans import Translator
from deep_translator import GoogleTranslator
from vanna.ollama import Ollama
from vanna.vannadb import VannaDB_VectorStore

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class MyVanna(VannaDB_VectorStore, Ollama):
    def __init__(self, config=None):
        MY_VANNA_MODEL = 'mumbai_hacks' # Your model name from https://vanna.ai/account/profile
        VannaDB_VectorStore.__init__(self, vanna_model=MY_VANNA_MODEL, vanna_api_key='6314c5f41d7b4e4e8e865db9456d3002', config=config)
        Ollama.__init__(self, config=config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    
    return f"File uploaded successfully: {file.filename}", 200

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()


def start_conversion(path='output.wav', lang='en-IN'):
    with sr.AudioFile(path) as source:
        audio_text = r.record(source, duration=60)
        try:
            text = r.recognize_google(audio_text, language=lang)
            return text
        except Exception as e:
            return f"Error in audio transcription: {e}"


# def translate_to_english(text):
#     translator = Translator()
#     translated = translator.translate(text, src='hi', dest='en')
#     return translated.text

def translate_to_english(text):
    translated = GoogleTranslator(source='hi', target='en').translate(text)
    return translated


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
        df['expiry_date'] = pd.to_datetime(df['expiry_date'], format='%Y-%m-%d')
        for col in df.columns:
            df[col] = df[col].apply(lambda x: str(x) if not isinstance(x, str) else x)
        return df
    except Exception as e:
        return f"Error fetching data: {e}"
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def query_model(table, question):
    tokenizer = TapasTokenizer.from_pretrained("google/tapas-base-finetuned-sqa")
    model = TapasForQuestionAnswering.from_pretrained("google/tapas-base-finetuned-sqa")
    inputs = tokenizer(table=table, queries=[question], padding="max_length", return_tensors="pt")
    outputs = model(**inputs)
    result = tokenizer.convert_logits_to_predictions(inputs, outputs.logits.detach(),
                                                     outputs.logits_aggregation.detach() if outputs.logits_aggregation is not None else None)
    predicted_answer_coordinates = result[0] if isinstance(result, tuple) else result
    answer = ""
    for coordinates_list in predicted_answer_coordinates:
        for coordinates in coordinates_list:
            if isinstance(coordinates, tuple) and len(coordinates) == 2:
                row_index, col_index = coordinates
                answer += str(table.iat[row_index, col_index]) + " "
    return answer.strip()


@app.route("/process-audio", methods=["POST"])
def process_audio():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    question = start_conversion(file_path, "en-IN")
    user_prompt = translate_to_english(question)

    if "Error" in user_prompt:
        return jsonify({"error": user_prompt}), 500

    query = "SELECT * FROM mumbai_hacks.inventory"
    table = fetch_data_from_postgres(query)

    if isinstance(table, str) and "Error" in table:
        return jsonify({"error": table}), 500

    answer = query_model(table, user_prompt)
    # translator = Translator()
    # translated = translator.translate(answer, src='en', dest='hi').text

    translated = GoogleTranslator(source='en', target='hi').translate(answer)

    print(translated)
    return jsonify({"question": question, "answer": translated})


@app.route("/process-text", methods=["POST"])
def process_text():
    data = request.json  # or use request.get_json()
    text = data.get("text", "")
    print('###### Text: ', text)
    answer = query_lama_model(text)

    # query = "SELECT * FROM mumbai_hacks.inventory"
    # table = fetch_data_from_postgres(query)
    #
    # if isinstance(table, str) and "Error" in table:
    #     return jsonify({"error": table}), 500
    #
    # answer = query_model(table, text)
    print(answer)
    return jsonify({"question": text, "answer": answer})

def query_lama_model(text):
    vn = MyVanna(config={'model': 'llama3'})
    vn.connect_to_postgres(host='localhost', dbname='postgres', user='postgres', password='Anurag@#', port='5432')
    a, b, c = vn.ask('Which item will expire first?')
    print("SQL: ", a)
    print("Result: ", b)
    return b



if __name__ == '__main__':
    app.run(debug=True)
