class Character:
    DirectionOffsets = {
        1: (0, -1),
        2: (1, 0),
        3: (0, 1),
        4: (-1, 0),
    }

    MovementOffsets = {
        "forward": 0,
        "sideright": 1,
        "backward": 2,
        "sideleft": 3,
    }

    def __init__(self, Id, X, Y, Direction, Room, Inventory):
        self.Id = Id
        self.X = X
        self.Y = Y
        self.Direction = Direction
        self.Room = Room
        self.Inventory = list(Inventory)

    def GetId(self):
        return self.Id

    def GetX(self):
        return self.X

    def GetY(self):
        return self.Y

    def GetDirection(self):
        return self.Direction

    def GetRoom(self):
        return self.Room

    def ChangeRoom(self, NewRoomId):
        self.Room = NewRoomId

    def GetInventory(self):
        return self.Inventory

    def FormatInventory(self):
        Lines = ["===", "PLAYER INVENTORY"]
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

    def RemoveItem(self, ItemObject):
        self.Inventory.remove(ItemObject)

    def RemoveItemAt(self, Index):
        return self.Inventory.pop(Index)

    def AddItem(self, ItemObject):
        if ItemObject.GetIsStackable():
            for ExistingItem in self.Inventory:
                if ExistingItem.CanStackWith(ItemObject):
                    ExistingItem.AddQuantity(ItemObject.GetQuantity())
                    return
        self.Inventory.append(ItemObject)

    def SetX(self, NewX):
        self.X = NewX

    def SetY(self, NewY):
        self.Y = NewY

    def GetDirectionalOffset(self, Direction):
        return self.DirectionOffsets[Direction]

    def RotateRight(self):
        self.Direction = (self.Direction % 4) + 1

    def RotateLeft(self):
        self.Direction = 4 if self.Direction == 1 else self.Direction - 1

    def GetMovementOffset(self, Command):
        RotationOffset = self.MovementOffsets[Command]
        TargetDirection = (self.Direction + RotationOffset - 1) % 4 + 1
        return self.GetDirectionalOffset(TargetDirection)

    def MoveCharacter(self, MapGrid, Command):
        if Command == "right":
            self.RotateRight()
            return True

        if Command == "left":
            self.RotateLeft()
            return True

        if Command not in self.MovementOffsets:
            return False

        DeltaX, DeltaY = self.GetMovementOffset(Command)
        NewX = self.X + DeltaX
        NewY = self.Y + DeltaY

        if not (0 <= NewY < len(MapGrid) and 0 <= NewX < len(MapGrid[0])):
            return False

        TargetObject = MapGrid[NewY][NewX]
        if TargetObject.GetIsPassable():
            self.X = NewX
            self.Y = NewY
            return True

        return False
