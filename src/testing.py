from psychopy import visual, core, event

def stimulus_and_mask(win, stimulus, mask_1, mask_2, prompt):
    """
    Shows a single stimulus begind a mask. Params are
    self explanatory
    """
    N_MASK_SECONDS = 0.5
    N_STIM_SECONDS = 0.1

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

    event.waitKeys()

    win.flip()

def trial(win, stim_1, stim_2, calibrator=False):
    """
    Performs a single Trial

    stim_1 = stimulus shown first
    stim_2 = stimulus shown second
    calibrator = if True, question is "Did you see something?"
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

    stimulus_and_mask(win, stim_1, mask_1, mask_2, prompt)
    stimulus_and_mask(win, stim_2, mask_1, mask_2, prompt)

def main():

    win = visual.Window([1680,1050],
                          monitor = "testMonitor",
                          units = "cm",
                          rgb=(-1,-1,-1),
                          fullscr = True)

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

    trial(win, gabor, disc)

if __name__ == '__main__':
    main()
