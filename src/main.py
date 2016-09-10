from psychopy import gui, visual
from experiment_objects import Trial
import new_testing
import os
import shutil


def get_subject_info():
    check = gui.Dlg("Startup")

    check.addField("New Experiment?", False)
    check.addField("Subject Number", 1)
    check.addField("Round Number", 1)

    check.show()

    return tuple(check.data)


def delete_logs():

    folder = ""
    if 'src' in os.getcwd():
        folder = "../subject_logs"
    else:
        folder = "subject_logs"

    if os.path.exists(folder):
        shutil.rmtree(folder)

    os.mkdir(folder)


def main():

    new_experiment, subject_number, round_number = get_subject_info()

    if new_experiment:
        delete_logs()

    window = visual.Window([1680, 1050],
                           monitor="testMonitor",
                           units="cm",
                           color='black',
                           colorSpace='rgb',
                           fullscr=True)

    trial = Trial(window, subject_number, round_number)

    new_testing.main(trial)

if __name__ == '__main__':
    main()
