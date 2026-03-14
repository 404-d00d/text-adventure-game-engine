from WorldObject import WorldObject


class Door(WorldObject):
    def __init__(self, Inventory, Id, IsOpen=False):
        self.IsOpen = IsOpen
        Description = (
            "You see a door.\n"
            "There is a doorknob on it."
        )
        Inspect = (
            "The paint on the door appears to be a recent coat.\n"
            "There is some noticeable grain on the door, along with tiny bumps in the surface.\n"
            "The doorknob has fingerprint marks on it from constant use."
        )
        Interaction = ""
        super().__init__(Inventory, Id, Description, Inspect, Interaction, IsPassable=IsOpen)
        self.Options = (
            "-----\n"
            "1. Look Closer\n"
            "2. Interact\n"
            "3. Show Inventory\n"
            "Any Other Option.\n"
            "Do Nothing"
        )

    def GetDisplayId(self):
        return -self.Id if self.IsOpen else self.Id

    def AlterDoor(self):
        self.IsOpen = not self.IsOpen
        self.SetIsPassable(self.IsOpen)

    def CreateUnique(self, DifferentInventory):
        CreatedInventory = [ItemObject.CreateUnique() for ItemObject in DifferentInventory]
        return Door(CreatedInventory, self.Id, self.IsOpen)

    def Interact(self, Response, Player, InputFunction=input, OutputFunction=print):
        if Response == "1":
            return self.Inspect
        if Response == "2":
            self.AlterDoor()
            if self.IsOpen:
                return (
                    "You grab the doorknob and twist it.\n"
                    "The door swings open."
                )
            return (
                "You push the door shut.\n"
                "It closes with a thud."
            )
        if Response == "3":
            return self.LootInventory(Player, InputFunction, OutputFunction)
        return "You do nothing."


class LockedDoor(Door):
    def __init__(self, Inventory, IsLocked, Id, IsOpen=False):
        self.IsLocked = IsLocked
        super().__init__(Inventory, Id, IsOpen)
        self.Description = (
            "You see a door.\n"
            "There is a doorknob on it, as well as a lock underneath it."
        )
        self.Inspect = (
            "The paint on the door appears to be a recent coat.\n"
            "There is some noticeable grain on the door, along with tiny bumps in the surface.\n"
            "The doorknob has fingerprint marks on it from constant use.\n"
            "There is also a brass plate on the door with a key-shaped lock."
        )
        self.Options = (
            "-----\n"
            "1. Look Closer\n"
            "2. Interact - Doorknob\n"
            "3. Interact - Lock\n"
            "4. Show Inventory\n"
            "Any Other Option.\n"
            "Do Nothing"
        )

    def UnlockDoor(self):
        self.IsLocked = False

    def LockDoor(self):
        self.IsLocked = True
        if self.IsOpen:
            self.AlterDoor()

    def GetLockState(self):
        return self.IsLocked

    def CreateUnique(self, DifferentInventory, DifferentState=None):
        CreatedInventory = [ItemObject.CreateUnique() for ItemObject in DifferentInventory]
        LockState = self.IsLocked if DifferentState is None else DifferentState
        return LockedDoor(CreatedInventory, LockState, self.Id, self.IsOpen)

    def Interact(self, Response, Player, InputFunction=input, OutputFunction=print):
        if Response == "1":
            return self.Inspect
        if Response == "2":
            if self.IsLocked:
                return "This door is locked."
            self.AlterDoor()
            if self.IsOpen:
                return (
                    "You grab the doorknob and twist it.\n"
                    "The door swings open."
                )
            return (
                "You push the door shut.\n"
                "It closes with a thud."
            )
        if Response == "3":
            if self.IsLocked:
                self.UnlockDoor()
                return "You unlock the door.\nThe door is now unlocked."
            self.LockDoor()
            return "You lock the door.\nThe door is now locked."
        if Response == "4":
            return self.LootInventory(Player, InputFunction, OutputFunction)
        return "You do nothing."


class KeyedLockedDoor(LockedDoor):
    def __init__(self, Inventory, IsLocked, KeyId, Id, IsOpen=False):
        self.KeyId = KeyId
        super().__init__(Inventory, IsLocked, Id, IsOpen)

    def CreateUnique(self, DifferentInventory, DifferentState=None, DifferentKeyId=None):
        CreatedInventory = [ItemObject.CreateUnique() for ItemObject in DifferentInventory]
        LockState = self.IsLocked if DifferentState is None else DifferentState
        DoorKeyId = self.KeyId if DifferentKeyId is None else DifferentKeyId
        return KeyedLockedDoor(CreatedInventory, LockState, DoorKeyId, self.Id, self.IsOpen)

    def Interact(self, Response, Player, InputFunction=input, OutputFunction=print):
        if Response == "1":
            return self.Inspect
        if Response == "2":
            if self.IsLocked:
                return "This door is locked."
            self.AlterDoor()
            if self.IsOpen:
                return (
                    "You grab the doorknob and twist it.\n"
                    "The door swings open."
                )
            return (
                "You push the door shut.\n"
                "It closes with a thud."
            )
        if Response == "3":
            for ItemObject in Player.GetInventory():
                if ItemObject.GetId() == "key" and ItemObject.GetDoorId() == self.KeyId:
                    if self.IsLocked:
                        self.UnlockDoor()
                        return "You unlock the door."
                    self.LockDoor()
                    return "You lock the door."
            return "You cannot unlock this door."
        if Response == "4":
            return self.LootInventory(Player, InputFunction, OutputFunction)
        return "You do nothing."


class CodeLockedDoor(LockedDoor):
    def __init__(self, Inventory, IsLocked, Code, Id, IsOpen=False):
        self.Code = str(Code)
        super().__init__(Inventory, IsLocked, Id, IsOpen)
        self.Description = (
            "You see a door.\n"
            "There is a doorknob on it, as well as a keypad underneath it."
        )
        self.Inspect = (
            "The paint on the door appears to be a recent coat.\n"
            "There is some noticeable grain on the door, along with tiny bumps in the surface.\n"
            "The doorknob has fingerprint marks on it from constant use.\n"
            "The keypad is worn and smudged from constant use."
        )
        self.Options = (
            "-----\n"
            "1. Look Closer\n"
            "2. Interact - Doorknob\n"
            "3. Interact - Keypad\n"
            "4. Show Inventory\n"
            "Any Other Option.\n"
            "Do Nothing"
        )

    def KeypadResponse(self, InputtedCode):
        if str(InputtedCode) == self.Code:
            self.UnlockDoor()
            return "You hear a pleasant tone. The door is unlocked."

        if not self.IsLocked:
            self.LockDoor()
            return "You hear a harsh beep. The door is now locked."

        return "You hear a harsh beep. The door is still locked."

    def CreateUnique(self, DifferentInventory, DifferentState=None, DifferentCode=None):
        CreatedInventory = [ItemObject.CreateUnique() for ItemObject in DifferentInventory]
        LockState = self.IsLocked if DifferentState is None else DifferentState
        DoorCode = self.Code if DifferentCode is None else DifferentCode
        return CodeLockedDoor(CreatedInventory, LockState, DoorCode, self.Id, self.IsOpen)

    def Interact(self, Response, Player, InputFunction=input, OutputFunction=print):
        if Response == "1":
            return self.Inspect
        if Response == "2":
            if self.IsLocked:
                return "This door is locked."
            self.AlterDoor()
            if self.IsOpen:
                return (
                    "You grab the doorknob and twist it.\n"
                    "The door swings open."
                )
            return (
                "You push the door shut.\n"
                "It closes with a thud."
            )
        if Response == "3":
            Keycode = InputFunction("Enter Keypad Code: ")
            return self.KeypadResponse(Keycode)
        if Response == "4":
            return self.LootInventory(Player, InputFunction, OutputFunction)
        return "You do nothing."
