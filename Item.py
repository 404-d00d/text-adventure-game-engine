class Item:
    def __init__(self, id, name, description, isStackable, quantity=1, maxQuantity=1):
        self.Id = id
        self.Name = name
        self.Description = description
        self.IsStackable = isStackable
        self.Quantity = 1 if not isStackable else quantity
        self.MaxQuantity = 1 if not isStackable else maxQuantity

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

    def SetQuantity(self, newQuantity):
        if not self.IsStackable:
            self.Quantity = 1
            return

        if self.MaxQuantity > 0:
            self.Quantity = max(0, min(newQuantity, self.MaxQuantity))
        else:
            self.Quantity = max(0, newQuantity)

    def CanStackWith(self, otherItem):
        return (
            self.IsStackable
            and otherItem.GetIsStackable()
            and self.Id == otherItem.GetId()
            and self.Name == otherItem.GetName()
        )

    def AddQuantity(self, amount):
        if not self.IsStackable:
            return amount

        if amount <= 0:
            return 0

        if self.MaxQuantity <= 0:
            self.Quantity += amount
            return 0

        spaceLeft = self.MaxQuantity - self.Quantity
        addedAmount = min(spaceLeft, amount)
        self.Quantity += addedAmount
        return amount - addedAmount

    def RemoveQuantity(self, amount):
        if not self.IsStackable:
            self.Quantity = 0
            return

        self.Quantity = max(0, self.Quantity - amount)

    def CreateUnique(self):
        return Item(
            self.Id,
            self.Name,
            self.Description,
            self.IsStackable,
            self.Quantity,
            self.MaxQuantity,
        )
