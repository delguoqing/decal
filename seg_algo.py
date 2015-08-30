# -*- coding: gbk -*-
from common_algo import cross, dblcmp

def is_seg_proper_intersect(xa, ya, xb, yb, xc, yc, xd, yd):
	c_abd = dblcmp(cross(xb - xa, yb - ya, xd - xa, yd - ya))
	c_abc = dblcmp(cross(xb - xa, yb - ya, xc - xa, yc - ya))
	c_cda = dblcmp(cross(xd - xc, yd - yc, xa - xc, ya - yc))
	c_cdb = dblcmp(cross(xd - xc, yd - yc, xb - xc, yb - yc))
	return c_abd * c_abc < 0 and c_cda * c_cdb < 0

def get_seg_proper_intersect(xa, ya, xb, yb, xc, yc, xd, yd):
	s_abd = cross(xb - xa, yb - ya, xd - xa, yd - ya)
	c_abd = dblcmp(s_abd)
	s_abc = cross(xb - xa, yb - ya, xc - xa, yc - ya)
	c_abc = dblcmp(s_abc)
	c_cda = dblcmp(cross(xd - xc, yd - yc, xa - xc, ya - yc))
	c_cdb = dblcmp(cross(xd - xc, yd - yc, xb - xc, yb - yc))
	if c_abd * c_abc >= 0 or c_cda * c_cdb >= 0:
		return None
	i = 1.0 * s_abd / (s_abd - s_abc)
	j = 1.0 - i
	return xd * i + xc * j, yd * i + yc * j

# 前提是已经判定a, b, c三点共线
def between(xc, yc, xa, ya, xb, yb):
	if math.fabs(xb - xa) > math.fabs(yb - ya):
		return dblcmp(xa - xc) * dblcmp(xb - xc)
	else:
		return dblcmp(ya - yc) * dblcmp(yb - yc)

def is_seg_intersect(xa, ya, xb, yb, xc, yc, xd, yd):
	c_abd = dblcmp(cross(xb - xa, yb - ya, xd - xa, yd - ya))
	if c_abd == 0 and between(xd, yd, xa, ya, xb, yb) <= 0:
		return True
	c_abc = dblcmp(cross(xb - xa, yb - ya, xc - xa, yc - ya))
	if c_abc == 0 and between(xc, yc, xa, ya, xb, yb) <= 0:
		return True
	c_cda = dblcmp(cross(xd - xc, yd - yc, xa - xc, ya - yc))
	if c_cda == 0 and between(xa, ya, xc, yc, xd, yd) <= 0:
		return True
	c_cdb = dblcmp(cross(xd - xc, yd - yc, xb - xc, yb - yc))
	if c_cdb == 0 and between(xb, yb, xc, yc, xd, yd) <= 0:
		return True
	return c_abd * c_abc < 0 and c_cda * c_cdb < 0

def get_seg_intersect(xa, ya, xb, yb, xc, yc, xd, yd):
	res = []
	s_abd = cross(xb - xa, yb - ya, xd - xa, yd - ya)
	c_abd = dblcmp(s_abd)
	if c_abd == 0 and between(xd, yd, xa, ya, xb, yb) <= 0:
		res.append((xd, yd))
	s_abc = cross(xb - xa, yb - ya, xc - xa, yc - ya)
	c_abc = dblcmp(s_abc)
	if c_abc == 0 and between(xc, yc, xa, ya, xb, yb) <= 0:
		res.append((xc, yc))
	c_cda = dblcmp(cross(xd - xc, yd - yc, xa - xc, ya - yc))
	if c_cda == 0 and between(xa, ya, xc, yc, xd, yd) < 0:
		res.append((xa, ya))
	c_cdb = dblcmp(cross(xd - xc, yd - yc, xb - xc, yb - yc))
	if c_cdb == 0 and between(xb, yb, xc, yc, xd, yd) < 0:
		res.append((xb, yb))
	# 如果至少有一个点与另一条线段共线，那么此时可以断定交点已经全部求完
	if len(res) > 0:
		return res
	if c_abd * c_abc < 0 and c_cda * c_cdb < 0:
		i = 1.0 * s_abd / (s_abd - s_abc)
		j = 1.0 - i
		res.append((xd * i + xc * j, yd * i + yc * j))
	return res

if __name__ == '__main__':
	assert not is_seg_proper_intersect(1, 1, 2, 2, 2, 1.5, 3, 1.2)
	assert is_seg_proper_intersect(1, 1, 2, 2, 0, 1.5, 3, 1.2)
	
	print (get_seg_proper_intersect(1, 1, 2, 2, 2, 1.5, 3, 1.2))
	print (get_seg_proper_intersect(1, 1, 2, 2, 0, 1.5, 3, 1.2))
	
	assert not is_seg_intersect(1, 1, 2, 2, 2, 1.5, 3, 1.2)
	assert is_seg_intersect(1, 1, 2, 2, 0, 1.5, 3, 1.2)
	assert is_seg_intersect(1, 1, 2, 2, 2, 2, 3, 2)
	assert not is_seg_intersect(1, 1, 2, 2, 3.1, 3.1, 3, 2)
	
	assert is_seg_intersect(1, 0, 10, 0, 2, 0, 11, 0)
	print (get_seg_intersect(1, 0, 10, 0, 2, 0, 11, 0))
	print (get_seg_intersect(1, 1, 2, 2, 0, 1.5, 3, 1.2))
	print (get_seg_intersect(1, 1, 2, 2, 2, 2, 3, 2), get_seg_intersect(2, 2, 3, 2, 1, 1, 2, 2))
	