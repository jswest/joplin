import argparse
import glob
import os
import shutil
from tqdm import tqdm
from pathlib import Path
from playwright.sync_api import sync_playwright

def convert_html_to_pdf(html_file, output_pdf, browser):
    page = browser.new_page()
    page.goto(f"file://{html_file}")
    page.pdf(path=output_pdf, format="Letter")
    page.close()

def main():
    parser = argparse.ArgumentParser(description="Convert HTML files to PDF and copy existing PDFs using a headless browser.")
    parser.add_argument('input_path', help="The path to the directory to search")
    parser.add_argument('output_path', help="The path to the directory to store the PDFs")
    args = parser.parse_args()

    input_path = os.path.abspath(args.input_path)
    output_path = os.path.abspath(args.output_path)

    os.makedirs(output_path, exist_ok=True)

    pdf_files = glob.glob(os.path.join(input_path, '**', '*.pdf'), recursive=True)
    html_files = glob.glob(os.path.join(input_path, '**', '*.html'), recursive=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for html_file in tqdm(html_files, desc="Converting HTML to PDF"):
            try:
                slug = os.path.basename(html_file)
                output_pdf = os.path.join(output_path, slug + '.pdf')
                convert_html_to_pdf(html_file, output_pdf, browser)
            except Exception as e:
                print(f"Error converting {html_file}: {e}")
        browser.close()

    for pdf_file in tqdm(pdf_files, desc="Copying existing PDFs"):
        slug = os.path.basename(pdf_file)
        shutil.copy(pdf_file, os.path.join(output_path, slug))

if __name__ == "__main__":
    main()
