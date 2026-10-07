class Game:
    def __init__(self, PlayerCharacter, GameplayObject, MapObjects):
        self.PlayerCharacter = PlayerCharacter
        self.GameplayObject = GameplayObject
        self.MapObjects = MapObjects

    def GetPlayerCharacter(self):
        return self.PlayerCharacter

    def GetGameplayObject(self):
        return self.GameplayObject

    def GetCurrentMap(self):
        return self.MapObjects.get(self.PlayerCharacter.GetRoom())

    def HandleMapTransition(self):
        CurrentMap = self.GetCurrentMap()
        if CurrentMap is None:
            return False

        TransitionObject = CurrentMap.GetTransitionAt(
            self.PlayerCharacter.GetX(),
            self.PlayerCharacter.GetY(),
        )
        if TransitionObject is None:
            return False

        TransitionObject.Apply(self.PlayerCharacter)
        self.GameplayObject.SetResult(TransitionObject.GetMessage())
        return True

    def ProcessCommands(self, ActionText):
        for CommandCharacter in ActionText:
            CurrentMap = self.GetCurrentMap()
            if CurrentMap is None:
                break

            ShouldContinue, DidMove = self.GameplayObject.ExecuteCommand(
                CommandCharacter,
                CurrentMap.GetMap(),
                self.PlayerCharacter,
            )

            if DidMove:
                self.HandleMapTransition()

            if not ShouldContinue:
                break