class WorldObject:
    def __init__(self, Inventory, Id, Description, Inspect, Interaction, IsPassable=False):
        self.Inventory = list(Inventory)
        self.Id = Id
        self.Description = Description
        self.Inspect = Inspect
        self.Interaction = Interaction
        self.IsPassable = IsPassable
        self.Options = (
            "-----\n"
            "1. Look Closer\n"
            "2. Interact\n"
            "3. Show Inventory\n"
            "4. Add To Inventory\n"
            "Any Other Option.\n"
            "Do Nothing"
        )

    def GetId(self):
        return self.Id

    def GetDisplayId(self):
        return self.Id

    def GetInventory(self):
        return self.Inventory

    def GetIsPassable(self):
        return self.IsPassable

    def SetIsPassable(self, NewState):
        self.IsPassable = NewState

    def FormatInventory(self):
        Lines = ["===", "OBJECT INVENTORY"]
        if not self.Inventory:
            Lines.append("(empty)")
        else:
            for Index, ItemObject in enumerate(self.Inventory):
                Lines.append(
                    str(Index)
                    + ": "
                    + str(ItemObject.GetQuantity())
                    + " "
                    + ItemObject.GetName()
                )
        return "\n".join(Lines)

    def ShowInventory(self):
        print(self.FormatInventory())

    def LootInventory(self, Player, InputFunction=input, OutputFunction=print):
        if not self.Inventory:
            return "There is nothing inside."

        while True:
            OutputFunction(self.FormatInventory())
            OutputFunction("e: Exit Inventory")
            Selection = InputFunction("Choose Your Option: ").strip()

            if Selection.lower() == "e":
                return "You are done with this item."

            try:
                SelectionIndex = int(Selection)
                ItemObject = self.Inventory.pop(SelectionIndex)
                OutputFunction(ItemObject.GetName() + " is the item you selected.")
                Player.AddItem(ItemObject)
            except (ValueError, IndexError):
                OutputFunction("This option is not valid.")

    def PlaceIntoInventory(self, Player, InputFunction=input, OutputFunction=print):
        if not Player.GetInventory():
            return "You have nothing to place into this object."

        while True:
            OutputFunction(Player.FormatInventory())
            OutputFunction("e: Exit Inventory")
            Selection = InputFunction("Choose Your Option: ").strip()

            if Selection.lower() == "e":
                return "You are done with this item."

            try:
                SelectionIndex = int(Selection)
                ItemObject = Player.RemoveItemAt(SelectionIndex)
                self.Inventory.append(ItemObject)
                OutputFunction(ItemObject.GetName() + " is the item you put into the object.")
            except (ValueError, IndexError):
                OutputFunction("This option is not valid.")

    def ShowDescription(self):
        return self.Description

    def ShowOptions(self):
        return self.Options

    def Interact(self, Response, Player, InputFunction=input, OutputFunction=print):
        if Response == "1":
            return self.Inspect
        if Response == "2":
            return self.Interaction
        if Response == "3":
            return self.LootInventory(Player, InputFunction, OutputFunction)
        if Response == "4":
            return self.PlaceIntoInventory(Player, InputFunction, OutputFunction)
        return "You do nothing."

    def CreateUnique(self, DifferentInventory):
        CreatedInventory = [ItemObject.CreateUnique() for ItemObject in DifferentInventory]
        return WorldObject(
            CreatedInventory,
            self.Id,
            self.Description,
            self.Inspect,
            self.Interaction,
            self.IsPassable,
        )
