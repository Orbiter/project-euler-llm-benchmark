import os
import requests

# Base URL for Project Euler problems
base_url = "https://projecteuler.net/"

# Directory to save the files
output_dir = "problems"

# Ensure the directory exists
os.makedirs(output_dir, exist_ok=True)

# Loop through numbers from 1 to 913
for i in range(1, 914):
    # Create the full URL for the current problem
    url = f"{base_url}minimal={i}"

    # Format the filename with leading zeros (e.g., 0001.txt, 0002.txt, ...)
    filename = f"{i:04d}.txt"

    # Create the full file path
    filepath = os.path.join(output_dir, filename)

    text = ""
    # Check if the file already exists
    if os.path.exists(filepath):
        print(f"Skipping {url}, file already exists: {filepath}")
        # load the text file
        with open(filepath, 'r', encoding='utf-8') as file:
            text = file.read()
        
    else: 
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:

            text = response.text
            # replace all "<p>" with "" and all "</p>" with "\n"
            text = text.replace("<p>", "").replace("</p>", "\n")

            # Write the content of the response to a text file
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(text)

            print(f"Downloaded {url} and saved it as {filepath}")
        else:
            print(f"Failed to download {url}, status code: {response.status_code}")

    # find images in text
    # this would be a tag like:
    # <img src="resources/images/0015.png?1678992052" class="dark_img" alt=""></div>
    start = 0
    imgcount = 0
    while True:
        start = text.find("<img", start)
        if start == -1: break
        src_start = text.find('src="', start)
        src_end = text.find('"', src_start + 5)
        img = text[src_start + 5:src_end]
        # find next ">" after the img tag
        end = text.find(">", src_end)
        text = text[:start] + " " + text[end + 1:]

        # check if we have the image already
        ext = img.split(".")[-1]
        ext = ext.split("?")[0]
        img_filename = filename = f"{i:04d}-{imgcount}.{ext}"
        img_filepath = os.path.join(output_dir, img_filename)
        imgcount += 1
        if os.path.exists(img_filepath):
            print(f"Skipping {img}, file already exists: {img_filepath}")
            # save text again because we removed the image tag
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(text)
            break # end loop because we must assume that we have all images, otherwise counting would be wrong
        else:
            # load the image
            img_url = base_url + img
            img_response = requests.get(img_url)
            if img_response.status_code == 200:
                # save the image
                with open(img_filepath, 'wb') as file:
                    file.write(img_response.content)
                print(f"Downloaded {img_url} and saved it as {img_filepath}")

                # save text again because we removed the image tag
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(text)

                # end loop
                continue
            else:
                print(f"Failed to download {img_url}, status code: {img_response.status_code}")
    
    # find markup in text that has contained the images
    # i.e. "<div class="center">.*</div>"
    # each of this is replaced with (see image)
    start = 0
    while True:
        start = text.find("<div class=\"center\">", start)
        if start == -1: break
        end = text.find("</div>", start)
        text = text[:start] + "(see image)" + text[end + 6:]

        # save text again because we removed the image tag
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(text)