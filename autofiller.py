import os

from urllib.request import urlopen

import tkinter
from tkinter.filedialog import askopenfilenames

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import mutagen
from mutagen.mp3 import MP3
from mutagen.id3 import ID3NoHeaderError, TALB, TPE1, TPE2, TYER, TRCK, TIT2,APIC, TPOS, TCOM

from dotenv import load_dotenv


class Song:
    def __init__(self, title, path):
        self.title = title
        self.path = path


def main():
    load_dotenv()
    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")
    file_paths = get_input_files()
    song_list, wrong_file_extension = get_tracks_and_artists(file_paths)

    if len(wrong_file_extension) > 0:
        print("One or more of the files that you input are not MP3 files. A list of all offending files will be "
              "output below. Please run the script again, making sure to pass in only MP3 files. \n")

        for file in wrong_file_extension:
            print(file)

        print()

    credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    spotify = spotipy.Spotify(client_credentials_manager=credentials_manager)

    error_list = obtain_and_edit_metadata(song_list, spotify)

    print("\nScript complete! For more detailed information on what was edited see the console output above. \n")

    if len(error_list) > 0:
        print("Spotify was unable to find one or more of your songs, or was unable to get all relevant song "
              "data for those tracks. A list of skipped tracks will be output below. For tips on how to try and make "
              "these tracks work, see the \"Troubleshooting\" section on the Github page. \n")

        for song in error_list:
            print(f"{song.title}")

        print()

    print("Thank you for using the MP3 Metadata Autofiller. \n")


def obtain_and_edit_metadata(song_list, spotify):
    error_list = []

    for song in song_list:
        track_query = spotify.search(q=song.title, limit=1)
        try:
            song_name = str(track_query['tracks']['items'][0]['name'])
            album_name = str(track_query['tracks']['items'][0]['album']['name'])
            release_year = str(track_query['tracks']['items'][0]['album']['release_date'])[:4]
            track_number = str(track_query['tracks']['items'][0]['track_number'])
            total_tracks = str(track_query['tracks']['items'][0]['album']['total_tracks'])
            disk_number = str(track_query['tracks']['items'][0]['disc_number'])
            album_artist = str(track_query['tracks']['items'][0]['album']['artists'][0]['name'])
            album_art = str(track_query['tracks']['items'][0]['album']['images'][0]['url'])
        except IndexError:
            print(f"Failed to add metadata to {song.title}!")
            error_list.append(song)
            continue

        song_artists = []
        artist_index = 0

        while True:
            try:
                curr_song_artist = str(track_query['tracks']['items'][0]['artists'][artist_index]['name'])
                song_artists.append(curr_song_artist)
                artist_index += 1
            except IndexError:
                break

        try:
            mp3_file = MP3(song.path)
            composer = str(mp3_file.get('TCOM'))
            composer = composer.split('-')[0].strip()
            mp3_file.delete()
            mp3_file.save()
        except ID3NoHeaderError:
            print("except")
            mp3_file = mutagen.File(song.path, easy=True)
            mp3_file.add_tags()

        mp3_file['TIT2'] = TIT2(encoding=3, text=song_name)
        mp3_file['TPE1'] = TPE1(encoding=3, text=", ".join(song_artists))
        mp3_file['TALB'] = TALB(encoding=3, text=album_name)
        mp3_file['TCOM'] = TCOM(encoding=3, text=composer)
        mp3_file['TPE2'] = TPE2(encoding=3, text=album_artist)
        mp3_file['TRCK'] = TRCK(encoding=3, text=track_number + "/" + total_tracks)
        mp3_file['TYER'] = TYER(encoding=3, text=release_year)
        mp3_file['TPOS'] = TPOS(encoding=3, text=disk_number)

        album_art = urlopen(album_art)

        mp3_file['APIC'] = APIC(
            encoding=3,
            mime='image/jpeg',
            type=3, desc=u'Cover',
            data=album_art.read()
        )

        album_art.close()
        mp3_file.save(v2_version=3)
        print(f"Added metadata to {song.title} successfully!")

    return error_list


def get_input_files():
    print("Please select the MP3 file(s) you wish to get metadata for. Ensure that the name of the file or files are "
          "in the following format: \"Track Name\" \n")
    tkinter.Tk().withdraw()
    files = askopenfilenames()
    return files


def get_tracks_and_artists(files):
    song_list = []
    wrong_file_extension = []

    for file in files:
        file_name = str(file)
        head, tail = os.path.split(file_name)

        if not tail.endswith(".mp3"):
            wrong_file_extension.append(file)
            continue

        try:
            track_name = tail[0: tail.index(".mp3")].strip()
            curr_song = Song(track_name, file)
            song_list.append(curr_song)
        except ValueError:
            continue

    return song_list, wrong_file_extension


main()
