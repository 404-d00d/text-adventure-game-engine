class Gameplay:
    def __init__(self, InputFunction=input, OutputFunction=print):
        self.Result = ""
        self.InputFunction = InputFunction
        self.OutputFunction = OutputFunction

    def ShowResult(self):
        return self.Result

    def SetResult(self, Message):
        self.Result = Message

    def ClearResult(self):
        self.Result = ""

    def GetInteractionTarget(self, CharacterObject, MapGrid, InFront):
        if InFront:
            DeltaX, DeltaY = CharacterObject.GetDirectionalOffset(CharacterObject.GetDirection())
        else:
            DeltaX, DeltaY = 0, 0

        TargetX = CharacterObject.GetX() + DeltaX
        TargetY = CharacterObject.GetY() + DeltaY

        if 0 <= TargetY < len(MapGrid) and 0 <= TargetX < len(MapGrid[0]):
            return MapGrid[TargetY][TargetX]
        return None

    def InteractObject(self, CharacterObject, MapGrid, InFront):
        TargetObject = self.GetInteractionTarget(CharacterObject, MapGrid, InFront)
        if TargetObject is None:
            self.Result = "You cannot interact with this object."
            return

        self.OutputFunction(TargetObject.ShowDescription())
        self.OutputFunction(TargetObject.ShowOptions())
        Response = self.InputFunction(": ").strip()
        self.Result = TargetObject.Interact(
            Response,
            CharacterObject,
            self.InputFunction,
            self.OutputFunction,
        )

    def InventoryMenu(self, Player):
        while True:
            self.OutputFunction(Player.FormatInventory())
            self.OutputFunction("e: Exit Inventory")
            Selection = self.InputFunction("Choose Your Option: ").strip()

            if Selection.lower() == "e":
                self.Result = "You close your inventory."
                return

            try:
                SelectionIndex = int(Selection)
                ItemObject = Player.GetInventory()[SelectionIndex]
                self.OutputFunction(ItemObject.GetName())
                self.OutputFunction(ItemObject.GetDescription())
                self.OutputFunction("")
            except (ValueError, IndexError):
                self.OutputFunction("This option is not valid.")

    def ExecuteCommand(self, CommandCharacter, MapGrid, PlayerCharacter):
        if CommandCharacter == "e":
            PlayerCharacter.MoveCharacter(MapGrid, "right")
            return True, False

        if CommandCharacter == "q":
            PlayerCharacter.MoveCharacter(MapGrid, "left")
            return True, False

        if CommandCharacter == "w":
            DidMove = PlayerCharacter.MoveCharacter(MapGrid, "forward")
            return True, DidMove

        if CommandCharacter == "a":
            DidMove = PlayerCharacter.MoveCharacter(MapGrid, "sideleft")
            return True, DidMove

        if CommandCharacter == "s":
            DidMove = PlayerCharacter.MoveCharacter(MapGrid, "backward")
            return True, DidMove

        if CommandCharacter == "d":
            DidMove = PlayerCharacter.MoveCharacter(MapGrid, "sideright")
            return True, DidMove

        if CommandCharacter == "f":
            self.InteractObject(PlayerCharacter, MapGrid, True)
            return False, False

        if CommandCharacter == "F":
            self.InteractObject(PlayerCharacter, MapGrid, False)
            return False, False

        if CommandCharacter == "i":
            self.InventoryMenu(PlayerCharacter)
            return False, False

        if CommandCharacter.strip() == "":
            return True, False

        self.Result = "ERROR: Not a valid command."
        return False, False