import os
from bs4 import BeautifulSoup
from openpyxl import Workbook

def html_to_excel_with_custom_headers(input_folder, output_excel_file):
    # Create a new Excel workbook
    workbook = Workbook()
    
    # Process each HTML file in the input folder
    for html_file in os.listdir(input_folder):
        if html_file.endswith(".html"):  # Process only .html files
            html_file_path = os.path.join(input_folder, html_file)
            
            # Read the HTML file content
            with open(html_file_path, "r", encoding="utf-8") as file:
                html_string = file.read()
            
            # Parse the HTML
            soup = BeautifulSoup(html_string, "html.parser")
            
            # Find the table
            table = soup.find("table", {"id": "ratings-table"})
            if not table:
                print(f"Table not found in {html_file_path}. Skipping this file.")
                continue

            # Define the custom header row
            custom_headers = [
                "Rk", "Team", "Conf", "W-L", "NetRtg", "ORtg", "ORtg_RANK", "DRtg", "DRtg_RANK",
                "AdjT", "AdjT_RANK", "Luck", "Luck_RANK", "Strength of Schedule NetRtg", "Strength of Schedule NetRtg_RANK",
                "Strength of Schedule ORtg", "Strength of Schedule ORtg_RANK", "Strength of Schedule DRtg",
                "Strength of Schedule DRtg_RANK", "NCSOS NetRtg", "NCSOS NetRtg_RANK"
            ]
            
            # Extract rows
            rows = []
            for tr in table.find_all("tr")[1:]:  # Skip the header row
                row = [td.text.strip() for td in tr.find_all("td")]
                if row:  # Only include non-empty rows
                    rows.append(row)
            
            # Create a sheet for this HTML file
            sheet_name = os.path.splitext(html_file)[0][:31]  # Excel sheet names must be <= 31 chars
            worksheet = workbook.create_sheet(title=sheet_name)
            
            # Write headers and rows to the sheet
            worksheet.append(custom_headers)
            for row in rows:
                worksheet.append(row)
    
    # Remove the default sheet created by openpyxl if it's empty
    default_sheet = workbook.active
    if not default_sheet._cells:  # If the default sheet is empty, remove it
        workbook.remove(default_sheet)
    
    # Save the workbook
    workbook.save(output_excel_file)
    print(f"Data successfully written to {output_excel_file}")

# Usage
input_folder = "kenpom_html"  # Folder containing HTML files
output_excel_file = "kenpom_data.xlsx"  # Output Excel file

html_to_excel_with_custom_headers(input_folder, output_excel_file)
