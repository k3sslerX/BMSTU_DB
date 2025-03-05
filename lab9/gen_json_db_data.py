from datetime import datetime
from time import sleep
import json

import random
from random import randint


class Data:
    def __init__(self, rows_count: int = 1000) -> None:
        self.person = None
        self.rows_count = rows_count

        self.min_age = 14
        self.max_age = 90
        self.min_song_duration = 60
        self.max_song_duration = 1200
        self.min_popularity = 1
        self.average_popularity = 50_000
        self.max_popularity = 10**7
        self.min_songs_count = 5
        self.max_songs_count = 20
        self.min_artists_count_on_album = 1
        self.max_artists_count_on_album = 4
        self.min_artists_count_on_song = 1
        self.max_artists_count_on_song = 3
        self.min_labels_count_on_album = 1
        self.max_labels_count_on_album = 3
            
        self.date_format = "%Y-%m-%d"

    @staticmethod
    def generate_song_title() -> str:
        adjectives = ["Lonely", "Happy", "Silent", "Mysterious", "Wild", "Golden"]
        nouns = ["Dream", "Night", "Journey", "Heart", "Sky", "Fire"]
        verbs = ["Whispers", "Falls", "Rises", "Burns", "Flows", "Shines"]
    
        adjective = random.choice(adjectives)
        noun = random.choice(nouns)
        verb = random.choice(verbs)
        
        title_format = random.choice([
            adjective,
            noun,
            verb,
            f"{noun} {verb}",
            f"The {adjective} {noun}",
            f"{noun} that {verb}",
            f"{verb} in the {adjective} {noun}",
            f"{adjective} {noun} {verb}",
        ])
        
        return title_format

    @staticmethod
    def generate_album_title() -> str:
        adjectives = ["Eternal", "Silent", "Lost", "Infinite", "Golden", "Mysterious"]
        nouns = ["Echoes", "Dreams", "Horizons", "Memories", "Voices", "Reflections"]
        themes = ["Journey", "Saga", "Chronicles", "Tales", "Odyssey", "Visions"]

        adjective = random.choice(adjectives)
        noun = random.choice(nouns)
        theme = random.choice(themes)
        
        title_format = random.choice([
            adjective,
            theme,
            noun,
            f"{adjective} {noun}",
            f"{noun} of {theme}",
            f"{theme} of the {adjective} {noun}",
            f"{adjective} {theme}",
        ])
        
        return title_format
    
    @staticmethod
    def generate_ganre() -> str:
        music_genres = [
            "Rock", "Pop", "Jazz", "Classical", "Hip Hop", "Electronic",
            "Blues", "Reggae", "Country", "Funk", "Soul", "R&B",
            "Metal", "Punk", "Folk", "Disco", "Techno",
            "House", "Trance", "Dubstep", "Ambient", "Ska",
            "Gospel", "Latin", "Indie", "Alternative", "Opera",
            "Swing", "Bluegrass", "Flamenco", "Tango",
            "Afrobeat", "Dancehall", "Trap", "World Music", "Celtic"
            ]

        return random.choice(music_genres)

    @staticmethod
    def generate_label_name() -> str:
        adjectives = ["Golden", "Silver", "Electric", "Magic", "Epic", "Loud", "Silent", "Dynamic", "Wild", "Blue", "Dark", "Neon", "Mystic", "Infinite", "Vivid"]
        nouns = ["Beats", "Records", "Sounds", "Harmony", "Groove", "Vibes", "Tunes", "Rhythms", "Melodies", "Waves", "Noise", "Echo", "Jams", "Tracks", "Sessions"]
        endings = ["Music", "Productions", "Studio", "Lab", "House", "Collective", "Crew", "Nation", "Factory", "Inc.", "Network", "Club"]

        adjective = random.choice(adjectives)
        noun = random.choice(nouns)
        ending = random.choice(endings)

        label_name = f"{adjective} {noun} {ending}"

        return label_name
    
    def generate_artist(self, index: int) -> tuple:
        artist_data = (index, self.person.first_name(),
                         self.person.first_name(),
                         self.person.last_name(),
                         randint(self.min_age, self.max_age),
                         self.person.birthdate().strftime(self.date_format))
        
        return artist_data
    
    def generate_artist_as_dict(self) -> dict:
        artist_data = {"stage_name": self.person.first_name(),
                       "first_name": self.person.first_name(),
                       "last_name": self.person.last_name(),
                       "age": randint(self.min_age, self.max_age),
                       "career_start": self.person.birthdate().strftime(self.date_format)}
        
        return artist_data
    
    def generate_song(self, index: int) -> tuple:
        popularity = randint(self.min_popularity, self.average_popularity) if randint(1, 10) <= 7 else randint(self.average_popularity, self.max_popularity)
        song_data = (index, self.generate_song_title(),
                         randint(self.min_song_duration, self.max_song_duration),
                         popularity,
                         randint(1, 4) == 1)
        
        return song_data
    
    def generate_album(self, index: int) -> tuple:
        songs_count = randint(self.min_songs_count, self.max_songs_count)
        album_data = (index, self.generate_album_title(),
                         songs_count,
                         self.generate_ganre(),
                         self.person.birthdate().strftime(self.date_format),
                         randint(90, 180) * songs_count)

        return album_data

    def generate_artists_data(self) -> list[tuple]:
        data = list()
        for i in range(self.rows_count):
            data.append(self.generate_artist(i))

        return data
    
    def generate_songs_data(self) -> list[tuple]:
        data = list()
        for i in range(self.rows_count):
            data.append(self.generate_song(i))

        return data
    
    def generate_albums_data(self) -> list[tuple]:
        data = list()
        for i in range(self.rows_count):
            data.append(self.generate_album(i))

        return data
    
    def generate_full_data(self) -> None:
        full_data = {
            'artists': [],
            'songs': [],
            'albums': [],
            'labels': []
        }

        full_data['artists'] = self.generate_artists_data()

        song_id = 0
        record_id = 0
        for row_number in range(self.rows_count):
            current_album = self.generate_album(row_number)
            album_artists_id = list(set([random.choice(full_data['artists'])[0] for _ in range(randint(self.min_artists_count_on_album, self.max_artists_count_on_album))]))
            album_labels = [self.generate_label_name() for _ in range(randint(self.min_labels_count_on_album, self.max_labels_count_on_album))]

            for song_number in range(current_album[2]):
                current_song = self.generate_song(song_id)
                song_artists_id = list(set([random.choice(album_artists_id) for _ in range(randint(self.min_artists_count_on_song, self.max_artists_count_on_song))]))
                for artist_id in song_artists_id:
                    full_data['labels'].append((record_id, current_album[0], song_id, artist_id, random.choice(album_labels)))
                    record_id += 1
                
                full_data['songs'].append(current_song)
                song_id += 1
            
            full_data['albums'].append(current_album)

        self.full_data =  full_data
    
    @staticmethod
    def save_data_to_file(file_path: str, data: list[tuple]) -> None:
        with open(file_path, "w") as file:
            for row in data:
                file.write(', '.join([str(item) for item in row]) + '\n')
    
    def write_artists_data_to_file(self) -> None:
        if self.full_data is None:
            raise ValueError('no data were generated')
        data = self.full_data['artists']
        self.save_data_to_file('../data/artists.txt', data)

    def write_songs_data_to_file(self) -> None:
        if self.full_data is None:
            raise ValueError('no data were generated')
        data = self.full_data['songs']
        self.save_data_to_file('../data/songs.txt', data)

    def write_albums_data_to_file(self) -> None:
        if self.full_data is None:
            raise ValueError('no data were generated')
        data = self.full_data['albums']
        self.save_data_to_file('../data/albums.txt', data)

    def write_labels_data_to_file(self) -> None:
        if self.full_data is None:
            raise ValueError('no data were generated')
        data = self.full_data['labels']
        self.save_data_to_file('../data/labels.txt', data)
    

class GenJson:
    def __init__(self, folder_path = "./"):
        self.folder_path = folder_path
        self.generator = Data()
        self.file_id = 1
        self.table_name = 'artists'
    
    def start(self, delay: int, records_count: int) -> None:
        print("Generation start")
        while True:
            file_name = self.gen_file(records_count)
            print("write data into ", file_name)
            sleep(delay)
    
    def gen_file(self, records_count: int) -> str:
        data_list = list()
        for _ in range(records_count):
            data_list.append(self.generator.generate_artist_as_dict())
        
        file_path = self.folder_path + self.generate_file_name()
        self.write_list_to_json_file(file_path, data_list)

        return file_path

    def generate_file_name(self) -> str:
        file_name = f"{self.file_id}#{self.table_name}#{datetime.now().strftime('%d-%m-%Y')}.json"
        self.file_id += 1
        return file_name

    @staticmethod
    def write_list_to_json_file(file_name: str, data: list) -> None:
        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)


# if __name__ == "__main__":
#     generator = GenJson(folder_path='C:\\sync_data\\programing\\DB\\lab_08\\nifi\\in_file')
#     generator.start(5, 10)
#     print("\n--- exit ---\n")
    