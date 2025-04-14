import os
import pandas as pd

# Paths
image_folder = "images"  # Change to your image folder path
csv_file = "words.csv"   # Change to your CSV filename

# Read the CSV
df = pd.read_csv(csv_file)

# Start building HTML
html_output = ""

for _, row in df.iterrows():
    english = row['english'].strip()
    farsi = row['farsi'].strip()
    image_path = os.path.join(image_folder, f"{english}.jpg")
    
    if os.path.exists(image_path):
        html_output += f"""
<div style="margin-bottom: 40px;">
  <img src="{image_path}" alt="{english}" style="max-width:300px;"><br><br>
  <div style="font-size: 24px;">{farsi}</div>
</div>
"""
    else:
        # Stop if image is missing
        print(f"Missing image for: {english}")
        break

# Output result
with open("output.html", "w", encoding="utf-8") as f:
    f.write(html_output)

print("HTML written to output.html")
