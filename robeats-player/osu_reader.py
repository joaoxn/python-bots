from enum import Enum
from io import TextIOWrapper
from math import floor

COLUMN_COUNT = 4

class HitObjectType(Enum):
    TAP = 1
    HOLD = 128


class HitObject:
    column: int
    time: int
    type: HitObjectType
    endTime: int

    x: int
    y: int
    hitSound: int
    hitSample: str

    def __init__(self, column, time, type, endTime, x, y, hitSound, hitSample):
        self.column = column
        self.time = time
        self.type = type
        self.endTime = endTime
        self.x = x
        self.y = y
        self.hitSound = hitSound
        self.hitSample = hitSample

    def __str__(self):
        if self.type == HitObjectType.HOLD:
            return f"[{self.time:.2f}s] col{self.column} (HOLD {self.endTime-self.time:.2f}s)"
        return f"[{self.time:.2f}s] col{self.column} ({self.type.name})"


def clamp(x, minimum, maximum):
    return max(minimum, min(x, maximum))


def read_file_text(file: TextIOWrapper) -> list[HitObject]:
    notes = []
    listing_hit_objects = False
    for line in file:
        text = line.strip()

        if listing_hit_objects:
            data = text.split(",")

            hit_object = HitObject(
                column=clamp(floor(int(data[0]) * COLUMN_COUNT / 512), 0, COLUMN_COUNT - 1),
                time=int(data[2]) / 1000,
                type = HitObjectType(int(data[3])),
                endTime=int(data[5].split(":", 1)[0]) / 1000,

                x=int(data[0]),
                y=int(data[1]),
                hitSound=int(data[4]),
                hitSample=data[5].split(":", 1)[1]
            )
            notes.append(hit_object)

        if text != "[HitObjects]": continue
        listing_hit_objects = True
    return notes


def read(filepath: str) -> list[HitObject]:
    try:
        with open(filepath, "r") as file:
            return read_file_text(file)
    except FileNotFoundError as e:
        print(f"Error: The file '{filepath}' was not found.")
        raise e
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e
