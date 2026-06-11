def fingers_up(landmarks):
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    fingers = []
    is_right_hand = landmarks[0][0] < landmarks[17][0]
    if is_right_hand:
        fingers.append(1 if landmarks[4][0] < landmarks[3][0] else 0)
    else:
        fingers.append(1 if landmarks[4][0] > landmarks[3][0] else 0)
    for tip, pip in zip(tips, pips):
        fingers.append(1 if landmarks[tip][1] < landmarks[pip][1] else 0)
    return fingers

def classify_gesture(fingers):
    gestures = {
        (0,0,0,0,0): "Fist",
        (1,1,1,1,1): "Open Palm",
        (1,0,0,0,0): "Thumbs Up",
        (0,1,1,0,0): "Peace",
        (0,1,0,0,0): "Pointing",
        (1,1,0,0,1): "Rock",
        (0,1,1,1,1): "Four Fingers",
    }
    return gestures.get(tuple(fingers), "Unknown")