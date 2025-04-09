import os
import time
from urllib.request import urlretrieve
from PIL import Image, UnidentifiedImageError
from google_images_search import GoogleImagesSearch
import apikey  # Ensure you have a separate `apikey.py` file with API keys

# API Credentials
try:
    API_KEY = apikey.api_key
    CSE_ID = apikey.cse_id
except AttributeError:
    raise ValueError("API keys not found in apikey.py. Ensure api_key and cse_id are defined.")

# Initialize Google Images Search
gis = GoogleImagesSearch(API_KEY, CSE_ID)

# Ensure images folder exists
IMAGE_FOLDER = "images"
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# Fixed image size
IMAGE_SIZE = (300, 300)


def search_and_download_image(word, category, max_attempts=5):
    """Searches for an image and tries up to max_attempts to find a valid one."""
    image_path = os.path.join(IMAGE_FOLDER, f"{word}.jpg")

    # Skip download if the image already exists
    if os.path.exists(image_path):
        print(f"Image already exists for {word}. Skipping download.")
        return image_path

    query = f"{word}"
    gis.search({'q': query, 'num': max_attempts})

    for i, result in enumerate(gis.results()):
        try:
            image_url = result.url

            # Download the image
            urlretrieve(image_url, image_path)
            print(f"Downloaded image {i + 1} for {word}: {image_path}")
            time.sleep(1)  # Avoid API rate limits

            # Open, resize, and save the image
            with Image.open(image_path) as img:
                img = img.convert("RGB")
                img = img.resize(IMAGE_SIZE)
                img.save(image_path)
                print(f"Resized and saved: {image_path}")
                return image_path

        except (UnidentifiedImageError, OSError):
            print(f"Invalid image for {word}. Trying next...")

    print(f"Failed to get a valid image for {word}")
    return None


# Example list of categories with words
categories = [
    ("Animal", ["dog", "cat", "fish", "bird", "cow", "pig", "mouse", "horse", "wing"]),
    ("Transportation", ["train", "plane", "car", "truck", "bicycle", "bus", "boat", "ship", "tire", "gasoline", "engine", "ticket"]),
    ("Location", ["city", "house", "apartment", "street", "airport", "train station", "bridge", "hotel", "restaurant", 
                  "farm", "court", "school", "office", "room", "town", "university", "club", "bar", "park", "camp", "store", 
                  "theater", "library", "hospital", "church", "market", "country", "building", "ground", "space", "bank"]),
    ("Clothing", ["hat", "dress", "suit", "skirt", "shirt", "T-shirt", "pants", "shoes", "pocket", "coat", "stain"]),
    ("Color", ["red", "green", "blue", "yellow", "brown", "pink", "orange", "black", "white", "gray"]),
    ("People", ["son", "daughter", "mother", "father", "parent", "baby", "man", "woman", "brother", "sister", "family", "grandfather", 
                "grandmother", "husband", "wife", "king", "queen", "president", "neighbor", "boy", "girl", "child", "adult", 
                "human", "friend", "victim", "player", "fan", "crowd", "person"]),
    ("Job", ["teacher", "student", "lawyer", "doctor", "patient", "waiter", "secretary", "priest", "police", "army", "soldier", 
             "artist", "author", "manager", "reporter", "actor"]),
    ("Society", ["religion", "heaven", "hell", "death", "medicine", "money", "dollar", "bill", "marriage", "wedding", "team", 
                 "relationship", "race", "sex", "murder", "prison", "technology", "energy", "war", "peace", "attack", "election", 
                 "magazine", "newspaper", "poison", "gun", "sport", "race", "exercise", "ball", "game", "price", "contract", 
                 "drug", "sign", "science", "God"]),
    ("Art", ["band", "song", "instrument", "music", "movie", "art"]),
    ("Beverages", ["coffee", "tea", "wine", "beer", "juice", "water", "milk"]),
    ("Food", ["egg", "cheese", "bread", "soup", "cake", "chicken", "pork", "beef", "apple", "banana", "orange", "lemon", "corn", 
              "rice", "oil", "seed", "knife", "spoon", "fork", "plate", "cup", "breakfast", "lunch", "dinner", "sugar", "salt", 
              "bottle"]),
    ("Home", ["table", "chair", "bed", "dream", "window", "door", "bedroom", "kitchen", "bathroom", "pencil", "pen", "photograph", 
              "soap", "book", "page", "key", "paint", "letter", "note", "wall", "paper", "floor", "ceiling", "roof", "pool", 
              "lock", "telephone", "garden", "yard", "needle", "bag", "box", "gift", "card", "ring", "tool"]),
    ("Electronics", ["clock", "lamp", "fan", "cell phone", "network", "computer", "program", "laptop", "screen", "camera", "television", 
                     "radio"]),
    ("Body", ["head", "neck", "face", "beard", "hair", "eye", "mouth", "lip", "nose", "tooth", "ear", "tear", "tongue", "back", 
              "toe", "finger", "foot", "hand", "leg", "arm", "shoulder", "heart", "blood", "brain", "knee", "sweat", "disease", 
              "bone", "voice", "skin"]),
    ("Nature", ["sea", "ocean", "river", "mountain", "rain", "snow", "tree", "sun", "moon", "world", "earth", "forest", "sky", 
                "plant", "wind", "soil", "flower", "valley", "root", "lake", "star", "grass", "leaf", "air", "sand", "beach", 
                "wave", "fire", "ice", "island", "hill", "heat"]),
    ("Materials", ["glass", "metal", "plastic", "wood", "stone", "diamond", "clay", "dust", "gold", "copper", "silver"]),
    ("Measurements", ["meter", "centimeter", "kilogram", "inch", "foot", "pound", "half", "circle", "square", "temperature", 
                           "date", "weight", "edge", "corner"]),
    ("Misc Nouns", ["map", "dot", "consonant", "vowel", "light", "sound", "yes", "no", "piece", "pain", "injury", "hole", "image", 
                    "pattern"]),
    ("Directions", ["top", "bottom", "side", "front", "back", "outside", "inside", "up", "down", "left", "right", "straight", 
                    "north", "south", "east", "west"]),
    ("Seasons", ["summer", "spring", "winter", "fall"]),
    ("Numbers", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", 
                 "21", "22", "30", "31", "32", "40", "41", "42", "50", "51", "52", "60", "61", "62", "70", "71", "72", "80", 
                 "81", "82", "90", "91", "92", "100", "101", "102", "110", "111", "1000", "1001", "10000", "100000", "million", 
                 "billion", "1st", "2nd", "3rd", "4th", "5th"]),
    ("Months", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]),
    ("Days of the Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]),
    ("Time", ["year", "month", "week", "day", "hour", "minute", "second", "morning", "afternoon", "evening", "night"]),
    ("Verbs", ["work", "play", "walk", "run", "drive", "fly", "swim", "go", "stop", "follow", "think", "speak", "eat", "drink", 
               "kill", "die", "smile", "laugh", "cry", "buy", "pay", "sell", "shoot", "learn", "jump", "smell", "hear", "listen", 
               "taste", "touch", "see", "watch", "kiss", "burn", "melt", "dig", "explode", "sit", "stand", "love", "pass", "by", 
               "cut", "fight", "lie", "dance", "sleep", "wake", "sing", "count", "marry", "pray", "win", "lose", "mix", "bend", 
               "wash", "cook", "open", "close", "write", "call", "turn", "build", "teach", "grow", "draw", "feed", "catch", 
               "throw", "clean", "find", "fall", "push", "pull", "carry", "break", "wear", "hang", "shake", "sign", "beat", "lift"]),
    ("Adjectives", ["long", "short", "tall", "wide", "big", "small", "slow", "fast", "hot", "cold", "warm", "cool", "new", "old", 
                    "young", "good", "bad", "wet", "dry", "sick", "healthy", "loud", "quiet", "happy", "sad", "beautiful", 
                    "ugly", "deaf", "blind", "nice", "mean", "rich", "poor", "thick", "thin", "expensive", "cheap", "flat", 
                    "curved", "male", "female", "tight", "loose", "high", "low", "soft", "hard", "deep", "shallow", "clean", 
                    "dirty", "strong", "weak", "dead", "alive", "heavy", "light", "dark", "light", "nuclear", "famous"]),
    ("Pronouns", ["I", "you", "he", "she", "it", "we", "you", "they"])
]


# Process each category
for category, words in categories:
    print(f"Processing category: {category}")
    for word in words:
        print(f"  Processing word: {word}")
        search_and_download_image(word, category)
        
