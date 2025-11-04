from enum import Enum

class DefectLabel(str, Enum):
    hole = "Hole"
    knot = "Knot"
    line = "Line"
    stain = "Stain"
