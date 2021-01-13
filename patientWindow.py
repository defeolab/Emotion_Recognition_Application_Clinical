import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import expClinical
import sys, os
import json


class PatientWindow :

    def __init__(self, parent, id, name=None, surname=None):
        self.name = name
        self.surname = surname
        self.patientId = id
        #self.environment = environment          #0 = clinical, 1 = neuromarketing
        self.parent = parent
        self.widgets = self.addWidgets()

    def browseFiles(self):
        filename = filedialog.askopenfile(initialdir= os.getcwd() +"/data/"+ str(self.patientId),
                                              title="Select a File",
                                              filetypes=(("csv files",
                                                          "*.csv"),
                                                         ("all files",
                                                          "*.*")))

        if filename is not None :

            comand = "start " + filename.name
            try :
                os.system(comand)
            except:
                print(comand)


    def addWidgets(self):
        widgets = []

        self.parent.columnconfigure(1, weight = 2)

        experiments_frame = ttk.LabelFrame(self.parent)
        experiments_frame.columnconfigure(1, weight =1)

        experiments_frame.grid(row=1, column=1, rowspan = 2, pady=3, padx=100 , sticky=tk.E + tk.W + tk.N + tk.S)
        ttk.Label(experiments_frame, text="Participant n " + self.patientId, font='Times 18').grid(row =0, column=1)

        angraphic = ttk.Button(self.parent, text="Show Anagraphic", command= self.show_anagraphic)
        angraphic.grid(row=1, column= 2)

        widgets.append(experiments_frame)

        clinical_frame = ttk.LabelFrame(experiments_frame, text="Experiment", relief=tk.RIDGE)
        clinical_frame.grid(row=1, column=1, sticky=tk.E + tk.W + tk.N + tk.S, padx=30, pady=15)

        button3 = ttk.Button(clinical_frame, text="Clinical Experiment", command=self.run_expClinical)
        clinical_frame.columnconfigure(1, weight=1)
        button3.grid(row=1, column=1, pady=10)

        show_data_but = ttk.Button(experiments_frame, text="Show Previous Data", command=self.browseFiles)
        show_data_but.grid(row=2, column=1, pady=30)

        widgets.extend([clinical_frame, button3, show_data_but])

        return widgets

    def run_expClinical(self):
        try:
            if self.patientId is None:
                self.patientId = '';
            #os.system('expClinical.py')
            expClinical.runExp(self.patientId)

        except:
            print("exit with " + str(sys.exc_info()[0]))


    def show_anagraphic(self):
        top = tk.Toplevel()
        top.title("Anagraphic data")
        top.geometry("500x500")

        fp = open('anagraphicData.txt', 'r')
        data = json.load(fp)

        participants = data['Participants']

        user = None

        for p in participants:
            if str(p['id']) == self.patientId:
                user = p
                break


        if user is not None:

            ttk.Label(top, text="Participant n " + self.patientId, font='Times 26').grid(row=0, column=1, pady =30, padx = 20)
            ttk.Label(top, text="Age :  " + user['age'], font='Times 18').grid(row=1, column=1, sticky=tk.W, pady =20, padx = 5)
            ttk.Label(top, text="Gender :  " + user['gender'], font='Times 18').grid(row=2, column=1, sticky=tk.W, pady =20, padx = 5)
            ttk.Label(top, text="Educational Level :  " + user['edu'], font='Times 18').grid(row=3, column=1, sticky=tk.W, pady =20, padx = 5)



        else:
            ttk.Label(top, text="Data on Participant n " + self.patientId+ " not found.", font='Times 18').grid(row=0, column=1, padx = 5)
            top.rowconfigure(0, weight=1)

        ttk.Button(top, text="Close", command=top.destroy).grid(row=4, column=1, pady=50)
