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
            first_stim = "right tilted gabor"
        else:
            first_stim = "left tilted gabor"

        if param[2]:
            second_stim = "right tilted gabor"
        else:
            second_stim = "left tilted gabor"
    if condition == 3:
        if param[1]:
            first_stim = "blank"
            if param[2] == 0:
                second_stim = "disc"
            elif param[2] == 1:
                second_stim = "left tilted gabor"
            else:
                second_stim = "right tilted gabor"
        else:
            second_stim = "blank"
            if param[2] == 0:
                first_stim = "disc"
            elif param[2] == 1:
                first_stim = "left tilted gabor"
            else:
                first_stim = "right tilted gabor"

    log_message = "Condition {}. ".format(condition)
    log_message += "First Stimulus is the {}. ".format(first_stim)
    log_message += "Second Stimulus is the {}. ".format(second_stim)
    log_message += detail

    logging.warn(log_message)
    logging.flush()


def press_to_continue(window, message):

    prompt = visual.TextStim(window,
                             text=message,
                             alignHoriz='center',
                             alignVert='center')

    prompt.draw()
    window.flip()

    event.waitKeys(keyList=['space'])

    window.flip()


def show_feedback(window, proportion):

        feedback = "Your accuracy: {}%".format(proportion)

        feedback = visual.TextStim(window,
                                   text=feedback,
                                   alignHoriz='center',
                                   alignVert='center')

        for frameN in range(120):
            feedback.draw()
            window.flip()


def stimulus_and_mask(window, stimulus, question, block3):
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
        if not block3:
            logging.warn("Subject said RIGHT")
        else:
            logging.warn("Subject saw stimulus")
    else:
        if not block3:
            logging.warn("Subject said LEFT")
        else:
            logging.warn("Subject didn't see stimulus")
    logging.flush()

    window.flip()

    return int(keys[0] == 'right') * 2 - 1


def trial(window, first_stim, second_stim, question_1, question_2,
          block3=False):
    response_1 = stimulus_and_mask(window, first_stim, question_1, block3)
    response_2 = stimulus_and_mask(window, second_stim, question_1, block3)

    last_question = visual.TextStim(window,
                                    text=question_2)

    if block3:
        if response_1 == -1 and response_2 == -1:
            return (-1, -1, 2)
    last_question.draw()
    window.flip()

    keys = event.waitKeys(keyList=['1', '2'])
    if keys[0] == '1':
        if not block3:
            logging.warn("Subject more confident about the first trial")
        else:
            logging.warn("Subject saw a Gabor")
    else:
        if not block3:
            logging.warn("Subject more confident about the second trial")
        else:
            logging.warn("Subject saw a disc")
    logging.flush()

    window.flip()

    return (response_1, response_2, int(keys[0])-1)


def find_param(trial_num, trial_params):
    for param in trial_params.keys():
        if trial_num in trial_params[param]:
            return param


def block_1_trials():

    N_TRIALS = 540
    all_trials = [i for i in range(N_TRIALS)]
    shuffle(all_trials)

    # condition 1: blank & disc - 2 positions x 7 contrasts
    # condition 2: 2 gabors - 2 orientations x 2 orientation

    trial_params = {
        # condition 1
        # format: (condition number, disc position, disc contrast)
        (1, 0, 1): all_trials[:10],
        (1, 0, 2): all_trials[10:20],
        (1, 0, 3): all_trials[20:30],
        (1, 0, 4): all_trials[30:40],
        (1, 0, 5): all_trials[40:50],
        (1, 0, 6): all_trials[50:60],
        (1, 0, 7): all_trials[60:70],
        (1, 1, 1): all_trials[70:80],
        (1, 1, 2): all_trials[80:90],
        (1, 1, 3): all_trials[90:100],
        (1, 1, 4): all_trials[100:110],
        (1, 1, 5): all_trials[110:120],
        (1, 1, 6): all_trials[120:130],
        (1, 1, 7): all_trials[130:140],

        # condition 2
        # format: (condition number, first orientation, second orientation)
        (2, 0, 0): all_trials[140:240],
        (2, 0, 1): all_trials[240:340],
        (2, 1, 0): all_trials[340:440],
        (2, 1, 1): all_trials[440:]

    }

    return trial_params


def block_1(window, filename, discs):

    # Declaring the constants.
    TILT_ANGlE = 10  # for the gabor
    first_interval_contrast = 0.5
    second_interval_contrast = 0.5

    blank = discs[0]

    gabors_first = [visual.GratingStim(window,
                                       tex='sin',
                                       mask='gauss',
                                       sf=5,
                                       name='gabor',
                                       size=[8, 8],
                                       ori=TILT_ANGlE * i,
                                       autoLog=False,
                                       opacity=first_interval_contrast)
                    for i in [-1, 1]]

    gabors_second = [visual.GratingStim(window,
                                        tex='sin',
                                        mask='gauss',
                                        sf=5,
                                        name='gabor',
                                        size=[8, 8],
                                        ori=TILT_ANGlE * i,
                                        autoLog=False,
                                        opacity=second_interval_contrast)
                     for i in [-1, 1]]

    questions = ["Left or Right?",
                 "Which one were you more confident about?"]

    trial_params = block_1_trials()

    stimulus_param = [None, None]

    last_one_correct_first = False
    last_one_correct_second = False

    n_correct = 0
    n_counted = 0

    for trial_num in range(540):
        press_to_continue(window, "Press space to continue")

        result = [trial_num + 1]

        if n_counted > 0 and not trial_num % 10:
            try:
                show_feedback(window, (n_correct/n_counted)*100)
                n_counted = 0
                n_correct = 0
                press_to_continue(window, "Press space to continue")
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
            result += ["", "", "", "", "", "", ""]

        else:
            # condition 2
            result.append(2)
            first_gabor = gabors_first[param[1]]
            second_gabor = gabors_second[param[2]]
            first_gabor.opacity = first_interval_contrast
            second_gabor.opacity = second_interval_contrast
            stimulus_param = [first_gabor, second_gabor]

            result += ["", ""]
            result += [first_gabor.ori, second_gabor.ori,
                       first_interval_contrast, second_interval_contrast]
            result += ["", "", ""]

        response = trial(window, *(stimulus_param + questions))
        result += [response[0]*TILT_ANGlE, response[1]*TILT_ANGlE,
                   response[2]+1]

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

                if confident_trial == 0:
                    if last_one_correct_first:
                        logging.warn("Two successive correct trials for the" +
                                     "first condition")
                        logging.flush()
                        first_interval_contrast -= 0.02
                        if first_interval_contrast < 0.02:
                            first_interval_contrast = 0.02
                            logging.warn("Minimum contrast for Gabor 1" +
                                         " reached")
                            logging.flush()
                        logging.warn("First interval gabor contrast is now {}"
                                     .format(first_interval_contrast))
                        logging.flush()

                    last_one_correct_first = not last_one_correct_first

                elif confident_trial == 1:
                    if last_one_correct_second:
                        logging.warn("Two successive correct trials for the" +
                                     " second condition")
                        logging.flush()
                        second_interval_contrast -= 0.02
                        if second_interval_contrast < 0.02:
                            second_interval_contrast = 0.02
                            logging.warn("Minimum contrast for Gabor 2" +
                                         " reached")
                            logging.flush()
                        logging.warn("Second interval gabor contrast is now {}"
                                     .format(second_interval_contrast))
                        logging.flush()

                    last_one_correct_second = not last_one_correct_second

            else:
                # Incorrect response
                logging.warn("Incorrect trial")
                logging.flush()
                if confident_trial == 0:
                    logging.warn("Increasing first interval contrast")
                    logging.flush()
                    first_interval_contrast += 0.02
                    if first_interval_contrast > 1:
                        first_interval_contrast = 1
                        logging.warn("Maximum contrast for first interval" +
                                     " reached")
                        logging.flush()
                    logging.warn("First interval contrast is now {}"
                                 .format(first_interval_contrast))
                    logging.flush()
                    last_one_correct_first = False

                elif confident_trial == 1:
                    logging.warn("Increasing second interval contrast")
                    logging.flush()
                    second_interval_contrast += 0.02
                    if second_interval_contrast > 1:
                        second_interval_contrast = 1
                        logging.warn("Maximum contrast for second interval" +
                                     " reached")
                        logging.flush()
                    logging.warn("Second interval contrast is now {}"
                                 .format(second_interval_contrast))
                    logging.flush()
                    last_one_correct_second = False


        logging.warn("\n\n\n")

    return (first_interval_contrast, second_interval_contrast)


def block_2_trials():

    N_TRIALS = 340
    all_trials = [i for i in range(N_TRIALS)]
    shuffle(all_trials)

    trial_params = {
        # format: (condition, stimulus position, stimulus
        # (0= disc, 1=gabor_left, 2= gabor_right), contrast level)

        (3, 0, 0, 1): all_trials[:10],
        (3, 0, 0, 2): all_trials[10:20],
        (3, 0, 0, 3): all_trials[20:30],
        (3, 0, 0, 4): all_trials[30:40],
        (3, 0, 0, 5): all_trials[40:50],
        (3, 0, 0, 6): all_trials[50:60],
        (3, 0, 0, 7): all_trials[60:70],

        (3, 0, 1, 1): all_trials[70:80],
        (3, 0, 1, 2): all_trials[80:90],
        (3, 0, 1, 3): all_trials[90:100],
        (3, 0, 1, 4): all_trials[100:110],
        (3, 0, 1, 5): all_trials[110:120],

        (3, 1, 0, 1): all_trials[120:130],
        (3, 1, 0, 2): all_trials[130:140],
        (3, 1, 0, 3): all_trials[140:150],
        (3, 1, 0, 4): all_trials[150:160],
        (3, 1, 0, 5): all_trials[160:170],
        (3, 1, 0, 6): all_trials[170:180],
        (3, 1, 0, 7): all_trials[180:190],

        (3, 1, 1, 1): all_trials[190:200],
        (3, 1, 1, 2): all_trials[200:210],
        (3, 1, 1, 3): all_trials[210:220],
        (3, 1, 1, 4): all_trials[220:230],
        (3, 1, 1, 5): all_trials[230:240],

        (3, 0, 2, 1): all_trials[240:250],
        (3, 0, 2, 2): all_trials[250:260],
        (3, 0, 2, 3): all_trials[260:270],
        (3, 0, 2, 4): all_trials[270:280],
        (3, 0, 2, 5): all_trials[280:290],

        (3, 1, 2, 1): all_trials[290:300],
        (3, 1, 2, 2): all_trials[300:310],
        (3, 1, 2, 3): all_trials[310:320],
        (3, 1, 2, 4): all_trials[320:330],
        (3, 1, 2, 5): all_trials[330:]

    }

    return trial_params


def generate_contrasts(contrast):
    if 0.9 > contrast > 0.1:
        return [contrast - 0.1, contrast - 0.05, contrast,
                contrast + 0.05, contrast + 0.1]

    elif contrast <= 0.1:
        return [contrast * 0.35, contrast * 0.65, contrast,
                contrast * 1.35, contrast * 1.65]

    elif contrast >= 0.9:
        distance_to_1 = 1 - contrast

        return [contrast - distance_to_1 * 0.65,
                contrast - distance_to_1 * 0.35,
                contrast,
                contrast + distance_to_1 * 0.35,
                contrast + distance_to_1 * 0.65]


def block_2(window, filename, discs, first_interval_contrast=0.5,
            second_interval_contrast=0.5):
    TILT_ANGLE = 10

    blank = discs[0]

    gabor_first_transparencies = generate_contrasts(first_interval_contrast)

    gabor_second_transparencies = generate_contrasts(second_interval_contrast)

    gabor_right = visual.GratingStim(window,
                                     tex='sin',
                                     mask='gauss',
                                     sf=5,
                                     name='gabor',
                                     size=[8, 8],
                                     ori=10,
                                     autoLog=False)

    gabor_left = visual.GratingStim(window,
                                    tex='sin',
                                    mask='gauss',
                                    sf=5,
                                    name='gabor',
                                    size=[8, 8],
                                    ori=-10,
                                    autoLog=False)

    questions = ["Did you see something? (Press Left for No, Right for Yes)",
                 "Gabor or disc? (1 for Gabor, 2 for Disc)"]

    trial_params = block_2_trials()

    for trial_num in range(34):
        press_to_continue(window, "Press space to continue")

        logging.warn("BLOCK 2, TRIAL {}".format(trial_num+1))
        logging.flush()

        param = find_param(trial_num, trial_params)
        generate_log_message(param)

        result = [55 + trial_num, 3, "", "", "", "", "", "", param[1] + 1,
                  param[2]]

        stimulus_param = [None, None]
        stimulus = None

        if param[2] == 0:
            stimulus = discs[param[3]]
            logging.warn("Disc contrast is {}".format(stimulus.opacity))
            logging.flush()

        if param[2] == 1:
            stimulus = gabor_left
            if param[1] == 0:
                stimulus.opacity = gabor_first_transparencies[param[3] - 1]
            else:
                stimulus.opacity = gabor_second_transparencies[param[3] - 1]
            logging.warn("Gabor contrast is {}".format(stimulus.opacity))
            logging.flush()

        if param[2] == 2:
            stimulus = gabor_right
            if param[1] == 0:
                stimulus.opacity = gabor_first_transparencies[param[3] - 1]
            else:
                stimulus.opacity = gabor_second_transparencies[param[3] - 1]
            logging.warn("Gabor contrast is {}".format(stimulus.opacity))
            logging.flush()

        result += [stimulus.opacity, "", "", ""]
        stimulus_param[param[1]] = stimulus
        stimulus_param[1 - param[1]] = blank

        response = trial(window, *(stimulus_param + questions), block3=True)

        result += [(response[0]+1)/2,
                   (response[1]+1)/2,
                   response[2]]

        with open(filename, 'ab') as f:
            wr = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
            wr.writerow(result)

        logging.warn("\n\n\n")
        logging.flush()


def generate_log_file(subject_number, round_number):
    filename = ""
    if "src" in os.getcwd():
        filename = "../subject_logs/subject_{}_round_{}.csv" \
            .format(subject_number, round_number)
    else:
        filename = "subject_logs/subject_{}_round_{}.csv" \
            .format(subject_number, round_number)

    with open(filename, 'wb') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)

        header = ["", "", "Trial Parameters",
                  "", "", "", "", "", "", "", "",
                  "Subject Response"]

        subheader_1 = ["", "",
                       "Condition 1", "",
                       "Condition 2", "", "", "",
                       "Condition 3", "", "",
                       "Block 1", "", "",
                       "Block 2"]

        subheader_2 = ["Trial Number", "Condition",
                       "Disc position", "Contrast",
                       "First Gabor Tilt", "Second Gabor Tilt",
                       "First Gabor Contrast", "Second Gabor Contrast",
                       "Stimulus Position",
                       "Stimulus (0= disc, 1/2 = gabor left/right)",
                       "Contrast",
                       "Tilt 1 (1=right)", "Tilt 2 (1=right)",
                                           "Confident trial",
                       "Stimulus 1 seen", "Stimulus 2 seen",
                       "Gabor or Disc?(0 = gabor, 1 = disc, 2=unseen)"]

        wr.writerow(header)
        wr.writerow(subheader_1)
        wr.writerow(subheader_2)

    return filename


def main(trial):

    window = trial.window
    subject_number = trial.subject_number
    round_number = trial.round_number

    filename = generate_log_file(subject_number, round_number)

    CONTRASTS = [0, 0.01, 0.17, 0.33, 0.49, 0.65, 0.81, 0.97]  # disc contrasts

    discs = [visual.Circle(win=window,
                           radius=2.6,
                           fillColor='white',
                           lineWidth=0,
                           opacity=contrast) for contrast in CONTRASTS]

    first_interval_contrast, second_interval_contrast = block_1(window,
                                                                filename,
                                                                discs)
    press_to_continue(window, "End of section.")

    block_2(window, filename, discs, first_interval_contrast,
            second_interval_contrast)


if __name__ == '__main__':
    main()
