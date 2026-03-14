from Character import Character
from Display import Display
from Gameplay import Gameplay
from WorldObject import WorldObject
from Doors import Door, CodeLockedDoor, KeyedLockedDoor
from Toilet import Toilet
from Map import Map
from Item import Key


def BuildGame():
    PlayerCharacter = Character(0, 2, 2, 1, 1, [])
    DisplayObject = Display()
    GameplayObject = Gameplay()

    MapTransition1 = {
        (4, 1): {2: (1, 1)},
    }

    MapTransition2 = {
        (0, 1): {1: (3, 1)},
        (2, 9): {3: (0, 0)},
    }

    Key1 = Key(
        "key",
        "Worn Door Key",
        "A key for a hotel room.\nIt is very worn.",
        False,
        12345,
    )

    Space = WorldObject([], 0, "", "", "", IsPassable=True)
    Wall = WorldObject([], 1, "", "", "", IsPassable=False)
    Sink = WorldObject([], 7, "", "", "", IsPassable=False)
    Mirror = WorldObject([], 6, "", "", "", IsPassable=False)
    VerticalDoor = Door([], 2)
    LockedVerticalDoor = KeyedLockedDoor([], True, 12345, 2)
    HorizontalCodeDoor = CodeLockedDoor([], True, "1492", 4)
    ToiletObject = Toilet([], 3)

    BathroomMapGrid = [
        [Wall.CreateUnique([]), Wall.CreateUnique([]), Wall.CreateUnique([]), Wall.CreateUnique([]), Wall.CreateUnique([])],
        [Wall.CreateUnique([]), Space.CreateUnique([]), ToiletObject, Space.CreateUnique([]), VerticalDoor],
        [Wall.CreateUnique([]), Space.CreateUnique([]), Space.CreateUnique([]), Space.CreateUnique([Key1]), Wall.CreateUnique([])],
        [Wall.CreateUnique([]), Space.CreateUnique([]), Space.CreateUnique([]), Space.CreateUnique([]), Wall.CreateUnique([])],
        [Wall.CreateUnique([]), Wall.CreateUnique([]), Wall.CreateUnique([]), Wall.CreateUnique([]), Wall.CreateUnique([])],
    ]

    HallwayMapGrid = [
        [Wall.CreateUnique([]), HorizontalCodeDoor, Wall.CreateUnique([])],
        [VerticalDoor.CreateUnique([]), Space.CreateUnique([]), Wall.CreateUnique([])],
        [Wall.CreateUnique([]), Space.CreateUnique([]), Wall.CreateUnique([])],
        [Wall.CreateUnique([]), Space.CreateUnique([]), Wall.CreateUnique([])],
        [Wall.CreateUnique([]), Space.CreateUnique([]), Wall.CreateUnique([])],
        [Wall.CreateUnique([]), Space.CreateUnique([]), Wall.CreateUnique([])],
        [Wall.CreateUnique([]), Space.CreateUnique([]), Wall.CreateUnique([])],
        [Wall.CreateUnique([]), Space.CreateUnique([]), Wall.CreateUnique([])],
        [Wall.CreateUnique([]), Space.CreateUnique([]), Wall.CreateUnique([])],
        [Wall.CreateUnique([]), Space.CreateUnique([]), LockedVerticalDoor],
        [Wall.CreateUnique([]), Wall.CreateUnique([]), Wall.CreateUnique([])],
    ]

    BathroomDescription = (
        "-----\n"
        "You are in a bathroom.\n"
        "It is brightly lit and smells like lavender."
    )

    HallwayDescription = (
        "-----\n"
        "You are in a hallway.\n"
        "It is dull yellow and white and its odor is reminiscent of bleach."
    )

    Map1 = Map(1, BathroomMapGrid, MapTransition1, BathroomDescription)
    Map2 = Map(2, HallwayMapGrid, MapTransition2, HallwayDescription)

    CharacterList = [PlayerCharacter]
    MapObjects = {
        1: Map1,
        2: Map2,
    }

    return PlayerCharacter, DisplayObject, GameplayObject, CharacterList, MapObjects


def HandleRoomTransition(PlayerCharacter, GameplayObject, MapObjects):
    CurrentMap = MapObjects.get(PlayerCharacter.GetRoom())
    if CurrentMap is None:
        return

    Transitions = CurrentMap.GetConnections()
    TransitionData = Transitions.get((PlayerCharacter.GetX(), PlayerCharacter.GetY()))
    if TransitionData is None:
        return

    NewRoomId = list(TransitionData.keys())[0]
    NewPosition = TransitionData[NewRoomId]
    PlayerCharacter.SetX(NewPosition[0])
    PlayerCharacter.SetY(NewPosition[1])
    PlayerCharacter.ChangeRoom(NewRoomId)
    GameplayObject.SetResult("You enter another room.")


def Main():
    (
        PlayerCharacter,
        DisplayObject,
        GameplayObject,
        CharacterList,
        MapObjects,
    ) = BuildGame()

    DisplayObject.ClearScreen()
    print(
        "You wake up and find yourself on the floor, lying on your back.\n"
        "You blink rapidly, then push yourself upright as the drowsiness fades.\n"
    )
    input("Press Enter To Begin: ")

    while PlayerCharacter.GetRoom() != 3:
        CurrentMap = MapObjects.get(PlayerCharacter.GetRoom())

        DisplayObject.ClearScreen()
        DisplayObject.PrintDisplay(CharacterList, CurrentMap.GetMap())

        CurrentResult = GameplayObject.ShowResult()
        if CurrentResult:
            print(CurrentResult)

        GameplayObject.ClearResult()
        print(CurrentMap.GetMapSummary())

        ActionText = input("COMMAND: ")
        GameplayObject.CharacterActions(
            ActionText,
            CurrentMap.GetMap(),
            PlayerCharacter,
            False,
        )

        HandleRoomTransition(PlayerCharacter, GameplayObject, MapObjects)

    print(
        "You leave the building.\n"
        "CONGRATULATIONS.\n"
        "YOU HAVE BEATEN THE GAME."
    )
    input("Press Enter To Exit: ")


if __name__ == "__main__":
    Main()
