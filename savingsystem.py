# Imports, sorted alphabetically.

# Python packages
import cPickle as pickle
import os
import random
import struct
import time

# Third-party packages
# Nothing for now...

# Modules from this project
from blocks import BlockID
from debug import performance_info
import globals as G
from player import Player


__all__ = (
    'sector_to_filename', 'region_to_filename', 'sector_to_region',
    'sector_to_offset', 'save_world', 'world_exists', 'remove_world',
    'sector_exists', 'load_region', 'open_world',
)


structvec = struct.Struct("hhh")
structushort = struct.Struct("H")
structuchar2 = struct.Struct("BB")
structvecBB = struct.Struct("hhhBB")

null2 = struct.pack("xx") #Two \0's
null1024 = null2*512      #1024 \0's
air = G.BLOCKS_DIR[(0,0)]

def sector_to_filename(secpos):
    x,y,z = secpos
    return "%i.%i.%i.pyr" % (x/4, y/4, z/4)
def region_to_filename(region):
    return "%i.%i.%i.pyr" % region
def sector_to_region(secpos):
    x,y,z = secpos
    return (x/4, y/4, z/4)
def sector_to_offset(secpos):
    x,y,z = secpos
    return ((x % 4)*16 + (y % 4)*4 + (z % 4)) * 1024
def sector_to_blockpos(secpos):
    x,y,z = secpos
    return x*8, y*8, z*8

def save_sector_to_string(blocks, secpos):
    cx, cy, cz = sector_to_blockpos(secpos)
    fstr = ""
    for x in xrange(cx, cx+8):
        for y in xrange(cy, cy+8):
            for z in xrange(cz, cz+8):
                blk = blocks.get((x,y,z), air).id
                if blk:
                    if isinstance(blk, int):
                        blk = BlockID(blk)
                    fstr += structuchar2.pack(blk.main, blk.sub)
                else:
                    fstr += null2
    return fstr

@performance_info
def save_world(window, game_dir, world=None):
    if world is None: world = "world"
    if not os.path.exists(os.path.join(game_dir, world)):
        os.makedirs(os.path.join(game_dir, world))

    #Non block related data
    save = (4,window.player, window.time_of_day, G.SEED)
    pickle.dump(save, open(os.path.join(game_dir, world, "save.pkl"), "wb"))

    save_blocks(window.world, world)

def save_blocks(blocks, world):
    #blocks and sectors (window.world and window.world.sectors)
    #Saves individual sectors in region files (4x4x4 sectors)
    if not os.path.exists(os.path.join(G.game_dir, world)):
        os.makedirs(os.path.join(G.game_dir, world))

    for secpos in blocks.sectors: #TODO: only save dirty sectors
        if not blocks.sectors[secpos]:
            continue #Skip writing empty sectors
        file = os.path.join(G.game_dir, world, sector_to_filename(secpos))
        if not os.path.exists(file):
            with open(file, "w") as f:
                f.truncate(64*1024) #Preallocate the file to be 64kb
        with open(file, "rb+") as f: #Load up the region file
            f.seek(sector_to_offset(secpos)) #Seek to the sector offset
            f.write(save_sector_to_string(blocks, secpos))


def world_exists(game_dir, world=None):
    if world is None: world = "world"
    return os.path.lexists(os.path.join(game_dir, world))


def remove_world(game_dir, world=None):
    if world is None: world = "world"
    if world_exists(game_dir, world):
        import shutil
        shutil.rmtree(os.path.join(game_dir, world))

def sector_exists(sector, world=None):
    if world is None: world = "world"
    return os.path.lexists(os.path.join(G.game_dir, world, sector_to_filename(sector)))

def load_region(world, world_name=None, region=None, sector=None):
    if world_name is None: world_name = "world"
    sectors = world.sectors
    blocks = world
    SECTOR_SIZE = G.SECTOR_SIZE
    BLOCKS_DIR = G.BLOCKS_DIR
    if sector: region = sector_to_region(sector)
    rx,ry,rz = region
    rx,ry,rz = rx*32, ry*32, rz*32
    with open(os.path.join(G.game_dir, world_name, region_to_filename(region)), "rb") as f:
        #Load every chunk in this region (4x4x4)
        for cx in xrange(rx, rx+32, 8):
            for cy in xrange(ry, ry+32, 8):
                for cz in xrange(rz, rz+32, 8):
                    #Now load every block in this chunk (8x8x8)
                    fstr = f.read(1024)
                    if fstr != null1024:
                        fpos = 0
                        for x in xrange(cx, cx+8):
                            for y in xrange(cy, cy+8):
                                for z in xrange(cz, cz+8):
                                    read = fstr[fpos:fpos+2]
                                    fpos += 2
                                    unpacked = structuchar2.unpack(read)
                                    if read != null2 and unpacked in BLOCKS_DIR:
                                        position = x,y,z
                                        blocks[position] = BLOCKS_DIR[unpacked]
                                        sectors[(x/SECTOR_SIZE, y/SECTOR_SIZE, z/SECTOR_SIZE)].append(position)

@performance_info
def open_world(gamecontroller, game_dir, world=None):
    if world is None: world = "world"

    #Non block related data
    loaded_save = pickle.load(open(os.path.join(game_dir, world, "save.pkl"), "rb"))
    if loaded_save[0] == 4:
        if isinstance(loaded_save[1], Player): gamecontroller.player = loaded_save[1]
        if isinstance(loaded_save[2], float): gamecontroller.time_of_day = loaded_save[2]
        if isinstance(loaded_save[3], str):
            G.SEED = loaded_save[3]
            random.seed(G.SEED)
            print('Loaded seed from save: ' + G.SEED)
    elif loaded_save[0] == 3: #Version 3
        if isinstance(loaded_save[1], Player): gamecontroller.player = loaded_save[1]
        if isinstance(loaded_save[2], float): gamecontroller.time_of_day = loaded_save[2]
        G.SEED = str(long(time.time() * 256))
        random.seed(G.SEED)
        print('No seed in save, generated random seed: ' + G.SEED)

    #blocks and sectors (window.world and window.world.sectors)
    #Are loaded on the fly
