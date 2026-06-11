ACTION_MAP = {
    "Fist": "Pause",
    "Open Palm": "Play",
    "Thumbs Up": "Volume Up",
    "Peace": "Mute",
    "Pointing": "Next Track",
    "Rock": "Shuffle",
    "Four Fingers": "Previous Track",
}
def get_action(gesture):
    return ACTION_MAP.get(gesture, "No Action")
