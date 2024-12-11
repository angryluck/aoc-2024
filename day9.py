from aocd import get_data

# Data
data = get_data(year=2024, day=9)

test = """\
2333133121414131402\
"""



# Convert data (text) to workable input
def parse(text:str) -> []:
    total = [] # The output-string as a list
    is_file = True
    ID = 0
    for char in text:
        blocks = int(char)
        total.extend([ID if is_file else "." for _ in range(blocks)])
        if is_file:
            ID += 1
        is_file = not is_file
    return total

def swap(i1:int, i2:int, total:[]) -> ():
    tmp1 = total[i1]
    tmp2 = total[i2]
    total[i2] = tmp1
    total[i1] = tmp2

def order(total:[]) -> ():
    end = len(total)-1
    start = 0
    while total[start] != ".":
        start += 1
    while start < end:
        swap(start, end, total)
        while total[start] != ".":
            start += 1
        while total[end] == ".":
            end -= 1

def checksum(total:[]) -> ():
    vals = [0 if c == "." else c for c in total]
    return sum(i*v for i,v in enumerate(vals))


# Part 1

def part1(text:str) -> int:
    total = parse(text)
    order(total)
    return checksum(total)

print("Part 1 test:", part1(test))
print("Part 1 real:", part1(data))




# Part 2
class File:
    def __init__(self, val: int, index: int) -> None:
        self.ID = index
        self.count = val
        self.is_file = True
        self.is_free = False

    def __str__(self) -> str:
        return str(self.ID)

    def vals(self) -> [int]:
        return [self.ID for _ in range(self.count)]

class Free:
    def __init__(self, val: int) -> None:
        self.count = val
        self.is_file = False
        self.is_free = True

    def __str__(self) -> str:
        return "."

    def vals(self) -> list[int]:
        return [0 for _ in range(self.count)]


def parse2(text:str)->[]:
    disk = []
    is_file = True
    index = 0
    for char in text:
        # blocks = int(char)
        val = int(char)
        if is_file:
            disk.append(File(val, index))
            index += 1
        else:
            disk.append(Free(val))
        is_file = not is_file
    return disk

disk = parse2(test)
def disk_to_str(disk:[]) -> str:
    return "".join(str(d) for d in disk)


def insert(disk:[], index: int)->None:
    file = disk[index]
    if file.is_free:
        return
    for i in range(index):
        if disk[i].is_free and disk[i].count >= file.count:
            file = disk.pop(index)
            disk[i].count -= file.count
            disk.insert(i, file)
            disk.insert(index, Free(file.count))
            return


### To check whether old checksum function still works:
# test2 = "00992111777.44.333....5555.6666.....8888.."
# vals = [0 if c == "." else int(c) for c in test2]
# total = sum((i*v) for i,v in enumerate(vals))
# print(total)

def checksum2(total:str) -> int:
    vals = [0 if c == "." else int(c) for c in total]
    return sum(i*v for i,v in enumerate(vals))

def checksum3(disk:[]) -> int:
    # NOTE: Slightly stupid hack here, utilizing that I defined a 'vals'
    # function for both File and Free. Preferably should use some if-else
    # statement here
    vals_nested = [d.vals() for d in disk]
    vals = [val for d in vals_nested for val in d]
    return sum(i*v for i,v in enumerate(vals))


def part2(text:str) -> int:
    disk = parse2(text)
    # remove_index = len(disk)-1
    for i in range(len(disk)-1, -1, -1):
        if disk[i].is_free:
            continue
        # file = disk.pop(i)
        insert(disk, i)
        print("Index:", i, "\r", end="")
    # print(disk_to_str(disk))
    return checksum3(disk)

print("Part 2 test:", part2(test))
print("Part 2 real:", part2(data))
