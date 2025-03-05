import pandas as pd
from ollama import chat
from ollama import ChatResponse
import fitz  # PyMuPDF

MODEL_NAME = "llama3.2"

PATH = "/Users/seven/Downloads/"
CSV_PATH = PATH + "table.csv"
OUTPUT_CSV = PATH + "output_table.csv"
Clinical_Signs_Extraction_DETAIL_ROWS = set(range(4, 11))
Parameter_Specific_Extraction_Rows = set(range(55, 60))

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def ollama_result_query(text, item):
    response: ChatResponse = chat(model=MODEL_NAME, messages=[
    {
        'role': 'user',
        'content': "Given the following text: \"" + text + "\", extract the specific result for " + item + ". Output only the raw extracted value with no explanations, steps, notes, formatting, or extra text."
    },
    ])
    return response['message']['content']

def Clinical_Signs_Extraction(text, item):
    Symptom_keywords = {
        "vomit_nausea": "Vomiting, nausea, regurgitation, emesis",
        "lethargy_weakness": "Lethargy, weakness, dull, depressed",
        "appetite_loss": "Inappetence, anorexia, hyporexia, not eating",
        "diarrhea_melena": "Diarrhea, melena, loose stools, tarry stools",
        "abdominal_pain": "Abdominal pain, prayer position, cranial abdominal pain",
        "weight_loss": "Weight loss, cachexia",
        "duration": ">14 days"

    }
    prompt1 = f"Based on the text: \"{text}\" identify if {Symptom_keywords[item]} is explicitly mentioned. If yes output 1 only. If no, output 0 only. Output only 1 or 0 with no explanations"
    if "1" in ollama_detail_query(prompt1):
        prompt2 = f"Based on the text: \"{text}\", Provide any relevant information or text related to {item}."
        return 1, ollama_detail_query(prompt2)
    return 0, None

def Parameter_Specific_Extraction(test, item):
    return 0, 0

def ollama_detail_query(prompt):
    response: ChatResponse = chat(model=MODEL_NAME, messages=[
    {
        'role': 'user',
        'content': prompt
    },
    ])
    return response['message']['content']

def process_csv():
    df = pd.read_csv(CSV_PATH)
    new_df = []
    for index in range(len(df)):
        print(f"Processing row {index + 1}/{len(df)}...")
        filename = df['filename'][index]
        item = df['items'][index]
        detail = None
        text = extract_text_from_pdf(PATH + filename + ".pdf")
        result = ollama_result_query(text, item).strip()
        if index in Clinical_Signs_Extraction_DETAIL_ROWS:
            result, detail = Clinical_Signs_Extraction(text, item)   
        if index in Parameter_Specific_Extraction_Rows:
            result, detail = Parameter_Specific_Extraction(text, item)   
        new_df.append({
            'filenames': filename,
            'items': item,
            'result': result,
            'details': detail
            })
    return pd.DataFrame(new_df)

def main():
    result_df = process_csv()
    result_df.to_csv(OUTPUT_CSV, index=False)
    print("Results added to CSV.")

if __name__ == "__main__":
    main()