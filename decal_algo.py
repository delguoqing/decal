# -*- coding: gbk -*-
import math
from common_algo import dblcmp, cross

# ǰ�����Ѿ��ж�a, b, c���㹲��
def between(xc, yc, xa, ya, xb, yb):
	if math.fabs(xb - xa) > math.fabs(yb - ya):
		da = xa - xc
		db = xb - xc
	else:
		da = ya - yc
		db = yb - yc
	sa = dblcmp(da)
	if sa == 0:
		return 0.0
	sb = dblcmp(db)
	if sb == 0:
		return None
	if sa * sb < 0:
		return 1.0 * da / (da - db)
	return None
	
# (xa, ya) -> (xb, yb)
# (xc, yc) -> (xd, yd)
# �����߶ζ����з���ģ������յ㲻���뽻�㡣�����յ㲻�ǣ��������ֻ��1������
# ����ֵ��(x, y, f1(�������߶�ab�ϵı���), f2(�������߶�cd�ϵı���), A�Ƿ���CD����࣬C�Ƿ���AB�����)
def calc_seg_intersect(xa, ya, xb, yb, xc, yc, xd, yd):

	s_abc = cross(xb - xa, yb - ya, xc - xa, yc - ya)
	c_abc = dblcmp(s_abc)
	c_cda = dblcmp(cross(xd - xc, yd - yc, xa - xc, ya - yc))
	
	if c_abc == 0:
		f = between(xc, yc, xa, ya, xb, yb)
		if f is not None:
			return xc, yc, f, 0.0, (c_cda == 1), False

	if c_cda == 0:
		f = between(xa, ya, xc, yc, xd, yd)
		if f is not None:
			return xa, ya, 0.0, f, False, (c_abc == 1)
		
	s_abd = cross(xb - xa, yb - ya, xd - xa, yd - ya)
	c_abd = dblcmp(s_abd)
	
	c_cdb = dblcmp(cross(xd - xc, yd - yc, xb - xc, yb - yc))

	if c_abd * c_abc < 0 and c_cda * c_cdb < 0:
		i = 1.0 * s_abc / (s_abc - s_abd)
		j = 1.0 - i
		res_x = xc * j + xd * i
		res_y = yc * j + yd * i
		return res_x, res_y, between(res_x, res_y, xa, ya, xb, yb), i, (c_cda == 1), (c_abc == 1)
	return None, None, None, None, (c_cda == 1), (c_abc == 1)

# �ȸ���������������������꣬Ȼ���ֵ�õ�z
def calc_z_in_tri(x, y, pa, pb, pc):
	s_abd = cross(pb[0] - pa[0], pb[1] - pa[1], x - pa[0], y - pa[1])
	s_adc = cross(x - pa[0], y - pa[1], pc[0] - pa[0], pc[1] - pa[1])
	s_bcd = cross(pc[0] - pb[0], pc[1] - pb[1], x - pb[0], y - pb[1])
	z = (s_bcd * pa[2] + s_adc * pb[2] + s_abd * pc[2]) / (s_abd + s_adc + s_bcd)
	return z

def decal_2d(rect, tri):
	p0, p1, p2, p3 = rect
	pa, pb, pc = tri
	
	cw = dblcmp(cross(pb[0] - pa[0], pb[1] - pa[1], pc[0] - pb[0], pc[1] - pb[1]))
	if cw == 0:	# ���������Ϊ0
		return ()
	if cw < 0:
		pb, pc = pc, pb
		tri = (pa, pb, pc)

	rect_e = ((p0, p1), (p1, p2), (p2, p3), (p3, p0))
	tri_e = ((pa, pb), (pb, pc), (pc, pa))
	
	rect_p_seq = ([], [], [], [])
	tri_p_seq = ([], [], [])	
	rp_inside = [True] * 4
	pid = 0
	for j, te in enumerate(tri_e):
		tp_inside = True	# �����εĶ����Ƿ��ھ��ε��ڲ�
		for i, re in enumerate(rect_e):
			x, y, f1, f2, tp_on_left, rp_on_left = calc_seg_intersect(
				te[0][0], te[0][1], te[1][0], te[1][1],
				re[0][0], re[0][1], re[1][0], re[1][1],)
			if x is not None:
				tri_p_seq[j].append((f1, (x, y), pid, i))
				rect_p_seq[i].append((f2, (x, y), pid, j))
				pid += 1
			if not tp_on_left:	# ֻҪ�в�������һ���ߵ���࣬��out
				tp_inside = False
			if not rp_on_left:
				rp_inside[i] = False
		if tp_inside:
			tri_p_seq[j].append((0.0, tri[j], pid, None))
			pid += 1
	for i in range(4):
		if rp_inside[i]:
			rect_p_seq[i].append((0.0, rect[i], pid, None))
			pid += 1
	
	if pid < 3:
		return ()

	# ���򣬲���һ������Ϊ��ʼ��	
	start_pid = None
	seq = None
	p_index = None
	for i, seg_p_seq in enumerate(tri_p_seq):
		seg_p_seq.sort()
		if start_pid is None and seg_p_seq:
			start_pid = seg_p_seq[0][2]
			seq = tri_p_seq
			p_index = (i, 0)
	for i, seg_p_seq in enumerate(rect_p_seq):
		seg_p_seq.sort()
		if start_pid is None and seg_p_seq:
			start_pid = seg_p_seq[0][2]
			seq = rect_p_seq
			p_index = (i, 0)		

	ret = []
	while True:
		i, j = p_index
		f, p, pid, rev_i = seq[i][j]
		ret.append(p)
		
		# ��Ҫ�л�������һ��������
		if rev_i is not None and j == len(seq[i]) - 1:
			next_p_seq = seq[(i + 1) % len(seq)]
			if not next_p_seq or dblcmp(next_p_seq[0][0]) != 0:
				if seq == tri_p_seq:
					seq = rect_p_seq
				else:
					seq = tri_p_seq
				for k, (_f, _p, _pid, _rev_i) in enumerate(seq[rev_i]):
					if pid == _pid:
						i, j = p_index = (rev_i, k)
						break
		# ����һ�����㣬��ʱ����������
		j += 1
		if j < len(seq[i]):
			p_index = (i, j)
		else:
			i = i + 1
			if i >= len(seq):
				i = 0
			j = 0
			p_index = (i, j)
		try:
			pid = seq[i][j][2]
		except IndexError:
			print ("fucking algorithm error")
			return ()
		if pid == start_pid:
			break
	return ret
	
def decal(rect, tri):
	p0, p1, p2, p3 = rect
	pa, pb, pc = tri
	
	cw = dblcmp(cross(pb[0] - pa[0], pb[1] - pa[1], pc[0] - pb[0], pc[1] - pb[1]))
	if cw == 0:	# ���������Ϊ0
		return ()
	if cw < 0:
		pb, pc = pc, pb
		tri = (pa, pb, pc)

	rect_e = ((p0, p1), (p1, p2), (p2, p3), (p3, p0))
	tri_e = ((pa, pb), (pb, pc), (pc, pa))
	
	rect_p_seq = ([], [], [], [])
	tri_p_seq = ([], [], [])	
	rp_inside = [True] * 4
	pid = 0
	for j, te in enumerate(tri_e):
		tp_inside = True	# �����εĶ����Ƿ��ھ��ε��ڲ�
		for i, re in enumerate(rect_e):
			x, y, f1, f2, tp_on_left, rp_on_left = calc_seg_intersect(
				te[0][0], te[0][1], te[1][0], te[1][1],
				re[0][0], re[0][1], re[1][0], re[1][1],)
			if x is not None:
				z = te[0][2] * (1 - f1) + te[1][2] * f1
				tri_p_seq[j].append((f1, (x, y, z), pid, i))
				rect_p_seq[i].append((f2, (x, y, z), pid, j))
				pid += 1
			if not tp_on_left:	# ֻҪ�в�������һ���ߵ���࣬��out
				tp_inside = False
			if not rp_on_left:
				rp_inside[i] = False
		if tp_inside:
			tri_p_seq[j].append((0.0, tri[j], pid, None))	# ��Ȼ��z����
			pid += 1
	for i in range(4):
		if rp_inside[i]:
			x, y, _ = rect[i]
			z = calc_z_in_tri(x, y, tri[0], tri[1], tri[2])
			rect_p_seq[i].append((0.0, (x, y, z), pid, None))
			pid += 1
	
	if pid < 3:
		return ()

	# ���򣬲���һ������Ϊ��ʼ��	
	start_pid = None
	seq = None
	p_index = None
	for i, seg_p_seq in enumerate(tri_p_seq):
		seg_p_seq.sort()
		if start_pid is None and seg_p_seq:
			start_pid = seg_p_seq[0][2]
			seq = tri_p_seq
			p_index = (i, 0)
	for i, seg_p_seq in enumerate(rect_p_seq):
		seg_p_seq.sort()
		if start_pid is None and seg_p_seq:
			start_pid = seg_p_seq[0][2]
			seq = rect_p_seq
			p_index = (i, 0)		

	ret = []
	while True:
		i, j = p_index
		f, p, pid, rev_i = seq[i][j]
		ret.append(p)
		
		# ��Ҫ�л�������һ��������
		if rev_i is not None and j == len(seq[i]) - 1:
			next_p_seq = seq[(i + 1) % len(seq)]
			if not next_p_seq or dblcmp(next_p_seq[0][0]) != 0:
				if seq == tri_p_seq:
					seq = rect_p_seq
				else:
					seq = tri_p_seq
				for k, (_f, _p, _pid, _rev_i) in enumerate(seq[rev_i]):
					if pid == _pid:
						i, j = p_index = (rev_i, k)
						break
		# ����һ�����㣬��ʱ����������
		j += 1
		if j < len(seq[i]):
			p_index = (i, j)
		else:
			i = i + 1
			if i >= len(seq):
				i = 0
			j = 0
			p_index = (i, j)
		try:
			pid = seq[i][j][2]
		except IndexError:
			print ("fucking algorithm error")
			return ()
		if pid == start_pid:
			break
	return ret

def test():
	# 1.���������ı��ε��ڲ�
	assert (decal_2d(
		((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)),
		((0.3, 0.3), (0.7, 0.3), (0.5, 0.7)))) == [(0.3, 0.3), (0.7, 0.3), (0.5, 0.7)]
	assert (decal_2d(
		((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)),
		((0.3, 0.3), (0.5, 0.7), (0.7, 0.3)))) == [(0.3, 0.3), (0.7, 0.3), (0.5, 0.7)]	
	# 1.1 ���Σ��ж����ڱ��ϣ�����������˵���㶼���ڲ�
	#	һ�������ڱ���
	assert (decal_2d(
		((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)),
		((0.3, 0.3), (0.7, 0.3), (0.5, 1.0)))) == [(0.3, 0.3), (0.7, 0.3), (0.5, 1.0)]
	# ���������ڱ���
	assert (decal_2d(
		((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)),
		((0.3, 0.0), (0.7, 0.3), (0.5, 1.0)))) == [(0.3, 0.0), (0.7, 0.3), (0.5, 1.0)]
	# ����������ͬһ������
	assert (decal_2d(
		((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)),
		((0.3, 0.0), (0.7, 0.0), (0.5, 0.7)))) == [(0.3, 0.0), (0.7, 0.0), (0.5, 0.7)]	
	# ���������ڱ���
	assert (decal_2d(
		((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)),
		((0.3, 0.0), (1.0, 0.3), (0.5, 1.0)))) == [(0.3, 0.0), (1.0, 0.3), (0.5, 1.0)]
	# 1.2 ���Σ��ж����ڽ��ϣ�Ҳ�ж����ڱ��ϣ�����������˵���㶼���ڲ�
	# 1�ǣ�1��
	assert (decal_2d(
		((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)),
		((0.3, 0.3), (0.7, 0.3), (0.0, 1.0)))) == [(0.3, 0.3), (0.7, 0.3), (0.0, 1.0)]
	# 1�ǣ����ߣ�����������ͬһ������
	assert (decal_2d(
		((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)),
		((0.3, 0.0), (0.7, 0.0), (1.0, 1.0)))) == [(0.3, 0.0), (0.7, 0.0), (1.0, 1.0)]		
	# 2�ǣ�1��
	assert (decal_2d(
		((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)),
		((0.0, 0.0), (0.7, 0.3), (0.0, 1.0)))) == [(0.0, 0.0), (0.7, 0.3), (0.0, 1.0)]
	# 3�ǣ�0��
	assert (decal_2d(
		((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)),
		((0.0, 0.0), (1.0, 1.0), (0.0, 1.0)))) == [(0.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
	# 2.�ı����������ε��ڲ�
	assert (decal_2d(
		((0.5, 0.5), (0.6, 0.5), (0.6, 0.6), (0.5, 0.6)),
		((0.0, 0.0), (20.0, 0.0), (10.0, 30.0)))) == [(0.5, 0.5), (0.6, 0.5), (0.6, 0.6), (0.5, 0.6)]
	# 2.1 �ж����ڱ���
	assert (decal_2d(
		((0.5, 0.5), (0.6, 0.5), (0.6, 1.5), (0.5, 1.5)),
		((0.0, 0.0), (20.0, 0.0), (10.0, 30.0)))) == [(0.5, 1.5), (0.5, 0.5), (0.6, 0.5), (0.6, 1.5)]
	# 3.��������һ���������ı����ڲ�
	# 3.1 �������㶼��ͬһ������
	assert (decal_2d(
		((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)),
		((0.3, 1.3), (0.7, 1.3), (0.5, 0.7)))) == [(0.4, 1.0), (0.5, 0.7), (0.6, 1.0)]
	# 3.2 �������㶼�ڲ�ͬ���ϣ����Ǳ������ı��ε�һ����
	assert (decal_2d(
		((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)),
		((-5.0, 1.3), (0.7, 1.3), (0.5, 0.7)))) == [(0.0, 0.7545454545454545), (0.5, 0.7), (0.6, 1.0), (0.0, 1.0)]
	# 3.2 �������㶼�ڲ�ͬ���ϣ����ǲ��������ı��ε�һ����
	assert (decal_2d(
		((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)),
		((-0.5, 0.5), (0.7, 1.3), (0.5, 0.7)))) == [(0.0, 0.6), (0.5, 0.7), (0.6, 1.0), (0.2499999999999999, 1.0), (0.0, 0.8333333333333334)]
	# 3.3 �������㶼�ڲ�ͬ���ϣ��������ڶԲ�
	assert (decal_2d(
		((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)),
		((0.5, 0.5), (0.7, 1.3), (0.7, -1.3)))) == [(0.5, 0.5), (0.5555555555555556, 0.0), (0.7, 0.0), (0.7, 1.0), (0.625, 1.0)]
	# 4.��������2���������ı����ڲ�
	assert (decal_2d(
		((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)),
		((0.5, 0.5), (0.7, 0.5), (0.7, -1.3)))) == [(0.5, 0.5), (0.5555555555555556, 0.0), (0.7, 0.0), (0.7, 0.5)]
	# 4.1 ������һ���߶δ����˶Խ���
	assert (decal_2d(
		((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)),
		((0.5, 0.5), (0.7, 0.5), (2.0, 2.0)))) == [(0.5, 0.5), (0.7, 0.5), (1.0, 0.8461538461538461), (1.0, 1.0)]
	# 5. ������û��һ���������ı����ڲ�������ȫ����Խ���ı���
	# 5.1 �������������ཻ
	assert (decal_2d(
		((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)),
		((0.5, -0.5), (0.7, -0.5), (0.8, 2.0)))) == [(0.72, 0.0), (0.76, 1.0), (0.68, 1.0), (0.5599999999999999, 0.0)]
	# 5.2 �����ڵ��������ཻ
	assert (decal_2d(
		((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)),
		((0.5, -0.5), (1.2, 0.5), (1.7, -0.5)))) == [(1.0, 0.21428571428571433), (0.85, 0.0), (1.0, 0.0)]
	# 5.3 �����ڵ��������ཻ�������������㷴�����������ڲ�
	assert (decal_2d(
		((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)),
		((0.5, -0.5), (6.5, 6.5), (-100.0, 100.0)))) == [(0.9285714285714286, 0.0), (1.0, 0.08333333333333333), (1.0, 1.0), (0.0, 1.0),
(0.0, 0.0)]
	# ��������뵽��
	assert (decal_2d(
		((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)),
		((0.5, -0.2), (0.5, 1.2), (-0.5, 0.5)))) == [(0.5, 0.0), (0.5, 1.0), (0.2142857142857143, 1.0), (0.0, 0.85), (0.0, 0.15000000000000002), (0.21428571428571436, 0.0)]
	
if __name__ == '__main__':
	test()