class Transition:
    def __init__(self, TargetMapId, TargetX, TargetY, Message="You enter another area."):
        self.TargetMapId = TargetMapId
        self.TargetX = TargetX
        self.TargetY = TargetY
        self.Message = Message

    def GetTargetMapId(self):
        return self.TargetMapId

    def GetTargetX(self):
        return self.TargetX

    def GetTargetY(self):
        return self.TargetY

    def GetMessage(self):
        return self.Message

    def Apply(self, CharacterObject):
        CharacterObject.SetX(self.TargetX)
        CharacterObject.SetY(self.TargetY)
        CharacterObject.ChangeRoom(self.TargetMapId)