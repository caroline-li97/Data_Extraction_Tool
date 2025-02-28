# Data Extraction Tool

This document outlines the steps to extract data from PDF files and save it to a CSV file using a Python script. Follow the instructions below to set up and run the process.

## Steps

### 1. Download or Clone the GitHub Repository
- To get the necessary files, either:
  - **Download**: Click the **Download** button on the GitHub page to download the repository as a ZIP file.
  - **Clone**: Alternatively, you can clone the repository using the following link:
    ```bash
    git clone https://github.com/caroline-li97/Data_Extraction_Tool.git
    ```

### 2. Update Configurations in `data_extract.py`
- Open the `data_extract.py` file in your text editor.
- Change the following variables:
  ```python
  PATH = "path_to_your_data_directory/"   # Set the directory where your data is located
  OUTPUT_CSV = PATH + "output.csv"  # Specify the path where the output CSV file will be saved
  CSV_PATH = PATH + "table.csv"           # Path to the input CSV file
  ```
- Update the DETAIL_ROWS variable to specify the rows you want to include details in the extraction. Modify it as needed:
  ```python
  DETAIL_ROWS = set(range(5, 12)) | set(range(54, 60)) # rows 6-12 and 55-60
  ```

### 3. Download Ollama
- Visit the [Ollama website](https://ollama.com/) and download the Ollama software for your operating system.
- Follow the installation instructions provided on the website.

### 4. Run Ollama and the Python Script
- Open your terminal (or command prompt) and run Ollama on your computer.
  ```bash
  ollama start
  ```
- Alternatively, you can double-click the Ollama app on your desktop (or wherever you downloaded it) to start it.
- After you run Ollama, In a separate terminal window, navigate to the directory where data_extract.py is located and run the script:
  ```bash
  python3 data_extract.py
  ```

### 5. Monitor the Process
- You should see the following output in the terminal:
  ```bash
  Processing row 7/59...
  ```
  This message indicates which row the script is processing now.
- Once the task is completed, the following message will appear:
  ```bash
  Results added to CSV.
  ```

### 6. Check the Output
- The processed data will be saved in the CSV file specified in the ```OUTPUT_CSV``` path.
- You can open the CSV file to verify the extracted results.

### 7. Troubleshooting
- Ensure that Ollama is running properly while you execute the Python script.
- Double-check the paths and filenames in data_extract.py to make sure they point to the correct locations.
