class Item:
    def __init__(self, Id, Name, Description, IsStackable, Quantity=1, MaxQuantity=1):
        self.Id = Id
        self.Name = Name
        self.Description = Description
        self.IsStackable = IsStackable
        self.Quantity = 1 if not IsStackable else Quantity
        self.MaxQuantity = 1 if not IsStackable else MaxQuantity

    def GetId(self):
        return self.Id

    def GetName(self):
        return self.Name

    def GetDescription(self):
        return self.Description

    def GetQuantity(self):
        return self.Quantity

    def GetIsStackable(self):
        return self.IsStackable

    def GetMaxQuantity(self):
        return self.MaxQuantity

    def CanStackWith(self, OtherItem):
        return (
            self.IsStackable
            and OtherItem.GetIsStackable()
            and self.Id == OtherItem.GetId()
            and self.Name == OtherItem.GetName()
        )

    def AddQuantity(self, Amount):
        if not self.IsStackable:
            return False

        NewQuantity = self.Quantity + Amount
        if self.MaxQuantity > 0:
            NewQuantity = min(NewQuantity, self.MaxQuantity)
        self.Quantity = NewQuantity
        return True

    def RemoveQuantity(self, Amount):
        if not self.IsStackable:
            self.Quantity = 0
            return

        self.Quantity = max(0, self.Quantity - Amount)

    def CreateUnique(self):
        return Item(
            self.Id,
            self.Name,
            self.Description,
            self.IsStackable,
            self.Quantity,
            self.MaxQuantity,
        )


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
