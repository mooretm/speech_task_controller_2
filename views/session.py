""" Session parameters dialog
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tktooltip import ToolTip


#########
# BEGIN #
#########
class SessionDialog(tk.Toplevel):
    """ Dialog for setting session parameters
    """
    def __init__(self, parent, sessionpars, sessionmodel, listmodel, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.sessionpars = sessionpars
        self.sessionmodel = sessionmodel
        self.listmodel = listmodel

        # Window setup
        self.withdraw()
        self.title("Session")
        self.grab_set()

        # Shared display settings
        options = {'padx':5, 'pady':5}

        #################
        # Create frames #
        #################
        # Session info frame
        frm_session = ttk.Labelframe(self, text='Session Information')
        frm_session.grid(column=0, row=5, padx=10, pady=10, sticky='nsew')

        # Session options frame
        frm_options = ttk.Labelframe(self, text='Options')
        frm_options.grid(column=0, row=6, padx=10, pady=10, stick='nsew')

        # Audio file browser frame
        frm_audiopath = ttk.Labelframe(self, text="Audio File Directory")
        frm_audiopath.grid(column=0, row=10, padx=10, pady=10, ipadx=5, ipady=5)

        # Sentence file browser frame
        frm_sentencepath = ttk.Labelframe(self, text='Sentence File Directory')
        frm_sentencepath.grid(column=0, row=15, padx=10, pady=10, ipadx=5, ipady=5)


        #######################
        # Create view widgets #
        #######################
        # Subject
        lbl_sub = ttk.Label(frm_session, text="Subject:")
        lbl_sub.grid(row=2, column=0, sticky='e', **options)
        ttk.Entry(frm_session, width=20, 
            textvariable=self.sessionpars['Subject']
            ).grid(row=2, column=1, sticky='w')
        
        # Condition
        lbl_cond = ttk.Label(frm_session, text="Condition:")
        lbl_cond.grid(row=3, column=0, sticky='e', **options)
        ttk.Entry(frm_session, width=20, 
            textvariable=self.sessionpars['Condition']
            ).grid(row=3, column=1, sticky='w')

        # List
        lbl_list = ttk.Label(frm_session, text="List(s):")
        lbl_list.grid(row=4, column=0, sticky='e', **options)
        ttk.Entry(frm_session, width=20, 
            textvariable=self.sessionpars['List Number']
            ).grid(row=4, column=1, sticky='w')

        # Level
        lbl_level = ttk.Label(frm_session, text="Level(s) (dB):")
        lbl_level.grid(row=5, column=0, sticky='e', **options)
        ttk.Entry(frm_session, width=20, 
            textvariable=self.sessionpars['Presentation Level']
            ).grid(row=5, column=1, sticky='w')

        # Sentences per list
        lbl_ppl = ttk.Label(frm_session, text="# Sentences:")
        lbl_ppl.grid(row=6, column=0, sticky='e', **options)
        ttk.Entry(frm_session, width=20, 
            textvariable=self.sessionpars['sentences_per_list']
            ).grid(row=6, column=1, sticky='w')

        # Randomize
        #self.random_var = tk.IntVar(value=self.sessionpars['randomize'])
        chk_random = ttk.Checkbutton(frm_options, text="Randomize",
            takefocus=0, variable=self.sessionpars['randomize'])
        chk_random.grid(row=7, column=0, sticky='e', **options)

        # Audio directory
        ttk.Label(frm_audiopath, text="Path:"
            ).grid(row=6, column=0, sticky='e', **options)
        ttk.Label(frm_audiopath, textvariable=self.sessionpars['Audio Files Path'], 
            borderwidth=2, relief="solid", width=60
            ).grid(row=6, column=1, sticky='w')
        ttk.Button(frm_audiopath, text="Browse", command=self._get_audio_directory
            ).grid(row=7, column=1, sticky='w', pady=(0, 10))

        # Sentence directory
        ttk.Label(frm_sentencepath, text="Path:"
            ).grid(row=9, column=0, sticky='e', **options)
        ttk.Label(frm_sentencepath, textvariable=self.sessionpars['Sentence File Path'], 
            borderwidth=2, relief="solid", width=60
            ).grid(row=9, column=1, sticky='w')
        ttk.Button(frm_sentencepath, text="Browse", command=self._get_sentence_directory
            ).grid(row=10, column=1, sticky='w', pady=(0, 5))

        # Submit button
        btn_submit = ttk.Button(self, text="Submit", command=self._on_submit)
        btn_submit.grid(column=0, columnspan=2, row=20, pady=(0,10))

        # Tool tips
        ToolTip(
            lbl_sub,
            msg="Subject ID. Can be letters, numbers or both.",
            delay=0.5
        )

        ToolTip(
            lbl_cond,
            msg="Separate multiple conditions with underscores (_). \nExample: aided_quiet",
            delay=0.5
        )

        ToolTip(
            lbl_list,
            msg="Enter each list number separated by a space.",
            delay=0.5
        )

        ToolTip(
            lbl_level,
            msg="Enter each level separated by a space.",
            delay=0.5
        )

        ToolTip(
            lbl_ppl, 
            msg="Number of sentences to present for each list.",
            delay=0.5
        )

        ToolTip(
            chk_random, 
            msg="Randomize the presentation of sentences across lists.\nLevels remain consistent for each list.",
            delay=0.5
        )

        # Center the session dialog window
        self.center_window()


    #############
    # Functions #
    #############
    def center_window(self):
        """ Center the root window 
        """
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        size = tuple(int(_) for _ in self.geometry().split('+')[0].split('x'))
        x = screen_width/2 - size[0]/2
        y = screen_height/2 - size[1]/2
        self.geometry("+%d+%d" % (x, y))
        self.deiconify()


    def _get_audio_directory(self):
        """ Ask user to specify audio files directory and 
            store it in sessionpars
        """
        self.sessionpars['Audio Files Path'].set(
            filedialog.askdirectory(title="Audio File Directory"))


    def _get_sentence_directory(self):
        """ Ask user to specify sentence file and store
            it in sessionpars
        """
        self.sessionpars['Sentence File Path'].set(
            filedialog.askdirectory(title="Sentence File Directory"))


    def _chk_lengths(self):
        """ Validate the number of entered lists and presentations levels.
            If an invalid number exists, display an error message and return 
            invalid flag.
        """
        lists = self.sessionpars['List Number'].get().split()
        lists = [int(val) for val in lists]

        levels = self.sessionpars['Presentation Level'].get().split()
        levels = [float(val) for val in levels]

        if (len(levels) != len(lists)) and (len(levels) != 1):
            messagebox.showerror(
                title="Invalid Parameters",
                message="Invalid number of levels!",
                detail="Either provide a single level, or an equal number of levels and lists."
            )
            return 'invalid'
        else:
            return 'valid'


    def _on_submit(self):
        """ Set new_db_lvl to specified presentation level.
            Send event to controller to write sessionpars data to file
        """
        # No longer need to set new_db_lvl here because it will be pulled 
        # from the list of levels from the listmodel
        #self.sessionpars['new_db_lvl'].set(self.sessionpars['Presentation Level'].get())

        # Load listmodel
        print("\nViews_Session: Attempting to load listmodel stimuli")
        self.listmodel.load()
        print("Success!")

        # Validate number of provided lists/levels
        list_lvl_num_chk = self._chk_lengths()
        if list_lvl_num_chk == 'invalid':
            return

        print("\nViews_Session_140: Sending save event to controller...")
        self.parent.event_generate('<<SessionSubmit>>')
        self.destroy()
