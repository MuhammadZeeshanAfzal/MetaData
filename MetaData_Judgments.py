########################################################
#### complete updated but not final without data in image form
########################################################
# """How to Use
# For a Single File:
# bashpython legal_pdf_extractor.py --pdf CR-439_2022.pdf --output legal_metadata.json
# For an Entire Folder:
# bashpython MetaData_Judgments.py --folder D:\pythonprogram\Pak_Law_scrapper\AllData\FederalShariatCourt\FederalShariatCourt --output legal_metadata.json
# Additional Options:
# bash# Custom file pattern
# python legal_pdf_extractor.py --folder /path/to/pdfs --pattern "*.PDF" --output legal_metadata.json

# # Verbose logging
# python legal_pdf_extractor.py --folder /path/to/pdfs --verbose

# # Set API key directly
# python MetaData_judgments.py --folder D:\pythonprogram\Pak_Law_scrapper\AllData\LahoreHighCourt\LahoreJudgements --api-key "sk-proj-7xlHXJEnZNjDrtI3q2OlT3BlbkFJNYPV9PHTXbkOJHEeqXow"
# Key Features Added"""



# #!/usr/bin/env python3
# """
# Legal PDF Metadata Extractor

# This script extracts metadata from legal PDF documents using PyMuPDF for PDF parsing
# and OpenAI's API for intelligent metadata extraction from the document content.

# Features:
# - Batch processing of multiple PDF files
# - Skips already processed files
# - Appends data to a single JSON file
# - Handles API key expiration and balance issues
# """

# import os
# import sys
# import json
# import logging
# import argparse
# import glob
# import time
# from typing import Dict, Any, Optional, List
# from datetime import datetime

# import fitz  # PyMuPDF
# from openai import OpenAI, APIError, RateLimitError, APIConnectionError
# from dotenv import load_dotenv

# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S"
# )
# logger = logging.getLogger(__name__)

# class LegalPDFExtractor:
#     """A class to extract metadata from legal PDF documents using OpenAI APIs."""
    
#     # Define metadata fields to extract
#     METADATA_FIELDS = [
#         "Court Name",
#         "Case Title",
#         "Case Number",
#         "Type of Petition or Application",
#         "FIR Number and Date",
#         "Legal Sections Involved",
#         "Applicant and Respondents",
#         "Advocate Names for each party",
#         "Judge Name(s)",
#         "Hearing Date",
#         "Decision/Order Date",
#         "Outcome of the Application",
#         "Cited Case Laws",
#         "Short Summary of the Case"
#     ]
    
#     def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
#         """
#         Initialize the extractor with OpenAI API key and model.
        
#         Args:
#             api_key: OpenAI API key. If None, will try to get from environment.
#             model: OpenAI model to use for extraction.
#         """
#         # Load environment variables from .env file if present
#         load_dotenv()
        
#         # Use provided API key or get from environment
#         self.api_key = api_key or os.getenv("OPENAI_API_KEY")
#         if not self.api_key:
#             raise ValueError("OpenAI API key is required. Provide it as an argument or set OPENAI_API_KEY environment variable.")
        
#         self.model = model
#         self.client = OpenAI(api_key=self.api_key)
        
#         # Track processed files
#         self.processed_files = set()
    
#     def extract_text_from_pdf(self, file_path: str) -> tuple[str, int, Dict[str, Any]]:
#         """
#         Extract text content and metadata from a PDF file.
        
#         Args:
#             file_path: Path to the PDF file
            
#         Returns:
#             Tuple of (extracted text, page count, pdf metadata)
        
#         Raises:
#             FileNotFoundError: If the PDF file doesn't exist
#             ValueError: If the file is not a valid PDF
#         """
#         if not os.path.exists(file_path):
#             raise FileNotFoundError(f"PDF file not found: {file_path}")
        
#         try:
#             doc = fitz.open(file_path)
            
#             # Extract embedded PDF metadata
#             pdf_metadata = doc.metadata
#             page_count = len(doc)
            
#             # Extract text from all pages
#             full_text = ""
#             for page in doc:
#                 full_text += page.get_text()
            
#             doc.close()
#             return full_text, page_count, pdf_metadata
            
#         except Exception as e:
#             raise ValueError(f"Error processing PDF file: {str(e)}")
    
#     def _create_metadata_extraction_prompt(self, pdf_text: str) -> str:
#         """
#         Create a prompt for the OpenAI API to extract metadata.
        
#         Args:
#             pdf_text: The text content of the PDF
            
#         Returns:
#             Formatted prompt string
#         """
#         # Generate the expected JSON structure for the output
#         json_structure = {
#             "source_file": "",
#             "Page count": "",
#         }
        
#         # Add all metadata fields to the JSON structure
#         for field in self.METADATA_FIELDS:
#             json_structure[field] = ""
            
#         # Create the prompt
#         prompt = f"""
#         You are a legal document analysis expert.

#         Please read the full text of the PDF document below and extract the following metadata in a valid and well-formatted JSON object.

#         Use **key-value pairs only**. Each field should be a key, and the corresponding answer should be the value. If any field is missing or not found in the document, set its value to "Not mentioned in the document".

#         Return the result in this exact structure:
#         {json.dumps(json_structure, indent=2)}

#         Here is the full text of the PDF document:
#         \"\"\"
#         {pdf_text}
#         \"\"\"
        
#         Important: Your response should contain ONLY the JSON object, no explanations or additional text.
#         """
        
#         return prompt
    
#     def extract_metadata(self, pdf_path: str) -> Dict[str, Any]:
#         """
#         Extract metadata from a legal PDF document.
        
#         Args:
#             pdf_path: Path to the PDF file
            
#         Returns:
#             Dictionary containing the extracted metadata
            
#         Raises:
#             ValueError: For API key issues or other fatal errors
#         """
#         logger.info(f"Processing file: {pdf_path}")
        
#         # Extract text and basic metadata from PDF
#         try:
#             pdf_text, page_count, pdf_metadata = self.extract_text_from_pdf(pdf_path)
#             logger.info(f"Successfully extracted text from PDF. Page count: {page_count}")
#         except Exception as e:
#             logger.error(f"Failed to extract text from PDF: {str(e)}")
#             raise
        
#         # Truncate text if it's too long (OpenAI has token limits)
#         if len(pdf_text) > 100000:  # Approximately 25,000 tokens
#             logger.warning("PDF text is very long, truncating to 100,000 characters")
#             pdf_text = pdf_text[:100000]
        
#         # Create prompt for OpenAI
#         prompt = self._create_metadata_extraction_prompt(pdf_text)
        
#         # Call OpenAI API with retry mechanism for rate limits
#         max_retries = 3
#         retry_delay = 5  # seconds
        
#         for attempt in range(max_retries):
#             try:
#                 logger.info(f"Calling OpenAI API with model: {self.model} (attempt {attempt+1}/{max_retries})")
#                 response = self.client.chat.completions.create(
#                     model=self.model,
#                     messages=[
#                         {"role": "system", "content": "You are a legal document metadata extractor."},
#                         {"role": "user", "content": prompt}
#                     ],
#                     temperature=0.3
#                 )
                
#                 # Get the response content
#                 result_text = response.choices[0].message.content
#                 logger.info("Successfully received metadata from OpenAI API")
                
#                 # Parse the JSON response
#                 try:
#                     # Clean up the response in case it includes markdown code blocks
#                     if "```json" in result_text:
#                         result_text = result_text.split("```json")[1].split("```")[0].strip()
#                     elif "```" in result_text:
#                         result_text = result_text.split("```")[1].split("```")[0].strip()
                    
#                     metadata = json.loads(result_text)
                    
#                     # Add page count and file info
#                     metadata["Page count"] = page_count
#                     metadata["source_file"] = os.path.basename(pdf_path)
#                     # metadata["full_path"] = os.path.abspath(pdf_path)
                    
#                     # Add timestamp for when extraction was performed
#                     # metadata["extraction_timestamp"] = datetime.now().isoformat()
                    
#                     return metadata
                    
#                 except json.JSONDecodeError as e:
#                     logger.error(f"Failed to parse JSON response: {str(e)}")
#                     logger.debug(f"Raw response: {result_text}")
#                     raise ValueError("OpenAI API returned a response that couldn't be parsed as JSON")
                    
#             except RateLimitError as e:
#                 if attempt < max_retries - 1:
#                     wait_time = retry_delay * (2 ** attempt)  # Exponential backoff
#                     logger.warning(f"Rate limit hit. Waiting {wait_time} seconds before retry...")
#                     time.sleep(wait_time)
#                 else:
#                     logger.error("Maximum retries reached for rate limit")
#                     raise ValueError(f"OpenAI API rate limit exceeded after {max_retries} attempts")
                    
#             except APIError as e:
#                 if "insufficient_quota" in str(e).lower() or "billing" in str(e).lower():
#                     logger.critical("OpenAI API key has insufficient balance or is expired")
#                     raise ValueError("OpenAI API key has insufficient balance or is expired") from e
#                 else:
#                     logger.error(f"API Error: {str(e)}")
#                     raise
                    
#             except APIConnectionError as e:
#                 if attempt < max_retries - 1:
#                     wait_time = retry_delay * (2 ** attempt)
#                     logger.warning(f"Connection error. Waiting {wait_time} seconds before retry...")
#                     time.sleep(wait_time)
#                 else:
#                     logger.error("Maximum retries reached for connection errors")
#                     raise ValueError(f"OpenAI API connection error after {max_retries} attempts") from e
                    
#             except Exception as e:
#                 logger.error(f"Error calling OpenAI API: {str(e)}")
#                 raise
    
#     def append_metadata_to_json(self, metadata: Dict[str, Any], output_path: str) -> None:
#         """
#         Append extracted metadata to a JSON file. If file doesn't exist, create it.
        
#         Args:
#             metadata: The extracted metadata dictionary
#             output_path: Path where to save/append the JSON file
#         """
#         try:
#             # Initialize with empty list if file doesn't exist
#             if not os.path.exists(output_path):
#                 data = []
#             else:
#                 # Load existing data
#                 with open(output_path, "r", encoding="utf-8") as f:
#                     try:
#                         data = json.load(f)
#                         # Ensure data is a list
#                         if not isinstance(data, list):
#                             data = [data]
#                     except json.JSONDecodeError:
#                         logger.warning(f"Existing file {output_path} is not valid JSON. Creating new file.")
#                         data = []
            
#             # Append new metadata
#             data.append(metadata)
            
#             # Write back to file
#             with open(output_path, "w", encoding="utf-8") as f:
#                 json.dump(data, f, ensure_ascii=False, indent=4)
                
#             logger.info(f"Metadata appended to {output_path}")
            
#         except Exception as e:
#             logger.error(f"Failed to append metadata to {output_path}: {str(e)}")
#             raise
    
#     def is_already_processed(self, pdf_path: str, output_path: str) -> bool:
#         """
#         Check if a PDF file has already been processed by looking at the output JSON.
        
#         Args:
#             pdf_path: Path to the PDF file
#             output_path: Path to the output JSON file
            
#         Returns:
#             True if file has already been processed, False otherwise
#         """
#         # If output file doesn't exist, nothing has been processed
#         if not os.path.exists(output_path):
#             return False
            
#         # Check if this specific file is in the processed set
#         if pdf_path in self.processed_files:
#             return True
            
#         try:
#             # Load existing data
#             with open(output_path, "r", encoding="utf-8") as f:
#                 try:
#                     data = json.load(f)
#                     # Ensure data is a list
#                     if not isinstance(data, list):
#                         data = [data]
                        
#                     # Check if the file is already in the data
#                     pdf_filename = os.path.basename(pdf_path)
#                     pdf_full_path = os.path.abspath(pdf_path)
                    
#                     for item in data:
#                         if isinstance(item, dict):
#                             # Check if source_file matches
#                             if item.get("source_file") == pdf_filename:
#                                 logger.info(f"File {pdf_path} already processed (found by filename)")
#                                 self.processed_files.add(pdf_path)  # Add to processed set
#                                 return True
#                             # Check if full_path matches
#                             if item.get("full_path") == pdf_full_path:
#                                 logger.info(f"File {pdf_path} already processed (found by full path)")
#                                 self.processed_files.add(pdf_path)  # Add to processed set
#                                 return True
                                
#                     return False
                    
#                 except json.JSONDecodeError:
#                     logger.warning(f"Existing file {output_path} is not valid JSON.")
#                     return False
                    
#         except Exception as e:
#             logger.error(f"Error checking if file is processed: {str(e)}")
#             return False
    
#     def process_folder(self, folder_path: str, output_path: str, file_pattern: str = "*.pdf") -> Dict[str, Any]:
#         """
#         Process all PDF files in a folder.
        
#         Args:
#             folder_path: Path to the folder containing PDF files
#             output_path: Path where to save the JSON output
#             file_pattern: Pattern to match PDF files (default: "*.pdf")
            
#         Returns:
#             Dictionary with processing statistics
#         """
#         # Ensure folder exists
#         if not os.path.isdir(folder_path):
#             raise ValueError(f"Folder not found: {folder_path}")
            
#         # Find all PDF files
#         pdf_files = glob.glob(os.path.join(folder_path, file_pattern))
        
#         if not pdf_files:
#             logger.warning(f"No files matching pattern '{file_pattern}' found in {folder_path}")
#             return {"total": 0, "processed": 0, "skipped": 0, "failed": 0}
            
#         logger.info(f"Found {len(pdf_files)} files to process")
        
#         # Statistics
#         stats = {
#             "total": len(pdf_files),
#             "processed": 0,
#             "skipped": 0,
#             "failed": 0
#         }
        
#         # Process each file
#         for pdf_path in pdf_files:
#             try:
#                 # Skip if already processed
#                 if self.is_already_processed(pdf_path, output_path):
#                     logger.info(f"Skipping already processed file: {pdf_path}")
#                     stats["skipped"] += 1
#                     continue
                    
#                 # Extract metadata
#                 metadata = self.extract_metadata(pdf_path)
                
#                 # Append to output file
#                 self.append_metadata_to_json(metadata, output_path)
                
#                 # Add to processed set
#                 self.processed_files.add(pdf_path)
                
#                 stats["processed"] += 1
#                 logger.info(f"Successfully processed {pdf_path}")
                
#             except ValueError as e:
#                 # Check if this is an API key issue (fatal error)
#                 if "api key has insufficient balance" in str(e).lower() or "api key is expired" in str(e).lower():
#                     logger.critical(f"Fatal error: {str(e)}")
#                     raise  # Re-raise to stop processing
                    
#                 # For other errors, continue with next file
#                 logger.error(f"Error processing {pdf_path}: {str(e)}")
#                 stats["failed"] += 1
                
#             except Exception as e:
#                 logger.error(f"Unexpected error processing {pdf_path}: {str(e)}")
#                 stats["failed"] += 1
        
#         return stats


# def main():
#     """Main function to run the metadata extraction process from command line."""
#     parser = argparse.ArgumentParser(description="Extract metadata from legal PDF documents")
#     parser.add_argument("--pdf", help="Path to a single PDF file")
#     parser.add_argument("--folder", help="Path to folder containing PDF files")
#     parser.add_argument("--pattern", help="File pattern for PDF files (default: *.pdf)", default="*.pdf")
#     parser.add_argument("--output", "-o", help="Output JSON file path", default="legal_metadata.json")
#     parser.add_argument("--api-key", help="OpenAI API key (if not set in environment)")
#     parser.add_argument("--model", help="OpenAI model to use", default="gpt-4o-mini")
#     parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    
#     args = parser.parse_args()
    
#     # Validate arguments
#     if not args.pdf and not args.folder:
#         parser.error("Either --pdf or --folder argument is required")
    
#     # Set logging level based on verbose flag
#     if args.verbose:
#         logger.setLevel(logging.DEBUG)
    
#     try:
#         # Initialize the extractor
#         extractor = LegalPDFExtractor(api_key=args.api_key, model=args.model)
        
#         # Process a single file
#         if args.pdf:
#             if extractor.is_already_processed(args.pdf, args.output):
#                 print(f"⏭️ Skipping already processed file: {args.pdf}")
#                 return 0
                
#             metadata = extractor.extract_metadata(args.pdf)
#             extractor.append_metadata_to_json(metadata, args.output)
#             print(f"✅ Successfully extracted metadata from {args.pdf}")
#             print(f"   Appended to: {args.output}")
            
#         # Process a folder
#         elif args.folder:
#             start_time = time.time()
#             stats = extractor.process_folder(args.folder, args.output, args.pattern)
#             elapsed_time = time.time() - start_time
            
#             print("\n📊 Processing Summary:")
#             print(f"   Total files found: {stats['total']}")
#             print(f"   Successfully processed: {stats['processed']}")
#             print(f"   Skipped (already processed): {stats['skipped']}")
#             print(f"   Failed: {stats['failed']}")
#             print(f"   Time elapsed: {elapsed_time:.2f} seconds")
#             print(f"   Output file: {args.output}")
            
#             if stats['failed'] > 0:
#                 print("\n⚠️  Some files failed to process. Check the log for details.")
                
#         return 0
        
#     except ValueError as e:
#         if "api key has insufficient balance" in str(e).lower() or "api key is expired" in str(e).lower():
#             print(f"\n❌ Critical Error: {str(e)}")
#             print("   Please check your OpenAI API key and billing status.")
#         else:
#             print(f"\n❌ Error: {str(e)}")
#         return 1
        
#     except Exception as e:
#         logger.error(f"Unexpected error: {str(e)}")
#         print(f"\n❌ Unexpected error: {str(e)}")
#         return 1


# if __name__ == "__main__":
#     sys.exit(main())











########################################################
#### Final updated code
########################################################

# !/usr/bin/env python3
"""
Legal PDF Metadata Extractor

This script extracts metadata from legal PDF documents using PyMuPDF for PDF parsing,
Pytesseract for OCR on image-based PDFs, and OpenAI's API for intelligent metadata extraction.

Features:
- Handles both text-based and image-based (scanned) PDFs
- Batch processing of multiple PDF files
- Skips already processed files
- Appends data to a single JSON file
- Handles API key expiration and balance issues
"""

import os
import sys
import json
import logging
import argparse
import glob
import time
import tempfile
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path

import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import numpy as np
from openai import OpenAI, APIError, RateLimitError, APIConnectionError
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

class LegalPDFExtractor:
    """A class to extract metadata from legal PDF documents using OpenAI APIs."""
    
    # Define metadata fields to extract
    METADATA_FIELDS = [
        "Court Name",
        "Case Title",
        "Case Number",
        "Type of Petition or Application",
        "FIR Number and Date",
        "Legal Sections Involved",
        "Applicant and Respondents",
        "Advocate Names for each party",
        "Judge Name(s)",
        "Hearing Date",
        "Decision/Order Date",
        "Outcome of the Application",
        "Cited Case Laws",
        "Short Summary of the Case"
    ]
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini", 
                 tesseract_path: Optional[str] = None, ocr_language: str = "eng"):
        """
        Initialize the extractor with OpenAI API key and model.
        
        Args:
            api_key: OpenAI API key. If None, will try to get from environment.
            model: OpenAI model to use for extraction.
            tesseract_path: Path to tesseract executable. If None, uses default.
            ocr_language: Language for OCR (default: eng)
        """
        # Load environment variables from .env file if present
        load_dotenv()
        
        # Use provided API key or get from environment
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Provide it as an argument or set OPENAI_API_KEY environment variable.")
        
        self.model = model
        self.client = OpenAI(api_key=self.api_key)
        
        # OCR setup
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        self.ocr_language = ocr_language
        
        # Track processed files
        self.processed_files = set()
    
    def extract_text_from_pdf(self, file_path: str) -> tuple[str, int, Dict[str, Any], bool]:
        """
        Extract text content and metadata from a PDF file.
        Uses OCR for image-based PDFs.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Tuple of (extracted text, page count, pdf metadata, is_ocr_used)
        
        Raises:
            FileNotFoundError: If the PDF file doesn't exist
            ValueError: If the file is not a valid PDF
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        try:
            doc = fitz.open(file_path)
            
            # Extract embedded PDF metadata
            pdf_metadata = doc.metadata
            page_count = len(doc)
            
            # First try normal text extraction
            full_text = ""
            for page in doc:
                full_text += page.get_text()
            
            # Check if we got meaningful text
            # If text is too short or contains mostly whitespace/special chars, use OCR
            is_ocr_used = False
            clean_text = full_text.strip()
            if len(clean_text) < 100 or len(clean_text.split()) < 20:
                logger.info(f"Text extraction yielded limited content ({len(clean_text)} chars). Using OCR.")
                full_text = self._extract_text_with_ocr(doc)
                is_ocr_used = True
            
            doc.close()
            return full_text, page_count, pdf_metadata, is_ocr_used
            
        except Exception as e:
            raise ValueError(f"Error processing PDF file: {str(e)}")
    
    def _extract_text_with_ocr(self, doc) -> str:
        """
        Extract text from PDF using OCR for image-based documents.
        
        Args:
            doc: PyMuPDF document object
            
        Returns:
            Extracted text as string
        """
        logger.info("Running OCR on PDF pages")
        full_text = ""
        
        for page_num, page in enumerate(doc):
            logger.info(f"Processing page {page_num+1}/{len(doc)} with OCR")
            
            # Get the page as a pixmap
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # Higher resolution for better OCR
            
            # Convert pixmap to PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # Use pytesseract to extract text
            page_text = pytesseract.image_to_string(img, lang=self.ocr_language)
            full_text += page_text + "\n\n"
        
        return full_text
    
    def _create_metadata_extraction_prompt(self, pdf_text: str, is_ocr_used: bool = False) -> str:
        """
        Create a prompt for the OpenAI API to extract metadata.
        
        Args:
            pdf_text: The text content of the PDF
            is_ocr_used: Whether OCR was used for extraction (may contain more errors)
            
        Returns:
            Formatted prompt string
        """
        # Generate the expected JSON structure for the output
        json_structure = {
            "source_file": "",
            "Page count": "",
        }
        
        # Add all metadata fields to the JSON structure
        for field in self.METADATA_FIELDS:
            json_structure[field] = ""
        
        ocr_guidance = ""
        if is_ocr_used:
            ocr_guidance = """
            Note: This text was extracted using OCR and may contain recognition errors.
            Please be forgiving of misspellings and formatting issues when extracting information.
            """
            
        # Create the prompt
        prompt = f"""
        You are a legal document analysis expert.

        Please read the full text of the PDF document below and extract the following metadata in a valid and well-formatted JSON object.{ocr_guidance}

        Use **key-value pairs only**. Each field should be a key, and the corresponding answer should be the value. If any field is missing or not found in the document, set its value to "Not mentioned in the document".

        You are a legal document analysis expert who only responds in English.
        The output must be entirely in English. Do not use any other language under any circumstances.

        Return the result in this exact structure:
        {json.dumps(json_structure, indent=2)}

        Here is the full text of the PDF document:
        \"\"\"
        {pdf_text}
        \"\"\"
        
        Important: Your response should contain ONLY the JSON object, no explanations or additional text.
        """
        
        return prompt
    
    def extract_metadata(self, pdf_path: str) -> Dict[str, Any]:
        """
        Extract metadata from a legal PDF document.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing the extracted metadata
            
        Raises:
            ValueError: For API key issues or other fatal errors
        """
        logger.info(f"Processing file: {pdf_path}")
        
        # Extract text and basic metadata from PDF
        try:
            pdf_text, page_count, pdf_metadata, is_ocr_used = self.extract_text_from_pdf(pdf_path)
            if is_ocr_used:
                logger.info(f"Successfully extracted text using OCR. Page count: {page_count}")
            else:
                logger.info(f"Successfully extracted text directly. Page count: {page_count}")
        except Exception as e:
            logger.error(f"Failed to extract text from PDF: {str(e)}")
            raise
        
        # Truncate text if it's too long (OpenAI has token limits)
        if len(pdf_text) > 100000:  # Approximately 25,000 tokens
            logger.warning("PDF text is very long, truncating to 100,000 characters")
            pdf_text = pdf_text[:100000]
        
        # Create prompt for OpenAI
        prompt = self._create_metadata_extraction_prompt(pdf_text, is_ocr_used)
        
        # Call OpenAI API with retry mechanism for rate limits
        max_retries = 3
        retry_delay = 5  # seconds
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Calling OpenAI API with model: {self.model} (attempt {attempt+1}/{max_retries})")
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a legal document metadata extractor."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3
                )
                
                # Get the response content
                result_text = response.choices[0].message.content
                logger.info("Successfully received metadata from OpenAI API")
                
                # Parse the JSON response
                try:
                    # Clean up the response in case it includes markdown code blocks
                    if "```json" in result_text:
                        result_text = result_text.split("```json")[1].split("```")[0].strip()
                    elif "```" in result_text:
                        result_text = result_text.split("```")[1].split("```")[0].strip()
                    
                    metadata = json.loads(result_text)
                    
                    # Add page count and file info
                    metadata["Page count"] = page_count
                    metadata["source_file"] = os.path.basename(pdf_path)
                    # metadata["extraction_method"] = "OCR" if is_ocr_used else "Text extraction"
                    
                    return metadata
                    
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse JSON response: {str(e)}")
                    logger.debug(f"Raw response: {result_text}")
                    raise ValueError("OpenAI API returned a response that couldn't be parsed as JSON")
                    
            except RateLimitError as e:
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (2 ** attempt)  # Exponential backoff
                    logger.warning(f"Rate limit hit. Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                else:
                    logger.error("Maximum retries reached for rate limit")
                    raise ValueError(f"OpenAI API rate limit exceeded after {max_retries} attempts")
                    
            except APIError as e:
                if "insufficient_quota" in str(e).lower() or "billing" in str(e).lower():
                    logger.critical("OpenAI API key has insufficient balance or is expired")
                    raise ValueError("OpenAI API key has insufficient balance or is expired") from e
                else:
                    logger.error(f"API Error: {str(e)}")
                    raise
                    
            except APIConnectionError as e:
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (2 ** attempt)
                    logger.warning(f"Connection error. Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                else:
                    logger.error("Maximum retries reached for connection errors")
                    raise ValueError(f"OpenAI API connection error after {max_retries} attempts") from e
                    
            except Exception as e:
                logger.error(f"Error calling OpenAI API: {str(e)}")
                raise
    
    def append_metadata_to_json(self, metadata: Dict[str, Any], output_path: str) -> None:
        """
        Append extracted metadata to a JSON file. If file doesn't exist, create it.
        
        Args:
            metadata: The extracted metadata dictionary
            output_path: Path where to save/append the JSON file
        """
        try:
            # Initialize with empty list if file doesn't exist
            if not os.path.exists(output_path):
                data = []
            else:
                # Load existing data
                with open(output_path, "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                        # Ensure data is a list
                        if not isinstance(data, list):
                            data = [data]
                    except json.JSONDecodeError:
                        logger.warning(f"Existing file {output_path} is not valid JSON. Creating new file.")
                        data = []
            
            # Append new metadata
            data.append(metadata)
            
            # Write back to file
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                
            logger.info(f"Metadata appended to {output_path}")
            
        except Exception as e:
            logger.error(f"Failed to append metadata to {output_path}: {str(e)}")
            raise
    
    def is_already_processed(self, pdf_path: str, output_path: str) -> bool:
        """
        Check if a PDF file has already been processed by looking at the output JSON.
        
        Args:
            pdf_path: Path to the PDF file
            output_path: Path to the output JSON file
            
        Returns:
            True if file has already been processed, False otherwise
        """
        # If output file doesn't exist, nothing has been processed
        if not os.path.exists(output_path):
            return False
            
        # Check if this specific file is in the processed set
        if pdf_path in self.processed_files:
            return True
            
        try:
            # Load existing data
            with open(output_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    # Ensure data is a list
                    if not isinstance(data, list):
                        data = [data]
                        
                    # Check if the file is already in the data
                    pdf_filename = os.path.basename(pdf_path)
                    pdf_full_path = os.path.abspath(pdf_path)
                    
                    for item in data:
                        if isinstance(item, dict):
                            # Check if source_file matches
                            if item.get("source_file") == pdf_filename:
                                logger.info(f"File {pdf_path} already processed (found by filename)")
                                self.processed_files.add(pdf_path)  # Add to processed set
                                return True
                            # Check if full_path matches
                            if item.get("full_path") == pdf_full_path:
                                logger.info(f"File {pdf_path} already processed (found by full path)")
                                self.processed_files.add(pdf_path)  # Add to processed set
                                return True
                                
                    return False
                    
                except json.JSONDecodeError:
                    logger.warning(f"Existing file {output_path} is not valid JSON.")
                    return False
                    
        except Exception as e:
            logger.error(f"Error checking if file is processed: {str(e)}")
            return False
    
    def process_folder(self, folder_path: str, output_path: str, file_pattern: str = "*.pdf") -> Dict[str, Any]:
        """
        Process all PDF files in a folder.
        
        Args:
            folder_path: Path to the folder containing PDF files
            output_path: Path where to save the JSON output
            file_pattern: Pattern to match PDF files (default: "*.pdf")
            
        Returns:
            Dictionary with processing statistics
        """
        # Ensure folder exists
        if not os.path.isdir(folder_path):
            raise ValueError(f"Folder not found: {folder_path}")
            
        # Find all PDF files
        pdf_files = glob.glob(os.path.join(folder_path, file_pattern))
        
        if not pdf_files:
            logger.warning(f"No files matching pattern '{file_pattern}' found in {folder_path}")
            return {"total": 0, "processed": 0, "skipped": 0, "failed": 0}
            
        logger.info(f"Found {len(pdf_files)} files to process")
        
        # Statistics
        stats = {
            "total": len(pdf_files),
            "processed": 0,
            "skipped": 0,
            "failed": 0
        }
        
        # Process each file
        for pdf_path in pdf_files:
            try:
                # Skip if already processed
                if self.is_already_processed(pdf_path, output_path):
                    logger.info(f"Skipping already processed file: {pdf_path}")
                    stats["skipped"] += 1
                    continue
                    
                # Extract metadata
                metadata = self.extract_metadata(pdf_path)
                
                # Append to output file
                self.append_metadata_to_json(metadata, output_path)
                
                # Add to processed set
                self.processed_files.add(pdf_path)
                
                stats["processed"] += 1
                logger.info(f"Successfully processed {pdf_path}")
                
            except ValueError as e:
                # Check if this is an API key issue (fatal error)
                if "api key has insufficient balance" in str(e).lower() or "api key is expired" in str(e).lower():
                    logger.critical(f"Fatal error: {str(e)}")
                    raise  # Re-raise to stop processing
                    
                # For other errors, continue with next file
                logger.error(f"Error processing {pdf_path}: {str(e)}")
                stats["failed"] += 1
                
            except Exception as e:
                logger.error(f"Unexpected error processing {pdf_path}: {str(e)}")
                stats["failed"] += 1
        
        return stats


def main():
    """Main function to run the metadata extraction process from command line."""
    parser = argparse.ArgumentParser(description="Extract metadata from legal PDF documents")
    parser.add_argument("--pdf", help="Path to a single PDF file")
    parser.add_argument("--folder",default=r"D:\pythonprogram\Pak_Law_scrapper\AllData\SindhServicesTribunal\SindhServiceTribunals", help="Path to folder containing PDF files")
    parser.add_argument("--pattern", help="File pattern for PDF files (default: *.pdf)", default="*.pdf")
    parser.add_argument("--output", "-o", help="Output JSON file path", default="SindhServiceTribunals.json")
    parser.add_argument("--api-key",default="sk-proj-7xlHXJEnZNjDrtI3q2OlT3BlbkFJNYPV9PHTXbkOJHEeqXow", help="OpenAI API key (if not set in environment)")
    parser.add_argument("--model", help="OpenAI model to use", default="gpt-4o-mini")
    parser.add_argument("--tesseract-path", help="Path to tesseract executable (for OCR)")
    parser.add_argument("--ocr-language", help="Language for OCR (default: eng)", default="eng")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.pdf and not args.folder:
        parser.error("Either --pdf or --folder argument is required")
    
    # Set logging level based on verbose flag
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    try:
        # Initialize the extractor
        extractor = LegalPDFExtractor(
            api_key=args.api_key, 
            model=args.model,
            tesseract_path=args.tesseract_path,
            ocr_language=args.ocr_language
        )
        
        # Process a single file
        if args.pdf:
            if extractor.is_already_processed(args.pdf, args.output):
                print(f"⏭️ Skipping already processed file: {args.pdf}")
                return 0
                
            metadata = extractor.extract_metadata(args.pdf)
            extractor.append_metadata_to_json(metadata, args.output)
            print(f"✅ Successfully extracted metadata from {args.pdf}")
            print(f"   Method: {metadata.get('extraction_method', 'Unknown')}")
            print(f"   Appended to: {args.output}")
            
        # Process a folder
        elif args.folder:
            start_time = time.time()
            stats = extractor.process_folder(args.folder, args.output, args.pattern)
            elapsed_time = time.time() - start_time
            
            print("\n📊 Processing Summary:")
            print(f"   Total files found: {stats['total']}")
            print(f"   Successfully processed: {stats['processed']}")
            print(f"   Skipped (already processed): {stats['skipped']}")
            print(f"   Failed: {stats['failed']}")
            print(f"   Time elapsed: {elapsed_time:.2f} seconds")
            print(f"   Output file: {args.output}")
            
            if stats['failed'] > 0:
                print("\n⚠️  Some files failed to process. Check the log for details.")
                
        return 0
        
    except ValueError as e:
        if "api key has insufficient balance" in str(e).lower() or "api key is expired" in str(e).lower():
            print(f"\n❌ Critical Error: {str(e)}")
            print("   Please check your OpenAI API key and billing status.")
        else:
            print(f"\n❌ Error: {str(e)}")
        return 1
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        print(f"\n❌ Unexpected error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

