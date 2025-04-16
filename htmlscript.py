import os
import pandas as pd

# Paths
image_folder = "images"  # Change to your image folder path
csv_file = "farsi_translations_transliteration_final.csv"   # Change to your CSV filename

# Read the CSV with safer encoding and select English + Phonetic columns
df = pd.read_csv(csv_file, usecols=[1, 3], skipinitialspace=True, encoding='ISO-8859-1')
df.columns = ['English', 'Phonetic']

# List of all image files in the folder (lowercased for case-insensitive match)
available_images = {filename.lower() for filename in os.listdir(image_folder)}

# HTML accumulator
html_output = ""

import base64

for _, row in df.iterrows():
    english = str(row['English']).strip()
    phonetic = str(row['Phonetic']).strip()
    
    image_filename = f"{english}.jpg"
    image_filename_lower = image_filename.lower()

    matching_image = next((img for img in available_images if img == image_filename_lower), None)
    
    if matching_image:
        image_path = os.path.join(image_folder, matching_image)
        
        # Read and encode image as base64
        with open(image_path, "rb") as img_file:
            img_data = base64.b64encode(img_file.read()).decode('utf-8')
            img_src = f"data:image/jpeg;base64,{img_data}"
        
        html_output += f"""
<div style="margin-bottom: 40px;">
  <img src="{img_src}" alt="{english}" style="max-width:300px;"><br><br>
  <div style="font-size: 24px;">{phonetic}</div>
</div>
"""
    else:
        print(f"❌ Image not retrieved for: {english} — skipping...")

# Save HTML
with open("output.html", "w", encoding="utf-8") as f:
    f.write(html_output)

print("✅ HTML written to output.html")
