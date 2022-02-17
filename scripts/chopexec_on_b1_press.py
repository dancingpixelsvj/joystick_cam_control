# when b1 is pressed reset cam pos to origin

def offToOn(channel, sampleIndex, val, prev):
	if channel.name == 'b1':
		parent().Reset_to_origin()



	