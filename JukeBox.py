# 1 Pay money
# 2 Choose a CD and a song.
# 3 Play!
# All songs are equally priced
# During song play, no other request is accepted


class User:
    def __init__(self, money, jukebox):
        self.money = money
        self.jukebox = jukebox

    def request_play(self):
        if self.money >= self.jukebox.cost:
            self.money -= self.jukebox.cost
            self.jukebox.request(self, self.jukebox.cost)

    def choose_song(self):
        cd_id = int(input())
        song_id = int(input())
        return (cd_id, song_id)


class JukeBox:
    def __init__(self):
        self.cds = []
        self.cost = 10
        self.play_now = None
        self.sales = 0

    def add_CD(self, name, num_songs):
        self.cds.append(CD(name, num_songs))

    def request(self, user, pay):
        if self.play_now:
            user.money += self.cost
            return
        self.sales += pay
        self.show_playlist()
        print("Choose cd id and song id.")
        cd_id, song_id = user.choose_song()
        self.play_song(cd_id, song_id)

    def show_playlist(self):
        for i, cd in enumerate(self.cds):
            print('CD {0}'.format(i))
            cd.show_info()

    def play_song(self, cd_id, song_id):
        self.play_now = self.cds[cd_id].songs[song_id]
        self.play_now.play()

    def end_song(self):
        self.play_now = None


class CD:
    def __init__(self, name, num_songs):
        self.name = name
        self.num_songs = num_songs
        self.songs = [Song(i) for i in range(num_songs)]

    def show_info(self):
        print('CD name is {0}. Contains {1} songs'.format(
            self.name, self.num_songs))
        for song in self.songs:
            song.show_info()


class Song:
    def __init__(self, name):
        self.name = name

    def show_info(self):
        print('Song name is {0}'.format(self.name))

    def play(self):
        print('Tahhh')


juke = JukeBox()
juke.add_CD('yah', 10)
juke.add_CD('the', 8)
user = User(100, juke)
user.request_play()
