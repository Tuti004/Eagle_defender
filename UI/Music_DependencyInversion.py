from abc import ABC, abstractmethod
import random
import pygame

class MusicPlayerDI(ABC):
    @abstractmethod
    def play_next_song(self):
        pass

class ShuffleDI(MusicPlayerDI):
    def __init__(self, canvas, song_list):
        self.canvas = canvas
        self.song_list = song_list
        self.current_song_index = 0
        self.shuffled_song_list = list(song_list)
        random.shuffle(self.shuffled_song_list)

    def play_next_song(self):
        pygame.mixer.music.load(self.shuffled_song_list[self.current_song_index])
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)
        song_length_ms = pygame.mixer.Sound(self.shuffled_song_list[self.current_song_index]).get_length() * 1000
        self.canvas.after(int(song_length_ms), self.play_next_song)

        # Ajusta el índice para el bucle infinito
        self.current_song_index = (self.current_song_index + 1) % len(self.shuffled_song_list)



