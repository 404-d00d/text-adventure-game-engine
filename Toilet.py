from WorldObject import WorldObject


class Toilet(WorldObject):
    def __init__(self, Inventory, Id):
        Description = (
            "You see a toilet.\n"
            "It is porcelain white, with no blemishes or marks on the body.\n"
            "The tank lid and tank appear to be bolted to the toilet basin and the wall itself.\n"
            "The toilet lid is closed."
        )
        Inspect = (
            "You lift up the toilet lid.\n"
            "The bowl is filled with water, chunks of food, and bile.\n"
            "You immediately close the toilet lid."
        )
        Interaction = (
            "You push down on the toilet handle on the tank.\n"
            "You hear the water rush through the bowl and down the pipes."
        )
        super().__init__(Inventory, Id, Description, Inspect, Interaction, IsPassable=False)

    def FlushToilet(self):
        self.Inspect = (
            "You lift up the toilet lid.\n"
            "The bowl is clear and clean.\n"
            "The water in the bowl is transparent."
        )

    def Interact(self, Response, Player, InputFunction=input, OutputFunction=print):
        if Response == "1":
            return self.Inspect
        if Response == "2":
            self.FlushToilet()
            return self.Interaction
        if Response == "3":
            return self.LootInventory(Player, InputFunction, OutputFunction)
        return "You do nothing."

    def CreateUnique(self, DifferentInventory):
        CreatedInventory = [ItemObject.CreateUnique() for ItemObject in DifferentInventory]
        return Toilet(CreatedInventory, self.Id)
