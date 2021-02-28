# MP3 Metadata Autofiller
A Python script that uses the Spotify Web API to add album art to and fill in an MP3 file's metadata.

# Dependencies
For this program to function correctly you must have Python installed, along with the spotipy and mutagen libaries for Python.

- Download Python: https://www.python.org/downloads/
- Install spotipy: `pip install spotipy`
- Install mutagen: `pip install mutagen`

# How to Use
- Download and install Python, along with the other relevant dependencies as outlined above. 
- Download the zip file of the mp3-metadata-autofiller Github archive, and extract it to a folder. 
- Create a Spotify account (if you don't have one already), log in, and navigate to the following link: https://developer.spotify.com/dashboard/
- Click on the "Create an App" button on the top right corner of the page. 
- Name and describe your app to be whatever you'd like, and click on the "Create" button.
- You should be redirected to a seperate page for your app. Underneath the title and description for your app, there should be a "Client ID", and a "Client Secret" value (you may have to click the text labeled "Show Client Secret" to see the Client Secret value). 
- Edit lines 21 and 22 in the autofiller.py script, replacing the "PLACEHOLDER" text with your Client ID and Client Secret values (ex: client_id = "PLACEHOLDER" should become client_id = "YOUR_CLIENT_ID_VALUE", and the same goes for the client_secret variable). 
- Run a terminal window in the folder that you extracted the zip file to, and enter `python autofiller.py`.
- A file selection window will appear. Select the MP3 file that you wish to find metadata for. Ensure that the name of the file is in the following format: "Artist Name - Track Name" (ex: Billy Joel - Tell Her About It).  

# Troubleshooting
If the script is unable to locate your song or is getting incorrect information, here are a few things to try or take note of. 

- Ensure that the song you are looking for is actually on Spotify.
- Make sure that your artist and track name information is accurate. For example, "Tom Petty - Stop Draggin' My Heart Around" does not work, but "Stevie Nicks & Tom Petty - Stop Draggin' My Heart Around" does work. 
- A bug exists in the Spotify API itself. If a song title has special characters (things like the apostrophe, quotation marks, or non-English letters), and you provide both the song title and the artist into a search query, then the query will break and always return no results. To solve this issue, the script checks whether a song title has special characters, and only searches using the song title if this is the case, which works as intended. However, this means that if your song has both special characters and a very commonly used song title, then Spotify may confuse the song you are looking for with another song with the same title. In this case, try removing the special character from the title to see if this improves the situation. Other than that, however, there's not much I can do about the issue seeing as the bug exists within the API itself.
- Some songs on Spotify aren't available in all markets. This Spotify search function searches the US market by default, but if you're not finding your song you can override this behavior. To do this, edit lines 36 and 38 of the autofiller.py script to include a "market" parameter in the search query. 
    - ex: "track_query = spotify.search(q="artist:" + artist_name + " track:" + track_name, limit=1)" can become "track_query = spotify.search(q="artist:" + artist_name + " track:" + track_name, limit=1, market="GB)" to search the Great Britain market.
    - A list of valid market values can be found at the following link: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2

