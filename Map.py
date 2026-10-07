class Map:
    def __init__(self, Id, Cells, Transitions, MapSummary):
        self.Id = Id
        self.Cells = Cells
        self.Transitions = Transitions
        self.MapSummary = MapSummary

    def GetMap(self):
        return self.Cells

    def GetId(self):
        return self.Id

    def GetTransitions(self):
        return self.Transitions

    def GetTransitionAt(self, X, Y):
        return self.Transitions.get((X, Y))

    def GetSpecificCell(self, X, Y):
        return self.Cells[Y][X]

    def GetMapSummary(self):
        return self.MapSummary