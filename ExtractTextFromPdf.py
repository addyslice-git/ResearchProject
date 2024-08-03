import os
import fitz  # PyMuPDF
import re

## this is the function that does the search for the keywords for me 

def search_keywords_in_pdf(pdf_path, keywords):
    # Open the PDF file
    document = fitz.open(pdf_path)
    results = {}

    # Iterate through each page
    for page_num in range(document.page_count):
        page = document.load_page(page_num)  # Load page
        text = page.get_text()  # Extract text from the page

        # Search for keywords in the text
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE):
                if keyword not in results:
                    results[keyword] = []
                # Collect the context and page number
                results[keyword].append((page_num + 1, text))

    return results

## this is the function that enables me to change the way the search query is done in the function
def search_keywords_in_directory(directory_path, keywords, section_names):
    # List all files in the 
    ## this is opening up a file 
    for file_name in os.listdir(directory_path):
        # Check if the file is a PDF
        if file_name.endswith('.pdf'):
            pdf_path = os.path.join(directory_path, file_name)
            print(f"Searching in {file_name}...\n")
            ## this is from where we are going to give the resul
 
            # Search for keywords in the current PDF
            results = search_keywords_in_pdf(pdf_path, keywords)         
            # Print the results
            for keyword, occurrences in results.items():
                print(f"\n\n****Keyword '{keyword}' found in {file_name}:")
                for page_num, context in occurrences:
                    print(f"\n Page {page_num}:")
                    # Print a snippet of the context around the keyword
                    start_idx = context.lower().find(keyword.lower())
                    snippet = context[max(0, start_idx-50):start_idx+len(keyword)+200]
                    print(f"    ...{snippet}...")
                print()

# Example usage
directory_path = 'C:\\Users\\addys\\OneDrive\\Documents\\PythonProjectIITM\\PaperData'
keywords = ['peak-voltage', 'cmxcm', 'cm2','electrolyte', 'electrolytic concentration', 'electrolytic concentration', 'electrode', 'current density', 'capacitive density']  # List of keywords to search for

section_names = ["experimental","results and discussion","conclusion"]
search_keywords_in_directory(directory_path, keywords, section_names)
