# Imports, sorted alphabetically.

# Python packages
# Nothing for now...

# Third-party packages
# Nothing for now...

# Modules from this project
from blocks import BlockID, dirt_block, farm_block, grass_block, wheat_crop_block
import globals as G


# From MinecraftWiki
# Items are objects which do not exist outside of the player's inventory and hands
# i.e., they cannot be placed in the game world.
# Some items simply place blocks or entities into the game world when used.
# Type
# * Materials: iron ingot, gold ingot, etc.
# * Food: found or crafted by the player and eaten to regain hunger points
# * Potions
# * Tools
# * Informative items: map, compass and clock
# * Weapons
# * Armor

def get_item(item_or_block_id):
    """
    Get the Block or Item with the specified id, which must either be an instance
    of BlockID, or a string format BlockID knows how to parse.
    """
    if not isinstance(item_or_block_id, BlockID):
        item_or_block_id = BlockID(str(item_or_block_id))
    if item_or_block_id.main >= G.ITEM_ID_MIN:
        return G.ITEMS_DIR[item_or_block_id]
    else:
        return G.BLOCKS_DIR[item_or_block_id]


class Item(object):
    id = None
    max_stack_size = 0
    amount_label_color = 255, 255, 255, 255
    name = "Item"
    group = None

    # How long can this item burn (-1 for non-fuel items)
    burning_time = -1
    # How long does it take to smelt this item (-1 for unsmeltable items)
    smelting_time = -1

    def __init__(self):
        self.id = BlockID(self.id)
        G.ITEMS_DIR[self.id] = self

    def on_right_click(self, world, player):
        pass

class ItemStack(object):
    def __init__(self, type = 0, amount = 1, durability = -1, data = 0):
        if amount < 1:
            amount = 1
        self.type = BlockID(type)
        self.amount = amount
        if durability == -1:
            self.durability = -1 if not hasattr(self.get_object(), 'durability') else self.get_object().durability
        else:
            self.durability = durability
        self.max_durability = get_item(type).durability if hasattr(get_item(type), 'durability') else -1
        self.data = data
        self.max_stack_size = get_item(type).max_stack_size

    # for debugging
    def __repr__(self):
        return '{ Item stack with type = ' + str(self.type) + ' }'

    def change_amount(self, change=0):
        overflow = 0
        if change != 0:
            self.amount += change
            if self.amount < 0:
                self.amount = 0
            elif self.amount > self.max_stack_size:
                overflow = self.amount - self.max_stack_size
                self.amount -= overflow

        return overflow

    # compatible with blocks
    @property
    def id(self):
        return self.type

    # compatible with blocks
    @property
    def name(self):
        return self.get_object().name

    def get_object(self):
        return get_item(self.id)

class CoalItem(Item):
    id = 263
    max_stack_size = 64
    name = "Coal"
    burning_time = 80

class LadderItem(Item):
    id = 999
    max_stack_size = 64
    name = "Ladder"

class DiamondItem(Item):
    id = 264
    max_stack_size = 64
    name = "Diamond"

class IronIngotItem(Item):
    id = 265
    max_stack_size = 64
    name = "Iron Ingot"

class GoldIngotItem(Item):
    id = 266
    max_stack_size = 64
    name = "Gold Ingot"

class StickItem(Item):
    id = 280
    max_stack_size = 64
    name = "Stick"
    burning_time = 5

class BreadItem(Item):
    id = 297
    max_stack_size = 64
    name = "Bread"
    regenerated_health = 3

class FlintItem(Item):
    id = 318
    max_stack_size = 64
    name = "Flint"

class YellowDyeItem(Item):
    id = 351
    max_stack_size = 64
    name = "Dandelion Yellow Dye"

class CactusGreenDyeItem(Item):
    id = 351,2
    max_stack_size = 64
    name = "Cactus Green Dye"

class RedDyeItem(Item):
    id = 351,1
    max_stack_size = 64
    name = "Red Dye"

class SugarItem(Item):
    id = 353
    max_stack_size = 64
    name = "Sugar"

class SeedItem(Item):
    id = 295
    max_stack_size = 64
    name = "Seed"

    def on_right_click(self, world, player):
        block, previous = world.hit_test(player.position, player.get_sight_vector(), player.attack_range)
        if previous:
            if world[block].id == farm_block.id: # plant wheat
                world.add_block(previous, wheat_crop_block)
                return True # remove from inventory

class WheatItem(Item):
    id = 296
    max_stack_size = 64
    name = "Wheat"

class PaperItem(Item):
    id = 339
    max_stack_size = 64
    name = "Cactus Green Dye"

class Tool(Item):
    material = None
    multiplier = 0
    tool_type = None

    def __init__(self):
        super(Tool, self).__init__()
        self.multiplier = 2 * (self.material + 1)

class WoodAxe(Tool):
    material = G.WOODEN_TOOL
    tool_type = G.AXE
    max_stack_size = 1
    id = 271
    durability = 20
    name = "Wooden Axe"

class StoneAxe(Tool):
    material = G.STONE_TOOL
    tool_type = G.AXE
    max_stack_size = 1
    id = 275
    durability = 40
    name = "Stone Axe"

class IronAxe(Tool):
    material = G.IRON_TOOL
    tool_type = G.AXE
    max_stack_size = 1
    id = 258
    durability = 60
    name = "Iron Axe"

class EmeraldAxe(Tool):
    material = G.IRON_TOOL
    tool_type = G.AXE
    max_stack_size = 1
    id = 258,1
    durability = 70
    name = "Emerald Axe"

class RubyAxe(Tool):
    material = G.IRON_TOOL
    tool_type = G.AXE
    max_stack_size = 1
    id = 258,2
    durability = 80
    name = "Ruby Axe"

class SapphireAxe(Tool):
    material = G.IRON_TOOL
    tool_type = G.AXE
    max_stack_size = 1
    id = 258,3
    durability = 80
    name = "Sapphire Axe"

class DiamondAxe(Tool):
    material = G.DIAMOND_TOOL
    tool_type = G.AXE
    max_stack_size = 1
    id = 279
    durability = 100
    name = "Diamond Axe"

class GoldenAxe(Tool):
    material = G.GOLDEN_TOOL
    tool_type = G.AXE
    max_stack_size = 1
    id = 286
    durability = 50
    name = "Golden Axe"

class WoodPickaxe(Tool):
    material = G.WOODEN_TOOL
    tool_type = G.PICKAXE
    max_stack_size = 1
    id = 270
    durability = 10
    name = "Wooden Pickaxe"

class StonePickaxe(Tool):
    material = G.STONE_TOOL
    tool_type = G.PICKAXE
    max_stack_size = 1
    id = 274
    durability = 30
    name = "Stone Pickaxe"

class IronPickaxe(Tool):
    material = G.IRON_TOOL
    tool_type = G.PICKAXE
    max_stack_size = 1
    id = 257
    durability = 40
    name = "Iron Pickaxe"

class EmeraldPickaxe(Tool):
    material = G.IRON_TOOL
    tool_type = G.PICKAXE
    max_stack_size = 1
    id = 257,1
    durability = 50
    name = "Emerald Pickaxe"

class RubyPickaxe(Tool):
    material = G.IRON_TOOL
    tool_type = G.PICKAXE
    max_stack_size = 1
    id = 257,2
    durability = 100
    name = "Ruby Pickaxe"

class SapphirePickaxe(Tool):
    material = G.IRON_TOOL
    tool_type = G.PICKAXE
    max_stack_size = 1
    id = 257,3
    durability = 200
    name = "Sapphire Pickaxe"

class DiamondPickaxe(Tool):
    material = G.DIAMOND_TOOL
    tool_type = G.PICKAXE
    max_stack_size = 1
    id = 278
    durability = 150
    name = "Diamond Pickaxe"

class GoldenPickaxe(Tool):
    material = G.GOLDEN_TOOL
    tool_type = G.PICKAXE
    max_stack_size = 1
    id = 285
    durability = 30
    name = "Golden Pickaxe"

class WoodShovel(Tool):
    material = G.WOODEN_TOOL
    tool_type = G.SHOVEL
    max_stack_size = 1
    id = 269
    durability = 10
    name = "Wooden Shovel"

class StoneShovel(Tool):
    material = G.STONE_TOOL
    tool_type = G.SHOVEL
    max_stack_size = 1
    id = 273
    durability = 30
    name = "Stone Shovel"

class IronShovel(Tool):
    material = G.IRON_TOOL
    tool_type = G.SHOVEL
    max_stack_size = 1
    id = 256
    durability = 70
    name = "Iron Shovel"

class EmeraldShovel(Tool):
    material = G.IRON_TOOL
    tool_type = G.SHOVEL
    max_stack_size = 1
    id = 256,1
    durability = 60
    name = "Emerald Shovel"

class RubyShovel(Tool):
    material = G.IRON_TOOL
    tool_type = G.SHOVEL
    max_stack_size = 1
    id = 256,2
    durability = 40
    name = "Ruby Shovel"

class SapphireShovel(Tool):
    material = G.IRON_TOOL
    tool_type = G.SHOVEL
    max_stack_size = 1
    id = 256,3
    durability = 70
    name = "Sapphire Shovel"

class DiamondShovel(Tool):
    material = G.DIAMOND_TOOL
    tool_type = G.SHOVEL
    max_stack_size = 1
    id = 277
    durability = 100
    name = "Diamond Shovel"

class GoldenShovel(Tool):
    material = G.GOLDEN_TOOL
    tool_type = G.SHOVEL
    max_stack_size = 1
    id = 284
    durability = 30
    name = "Golden Shovel"

class Hoe(Tool):
    def __init__(self):
        super(Hoe, self).__init__()

    def on_right_click(self, world, player):
        block, previous = world.hit_test(player.position, player.get_sight_vector(), player.attack_range)
        if previous:
            if world[block].id == dirt_block.id or world[block].id == grass_block.id:
                world.add_block(block, farm_block)

class WoodHoe(Hoe):
    material = G.WOODEN_TOOL
    tool_type = G.HOE
    max_stack_size = 1
    id = 290
    durability = 60
    name = "Wooden Hoe"

class StoneHoe(Hoe):
    material = G.STONE_TOOL
    tool_type = G.HOE
    max_stack_size = 1
    id = 291
    durability = 40
    name = "Stone Hoe"

class IronHoe(Hoe):
    material = G.IRON_TOOL
    tool_type = G.HOE
    max_stack_size = 1
    id = 292
    durability = 40
    name = "Iron Hoe"

class EmeraldHoe(Hoe):
    material = G.IRON_TOOL
    tool_type = G.HOE
    max_stack_size = 1
    id = 292,1
    durability = 50
    name = "Emerald Hoe"

class RubyHoe(Hoe):
    material = G.IRON_TOOL
    tool_type = G.HOE
    max_stack_size = 1
    id = 292,2
    durability = 60
    name = "Ruby Hoe"

class SapphireHoe(Hoe):
    material = G.IRON_TOOL
    tool_type = G.HOE
    max_stack_size = 1
    id = 292,3
    durability = 80
    name = "Sapphire Hoe"

class DiamondHoe(Hoe):
    material = G.DIAMOND_TOOL
    tool_type = G.HOE
    max_stack_size = 1
    id = 293
    durability = 100
    name = "Diamond Hoe"

class GoldenHoe(Hoe):
    material = G.GOLDEN_TOOL
    tool_type = G.HOE
    max_stack_size = 1
    id = 294
    durability = 100
    name = "Golden Hoe"

class Armor(Item):
    material = None
    defense_point = 0
    armor_type = None
    max_stack_size = 1

    def __init__(self):
        super(Armor, self).__init__()

class IronHelmet(Armor):
    material = G.IRON_TOOL
    defense_point = 1
    armor_type = G.HELMET
    id = 306
    name = "Iron Helmet"

class IronChestplate(Armor):
    material = G.IRON_TOOL
    defense_point = 3
    armor_type = G.CHESTPLATE
    id = 307
    name = "Iron Chestplate"

class IronLeggings(Armor):
    material = G.IRON_TOOL
    defense_point = 2.5
    armor_type = G.LEGGINGS
    id = 308
    name = "Iron Leggings"

class IronBoots(Armor):
    material = G.IRON_TOOL
    defense_point = 1
    armor_type = G.BOOTS
    id = 309
    name = "Iron Boots"

##Emerald Armor .. Pretty much re-textured Iron armor (from Tekkit)

#class EmeraldHelmet(Armor):
    #material = globals.IRON_TOOL
    #defense_point = 1
    #armor_type = globals.HELMET
    #id = 306.1
    #name = "Emerald Helmet"

#class EmeraldChestplate(Armor):
    #material = globals.IRON_TOOL
    #defense_point = 3
    #armor_type = globals.CHESTPLATE
    #id = 307.1
    #name = "Emerald Chestplate"

#class EmeraldLeggings(Armor):
    #material = globals.IRON_TOOL
    #defense_point = 2.5
    #armor_type = globals.LEGGINGS
    #id = 308.1
    #name = "Emerald Leggings"

#class EmeraldBoots(Armor):
    #material = globals.IRON_TOOL
    #defense_point = 1
    #armor_type = globals.BOOTS
    #id = 309.1
    #name = "Emerald Boots"

coal_item = CoalItem()
diamond_item = DiamondItem()
stick_item = StickItem()
iron_ingot_item = IronIngotItem()
gold_ingot_item = GoldIngotItem()
flint_item = FlintItem()
wood_axe = WoodAxe()
stone_axe = StoneAxe()
iron_axe = IronAxe()
diamond_axe = DiamondAxe()
golden_axe = GoldenAxe()
emerald_axe = EmeraldAxe()
wood_pickaxe = WoodPickaxe()
stone_pickaxe = StonePickaxe()
iron_pickaxe = IronPickaxe()
diamond_pickaxe = DiamondPickaxe()
golden_pickaxe = GoldenPickaxe()
emerald_pickaxe = EmeraldPickaxe()
wood_shovel = WoodShovel()
stone_shovel = StoneShovel()
iron_shovel = IronShovel()
diamond_shovel = DiamondShovel()
golden_shovel = GoldenShovel()
emerald_shovel = EmeraldShovel()
emerald_hoe = EmeraldHoe()
wood_hoe = WoodHoe()
stone_hoe = StoneHoe()
iron_hoe = IronHoe()
diamond_hoe = DiamondHoe()
golden_hoe = GoldenHoe()
iron_helmet = IronHelmet()
iron_chestplate = IronChestplate()
iron_leggings = IronLeggings()
iron_boots = IronBoots()
#emerald_helmet = EmeraldHelmet()
#emerald_chestplace = EmeraldChestplate()
#emerald_leggings = EmeraldLeggings()
#emerald_boots = EmeraldBoots()
yellowdye_item = YellowDyeItem()
ladder_item = LadderItem()
ruby_pickaxe = RubyPickaxe()
ruby_shovel = RubyShovel()
ruby_axe = RubyAxe()
ruby_hoe = RubyHoe()
sapphire_pickaxe = SapphirePickaxe()
sapphire_shovel = SapphireShovel()
sapphire_axe = SapphireAxe()
sapphire_hoe = SapphireHoe()
ladder_item = LadderItem()
reddye_item = RedDyeItem()
sugar_item = SugarItem()
paper_item = PaperItem()
seed_item = SeedItem()
wheat_item = WheatItem()
bread_item = BreadItem()
