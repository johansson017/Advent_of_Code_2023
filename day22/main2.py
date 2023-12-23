import re
from collections import defaultdict
def ints(s):
	return list(map(int, re.findall(r'\d+', s)))

ll = [tuple(ints(x) + [i]) for i, x in enumerate(open('day22/input/input.txt').read().strip().split('\n'))]

def down(brick):
	return (brick[0], brick[1], brick[2] - 1, brick[3], brick[4], brick[5] - 1, brick[6])

def positions(brick):
	for x in range(brick[0], brick[3] + 1):
		for y in range(brick[1], brick[4] + 1):
			for z in range(brick[2], brick[5] + 1):
				yield (x,y,z)

occupied = {}
fallen = []
for brick in sorted(ll, key=lambda brick: brick[2]):
	while brick[2] > 0 and all(pos not in occupied for pos in positions(down(brick))):
		brick = down(brick)
	for pos in positions(brick):
		occupied[pos] = brick
	fallen.append(brick)

above = defaultdict(set)
below = defaultdict(set)
for brick in fallen:
	inthisbrick = set(positions(brick))
	for pos in positions(down(brick)):
		if pos in occupied and pos not in inthisbrick:
			above[occupied[pos]].add(brick)
			below[brick].add(occupied[pos])


def whatif(disintegrated):
	falling = set()
	def falls(brick):
		if brick in falling:
			return
		falling.add(brick)
		for parent in above[brick]:
			if not len(below[parent] - falling):
				# if everything below the parent is falling, so is the parent
				falls(parent)
	falls(disintegrated)
	return len(falling)

p1 = 0
p2 = 0
for brick in fallen:
	wouldfall = whatif(brick)
	p1 += wouldfall == 1
	p2 += wouldfall - 1

print(p1, p2)
