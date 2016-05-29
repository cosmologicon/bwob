

# window dimensions
wx, wy = 854, 480
# main gameplay area width
gx = 640

zoom0 = 40
zoomrange = -1, 1

controlschemes = "rando", "tetris", "pyweek", "utree"
controlscheme = "utree"


colors = [
	(50, 150, 50),
	(150, 50, 150),
	(150, 80, 0),
]

bends = [0.2, 0.4, -0.3]


# Available branch specs. Randomly-generated stalks will be selected from this list.
# Entries may be removed or duplicated. Duplicated entries are more likely to appear in
# proportion to the number of times they appear.

branchspecs = [
	# singles
	(1,),  # sharp right
	(2,),  # soft right
	(3,),  # straight
	(4,),  # soft left
	(5,),  # sharp left
	# doubles
	(1,3),
	(1,4),
	(2,3),
	(2,4),
	(2,5),
	(3,4),
	(3,5),
]

