# Textual Feedback Using LLM

A script to obtain textual feedback by LLMs of codes written in CS-F111 labs, BITS Pilani, Goa Campus. 

## 🔧 Setup & Usage

1. **Install dependencies:**

   ```pip install -r requirements.txt```


2. **Create a .env file in the project root and add Gemini API key:**

   GEMINI_API_KEY='your key here'

3. **Run the script with the folder path of the extracted files:**
    ```python feedback.py <folder_path>```

   Example: 
   ```python feedback.py all_extracted_files```

