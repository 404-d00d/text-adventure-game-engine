class Map:
    def __init__(self, Id, Cells, MapDict, MapSummary):
        self.Id = Id
        self.Cells = Cells
        self.ConnectingRooms = MapDict
        self.MapSummary = MapSummary

    def GetMap(self):
        return self.Cells

    def GetId(self):
        return self.Id

    def GetConnections(self):
        return self.ConnectingRooms

    def GetSpecificCell(self, X, Y):
        return self.Cells[Y][X]

    def GetMapSummary(self):
        return self.MapSummary
