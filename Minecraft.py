from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import pickle
import os

app = Ursina(title="Minecraft", fullscreen=True)

dirt = "asset/dirt.png"
stone = "asset/stone.jpg"
sky_texture = "asset/sky.jpg"
diamond = "asset/diamond.png"
leaf = "asset/leaf.jpg"
plank = "asset/plank.jpg"
wood = "asset/wood.jpg"
default_texture = stone
game_data = []

def save_game():
    with open("saves.pickle", "wb") as f:
        pickle.dump(game_data, f, -1)

def load_game():
    file = os.listdir('E:\Minecraft')
    if "saves.pickle" in file:
        saved_game = pickle.load(open("saves.pickle", "rb", -1))
        for data in saved_game:
            Voxsel(data[0], data[1])
        create_tree()
    else:
        start()

def create_tree():
    Voxsel((1,1,1), wood)
    Voxsel((1,2,1), wood)
    Voxsel((1,3,1), wood)
    Voxsel((1,4,1), leaf)
    Voxsel((1,4,2), leaf)
    Voxsel((1,3,2), leaf)
    Voxsel((1,4,0), leaf)
    Voxsel((1,3,0), leaf)
    Voxsel((2,4,1), leaf)
    Voxsel((2,3,1), leaf)
    Voxsel((0,4,1), leaf)
    Voxsel((0,3,1), leaf)
    Voxsel((2,3,2), leaf)
    Voxsel((0,3,0), leaf)
    Voxsel((2,3,0), leaf)
    Voxsel((0,3,2), leaf)


def update():
    global default_texture
    if held_keys['1']:
        default_texture = dirt
    if held_keys['2']:
        default_texture = diamond
    if held_keys['3']:
        default_texture = stone
    if held_keys['4']:
        default_texture = leaf
    if held_keys['5']:
        default_texture = plank
    if held_keys['6']:
        default_texture = wood
    if held_keys['l']:
        save_game()

class Voxsel(Button):
    def __init__(self, position=(0,0,0), texture=dirt):
        super().__init__(
            model="cube",
            texture=texture,
            position=position,
            origin=1,
            parent=scene,
            color=color.white,
            highlight_color=color.light_gray
        )

    def input(self, key):
        if self.hovered:
            if key == "right mouse down":
                Voxsel(self.position + mouse.normal, texture=default_texture)
                pos = self.position + mouse.normal
                game_data.append([(pos.x, pos.y, pos.z), default_texture])
            if key == "left mouse down":
                destroy(self)

class sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model="sphere",
            scale=150,
            texture=sky_texture,
            double_sided=True
        )

def start():
    for x in range(20):
        for z in range(20):
            grass_level = Voxsel((x,0,z))
            stone_level = Voxsel((x,-1,z), texture=stone)
            stone_level = Voxsel((x,-2,z), texture=stone)
            stone_level = Voxsel((x,-3,z), texture=diamond)
            game_data.append([(x,0,z) , dirt])
            game_data.append([(x,-1,z) , stone])
            game_data.append([(x,-2,z) , stone])
            game_data.append([(x,-3,z) , diamond])
    create_tree()

load_game()

player = FirstPersonController()
asmaan = sky()

app.run()