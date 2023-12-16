# THIRD-PARTY
import pygame

# PROJECT
import config
import utils

# SET CONSTANTS, MUSIC
MUSIC_END = pygame.USEREVENT+1
MUSIC_TYPE_MAIN_MENU = "main_menu"
MUSIC_TYPE_GAME = "game"
MUSIC = [
    {"file": "resources/music/main1.mid", "type": MUSIC_TYPE_MAIN_MENU, "title": "Belle Qui Tiens Ma Vie"},
    #{"file": "resources/music/court1.mid", "type": MUSIC_TYPE_GAME, "title": "Greensleeves"},
    #{"file": "resources/music/court2.mid", "type": MUSIC_TYPE_GAME, "title": "Trotto"},
    #{"file": "resources/music/court3.mid", "type": MUSIC_TYPE_GAME, "title": "Saltarello"},
    {"file": "resources/music/game_a1.mid", "type": MUSIC_TYPE_GAME, "title": "Robert deVisée - Guitar Suite in Gm - 1st Movement"},
    {"file": "resources/music/game_a2.mid", "type": MUSIC_TYPE_GAME, "title": "Robert deVisée - Guitar Suite in Gm - 2nd Movement"},
    {"file": "resources/music/game_a3.mid", "type": MUSIC_TYPE_GAME, "title": "Robert deVisée - Guitar Suite in Gm - 3rd Movement"},
    {"file": "resources/music/game_a4.mid", "type": MUSIC_TYPE_GAME, "title": "Robert deVisée - Guitar Suite in Gm - 4th Movement"},
    {"file": "resources/music/game_a5.mid", "type": MUSIC_TYPE_GAME, "title": "Robert deVisée - Guitar Suite in Gm - 5th Movement"},
    {"file": "resources/music/game_a6.mid", "type": MUSIC_TYPE_GAME, "title": "Robert deVisée - Guitar Suite in Gm - 6th Movement"},
    {"file": "resources/music/game_a7.mid", "type": MUSIC_TYPE_GAME, "title": "Robert deVisée - Guitar Suite in Gm - 7th Movement"},
    #{"file": "resources/music/drama1.mid", "type": MUSIC_TYPE_GAME, "title": "François Couperin - Les Plaisirs de Saint Germain en Laÿe"},
    #{"file": "resources/music/drama2.mid", "type": MUSIC_TYPE_GAME, "title": "Germain Pinell - Branle des Frondeurs"},
    #{"file": "resources/music/drama3.mid", "type": MUSIC_TYPE_GAME, "title": "Ennemond Gaultier le vieux - Canarie in A"},
    #{"file": "resources/music/drama4.mid", "type": MUSIC_TYPE_GAME, "title": "Menuett in A"},
    #{"file": "resources/music/drama5.mid", "type": MUSIC_TYPE_GAME, "title": "François Couperin - Les Baricades Misterieuses"},
    {"file": "resources/music/game_b1.mid", "type": MUSIC_TYPE_GAME, "title": "Suite in Bm - 1st Movement"},
    {"file": "resources/music/game_b2.mid", "type": MUSIC_TYPE_GAME, "title": "Suite in Bm - 2nd Movement"},
    {"file": "resources/music/game_b3.mid", "type": MUSIC_TYPE_GAME, "title": "Suite in Bm - 3rd Movement"},
    {"file": "resources/music/game_b4.mid", "type": MUSIC_TYPE_GAME, "title": "Suite in Bm - 4th Movement"},
    {"file": "resources/music/game_b5.mid", "type": MUSIC_TYPE_GAME, "title": "Suite in Bm - 5th Movement"},
    {"file": "resources/music/game_b6.mid", "type": MUSIC_TYPE_GAME, "title": "Suite in Bm - 6th Movement"},
    #{"file": "resources/music/mystery1.mid", "type": MUSIC_TYPE_GAME, "title": "Courante in Am"},
    #{"file": "resources/music/mystery2.mid", "type": MUSIC_TYPE_GAME, "title": "Johann Georg Weichenberger - Menuett in Gm"},
    {"file": "resources/music/game_c1.mid", "type": MUSIC_TYPE_GAME, "title": "Aria in Bm"},
    {"file": "resources/music/game_c2.mid", "type": MUSIC_TYPE_GAME, "title": "Camille Tallard - Menuett in A"},
    {"file": "resources/music/game_c3.mid", "type": MUSIC_TYPE_GAME, "title": "Rondeau in C"},
    {"file": "resources/music/game_c4.mid", "type": MUSIC_TYPE_GAME, "title": "Ballet in D"},
    {"file": "resources/music/game_c5.mid", "type": MUSIC_TYPE_GAME, "title": "Sylvius Leopold Weiss - Menuett in Dm"},
    {"file": "resources/music/game_c6.mid", "type": MUSIC_TYPE_GAME, "title": "Favorita in D"},
    {"file": "resources/music/game_c7.mid", "type": MUSIC_TYPE_GAME, "title": "Ivan Gelinek - Canarie in Bb"},
    {"file": "resources/music/game_c8.mid", "type": MUSIC_TYPE_GAME, "title": "Gavotte in A"},
    {"file": "resources/music/game_c9.mid", "type": MUSIC_TYPE_GAME, "title": "Ennemond Gaultier le vieux - Chaconne in A"},
    {"file": "resources/music/game_c10.mid", "type": MUSIC_TYPE_GAME, "title": "Bouree in F"},
    {"file": "resources/music/game_c11.mid", "type": MUSIC_TYPE_GAME, "title": "Ivan Gelinek - Allemande in Gm"}
]

# SET CONSTANTS, SOUNDS
SOUNDS = {
    'boot': 'resources/sound/boot.ogg',
    'ui_sel': 'resources/sound/ui_sel.wav',
    'ui_confirm': 'resources/sound/ui_confirm.wav',
    'ui_confirm_big': 'resources/sound/ui_confirm_big.wav',
    'ui_back': 'resources/sound/ui_back.wav',
    'fx_change_room': 'resources/sound/fx_change_room.wav',
    'fx_npc_hit': 'resources/sound/fx_npc_hit.wav',
    'fx_move': 'resources/sound/fx_move.wav',
    'fx_pick_up_item': 'resources/sound/fx_pick_up_item.wav',
}

# SET VARS
master_volume = 0
music_volume = 0
sound_volume = 0
music_title = None
music_type = None
music_playlist_index = 0
music_playlist_files = []
music_playlist_titles = []

def initialize():
    pygame.mixer.set_num_channels(32)
    change_master_volume(config.settings['master_volume'])
    pygame.mixer.music.set_endevent(MUSIC_END) 
    music_change_type(MUSIC_TYPE_MAIN_MENU)

def music_change_type(new_type):
    global music_type
    if music_type != new_type:
        music_type = new_type
        make_playlist()
        music_play(0)

def change_master_volume(new_volume = 10):
    global master_volume
    new_volume = round(new_volume / 10, 1)
    master_volume = new_volume
    change_sound_volume(config.settings['sound_volume'])
    change_music_volume(config.settings['music_volume'])

def change_sound_volume(new_volume = 10):
    global sound_volume
    new_volume = round(new_volume / 10, 1)
    sound_volume = new_volume * master_volume

def change_music_volume(new_volume = 10):
    global music_volume
    new_volume = round(new_volume / 10, 1)
    music_volume = new_volume * master_volume
    pygame.mixer.music.set_volume(music_volume)

def make_playlist():
    global music_playlist_files
    global music_playlist_titles
    music_playlist_files = []
    music_playlist_titles = []
    for track in MUSIC:
        if (music_type is None or music_type == track['type']):
            music_playlist_files.append(track['file'])
            music_playlist_titles.append(track['title'])

def music_play(index = None):
    if config.settings['enable_music']:
        global music_playlist_index
        global music_title
        if index is not None:
            music_playlist_index = index
        else:
            music_playlist_index = utils.increment_number_loop(music_playlist_index, len(music_playlist_files))
        track = music_playlist_files[music_playlist_index]
        music_title = music_playlist_titles[music_playlist_index]
        pygame.mixer.music.load(track)
        pygame.mixer.music.set_volume(music_volume)
        pygame.mixer.music.play()

def music_stop():
    global music_title
    music_title = None
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()

def music_status():
    return pygame.mixer.music.get_busy()

def sound_play(sound_file, sound_type = None):
    if config.settings['enable_sound'] and (sound_type is None or (sound_type == 'ui' and config.settings['enable_sound_ui'])):
        sound = pygame.mixer.Sound(SOUNDS[sound_file])
        sound.set_volume(sound_volume)
        length = int(sound.get_length() * 1000)
        pygame.mixer.find_channel(True).play(sound)