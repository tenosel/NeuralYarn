import numpy as np

def default_material():
	
	material_props = {
    "type": "direct",
    "roughness": 0.15,
    "radial_roughness": 0.25,
    "ior": 1.4,
    "color" : (0.178, 0.178, 0.2, 1),
    "random_roughness": 0
	}	
	return material_props

def get_light():
	rnd = np.random.RandomState(seed=20)
	curve_jitter_z = 0.02
	curve_jitter_xy = 1.0824423e-02
	curve_jitter_xy_l2 = 0
	migration = 2.3299906e-01
	fiber_thickness_x = 0.01
	fiber_thickness_y = 0.018
	l1  = {
	"name": "l1",
	"placement_params": {
		"type": "AREA",
		"num_points" : 93,
		"radius": 0.38002256,
		"jitter_xy" : curve_jitter_xy
		},
	"curve_params" : {
		"dif_z" : -3.6543832,
		"jitter_z" : curve_jitter_z,
		"migration": migration
		},
	"fiber_params" : {
		"line": {
			"length": 40.0,
			"resolution": 4,
			}
		},
	"ellipse": 1,
	}
	
	l2  = {
	"name": "l2",
	"placement_params": {
		"type": "CIRCLE",
		"num_points" : 2,
		"radius": 0.36877498,
		"middle_ply": False,
		"jitter_xy" : curve_jitter_xy_l2
		},
	"curve_params" : {
		"dif_z" : 10.704875,
		"jitter_z" : 0,
		"migration": 0
		},
	"fiber_params" : {
		"yarn" : l1
		},
	"ellipse": 0.83759594
	}
	
	material_props = default_material()
	
	
	flyaways = {
		"loop_prob": 4.6834272e-01,
		"amount": 223,
		"hair_length": (4.7458582, 0.05),
		"hair_angle": 1.1224194,
		"hair_squeeze": 1 +4.8124412e-01*1.5,
		"loop_length_short": (8.1423216, 0.01),
		"loop_distance_factor_short": (1.3118077e+01, 2.0849290),
		"enable": True
	}
	
	other = {
		"fiber_thickness_x" : fiber_thickness_x,
		"fiber_thickness_y" : fiber_thickness_y,
		"flyaway_thickness_x" : fiber_thickness_x,
		"flyaway_thickness_y" : fiber_thickness_y,
		}
		
	return l2, material_props, flyaways, other

def get_orange():
	rnd = np.random.RandomState(seed=20)
	curve_jitter_z = 0.02
	curve_jitter_xy = 1.4676226e-02
	curve_jitter_xy_l2 = 0
	migration = 1.9812550e-01
	fiber_thickness_x = 0.01
	fiber_thickness_y = 0.018
	l1  = {
	"name": "l1",
	"placement_params": {
		"type": "AREA",
		"num_points" : 52,
		"radius": 0.3090794,
		"jitter_xy" : curve_jitter_xy
		},
	"curve_params" : {
		"dif_z" : -3.1808367,
		"jitter_z" : curve_jitter_z,
		"migration": migration
		},
	"fiber_params" : {
		"line": {
			"length": 40.0,
			"resolution": 4,
			}
		},
	"ellipse": 1
	}
	
	l2  = {
	"name": "l2",
	"placement_params": {
		"type": "CIRCLE",
		"num_points" : 4,
		"radius": 0.44024545,
		"middle_ply": False,
		"jitter_xy" : curve_jitter_xy_l2
		},
	"curve_params" : {
		"dif_z" : 6.9948416,
		"jitter_z" : 0,
		"migration": 0
		},
	"fiber_params" : {
		"yarn" : l1
		},
	"ellipse": 0.88865435
	}
	
	material_props = default_material()
	
	
	flyaways = {
		"loop_prob": 5.4171228e-01,
		"amount": 163,
		"hair_length": (3.5033882, 0.05),
		"hair_angle": 1.0695581,
		"hair_squeeze": 1 + 4.6039239e-01*1.5,
		"loop_length_short": (5.1399508, 0.01),
		"loop_distance_factor_short": (7.8342690, 1.7788323),
		"enable": True
	}
	
	
	other = {
		"fiber_thickness_x" : fiber_thickness_x,
		"fiber_thickness_y" : fiber_thickness_y,
		"flyaway_thickness_x" : fiber_thickness_x,
		"flyaway_thickness_y" : fiber_thickness_y,
		}
		
	return l2, material_props, flyaways, other

	
def get_grey_thick():
	rnd = np.random.RandomState(seed=20)
	fiber_thickness_x = 0.007
	fiber_thickness_y = 0.011
	curve_jitter_z = 0.02
	curve_jitter_xy = 9.8175816e-03
	curve_jitter_xy_l2 = 0
	migration = 1.5537545e-01
	l1  = {
	"name": "l1",
	"placement_params": {
		"type": "AREA",
		"num_points" : 148,
		"radius": 0.3341097,
		"jitter_xy" : curve_jitter_xy
		},
	"curve_params" : {
		"dif_z" : -2.5247045,
		"jitter_z" : curve_jitter_z,
		"migration": migration
		},
	"fiber_params" : {
		"line": {
			"length": 40.0,
			"resolution": 4,
			}
		},
	"ellipse": 1
	}
	
	l2  = {
	"name": "l2",
	"placement_params": {
		"type": "CIRCLE",
		"num_points" : 2,
		"radius": 0.2544184,
		"middle_ply": False,
		"jitter_xy" : curve_jitter_xy_l2
		},
	"curve_params" : {
		"dif_z" : 3.825475,
		"jitter_z" : 0,
		"migration": 0
		},
	"fiber_params" : {
		"yarn" : l1
		},
	"ellipse": 0.69386435
	}
	
	material_props = default_material()
	
	
	flyaways = {
		"loop_prob": 4.3567708e-01,
		"amount": 176,
		"hair_length": (1.9258337, 0.05),
		"hair_angle": 9.6773249e-01 ,
		"hair_squeeze": 1 +4.2941096e-01*1.5,
		"loop_length_short": (4.0252581, 0.01),
		"loop_distance_factor_short": (5.4163060 , 1.6969073),
		"enable": True
	}
	
	
	other = {
		"fiber_thickness_x" : fiber_thickness_x,
		"fiber_thickness_y" : fiber_thickness_y,
		"flyaway_thickness_x" : fiber_thickness_x,
		"flyaway_thickness_y" : fiber_thickness_y,
		}
		
	return l2, material_props, flyaways, other	
	
# As in Fig. 15 d)	
def get_grey_thick_4level():
	rnd = np.random.RandomState(seed=20)
	fiber_thickness_x = 0.007
	fiber_thickness_y = 0.011
	curve_jitter_z = 0.02
	curve_jitter_xy = 9.8175816e-03
	curve_jitter_xy_l2 = 0
	migration = 1.5537545e-01
	l1  = {
	"name": "l1",
	"placement_params": {
		"type": "AREA",
		"num_points" : 148,
		"radius": 0.3341097,
		"jitter_xy" : curve_jitter_xy
		},
	"curve_params" : {
		"dif_z" : -2.5247045,
		"jitter_z" : curve_jitter_z,
		"migration": migration
		},
	"fiber_params" : {
		"line": {
			"length": 40.0,
			"resolution": 4,
			}
		},
	"ellipse": 1
	}
	
	l2  = {
	"name": "l2",
	"placement_params": {
		"type": "CIRCLE",
		"num_points" : 2,
		"radius": 0.2544184,
		"middle_ply": False,
		"jitter_xy" : curve_jitter_xy_l2
		},
	"curve_params" : {
		"dif_z" : 3.825475,
		"jitter_z" : 0,
		"migration": 0
		},
	"fiber_params" : {
		"yarn" : l1
		},
	"ellipse": 0.69386435
	}
	
	l3  = {
	"name": "l3",
	"placement_params": {
		"type": "CIRCLE",
		"num_points" : 2,
		"radius": 0.32,
		"middle_ply": False,
		"jitter_xy" : curve_jitter_xy_l2
		},
	"curve_params" : {
		"dif_z" : -4.825475,
		"jitter_z" : 0,
		"migration": 0
		},
	"fiber_params" : {
		"yarn" : l2
		},
	"ellipse": 0.86
	}
	
	material_props = default_material()
	

	flyaways = {
		"loop_prob": 4.3567708e-01,
		"amount": 176,
		"hair_length": (1.9258337, 0.05),
		"hair_angle": 9.6773249e-01 ,
		"hair_squeeze": 1 +4.2941096e-01*1.5,
		"loop_length_short": (4.0252581, 0.01),
		"loop_distance_factor_short": (5.4163060 , 1.6969073),
		"enable": True
	}

	
	other = {
		"fiber_thickness_x" : fiber_thickness_x,
		"fiber_thickness_y" : fiber_thickness_y,
		"flyaway_thickness_x" : fiber_thickness_x,
		"flyaway_thickness_y" : fiber_thickness_y,
		}
		
	return l3, material_props, flyaways, other	

		
def get_pink_4ply():
	rnd = np.random.RandomState(seed=20)
	curve_jitter_z = 0.02
	curve_jitter_xy = 1.8280927e-02
	curve_jitter_xy_l2 = 0
	migration = 2.2564596e-01
	fiber_thickness_x = 0.007
	fiber_thickness_y = 0.011
	l1  = {
	"name": "l1",
	"placement_params": {
		"type": "AREA",
		"num_points" : 49,
		"radius": 0.24919415,
		"jitter_xy" : curve_jitter_xy
		},
	"curve_params" : {
		"dif_z" : -2.4189832,
		"jitter_z" : curve_jitter_z,
		"migration": migration
		},
	"fiber_params" : {
		"line": {
			"length": 40.0,
			"resolution": 4,
			}
		},
	"ellipse": 1
	}
	
	l2  = {
	"name": "l2",
	"placement_params": {
		"type": "CIRCLE",
		"num_points" : 4,
		"radius": 0.36432442,
		"middle_ply": False,
		"jitter_xy" : curve_jitter_xy_l2
		},
	"curve_params" : {
		"dif_z" : 5.6048384,
		"jitter_z" : 0,
		"migration": 0
		},
	"fiber_params" : {
		"yarn" : l1
		},
	"ellipse": 0.9214183
	}
	
	material_props = default_material()
	
	
	flyaways = {
		"loop_prob": 5.6389588e-01,
		"amount": 153,
		"hair_length": (3.1847796, 0.05),
		"hair_angle": 8.1989717e-01,
		"hair_squeeze": 1 + 4.5290235e-01 *1.5,
		"loop_length_short": (4.6552114, 0.01),
		"loop_distance_factor_short": (4.6890984, 2.3526678),
		"enable": True
	}
	
	other = {
		"fiber_thickness_x" : fiber_thickness_x,
		"fiber_thickness_y" : fiber_thickness_y,
		"flyaway_thickness_x" : fiber_thickness_x,
		"flyaway_thickness_y" : fiber_thickness_y,
		}
		
	return l2, material_props, flyaways, other

def get_grey_thin():
	rnd = np.random.RandomState(seed=20)
	curve_jitter_z = 0.02
	curve_jitter_xy = 1.5261699e-02
	curve_jitter_xy_l2 = 0
	migration = 1.6829909e-01
	fiber_thickness_x = 0.007
	fiber_thickness_y = 0.011
	l1  = {
	"name": "l1",
	"placement_params": {
		"type": "AREA",
		"num_points" : 82,
		"radius": 0.14561464,
		"jitter_xy" : curve_jitter_xy
		},
	"curve_params" : {
		"dif_z" : -1.1751631,
		"jitter_z" : curve_jitter_z,
		"migration": migration
		},
	"fiber_params" : {
		"line": {
			"length": 40.0,
			"resolution": 4,
			}
		},
	"ellipse": 1
	}
	
	l2  = {
	"name": "l2",
	"placement_params": {
		"type": "CIRCLE",
		"num_points" : 2,
		"radius": 0.13947915,
		"middle_ply": False,
		"jitter_xy" : curve_jitter_xy_l2
		},
	"curve_params" : {
		"dif_z" : 3.3483522,
		"jitter_z" : 0,
		"migration": 0
		},
	"fiber_params" : {
		"yarn" : l1
		},
	"ellipse": 0.79097
	}
	
	material_props = default_material()


	flyaways = {
		"loop_prob": 4.2104611e-01,
		"amount": 200,
		"hair_length": (1.7228923 , 0.05),
		"hair_angle": 8.5089332e-01,
		"hair_squeeze": 1 + 3.5832524e-01 *1.5,
		"loop_length_short": ( 3.2249172, 0.01),
		"loop_distance_factor_short": (3.3760602, 1.5249424),
		"enable": True
	}
	
	
	other = {
		"fiber_thickness_x" : fiber_thickness_x,
		"fiber_thickness_y" : fiber_thickness_y,
		"flyaway_thickness_x" : fiber_thickness_x,
		"flyaway_thickness_y" : fiber_thickness_y,
		}
		
	return l2, material_props, flyaways, other
	
# As in Fig. 15 e)
def get_grey_thin_4level():
	rnd = np.random.RandomState(seed=20)
	curve_jitter_z = 0.02
	curve_jitter_xy = 1.5261699e-02
	curve_jitter_xy_l2 = 0
	migration = 1.6829909e-01
	fiber_thickness_x = 0.007
	fiber_thickness_y = 0.011
	l1  = {
	"name": "l1",
	"placement_params": {
		"type": "AREA",
		"num_points" : 82,
		"radius": 0.14561464,
		"jitter_xy" : curve_jitter_xy
		},
	"curve_params" : {
		"dif_z" : -1.1751631,
		"jitter_z" : curve_jitter_z,
		"migration": migration
		},
	"fiber_params" : {
		"line": {
			"length": 40.0,
			"resolution": 4,
			}
		},
	"ellipse": 1
	}
	
	l2  = {
	"name": "l2",
	"placement_params": {
		"type": "CIRCLE",
		"num_points" : 2,
		"radius": 0.13947915,
		"middle_ply": False,
		"jitter_xy" : curve_jitter_xy_l2
		},
	"curve_params" : {
		"dif_z" : 3.3483522,
		"jitter_z" : 0,
		"migration": 0
		},
	"fiber_params" : {
		"yarn" : l1
		},
	"ellipse": 0.79097
	}
	
	l3  = {
	"name": "l3",
	"placement_params": {
		"type": "CIRCLE",
		"num_points" : 2,
		"radius": 0.20,
		"middle_ply": False,
		"jitter_xy" : curve_jitter_xy_l2
		},
	"curve_params" : {
		"dif_z" : -5.3483522,
		"jitter_z" : 0,
		"migration": 0
		},
	"fiber_params" : {
		"yarn" : l2
		},
	"ellipse": 0.86
	}
	
	material_props = default_material()


	flyaways = {
		"loop_prob": 4.2104611e-01,
		"amount": 200,
		"hair_length": (1.7228923 , 0.05),
		"hair_angle": 8.5089332e-01,
		"hair_squeeze": 1 + 3.5832524e-01 *1.5,
		"loop_length_short": ( 3.2249172, 0.01),
		"loop_distance_factor_short": (3.3760602, 1.5249424),
		"loop_length_long": (5.139884, 7.35203 ),
		"loop_distance_factor_long": (8, 10),
		"loop_squeeze": 1,
		"enable": True
	}
	
	
	other = {
		"fiber_thickness_x" : fiber_thickness_x,
		"fiber_thickness_y" : fiber_thickness_y,
		"flyaway_thickness_x" : fiber_thickness_x,
		"flyaway_thickness_y" : fiber_thickness_y,
		}
		
	return l3, material_props, flyaways, other
	

def get_yellow():
	rnd = np.random.RandomState(seed=20)
	curve_jitter_z = 0.02
	curve_jitter_xy = 1.1380553e-02
	curve_jitter_xy_l2 = 0
	migration = 1.6266209e-01
	fiber_thickness_x = 0.007
	fiber_thickness_y = 0.011
	l1  = {
	"name": "l1",
	"placement_params": {
		"type": "AREA",
		"num_points" : 64,
		"radius": 0.27770048,
		"jitter_xy" : curve_jitter_xy
		},
	"curve_params" : {
		"dif_z" : -2.0234628 ,
		"jitter_z" : curve_jitter_z,
		"migration": migration
		},
	"fiber_params" : {
		"line": {
			"length": 40.0,
			"resolution": 4,
			}
		},
	"ellipse": 1
	}
	
	l2  = {
	"name": "l2",
	"placement_params": {
		"type": "CIRCLE",
		"num_points" : 4,
		"radius": 0.3929647,
		"middle_ply": False,
		"jitter_xy" : curve_jitter_xy_l2
		},
	"curve_params" : {
		"dif_z" : 6.3978333,
		"jitter_z" : 0,
		"migration": 0
		},
	"fiber_params" : {
		"yarn" : l1
		},
	"ellipse": 0.8495044
	}
	
	material_props = default_material()

	
	flyaways = {
		"loop_prob": 3.5111555e-01 ,
		"amount": 183,
		"hair_length": (1.7800096, 0.05),
		"hair_angle": 8.7905598e-01,
		"hair_squeeze": 1 + 5.1986212e-01*1.5,
		"loop_length_short": (4.1443834, 0.01),
		"loop_distance_factor_short": (7.7870250, 1.4530934),
		"enable": True
	}
	
	other = {
		"fiber_thickness_x" : fiber_thickness_x,
		"fiber_thickness_y" : fiber_thickness_y,
		"flyaway_thickness_x" : fiber_thickness_x,
		"flyaway_thickness_y" : fiber_thickness_y,
		}
		
	return l2, material_props, flyaways, other		


def get_blue():
	rnd = np.random.RandomState(seed=20)
	curve_jitter_z = 0.02
	curve_jitter_xy = 1.3559038e-02
	curve_jitter_xy_l2 = 0
	migration = 1.9451331e-01
	fiber_thickness_x = 0.007
	fiber_thickness_y = 0.011
	l1  = {
	"name": "l1",
	"placement_params": {
		"type": "AREA",
		"num_points" : 73,
		"radius": 0.40591604,
				"jitter_xy" : curve_jitter_xy
		},
	"curve_params" : {
		"dif_z" : -2.865765,
		"jitter_z" : curve_jitter_z,
		"migration": migration
		},
	"fiber_params" : {
		"line": {
			"length": 40.0,
			"resolution": 4,
			}
		},
	"ellipse": 1,
	}
	
	l2  = {
	"name": "l2",
	"placement_params": {
		"type": "CIRCLE",
		"num_points" : 4,
		"radius": 0.60239923,
		"middle_ply": False,
		"jitter_xy" : curve_jitter_xy_l2
		},
	"curve_params" : {
		"dif_z" : 11.009346,
		"jitter_z" : 0,
		"migration": 0
		},
	"fiber_params" : {
		"yarn" : l1
		},
	"ellipse": 0.73451215
	}
	
	material_props = default_material()
	
		
	flyaways = {
		"loop_prob": 4.5316660e-01,
		"amount": 182,
		"hair_length": (2.9103725, 0.05),
		"hair_angle": 8.4900349e-01,
		"hair_squeeze": 1 + 7.2775346e-01 *1.5,
		"loop_length_short": (7.2018127, 0.01),
		"loop_distance_factor_short": (1.0612761e+01, 1.6843938),
		"enable": True
	}
	
	other = {
		"fiber_thickness_x" : fiber_thickness_x,
		"fiber_thickness_y" : fiber_thickness_y,
		"flyaway_thickness_x" : fiber_thickness_x,
		"flyaway_thickness_y" : fiber_thickness_y,
		}
		
	return l2, material_props, flyaways, other	
			
def get_mixed():
	rnd = np.random.RandomState(seed=20)
	curve_jitter_z = 0.02
	curve_jitter_xy = 1.8884758e-02
	curve_jitter_xy_l2 = 0
	migration = 1.8518642e-01
	fiber_thickness_x = 0.01
	fiber_thickness_y = 0.018
	l1  = {
	"name": "l1",
	"placement_params": {
		"type": "AREA",
		"num_points" : 99,
		"radius": 0.5205193,
		"jitter_xy" : curve_jitter_xy
		},
	"curve_params" : {
		"dif_z" : -6.152366,
		"jitter_z" : curve_jitter_z,
		"migration": migration
		},
	"fiber_params" : {
		"line": {
			"length": 40.0,
			"resolution": 4,
			}
		},
	"ellipse": 1,
	}
	
	l2  = {
	"name": "l2",
	"placement_params": {
		"type": "CIRCLE",
		"num_points" : 3,
		"radius": 0.63914716,
		"middle_ply": False,
		"jitter_xy" : curve_jitter_xy_l2
		},
	"curve_params" : {
		"dif_z" : 14.9614525,
		"jitter_z" : 0,
		"migration": 0
		},
	"fiber_params" : {
		"yarn" : l1
		},
	"ellipse": 0.81179607
	}
	
	material_props = default_material()
	
	
	flyaways = {
		"loop_prob": 5.3245062e-01,
		"amount": 160,
		"hair_length": (4.7082000, 0.05),
		"hair_angle": 7.7463073e-01,
		"hair_squeeze": 1 + 5.4821879e-01 *1.5,
		"loop_length_short": (1.2376551e+01, 0.01),
		"loop_distance_factor_short": (1.1104931e+01, 2.6809387),
		"enable": True
	}
	
	other = {
		"fiber_thickness_x" : fiber_thickness_x,
		"fiber_thickness_y" : fiber_thickness_y,
		"flyaway_thickness_x" : fiber_thickness_x,
		"flyaway_thickness_y" : fiber_thickness_y,
		}
		
	return l2, material_props, flyaways, other

def get_pink_6ply():
	rnd = np.random.RandomState(seed=20)
	fiber_thickness_x = 0.01
	fiber_thickness_y = 0.018
	curve_jitter_z = 0.02
	curve_jitter_xy = 1.6286893e-02
	curve_jitter_xy_l2 = 0
	migration = 2.1577866e-01
	l1  = {
	"name": "l1",
	"placement_params": {
		"type": "AREA",
		"num_points" : 64,
		"radius": 0.38961697,
		"jitter_xy" : curve_jitter_xy
		},
	"curve_params" : {
		"dif_z" : -3.2881775,
		"jitter_z" : curve_jitter_z,
		"migration": migration
		},
	"fiber_params" : {
		"line": {
			"length": 40.0,
			"resolution": 4,
			}
		},
	"ellipse": 1
	}
	
	l2  = {
	"name": "l2",
	"placement_params": {
		"type": "CIRCLE",
		"num_points" : 6,
		"radius": 0.67214125,
		"middle_ply": False,
		"jitter_xy" : curve_jitter_xy_l2
		},
	"curve_params" : {
		"dif_z" : 10.67939,
		"jitter_z" : 0,
		"migration": 0
		},
	"fiber_params" : {
		"yarn" : l1
		},
	"ellipse": 0.89814955
	}
	
	material_props = default_material()
	

	flyaways = {
		"loop_prob": 5.4462570e-01,
		"amount": 175,
		"hair_length": (3.7025852, 0.05),
		"hair_angle": 9.6676326e-01,
		"hair_squeeze": 1 + 6.1938077e-01 *1.5,
		"loop_length_short": (7.0356255, 0.01),
		"loop_distance_factor_short": (1.0737836e+01, 2.1395535),
		"enable": True
	}
	
	other = {
		"fiber_thickness_x" : fiber_thickness_x,
		"fiber_thickness_y" : fiber_thickness_y,
		"flyaway_thickness_x" : fiber_thickness_x,
		"flyaway_thickness_y" : fiber_thickness_y,
		}
		
	return l2, material_props, flyaways, other	

	
def get_golden():
	rnd = np.random.RandomState(seed=20)
	fiber_thickness_x = 0.01
	fiber_thickness_y = 0.018
	curve_jitter_z = 0.02
	curve_jitter_xy = 1.3717855e-02
	curve_jitter_xy_l2 = 0
	migration = 1.9197150e-01
	l1  = {
	"name": "l1",
	"placement_params": {
		"type": "AREA",
		"num_points" : 43,
		"radius": 0.24072605,
		"jitter_xy" : curve_jitter_xy
		},
	"curve_params" : {
		"dif_z" : -2.3922226 ,
		"jitter_z" : curve_jitter_z,
		"migration": migration
		},
	"fiber_params" : {
		"line": {
			"length": 40.0,
			"resolution": 4,
			}
		},
	"ellipse": 1
	}
	
	l2  = {
	"name": "l2",
	"placement_params": {
		"type": "CIRCLE",
		"num_points" : 3,
		"radius": 0.28942686,
		"middle_ply": False,
		"jitter_xy" : curve_jitter_xy_l2
		},
	"curve_params" : {
		"dif_z" : 6.4739985,
		"jitter_z" : 0,
		"migration": 0
		},
	"fiber_params" : {
		"yarn" : l1
		},
	"ellipse": 0.8116607
	}
	
	material_props = default_material()

	
	flyaways = {
		"loop_prob": 5.0455111e-01,
		"amount": 123,
		"hair_length": (2.2595623, 0.05),
		"hair_angle":7.7107286e-01 ,
		"hair_squeeze": 1 +4.3868071e-01*1.5,
		"loop_length_short": (4.4779601, 0.01),
		"loop_distance_factor_short": (4.4419546, 2.0816653),
		"enable": True
	}

	
	other = {
		"fiber_thickness_x" : fiber_thickness_x,
		"fiber_thickness_y" : fiber_thickness_y,
		"flyaway_thickness_x" : fiber_thickness_x,
		"flyaway_thickness_y" : fiber_thickness_y,
		}
		
	return l2, material_props, flyaways, other
		

	
def get_red():
	rnd = np.random.RandomState(seed=20)
	curve_jitter_z = 0.02
	curve_jitter_xy = 1.3876019e-02
	curve_jitter_xy_l2 = 0
	migration = 2.0379692e-01
	fiber_thickness_x = 0.007
	fiber_thickness_y = 0.011
	l1  = {
	"name": "l1",
	"placement_params": {
		"type": "AREA",
		"num_points" : 130,
		"radius": 0.29728216,
		"jitter_xy" : curve_jitter_xy
		},
	"curve_params" : {
		"dif_z" : -2.442278 ,
		"jitter_z" : curve_jitter_z,
		"migration": migration
		},
	"fiber_params" : {
		"line": {
			"length": 30.0,
			"resolution": 4,
			}
		},
	"ellipse": 1
	}
	
	l2  = {
	"name": "l2",
	"placement_params": {
		"type": "CIRCLE",
		"num_points" : 4,
		"radius": 0.44882327,
		"middle_ply": False,
		"jitter_xy" : curve_jitter_xy_l2
		},
	"curve_params" : {
		"dif_z" : 7.51518,
		"jitter_z" : 0,
		"migration": 0
		},
	"fiber_params" : {
		"yarn" : l1
		},
	"ellipse": 0.8083649
	}
	
	material_props = default_material()
	
	
	flyaways = {
		"loop_prob": 4.7552925e-01,
		"amount": 151,
		"hair_length": (2.4101708, 0.05),
		"hair_angle": 8.6318338e-01,
		"hair_squeeze": 1 + 6.5422958e-01*1.5,
		"loop_length_short": (4.7530303, 0.01),
		"loop_distance_factor_short": (7.7668934, 2.3484037),
		"enable": True
	}
	
	other = {
		"fiber_thickness_x" : fiber_thickness_x,
		"fiber_thickness_y" : fiber_thickness_y,
		"flyaway_thickness_x" : fiber_thickness_x,
		"flyaway_thickness_y" : fiber_thickness_y,
		}
		
	return l2, material_props, flyaways, other
		
					
def get_rose():
	rnd = np.random.RandomState(seed=20)
	curve_jitter_z = 0.02
	curve_jitter_xy = 1.4466001e-02
	curve_jitter_xy_l2 = 0
	migration =2.0764436e-01
	fiber_thickness_x = 0.01
	fiber_thickness_y = 0.018
	l1  = {
	"name": "l1",
	"placement_params": {
		"type": "AREA",
		"num_points" : 72,
		"radius": 0.32925424,
		"jitter_xy" : curve_jitter_xy
		},
	"curve_params" : {
		"dif_z" : -3.6105819,
		"jitter_z" : curve_jitter_z,
		"migration": migration
		},
	"fiber_params" : {
		"line": {
			"length": 40.0,
			"resolution": 4,
			}
		},
	"ellipse": 1
	}
	
	l2  = {
	"name": "l2",
	"placement_params": {
		"type": "CIRCLE",
		"num_points" : 4,
		"radius": 0.5553524,
		"middle_ply": False,
		"jitter_xy" : curve_jitter_xy_l2
		},
	"curve_params" : {
		"dif_z" : 4.5149097,
		"jitter_z" : 0,
		"migration": 0
		},
	"fiber_params" : {
		"yarn" : l1
		},
	"ellipse": 0.8603054
	}
	
	material_props = default_material()
	
	flyaways = {
		"loop_prob": 5.0607127e-01,
		"amount": 147,
		"hair_length": (2.6149280, 0.05),
		"hair_angle": 8.3027536e-01,
		"hair_squeeze": 1 + 4.9014309e-01*1.5,
		"loop_length_short": (4.3994718, 0.01),
		"loop_distance_factor_short": (8.2998505, 1.5339578),
		"enable": True
	}

	other = {
		"fiber_thickness_x" : fiber_thickness_x,
		"fiber_thickness_y" : fiber_thickness_y,
		"flyaway_thickness_x" : fiber_thickness_x,
		"flyaway_thickness_y" : fiber_thickness_y,
		}
		
	return l2, material_props, flyaways, other	

	
# As in Fig. 15 b-c)
def get_light_rose():
	rnd = np.random.RandomState(seed=20)
	curve_jitter_z = 0.02
	curve_jitter_xy = 9.5352046e-03
	curve_jitter_xy_l2 = 0
	migration = 2.6263532e-01
	fiber_thickness_x = 0.007
	fiber_thickness_y = 0.011
	l1  = {
	"name": "l1",
	"placement_params": {
		"type": "AREA",
		"num_points" : 104,
		"radius": 0.45795327,
		"jitter_xy" : curve_jitter_xy
		},
	"curve_params" : {
		"dif_z" : -4.4426484,
		"jitter_z" : curve_jitter_z,
		"migration": migration
		},
	"fiber_params" : {
		"line": {
			"length": 40.0,
			"resolution": 4,
			}
		},
	"ellipse": 1
	}
	
	l2  = {
	"name": "l2",
	"placement_params": {
		"type": "CIRCLE",
		"num_points" : 5,
		"radius": 0.7423457,
		"middle_ply": False,
		"jitter_xy" : curve_jitter_xy_l2
		},
	"curve_params" : {
		"dif_z" : 12.714859,
		"jitter_z" : 0,
		"migration": 0
		},
	"fiber_params" : {
		"yarn" : l1
		},
	"ellipse": 0.9861847
	}
	
	#material_props = default_material()
	
	material_props = {
		"type": "direct",
		"roughness": 0.16149087,
		"radial_roughness": 0.29831055,
		"ior": 1.3959906,
		"color": (
			0.4492084,
			0.2636265,
			0.53100955,
			1
		),
		"random_roughness": 0.96294665
	}
	

	flyaways = {
		"loop_prob": 5.3044379e-01,
		"amount": 170,
		"hair_length": (2.8071439 , 0.05),
		"hair_angle": 7.5017560e-01,
		"hair_squeeze": 1 + 6.1667740e-01 *1.5,
		"loop_length_short": (7.0983009, 0.01),
		"loop_distance_factor_short": (1.2789481e+01, 2.4046965),
		"enable": True
	}
	
	
	other = {
		"fiber_thickness_x" : fiber_thickness_x,
		"fiber_thickness_y" : fiber_thickness_y,
		"flyaway_thickness_x" : fiber_thickness_x,
		"flyaway_thickness_y" : fiber_thickness_y,
		}
		
	return l2, material_props, flyaways, other	
	
