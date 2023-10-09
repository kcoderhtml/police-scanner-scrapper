import requests
from bs4 import BeautifulSoup
import pygame
import tempfile
import os
from urllib.parse import urlparse

def get_filename_from_url(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    filename = os.path.basename(path)
    return filename

def save_audio_file(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        filename = get_filename_from_url(url)
        with open(filename, 'wb') as file:
            file.write(response.content)
    else:
        print("Failed to download the audio file.")

def play_audio_file(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        # Create a temporary file to store the audio
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(response.content)
        temp_file.close()

        # Initialize pygame
        pygame.init()
        pygame.mixer.init()

        # Load and play the audio file using pygame
        pygame.mixer.music.load(temp_file.name)
        pygame.mixer.music.play()

        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            continue

        # Prompt for user input
        user_input = input(f"Do you want to save {url}? (y/n): ")
        if user_input.lower() == "y":
            save_audio_file(url)

        # Clean up the temporary file
        os.remove(temp_file.name)

        # Quit pygame
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        pygame.quit()
    else:
        print("Failed to download the audio file.")

def play_urls_with_prefix(urls, prefix):
    for url in urls:
        full_url = prefix + url
        play_audio_file(full_url)

def find_button_with_attributes():
    # load webste from file
    with open('test2.html', 'r') as f:
        response = f.read()

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response, 'html.parser')

    # Find the <button> element with the specified attributes
    buttons = soup.find_all('button', {
        'aria-label': 'Play',
        'onclick': lambda value: value and 'click_play_clip' in value,
        'class': 'player-action glyphicon glyphicon-play',
        'aria-hidden': 'false'
    })

    urls = []
    for button in buttons:
        onclick_value = button.get('onclick')
        if onclick_value:
            # Extract the URL from the onclick attribute
            start_index = onclick_value.index("'") + 1
            end_index = onclick_value.index("'", start_index)
            url = onclick_value[start_index:end_index]
            urls.append(url)

    return urls

# play the found URLs if any exist
found_urls = find_button_with_attributes()
if found_urls:
    prefix = 'http://scancbus.com'
    play_urls_with_prefix(found_urls, prefix)
else:
    print("No buttons matching the specified attributes were found.")