import math

EPS = 1e-6

def cross(x1, y1, x2, y2):
	return x1 * y2 - x2 * y1

def dblcmp(f):
	if math.fabs(f) < EPS:
		return 0
	if f > 0:
		return 1
	return -1