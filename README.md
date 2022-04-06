# A tox to control TouchDesigner camera with a joystick

*An extension to the [patch](https://forum.derivative.ca/t/fps-joypad-control-designed-for-osc-control-of-disguise-d3-visualiser/118314) by Nick Diacre. Original component allowed to control virtual camera in TouchDesigner with a gamepad. This extension adds functionality such as saving camera trajectories, replaying them in real time and controlling camera speed through custom parameters of the component.*

## Main features
- save current camera position as origin
- reset camera to origin
- control camera speed
- record controller values
- play back recorded values

## Contents of the repository
- joypad_control.tox - camera control component. Drop it to your project and connect a joypad to control the camera.
- joypad_control_example.toe - a sample scene that uses joypad_control.tox
- scripts folder - scripts that are used in the component
  - camera_control_ext.py - an extension that contains Cam_controller class
  - parexec_joypad_control_custom_pars.py - script that calls Cam_controller methods when custom parameters of the component change
  - execute_script_cam.py - a script that every frame updates camera's parent position
  - chopexec_on_b1_press.py - an additional script that listens to pressing of b1 on joypad to reset camera position
  - NOTE: the same scripts are saved in the joypad_control.tox, the .tox does not load external scripts. This folder is for reference only. No need to download it if you want to just use the joypad_control.tox

## Mapping for an Xbox (or any other Xinput) controller
xaxis: movement sideways (left stick moving left and right)

yaxis: movement forward and backward (left stick moving up and down)

zaxis: movement up and down (left and right triggers)

xrot: look sideways (right stick moving left and right)

yrot: look up and down (right stick moving up and down)

b1: reset camera position to origin ("A" button)

## Notes

1. Dinput controllers are not currently supported.
2. Some controllers (like Xiaomi) have been reported to not map left and right triggers to zaxis channel on Joystick CHOP, but to slider 1 and 2 channels. In that case inside joypad_control.tox you'll need to swap the thread coming out of select1 CHOP and connect null_slider_control (end of yellow chain) to null_controller_input instead.
3. In this patch camera speed is influenced by frame drops. When recording make sure that no frame drop happens. Only then the playback speed will match camera movement speed at recording.
4. The heading direction ignores rotation of the camera on the X axis so you can look around but won’t fly off in the direction you are looking if its up or down.
