import ac
import acsys

# Globals
checkboxState = 0
startFrameInput = 0
endFrameInput = 0
currentFrameLabel = 0
currentModeLabel = 0
lastFrame = -1
currentCameraIndex= 0
camera_modes = [0,2,4]

def acMain(ac_version):
    global startFrameInput, endFrameInput, currentFrameLabel, currentModeLabel

    appWindow = ac.newApp("Replay Frame Looper")
    ac.setSize(appWindow, 400, 200)

    # Checkbox
    checkbox = ac.addCheckBox(appWindow, "Enable replay loop")
    ac.setPosition(checkbox, 180, 150)
    ac.setFontSize(checkbox, 14)
    ac.addOnCheckBoxChanged(checkbox, onCheckboxChanged)

    # Start Frame Input
    start_frame_label = ac.addLabel(appWindow, "Start Frame:")
    ac.setPosition(start_frame_label, 40, 60)
    startFrameInput = ac.addTextInput(appWindow, "")
    ac.setPosition(startFrameInput, 120, 60)
    ac.setSize(startFrameInput, 100, 20)

    # End Frame Input
    end_frame_label = ac.addLabel(appWindow, "End Frame:")
    ac.setPosition(end_frame_label, 43, 90)
    endFrameInput = ac.addTextInput(appWindow, "")
    ac.setPosition(endFrameInput, 120, 90)
    ac.setSize(endFrameInput, 100, 20)

    # Current Frame Label
    currentFrameLabel = ac.addLabel(appWindow, "Current Frame: 0")
    ac.setPosition(currentFrameLabel, 20, 130)

    currentModeLabel= ac.addLabel(appWindow, "Current Mode: 0")
    ac.setPosition(currentModeLabel, 20, 150)
    return "Replay Frame Looper"

def acUpdate(deltaT):
    
    global checkboxState, startFrameInput, endFrameInput, currentFrameLabel, currentModeLabel
    global lastFrame, currentCameraIndex

    current_frame = ac.ext_getReplayPosition()
    ac.setText(currentFrameLabel, "Current Frame: " + str(current_frame))

    if checkboxState != 1:
        lastFrame = current_frame
        return

    try:
        start_frame = int(ac.getText(startFrameInput))
        end_frame = int(ac.getText(endFrameInput))
    except ValueError:
        lastFrame = current_frame
        return  # Invalid input

    if end_frame <= start_frame:
        lastFrame = current_frame
        return  # Invalid range

    # If out of bounds, reset to start and cycle camera
    if current_frame < start_frame or current_frame > end_frame:
        ac.ext_setReplayPosition(start_frame)

        # Cycle camera: 1 → 2 → 3 → 1 ...
        currentCameraIndex = (currentCameraIndex + 1) % len(camera_modes) 
        currentCameraMode = camera_modes[currentCameraIndex]
        ac.ext_setCurrentCamera(currentCameraMode)
        ac.setText(currentModeLabel, "Current Mode: " + str(currentCameraMode))

    lastFrame = current_frame

def onCheckboxChanged(name, state):
    global checkboxState
    checkboxState = state

