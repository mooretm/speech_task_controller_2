""" Model for loading and subsetting audio and sentence files.

    Written by: Travis M. Moore
"""

###########
# Imports #
###########
# Import GUI packages
from tkinter import messagebox

# Import data science packages
import numpy as np
import pandas as pd

# Import system packages
import os
from glob import glob


#########
# BEGIN #
#########
class StimulusList:
    """ Load audio files and written sentences into dataframes.
        Subset dataframes based on provided list numbers.

        Returns:
            self.audio_df: data frame of audio paths/names
            self.sentence_df: data frame of sentences, indexes
    """

    def __init__(self, sessionpars):
        # Initialize
        self.sessionpars = sessionpars


    def load(self):
        """ Controller to call task functions 
            in the proper order.
        """
        # Retrieve specified list number(s)
        self._get_list_and_level_vals()

        try:
            # Load and subset sentences
            # Must occur before audio call
            self._get_sentences()
            # Load and subset audio files based on sentence df length
            self._get_audio_files()
            # Create list of presentation levels based on sentence 
            #   df length and sentences_per_list
            self._get_levels()
            # Create master df of sentences, audio and levels
            self._make_master_df()
        except FileNotFoundError:
            print("Models_Listmodel_52: Cannot find stimuli!")


    def _get_list_and_level_vals(self):
        """ Get list and level values, convert to lists
        """
        self.lists = self.sessionpars['List Number'].get().split()
        self.lists = [int(val) for val in self.lists]

        self.levels = self.sessionpars['Presentation Level'].get().split()
        self.levels = [float(val) for val in self.levels]


    #############
    # Sentences #
    #############
    def _get_sentences(self):
        """ Open sentences file and load contents into dataframe. 
            Subset by specified list number(s) from session info.
        """
        # Check whether sentence directory exists
        print("\nModels_listmodel_66: Checking for sentences dir...")
        if not os.path.exists(self.sessionpars['Sentence File Path'].get()):
            print("Models_listmodel_68: Not a valid 'sentences' file directory!")
            raise FileNotFoundError

        # If a valid directory has been given, 
        # get a list of sentence files
        glob_pattern = os.path.join(self.sessionpars['Sentence File Path'].get(), '*.csv')
        sentence_file = glob(glob_pattern)
        # Check to make sure there's only one file in the directory
        if len(sentence_file) > 1:
            messagebox.showwarning(
                title="Too Many Files!",
                message="Multiple sentence files found - grabbing one at random."
            )
        # Read sentence file into dataframe
        s = pd.read_csv(sentence_file[0])
        s = s.groupby('list_num').head(self.sessionpars['sentences_per_list'].get()).reset_index(drop=True)

        # Get sentences for specified list numbers
        self.sentence_df = s.loc[s['list_num'].isin(self.lists)].reset_index()
        #print(self.sentence_df)
        print("Models_listmodel_91: Sentence list dataframe loaded into listmodel")


    ###############
    # Audio Files #
    ###############
    def _get_audio_files(self):
        """ Load in files as full paths. Select files based 
            on sentences data frame.
        """
        # Check whether audio directory exists
        print("\nModels_listmodel_102: Checking for audio files dir...")
        if not os.path.exists(self.sessionpars['Audio Files Path'].get()):
            print("Models_listmodel_104: Not a valid audio files directory!")
            messagebox.showerror(
                title='Directory Not Found!',
                message="Cannot find the audio file directory!\n" +
                "Please choose another file path."
            )

        # If a valid directory has been given, 
        # get the audio file paths and names
        glob_pattern = os.path.join(self.sessionpars['Audio Files Path'].get(), '*.wav')
        # Create audio paths dataframe
        self.audio_df = pd.DataFrame(glob(glob_pattern), columns=['path'])
        # Create new column based on file names (which are numbered)
        self.audio_df['file_num'] = self.audio_df['path'].apply(lambda x: x.split(os.sep)[-1][:-4])
        # Convert to integers
        self.audio_df['file_num'] = self.audio_df['file_num'].astype(int)
        # Sort ascending by new column of integers
        self.audio_df = self.audio_df.sort_values(by=['file_num'])

        # Subset based on sentence dataframe values
        self.audio_df = self.audio_df.loc[self.audio_df['file_num'].isin(self.sentence_df['sentence_num'])]
        #print(self.audio_df)
        print("Models_listmodel_126: Audio list dataframe loaded into listmodel")


    ##########
    # Levels #
    ##########
    def _get_levels(self):
        if len(self.levels) == 1:
            self.all_levels = np.repeat(self.levels, self.sentence_df.shape[0])
        else:
            # create enough levels for each list
            self.all_levels = np.repeat(self.levels, self.sessionpars['sentences_per_list'].get())
        #print(f"\nPresentation levels: {self.all_levels}")
        print("\nModels_listmodel: Created list of presentation levels")


    ####################
    # Create Master DF #
    ####################
    def _make_master_df(self):
        self.stim_master = self.sentence_df.copy()
        self.stim_master.drop('index', axis=1, inplace=True)
        self.stim_master['audio'] = list(self.audio_df['path'])
        self.stim_master['level'] = self.all_levels
        
        # Reorder df column order
        self.stim_master = self.stim_master[list((
            'list_num', 'sentence_num', 'level', 'sentence', 'audio'
        ))]

        # Convert str to float
        self.stim_master.level.astype(float)
        print("\nModels_listmodel: Created master stimulus dataframe")
        print(self.stim_master)


