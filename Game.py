class Game:
    MovementCommands = {
        "w": "forward",
        "a": "sideleft",
        "s": "backward",
        "d": "sideright",
    }

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

    def TryMapTransition(self, X, Y):
        CurrentMap = self.GetCurrentMap()

        if CurrentMap is None:
            return False

        TransitionObject = CurrentMap.GetTransitionAt(X, Y)

        if TransitionObject is None:
            return False

        TransitionObject.Apply(self.PlayerCharacter)
        self.GameplayObject.SetResult(
            TransitionObject.GetMessage()
        )

        return True

    def HandleMapTransition(self):
        return self.TryMapTransition(
            self.PlayerCharacter.GetX(),
            self.PlayerCharacter.GetY(),
        )

    def ProcessMovement(self, MovementCommand):
        CurrentMap = self.GetCurrentMap()

        if CurrentMap is None:
            return False

        MapGrid = CurrentMap.GetMap()

        TargetX, TargetY = self.PlayerCharacter.GetMovementTarget(
            MovementCommand
        )

        TargetIsInsideMap = (
            0 <= TargetY < len(MapGrid)
            and 0 <= TargetX < len(MapGrid[0])
        )

        # If the player is trying to move outside the current map,
        # check whether that outside coordinate is a transition point.
        if not TargetIsInsideMap:
            return self.TryMapTransition(
                TargetX,
                TargetY,
            )

        # Otherwise perform normal movement inside the current map.
        DidMove = self.PlayerCharacter.MoveCharacter(
            MapGrid,
            MovementCommand,
        )

        if not DidMove:
            return False

        # A transition may also exist on a real tile inside the map.
        # This supports traditional "step onto doorway and change room"
        # behavior.
        self.HandleMapTransition()

        return True

    def ProcessCommands(self, ActionText):
        for CommandCharacter in ActionText:
            CurrentMap = self.GetCurrentMap()

            if CurrentMap is None:
                break

            MovementCommand = self.MovementCommands.get(
                CommandCharacter
            )

            if MovementCommand is not None:
                self.ProcessMovement(MovementCommand)
                continue

            ShouldContinue, DidMove = self.GameplayObject.ExecuteCommand(
                CommandCharacter,
                CurrentMap.GetMap(),
                self.PlayerCharacter,
            )

            if DidMove:
                self.HandleMapTransition()

            if not ShouldContinue:
                break