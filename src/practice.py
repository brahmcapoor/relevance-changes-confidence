from __future__ import division
import csv
import os
import random
from psychopy import visual, logging
from testing import stimulus_and_mask, trial, press_to_continue, show_feedback


def generate_log_file(subject_number, round_number):
    filename = ""

    if "src" in os.getcwd():
        filename = "../subject_logs/subject_{}_round_{}_practice.csv" \
            .format(subject_number, round_number)
    else:
        filename = "subject_logs/subject_{}_round_{}_practice.csv" \
            .format(subject_number, round_number)

    with open(filename, 'wb') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)

        header = ["", "",
                  "Trial parameter", "", "", "", "", "", "",
                  "Subject response"]

        subheader_1 = ["", "",
                       "Condition 2", "", "", "",
                       "Condition 3", "", "",
                       "Condition 2", "", "",
                       "Condition 3"]

        subheader_2 = ["Trial Number", "Condition",

                       "First Gabor Tilt", "Second Gabor Tilt",
                       "First Gabor Contrast", "Second Gabor Contrast",

                       "Stimulus Position",
                       "Stimulus (0= disc, 1/2 = gabor left/right)",
                       "Contrast",

                       "Tilt 1", "Tilt 2",
                                           "Confident trial",

                       "Stimulus 1 seen", "Stimulus 2 seen",
                       "Gabor or Disc?(0 = gabor, 1 = disc, 2=unseen)"]

        wr.writerow(header)
        wr.writerow(subheader_1)
        wr.writerow(subheader_2)

    return filename


def practice_condition_2(window, filename):
    N_PRACTICE_TRIALS = 20

    TILT_ANGLE = 10

    gabors_first = [visual.GratingStim(window,
                                       tex='sin',
                                       mask='gauss',
                                       sf=5,
                                       name='gabor',
                                       size=[8, 8],
                                       ori=TILT_ANGLE * i,
                                       autoLog=False,
                                       opacity=0.5)
                    for i in [-1, 1]]

    gabors_second = [visual.GratingStim(window,
                                        tex='sin',
                                        mask='gauss',
                                        sf=5,
                                        name='gabor',
                                        size=[8, 8],
                                        ori=TILT_ANGLE * i,
                                        autoLog=False,
                                        opacity=0.5)
                     for i in [-1, 1]]

    first_stimuli = {
        TILT_ANGLE * -1: gabors_first[0],
        TILT_ANGLE: gabors_first[1]
    }

    second_stimuli = {
        TILT_ANGLE * -1: gabors_second[0],
        TILT_ANGLE: gabors_second[1]
    }

    questions = ["Left or Right?",
                 "Which one were you more confident about?"]

    n_correct = 0

    for i in range(1, N_PRACTICE_TRIALS + 1):
        logging.warn("TRIAL {}".format(i))

        row_record = [i, 2]
        press_to_continue(window, "Press space to continue")

        first_gabor_tilt = random.choice([-1, 1])*TILT_ANGLE
        row_record.append(first_gabor_tilt)
        logging.warn("First gabor is tilted {}".format("right"
                                                       if first_gabor_tilt > 0
                                                       else "left"))
        logging.flush()
        first_gabor = first_stimuli[first_gabor_tilt]
        first_gabor.opacity = random.choice([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
                                            )
        logging.warn("First gabor opacity is {}".format(first_gabor.opacity))
        logging.flush()

        second_gabor_tilt = random.choice([-1, 1])*TILT_ANGLE
        row_record.append(second_gabor_tilt)
        logging.warn("Second gabor is tilted {}".format("right"
                                                        if
                                                        second_gabor_tilt > 0
                                                        else "left"))
        logging.flush()
        second_gabor = second_stimuli[second_gabor_tilt]
        second_gabor.opacity = random.choice([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7
                                              ])
        logging.warn("Second gabor opacity is {}".format(second_gabor.opacity))
        logging.flush()

        row_record += [first_gabor.opacity, second_gabor.opacity, "", "", ""]
        stimulus_param = [first_gabor, second_gabor]

        response = trial(window, *(stimulus_param+questions))

        if response[response[2]] * TILT_ANGLE == \
                stimulus_param[response[2]].ori:
            logging.warn("Correct trial")
            logging.flush()
            n_correct += 1

        row_record += [response[0]*TILT_ANGLE,
                       response[1]*TILT_ANGLE,
                       response[2] + 1]

        with open(filename, 'ab') as f:
            wr = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)

            wr.writerow(row_record)

        logging.warn("\n\n\n")
        logging.flush()

        if not i % 10:
            show_feedback(window, n_correct/10 * 100)
            n_correct = 0


def practice_condition_3(window, filename, discs):
    N_PRACTICE_TRIALS = 20

    TILT_ANGLE = 10

    blank = discs[0]

    discs = discs[1:]

    gabor_right = visual.GratingStim(window,
                                     tex='sin',
                                     mask='gauss',
                                     sf=5,
                                     name='gabor',
                                     size=[8, 8],
                                     ori=TILT_ANGLE,
                                     autoLog=False,
                                     opacity=0.5)

    gabor_left = visual.GratingStim(window,
                                    tex='sin',
                                    mask='gauss',
                                    sf=5,
                                    name='gabor',
                                    size=[8, 8],
                                    ori=TILT_ANGLE * -1,
                                    autoLog=False,
                                    opacity=0.5)

    questions = ["Did you see something? (Press Left for No, Right for Yes)",
                 "Gabor or disc? (1 for Gabor, 2 for Disc)"]

    stimulus_param = [None, None]
    for i in range(1, N_PRACTICE_TRIALS + 1):
        record_row = [20 + i, 3, "", "", "", ""]

        logging.warn("TRIAL {}".format(20 + i))

        stim_position = random.randint(0, 1)
        record_row.append(stim_position + 1)
        stimulus_param[1 - stim_position] = blank

        stim_type = random.randint(0, 2)
        record_row.append(stim_type)

        if stim_type == 0:
            stimulus_param[stim_position] = random.choice(discs)
        elif stim_type == 1:
            stimulus_param[stim_position] = gabor_left
        elif stim_type == 2:
            stimulus_param[stim_position] = gabor_right

        response = trial(window, *(stimulus_param+questions), block3=True)

        record_row += [stimulus_param[stim_position].opacity, "", "", ""]

        record_row += [(response[0]+1)/2,
                       (response[1]+1)/2,
                       response[2]]

        with open(filename, 'ab') as f:
            wr = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)

            wr.writerow(record_row)

        logging.warn("\n\n\n")
        logging.flush()

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

    practice_condition_2(window, filename)
    press_to_continue(window, "End of section")
    practice_condition_3(window, filename, discs)


if __name__ == '__main__':
    main()
