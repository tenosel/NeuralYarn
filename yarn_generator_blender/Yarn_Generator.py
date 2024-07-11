import bpy
import bmesh
from math import pi, sin, cos, atan2, sqrt
from mathutils import Vector
import mathutils
import numpy as np
import os
import time
import datetime

rnd = np.random.RandomState(5)

m_to_mm = 1e-3 # meter to mili meter


def flyaway_mapping(hair_length_mean, hair_angle, amount, loop_prob, loop_length_mean, loop_distance_mean, loop_distance_std, fuzzyness):
	flyaways = {
			"loop_prob": loop_prob,
			"amount": amount,
			"hair_length": (hair_length_mean, 0.05),
			"hair_angle": hair_angle,
			"hair_squeeze": 1 + fuzzyness*1.5,
			"loop_length_short": (loop_length_mean, 0.01),
			"loop_distance_factor_short": (loop_distance_mean, loop_distance_std),
			"enable": True,
			"mapping_parameters" : { "amount": amount, "loop_prob" : loop_prob, "hair_length_mean": hair_length_mean, "hair_angle": hair_angle, "loop_length_mean": loop_length_mean,"loop_distance_mean": loop_distance_mean, "loop_distance_std": loop_distance_std, "fuzzyness": fuzzyness} 
		}
	return flyaways


def get_context():
	# create a context that works when blender is executed from the command line.
	# there should be a cleaner solution to this, but this copy'paste seems to work for now
	idx = bpy.context.window_manager.windows[:].index(bpy.context.window)
	window = bpy.context.window_manager.windows[idx]
	screen = window.screen
	views_3d = sorted(
			[a for a in screen.areas if a.type == 'VIEW_3D'],
			key=lambda a: (a.width * a.height))
	
	a = views_3d[0]
	# override
	o = {"window" : window,
		 "screen" : screen,
		 "area" : a,
		 "space_data": a.spaces.active,
		 "region" : a.regions[-1]
	}
	return o

def create_fiber(length=1.0, resolution=5):
	# https://b3d.interplanety.org/en/how-to-create-mesh-through-the-blender-python-api/
	
	obj_name = 'fiber'
	nodes = int(resolution * length / m_to_mm)
	
	vertices = []
	edges = []
	vertices.append([0, 0, 0])
	for i in range(1, nodes):
		vertices.append([0, 0, i*float(length)/float(nodes)])
		edges.append([i-1, i])
	faces = []

	new_mesh = bpy.data.meshes.new(obj_name)
	new_mesh.from_pydata(vertices, edges, faces)
	new_mesh.update()
	# make object from mesh
	new_object = bpy.data.objects.new(obj_name, new_mesh)
	
	c = bpy.context.collection
	c.objects.link(new_object)
		
	return new_object


def sample_points_circle(num_points, radius, middle_ply, jitter_xy, **kwargs):
	points = []
	for i in range(num_points):
		angle = float(i) / float(num_points) * 2*pi
		v = Vector([sin(angle), cos(angle), 0])
		v *= radius
		v += Vector([*rnd.normal(loc=0, scale=jitter_xy, size=2), 0])
		points.append(v)
	if middle_ply:
		points.append(Vector([0, 0, 0]))
	return points

def sample_points_area(num_points, radius, jitter_xy, **kwargs):
	points = []
	radius_scale = (num_points)**0.3 / radius
	for i in range(1, num_points+1):
		a = float(i) *0.137 * 2*pi
		r = float(i)** 0.3 / radius_scale
		v = Vector([sin(a)*r, cos(a)*r, 0])
		
		v += Vector([*rnd.normal(loc=0, scale=jitter_xy, size=2), 0])
		points.append(v)
	return points



def create_spiral(location=Vector([0, 0, 0]), dif_z=1.0, jitter_z=0, migration=0):

	override_context = get_context()
	turns = 48 # just needs to be sufficiently long
	
	radius = sqrt(location[0]**2 + location[1]**2)
	if dif_z < 0:
		dif_z = -1*dif_z
		sd='COUNTER_CLOCKWISE'
	else:
		sd='CLOCKWISE'
	bpy.ops.curve.spirals(override_context, spiral_type='ARCH',
		radius = radius, turns = turns, dif_z = dif_z,
		curve_type='BEZIER', handleType='AUTO', steps=16, spiral_direction=sd
		)
	bpy.ops.object.mode_set(mode='OBJECT') # or 'EDIT'
	obj = bpy.context.active_object
	
	object_rotation = atan2(location[1], location[0])
	obj.rotation_mode = "XYZ"
	obj.rotation_euler = [0, 0, object_rotation]
	#obj.location = location
	
	#set tilt
	obj.data.twist_mode = "Z_UP"
	
	# add some jitter to vertices
	# (this is always done even if jitter is 0, so that the random state is the same in both cases
	assert(len(obj.data.splines) == 1)
	phase_offset = rnd.uniform(0, 2*pi)
	phase_speed = rnd.uniform(0.0, 2)
	migration_strength = max(0, rnd.normal(loc=0.0, scale=migration))
	
	B = obj.data.splines[0].bezier_points
	for b in B:
		z = b.co[2]
		xy_scale = 1+ migration_strength*cos(phase_offset + z*phase_speed / m_to_mm)
		b.co[0] *= xy_scale
		b.co[1] *= xy_scale
		
		b.co[2] += (rnd.random()-0.5) * dif_z * jitter_z
	
	return obj
	

def build(params):
	curve_name="py_curve"
	
	if params["placement_params"]["type"] == "CIRCLE":
		fiber_starts = sample_points_circle(**params["placement_params"])
	elif params["placement_params"]["type"] == "AREA":
		fiber_starts = sample_points_area(**params["placement_params"])
	else:
		raise Exception("invalid placement_params type")
	
	fiber_obs = []
	
	
	if "line" in params["fiber_params"]:
		fiber_obj_template = create_fiber(length = params["fiber_params"]["line"]["length"], resolution=params["fiber_params"]["line"]["resolution"])
	elif "yarn" in params["fiber_params"]:
		fiber_obj_template = build(params["fiber_params"]["yarn"])
	else:
		raise Exception("invalid fiber_params")
	
	for i, pos in enumerate(fiber_starts):
		
		# copy the yarn template
		fiber_obj = fiber_obj_template.copy()
		fiber_obj.data = fiber_obj.data.copy() # also copy the data block
		# link to collection if need be
		bpy.context.collection.objects.link(fiber_obj)
		
		
		# don't apply ellipse to middle ply	
		if pos != Vector([0, 0, 0]):
			# turn fiber into an ellipsis
			bpy.ops.object.select_all(action='DESELECT')
			fiber_obj.select_set(True)
			#bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
			#fiber_obj.scale = (params["ellipse"], 1, 1)
			fiber_obj.scale = (params["ellipse"], 1, 1)
			bpy.ops.object.transform_apply(location = False, scale = True, rotation = False)
			
			# rotate to let the ellipse face the center
			fiber_obj.rotation_mode = "XYZ"
			fiber_obj.rotation_euler = [0, 0, atan2(pos[1], pos[0])]
			bpy.ops.object.transform_apply(location = False, scale = False, rotation = True)
			
			#bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
			#bpy.ops.object.origin_set(type='ORIGIN_CURSOR')


		# create curve and apply it to yarn
		curve_obj = create_spiral(location = pos, **params["curve_params"])
		
		# create and apply curve modifier   	
		bpy.context.view_layer.objects.active = fiber_obj   	
		bpy.ops.object.modifier_add(type='CURVE')
		mod = fiber_obj.modifiers[0]
		mod.name = "curve_mod"
		mod.object = curve_obj
		mod.deform_axis="POS_Z"
		bpy.ops.object.modifier_apply(modifier="curve_mod")
		
		# delete curve
		bpy.ops.object.select_all(action='DESELECT')
		curve_obj.select_set(True)
		bpy.ops.object.delete()
		
		# add processed yarn
		fiber_obs.append(fiber_obj)
		
		
	# delete fiber template
	bpy.ops.object.select_all(action='DESELECT')
	fiber_obj_template.select_set(True)
	bpy.ops.object.delete()
	
	# merge objects:
	bpy.context.view_layer.objects.active = fiber_obs[0]
	if len(fiber_obs) > 1:
		for o in fiber_obs:
			o.select_set(True)
		bpy.ops.object.join()
	
	result = bpy.context.view_layer.objects.active
	result.name = "YarnMesh"
	return result



def gen_flyaways(yarn_mesh, p, fiber_resolution, fiber_length, yarn_radius):
	
	# collect edges
	bm = bmesh.new()   # create an empty BMesh
	bm.from_mesh(yarn_mesh.data)   # fill it in from a Mesh
	
	bm.verts.ensure_lookup_table()
	bm.edges.ensure_lookup_table()
	
	# create object for flyaways
	new_mesh = bpy.data.meshes.new("flyaways")
	new_object = bpy.data.objects.new("flyaways", new_mesh)
	bpy.context.collection.objects.link(new_object)
	bm_f = bmesh.new() # create an empty BMesh to edit the new mesh
	bm_f.from_mesh(new_mesh)
	
	
	flyaways_created = 0
	amount = int(p["amount"] * fiber_length)
	for flyaway in range(amount):
	
		loop = True if rnd.uniform(0, 1) < p["loop_prob"] else False
		squeeze_factorx = 2
		if loop:
			long_loop = True if rnd.uniform(0, 1) < 0.04 else False 
			
			squeeze_factor = 1
			
			if long_loop:
				flyaway_length = p["loop_length_short"][0]*2 
				distance = rnd.normal(p["loop_distance_factor_short"][0]*2, p["loop_distance_factor_short"][1])
			else:
				flyaway_length = rnd.normal(p["loop_length_short"][0], p["loop_length_short"][1])
			
				dist = rnd.normal(p["loop_distance_factor_short"][0], p["loop_distance_factor_short"][1])
				
				dif = dist - p["loop_distance_factor_short"][0]
				if dif < 0:
					distance = p["loop_distance_factor_short"][0] - dif
				else:
					distance = dist
					
			distance = distance/10000.0
			
		else:
			long_hair = True if rnd.uniform(0, 1) < 0.04 else False

			squeeze_factor = p["hair_squeeze"]
			squeeze_factorx = -1
			
			if long_hair:
				flyaway_length = rnd.normal(p["hair_length"][0]*3, p["hair_length"][1])
			else:
				flyaway_length = rnd.normal(p["hair_length"][0], p["hair_length"][1])
				
		
		num_vertices = round(flyaway_length * fiber_resolution * 1000)
		
		# add vertices to make sure flyaways are properly connected to the yarn
		if loop:
			num_vertices += 2
		else:
			num_vertices += 1
			
	
		# --------------- select a vertex strip to generate flyaway from --------------- 
		last_v = bm.verts[rnd.randint(0, len(bm.verts))]
		if len(last_v.link_edges) == 0:
			continue
		if len(last_v.link_edges) > 1:
			last_edge = last_v.link_edges[0] if rnd.uniform(0,1)>0.5 else last_v.link_edges[1] # this decides, if we go up or down
		else:
			last_edge = last_v.link_edges[0]
		v_list = [last_v]
		e_list = []
		
		for i in range(num_vertices):
			if len(last_v.link_edges) < 2:
				break
			next_edge = last_v.link_edges[0] if last_v.link_edges[0] is not last_edge else last_v.link_edges[1]
			e_list.append(next_edge)
			if len(next_edge.verts) < 2:
				break
			next_v = next_edge.verts[0] if next_edge.verts[0] is not last_v else next_edge.verts[1]
			v_list.append(next_v)
			last_v = next_v
			last_edge = next_edge
		if len(v_list) < num_vertices:
			continue
		#________________________________________________________________
	
		dir = Vector([v_list[-1].co[0], v_list[-1].co[1], 0])
		#distance += dir.length # properly move all vertices to the outside of the yarn
		dir = dir.normalized()
		
		# copy vertices to new BMesh
		v_list_f = []
		e_list_f = []
		for v in v_list:
			v_list_f.append(bm_f.verts.new(v.co))
		for i in range(len(v_list_f)-1):
			e_list_f.append(bm_f.edges.new((v_list_f[i], v_list_f[i+1])))
	
	
		# squeeze a bit to make them more curly
		z_ref = v_list_f[0].co[2]
		for i, v in enumerate(v_list_f):
			v.co[2] = z_ref + (v.co[2]-z_ref) / squeeze_factor
			
			
		x_ref = v_list_f[0].co[0]
		for i, v in enumerate(v_list_f): 
			v.co[0] = x_ref + (v.co[0]-x_ref) / squeeze_factorx
			
		
		if loop:
			v_list = v_list_f[1:-1]
			e_list = e_list_f[1:-1]
			# create some sort of arc
			for i, v in enumerate(v_list):
				v.co += dir * sin(i * pi / len(v_list)) * distance
		else: # open ended flyaway
			v_list = v_list_f[1:]
			e_list = e_list_f[1:]
			angle = p["hair_angle"] 
			bmesh.ops.rotate(bm_f,
				cent = v_list[0].co,
				matrix = mathutils.Matrix.Rotation(angle, 3, dir),
				verts = v_list)
		flyaways_created += 1
	print("Created {} of {} flyaways".format(flyaways_created, amount))
	
	bm_f.to_mesh(new_mesh)
	new_object.location = yarn_mesh.location
	return new_object
	


def convert_to_curve(obj, ellipse_x = 0.015, ellipse_y = 0.015, curve_name='Fiber_Curve'):
	
	bpy.context.view_layer.objects.active = obj
	
	# convert to curve
	bpy.ops.object.select_all(action='DESELECT')
	obj.select_set(True)
	bpy.ops.object.convert(target='CURVE')
	
	
	bpy.ops.object.mode_set(mode='EDIT')
	bpy.ops.curve.spline_type_set(type='NURBS')
	bpy.ops.object.mode_set(mode='OBJECT')
	
	bpy.ops.object.shade_smooth()
	
	# fiber thickness
	obj.data.bevel_mode = 'OBJECT'
	if curve_name not in bpy.data.objects:
		raise Exception("curve object not found: " + curve_name)
	curve_obj = bpy.data.objects[curve_name]
	obj.data.bevel_object = curve_obj
	curve_obj.scale[0] = ellipse_x
	curve_obj.scale[1] = ellipse_y
	
	obj.data.use_fill_caps = True
	

def create_material(mat_name = "yarn", type="direct", **kwargs):
	
	# check if it already exists
	mat = bpy.data.materials.get(mat_name)
	if mat is not None:
		bpy.data.materials.remove(mat)
		
	# create material
	mat = bpy.data.materials.new(name=mat_name)
	mat.use_nodes = True
	node_tree = mat.node_tree
	nodes = node_tree.nodes
	
	n = nodes.get("Principled BSDF")
	if n:
		nodes.remove(n)
	
	bsdf = nodes.new(type="ShaderNodeBsdfHairPrincipled")

	if "direct" == type:
		bsdf.parametrization="COLOR"
	
		# yarn color
		bsdf.inputs[0].default_value = kwargs["color"]

		# Roughness
		bsdf.inputs[5].default_value = kwargs["roughness"]
		
		# Radial Roughness
		bsdf.inputs[6].default_value = kwargs["radial_roughness"]
		
		# IOR
		bsdf.inputs[8].default_value = kwargs["ior"]
		
		# random_roughness
		bsdf.inputs[11].default_value = kwargs["random_roughness"]

		output = nodes.get("Material Output")
		node_tree.links.new(bsdf.outputs[0], output.inputs[0])
		
		# viewport options
		mat.diffuse_color = kwargs["color"]
	elif "melanin" == type:
		bsdf.parametrization="MELANIN"
		
		# melanin
		bsdf.inputs[1].default_value = kwargs["melanin"]

		# melanin redness
		bsdf.inputs[2].default_value = kwargs["melanin_redness"]
		
		# tint
		bsdf.inputs[3].default_value = kwargs["tint"]
		
		# roughness
		bsdf.inputs[5].default_value = kwargs["roughness"]
		
		# radial roughness
		bsdf.inputs[6].default_value = kwargs["radial_roughness"]
		
		# ior
		bsdf.inputs[8].default_value = kwargs["ior"]
		
		# random_color
		bsdf.inputs[10].default_value = kwargs["random_color"]
		
		# random_roughness
		bsdf.inputs[11].default_value = kwargs["random_roughness"]
		
		output = nodes.get("Material Output")
		node_tree.links.new(bsdf.outputs[0], output.inputs[0])
		
		# viewport options
		mat.diffuse_color = kwargs["tint"]

	else:
		raise Exception("invalid material type: "+type)

	return mat


def apply_material(yarn, material):
	bpy.ops.object.select_all(action='DESELECT')
	yarn.select_set(True)
		
	#If a material is already assigned (material slots is not empty)
	if yarn.material_slots:
		#Assign the material to the first slot
		yarn.material_slots[0].material = material
	#If no material is assigned
	else:
		#Create a new material (link/slot) for the object
		yarn.data.materials.append(material)



def render(name):
	time_start = time.time()
	
	if name.endswith(".exr"):
		bpy.context.scene.render.image_settings.file_format="OPEN_EXR"
	elif name.endswith(".png"):
		bpy.context.scene.render.image_settings.file_format="PNG"
	else:
		raise Exception("unknown file format")
	bpy.context.scene.render.filepath=name
	bpy.ops.render.render(write_still=True)
	time_elapsed = time.time() - time_start
	
	print("Rendering took {:.2f} seconds".format(time_elapsed))
	#with open("log.txt", "a") as f:
		#f.write("{}: Rendering took {:.2f} seconds\n".format(datetime.datetime.now(), time_elapsed))



def carbage_collection():
	for block in bpy.data.meshes:
		if block.users == 0:
			bpy.data.meshes.remove(block)

	for block in bpy.data.materials:
		if block.users == 0:
			bpy.data.materials.remove(block)

	for block in bpy.data.textures:
		if block.users == 0:
			bpy.data.textures.remove(block)

	for block in bpy.data.images:
		if block.users == 0:
			bpy.data.images.remove(block)
			
	for block in bpy.data.curves:
		if block.users == 0:
			bpy.data.curves.remove(block)

def clear_collection():
	print("\n\nscript started")
	
	# ensure clear collection Yarn
	collection = bpy.data.collections.get('Yarn')
	if collection:
		for obj in collection.objects:
			bpy.data.objects.remove(obj, do_unlink=True)
		#bpy.data.collections.remove(collection)
		layer_collection = bpy.context.view_layer.layer_collection.children[collection.name]
		bpy.context.view_layer.active_layer_collection = layer_collection
	else:
		new_collection = bpy.data.collections.new('Yarn')
		bpy.context.scene.collection.children.link(new_collection)
		layer_collection = bpy.context.view_layer.layer_collection.children[new_collection.name]
		bpy.context.view_layer.active_layer_collection = layer_collection
	carbage_collection()


def sample_material_properties(yarns):
	values = [0, 0.2, 0.3, 0.5, 0.8]
	for roughness in values:
		for radial_roughness in values:
			
			bpy.data.materials.remove(bpy.data.materials["yarn"], do_unlink=True)
			blender_mat = create_material("yarn", roughness, radial_roughness)
			for yarn in yarns:
				apply_material(yarn, blender_mat)
			fn = os.path.join(bpy.path.abspath("//"), "materials", "mat_r_{:.2f}_rr_{:.2f}.png".format(roughness, radial_roughness))
			render(fn)

def adjust_level_units(placement_params):
	f = m_to_mm
	placement_params["placement_params"]["radius"] *= f
	placement_params["placement_params"]["jitter_xy"] *= f
	placement_params["curve_params"]["dif_z"] *= f
	#placement_params["curve_params"]["jitter_z"] *= f # DONT adjust jitter_z, it is a factor not an offset
	
	if "line" in placement_params["fiber_params"]:
		placement_params["fiber_params"]["line"]["length"] *= f
	elif "yarn" in placement_params["fiber_params"]:
		adjust_level_units(placement_params["fiber_params"]["yarn"])
	else:
		raise Exception("unknown fiber_params")
		
	
def adjust_units(levels_description, material_properties, flyaways, other_properties):
	f = m_to_mm
	adjust_level_units(levels_description)
	
	flyaways["hair_length"]   	= [x*f for x in flyaways["hair_length"]]
	flyaways["loop_length_short"] = [x*f for x in flyaways["loop_length_short"]]
	
	other_properties["fiber_thickness_x"] *= f
	other_properties["fiber_thickness_y"] *= f
	other_properties["flyaway_thickness_x"] *= f
	other_properties["flyaway_thickness_y"] *= f

def get_fiber_resolution(levels_description):
	if "line" in levels_description["fiber_params"]:
		return levels_description["fiber_params"]["line"]["resolution"]
	elif "yarn" in levels_description["fiber_params"]:
		return get_fiber_resolution(levels_description["fiber_params"]["yarn"])
	else:
		raise Exception("unknown fiber_params")
		
def get_fiber_length(levels_description):
	if "line" in levels_description["fiber_params"]:
		return levels_description["fiber_params"]["line"]["length"]
	elif "yarn" in levels_description["fiber_params"]:
		return get_fiber_resolution(levels_description["fiber_params"]["yarn"])
	else:
		raise Exception("unknown fiber_params")


def create_yarn(levels_description, material_properties, flyaways, other_properties, yarn_location = None):
	time_start = time.time()

	adjust_units(levels_description, material_properties, flyaways, other_properties)
	
	material = create_material(**material_properties)
	yarn = build(levels_description)
	
	if flyaways["enable"]:
		flyaways_obj = gen_flyaways(yarn,
			flyaways,
			fiber_resolution = get_fiber_resolution(levels_description),
			fiber_length = get_fiber_length(levels_description),
			yarn_radius = levels_description["placement_params"]["radius"])
		convert_to_curve(
			flyaways_obj,
			ellipse_x = other_properties["flyaway_thickness_x"],
			ellipse_y = other_properties["flyaway_thickness_y"],
			curve_name="Flyaway_Curve"
		)
		apply_material(flyaways_obj, material)
	else:
		flyaways_obj = None
	convert_to_curve(
		yarn,
		ellipse_x = other_properties["fiber_thickness_x"],
		ellipse_y = other_properties["fiber_thickness_y"],
		curve_name="Fiber_Curve"
	)
	apply_material(yarn, material)
	
	if yarn_location is not None:
		yarn.location = yarn_location
		if flyaways_obj is not None:
			flyaways_obj.location = yarn_location
	
	bpy.data.curves["YarnMesh"].resolution_u = 6 
	bpy.data.curves["flyaways"].resolution_u = 6 
	
	time_elapsed = time.time() - time_start
	print("Generation took {:.2f} seconds".format(time_elapsed))

