""" Main view for presentation controller.

    Written by: Travis M. Moore
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Import data science packages
import numpy as np
import random

# Import text packages
import string # for creating alphabet list

# Import custom modules
from models import audiomodel as a


#########
# BEGIN #
#########
class MainFrame(ttk.Frame):
    def __init__(self, parent, scoremodel, sessionpars, listmodel, 
    *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Initialize
        self.scoremodel = scoremodel
        self.sessionpars = sessionpars
        self.listmodel = listmodel
        self.counter = 0

        # Set widget display options
        self.myFont = tk.font.nametofont('TkDefaultFont').configure(size=10)
        options = {'padx':10, 'pady':10}

        style = ttk.Style()
        style.configure('Start.TButton', 
            font=('TkDefaultFont', 10, 'bold'), 
            foreground='green',
            background='black')

        style.configure('Repeat.TButton', 
            font=('TkDefaultFont', 10, 'bold'), 
            foreground='black',
            background='black')


        #################
        # Create frames #
        #################
        # Main content frame
        frm_main = ttk.Frame(self)
        frm_main.grid(column=5, row=5, sticky='nsew')

        # Words and checkbuttons frame
        self.frm_sentence = ttk.LabelFrame(frm_main, text='Sentence:', 
            padding=8, width=500, height=80)
        self.frm_sentence.grid(column=5, columnspan=15, row=5, sticky='nsew', 
            **options)
        self.frm_sentence.grid_propagate(0)

        # Vertical separator for session info
        sep = ttk.Separator(frm_main, orient='vertical')
        sep.grid(column=20, row=5, rowspan=50, sticky='ns')

        # Session info frame
        self.frm_params = ttk.LabelFrame(frm_main, text="Session Info")
        self.frm_params.grid(column=25, row=5, rowspan=15, sticky='n',
            **options, ipadx=5, ipady=5)


        #######################
        # Session info labels #
        #######################
        # Create session info label textvariables for updating
        self.subject_var = tk.StringVar(value="Subject:")
        self.condition_var = tk.StringVar(value="Condition:")
        self.level_var = tk.StringVar(value="Level:")
        self.list_var = tk.StringVar(value="List:")
        self.speaker_var = tk.StringVar(value="Speaker:")
        self.trial_var = tk.StringVar(value="Trial:")

        # Plot session info labels
        # Subject
        ttk.Label(self.frm_params, 
            textvariable=self.subject_var).grid(sticky='w')
        # Condition
        ttk.Label(self.frm_params, 
            textvariable=self.condition_var).grid(sticky='w')
        # Speaker number
        ttk.Label(self.frm_params, 
           textvariable=self.speaker_var).grid(sticky='w')
         # List number(s)  
        ttk.Label(self.frm_params, 
            textvariable=self.list_var).grid(sticky='w')
        # Level
        ttk.Label(self.frm_params, 
           textvariable=self.level_var).grid(sticky='w')
        # Trial number
        ttk.Label(self.frm_params, 
            textvariable=self.trial_var).grid(sticky='w')


        #################
        # User controls #
        #################
        # "Start" button
        self.btn_start = ttk.Button(frm_main, text='Start',
            command=self._on_start, style='Start.TButton')
        self.btn_start.grid(column=6, row=15, #rowspan=6, 
            sticky='nsew', pady=(0,10))

        # "Repeat" button
        self.btn_repeat = ttk.Button(frm_main, text='Repeat',
            command=self._on_repeat, style='Repeat.TButton',
            takefocus=0)
        # NOTE: Only place widget when START is clicked

        # "Select All" button
        self.btn_select_all = ttk.Button(frm_main, text="Select All", 
            state='disabled', command=self._on_select_all, takefocus=0)
        self.btn_select_all.grid(column=5, row=8, pady=(0,10))

        # "Next" button
        self.btn_next = ttk.Button(frm_main, text='Next', state='disabled', 
            command=self._on_next)
        self.btn_next.grid(column=5, row=15, pady=(0,10))


        ##########################
        # Words and checkbuttons #
        ##########################
        # Create list of labels for displaying words
        self.text_vars = list(string.ascii_lowercase)
        self.word_labels = []
        for idx, letter in enumerate(self.text_vars):
            self.text_vars[idx] = tk.StringVar(value='')
            self.lbl_word = ttk.Label(self.frm_sentence, 
                textvariable=self.text_vars[idx], font=self.myFont)
            self.lbl_word.grid(column=idx, row=0)
            self.word_labels.append(self.lbl_word)

        # Set temporary instructions text in the first word label
        self.text_vars[0].set("Click the START button to begin.")

        # Create list of checkbuttons for displaying beneath key words
        self.chk_vars = list(string.ascii_uppercase)
        self.word_chks = []
        for idx in range(0, len(self.text_vars)):
            self.chk_vars[idx] = tk.IntVar(value=0)
            self.chk_word = ttk.Checkbutton(self.frm_sentence, 
                text='', takefocus=0, variable=self.chk_vars[idx])
            self.word_chks.append(self.chk_word)


    #####################
    # General functions #
    #####################
    def _get_stimuli(self):
        """ Load in current stimulus lists from listmodel
        """
        try:
            self.listmodel.load()
            self.stim_master = self.listmodel.stim_master
        except AttributeError:
            print("Views_Main_178: Problem loading stimuli!")
            self._reset()
            self.text_vars[0].set("Stimuli not found!\nGo to File-->Session to provide stimulus paths.")
            # Open session dialog for user
            self.event_generate('<<FileSession>>')


    def _update_labels(self, *_):
        """ Update session info labels
        """
        # NOTE: This func is called from the controller
        try:
            self.subject_var.set(f"Subject: {self.sessionpars['Subject'].get()}")
            self.condition_var.set(f"Condition: {self.sessionpars['Condition'].get()}")
            self.speaker_var.set(f"Speaker: {self.sessionpars['Speaker Number'].get()}")
            self.list_var.set(f"List(s): {self.sessionpars['List Number'].get()}")
            self.level_var.set(f"Level: {self.stim_master.loc[self.counter, 'level']}")
            self.trial_var.set(f"Trial: {self.counter+1} of {len(self.stim_master)}")
        except AttributeError:
            print("Views_Main_189: Cannot calculate trials data: stimuli not yet loaded!")


    def _get_level(self):
        """ Send event to controller to calculate new 
            raw level for the updated presentation level.
        """
        # Load level based on stim_master list
        self.sessionpars['new_db_lvl'].set(self.stim_master.loc[self.counter, 'level'])
        self._update_labels()

        # Send event to controller
        self.event_generate('<<GetLevel>>')


    def _enable_btns(self):
        """ Enable NEXT button.
            Set NEXT button text to "Next."
        """
        self.btn_next.config(state='enabled')
        self.btn_next.config(text="Next")


    def _disable_btns(self, btntext):
        """ Disable NEXT button.
            Set NEXT button text to: "Presenting"
        """
        self.btn_next.config(state='disabled')
        self.btn_next.config(text=btntext)


    def _reset(self):
        """ Reset all word labels and checkbuttons to default 
            values for next trial
        """
        # Reset word label text
        for val in self.text_vars:
            val.set('')
        # Reset word label font
        for lbl in self.word_labels:
            lbl.config(font=('TkDefaultFont 10'))
        # Hide checkbuttons
        for chk in self.word_chks:
            chk.grid_remove()
        # Reset checkbutton values to 0
        for val in self.chk_vars:
            val.set(0)


    ####################
    # Button functions #
    ####################
    def _on_start(self):
        """ Handle buttons, apply randomization, get first 
            sentence, audio file and level, display/present
        """
        # Send event to controller to disable session menu
        # once task has started
        self.event_generate('<<MainStart>>')

        # Clean up buttons
        self.btn_start.grid_remove()
        self.btn_select_all.config(state='enabled')
        self.btn_next.config(state='enabled')
        # Show REPEAT button
        self.btn_repeat.grid(column=7, row=15,
        sticky='nsew', pady=(0,10))

        # Call listmodel load func to get latest lists
        self._get_stimuli()

        # Apply randomization if selected in session dialog
        if self.sessionpars['randomize'].get() == 1:
            print('\nViews_Main: Randomize = True')
            print('(Audio paths not printed below to save space)')
            trials = list(self.stim_master.index)
            random.shuffle(trials)
            self.stim_master['order'] = trials
            self.stim_master.sort_values(by='order', inplace=True)
            self.stim_master.set_index('order', inplace=True)
            print(self.stim_master.drop('audio', axis=1))
        else:
            print('\nViews_Main: Randomize = False')

        # Get presentation level
        self._get_level()

        # Update session info labels after loading listmodel
        # and getting presentation level
        self._update_labels()

        # Display first sentence and present first audio file
        self._display()
        self._play()


    def _on_next(self):
        """ Control the order of operations when NEXT 
            button is clicked
        """
        # Score responses
        self._score()
        # Reset word labels and checkbuttons
        self._reset()
        
        if self.counter >= len(self.stim_master)-1:
            print("Out of sentences!")
            self.text_vars[0].set("Done!")
            self.trial_var.set(f"Trial {len(self.stim_master)} of " +
                f"{len(self.stim_master)}")
            self.btn_next.config(state='disabled')
            #self.btn_wrong.config(state='disabled')
            self.event_generate('<<MainDone>>')
            return

        # Update trial counter call before _get_level
        # and _update_labels funcs
        self.counter += 1
        
        # Get next level and calculate dB FS
        self._get_level()

        # Update session info labels
        self._update_labels()

        # Start next trial: display sentence and present audio
        self._display()
        self._play()


    def _on_select_all(self):
        """ Select all checkboxes convenience function
        """
        print("Views_Main_281: Selected all checkboxes")

        for ii in self.keyword_chks:
            self.chk_vars[ii].set(1)


    def _on_repeat(self):
        """ Repeat the current sentence without scoring or 
            advancing the sentence counter
        """
        print("Views_Main_276: Repeat current sentence")
        self._play()


    ###################
    # Play audio file #
    ###################
    def _play(self):
        """ Load next audio file and present it
        """
        try:
            # Create audio object
            print(f"Views_Main_363: Raw level sent to audio object: " +
                f"{self.sessionpars['new_raw_lvl'].get()}")
            audio = a.Audio(self.stim_master.loc[self.counter, 'audio'],
                self.sessionpars['new_raw_lvl'].get())

            # Disable right/wrong buttons to prevent multiple clicks
            self._disable_btns("Presenting")
            # Update tasks is required before playing audio
            # for _disable_btns to update the GUI
            self.update()

            # Present audio
            try:
                audio.play(
                    device_id=self.sessionpars['Audio Device ID'].get(),
                    channels=self.sessionpars['Speaker Number'].get()
                    )
            except ValueError:
                # Show error messagebox
                messagebox.showerror(title="Invalid Audio Device",
                    message="Please provide a valid audio device ID!")
                # Give instructions in sentence label
                self._reset()
                self.text_vars[0].set("Please restart the application " +
                    "to apply changes.")
                # Open audio device dialog for user
                self.event_generate('<<ToolsAudioSettings>>')
                # Disable right/wrong buttons
                self._disable_btns("Ready")
                # Restore START button
                self.btn_start.grid(column=7, row=15, rowspan=6, 
                    sticky='nsew', pady=(0,10))
                return

            # Re-enable buttons after audio has finished playing
            # NOTE: .after expects an integer duration in ms
            self.after((int(np.ceil(audio.dur)))*1000, self._enable_btns)
        except KeyError:
            messagebox.showerror(title="Cannot Find File",
                message="Requested audio file does not exist!")
            print("Views_Main_354: Audio file does not exist!")
            return


    ##################################
    # Display words and checkbuttons #
    ##################################
    def _display(self):
        """ Display each word. Display checkbutton beneath 
            each key word (capitalized). Underline each 
            key word.
        """
        # Track indexes of key word checkboxes for 
        # SELECT ALL button
        self.keyword_chks = []
        try:
            # Get next sentence and split into a list of words
            self.words = self.stim_master.loc[
                self.counter, 'sentence'].split()
            # Remove period from last word
            if self.words[-1][-1] == '.':
                self.words[-1] = self.words[-1][:-1]

            # Display words and checkboxes
            for idx, word in enumerate(self.words):
                if word.isupper() and word != 'A':
                    # Words
                    self.text_vars[idx].set(word)
                    self.word_labels[idx].config(
                        font=('TkDefaultFont 10 underline'))
                    # Checkboxes
                    self.word_chks[idx].grid(column=idx, row=1)
                    self.keyword_chks.append(idx)
                else:
                    # Words
                    self.text_vars[idx].set(word)
        except KeyError:
            print("Out of sentences!")
            self.text_vars[0].set("Done!")
            self.trial_var.set(f"Trial {len(self.stim_master)} of " +
                f"{len(self.stim_master)}")
            self.btn_next.config(state='disabled')
            #self.btn_wrong.config(state='disabled')
            self.event_generate('<<MainDone>>')
            return


    ################################
    # Store correct response words #
    ################################
    def _score(self):
        """ Get words marked correct and incorrect, update 
            scoremodel, and send event to controller
        """
        # Get correct words
        correct = []
        for idx, value in enumerate(self.chk_vars):
            if value.get() != 0:
                correct.append(self.words[idx])

        # Get incorrect words
        # Exclude correct words from list of words
        incorrect = list(set(self.words).difference(correct))
        # Only take capitalized words
        incorrect = [word for word in incorrect if word.isupper()]
        # Remove 'A' if it exists (never a key word, but can be capital)
        try:
            incorrect.remove('A')
        except ValueError:
            # There was no 'A' in the list
            pass

        if len(correct) >= self.sessionpars['score_criterion'].get():
            outcome = 1
        else:
            outcome = 0

        # Update scoremodel with values
        self.scoremodel.fields['Words Correct'] = ' '.join(correct)
        self.scoremodel.fields['Num Words Correct'] = len(
            self.scoremodel.fields['Words Correct'].split())
        self.scoremodel.fields['Words Incorrect'] = ' '.join(incorrect)
        self.scoremodel.fields['Trial'] = self.counter + 1
        self.scoremodel.fields['Outcome'] = outcome

        # Send event to controller to write response to file
        self.event_generate('<<SubmitResponse>>')
