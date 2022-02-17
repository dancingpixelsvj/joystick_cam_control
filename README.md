# A tox to control TouchDesigner camera with a joystick

*adapted from the [patch](https://forum.derivative.ca/t/fps-joypad-control-designed-for-osc-control-of-disguise-d3-visualiser/118314) by Nick Diacre*

## Main features
The component has custom parameters and an extension that allow to:
- save current camera position as origin
- reset camera to origin
- control camera speed
- record controller values
- play back recorded values

## Mapping for an Xbox (or any other Xinput) controller
xaxis: movement sideways (left stick moving left and right)

yaxis: movement forward and backward (left stick moving up and down)

zaxis: movement up and down (left and right triggers)

xrot: look sideways (right stick moving left and right)

yrot: look up and down (right stick moving up and down)

b1: reset camera position to origin ("A" button)

## Notes

- Dinput controllers are not currently supported.
- In this patch camera speed is influenced by frame drops. When recording make sure that no frame drop happens. Only then the playback speed will match camera movement speed at recording.
- The heading direction ignores rotation of the camera on the X axis so you can look around but won’t fly off in the direction you are looking if its up or down.
