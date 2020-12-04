# GUI to centralize the program

## Step 1: Take face and body pictures

## Step 2: Push submit button.
The pictures will be sent as messages to the respective topics: face recognition to detect if it is a new subject or existing, pose estimation to identify 
anatomical ratios and BMI estimation.

## Step 3: Receive messages with BMI estimation, user ID, and anatomical ratios.

## Step 4: Dislay BMI, ratios and historical data if user exists. 


## Files:

mplwidget.py: Class definition to add matplotlib figures

acquire_images_gui.ui: Original xml code with the controls of the GUI

wwgui.py: Actual library with the GUI controls in python

wwatchers.py: Main program. run with python3 wwatchers.py

