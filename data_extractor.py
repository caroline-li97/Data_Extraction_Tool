import pandas as pd
from ollama import chat
from ollama import ChatResponse
import fitz  # PyMuPDF

MODEL_NAME = "llama3.2"

PATH = "/Users/seven/Downloads/"
CSV_PATH = PATH + "table.csv"
OUTPUT_CSV = PATH + "output_table.csv"
Clinical_Signs_Extraction_DETAIL_ROWS = set(range(5, 11))
Parameter_Specific_Extraction_Rows = set(range(54, 59))

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
    response = ollama_detail_query(prompt1) 
    if "1" in response:
        prompt2 = f"Please read the following text and extract any information related to {item}. \"{text}\""
        return 1, ollama_detail_query(prompt2)
    return 0, None

def Parameter_Specific_Extraction(text, item):
    Parameter_keywords = {
    "size_of_pancreas": ["pancreatic atrophy, decreased pancreatic size","pancreatic enlargement, increased pancreatic size"],
    "echogenecity_of_pancreatic_parenchyma": ["hyperechoic pancreas", "hypoechoic pancreas, normal echogenicity"],
    "echogenecity_of_peripancreatic_mesentery": ["hyperechoic mesentery", "hypoechoic mesentery, normal"],
    "pancreatic_echotexture": "homogeneous pancreatic echotexture, normal",
    "presence_free_fluid_effusion ": ["free fluid, effusion, abdominal fluid", "absence of free fluid"],
    "conclusions_about_pancreas": "normal pancreas"
    }
    if item == "pancreatic_echotexture":
        prompt1 = f"Based on the text: \"{text}\" identify if {Parameter_keywords[item]} is explicitly mentioned in the conclusion section. If yes output 1 only, if not, output 0 only. Output only 1 or 0 with no explanations"
    if item == "conclusions_about_pancreas":
        prompt1 = f"Based on the text: \"{text}\" identify if {Parameter_keywords[item]} is explicitly mentioned. If yes output 1 only, if not, output 0 only. Output only 1 or 0 with no explanations"
    else:
        prompt1 = f"Based on the text: \"{text}\" identify if {Parameter_keywords[item][0]} is explicitly mentioned. If yes output 2 only, if not, identify if {Parameter_keywords[item][1]} is explicitly mentioned. If yes output 1 only, if not, output 0 only. Output only 2 or 1 or 0 with no explanations"
    response1 = ollama_detail_query(prompt1)
    if "2" in response1 or "1" in response1:
        prompt2 = f"Please read the following text and extract any information related to {item}. \"{text}\""
        if "2" in response1:
            return 2, ollama_detail_query(prompt2)
        return 1, ollama_detail_query(prompt2)
    return 0, None

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
        text = extract_text_from_pdf(PATH + filename + ".pdf")
        if index in Clinical_Signs_Extraction_DETAIL_ROWS:
            result, detail = Clinical_Signs_Extraction(text, item)   
        elif index in Parameter_Specific_Extraction_Rows:
            result, detail = Parameter_Specific_Extraction(text, item)   
        else:
            result = ollama_result_query(text, item).strip()
            detail = None
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