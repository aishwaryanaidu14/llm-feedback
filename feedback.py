import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
import markdown
from bs4 import BeautifulSoup
import csv
import sys

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')


def markdown_to_text(markdown_string):
    # Convert Markdown to HTML
    html = markdown.markdown(markdown_string)
    # Use BeautifulSoup to extract text
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()


def analyze_code(file_content):
    """
    Sends the entire C file content to the Gemini model for analysis.
    """
    prompt = f"""
    Analyze the following C code file content and provide feedback on logical and syntax errors.
    Pay attention to any comments within the code, especially those like '@brief' or similar annotations,
    as they might indicate the intended functionality or specific requirements.

    File Content:
    ```c
    {file_content}
    ```

    Please provide a detailed analysis of the code, including:
    1. Syntax errors (point out specific lines if possible).
    2. Logical errors or potential runtime issues.
    3. How well the code seems to achieve any stated goals mentioned in comments (like @brief).
    
    DO NOT WRITE ANY CORRECTED CODE, KEEP THE RESPONSE UNDER 200 WORDS STRICTLY, DO NOT MENTION ANY THING RELATED TO OPTIMSATION OF THIS CODE 
    IF THERE ARE NO ERRORS WRITE "Your code was correct." AND DO NOT ADD ANYTHING ELSE TO THIS RESPONSE 
    """

    response = model.generate_content(prompt)
    return response.text


def process_c_files(folder_path):
    """
    Iterates through .c files in a folder, reads their full content,
    and sends it for analysis.
    """
    feedback = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.c'):
            student_id = filename[-15:-2]  # Remove '.c' from the filename
            print(filename)
            file_path = os.path.join(folder_path, filename)

            try:
                # Read the entire file content directly
                with open(file_path, 'r', encoding='utf-8') as file: # Added encoding for broader compatibility
                    file_content = file.read()

                print(f"Processing {filename}...")

                # Call analyze_code with the full content
                analysis = analyze_code(file_content)
                feedback[student_id] = analysis
                print(f"Analysis completed for {student_id}")

            except FileNotFoundError:
                print(f"Error: File not found {filename}")
                feedback[student_id] = f"Error: File not found."
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
                feedback[student_id] = f"Error processing file: {str(e)}"

    return feedback

def save_feedback_to_csv(feedback, csv_file_path):
    csv_data = []
    for key, value in feedback.items():
        csv_data.append({'student id': key, 'feedback': value})
    with open(csv_file_path, 'w', newline='') as csv_file:
        fieldnames = ['student id', 'feedback']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_data)

# Main execution
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: folder containing extracted files not provided")
        sys.exit(1)
    c_files_folder = sys.argv[1]
    output_csv = "LLM_Feedbacks.csv"
    
    if not os.path.exists(c_files_folder):
        print(f"Error: The folder '{c_files_folder}' does not exist.")
        print("Please create the folder and place the C files inside it.")
    elif not os.listdir(c_files_folder):
         print(f"Warning: The folder '{c_files_folder}' is empty.")
    else:
        print(f"Starting analysis of C files in '{c_files_folder}'...")
        feedback = process_c_files(c_files_folder)
        if feedback:
            save_feedback_to_csv(feedback, output_csv)
            print(f"\nFeedback has been saved to {output_csv}")
        else:
            print("\nNo C files were found or processed.")