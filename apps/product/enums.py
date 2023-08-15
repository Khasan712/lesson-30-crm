from enum import Enum


class Measure(Enum):
    kg = 'kg'
    litr = 'litr'
    piece = 'piece'

    @classmethod
    def choices(cls):
        return [
            (key.value, key.name)
            for key in cls
        ]