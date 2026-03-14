import os
import platform


class Display:
    def ClearScreen(self):
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    def RepresentObject(self, MapObject):
        DisplayId = MapObject.GetDisplayId()
        SymbolMap = {
            1: "N",
            3: "A",
            6: "0",
            7: "Q",
            2: "|",
            -2: "_",
            4: "_",
            -4: "|",
            0: ".",
        }
        return SymbolMap.get(DisplayId, " ")

    def PrintCharacter(self, CharacterObject):
        if CharacterObject.GetId() == 0:
            return {
                1: "^",
                2: ">",
                3: "v",
                4: "<",
            }[CharacterObject.GetDirection()]

        if CharacterObject.GetId() == 1:
            return {
                1: "M",
                2: "3",
                3: "W",
                4: "E",
            }[CharacterObject.GetDirection()]

        if CharacterObject.GetId() == 2:
            return {
                1: "n",
                2: "ↄ",
                3: "u",
                4: "c",
            }[CharacterObject.GetDirection()]

        return "?"

    def BuildDisplay(self, Characters, MapGrid):
        Lines = []
        for Y in range(len(MapGrid)):
            RowSymbols = []
            for X in range(len(MapGrid[0])):
                PrintedCharacter = None
                for CharacterObject in Characters:
                    if CharacterObject.GetX() == X and CharacterObject.GetY() == Y:
                        PrintedCharacter = self.PrintCharacter(CharacterObject)
                        break

                if PrintedCharacter is None:
                    RowSymbols.append(self.RepresentObject(MapGrid[Y][X]))
                else:
                    RowSymbols.append(PrintedCharacter)

            Lines.append(" ".join(RowSymbols))

        Lines.append("-----")
        return "\n".join(Lines)

    def PrintDisplay(self, Characters, MapGrid):
        print(self.BuildDisplay(Characters, MapGrid))
