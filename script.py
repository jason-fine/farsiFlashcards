import os
from google_images_search import GoogleImagesSearch
from googletrans import Translator
from docx import Document
from urllib.request import urlretrieve
import apikey

api_key = apikey.api_key
cse_id = apikey.cse_id

gis = GoogleImagesSearch(api_key, cse_id)

# Initialize Google Translator
translator = Translator()

def search_image(query):
    # Perform an image search
    gis.search({'q': query, 'num': 1})
    image_url = gis.results()[0].url  # Get the URL of the first result
    image_name = f'{query}.jpg'
    urlretrieve(image_url, image_name)  # Save the image locally
    return image_name

def translate_word(word):
    # Translate the word to Farsi using Google Translate API
    translation = translator.translate(word, src='en', dest='fa')
    return translation.text

def create_document(words):
    # Create a Word document
    doc = Document()
    doc.add_heading('Word List with Images and Translations', 0)

    for word in words:
        # Add the word to the document
        doc.add_heading(word, level=1)

        # Add image of the word
        image_name = search_image(word)
        doc.add_picture(image_name)

        # Translate the word and add the translation
        translation = translate_word(word)
        doc.add_paragraph(f'Farsi Translation: {translation}')

        # Add a line break between words
        doc.add_paragraph('')

        # Clean up the image after adding it to the document
        os.remove(image_name)

    # Save the document
    doc.save('Word_List_with_Images_and_Translations.docx')

# Example usage
words = ['apple', 'book', 'house']  # Add your list of words here
create_document(words)
