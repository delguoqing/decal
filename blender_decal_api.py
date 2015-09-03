# -*- coding: gbk -*-
import bpy
import bmesh
import decal_algo

def project_decal(mesh_src, mesh_dst):
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