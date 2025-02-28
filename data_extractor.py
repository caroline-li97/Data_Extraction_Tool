import pandas as pd
from ollama import chat
from ollama import ChatResponse
import fitz  # PyMuPDF

MODEL_NAME = "llama3.2"

PATH = "/Users/seven/Downloads/"
CSV_PATH = PATH + "table.csv"
OUTPUT_CSV = PATH + "output_table.csv"
DETAIL_ROWS = set(range(5, 12)) | set(range(54, 60))

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

def ollama_detail_query(text, item):
    response: ChatResponse = chat(model=MODEL_NAME, messages=[
    {
        'role': 'user',
        'content': "Given the following text: \"" + text + "\", extract the exact original text snippet related to " + item + ". Output only the raw extracted text verbatim with no explanations, steps, formatting, or extra text."
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
        if index in DETAIL_ROWS:
            detail = ollama_detail_query(text, item).strip()

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