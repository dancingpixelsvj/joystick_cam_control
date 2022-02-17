'''
a class that 
- saves current camera position as a new origin
- resets camera to origin
- toggles on and off constraints on up and down rotation angle of the camera
- adds controls for camera speed
- records controller values
- plays back recorded values
- erases all recordings

'''

class Cam_controller:

	def __init__(self, my_op):
		self.my_op = my_op
		print('A cam_controller object that extends functionality of {} component has been created'.format(my_op))

		#update recordings list menu based on the dictionary in the storage
		self.updateRecordingsMenu()

	'''
	method to get origin values from current view
	it grabs translate and rotate values of camera's parent
	and updates translation and rotation values of the parameters of it's owner component
	'''
	def Get_origin_from_current_view(self):
		#store camera parent's translate and rotate parameters in a dictionary
		origin_values = {
		'Tx': op('null_cam_parent').par.tx,
		'Ty': op('null_cam_parent').par.ty,
		'Tz': op('null_cam_parent').par.tz,
		'Rx': op('null_processed_input')['rx'].eval(),
		'Ry': op('null_cam_parent').par.ry
		}
		
		#update origin position parameters of the owner component
		for each_par_name, each_par_value in origin_values.items():
			setattr(self.my_op.par, each_par_name, each_par_value)
		print('new origin set')


	'''
	reset camera position to origin
	'''
	def Reset_to_origin(self):
		op('null_cam_parent').par.tx = self.my_op.par.Tx
		op('null_cam_parent').par.ty = self.my_op.par.Ty
		op('null_cam_parent').par.tz = self.my_op.par.Tz
		op('null_cam_parent').par.ry = self.my_op.par.Ry

		#to reset rx position we need to reset the speed operator
		op('speed1').par.resetvalue = self.my_op.par.Rx
		op('speed1').par.reset.pulse()

		print('camera position has been reset')

	'''
	enable constraints on rotation
	'''
	def Enable_rotation_constraints(self):

		#rotation constraint toggle values on the owner comp are boolean
		#and need to be casted into integers
		# then they will correspond to speed1 limit type values: 0 for off, 1 for clamping
		constraint_true_false = self.my_op.par.Constrainupdownrotation.eval()
		op('speed1').par.limittype = int(constraint_true_false)

		#Constraintodegrees parameter on owner component is enabled/disabled 
		#depending on whether constrain rotation toggle is turned on or off 
		self.my_op.par.Constraintodegrees.enable = constraint_true_false

		print(f'rotation constraints enabled = {constraint_true_false}')

	'''
	start recording
	'''
	def Start_recording(self):
		#when recording is turned on in parameters record1 is reset, 1 is put into a table cell
		op('record1').par.reset.pulse()
		op('table_recording_controller')[0,0] = 1

		print('recording started')

	'''
	stop recording
	'''
	def Stop_recording(self):
		#when recording is turned off in parameters, table cell is set to 0
		op('table_recording_controller')[0,0] = 0

		print('recording stopped')
	
	'''
	create and store an empty dictionary for recordings
	the dictionary will be stored on extension's owner component
	'''
	def set_recordings_dict(self):
		recordings_dictionary = {}
		self.my_op.store('Recordings', recordings_dictionary)

		print('empty dictionary has been created in storage')

	'''
	fetch the recordings dictionary from storage or create an empty one if there is none
	'''
	def get_recordings_dict(self):
		recordings_dictionary = self.my_op.fetch('Recordings', 'not_yet_assigned') 	#go to storage and fetch the dictionary

		#if there's no dictionary with this name create one with set_recordings_dict and refetch it again
		if recordings_dictionary == 'not_yet_assigned':
			self.set_recordings_dict()
			recordings_dictionary = self.my_op.fetch('Recordings')
		else:
			pass

		print('recordings dictionary grabbed')
		return recordings_dictionary

	'''
	save channels of record1 to storage
	'''
	def Save_recording(self):
		#go to storage and fetch the dictionary
		recordings_dictionary = self.get_recordings_dict()
		
		#get the name from custom parameters of my_op under which the recording should be saved
		recording_name = self.my_op.par.Saverecordingas.eval()

		#if the name is non-empty save recording under that name to storage
		if recording_name:

			#check record1 exists and has channels
			if op('record1') and op('record1').chans():
	
				#build a dictionary of channel values of record1 chop
				dict_of_recorded_channels = {}
				for channel in op('record1').chans():
					dict_of_recorded_channels[channel.name] = channel.vals

				#check to make sure length of each channel is the same
				len_first_channel = len( list (dict_of_recorded_channels.values())[0] )
				channels_have_same_length = all( len(channel) == len_first_channel for channel in dict_of_recorded_channels.values())

				if channels_have_same_length:
					#add this new dictionary to the dictionary of recordings
					recordings_dictionary[recording_name] = dict_of_recorded_channels

					print('new recording has been added')
			
					#store updated dictionary of recordings
					parent().store('Recordings', recordings_dictionary)

					print('updated Recordings dictionary stored')

					#update recordings menu labels
					self.updateRecordingsMenu()

				else:
					print('length of channels recorded is not the same')
			else:
				print('check that record1 operator exists and is connected to the input')
		else:
			print('no name specified for recording')


	'''
	populate menu with names of recordings
	'''
	def updateRecordingsMenu(self):

		#get the dictionary of recordings
		recordings_dictionary = self.get_recordings_dict()

		#make a list of dictionary keys
		list_of_recordings = list(recordings_dictionary.keys())

		#set this list as a list of menu names and labels
		self.my_op.par.Playrecording.menuNames = list_of_recordings
		self.my_op.par.Playrecording.menuLabels = list_of_recordings

		print('recordings menu has been updated')

	'''
	populate a table with channel names and values of one recording
	'''
	def createRecordingTable(self,recording_name):

		#fetch recordings dictionary from storage
		recordings_dictionary = self.get_recordings_dict()

		#get data for the specified recording
		selected_recording_dict = recordings_dictionary.get(recording_name)

		#make a table from that data
		table_for_recording = op('table_recording_data')
		table_for_recording.clear()

		#add values for each channel as one row of the table
		for chan_values in selected_recording_dict.values():
			table_for_recording.appendRow(chan_values)

		#insert channel names as the first column
		table_for_recording.insertCol(list(selected_recording_dict.keys()))

		print(f'{table_for_recording} updated with channel values from {recording_name}')

	'''
	start playback
	'''
	def Start_playback(self):

		recordings_dictionary = self.my_op.fetch('Recordings', 'not_yet_assigned') 	#go to storage and fetch the dictionary
		recording_name = self.my_op.par.Playrecording.eval()

		#if storage or recordings dictionary is empty
		if recordings_dictionary == 'not_yet_assigned' or not recordings_dictionary:
			print('no recordings stored')

		#if recording name is empty
		elif not recording_name:
			print('no recording is selected for playback')

		#if there's no recording in storage under that name
		elif not recordings_dictionary[recording_name]:
			print('no recording found with that name')

		else:
			self.createRecordingTable(recording_name)

			timer = op('timer_for_playback')
			chop_to_play = op('datto_recording_to_play')

			#set timer's length equal to the length of datto_recording_to_play
			timer.par.length = chop_to_play.numSamples

			print(f'playback set to length of {chop_to_play}')

			#point output to recorded data
			op('switch1').par.index = 1

			print('switch to camera control from recording')

			#toggle play on timer
			timer.par.play = 1

			print('playing')

	'''
	stop playback
	'''
	def Stop_playback(self):
		timer = op('timer_for_playback')
		
		#turn off play on timer
		timer.par.play = 0

		print('playback stopped')

		#point output to controller data
		op('switch1').par.index = 0

		print('switch to camera control from joypad')

	'''
	reset playback
	'''
	def Reset_playback(self):
		timer = op('timer_for_playback')

		#reinit and start timer
		timer.par.initialize.pulse()
		timer.par.start.pulse()

		print('playback reset')

	'''
	clear recordings from storage
	'''
	def Clear_recordings(self):

		#remove Recordings dictionary from storage
		self.my_op.unstore('Recordings')

		#reset channels of record1
		op('record1').par.reset.pulse()

		#clear table that held channels of the last recording
		op('table_recording_data').clear()

		print('recordings erased')

		#update menu in parameters
		#BUG: currently recordings menu updates but the top field still holds the name from before
		#TODO: fix
		self.updateRecordingsMenu()
		
		

		
	