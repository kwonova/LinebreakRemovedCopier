from pynput import keyboard
import clipboard

current_pressed = set()

# Define variables
global copyReadyState
copyReadyState = False
global copied
copied = False
global copiedString
copiedString = ''
global superCopied
superCopied = False

# When 'key' is pressed
def on_press(key):
    global copyReadyState
    global superCopied
    global copiedString

    # Add 'key' to current_pressed
    current_pressed.add(key)

    # When LineBreakRemovedCopy is ready and Ctrl+C is pressed again
    if copyReadyState and keyboard.KeyCode.from_char('\x03') in current_pressed:
        copyReadyState = False

        # Get clipboard data to result
        result = clipboard.paste()

        # When the 'result' is a text, remove line breaks and save a new text in 'copiedString'
        if len(result) != 0:
            resultChanged = result.split('\n')
            strippedResultList = []
            for i in resultChanged:
                strippedResultList.append(i.strip())
            copiedString = ' '.join(s for s in strippedResultList)
            superCopied = True

# When 'key' is released
def on_release(key):
    global copyReadyState
    global copied
    global superCopied
    global copiedString

    # When Ctrl+C is initially pressed and when C is released
    if keyboard.KeyCode.from_char('\x03') in current_pressed and keyboard.Key.ctrl_l in current_pressed and not copyReadyState:
        copied = True

    # When the text has been already LineBreakRemovedCopied and C is released
    if keyboard.KeyCode.from_char(
            '\x03') in current_pressed and keyboard.Key.ctrl_l in current_pressed and superCopied:

        # When 'copiedString' is a text, bring copiedString to the clipboard
        if len(copiedString) != 0:
            clipboard.copy(copiedString)

    # When 'key' is released
    if key in current_pressed:

        # Delete 'key' value from current_pressed
        current_pressed.remove(key)

        # When 'key' was left Ctrl key, initialize all states
        if keyboard.Key.ctrl_l == key:
            superCopied = False
            copied = False
            copyReadyState = False
            current_pressed.clear()

        # When firstly copied and when left Ctrl key remains, make LineBreakRemovedCopy be ready
        if copied and keyboard.Key.ctrl_l in current_pressed and not copyReadyState:
            copyReadyState = True
            copied = False

print('Welcome to Linebreak Removed Copier\n')
print('※ This tool is dedicated to lab buddies whose first language is not English.\n')
print("※ How to use: Ctrl + C C.")
print("  - When you copy the text using Ctrl + C, just click C key again (while pressing Ctrl key)")
print("  - You can also minimize this window.\n")
print("※ When this tool is seemingly stopped:")
print("  - Press 'Arrow' keys(→ ← ↑ ↓) and 'End' key multiple times in this console window.\n")
print("※ Contact : kwonova@yonsei.ac.kr")
print("\n")
print("Ready for copy...")
print("\n")

# Execution
with keyboard.Listener(
    on_press=on_press,
    on_release=on_release) as listener:
    listener.join()
