# from pudb import set_trace
"""CS 61A presents Ants Vs. SomeBees."""

#what is implemented: class will be initialized in gameplay iftrue
#what does calling Insect.__init__(self, armor) do?
# what is the function of make_test_assault_plan
import random
from ucb import main, interact, trace
from collections import OrderedDict

################
# Core Classes #
# ################
# Problem 2 (2 pt)

# Complete the Place constructor by adding code that tracks entrances. 
#Right now, a Place keeps track only of its exit. We would like a Place to keep track of its entrance 
#as well. A Place needs to track only one entrance. Tracking entrances will be useful when an 
#Ant needs to see what Bees are in front of it in the tunnel.

# However, simply passing an entrance to a Place constructor will be problematic; 
#we would need to have both the exit and the entrance before creating a Place! 
#(It's a chicken or the egg problem.) To get around this problem, we will keep track of entrances in the
#following way instead. The Place constructor should specify that:

#     A newly created Place always starts with its entrance as None.
#     If the Place has an exit, then the exit's entrance is set to that Place.

#Hint: Remember that when inside the definition of an __init__ method, 
#the name self is bound to the newly created object.

#Hint: Try drawing out two Places next to each other if things get confusing. 
#In the GUI, a place's entrance is to its right while the exit is to its left.

#requirments:
#     A newly created Place always starts with its entrance as None.
#     If the Place has an exit, then the exit's entrance is set to that Place.

class Place(object):
    """A Place holds insects and has an exit to another Place."""

    def __init__(self, name, exit=None):
        """Create a Place with the given NAME and EXIT.

        name -- A string; the name of this Place.
        exit -- The Place reached by exiting this Place (may be None).
        """
        self.name = name
        self.exit = exit
        self.bees = []        # A list of Bees
        self.ant = None       # An Ant
        self.entrance = None  # A Place
        # Phase 1: Add an entrance to the exit
        # BEGIN Problem 2
        "*** YOUR CODE HERE ***"
        #     If the Place has an exit, then the exit's entrance is set to that Place.
        if self.exit:
            self.exit.entrance = self

        # END Problem 2

    def add_insect(self, insect):
        """Add an Insect to this Place.

        There can be at most one Ant in a Place, unless exactly one of them is
        a container ant (Problem 9), in which case there can be two. If add_insect
        tries to add more Ants than is allowed, an assertion error is raised.

        There can be any number of Bees in a Place.
        """
        if insect.is_ant:
            if self.ant is None:
                self.ant = insect
            else:
                # BEGIN Problem 9
                assert self.ant is None, 'Two ants in {0}'.format(self)
                # END Problem 9
        else:
            self.bees.append(insect)
        insect.place = self

    def remove_insect(self, insect):
        """Remove an INSECT from this Place.

        A target Ant may either be directly in the Place, or be contained by a
        container Ant at this place. The true QueenAnt may not be removed. If
        remove_insect tries to remove an Ant that is not anywhere in this
        Place, an AssertionError is raised.

        A Bee is just removed from the list of Bees.
        """
        if insect.is_ant:
            # Special handling for QueenAnt
            # BEGIN Problem 13
            "*** YOUR CODE HERE ***"
            # END Problem 13

            # Special handling for container ants
            if self.ant is insect:
                # Bodyguard was removed. Contained ant should remain in the game
                if hasattr(self.ant, 'is_container') and self.ant.is_container:
                    self.ant = self.ant.contained_ant
                else:
                    self.ant = None
            else:
                # Contained ant was removed. Bodyguard should remain
                if hasattr(self.ant, 'is_container') and self.ant.is_container \
                        and self.ant.contained_ant is insect:
                    self.ant.contained_ant = None
                else:
                    assert False, '{0} is not in {1}'.format(insect, self)
        else:
            self.bees.remove(insect)

        insect.place = None

    def __str__(self):
        return self.name


class Insect(object):
    """An Insect, the base class of Ant and Bee, has armor and a Place."""

    is_ant = False
    damage = 0
    # ADD CLASS ATTRIBUTES HERE

    def __init__(self, armor, place=None):
        """Create an Insect with an ARMOR amount and a starting PLACE."""
        self.armor = armor
        self.place = place  # set by Place.add_insect and Place.remove_insect

    def reduce_armor(self, amount):
        """Reduce armor by AMOUNT, and remove the insect from its place if it
        has no armor remaining.

        >>> test_insect = Insect(5)
        >>> test_insect.reduce_armor(2)
        >>> test_insect.armor
        3
        """
        self.armor -= amount
        if self.armor <= 0:
            self.place.remove_insect(self)

    def action(self, colony):
        """The action performed each turn.

        colony -- The AntColony, used to access game state information.
        """

    def __repr__(self):
        cname = type(self).__name__
        return '{0}({1}, {2})'.format(cname, self.armor, self.place)


class Bee(Insect):
    """A Bee moves from place to place, following exits and stinging ants."""

    name = 'Bee'
    damage = 1
    # OVERRIDE CLASS ATTRIBUTES HERE


    def sting(self, ant):
        """Attack an ANT, reducing its armor by 1."""
        ant.reduce_armor(self.damage)

    def move_to(self, place):
        """Move from the Bee's current Place to a new PLACE."""
        self.place.remove_insect(self)
        place.add_insect(self)


    def blocked(self):
        """Return True if this Bee cannot advance to the next Place."""
        # Phase 4: Special handling for NinjaAnt:
            #DONE: Bee.blocked should return False if there is no Ant in Bee's place 
            #OR if there is an ant:
            #Bee.blocks_path should return False if ant.blocks_path is False

        # BEGIN Problem 7
            #Bee.blocked should return False if there is no Ant in Bee's place 
        if not self.place.ant or self.place.ant.blocks_path == False:
            return False

        return self.place.ant is not None
        # END Problem 7

    def action(self, colony):
        """A Bee's action stings the Ant that blocks its exit if it is blocked,
        or moves to the exit of its current place otherwise.

        colony -- The AntColony, used to access game state information.
        """
        destination = self.place.exit
        # Extra credit: Special handling for bee direction
        # BEGIN EC
        "*** YOUR CODE HERE ***"
        # END EC
        if self.blocked():
            self.sting(self.place.ant)
        elif self.armor > 0 and destination is not None:
            self.move_to(destination)


class Ant(Insect):
    """An Ant occupies a place and does work for the colony."""

    is_ant = True
    implemented = False  # Only implemented Ant classes should be instantiated
    food_cost = 0
    blocks_path = True
    # ADD CLASS ATTRIBUTES HERE

    def __init__(self, armor=1):
        """Create an Ant with an ARMOR quantity."""
        Insect.__init__(self, armor)

    def can_contain(self, other):
        # BEGIN Problem 9
        "*** YOUR CODE HERE ***"
        # END Problem 9

#problem 1
#Now that deploying Ants cost food, we need to be able gather more food! 
#To fix this issue, implement the HarvesterAnt class.
#A HarvesterAnt is a type of Ant that adds one food to the colony.food total as its action.

#requirments: HarvesterAnt.action() should increment colony.food 
class HarvesterAnt(Ant):
    """HarvesterAnt produces 1 additional food per turn for the colony."""

    name = 'Harvester'
    implemented = True
    # OVERRIDE CLASS ATTRIBUTES HERE
    food_cost = 2
    armor = 1

    def action(self, colony):
        """Produce 1 additional food for the COLONY.

        colony -- The AntColony, used to access game state information.
        """
        # BEGIN Problem 1
        "*** YOUR CODE HERE ***"
        colony.food += 1
        # END Problem 1

# Problem 3 (1 pt)

# In order for a ThrowerAnt to attack, it must know which bee it should hit. 
#The provided implementation of the nearest_bee method in the ThrowerAnt class only allows them 
#to hit bees in the same Place. Your job is to fix it so that a ThrowerAnt will throw_at the 
#nearest bee in front of it that is not still in the Hive.

# The nearest_bee method returns a random Bee from the nearest place that contains bees. 
#Places are inspected in order by following their entrance attributes.

#     Start from the current Place of the ThrowerAnt.
#     For each place, return a random bee if there is any, or consider the next place that 
#     is stored as the current place's entrance.
#     If there is no bee to attack, return None.

# Hint: The random_or_none function provided in ants.py returns a random element of a sequence or None if the sequence is empty.

#requirments:
#base:
    #nearest_bee should return None if place is Hive
    #if there are more than 0 bees in place nearest_bee should return a random bee in place 
#recursive:
    #nearest_bee(place.entrance)
class ThrowerAnt(Ant):
    """ThrowerAnt throws a leaf each turn at the nearest Bee in its range."""

    name = 'Thrower'
    implemented = True
    damage = 1
    # ADD/OVERRIDE CLASS ATTRIBUTES HERE
    food_cost = 3
    armor = 1
    max_range = float("inf") #sets max_range to infinity
    min_range = 0

    def nearest_bee(self, hive):
        """Return the nearest Bee in a Place that is not the HIVE, connected to
        the ThrowerAnt's Place by following entrances.

        This method returns None if there is no such Bee (or none in range).
        """
        # BEGIN Problem 3 and 4
        def find_nearest_place(place, transition_num):
            #to account for min/max throwing constraints
            if transition_num > self.max_range:
                return None
            if transition_num < self.min_range: #skip to next recursive call if not in min_range
                return find_nearest_place(place.entrance, transition_num + 1)
            if transition_num == 4:                             #skip to next recursive call if 4
                return find_nearest_place(place.entrance, transition_num + 1)

            #should return None if place is Hive
            if place.name == "Hive":
                return None
            #if there are more than 0 bees in place, it should return a random bee in place
            result_random_or_none = random_or_none(place.bees) 
            if result_random_or_none == None:
                return find_nearest_place(place.entrance, transition_num + 1)
            else:
                return result_random_or_none
        return find_nearest_place(self.place,0)
        # END Problem 3 and 4

    def throw_at(self, target):
        """Throw a leaf at the TARGET Bee, reducing its armor."""
        if target is not None:
            target.reduce_armor(self.damage)

    def action(self, colony):
        """Throw a leaf at the nearest Bee in range."""
        self.throw_at(self.nearest_bee(colony.hive))

def random_or_none(s):
    """Return a random element of sequence S, or return None if S is empty."""
    if s:
        return random.choice(s)

##############
# Extensions #
##############


# Problem 4 (2 pt)

# The ThrowerAnt is a great offensive unit, but it'd be nice to have a cheaper unit that can throw. 
#Implement two subclasses of ThrowerAnt that are less costly but have constraints on the distance they can throw:

#The LongThrower can only throw_at a Bee that is found after following at least 5 entrance transitions. 
#It cannot hit Bees that are in the same Place as it or the first 4 Places in front of it. 
#If there are two Bees, one too close to the LongThrower and the other within its range, 
#the LongThrower should throw past the closer Bee, instead targeting the farther one, which is within its range.


#The ShortThrower can only throw_at a Bee that is found after following at most 3 entrance transitions. 
#It cannot throw at any ants further than 3 Places in front of it.

# Neither of these specialized throwers can throw_at a Bee that is exactly 4 Places away. 
#Placing a single one of these (and no other ants) should never win a default game.

# Class   Food Cost   Armor

# ShortThrower    2   1

# LongThrower     2   1

# A good way to approach the implementation to ShortThrower and LongThrower is to have 
#it inherit the nearest_bee method from the base ThrowerAnt class. 
#The logic of choosing which bee a thrower ant will attack is essentially the same, 
#except the ShortThrower and LongThrower ants have maximum and minimum ranges, respectively.

# To implement these behaviors, you may need to modify the nearest_bee method 
#to reference min_range and max_range attributes, and only return a bee that is in range.

# The original ThrowerAnt has no minimum or maximum range, 
#so make sure that its min_range and max_range attributes should reflect that. 
#Then, implement the subclasses LongThrower and ShortThrower with appropriately constrained ranges and correct food costs.

#Hint: float('inf') returns an infinite positive value represented as a float that can be compared with other numbers.

#Don't forget to set the implemented class attribute of LongThrower and ShortThrower to True.

#requirements:

#DONE: LongThrower food_cost = 2, armor = 1
#DONE: LongThrower should only be able to throw_at a bee after moving at least 5 entrance transitions
    # DONE: LongThrower min_range = 4
    #DONE: LongThrower max_range = infinity?
#LongThrower should not hit bees in the same place as it is
#LongThrower should not hit bees exactly 4 places in front of it
#LongThrower should throw at bee farther away if there is one bee too close, and one bee father but within range
#LongThrower should inherit the nearest_bee method from the ThrowerAnt class
#LongThrower implemented should be True

#ShortThrower food_cost = 2, armor = 1
#ShortThrower should only throw at a bee within 3 entrance transitions
    #ShortThrower max_range = 3
    #ShortThrower min_range = 0
#ShortThrower should not hit bees exactly 4 places in front of it
#ShortThrower should inherit the nearest_bee method from the ThrowerAnt class

#ShortThrower implemented should be True
 
#DONE: ThrowerAnt should have max_range = infinity float("inf") and min range 0

#DONE: ThrowerAnt nearest_bee should only return bee within min_range and max_range



class ShortThrower(ThrowerAnt):
    """A ThrowerAnt that only throws leaves at Bees at most 3 places away."""

    name = 'Short'
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem 4
    implemented = True   # Change to True to view in the GUI
    food_cost = 2
    armor = 1
    max_range = 3
    # END Problem 4

class LongThrower(ThrowerAnt):
    """A ThrowerAnt that only throws leaves at Bees at least 5 places away."""

    name = 'Long'
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem 4
    implemented = True   # Change to True to view in the GUI
    food_cost = 2
    armor = 1
    min_range = 4




    # END Problem 4


# Problem 5 (2 pt)

# Implement the FireAnt, which damages all the bees in the same place as itself when it dies. 
#To implement this, we have to override the FireAnt's reduce_armor method.
# Normally, Insect.reduce_armor will decrement the insect's armor by the given amount 
#and remove the insect from its place if armor reaches zero or lower. 
#However, if a FireAnt's armor reaches zero or lower,
# it will reduce the armor of all Bees in its place by its damage attribute 
#(defaults to 3) before being removed from its place.

# Class   Food Cost   Armor
# FireAnt     5   1

#     Hint: To damage a Bee, call the reduce_armor method inherited from Insect.

#Hint: Damaging a bee may cause it to be removed from its place. 

#If you iterate over a list, but change the contents of that list at the same time, 
#you may not visit all the elements. This can be prevented by making a copy of the list. 
#You can either use a list slice, or use the built-in list function.

#      >>> lst = [1,2,3,4]
#      >>> lst[:]
#      [1, 2, 3, 4]
#      >>> list(lst)
#      [1, 2, 3, 4]
#      >>> lst[:] is not lst and list(lst) is not lst
#      True

#requirments:
#DONE: it should override reduce_armor method
#DONE: FireAnt.reduce_armor should reduce armor of all bees in fireants place by fireant.dammange if armor <=0
    #DONE: FireAnt should itterate over copy of place.bees
#DONE: Fireant should be removed from its place if armor <= 0

#DONE: FireAnt.food_cost should equal 5
#DONE: FireAnt.armor should equal 1

class FireAnt(Ant):
    """FireAnt cooks any Bee in its Place when it expires."""

    name = 'Fire'
    damage = 3
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem 5
    implemented = True   # Change to True to view in the GUI
    #FireAnt.food_cost should equal 5
    food_cost = 5
    #FireAnt.armor should equal 1

    armor = 1
    # END Problem 5

    def reduce_armor(self, amount):
        """Reduce armor by AMOUNT, and remove the FireAnt from its place if it
        has no armor remaining. If the FireAnt dies, damage each of the bees in
        the current place.
        """
        # BEGIN Problem 5
        "*** YOUR CODE HERE ***"
        #FireAnt.reduce_armor should reduce armor of all bees in fireants place by fireant.dammange if armor <=0
        
        #if armor <=0
        if self.armor - amount <= 0:
            #FireAnt should itterate over copy of place.bees
            bees_copy = self.place.bees[:]

            for bee in bees_copy:
                #FireAnt.reduce_armor should reduce armor of all bees in fireants place by 
                #fireant.dammange 
                bee.reduce_armor(self.damage)

        #Fireant should remove itself
        Insect.reduce_armor(self,amount)


        # END Problem 5

# Problem 6 (2 pt)

# Implement the HungryAnt, which will select a random Bee from its place and eat it whole. 
#After eating a Bee, it must spend 3 turns digesting before eating again. 
#If there is no bee available to eat, it will do nothing.

# Class   Food Cost   Armor

# HungryAnt   4   1

# Give HungryAnt a time_to_digest class attribute that holds the number of turns that it 
#takes a HungryAnt to digest (default to 3). Also, give each HungryAnt an instance 
#attribute digesting that counts the number of turns it has left to digest 
#(default is 0, since it hasn't eaten anything at the beginning).

# Implement the action method of the HungryAnt to check if it's digesting;
# if so, decrement its digesting counter. Otherwise, eat a random Bee in its place by 
#reducing the Bee's armor to 0 and restart the digesting timer.

#requirments
#DONE: HungryAnt should have time_to_digest class attribute default 3
#DONE:HungryAnt should have instance attribute digesting default 0

#action should decriment digesting if it is digesting
#action should eat a random bee in self.place if not digesting
    #eat should be acheived by setting bee's armor to 0

class HungryAnt(Ant):
    """HungryAnt will take three turns to digest a Bee in its place.
    While digesting, the HungryAnt can't eat another Bee.
    """
    name = 'Hungry'
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem 6
    implemented = True   # Change to True to view in the GUI
    #HungryAnt should have time_to_digest class attribute default 3
    time_to_digest = 3
    food_cost = 4

    # END Problem 6

    def __init__(self, armor=1, digesting=0):
        # BEGIN Problem 6
        "*** YOUR CODE HERE ***"
        Ant.__init__(self)
        self.armor = armor
        #HungryAnt should have instance attribute digesting default 0
        self.digesting = digesting


        # END Problem 6

    def eat_bee(self, bee):
        # BEGIN Problem 6
        "*** YOUR CODE HERE ***"
        bee.reduce_armor(bee.armor)
        self.digesting = self.time_to_digest
        # END Problem 6

    def action(self, colony):
        # BEGIN Problem 6
        "*** YOUR CODE HERE ***"
        #action should decriment digesting if it is digesting
        if self.digesting > 0:
            self.digesting -= 1
        else:
            random_bee = random_or_none(self.place.bees)
            if random_bee:
                self.eat_bee(random_or_none(self.place.bees))
        # END Problem 6



# Problem 7 (2 pt)

# Implement the NinjaAnt, which damages all Bees that pass by, but can never be stung.
# Class   Food Cost   Armor

# NinjaAnt    5   1

# A NinjaAnt does not block the path of a Bee that flies by. 
#To implement this behavior, first modify the Ant class to include a new class attribute blocks_path that is True by default.
# Set the value of blocks_path to False in the NinjaAnt class.

# Second, modify the Bee's method blocked to return False if either there is no Ant in the Bee's place 
#or if there is an Ant, but its blocks_path attribute is False. Now Bees will just fly past NinjaAnts.

# Finally, we want to make the NinjaAnt damage all Bees that fly past.
# Implement the action method in NinjaAnt to reduce the armor of all Bees in the same place as the NinjaAnt 
#by its damage attribute. Similar to the FireAnt, you must iterate over a list of bees that may change.

#DONE: NinvaAnt should have food_cost = 5
#DONE: CfNinjaAnt should have armor = 1

#DONE: Ant should have blocks_path default True
#DONE: NinjaAnt should have blocks_paths = False

#DONE: Bee.blocked should return False if there is no Ant in Bee's place 
#OR if there is an ant:
#DONE: Bee.blocks_path should return False if ant.blocks_path is False


#DONE: NinjaAnt.action should reduce armor of all bees in place by dammage




class NinjaAnt(Ant):
    """NinjaAnt does not block the path and damages all bees in its place."""

    name = 'Ninja'
    damage = 1
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem 7
    implemented = True   # Change to True to view in the GUI
    food_cost = 5
    armor = 1
    blocks_path = False

    # END Problem 7

    def action(self, colony):
        # BEGIN Problem 7
        "*** YOUR CODE HERE ***"

        #NinjaAnt should itterate over copy of place.bees
        bees_copy = self.place.bees[:]

        for bee in bees_copy:
            #NinjaAnt.reduce_armor should reduce armor of all bees in fireants place by 
            #fireant.damange 
            bee.reduce_armor(self.damage)

        # END Problem 7

# BEGIN Problem 8
# The WallAnt class
# END Problem 8

class BodyguardAnt(Ant):
    """BodyguardAnt provides protection to other Ants."""

    name = 'Bodyguard'
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem 9
    implemented = False   # Change to True to view in the GUI
    # END Problem 9

    def __init__(self, armor=2):
        Ant.__init__(self, armor)
        self.contained_ant = None  # The Ant hidden in this bodyguard

    def contain_ant(self, ant):
        # BEGIN Problem 9
        "*** YOUR CODE HERE ***"
        # END Problem 9

    def action(self, colony):
        # BEGIN Problem 9
        "*** YOUR CODE HERE ***"
        # END Problem 9



class TankAnt(BodyguardAnt):
    """TankAnt provides both offensive and defensive capabilities."""

    name = 'Tank'
    damage = 1
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem 10
    implemented = False   # Change to True to view in the GUI
    # END Problem 10

    def action(self, colony):
        # BEGIN Problem 10
        "*** YOUR CODE HERE ***"
        # END Problem 10

class Water(Place):
    """Water is a place that can only hold watersafe insects."""

    def add_insect(self, insect):
        """Add an Insect to this place. If the insect is not watersafe, reduce
        its armor to 0."""
        # BEGIN Problem 11
        "*** YOUR CODE HERE ***"
        # END Problem 11

# BEGIN Problem 12
# The ScubaThrower class
# END Problem 12

# BEGIN Problem 13
class QueenAnt(Ant):  # You should change this line
# END Problem 13
    """The Queen of the colony. The game is over if a bee enters her place."""

    name = 'Queen'
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem 13
    implemented = False   # Change to True to view in the GUI
    # END Problem 13

    def __init__(self, armor=1):
        # BEGIN Problem 13
        "*** YOUR CODE HERE ***"
        # END Problem 13

    def action(self, colony):
        """A queen ant throws a leaf, but also doubles the damage of ants
        in her tunnel.

        Impostor queens do only one thing: reduce their own armor to 0.
        """
        # BEGIN Problem 13
        "*** YOUR CODE HERE ***"
        # END Problem 13

    def reduce_armor(self, amount):
        """Reduce armor by AMOUNT, and if the True QueenAnt has no armor
        remaining, signal the end of the game.
        """
        # BEGIN Problem 13
        "*** YOUR CODE HERE ***"
        # END Problem 13

class AntRemover(Ant):
    """Allows the player to remove ants from the board in the GUI."""

    name = 'Remover'
    implemented = False

    def __init__(self):
        Ant.__init__(self, 0)


##################
# Status Effects #
##################

def make_slow(action, bee):
    """Return a new action method that calls ACTION every other turn.

    action -- An action method of some Bee
    """
    # BEGIN Problem EC
    "*** YOUR CODE HERE ***"
    # END Problem EC

def make_scare(action, bee):
    """Return a new action method that makes the bee go backwards.

    action -- An action method of some Bee
    """
    # BEGIN Problem EC
    "*** YOUR CODE HERE ***"
    # END Problem EC

def apply_effect(effect, bee, duration):
    """Apply a status effect to a BEE that lasts for DURATION turns."""
    # BEGIN Problem EC
    "*** YOUR CODE HERE ***"
    # END Problem EC


class SlowThrower(ThrowerAnt):
    """ThrowerAnt that causes Slow on Bees."""

    name = 'Slow'
    # BEGIN Problem EC
    implemented = False   # Change to True to view in the GUI
    # END Problem EC

    def throw_at(self, target):
        if target:
            apply_effect(make_slow, target, 3)


class ScaryThrower(ThrowerAnt):
    """ThrowerAnt that intimidates Bees, making them back away instead of advancing."""

    name = 'Scary'
    # BEGIN Problem EC
    implemented = False   # Change to True to view in the GUI
    # END Problem EC

    def throw_at(self, target):
        # BEGIN Problem EC
        "*** YOUR CODE HERE ***"
        # END Problem EC

class LaserAnt(ThrowerAnt):
    # This class is optional. Only one test is provided for this class.

    name = 'Laser'
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem OPTIONAL
    implemented = False   # Change to True to view in the GUI
    # END Problem OPTIONAL

    def __init__(self, armor=1):
        ThrowerAnt.__init__(self, armor)
        self.insects_shot = 0

    def insects_in_front(self, hive):
        # BEGIN Problem EC
        return {}
        # END Problem EC

    def calculate_damage(self, distance):
        # BEGIN Problem EC
        return 0
        # END Problem EC

    def action(self, colony):
        insects_and_distances = self.insects_in_front(colony.hive)
        for insect, distance in insects_and_distances.items():
            damage = self.calculate_damage(distance)
            insect.reduce_armor(damage)
            if damage:
                self.insects_shot += 1


##################
# Bees Extension #
##################

class Wasp(Bee):
    """Class of Bee that has higher damage."""
    name = 'Wasp'
    damage = 2

class Hornet(Bee):
    """Class of bee that is capable of taking two actions per turn, although
    its overall damage output is lower. Immune to status effects.
    """
    name = 'Hornet'
    damage = 0.25

    def action(self, colony):
        for i in range(2):
            if self.armor > 0:
                super().action(colony)

    def __setattr__(self, name, value):
        if name != 'action':
            object.__setattr__(self, name, value)

class NinjaBee(Bee):
    """A Bee that cannot be blocked. Is capable of moving past all defenses to
    assassinate the Queen.
    """
    name = 'NinjaBee'

    def blocked(self):
        return False

class Boss(Wasp, Hornet):
    """The leader of the bees. Combines the high damage of the Wasp along with
    status effect immunity of Hornets. Damage to the boss is capped up to 8
    damage by a single attack.
    """
    name = 'Boss'
    damage_cap = 8
    action = Wasp.action

    def reduce_armor(self, amount):
        super().reduce_armor(self.damage_modifier(amount))

    def damage_modifier(self, amount):
        return amount * self.damage_cap/(self.damage_cap + amount)

class Hive(Place):
    """The Place from which the Bees launch their assault.

    assault_plan -- An AssaultPlan; when & where bees enter the colony.
    """

    def __init__(self, assault_plan):
        self.name = 'Hive'
        self.assault_plan = assault_plan
        self.bees = []
        for bee in assault_plan.all_bees:
            self.add_insect(bee)
        # The following attributes are always None for a Hive
        self.entrance = None
        self.ant = None
        self.exit = None

    def strategy(self, colony):
        exits = [p for p in colony.places.values() if p.entrance is self]
        for bee in self.assault_plan.get(colony.time, []):
            bee.move_to(random.choice(exits))
            colony.active_bees.append(bee)


class AntColony(object):
    """An ant collective that manages global game state and simulates time.

    Attributes:
    time -- elapsed time
    food -- the colony's available food total
    queen -- the place where the queen resides
    places -- A list of all places in the colony (including a Hive)
    bee_entrances -- A list of places that bees can enter
    """

    def __init__(self, strategy, hive, ant_types, create_places, dimensions, food=2):
        """Create an AntColony for simulating a game.

        Arguments:
        strategy -- a function to deploy ants to places
        hive -- a Hive full of bees
        ant_types -- a list of ant constructors
        create_places -- a function that creates the set of places
        dimensions -- a pair containing the dimensions of the game layout
        """
        self.time = 0
        self.food = food
        self.strategy = strategy
        self.hive = hive
        self.ant_types = OrderedDict((a.name, a) for a in ant_types)
        self.dimensions = dimensions
        self.active_bees = []
        self.configure(hive, create_places)

    def configure(self, hive, create_places):
        """Configure the places in the colony."""
        self.queen = QueenPlace('AntQueen')
        self.places = OrderedDict()
        self.bee_entrances = []
        def register_place(place, is_bee_entrance):
            self.places[place.name] = place
            if is_bee_entrance:
                place.entrance = hive
                self.bee_entrances.append(place)
        register_place(self.hive, False)
        create_places(self.queen, register_place, self.dimensions[0], self.dimensions[1])

    #draws an ASCII diagram of the colony (alpha version)
    def draw(self):
        def get_place(tunnel, tile):
            return self.places["tunnel_{}_{}".format(tunnel, tile)]

        def draw_insect(insect):
            return "{}({})".format(insect.name, round(insect.armor, 2))

        def draw_segment(word, filler=" ",size=15, start="|", end=""):
            return start + word + filler*(size - len(start + word + end)) + end
        bees_in_hive = self.hive.bees[:]
        for tunnel in range(self.dimensions[0]):
            line = ''.join([draw_segment(get_place(tunnel, tile).name, "_") for tile in range(self.dimensions[1])])
            line += draw_segment("Hive", "_", 16, "|", "|") if not tunnel else draw_segment(draw_insect(bees_in_hive.pop(0)) if bees_in_hive else "", " ", 16, "|", "|")
            print(line)
            line = ''.join([draw_segment(draw_insect(get_place(tunnel, tile).ant) if get_place(tunnel, tile).ant else "") for tile in range(self.dimensions[1])])
            line += draw_segment(draw_insect(bees_in_hive.pop(0)) if bees_in_hive else "", " ", 16, "|", "|")
            print(line)
            for i in range(max([len(get_place(tunnel, tile).bees) for tile in range(self.dimensions[1])])):
                line = ''.join([draw_segment(draw_insect(get_place(tunnel, tile).bees[i]) if len(get_place(tunnel, tile).bees) > i else "") for tile in range(self.dimensions[1])])
                line += draw_segment(draw_insect(bees_in_hive.pop(0)) if bees_in_hive else "", " ", 16, "|", "|")
                print(line)
            line = ''.join([draw_segment("", "V" if isinstance(get_place(tunnel, tile), Water) else "_") for tile in range(self.dimensions[1])])
            line += draw_segment(". . ." if bees_in_hive else "", " ", 16, "|", "|") if tunnel == self.dimensions[0] - 1 else draw_segment(draw_insect(bees_in_hive.pop(0)) if bees_in_hive else "", " ", 16, "|", "|")
            print(line)


    def simulate(self):
        """Simulate an attack on the ant colony (i.e., play the game)."""
        num_bees = len(self.bees)
        try:
            while True:
                self.hive.strategy(self)            # Bees invade
                self.strategy(self)                 # Ants deploy
                for ant in self.ants:               # Ants take actions
                    if ant.armor > 0:
                        ant.action(self)
                for bee in self.active_bees[:]:     # Bees take actions
                    if bee.armor > 0:
                        bee.action(self)
                    if bee.armor <= 0:
                        num_bees -= 1
                        self.active_bees.remove(bee)
                if num_bees == 0:
                    raise AntsWinException()
                self.time += 1
        except AntsWinException:
            print('All bees are vanquished. You win!')
            return True
        except BeesWinException:
            print('The ant queen has perished. Please try again.')
            return False

    def deploy_ant(self, place_name, ant_type_name):
        """Place an ant if enough food is available.

        This method is called by the current strategy to deploy ants.
        """
        constructor = self.ant_types[ant_type_name]
        if self.food < constructor.food_cost:
            print('Not enough food remains to place ' + ant_type_name)
        else:
            ant = constructor()
            self.places[place_name].add_insect(ant)
            self.food -= constructor.food_cost
            return ant

    def remove_ant(self, place_name):
        """Remove an Ant from the Colony."""
        place = self.places[place_name]
        if place.ant is not None:
            place.remove_insect(place.ant)

    @property
    def ants(self):
        return [p.ant for p in self.places.values() if p.ant is not None]

    @property
    def bees(self):
        return [b for p in self.places.values() for b in p.bees]

    @property
    def insects(self):
        return self.ants + self.bees

    def __str__(self):
        status = ' (Food: {0}, Time: {1})'.format(self.food, self.time)
        return str([str(i) for i in self.ants + self.bees]) + status

class QueenPlace(Place):
    """QueenPlace at the end of the tunnel, where the queen resides."""

    def add_insect(self, insect):
        """Add an Insect to this Place.

        Can't actually add Ants to a QueenPlace. However, if a Bee attempts to
        enter the QueenPlace, a BeesWinException is raised, signaling the end
        of a game.
        """
        assert not insect.is_ant, 'Cannot add {0} to QueenPlace'
        raise BeesWinException()

def ants_win():
    """Signal that Ants win."""
    raise AntsWinException()

def bees_win():
    """Signal that Bees win."""
    raise BeesWinException()

def ant_types():
    """Return a list of all implemented Ant classes."""
    all_ant_types = []
    new_types = [Ant]
    while new_types:
        new_types = [t for c in new_types for t in c.__subclasses__()]
        all_ant_types.extend(new_types)
    return [t for t in all_ant_types if t.implemented]

class GameOverException(Exception):
    """Base game over Exception."""
    pass

class AntsWinException(GameOverException):
    """Exception to signal that the ants win."""
    pass

class BeesWinException(GameOverException):
    """Exception to signal that the bees win."""
    pass

def interactive_strategy(colony):
    """A strategy that starts an interactive session and lets the user make
    changes to the colony.

    For example, one might deploy a ThrowerAnt to the first tunnel by invoking
    colony.deploy_ant('tunnel_0_0', 'Thrower')
    """
    print('colony: ' + str(colony))
    msg = '<Control>-D (<Control>-Z <Enter> on Windows) completes a turn.\n'
    interact(msg)

def start_with_strategy(args, strategy):
    """Reads command-line arguments and starts a game with those options."""
    import argparse
    parser = argparse.ArgumentParser(description="Play Ants vs. SomeBees")
    parser.add_argument('-d', type=str, metavar='DIFFICULTY',
                        help='sets difficulty of game (test/easy/medium/hard/extra-hard)')
    parser.add_argument('-w', '--water', action='store_true',
                        help='loads a full layout with water')
    parser.add_argument('--food', type=int,
                        help='number of food to start with when testing', default=2)
    args = parser.parse_args()

    assault_plan = make_normal_assault_plan()
    layout = dry_layout
    tunnel_length = 9
    num_tunnels = 3
    food = args.food

    if args.water:
        layout = wet_layout
    if args.d in ['t', 'test']:
        assault_plan = make_test_assault_plan()
        num_tunnels = 1
    elif args.d in ['e', 'easy']:
        assault_plan = make_easy_assault_plan()
        num_tunnels = 2
    elif args.d in ['n', 'normal']:
        assault_plan = make_normal_assault_plan()
        num_tunnels = 3
    elif args.d in ['h', 'hard']:
        assault_plan = make_hard_assault_plan()
        num_tunnels = 4
    elif args.d in ['i', 'extra-hard']:
        assault_plan = make_extra_hard_assault_plan()
        num_tunnels = 4

    hive = Hive(assault_plan)
    dimensions = (num_tunnels, tunnel_length)
    return AntColony(strategy, hive, ant_types(), layout, dimensions, food).simulate()


###########
# Layouts #
###########

def wet_layout(queen, register_place, tunnels=3, length=9, moat_frequency=3):
    """Register a mix of wet and and dry places."""
    for tunnel in range(tunnels):
        exit = queen
        for step in range(length):
            if moat_frequency != 0 and (step + 1) % moat_frequency == 0:
                exit = Water('water_{0}_{1}'.format(tunnel, step), exit)
            else:
                exit = Place('tunnel_{0}_{1}'.format(tunnel, step), exit)
            register_place(exit, step == length - 1)

def dry_layout(queen, register_place, tunnels=3, length=9):
    """Register dry tunnels."""
    wet_layout(queen, register_place, tunnels, length, 0)


#################
# Assault Plans #
#################

class AssaultPlan(dict):
    """The Bees' plan of attack for the Colony.  Attacks come in timed waves.

    An AssaultPlan is a dictionary from times (int) to waves (list of Bees).

    >>> AssaultPlan().add_wave(4, 2)
    {4: [Bee(3, None), Bee(3, None)]}
    """

    def add_wave(self, bee_type, bee_armor, time, count):
        """Add a wave at time with count Bees that have the specified armor."""
        bees = [bee_type(bee_armor) for _ in range(count)]
        self.setdefault(time, []).extend(bees)
        return self

    @property
    def all_bees(self):
        """Place all Bees in the hive and return the list of Bees."""
        return [bee for wave in self.values() for bee in wave]

def make_test_assault_plan():
    return AssaultPlan().add_wave(Bee, 3, 2, 1).add_wave(Bee, 3, 3, 1)

def make_easy_assault_plan():
    plan = AssaultPlan()
    for time in range(3, 16, 2):
        plan.add_wave(Bee, 3, time, 1)
    plan.add_wave(Wasp, 3, 4, 1)
    plan.add_wave(NinjaBee, 3, 8, 1)
    plan.add_wave(Hornet, 3, 12, 1)
    plan.add_wave(Boss, 15, 16, 1)
    return plan

def make_normal_assault_plan():
    plan = AssaultPlan()
    for time in range(3, 16, 2):
        plan.add_wave(Bee, 3, time, 2)
    plan.add_wave(Wasp, 3, 4, 1)
    plan.add_wave(NinjaBee, 3, 8, 1)
    plan.add_wave(Hornet, 3, 12, 1)
    plan.add_wave(Wasp, 3, 16, 1)

    #Boss Stage
    for time in range(21, 30, 2):
        plan.add_wave(Bee, 3, time, 2)
    plan.add_wave(Wasp, 3, 22, 2)
    plan.add_wave(Hornet, 3, 24, 2)
    plan.add_wave(NinjaBee, 3, 26, 2)
    plan.add_wave(Hornet, 3, 28, 2)
    plan.add_wave(Boss, 20, 30, 1)
    return plan

def make_hard_assault_plan():
    plan = AssaultPlan()
    for time in range(3, 16, 2):
        plan.add_wave(Bee, 4, time, 2)
    plan.add_wave(Hornet, 4, 4, 2)
    plan.add_wave(Wasp, 4, 8, 2)
    plan.add_wave(NinjaBee, 4, 12, 2)
    plan.add_wave(Wasp, 4, 16, 2)

    #Boss Stage
    for time in range(21, 30, 2):
        plan.add_wave(Bee, 4, time, 3)
    plan.add_wave(Wasp, 4, 22, 2)
    plan.add_wave(Hornet, 4, 24, 2)
    plan.add_wave(NinjaBee, 4, 26, 2)
    plan.add_wave(Hornet, 4, 28, 2)
    plan.add_wave(Boss, 30, 30, 1)
    return plan

def make_extra_hard_assault_plan():
    plan = AssaultPlan()
    plan.add_wave(Hornet, 5, 2, 2)
    for time in range(3, 16, 2):
        plan.add_wave(Bee, 5, time, 2)
    plan.add_wave(Hornet, 5, 4, 2)
    plan.add_wave(Wasp, 5, 8, 2)
    plan.add_wave(NinjaBee, 5, 12, 2)
    plan.add_wave(Wasp, 5, 16, 2)

    #Boss Stage
    for time in range(21, 30, 2):
        plan.add_wave(Bee, 5, time, 3)
    plan.add_wave(Wasp, 5, 22, 2)
    plan.add_wave(Hornet, 5, 24, 2)
    plan.add_wave(NinjaBee, 5, 26, 2)
    plan.add_wave(Hornet, 5, 28, 2)
    plan.add_wave(Boss, 30, 30, 2)
    return plan


from utils import *
@main
def run(*args):
    Insect.reduce_armor = class_method_wrapper(Insect.reduce_armor,
            pre=print_expired_insects)
    start_with_strategy(args, interactive_strategy)
