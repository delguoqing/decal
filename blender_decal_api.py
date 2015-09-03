# -*- coding: gbk -*-
import bpy
import bmesh
import mathutils
import decal_algo
import common_algo

def project_decal_old(mesh_src, mesh_dst):
	if isinstance(mesh_src, str):
		mesh_src = bpy.data.meshes.get(mesh_src)
		print (mesh_src)
	if isinstance(mesh_dst, str):
		mesh_dst = bpy.data.meshes.get(mesh_dst)
		print (mesh_dst)
	if mesh_src is None or mesh_dst is None:
		print ("src or dst is None")
		return
	
	bm_src = bmesh.new()
	bm_src.from_mesh(mesh_src)
	
	bm_dst = bmesh.new()
	bm_dst.from_mesh(mesh_dst)
	
	bm_out = bmesh.new()
	
	for face_src in bm_src.faces:
		verts_src = []
		for loop_src in face_src.loops:
			verts_src.append(loop_src.vert.co)
		for face_dst in bm_dst.faces:
			verts_dst = []
			for loop_dst in face_dst.loops:
				verts_dst.append(loop_dst.vert.co)
				
			# 目前做了这个假设，所以先测试到这一步
			if len(verts_src) != 4 or len(verts_dst) != 3:
				continue
			
			# adapt arguments && run
			rect = []
			for co in verts_src:
				rect.append((co.x, co.y, co.z))
			tri = []
			for co in verts_dst:
				tri.append((co.x, co.y, co.z))
			res = decal_algo.decal(rect, tri)
			# add verts
			for x, y, z in res:
				bm_out.verts.new((x, y, z + 0.01))
			# add face (all these verts will be on the same plane, so let's blender do triangulate for us)
			if res:
				bm_out.faces.new(bm_out.verts[-len(res):])
	
	print(len(bm_out.verts))
	if len(bm_out.verts) >= 0:
		mesh = bpy.data.meshes.new(name="_decal")
		bm_out.to_mesh(mesh)
		obj = bpy.context.scene.objects.get("_decal")
		if obj is None:
			obj = bpy.data.objects.new("_decal", mesh)
			bpy.context.scene.objects.link(obj)
		else:
			obj.data = mesh
	
def norm_model(model_or_name):
	if isinstance(model_or_name, str):
		return bpy.data.objects.get(model_or_name)
	return model_or_name
	
def project_model(model_src, model_dst):
	model_src = norm_model(model_src)
	model_dst = norm_model(model_dst)
	if not (model_src and model_dst):
		print ("model_src or model_dst is None", model_src, model_dst)
		return
	
	mesh_src = model_src.data
	mesh_dst = model_dst.data
	
	bm_src = bmesh.new()
	bm_src.from_mesh(mesh_src)
	
	bm_dst = bmesh.new()
	bm_dst.from_mesh(mesh_dst)
	
	bm_out = bmesh.new()
	
	# world to decal matrix
	if hasattr(bm_src.faces, "ensure_lookup_table"):
		bm_src.faces.ensure_lookup_table()
	
	o = model_src.matrix_world * bm_src.faces[0].loops[0].vert.co
	a = model_src.matrix_world * bm_src.faces[0].loops[-1].vert.co
	b = model_src.matrix_world * bm_src.faces[0].loops[1].vert.co
	oa = a - o
	axis_x = oa.normalized()
	ob = b - o
	axis_y = ob.normalized()
	axis_z = oa.cross(ob).normalized()
	
	# uv
	uv_layer = bm_src.loops.layers.uv.active
	uv_o = bm_src.faces[0].loops[0][uv_layer].uv
	uv_a = bm_src.faces[0].loops[-1][uv_layer].uv
	uv_b = bm_src.faces[0].loops[1][uv_layer].uv
	
	world_to_decal = mathutils.Matrix()
	world_to_decal[0][:] = (axis_x.x, axis_x.y, axis_x.z, 0.0)
	world_to_decal[1][:] = (axis_y.x, axis_y.y, axis_y.z, 0.0)
	world_to_decal[2][:] = (axis_z.x, axis_z.y, axis_z.z, 0.0)
	world_to_decal[3][:] = (0.0,      0.0,      0.0,      1.0)
	world_to_decal *= mathutils.Matrix.Translation(-o)
	
	# decal to world matrix
	decal_to_world = world_to_decal.inverted()
	
	# src to decal matrix
	src_to_decal = world_to_decal * model_src.matrix_world
	
	# dst to decal matrix
	dst_to_decal = world_to_decal * model_dst.matrix_world
	
	added_vert_count = 0
	uvs = []
	
	for face_src in bm_src.faces:
		verts_src = []
		for loop_src in face_src.loops:
			verts_src.append(src_to_decal * loop_src.vert.co)
		for face_dst in bm_dst.faces:
			verts_dst = []
			for loop_dst in face_dst.loops:
				verts_dst.append(dst_to_decal * loop_dst.vert.co)
				
			# 目前做了这个假设，所以先测试到这一步
			if len(verts_src) != 4 or len(verts_dst) != 3:
				continue
			
			# adapt arguments && run
			rect = []
			#print ("rect:")
			for co in reversed(verts_src):
				#print ("\t", co)
				rect.append((co.x, co.y, co.z))
			tri = []
			#print ("tri:")
			for co in verts_dst:
				#print ("\t", co)
				tri.append((co.x, co.y, co.z))
			res = decal_algo.decal(rect, tri)
			# add verts
			for x, y, z in res:
				#print (x, y)
				import common_algo
				#assert common_algo.dblcmp(x) >= 0 and common_algo.dblcmp(y) >= 0, "should x, y all be positive in decal space"
				
				fx = x / oa.length
				u = uv_o.x * (1 - fx) + uv_a.x * fx
				fy = y / ob.length
				v = uv_o.y * (1 - fy) + uv_b.y * fy
				uvs.append((u, v))
				print ("u, v:", u, v)
				vec_decal = mathutils.Vector((x, y, z))
				vec_world = decal_to_world * vec_decal
				# should offset along which direction?
				vec_world.z += 0.01
				bm_out.verts.new(vec_world)
				
			added_vert_count += len(res)
			# SB blender
			bm_out.verts.index_update()
			if hasattr(bm_out.verts, "ensure_lookup_table"):
				bm_out.verts.ensure_lookup_table()
				
			# add face (all these verts will be on the same plane, so let's blender do triangulate for us)
			if res:
				bm_out.faces.new(bm_out.verts[-len(res):])

	# output 	
	print(len(bm_out.verts), added_vert_count)
	if len(bm_out.verts) >= 0:
		mesh = bpy.data.meshes.new(name="_decal")
		bm_out.to_mesh(mesh)
		
		# it seems like that bmesh can't modify uv at the moment
		mesh.uv_textures.new("tex_decal")
		for loop in mesh.loops:
			setattr(mesh.uv_layers[0].data[loop.index], "uv", uvs[loop.vertex_index])
			print (uvs[loop.vertex_index])
		for uv_face in mesh.uv_textures.active.data:
			uv_face.image = bpy.data.images["Checker"]
		
		obj = bpy.context.scene.objects.get("_decal")
		if obj is None:
			obj = bpy.data.objects.new("_decal", mesh)
			bpy.context.scene.objects.link(obj)
		else:
			obj.data = mesh
		
