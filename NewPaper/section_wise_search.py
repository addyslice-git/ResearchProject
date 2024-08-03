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
            mod_file_name = file_name[:-4]
            ## creating a new file to store the output for this file 
            new_file_loc = directory_path + f"/{mod_file_name}"+".txt"
            file = open(new_file_loc, 'w', encoding='utf-8')
            print(f"Searching in {file_name}...\n")
            file.writelines(f"results for {file_name}...\n")
            ## this is from where we are going to give the results for the various sections

            sections = search_keywords_in_pdf(pdf_path, section_names)
            index ={}
            for section, occurences in sections.items():
                for page_num, context in occurences:
                    if(context.lower().find(section.lower())!= -1):
                        section_idx = context.lower().find(section.lower())
                        file.writelines(f"Section {section} found.. on page {page_num} has index {section_idx}\n")
                        print(f"...{section} {section_idx}....")
                        index[section] =section_idx
                        break

            print(index)
            # Search for keywords in the current PDF
            results = search_keywords_in_pdf(pdf_path, keywords)
            

            if(len(index)!=0):
                for section in index:
                    for keyword, occurrences in results.items():
                        # print(f"\n\n****Keyword '{keyword}' found in {file_name}: after beginning of section: {section}")
                        for page_num, context in occurrences:
                            start_idx = context.lower().find(keyword.lower())
                            if(start_idx>index[section]):
                                file.writelines(f"\n\n****Keyword '{keyword}' found in {file_name}: after beginning of section: {section}\n")
                                # print(f"\n Page {page_num}:")
                                file.write(f"\n\t Page {page_num}:")
                                # Print a snippet of the context around the keyword
                                snippet = context[max(0, start_idx-100):start_idx+len(keyword)+200]
                                # print(f"    ...{snippet}...")
                                file.writelines(f"    \t\t...{snippet}...\n\n")
                        
                

            # if there are no sections found, then we will assume that the paper is a relevant one and we will be taking all of the content
            else:
            # Print the results
                for keyword, occurrences in results.items():
                    file.writelines("\n\n\tATTENTION!! The paper couldnt be detected into sections the whole paper is searched for keywords.\n\n\t")
                    file.writelines(f"\n\n****Keyword '{keyword}' found in {file_name}:\n\n")
                    for page_num, context in occurrences:
                        file.writelines(f"\n \tPage {page_num}:")
                        # Print a snippet of the context around the keyword
                        start_idx = context.lower().find(keyword.lower())
                        snippet = context[max(0, start_idx-100):start_idx+len(keyword)+200]
                        file.writelines(f"   \t\t ...{snippet}...\n\n")
                    # print()
            file.close()

# Example usage
directory_path = 'C:\\Users\\addys\\OneDrive\\Documents\\PythonProjectIITM\\PaperData'

electrode = ['electrode','Activated Carbon', 'Stainless Steel']  # List of keywords to search for
electolyte = []
cyclicVoltametry= ['potential window', 'specific capacitance', 'current density', 'scan rates', 'Morphology','Concentration']
units=['area','cmxcm', 'cm2', 'voltage', 'V', 'normal','N','molar', 'M', 'A/cm2', 'F/g','mV/s', ]

section_names = ["Experimental","Results and discussion","Conclusion", "Voltametric data and performance"]
keywordList = electrode + cyclicVoltametry + units + electolyte
search_keywords_in_directory(directory_path, keywordList, section_names)