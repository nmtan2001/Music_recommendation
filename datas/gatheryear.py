from spotipy.oauth2 import SpotifyOAuth
import spotipy
import requests
import base64
import time
import pandas as pd

# Replace with your own Client ID and Client Secret
CLIENT_ID = '338f97f982aa4b02baa16ce9512fd5fb'
CLIENT_SECRET = '73a09e941fda433a8d5a937a0bc99617'

# Base64 encode the client ID and client secret
client_credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
client_credentials_base64 = base64.b64encode(client_credentials.encode())

# Request the access token
token_url = 'https://accounts.spotify.com/api/token'
headers = {
    'Authorization': f'Basic {client_credentials_base64.decode()}'
}
data = {
    'grant_type': 'client_credentials'
}
response = requests.post(token_url, data=data, headers=headers)

if response.status_code == 200:
    access_token = response.json()['access_token']
    print("Access token obtained successfully.")
else:
    print("Error obtaining access token.")
    exit()


# # Create a Spotipy object
# sp = spotipy.Spotify(auth=access_token)

# # Get the track information
# track = sp.track('000CC8EParg64OmTxVnZ0p')

# # Get the release date
# release_date = track['album']['release_date']

# # Print the release date
# print(release_date)


def get_release_date(dataset, access_token):
    sp = spotipy.Spotify(auth=access_token)
    release_dates = []
    for trackid in dataset:
        info = sp.track(trackid)
        # time.sleep(5)
        release_date = info['album']['release_date']
        if release_date is not None:
            print(release_date)
            release_dates.append(
                {'track_id': trackid, 'release': release_date})
    return release_dates


df = pd.read_csv('df.csv')
df10 = df['track_id'][87000:89741]
# print(df10)

release_dates = get_release_date(df10, access_token)
# print(release_dates)
dfre = pd.DataFrame.from_records(release_dates)
dfre.columns = ['track_id', 'release']
dfre.to_csv('datas/df89k.csv', index=False)
