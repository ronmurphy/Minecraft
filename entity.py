# Imports, sorted alphabetically.

# Python packages
# Nothing for now...

# Third-party packages
# Nothing for now...

# Modules from this project
# Nothing for now...
import globals as G


__all__ = (
    'Entity', 'TileEntity', 'WheatCropEntity', 'FurnaceEntity',
)


class Entity(object):
    """
    Base class for players, mobs, TNT and so on.
    """
    def __init__(self, position, rotation, velocity=0, health=0, max_health=0,
                 attack_power=0, sight_range=0, attack_range=0):
        self.position = position
        self.rotation = rotation
        self.velocity = velocity
        self.health = health
        self.max_health = max_health
        # Attack power in hardness per second.  We will probably need to change
        # that later to include equiped weapon etc.
        self.attack_power = attack_power
        # Sight range is currently unusued - we probably want
        # it to check if monsters can see player
        self.sight_range = sight_range
        self.attack_range = attack_range

class TileEntity(Entity):
    """
    A Tile entity is extra data associated with a block
    """
    def __init__(self, world, position):
        super(TileEntity, self).__init__(position, rotation=(0,0))
        self.world = world

class WheatCropEntity(TileEntity):
    # seconds per stage
    grow_time = 10
    grow_task = None
    
    def __init__(self, world, position):
        super(WheatCropEntity, self).__init__(world, position)
        self.grow_task = G.main_timer.add_task(self.grow_time, self.grow_callback)

    def __del__(self):
        if self.grow_task is not None:
            G.main_timer.remove_task(self.grow_task)
        if self.world is None:
            return
        if self.position in self.world:
            self.world.hide_block(self.position)

    def grow_callback(self):
        if self.position in self.world:
            self.world[self.position].growth_stage = self.world[self.position].growth_stage + 1
            self.world.hide_block(self.position)
            self.world.show_block(self.position)
        else:
            # the block ceased to exist
            return
        if self.world[self.position].growth_stage < 7:
            self.grow_task = G.main_timer.add_task(self.grow_time, self.grow_callback)
        else:
            self.grow_task = None

class FurnaceEntity(TileEntity):
    fuel = None
    smelt_stack = None
    outcome_item = None
    smelt_outcome = None # output slot

    fuel_task = None
    smelt_task = None

    outcome_callback = None
    fuel_callback = None

    def __del__(self):
        if self.fuel_task is not None:
            G.main_timer.remove_task(self.fuel_task)
        if self.smelt_task is not None:
            G.main_timer.remove_task(self.smelt_task)

    def full(self, reserve=0):
        if self.smelt_outcome is None:
            return False

        return self.smelt_outcome.get_object().max_stack_size < self.smelt_outcome.amount + reserve

    def full(self, reserve=0):
        if self.smelt_outcome is None:
            return False

        return self.smelt_outcome.get_object().max_stack_size < self.smelt_outcome.amount + reserve


    def smelt_done(self):
        self.smelt_task = None
        # outcome
        if self.smelt_outcome is None:
            self.smelt_outcome = self.outcome_item
        else:
            self.smelt_outcome.change_amount(self.outcome_item.amount)
        # cost
        self.smelt_stack.change_amount(-1)
        # input slot has been empty
        if self.smelt_stack.amount <= 0:
            self.smelt_stack = None
            self.outcome_item = None
        if self.outcome_callback is not None:
            if callable(self.outcome_callback):
                self.outcome_callback()
        # stop
        if self.smelt_stack is None:
            return
        if self.full(self.outcome_item.amount):
            return
        if self.fuel is None or self.fuel_task is None:
            return
        # smelting task
        self.smelt_task = G.main_timer.add_task(self.smelt_stack.get_object().smelting_time, self.smelt_done)

    def remove_fuel(self):
        if self.fuel_callback is not None:
            if callable(self.fuel_callback):
                self.fuel_callback()
        self.fuel_task = None
        self.fuel.change_amount(-1)
        if self.fuel.amount <= 0:
            self.fuel = None
            # stop smelting task
            if self.smelt_task is not None:
                G.main_timer.remove_task(self.smelt_task)
            self.smelt_task = None
            return

        # continue
        if self.smelt_task is not None:
            self.fuel_task = G.main_timer.add_task(self.fuel.get_object().burning_time, self.remove_fuel)

    def smelt(self):
        if self.fuel is None or self.smelt_stack is None:
            return
        # smelting
        if self.fuel_task is not None or self.smelt_task is not None:
            return
        if self.full():
            return

        burning_time = self.fuel.get_object().burning_time
        smelting_time = self.smelt_stack.get_object().smelting_time
        # fuel task: remove fuel
        self.fuel_task = G.main_timer.add_task(burning_time, self.remove_fuel)
        # smelting task
        self.smelt_task = G.main_timer.add_task(smelting_time, self.smelt_done)
