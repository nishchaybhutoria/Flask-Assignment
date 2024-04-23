import csv, fitz

redemption_doc = fitz.open('eb_redemption_details.pdf')
purchase_doc = fitz.open('eb_purchase_details.pdf')
heading = 0

with open('redemption_data.csv', 'w', newline = '') as file:
    writer = csv.writer(file)    
    for page in redemption_doc:
        table = page.find_tables()[0]
        for line in table.extract()[heading:]:
            cleaned_line = [entry.replace('\n', ' ') if isinstance(entry, str) else entry for entry in line]
            writer.writerow(cleaned_line)
        heading |= 1

print("Processed redemption data")

heading = 0

with open('purchase_data.csv', 'w', newline = '') as file:
    writer = csv.writer(file)    
    for page in purchase_doc:
        table = page.find_tables()[0]
        for line in table.extract()[heading:]:
            cleaned_line = [entry.replace('\n', ' ') if isinstance(entry, str) else entry for entry in line]
            writer.writerow(cleaned_line)
        heading |= 1

print("Processed purchasing data")