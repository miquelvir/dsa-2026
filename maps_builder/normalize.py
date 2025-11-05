import argparse
import csv

parser = argparse.ArgumentParser(description="Example CLI parser")
parser.add_argument("--txt", required=True, help="The path to a streets.txt file")
args = parser.parse_args()
FILE_NAME = args.txt
OUTPUT_FILE_NAME = FILE_NAME.replace('.txt', '_normalized.txt')

id_map = {}
next_id = 1

with open(FILE_NAME, newline='', encoding='utf-8') as infile, \
     open(OUTPUT_FILE_NAME, 'w', newline='', encoding='utf-8') as outfile:
    
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    for row in reader:
        for idx in [0, 3]:  # positions of SRC_ID and DEST_ID
            old_id = row[idx]
            if old_id not in id_map:
                id_map[old_id] = str(next_id)
                next_id += 1
            row[idx] = id_map[old_id]
        
        writer.writerow(row)

print(f"✅ Normalization complete. Last ID: {next_id-1}")
print(f"Output written to: {OUTPUT_FILE_NAME}")
