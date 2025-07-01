from gtts import gTTS
import os
import time

products = [
    ["Embroidered Vest", 1799], ["Plaid Flannel", 599], ["Distressed Patchwork Denim", 1299],
    ["Resin Corset", 2099], ["Embroidered Frock", 1399], ["Tailored Set", 1199],
    ["Oversized Sweatshirt", 799], ["Embroidered Blazer", 1899], ["Paisley Shirt", 999],
    ["Tiered Skirt", 899], ["Beige Trousers", 899], ["Plaid Trench Coat", 1399],
    ["Ribbed Sweater", 799], ["Knitted Vest", 699], ["Cargo Jacket", 1299],
    ["Flowy Top", 599], ["Crochet Top", 1099], ["Baroque Shirt", 799],
    ["Grid Sweater", 1199], ["Solid Skirt", 699], ["Layered Chains (W)", 399],
    ["Bangle Stack", 299],["Rings Stack (W)", 499], ["Layered Chain (M)", 199], ["Leather Bracelet", 199],
    ["Rings Stack (M)", 199], ["Goggles", 199],
    ["Dice Keychain", 99], ["Blue Twilly", 99], ["Silk Printed Necktie", 199]
]

AUDIO_DIR = os.path.join("assets", "audio")

# ### ADDED FOR DEBUGGING ###
print(f"Current Working Directory: {os.getcwd()}")
print(f"Target Audio Directory (relative): {AUDIO_DIR}")
absolute_audio_path = os.path.abspath(AUDIO_DIR)
print(f"Target Audio Directory (absolute): {absolute_audio_path}")

try:
    os.makedirs(AUDIO_DIR, exist_ok=True)
    print(f"Directory '{absolute_audio_path}' ensured to exist.")

    # Test file creation: ### ADDED FOR DEBUGGING ###
    test_file_path = os.path.join(absolute_audio_path, "test_write.txt")
    with open(test_file_path, "w") as f:
        f.write("This is a test to check write permissions.\n")
    print(f"Successfully created test file: {test_file_path}")

except Exception as dir_error:
    print(f"ERROR: Could not create or access audio directory or write test file: {dir_error}")
    exit() # Exit if we can't even get to the directory

print(f"Generating audio files into: {absolute_audio_path}")

for i, product in enumerate(products):
    product_name = product[0]
    product_price = product[1]

    text_to_speak = f"{product_name}, priced at {product_price} rupees."
    output_filename = f"product_audio_{i}.mp3"
    output_path = os.path.join(AUDIO_DIR, output_filename) # Keep this relative, as os.makedirs handles abs path

    print(f"\nProcessing product {i}: '{product_name}'")
    print(f"  Text to speak: '{text_to_speak}'")
    print(f"  Saving to: {os.path.abspath(output_path)}") # Print absolute path for each audio file

    try:
        tts = gTTS(text=text_to_speak, lang='en', slow=False)
        tts.save(output_path)
        print(f"  SUCCESS: Saved {output_filename}")
        time.sleep(0.1) # Short delay to see output
    except Exception as e:
        print(f"  ERROR: Failed to save {output_filename} for '{product_name}': {e}")

print("\nAudio generation complete!")