###################################################
######### Make seperate file for every laws from One file#######
###################################################
# import os
# import re

# # Path to the input file
# input_file = "C:/Users/abc123/Desktop/deltaimmigration/Punjab.md"

# # Output directory to store individual .md files
# output_dir = "Punjab_Laws"
# os.makedirs(output_dir, exist_ok=True)

# # Read the entire file
# with open(input_file, 'r', encoding='utf-8') as f:
#     lines = f.readlines()

# law_title_pattern = re.compile(r"^## \d+\s+(.*)")

# current_title = None
# current_lines = []

# def save_law(title, content):
#     safe_title = title.replace(":", "").replace("/", "-").strip()
#     output_path = os.path.join(output_dir, f"{safe_title}.md")
#     with open(output_path, 'w', encoding='utf-8') as out_file:
#         out_file.writelines(content)

# for line in lines:
#     match = law_title_pattern.match(line)
#     if match:
#         if current_title:
#             save_law(current_title, current_lines)
#         current_title = match.group(1)
#         current_lines = [line]
#     else:
#         current_lines.append(line)

# # Save the last law
# if current_title:
#     save_law(current_title, current_lines)

# print("✅ All laws have been split into separate markdown files.")



###################################################
######### Make seperate file for every laws all .md files in folder#######
###################################################
# import os
# import re

# # Path to the input folder containing .md files
# input_folder = "D:\Web_Scraping\MetaData\All_MD_files"
# # Output directory to store individual law files
# output_dir = "Punjab_Laws"
# os.makedirs(output_dir, exist_ok=True)

# # Regex to match law titles like: ## 1 Some Law Title
# law_title_pattern = re.compile(r"^## \d+\s+(.*)")

# def save_law(title, content, source_filename):
#     # Make title safe for filenames
#     safe_title = title.replace(":", "").replace("/", "-").strip()
#     base_filename = os.path.splitext(os.path.basename(source_filename))[0]
#     output_filename = f"{base_filename}__{safe_title}.md"  # include original file name for uniqueness
#     output_path = os.path.join(output_dir, output_filename)
#     with open(output_path, 'w', encoding='utf-8') as out_file:
#         out_file.writelines(content)

# # Loop through all .md files in the folder
# for filename in os.listdir(input_folder):
#     if filename.endswith(".md"):
#         input_path = os.path.join(input_folder, filename)
#         with open(input_path, 'r', encoding='utf-8') as f:
#             lines = f.readlines()

#         current_title = None
#         current_lines = []

#         for line in lines:
#             match = law_title_pattern.match(line)
#             if match:
#                 if current_title:
#                     save_law(current_title, current_lines, filename)
#                 current_title = match.group(1)
#                 current_lines = [line]
#             else:
#                 current_lines.append(line)

#         # Save the last law in the file
#         if current_title:
#             save_law(current_title, current_lines, filename)

# print("All laws from all .md files have been split into separate markdown files.")

###################################################
######### Give folder path which have all .md files to get metaData #######
###################################################
# import os
# import re
# import json
# import sys
# import io

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# def split_laws_from_file(text):
#     # Split each law block starting with ## <law_id> <title>
#     return re.findall(r'^##\s+\d+\s+.+?(?=^##\s+\d+\s+|\Z)', text, re.DOTALL | re.MULTILINE)

# def extract_detailed_metadata(law_text, source_filename="Unknown File"):
#     metadata = {}

#     # Extract Law ID and Title
#     title_match = re.match(r'^##\s*(\d+)\s+(.+)', law_text)
#     metadata['document_number'] = title_match.group(1).strip() if title_match else "Unknown"
#     metadata['title'] = title_match.group(2).strip() if title_match else "Untitled"

#     # Document type
#     doc_types = ['Act', 'Ordinance', 'Rules', 'Order', 'Regulation']
#     metadata['document_type'] = next((t for t in doc_types if t.lower() in law_text.lower()), 'Unknown')

#     # Jurisdiction and assumed publisher
#     metadata['jurisdiction'] = "Punjab"
#     metadata['published_by'] = "Government of Punjab"
#     metadata['location'] = "Lahore"
#     metadata['language'] = "English"

#     # Enacted under (if mentioned)
#     enacted_under = re.search(r'enacted under the\s+(.+?)(?:\.|\n)', law_text, re.IGNORECASE)
#     metadata['enacted_under'] = enacted_under.group(1).strip() if enacted_under else "Unknown"

#     # Law category (simple guess)
#     metadata['law_category'] = "General"

#     # Section titles and count
#     section_titles = re.findall(r'(?i)section\s+\d+[A-Z]?\.\s*(.*)', law_text)
#     metadata['section_titles'] = [
#         re.sub(r'\*+', '', title).strip().rstrip('.') + '.'
#         for title in section_titles
#         if len(title.strip()) > 2
#     ]
#     metadata['section_count'] = len(metadata['section_titles'])

#     # Effective year
#     year_match = re.search(r'(\d{4})', law_text)
#     metadata['effective_date'] = year_match.group(1) if year_match else "Unknown"

#     # Amended or not
#     metadata['amended'] = 'amend' in law_text.lower()

#     # Keywords
#     keyword_pool = ['zakat', 'committee', 'penalty', 'council', 'chairman', 'water',
#                     'tax', 'property', 'municipal', 'government', 'meeting', 'rules',
#                     'court', 'appeal', 'tribunal', 'fund', 'license']
#     found_keywords = [kw for kw in keyword_pool if kw in law_text.lower()]
#     metadata['keywords'] = list(set(found_keywords))

#     # Applicable to
#     if 'council' in law_text.lower() and 'member' in law_text.lower():
#         metadata['applicable_to'] = "Punjab Zakat Council Members"
#     else:
#         metadata['applicable_to'] = "Punjab Citizens or Officers"

#     # Summary (first 500 characters)
#     summary = law_text[:500].strip().replace('\n', ' ')
#     metadata['summary'] = f"Law summary: {summary[:250]}..." if summary else "No summary available."

#     # Source file
#     metadata['source'] = source_filename

#     return metadata

# def process_laws_from_folder(folder_path):
#     all_metadata = []
#     for filename in os.listdir(folder_path):
#         if filename.endswith('.md'):
#             full_path = os.path.join(folder_path, filename)
#             with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
#                 text = f.read()
#                 laws = split_laws_from_file(text)
#                 for law in laws:
#                     metadata = extract_detailed_metadata(law, source_filename=filename)
#                     all_metadata.append(metadata)
#     return all_metadata

# def save_metadata(metadata, output_file="punjab_detailed_metadata.json"):
#     with open(output_file, 'w', encoding='utf-8') as f:
#         json.dump(metadata, f, indent=4, ensure_ascii=False)

# # ✅ SET YOUR FOLDER PATH HERE
# folder_path = "Punjab_Laws"

# # Run processing
# metadata = process_laws_from_folder(folder_path)
# save_metadata(metadata)

# print(f"✅ Metadata created for {len(metadata)} laws from folder: {folder_path}")



###################################################
######### Give folder path which have all .md files to get metaData using OPENAI #######
###################################################
# import os
# import re
# import json

# # Configure your OpenAI API key and client
# from openai import OpenAI

# client = OpenAI(api_key="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")  # <-- ✅ Replace this or use `os.environ.get("OPENAI_API_KEY")`

# def split_laws_from_text(text):
#     return re.findall(r'^##\s+\d+\s+.+?(?=^##\s+\d+\s+|\Z)', text, re.DOTALL | re.MULTILINE)

# def generate_metadata_from_law(law_text, model="gpt-4o-mini"):
#     prompt = f"""
# Extract structured metadata from the following law text. Return **ONLY** a JSON object with these fields:

# - document_number like(## 1020 after ##)
# - title
# - document_type
# - jurisdiction
# - published_by
# - location
# - language
# - enacted_under
# - law_category
# - section_titles (only include titles that start with "**Section"; if none, return an empty list)
# - section_count (count of titles that start with "**Section"; if none, return 0)
# - effective_date
# - amended
# - keywords
# - applicable_to
# - summary
# - source

# Law text:
# \"\"\"
# {law_text}
# \"\"\"

# """

#     try:
#         response = client.chat.completions.create(
#             model=model,
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.2
#         )
#         content = response.choices[0].message.content.strip()

#         # Remove accidental markdown wrappers
#         if content.startswith("```json"):
#             content = content.removeprefix("```json").removesuffix("```").strip()

#         return json.loads(content)
#     except Exception as e:
#         print("Error:", str(e).encode("utf-8", errors="ignore").decode())  # Safe print
#         return {"error": str(e), "raw_text": law_text[:300]}

# def process_laws_with_openai(folder_path):
#     all_metadata = []
#     for file in os.listdir(folder_path):
#         if file.endswith(".md"):
#             with open(os.path.join(folder_path, file), 'r', encoding='utf-8') as f:
#                 text = f.read()
#                 laws = split_laws_from_text(text)
#                 for law in laws:
#                     metadata = generate_metadata_from_law(law)
#                     metadata['source'] = file
#                     all_metadata.append(metadata)
#     return all_metadata

# def save_metadata(metadata, output_file="openai_punjab_metadata.json"):
#     with open(output_file, "w", encoding="utf-8") as f:
#         json.dump(metadata, f, indent=4, ensure_ascii=False)

# # Run the script
# folder_path = "Punjab_Laws"
# metadata = process_laws_with_openai(folder_path)
# save_metadata(metadata)
# print(f"Extracted metadata for {len(metadata)} laws using GPT-4o-mini")


###################################################
######### Give folder path which have all .md files to get metaData using OPENAI And save record one by one #######
###################################################
import os
import re
import json
from openai import OpenAI

client = OpenAI(api_key="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")

def split_laws_from_text(text):
    return re.findall(r'^##\s+\d+\s+.+?(?=^##\s+\d+\s+|\Z)', text, re.DOTALL | re.MULTILINE)

def generate_metadata_from_law(law_text, model="gpt-4o-mini"):
    prompt = f"""
Extract structured metadata from the following law text. Return **ONLY** a JSON object with these fields:

- document_number like(## 1020 after ##)
- title
- document_type
- jurisdiction
- published_by
- location
- language
- enacted_under
- law_category
- section_titles (only include titles that start with "**Section", but **remove** the "**Section [number]. "** prefix from each title; if none, return an empty list)
- section_count (count of titles that start with "**Section"; if none, return 0)
- effective_date
- amended
- keywords
- applicable_to
- summary (limit to 2–3 concise sentences)
- source

Law text:
\"\"\"{law_text}\"\"\"
"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        content = response.choices[0].message.content.strip()
        if content.startswith("```json"):
            content = content.removeprefix("```json").removesuffix("```").strip()
        return json.loads(content)
    except Exception as e:
        print("Error:", str(e).encode("utf-8", errors="ignore").decode())
        return {"error": str(e), "raw_text": law_text[:300]}

def process_laws_and_append_to_combined_file(folder_path, combined_file="all_metadata.json"):
    combined_path = os.path.join(folder_path, combined_file)

    # Load existing metadata if file already exists
    if os.path.exists(combined_path):
        with open(combined_path, 'r', encoding='utf-8') as f:
            all_metadata = json.load(f)
    else:
        all_metadata = []

    for file in os.listdir(folder_path):
        if file.endswith(".md"):
            print(f"Processing {file}...")
            file_path = os.path.join(folder_path, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
                laws = split_laws_from_text(text)

                for law in laws:
                    metadata = generate_metadata_from_law(law)
                    metadata['source'] = file
                    all_metadata.append(metadata)

            # Save current combined metadata after each file
            with open(combined_path, "w", encoding="utf-8") as out_f:
                json.dump(all_metadata, out_f, indent=4, ensure_ascii=False)
            print(f"Appended data and saved to {combined_path}")

# Run the function
folder_path = "testing"
process_laws_and_append_to_combined_file(folder_path)






###################################################
######### Give folder path which have all .md files to get metaData, and summaries using OPENAI #######
###################################################
# import os
# import re
# import json
# from openai import OpenAI

# client = OpenAI(api_key="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")

# def split_laws_from_text(text):
#     return re.findall(r'^##\s+\d+\s+.+?(?=^##\s+\d+\s+|\Z)', text, re.DOTALL | re.MULTILINE)

# def extract_metadata_rule_based(law_text):
#     metadata = {}

#     # Document Number & Title
#     title_match = re.match(r'^##\s*(\d+)\s+(.+)', law_text)
#     metadata['document_number'] = title_match.group(1) if title_match else "Unknown"
#     metadata['title'] = title_match.group(2).strip() if title_match else "Untitled"

#     # Document type
#     doc_types = ['Act', 'Ordinance', 'Rules', 'Order', 'Regulation']
#     metadata['document_type'] = next((t for t in doc_types if t.lower() in law_text.lower()), 'Unknown')

#     # Fixed jurisdiction fields
#     metadata['jurisdiction'] = "Punjab"
#     metadata['published_by'] = "Government of Punjab"
#     metadata['location'] = "Lahore"
#     metadata['language'] = "English"

#     # Enacted under
#     enacted_match = re.search(r'enacted under the\s+(.+?)(?:\.|\n)', law_text, re.IGNORECASE)
#     metadata['enacted_under'] = enacted_match.group(1).strip() if enacted_match else "Unknown"

#     # Law category
#     metadata['law_category'] = "General"

#     # Sections
#     section_titles = re.findall(r'(?i)section\s+\d+[A-Z]?\.\s*(.*)', law_text)
#     metadata['section_titles'] = [re.sub(r'\*+', '', s).strip().rstrip('.') + '.' for s in section_titles if len(s.strip()) > 2]
#     metadata['section_count'] = len(metadata['section_titles'])

#     # Effective year
#     year_match = re.search(r'\b(19|20)\d{2}\b', law_text)
#     metadata['effective_date'] = year_match.group(0) if year_match else "Unknown"

#     # Amended
#     metadata['amended'] = 'amend' in law_text.lower()

#     # Applicable to
#     if 'council' in law_text.lower() and 'member' in law_text.lower():
#         metadata['applicable_to'] = "Punjab Zakat Council Members"
#     else:
#         metadata['applicable_to'] = "Punjab Citizens or Officers"

#     return metadata

# def generate_summary_with_openai(law_text, model="gpt-4o-mini"):
#     prompt = f"Summarize the following Punjab law in 2-3 sentences:\n\n\"\"\"\n{law_text[:3500]}\n\"\"\""
#     try:
#         response = client.chat.completions.create(
#             model=model,
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.3
#         )
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         return f"Summary unavailable due to error: {str(e)}"

# def process_laws(folder_path):
#     all_metadata = []
#     for file in os.listdir(folder_path):
#         if file.endswith(".md"):
#             with open(os.path.join(folder_path, file), 'r', encoding='utf-8') as f:
#                 text = f.read()
#                 laws = split_laws_from_text(text)
#                 for law in laws:
#                     metadata = extract_metadata_rule_based(law)
#                     metadata['summary'] = generate_summary_with_openai(law)
#                     metadata['source'] = file
#                     all_metadata.append(metadata)
#     return all_metadata

# def save_metadata(metadata, output_file="punjab_metadata_hybrid.json"):
#     with open(output_file, "w", encoding="utf-8") as f:
#         json.dump(metadata, f, indent=4, ensure_ascii=False)

# #  Set folder and run
# folder_path = "Punjab_Laws"
# metadata = process_laws(folder_path)
# save_metadata(metadata)
# print(f" Saved metadata for {len(metadata)} laws using hybrid approach")





###################################################
######### For abdullah#######
###################################################
# import json
# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.chrome.options import Options

# # Setup options
# options = Options()
# # options.add_argument("--headless")

# # Setup driver
# service = Service("D:/Web_Scraping/DigiLawyer/driver/chromedriver-win64/chromedriver.exe")
# driver = webdriver.Chrome(service=service, options=options)

# # Open the website
# url = "https://www.rios.pk/collections/new-makeup/products/compact-powder"
# driver.get(url)
# print("Opened website...")
# time.sleep(5)

# total_shades = 13
# results = []

# actions = ActionChains(driver)

# for i in range(1, total_shades + 1):
#     print(f"\n--- Processing shade index {i} ---")
#     try:
#         # Get shade label
#         shade_xpath = f"//*[@id='shopify-section-template--18255288729768__main']/div/div/div[2]/sticky-scroll-direction/div/div[4]/variant-picker/fieldset/div/label[{i}]"
#         shade_element = driver.find_element(By.XPATH, shade_xpath)

#         actions.move_to_element(shade_element).perform()
#         shade_name = shade_element.text.strip()
#         print(f"Clicking shade: '{shade_name}'")

#         shade_element.click()
#         time.sleep(2)

#         # Always get first image
#         try:
#             img_xpath = f"//*[@id='gallery-viewer']/li[{i}]/div/a/picture/img"
#             img_element = driver.find_element(By.XPATH, img_xpath)
#             img_src = img_element.get_attribute("src")

#             if not img_src:
#                 img_src = "NaN"
#         except Exception:
#             print("⚠️ Could not find image for this shade.")
#             img_src = "NaN"

#         print(f"Image src: {img_src}")

#         results.append({
#             "shade name": shade_name,
#             "src": img_src
#         })

#     except Exception as e:
#         print(f"❌ Failed to process shade {i}: {e}")

# # Save results to JSON
# with open("shades_data.json", "w") as f:
#     json.dump(results, f, indent=4)

# print("\n✅ Done! All data saved to 'shades_data.json'")
# driver.quit()
