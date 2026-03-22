from Item import Item

class Key(Item):
    def __init__(self, Id, Name, Description, IsStackable, DoorId, Quantity=1, MaxQuantity=1):
        super().__init__(Id, Name, Description, IsStackable, Quantity, MaxQuantity)
        self.DoorId = DoorId

    def GetDoorId(self):
        return self.DoorId

    def CreateUnique(self):
        return Key(
            self.Id,
            self.Name,
            self.Description,
            self.IsStackable,
            self.DoorId,
            self.Quantity,
            self.MaxQuantity,
        )
