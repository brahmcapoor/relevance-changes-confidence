from psychopy import visual, core, event, logging
from random import shuffle

def stimulus_and_mask(win, stimulus, stim_number, mask_1, mask_2, prompt, dys):
    """
    Shows a single stimulus begind a mask. Params are
    self explanatory

    If the trial is a dys trial, returns a boolean indicating if the stimulus
    was seen. If the trial is a normal trial, returns an integer indicating if
    the stimulus was percieved to be angled right or left.
    """

    N_MASK_SECONDS = 0
    N_STIM_SECONDS = 1

    #first stimulus
    for i in range(int(N_MASK_SECONDS * 60)):
        mask_1.draw()
        mask_2.draw()
        win.flip()

    for i in range(int(N_STIM_SECONDS * 60)):
        stimulus.draw()
        win.flip()

    for i in range(int(N_MASK_SECONDS * 60)):
        mask_1.draw()
        mask_2.draw()
        win.flip()

    prompt.draw()
    win.flip()

    return_val = ""
    if dys:
        while True:
            keys = event.getKeys(['right', 'left'])
            if keys:
                break

        if keys[0] == 'right':
            logging.warn("Subject saw {} stimulus".format(stim_number))
            return_val = True
        else:
            logging.warn("Subject didn't see {} stimulus".format(stim_number))
            return_val = False

    else:
        while True:
            keys = event.getKeys(['right', 'left'])
            if keys:
                break

        if keys[0] == 'right':
            logging.warn("Subject said {} stimulus was tilted right".format(stim_number))
            return_val = 10
        else:
            logging.warn("Subject said {} stimulus was tilted left".format(stim_number))
            return_val = -10

    logging.flush()
    win.flip()

    return return_val

def trial(win, stim_1, stim_2, calibrator=False):
    """
    Performs a single Trial

    stim_1 = stimulus shown first
    stim_2 = stimulus shown second
    calibrator = if True, question is "Did you see something?"

    Returns a tuple: (a, b, c) where a is the index of the trial that the
    subject is more confident about, b is the response to the first
    stimulus and c is the response to the second stimulus
    """

    mask_1 = visual.GratingStim(win, tex='sin', mask='gauss', sf= 5,
        name='gabor', size = [8,8], autoLog=False)

    mask_2 = visual.GratingStim(win, tex='sin', mask='gauss', sf= 5,
        name='gabor', size = [8,8], ori = 90, autoLog=False)

    prompt = ""
    if calibrator:
        prompt = "Did you see something?"
    else:
        prompt = "Left or Right?"

    prompt = visual.TextStim(win,
                             text = prompt,
                             alignHoriz = 'center',
                             alignVert = 'center')

    last_question = visual.TextStim(win,
                                    text = "Which were you more confident about?",
                                    alignHoriz = 'center',
                                    alignVert = 'center')

    stim_1_response = stimulus_and_mask(win, stim_1, "first", mask_1, mask_2, prompt, calibrator)
    stim_2_response = stimulus_and_mask(win, stim_2, "second", mask_1, mask_2, prompt, calibrator)

    last_question.draw()
    win.flip()

    confident_trial = 0

    while True:
        keys = event.getKeys(['1', '2'])
        if keys:
            break

    if keys[0] == '1':
        logging.warn("Subject was more confident about the first stimulus")
        confident_trial = 0
    else:
        logging.warn("Subject was more confident about the second stimulus")
        confident_trial = 1


    logging.flush()

    return (confident_trial, stim_1_response, stim_2_response)

def show_feedback(window, proportion):
    """
    The feedback to be shown every 10 trials
    """

    feedback = "Your accuracy: {}%".format(proportion)

    feedback = visual.TextStim(window,
                               text = feedback,
                               alignHoriz = 'center',
                               alignVert = 'center')

    for frameN in range(120):
        feedback.draw()
        window.flip()

def generate_log(trial_param):

    """
    Generates the log message for a particular trial.
    """

    first_stim, \
    second_stim, \
    gabor_visibility, \
    disc_contrast, \
    gabor_orientation, \
    dys_trial = trial_param

    gabor_index = ""
    if isinstance(first_stim, visual.GratingStim):
        gabor_index = "first"
    else:
        gabor_index = "second"

    gabor_visible = ""
    if not gabor_visibility:
        gabor_visible = "and invisible"

    gabor_tilt = ""
    if gabor_orientation > 0:
        gabor_tilt = "and is tilted right"
    elif gabor_orientation < 0:
        gabor_tilt = "and is tilted left"

    trial_check = ""
    if dys_trial:
        trial_check = "if stimulus is seen"
    else:
        trial_check = "tilt of stimulus"



    return "Gabor is {} {}{}. Disc contrast is {}. Trial checks {}. ".format(gabor_index,
                                                                             gabor_visible,
                                                                             gabor_tilt,
                                                                             disc_contrast,
                                                                             trial_check)

def press_to_continue(window):

    prompt = visual.TextStim(window,
                             text = "Press space to continue",
                             alignHoriz = 'center',
                             alignVert = 'center')

    prompt.draw()
    window.flip()

    while True:
        keys = event.getKeys(['space'])
        if keys:
            break

def trials(win):
    """
    Wraps around all the trials
    """

    gabor = visual.GratingStim(win,
                               tex='sin',
                               mask='gauss',
                               sf= 5,
                               name='gabor',
                               size = [8,8],
                               ori = 5,
                               autoLog=False,
                               opacity = 0.5)

    disc = visual.Circle(win,
                         radius = 2.6,
                         fillColor = 'white',
                         pos = (0,0),
                         lineWidth = 0,
                         opacity = 0.1)

    N_TRIALS = 84
    CONTRAST_1 = 0.1
    CONTRAST_2 = 0.16
    CONTRAST_3 = 0.22
    CONTRAST_4 = 0.28
    CONTRAST_5 = 0.34
    CONTRAST_6 = 0.40
    CONTRAST_7 = 0.46
    RIGHT = 10
    LEFT = -10

    GABOR_INITIAL = 0.5
    gabor_transparency = GABOR_INITIAL


    #randomise trials
    all_trials = [i for i in range(N_TRIALS)]
    shuffle(all_trials)

    trial_params = {

        # Key format: (first_stimulus, gabor_visibility, disc_contrast, gabor_orientation, DYS trial)

        (gabor, disc,  False, CONTRAST_1, 0, False): all_trials[:1],
        (disc, gabor,  False, CONTRAST_1, 0, False) : all_trials[1:2],
        (gabor, disc,  False, CONTRAST_2, 0, False): all_trials[2:3],
        (disc, gabor,  False, CONTRAST_2, 0, False) : all_trials[3:4],
        (gabor, disc,  False, CONTRAST_3, 0, False): all_trials[4:5],
        (disc, gabor,  False, CONTRAST_3, 0, False) : all_trials[5:6],
        (gabor, disc,  False, CONTRAST_4, 0, False): all_trials[6:7],
        (disc, gabor,  False, CONTRAST_4, 0, False) : all_trials[7:8],
        (gabor, disc,  False, CONTRAST_5, 0, False): all_trials[8:9],
        (disc, gabor,  False, CONTRAST_5, 0, False) : all_trials[9:10],
        (gabor, disc,  False, CONTRAST_6, 0, False): all_trials[10:11],
        (disc, gabor,  False, CONTRAST_6, 0, False) : all_trials[11:12],
        (gabor, disc,  False, CONTRAST_7, 0, False): all_trials[12:13],
        (disc, gabor,  False, CONTRAST_7, 0, False) : all_trials[13:14],

        (gabor, disc,  True, CONTRAST_1, RIGHT, False): all_trials[14:16],
        (disc, gabor,  True, CONTRAST_1, RIGHT, False) : all_trials[16:18],
        (gabor, disc,  True, CONTRAST_2, RIGHT, False): all_trials[18:20],
        (disc, gabor,  True, CONTRAST_2, RIGHT, False) : all_trials[20:22],
        (gabor, disc,  True, CONTRAST_3, RIGHT, False): all_trials[22:24],
        (disc, gabor,  True, CONTRAST_3, RIGHT, False) : all_trials[24:26],
        (gabor, disc,  True, CONTRAST_4, RIGHT, False): all_trials[26:28],
        (disc, gabor,  True, CONTRAST_4, RIGHT, False) : all_trials[28:30],
        (gabor, disc,  True, CONTRAST_5, RIGHT, False): all_trials[30:32],
        (disc, gabor,  True, CONTRAST_5, RIGHT, False) : all_trials[32:34],
        (gabor, disc,  True, CONTRAST_6, RIGHT, False): all_trials[34:36],
        (disc, gabor,  True, CONTRAST_6, RIGHT, False) : all_trials[36:38],
        (gabor, disc,  True, CONTRAST_7, RIGHT, False): all_trials[38:40],
        (disc, gabor,  True, CONTRAST_7, RIGHT, False) : all_trials[40:42],

        (gabor, disc,  True, CONTRAST_1, LEFT, False): all_trials[42:44],
        (disc, gabor,  True, CONTRAST_1, LEFT, False) : all_trials[44:46],
        (gabor, disc,  True, CONTRAST_2, LEFT, False): all_trials[46:48],
        (disc, gabor,  True, CONTRAST_2, LEFT, False) : all_trials[48:50],
        (gabor, disc,  True, CONTRAST_3, LEFT, False): all_trials[50:52],
        (disc, gabor,  True, CONTRAST_3, LEFT, False) : all_trials[52:54],
        (gabor, disc,  True, CONTRAST_4, LEFT, False): all_trials[54:56],
        (disc, gabor,  True, CONTRAST_4, LEFT, False) : all_trials[56:58],
        (gabor, disc,  True, CONTRAST_5, LEFT, False): all_trials[58:60],
        (disc, gabor,  True, CONTRAST_5, LEFT, False) : all_trials[60:62],
        (gabor, disc,  True, CONTRAST_6, LEFT, False): all_trials[62:64],
        (disc, gabor,  True, CONTRAST_6, LEFT, False) : all_trials[64:66],
        (gabor, disc,  True, CONTRAST_7, LEFT, False): all_trials[66:68],
        (disc, gabor,  True, CONTRAST_7, LEFT, False) : all_trials[68:70],

        (gabor, disc,  False, CONTRAST_1, 0, True): all_trials[70:71],
        (disc, gabor,  False, CONTRAST_1, 0, True) : all_trials[71:72],
        (gabor, disc,  False, CONTRAST_2, 0, True): all_trials[72:73],
        (disc, gabor,  False, CONTRAST_2, 0, True) : all_trials[73:74],
        (gabor, disc,  False, CONTRAST_3, 0, True): all_trials[74:75],
        (disc, gabor,  False, CONTRAST_3, 0, True) : all_trials[75:76],
        (gabor, disc,  False, CONTRAST_4, 0, True): all_trials[76:77],
        (disc, gabor,  False, CONTRAST_4, 0, True) : all_trials[77:78],
        (gabor, disc,  False, CONTRAST_5, 0, True): all_trials[78:79],
        (disc, gabor,  False, CONTRAST_5, 0, True) : all_trials[79:80],
        (gabor, disc,  False, CONTRAST_6, 0, True): all_trials[80:81],
        (disc, gabor,  False, CONTRAST_6, 0, True) : all_trials[81:82],
        (gabor, disc,  False, CONTRAST_7, 0, True): all_trials[82:83],
        (disc, gabor,  False, CONTRAST_7, 0, True) : all_trials[83:]

    }

    n_correct = 0
    n_counted = 0

    last_one_correct = False

    for i in range(N_TRIALS):

        try:
            logging.warn("\n\n{} correct out of {} ({}%) in the last {} trials".format(n_correct, n_counted, (n_correct/n_counted * 100), i % 10 + 1))
        except ZeroDivisionError:
            logging.warn("\n\nNo statistics")

        if not i % 10 and i > 0:
            show_feedback(win, (n_correct/n_counted) * 100)
            n_correct = 0
            n_counted = 0

        for trial_param in trial_params.keys():
            if i in trial_params[trial_param]:

                trial_message = generate_log(trial_param)
                logging.warn("TRIAL {}: {}".format(i + 1, trial_message))
                logging.flush()

                first_stim = trial_param[0]
                second_stim = trial_param[1]
                gabor_visible = trial_param[2]

                if gabor_visible:
                    gabor.opacity = gabor_transparency
                else:
                    gabor.opacity = 0

                disc.opacity = trial_param[3]

                gabor.ori = trial_param[4]

                dys = trial_param[5]

                trial_response = trial(win, first_stim, second_stim, dys)
                confident_trial = trial_response[0]
                confident_response = trial_response[confident_trial + 1]

                # Now we check the results of the trial and log/change variables
                if trial_param[confident_trial] == gabor and gabor_visible:
                    # a trial that is counted towards the accuracy calculation
                    n_counted += 1
                    logging.warn("Counted trial")

                    if confident_response == gabor.ori
                        #subject got it right
                        logging.warn("Correct trial")
                        n_correct += 1

                        if last_one_correct:
                            # ensuring floating only happens after two correct trials
                            logging.warn("Two correct trials. Decreasing gabor transparency")
                            logging.flush()
                            gabor_transparency -= 0.02
                            if gabor_transparency < 0.02:
                                gabor_transparency = 0.02
                                logging.warn("MINIMUM CONTRAST FOR GABOR REACHED")
                                logging.flush()
                        last_one_correct = not last_one_correct

                    else:
                        # incorrect trial. Increase gabor transparency
                        logging.warn("Incorrect trial. Increasing gabor transparency")
                        logging.flush()
                        gabor_transparency += 0.02
                        if gabor_transparency > 1:
                            gabor_transparency = 1
                            logging.warn("MAXIMUM CONTRAST FOR GABOR REACHED")
                            logging.flush()
                        last_one_correct = False


                break
        press_to_continue(win)

#TODO: File saving

def main(trial):

    window = trial.window
    subject_number = trial.subject_number
    round_Number = trial.round_number

    trials(window)

if __name__ == '__main__':
    main()
