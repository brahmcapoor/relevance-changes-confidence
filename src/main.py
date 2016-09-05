from psychopy import gui, visual
from experiment_objects import Trial
import testing

def get_subject_info():
    check = gui.Dlg("Startup")

    check.addField("New Experiment?", False)
    check.addField("Subject Number", 1)
    check.addField("Round Number", 1)

    check.show()

    return tuple(check.data)

def main():

    new_experiment, subject_number, round_number = get_subject_info()

    win = visual.Window([1680,1050],
                          monitor = "testMonitor",
                          units = "cm",
                          color = 'black',
                          colorSpace='rgb',
                          fullscr = True)


    trial = Trial(win, subject_number, round_number)

    testing.main(trial)



if __name__ == '__main__':
    main()
