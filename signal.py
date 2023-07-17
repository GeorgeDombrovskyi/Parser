import os
import pygame



def play_mp3_file(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()


if __name__ == "__main__":

    mp3_file_path = "/Users/admin/Desktop/ShopParser/Rammstein-Reise, Reise.mp3"  # Replace this with the actual path to your MP3 file
    play_mp3_file(mp3_file_path)

    # To keep the program running until the audio finishes playing
    while pygame.mixer.music.get_busy():
        continue

