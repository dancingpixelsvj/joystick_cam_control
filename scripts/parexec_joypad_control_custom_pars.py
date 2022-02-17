def onPulse(par):
	#actions on pulsing custom parameters buttons
	if par.name == 'Getoriginfromview':
		parent().Get_origin_from_current_view()
	if par.name == 'Resettoorigin':
		parent().Reset_to_origin()
	if par.name == 'Resetplayback':
		parent().Reset_playback()
	if par.name == 'Save':
		parent().Save_recording()
	if par.name == 'Clearrecordings':
		parent().Clear_recordings()


def onValueChange(par, prev):
	# actions on turning on the toggle for constraining rotation
	if par.name == 'Constrainupdownrotation':
		parent().Enable_rotation_constraints()

	# actions on turning on the toggle for recording controller data
	if par.name == 'Recording' and par.val == 1:
		parent().Start_recording()
		
	elif par.name == 'Recording' and par.val == 0:
		parent().Stop_recording()

	# actions on turning on the toggle for playback of recorded controller data
	if par.name == 'Play' and par.val == 1:
		parent().Start_playback()
		
	elif par.name == 'Play' and par.val == 0:
		parent().Stop_playback()
