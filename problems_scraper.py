import os
import requests

# Base URL for Project Euler problems
base_url = "https://projecteuler.net/"

# Directory to save the files
output_dir = "problems"

# Extensions that are treated as text attachments and embedded into problem files
TEXT_ATTACHMENT_EXTS = (
    ".txt",
    ".csv",
    ".dat",
    ".lst",
)

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

    # find text attachments and inline their contents into the problem description
    start = 0
    attachments = []
    text_modified = False
    while True:
        start = text.find("<a", start)
        if start == -1:
            break

        href_start = text.find('href="', start)
        if href_start == -1:
            start += 2
            continue

        href_end = text.find('"', href_start + 6)
        if href_end == -1:
            start += 2
            continue

        href = text[href_start + 6:href_end]
        normalized_href = href.split("?")[0]

        if not normalized_href.startswith("resources/"):
            start = href_end
            continue

        if not normalized_href.lower().endswith(TEXT_ATTACHMENT_EXTS):
            start = href_end
            continue

        anchor_close = text.find("</a>", href_end)
        if anchor_close == -1:
            start = href_end
            continue

        anchor_end = anchor_close + len("</a>")
        filename = os.path.basename(normalized_href)
        attachment_url = base_url + href

        response = requests.get(attachment_url)
        if response.status_code != 200:
            print(f"Failed to download attachment {attachment_url}, status code: {response.status_code}")
            start = anchor_end
            continue

        attachments.append((filename, response.text))
        print(f"Processed attachment {attachment_url} for problem {i:04d}")

        # include a more natural inline reference to the attachment while still hinting where the contents live
        replacement = f"the attachment {filename}"
        text = text[:start] + replacement + text[anchor_end:]
        start = start + len(replacement)
        text_modified = True

        # remove the optional right-click hint immediately following the attachment
        phrase_start = start
        while phrase_start < len(text) and text[phrase_start] == ' ':
            phrase_start += 1

        if text[phrase_start:].startswith("(right click"):
            hint_end = text.find(")", phrase_start)
            if hint_end != -1:
                text = text[:start] + text[hint_end + 1:]
                text_modified = True

    if attachments:
        text = text.rstrip("\n") + "\n\n"
        for filename, content in attachments:
            text += f"Attachment {filename}\n```\n{content.rstrip('\n')}\n```\n\n"
        text = text.rstrip("\n") + "\n"
        text_modified = True

    if text_modified:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(text)

    if attachments:
        print(f"Appended {len(attachments)} attachment(s) to {filepath}")
