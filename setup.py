files = {
'action_mapper.py': 'ACTION_MAP = {\n    "Fist": "Pause",\n    "Open Palm": "Play",\n    "Thumbs Up": "Volume Up",\n    "Peace": "Mute",\n    "Pointing": "Next Track",\n    "Rock": "Shuffle",\n    "Four Fingers": "Previous Track",\n}\ndef get_action(gesture):\n    return ACTION_MAP.get(gesture, "No Action")\n',
'gesture_classifier.py': 'def fingers_up(landmarks):\n    tips = [8,12,16,20]\n    pips = [6,10,14,18]\n    fingers = []\n    fingers.append(1 if landmarks[4][0] > landmarks[3][0] else 0)\n    for tip,pip in zip(tips,pips):\n        fingers.append(1 if landmarks[tip][1] < landmarks[pip][1] else 0)\n    return fingers\ndef classify_gesture(fingers):\n    gestures = {(0,0,0,0,0):"Fist",(1,1,1,1,1):"Open Palm",(1,0,0,0,0):"Thumbs Up",(0,1,1,0,0):"Peace",(0,1,0,0,0):"Pointing",(1,1,0,0,1):"Rock",(0,1,1,1,1):"Four Fingers"}\n    return gestures.get(tuple(fingers),"Unknown")\n',
}
for filename, content in files.items():
    open(filename, 'w').write(content)
    print(f'{filename} created OK')
print('ALL FILES CREATED!')