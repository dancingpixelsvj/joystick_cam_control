'''
this script runs every frame
every frame it puts cam's parent component at the position where the camera was at previous frame
in this way every frame camera will start movement according to controller's values from an updated position
'''

def onFrameStart(frame):
	
#get values from the controller input.

	controller = op('null_processed_input')
	
	tx = controller['tx'].eval()
	ty = controller['ty'].eval()
	tz = controller['tz'].eval()
	rx = controller['rx'].eval()
	ry = controller['ry'].eval()
	
	
#move the camera with the controller data, when the data
#stops coming in camera sets to 0 for 0 movement
	
	cam = op('cam1')
	
	cam.par.tx = tx
	cam.par.ty = ty
	cam.par.tz = tz
	cam.par.rx = rx
	cam.par.ry = ry
	
	
#get the difference in transforms between the origin (reference COMP, pos 0,0,0) 
#and the camera, the object CHOP does this for us


#NOTE: Camera's heading direction ignores rotation of the camera on the X axis
#so you can look around but won’t fly off in the direction you are looking if its up or down.
#Therefore we do not update rx value of camera's parent

	object = op('object')
	
	tx = object['tx'].eval()
	ty = object['ty'].eval()
	tz = object['tz'].eval()
	ry = object['ry'].eval()
	
	
#store the new position in the parent of the camera
#now the camera will be moving from it's new origin
#again the next time it moves
#we do not update rx value

	parent = op('null_cam_parent')
	
	parent.par.tx = tx
	parent.par.ty = ty
	parent.par.tz = tz
	parent.par.ry = ry