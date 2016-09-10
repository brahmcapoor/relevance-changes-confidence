from __future__ import division
from psychopy import visual, core, event, logging
from random import shuffle
import csv
import os


def generate_log_message(param):
    """
    Generates the log message for a specific trial, given the paramter tuple
    """
    condition = param[0]
    first_stim = ""
    second_stim = ""
    detail = ""
    if condition == 1:
        if param[1]:
            second_stim = "disc"
            first_stim = "blank"
        else:
            first_stim = "disc"
            second_stim = "blank"
        detail = "Disc contrast is {}%.".format(16*param[2]-15)
    if condition == 2:
        if param[1]:
            first_stim = "Right tilted gabor"
        else:
            first_stim = "Left tilted gabor"

        if param[2]:
            second_stim = "Right tilted gabor"
        else:
            second_stim = "Left tilted gabor"
    if condition == 3:
        pass

    log_message = "Condition {}. ".format(condition)
    log_message += "First Stimulus is the {}. ".format(first_stim)
    log_message += "Second Stimulus is the {}. ".format(second_stim)
    log_message += detail

    logging.warn(log_message)
    logging.flush()


def show_feedback(window, proportion):

        feedback = "Your accuracy: {}%".format(proportion)

        feedback = visual.TextStim(window,
                                   text=feedback,
                                   alignHoriz='center',
                                   alignVert='center')

        for frameN in range(120):
            feedback.draw()
            window.flip()


def stimulus_and_mask(window, stimulus, question):
    N_MASK_SECONDS = 0.5
    N_STIM_SECONDS = 0.1

    MASK_1 = visual.GratingStim(window, tex='sin', mask='gauss', sf=5,
                                name='gabor', size=[8, 8], autoLog=False)

    MASK_2 = visual.GratingStim(window, tex='sin', mask='gauss', sf=5,
                                name='gabor', size=[8, 8], ori=90,
                                autoLog=False)

    for frameN in range(int(N_MASK_SECONDS * 60)):
        MASK_1.draw()
        MASK_2.draw()
        window.flip()

    for frameN in range(int(N_STIM_SECONDS * 60)):
        stimulus.draw()
        window.flip()

    for frameN in range(int(N_MASK_SECONDS * 60)):
        MASK_1.draw()
        MASK_2.draw()
        window.flip()

    question = visual.TextStim(window,
                               text=question)

    question.draw()
    window.flip()

    keys = event.waitKeys(keyList=['left', 'right'])
    if keys[0] == 'right':
        logging.warn("Subject said RIGHT")
    else:
        logging.warn("Subject said LEFT")
    logging.flush()

    window.flip()

    return int(keys[0] == 'right')


def trial(window, first_stim, second_stim, question_1, question_2):
    response_1 = stimulus_and_mask(window, first_stim, question_1)
    response_2 = stimulus_and_mask(window, second_stim, question_1)

    last_question = visual.TextStim(window,
                                    text=question_2)

    last_question.draw()
    window.flip()

    keys = event.waitKeys(keyList=['1', '2'])
    if keys[0] == '1':
        logging.warn("Subject more confident about the first trial")
    else:
        logging.warn("Subject more confident about the second trial")
    logging.flush()

    window.flip()

    return (response_1, response_2, int(keys[0])-1)


def block_1_trials():

    N_TRIALS = 54
    all_trials = [i for i in range(N_TRIALS)]
    shuffle(all_trials)

    # condition 1: blank & disc - 2 positions x 7 contrasts
    # condition 2: 2 gabors - 2 orientations x 2 orientation

    trial_params = {
        # condition 1
        # format: (condition number, disc position, disc contrast)
        (1, 0, 1): all_trials[:1],
        (1, 0, 2): all_trials[1:2],
        (1, 0, 3): all_trials[2:3],
        (1, 0, 4): all_trials[3:4],
        (1, 0, 5): all_trials[4:5],
        (1, 0, 6): all_trials[5:6],
        (1, 0, 7): all_trials[6:7],
        (1, 1, 1): all_trials[7:8],
        (1, 1, 2): all_trials[8:9],
        (1, 1, 3): all_trials[9:10],
        (1, 1, 4): all_trials[10:11],
        (1, 1, 5): all_trials[11:12],
        (1, 1, 6): all_trials[12:13],
        (1, 1, 6): all_trials[13:14],

        # condition 2
        # format: (condition number, first orientation, second orientation)
        (2, 0, 0): all_trials[14:24],
        (2, 0, 1): all_trials[24:34],
        (2, 1, 0): all_trials[34:44],
        (2, 1, 1): all_trials[44:54]

    }

    return trial_params


def find_param(trial_num, trial_params):
    for param in trial_params.keys():
        if trial_num in trial_params[param]:
            return param


def block_1(window, filename):

    # Declaring the constants.
    CONTRASTS = [0, 0.01, 0.17, 0.33, 0.49, 0.65, 0.81, 0.97]  # disc contrasts
    TILT_ANGlE = 10  # for the gabor
    gabor_contrast = 0.5

    discs = [visual.Circle(win=window,
                           radius=2.6,
                           fillColor='white',
                           lineWidth=0,
                           opacity=contrast) for contrast in CONTRASTS]

    blank = discs[0]

    gabors = [visual.GratingStim(window,
                                 tex='sin',
                                 mask='gauss',
                                 sf=5,
                                 name='gabor',
                                 size=[8, 8],
                                 ori=TILT_ANGlE * i,
                                 autoLog=False,
                                 opacity=gabor_contrast) for i in [-1, 1]]

    questions = ["Left or Right?",
                 "Which one were you more confident about?"]

    trial_params = block_1_trials()

    stimulus_param = [None, None]

    last_one_correct = False

    n_correct = 0
    n_counted = 0

    for trial_num in range(54):

        result = [trial_num + 1]

        if n_counted > 0 and not trial_num % 10:
            try:
                show_feedback(window, (n_correct/n_counted)*100)
                n_counted = 0
                n_correct = 0
            except ZeroDivisionError:
                pass

        logging.warn("BLOCK 1, TRIAL {}".format(trial_num + 1))
        logging.flush()
        param = find_param(trial_num, trial_params)
        generate_log_message(param)

        if param[0] == 1:
            # condition 1
            result.append(1)
            disc_position = param[1]
            blank_position = 1 - disc_position

            disc_stim = discs[param[2]]

            stimulus_param[disc_position] = disc_stim
            stimulus_param[blank_position] = blank

            result += [param[1], (param[2]*16-15)]
            result += ["", "", "", "", "", ""]

        else:
            # condition 2
            result.append(2)
            first_gabor = gabors[param[1]]
            second_gabor = gabors[param[2]]
            first_gabor.opacity = gabor_contrast
            second_gabor.opacity = gabor_contrast
            stimulus_param = [first_gabor, second_gabor]

            result += ["", ""]
            result += [first_gabor.ori, second_gabor.ori, gabor_contrast]
            result += ["", "", ""]

        response = trial(window, *(stimulus_param + questions))
        result += [response[0], response[1], response[2]+1]

        with open(filename, 'ab') as f:
            wr = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
            wr.writerow(result)

        # Float transparency of gabor
        if param[0] == 2:
            n_counted += 1
            confident_trial = response[2]
            if response[confident_trial] == param[confident_trial + 1]:
                # correct trial
                n_correct += 1
                logging.warn("CORRECT TRIAL")
                logging.flush()

                if last_one_correct:
                    logging.warn("Two successive correct trials")
                    logging.flush()
                    gabor_contrast -= 0.02
                    if gabor_contrast < 0.02:
                        gabor_contrast = 0.02
                        logging.warn("Minimum contrast for Gabor reached")
                        logging.flush()
                    logging.warn("Gabor contrast is now {}"
                                 .format(gabor_contrast))

                last_one_correct = not last_one_correct

        trial_record = [trial_num] + list(param) + list(response)

        logging.warn("\n\n\n")

    return gabor_transparency


def create_log_files(subject_number, round_number):
    filename = ""
    if "src" in os.getcwd():
        filename = "../subject_logs/subject_{}_round_{}.csv" \
            .format(subject_number, round_number)
    else:
        filename = "subject_logs/subject_{}.csv_round_{}" \
            .format(subject_number, round_number)

    with open(filename, 'wb') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)

        header = ["", "", "Trial Parameters",
                  "", "", "", "", "", "", "",
                  "Subject Response"]

        subheader_1 = ["", "",
                       "Condition 1", "",
                       "Condition 2", "", "",
                       "Condition 3", "", "",
                       "Block 1", "", "",
                       "Block 2"]

        subheader_2 = ["Trial Number", "Condition",
                       "Disc position", "Contrast",
                       "First Gabor Tilt", "Second Gabor Tilt", "Contrast",
                       "Stimulus Position", "Stimulus", "Contrast",
                       "Tilt 1 (1=right)", "Tilt 2 (1=right)",
                                           "Confident trial",
                       "Stimulus 1 seen", "Stimulus 2 seen", "Gabor or Disc?"]

        wr.writerow(header)
        wr.writerow(subheader_1)
        wr.writerow(subheader_2)

    return filename


def main(trial):

    window = trial.window
    subject_number = trial.subject_number
    round_number = trial.round_number

    filename = create_log_files(subject_number, round_number)

    gabor_transparency = block_1(window, filename)
    # block_2(window, filename)

if __name__ == '__main__':
    main()
