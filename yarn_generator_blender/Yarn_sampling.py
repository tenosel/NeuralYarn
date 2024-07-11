
import bpy
import os
import sys
import numpy as np
import json
from math import pi

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path: # for local includes
    sys.path.append(dir)

import Yarn_Generator


def generate_yarn_parameter_sample(sample_seed):
	rnd = np.random.RandomState(seed=sample_seed)
	
	curve_jitter_z = 0.02
	
	#-------------
	#params
	
	curve_jitter_xy = rnd.uniform(0, 0.03)
	curve_jitter_xy_l2 = rnd.uniform(0, 0.02)
	migration = rnd.uniform(0, 0.3)
	fiber_thickness_x = rnd.uniform(0.006, 0.01) 
	fiber_thickness_y = min(rnd.uniform(fiber_thickness_x, fiber_thickness_x*2.5), 0.02)
	num_plys = rnd.randint(2, 7)
	middle_ply = False
	#cw = [-1, 1]
	#clockwise = rnd.choice(cw)
	
	num_fibers = rnd.randint(40, 200)
	
	if num_plys == 2:
		r_fraction = rnd.uniform(0.67, 0.9)
	elif num_plys == 3:
		r_fraction = rnd.uniform(0.72, 0.91)
	elif num_plys > 3:
		r_fraction = rnd.uniform(0.85, 0.95)
	
	gangwinkel_ply = rnd.uniform(50, 81)*(np.pi/180) # all angles are radians
	area_frac_ply = rnd.uniform(0.035, 0.215)
	rx = np.sqrt(num_fibers * fiber_thickness_x * fiber_thickness_y/ area_frac_ply / r_fraction)
	if num_plys > 4:
		area_frac_yarn = rnd.uniform(0.65, 0.82)
	else:
		area_frac_yarn = rnd.uniform(0.55, 0.82) 
	ex_2 = rx / np.sin(gangwinkel_ply)
	ey_2 = r_fraction * ex_2
	yarn_radius = np.sqrt(num_plys * ex_2 * ey_2 / area_frac_yarn) - ey_2
	alpha_ply = 2 * np.pi * yarn_radius * np.tan(gangwinkel_ply) #*clockwise
	gangwinkel = rnd.uniform(50, 81)*(np.pi/180)
	alpha = -1 * 2 * np.pi * rx * np.tan(gangwinkel)

	#-------------

	l1  = {
	"name": "l1",
	"placement_params": {
		"type": "AREA",
		"num_points" : num_fibers, 
		"radius": rx, 
		"jitter_xy" : curve_jitter_xy
		},
	"curve_params" : {
		"dif_z" : alpha, 
		"jitter_z" : curve_jitter_z,
		"migration": migration
		},
	"fiber_params" : {
		"line": {
			"length": 60.0,
			"resolution": 4,
			}
		},
	"ellipse": 1
	}
	
	l2  = {
	"name": "l2",
	"placement_params": {
		"type": "CIRCLE",
		"num_points" : num_plys, 
		"radius": yarn_radius, 
		"middle_ply": middle_ply, 
		"jitter_xy" : curve_jitter_xy_l2
		},
	"curve_params" : {
		"dif_z" : alpha_ply,
		"jitter_z" : 0,
		"migration": 0
		},
	"fiber_params" : {
		"yarn" : l1
		},
	"ellipse": r_fraction, 
	}
	
	
	material_type = "direct"	#rnd.choice(["direct", "melanin"])
	if "direct" == material_type:
		material_props = {
			"type": material_type,
			"roughness": rnd.uniform(0.001, 0.6),#(0.10, 0.25),
			"radial_roughness": rnd.uniform(0.2, 0.99),#(0.15, 0.40),
			"ior": rnd.uniform(1.4, 1.62),
			"color" : (*rnd.uniform(0, 1, size=3), 1),
			"random_roughness": rnd.uniform(0, 1)
		}
	elif "melanin" == material_type:
		material_props = {
			"type": material_type,
			"melanin": rnd.uniform(0.0, 0.7),#(0.0, 0.3),
			"melanin_redness": rnd.uniform(0, 1),#(0.1, 0.5),
			"tint": (*rnd.uniform(0, 1, size=3), 1),
			"roughness": rnd.uniform(0.05, 0.6),#(0.10, 0.25),
			"radial_roughness": rnd.uniform(0.1, 0.9),#(0.15, 0.40),
			"ior": rnd.uniform(1.4, 1.62),
			"random_color" : rnd.uniform(0, 0.75),
			"random_roughness" : rnd.uniform(0, 0.75),
		}
	
	loop_length_short = abs(l2["curve_params"]["dif_z"])
	whole_radius = yarn_radius + rx * r_fraction
	ldm = rnd.uniform(whole_radius*3, whole_radius*20)
	t = whole_radius*20 - ldm
	bound = min(5, t)
	bound_amount = min(num_fibers * num_plys*2, 300)
	lds = rnd.uniform(0.01, bound)
	flyaways = Yarn_Generator.flyaway_mapping(
		hair_length_mean = rnd.uniform(whole_radius*1.5, whole_radius*8),
		hair_angle = rnd.uniform(0.05, pi/2),
		amount = rnd.uniform(30, bound_amount), 
		loop_prob = rnd.uniform(0.35,0.65), 
		loop_length_mean = rnd.uniform(loop_length_short*0.6, loop_length_short*1.3),
		loop_distance_mean = ldm,  
		loop_distance_std = lds,
		fuzzyness = rnd.uniform(0, 1),
		)
	
	other = {
		"fiber_thickness_x" : fiber_thickness_x,
		"fiber_thickness_y" : fiber_thickness_y,
		"flyaway_thickness_x" : fiber_thickness_x,
		"flyaway_thickness_y" : fiber_thickness_y,
		}
		
	return l2, material_props, flyaways, other


# puts everything changed by adjust_scene into its normal values
def reset_scene(scene):
	# Wall material
	w = bpy.data.materials["Wall"]
	w.node_tree.nodes["Principled BSDF"].inputs[0].default_value = [0.01, 0.01, 0.01, 1.0] # main color
	w.node_tree.nodes["Normal Map"].inputs[0].default_value = 0.2 # normal map strength color
	w.node_tree.nodes["Noise Texture"].inputs[2].default_value = 10 # spatial noise scale
	w.node_tree.nodes["Noise Offset"].inputs[1].default_value = [0, 0, 0] # 3d seed for noise vector

	if "lab_01" == scene:
		bpy.data.objects["Camera"].location = (0, 0.175, 0.1)
		bpy.data.cameras["Camera"].lens = 950
		
		# light
		bpy.data.lights["Area_Main"].energy   = 6
		bpy.data.lights["Area_Second"].energy = 6
		bpy.data.lights["Area_Main"].color = (1, 1, 1)
		bpy.data.lights["Area_Second"].color = (1, 1, 1)
	else:
		raise Exception("unknown scene :P")

def adjust_scene(scene, sample_seed):
	rnd = np.random.RandomState(seed=sample_seed)
	reset_scene(scene)

	# Wall material
	w = bpy.data.materials["Wall"]
	w.node_tree.nodes["Principled BSDF"].inputs[0].default_value = [*rnd.normal(loc=0.01, scale=0.001, size=3), 1.0] # main color
	w.node_tree.nodes["Normal Map"].inputs[0].default_value      = rnd.normal(loc=0.2, scale=0.05, size=1) # normal map strength color
	w.node_tree.nodes["Noise Texture"].inputs[2].default_value   = rnd.normal(loc=10, scale=5) # spatial noise scale
	w.node_tree.nodes["Noise Offset"].inputs[1].default_value    = rnd.uniform(0, 100, size=3) # 3d seed for noise vector
		
	if "lab_01" == scene:
	
		# light
		bpy.data.lights["Area_Main"].energy   = rnd.normal(loc=6.0, scale=2)
		bpy.data.lights["Area_Second"].energy = rnd.normal(loc=6.0, scale=2)
		bpy.data.lights["Area_Main"].color    = rnd.uniform(0.9, 1, size=3)
		bpy.data.lights["Area_Second"].color  = rnd.uniform(0.9, 1, size=3)
	else:
		raise Exception("unknown scene")

def create_images(scene, output_dir, amount=100, start=0):
	os.makedirs(output_dir, exist_ok  = True)

	def output_file_json(i):
		return os.path.join(bpy.path.abspath("//"), output_dir, "Yarn_{:04}.json".format(i))
	def output_file_render(i):
		return os.path.join(bpy.path.abspath("//"), output_dir, "Yarn_{:04}.png".format(i)) 
	
	yarn_location = None
	if "lab_01" == scene:
		yarn_location = (0, 19*0.025, 0.085)

	
	# check where we should start
	while os.path.isfile(output_file_json(start)):
		start += 1
		
	for i in range(start, start+amount):
		if os.path.isfile(output_file_json(i)):
			print("skipping ", i)
			continue
	
		print("GENERATING SAMPLE", i)
		p = generate_yarn_parameter_sample(i)
		with open(output_file_json(i), "wt") as f:
			def convert(o):
				if isinstance(o, np.int32): return int(o)
				if isinstance(o, np.bool_): return bool(o)
				print(type(o))
				raise TypeError
			d = {"fiber": p[0], "material": p[1], "flyaways": p[2], "thickness" : p[3]}
			json.dump(d, f, indent="\t", default=convert)
		Yarn_Generator.clear_collection()
		Yarn_Generator.create_yarn(*p, yarn_location=yarn_location)
		adjust_scene(scene, i)
		
		Yarn_Generator.render(output_file_render(i))
	print("all done")
	


if __name__ == "__main__":
	
	create_images(scene="lab_01", output_dir = "Generated_flyawaymodel", amount=1, start=600000)
	
