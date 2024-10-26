from transformers import TapasTokenizer, TapasForQuestionAnswering
import pandas as pd
import psycopg2
import speech_recognition as sr
from googletrans import Translator

# Initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()

def getSelection():
    while True:
        try:
            userInput = int(input())
            if (userInput<1 or userInput>3):
                print("Not an integer! Try again.")
                continue
        except ValueError:
            print("Not an integer! Try again.")
            continue
        else:
            return userInput
            break
# Reading Audio file as source
# listening the audio file and store in audio_text variable
def startConvertion(path = 'output.wav',lang = 'en-IN'):
    with sr.AudioFile(path) as source:
        print('Fetching File')
        audio_text = r.record(source, duration=60)
        # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
        try:
            # using google speech recognition
            print('Converting audio transcripts into text ...')
            text = r.recognize_google(audio_text, language = lang)
            englishTest = translate_to_english(text)
            print(englishTest)
            return englishTest
        except:
            print('Sorry.. run again...')

def translate_to_english(hindi_text):
    translator = Translator()
    translated = translator.translate(hindi_text, src='hi', dest='en')
    return translated.text

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
        df['expiry_date'] = pd.to_datetime(df['expiry_date'], format='%Y-%m-%d')

        # Convert all columns to strings after ensuring expiry_date is datetime
        for col in df.columns:
            df[col] = df[col].apply(lambda x: str(x) if not isinstance(x, str) else x)

        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def query_model(table, question):
    tokenizer = TapasTokenizer.from_pretrained("google/tapas-base-finetuned-sqa")
    model = TapasForQuestionAnswering.from_pretrained("google/tapas-base-finetuned-sqa")

    # Prepare the inputs
    inputs = tokenizer(table=table, queries=[question], padding="max_length", return_tensors="pt")

    # Get model outputs
    outputs = model(**inputs)

    # Detach the logits
    logits = outputs.logits.detach()  # Keep it as a tensor
    logits_aggregation = (
        outputs.logits_aggregation.detach() if outputs.logits_aggregation is not None else None
    )

    # Convert the output logits to predicted answer coordinates
    result = tokenizer.convert_logits_to_predictions(inputs, logits, logits_aggregation)

    # Handle the structure of the result
    if isinstance(result, tuple):
        predicted_answer_coordinates = result[0]  # Take the first element
    else:
        predicted_answer_coordinates = result

    # Extract the answer
    answer = ""
    print("Predicted Answer Coordinates:", predicted_answer_coordinates)  # Debugging output

    # Iterate through the predicted answer coordinates
    for coordinates_list in predicted_answer_coordinates:
        for coordinates in coordinates_list:  # Each coordinates is a tuple (row_index, col_index)
            if isinstance(coordinates, tuple) and len(coordinates) == 2:
                row_index, col_index = coordinates  # Unpack row and column indices
                answer += str(table.iat[row_index, col_index]) + " "  # Access DataFrame correctly
            else:
                print("Unexpected coordinate format:", coordinates)  # Debugging output

    return answer.strip()

if __name__ == "__main__":
    # calling startConvertion method to start process
    user_prompt = startConvertion("UI/uploads/output.wav",
                    "en-IN")  # for time being I am using static file name here, we can take file input from user.


    query = "select * from mumbai_hacks.inventory"
    table = fetch_data_from_postgres(query)
    #user_prompt = "what is the quantity of pasta?"
    answer = query_model(table, user_prompt)
    print("Answer:", answer)