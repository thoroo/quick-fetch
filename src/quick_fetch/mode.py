
import inquirer

_MODE_MOUSE = 'Grab from mouse position'
_MODE_XPATH = 'Fetch from XPaths'

def pick_mode():
    
    question = [
        inquirer.List(name='mode',
                      message='Choose download mode',
                      choices=[_MODE_MOUSE, _MODE_XPATH])
    ]

    chosen_mode = next(iter(inquirer.prompt(question).values()))

    return chosen_mode