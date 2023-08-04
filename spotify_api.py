from secrets import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_PLAYLIST_ID as AFTERGLOW_PLAYLIST_ID
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from typing import List


class SpotifyPlaylistExporter:
    def __init__(self, playlist_id: str) -> None:
        self.client_id = SPOTIFY_CLIENT_ID
        self.client_secret = SPOTIFY_CLIENT_SECRET
        self.playlist_id = playlist_id

    def _get_spotify_client(self) -> spotipy.Spotify:
        credentials_manager = SpotifyClientCredentials(client_id=self.client_id, client_secret=self.client_secret)
        return spotipy.Spotify(client_credentials_manager=credentials_manager)

    def _get_playlist_tracks(self) -> List[str]:
        sp = self._get_spotify_client()
        playlist = sp.playlist(self.playlist_id)
        tracks = playlist['tracks']

        track_list = []
        while tracks:
            for item in tracks['items']:
                track = item['track']
                track_name = track['name']
                artist_names = " ".join(artist['name'] for artist in track['artists'])
                track_list.append(f"{track_name} {artist_names}")
            tracks = sp.next(tracks) if tracks['next'] else None

        return track_list

    def export_to_txt(self, file_name: str) -> None:
        tracks = self._get_playlist_tracks()

        with open(file_name, 'w') as file:
            for track_line in tracks:
                file.write(f"{track_line}\n")

        print(f"{len(tracks)} tracks exported to {file_name}.")


if __name__ == "__main__":
    exporter = SpotifyPlaylistExporter(AFTERGLOW_PLAYLIST_ID)
    exporter.export_to_txt("afterglow.songs")
