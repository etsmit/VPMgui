import sys
import os
import time
from PyQt5.Qt import QApplication, QMainWindow
from PyQt5.uic import loadUiType
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

import numpy as np


qtCreatorFile = r"VPM_Config_evan.ui"
Ui_MainWindow, QtBaseClass = loadUiType(qtCreatorFile)
path = r"/users/esmith/VPMgui/"
os.chdir(path)
Config_Commands = open("Config_commands.txt")
Command = Config_Commands.readlines()

#global variables

#dictionary mapping Rx item name to code for config string
Rcvr_Dict = {"PF342 (Rcvr_342)": "Rcvr_342", "PF800 (Rcvr_800)": "Rcvr_800", "L-Band (Rcvr1_2)": "Rcvr1_2", "S-Band (Rcvr2_3)": "Rcvr2_3", "C-Band (Rcvr4_6)": "Rcvr4_6", "X-Band (Rcvr8_10)": "Rcvr8_10", "UWBR (Rcvr_2500)": "Rcvr_2500"}

#which nchan items to gray out based on dedisp method and bandwidth
#keys are formatted {mode}/{bw}
Nchan_Grayout_Scheme = {'coherent/100' : np.r_[0,5:9], 'coherent/200' : np.r_[0,6:9], 'coherent/800' : np.r_[8], 'coherent/1500' : np.r_[8], 'incoherent/100' : np.r_[0:4,8], 'incoherent/200' : np.r_[0:5], 'incoherent/800' : np.array([]), 'incoherent/1500' : np.r_[8]}


Scale_Scheme = {
    'coherent/100/64':820, 'coherent/100/128':595, 'coherent/100/256':1650, 'coherent/100/512':2355,
    'coherent/200/64':605, 'coherent/200/128':865, 'coherent/200/256':620, 'coherent/200/512':1720, 'coherent/200/1024':2430,
    'coherent/800/32':375, 'coherent/800/64':420, 'coherent/800/128':800, 'coherent/800/256':940, 'coherent/800/512':1585, 'coherent/800/1024':880,  'coherent/800/2048':3155, 'coherent/800/4096':4550,
    'coherent/1500/32':365, 'coherent/1500/64':530, 'coherent/1500/128':730, 'coherent/1500/256':1070, 'coherent/1500/512':1450, 'coherent/1500/1024':1085,  'coherent/1500/2048':3000, 'coherent/1500/4096':3750,
    'incoherent/100/512':1875, 'incoherent/100/1024':4010, 'incoherent/100/2048':550, 'incoherent/100/4096':990, 'incoherent/100/8192':580,
    'incoherent/200/1024':1920, 'incoherent/200/2048':1030, 'incoherent/200/4096':540, 'incoherent/200/8192':1045, 
    'incoherent/800/32':14380, 'incoherent/800/64':7240, 'incoherent/800/128':14690, 'incoherent/800/256':7340, 'incoherent/800/512':15320, 'incoherent/800/1024':7495, 'incoherent/800/2048':14300, 'incoherent/800/4096':7545, 'incoherent/800/8192':24725,
    'incoherent/1500/32':14675, 'incoherent/1500/64':6835, 'incoherent/1500/128':13485, 'incoherent/1500/256':6750, 'incoherent/1500/512':13345, 'incoherent/1500/1024':6655, 'incoherent/1500/2048':13035, 'incoherent/1500/4096':6595, 'incoherent/1500/8192':13500,
    }

#conversion gui -> internal variable names
Diode_Scheme = {'Low Power':"'lo'", 'High Power':"'hi'", 'Off':"'off'"}
Stokes_Scheme= {'Total Intensity':"'total_intensity'", 'Full Stokes':"'full_stokes'"}

#derived stuff specific to each receiver
#nwin, restfreq, bw, dopplertrackfreq, deltafreq
Rcvr_specific = {
    'Rcvr_342' : [1, 350, 100, 0, 350, 0.0],
    'Rcvr_800' : [1, 820, 200, 1, 820, 0.0],
    'Rcvr1_2'  : [1, 1500, 800, 2, 1500, 0.0],
    'Rcvr2_3'  : [1, 2165, 1500, 3, 2165, 0.0],
    'Rcvr4_6'  : [4, """[{'bank':'A','restfreq':7687.5},\n\t{'bank':'B','restfreq':6562.5},\n\t{'bank':'C','restfreq':5437.5},\n\t{'bank':'D','restfreq':4312.5}]""", 1500, 3, 5637.5, "0.0,0.0,0.0,0.0"],
    'Rcvr8_10' : [4, """[{'bank':'A','restfreq':11506.8359375},\n\t{'bank':'B','restfreq':10504.8828125},\n\t{'bank':'C','restfreq':9502.9296875},\n\t{'bank':'D','restfreq':8500.9765625}]""", 1500, 3, 9702.9296875, "0.0,0.0,0.0,0.0"],
    'Rcvr_2500': [3, "1225.0,2350.0,3475.0", 1500, 3, 6875.0, 0.0],
    }




class App(QMainWindow, Ui_MainWindow):
    def __init__(self):
        # Do QMainWindow stuff
        QMainWindow.__init__(self)
        # Set up the UI file
        self.setupUi(self)
        self.Band_Width.activated.connect(self.Combo_Box_Bw_Nchan)
        self.Nchan.activated.connect(self.Auto_Select_Nchan_Tint)
        self.Nchan.activated.connect(self.Auto_Select_Tint_and_Scale)
        self.Receiver_Names.activated.connect(self.Auto_Select_Rx_specifics)
        self.Receiver_Names.activated.connect(self.Combo_Box_Bw_Nchan)
        self.Dispersion_Mode.activated.connect(self.Combo_Box_Bw_Nchan)
        #self.Create_Script.clicked.connect(self.Create_Name)
        self.Create_Script.clicked.connect(self.Generate_Script)
        self.Observation_Mode.activated.connect(self.Polarization_Mode)

    #Gray out nchan values based on the coherent/incoherent and bandwaidth selected
    def Combo_Box_Bw_Nchan(self):
        Count_Nchan = self.Nchan.count()
        print(type(self.Nchan))
        for contents in range(Count_Nchan):
            self.Nchan.model().item(contents).setEnabled(True)
            self.Tint.model().item(contents).setEnabled(True)

        def Gray_Out_Bw_Nchan(grayout_index,Band_Width_Item):
            Band_Width_Selected_Item  = self.Band_Width.currentText()

            if Band_Width_Selected_Item == Band_Width_Item:
                self.Nchan.model().item(1).setEnabled(False)
                self.Tint.model().item(1).setEnabled(False)

                for i in range(9):
                    self.Nchan.model().item(i).setEnabled(True)
                for i in grayout_index:
                    self.Nchan.model().item(i).setEnabled(False)
                    self.Tint.model().item(i).setEnabled(False)

        current_mode = f'{self.Dispersion_Mode.currentText()}/{self.Band_Width.currentText()}'
        print(current_mode, Nchan_Grayout_Scheme[current_mode])
        
        Gray_Out_Bw_Nchan( Nchan_Grayout_Scheme[current_mode], self.Band_Width.currentText() )

    #need to autofill the Rx specific options
    #Rx specific things
    #nwin, restfreq, bw, bw_index, dopplertrackfreq, deltafreq
    def Auto_Select_Rx_specifics(self):
        rx = Rcvr_Dict[self.Receiver_Names.currentText()]
        print(rx)

        #self.Rest_Frequency.clear()
        self.DopplerTrackFreq.clear()
        self.DeltaFreq.clear()

        self.Num_Win.setCurrentIndex(Rcvr_specific[rx][0]-1)
        #self.Rest_Frequency.insert(str(Rcvr_specific[rx][1]))
        self.textEdit.setText(str(Rcvr_specific[rx][1]))
        self.Band_Width.setCurrentIndex(Rcvr_specific[rx][3])
        self.DopplerTrackFreq.insert(str(Rcvr_specific[rx][4]))
        self.DeltaFreq.insert(str(Rcvr_specific[rx][5]))
        

    #not sure what this does
    def Auto_Select_Nchan_Tint(self):
        Tint_Count = self.Tint.count()
        Item       = self.Nchan.currentIndex()
        self.Tint.setCurrentIndex(Item)
        for j in range(Tint_Count):
            if j == Item:
                None
            else:
                self.Tint.model().item(j).setEnabled(False)

    #select scale based on bw, nchan, mode
    def Auto_Select_Tint_and_Scale(self):
        bw = self.Band_Width.currentText()
        mode = self.Dispersion_Mode.currentText()
        nchan = self.Nchan.currentText
        
        key = f'{mode}/{bw}/{nchan}'
        scale = Scale_Scheme[key]
    
        tint = 16 * nchan / bw

        return tint,scale


    def Create_Name(self):
        rcvr    = self.Receiver_Names.currentText()
        ddmode  = self.Dispersion_Mode.currentText()
        bw      = self.Band_Width.currentText()
        nchan   = self.Nchan.currentText()
        nwin    = 1
        obsmode = self.Observation_Mode.currentText()
        Config_Name = "config_vpm_{}_{}{}x{}x{}_{}".format(Rcvr_Dict[rcvr],ddmode,bw,nchan,nwin,obsmode)
        self.Display_Script.append(Config_Name)

    def Generate_Script(self):
        self.Display_Script.clear()
        Config_dict = {}
        #set obvious things
        Config_dict['obstype'] = "'Pulsar'"
        Config_dict['vframe'] = "'topo'"
        Config_dict['vlow'] = "0.0"
        Config_dict['vhigh'] = "0.0"
        Config_dict['vegas.outbits'] = "8"
        Config_dict['swtype'] = "'none'"
        Config_dict['swper'] = "0.04"
        Config_dict['swfreq'] = "0.0"
        Config_dict['pol'] = "'Linear'"

        #now set things from the gui
        rx = Rcvr_Dict[self.Receiver_Names.currentText()]
        Config_dict['receiver'] = rx
        Config_dict['vegas.numchan'] = self.Nchan.currentText()
        Config_dict['noisecal'] = Diode_Scheme[self.Noise_Diode_State.currentText()]
        Config_dict['vegas.polnmode'] = Stokes_Scheme[self.Polarization_Products.currentText()]

        obsmode = f'{self.Dispersion_Mode.currentText()}_{self.Observation_Mode.currentText}'
        Config_dict['vegas.obsmode'] = obsmode

        if obsmode[-3:] == 'cal':
            Config_dict['swmode'] = "'tp_cal'"
        else:
            Config_dict['swmode'] = "'tp_nocal'"
        

        
        #unpickable things
        tint,scale = self.Auto_Select_Tint_and_Scale()
        Config_dict['vegas.scale'] = scale
        Config_dict['tint'] = f'{tint*1e6}e-6'


        #Rx specific things
        #nwin, restfreq, bw, dopplertrackfreq, deltafreq
        #these are grabbed from the gui, which are set automatically via Auto_Select_Rx_specifics()
        Config_dict['nwin'] = self.Num_Win.currentText()
        Config_dict['restfreq'] = self.RestFrequency.currentText()
        Config_dict['bandwidth'] = self.Band_Width.currentText()
        Config_dict['dopplertrackfreq'] = self.DopplerTrackFreq.currentText()
        Config_dict['deltafreq'] = self.DeltaFreq.currentText()
        


        Command_List = [self.Observation_Mode.currentText(),
                        self.Receiver_Names.currentText(),
                        self.Rest_Frequency.text(),
                        self.Noise_Diode_State.currentText(),
                        self.Polarization.currentText(),
                        self.Band_Width.currentText(),
                        self.Tint.currentText(),
                        self.Nchan.currentText(),
                        self.Scale.currentText(),
                        self.Polarization_Products.currentText(),
                       self.Parfile.text(),
                       self.Fold_Time.text(),
                       self.Dispersion_Mode.currentText(),
                       self.Fold_Bins.text()
                        ]




        def Generate_Command(Widget_Input, Widget_List):
            print(Widget_List,Widget_Input)
            Full_Command_Statement = Command[Widget_List].replace("null", Widget_Input)
            return self.Display_Script.append(Full_Command_Statement)


        rcvr = self.Receiver_Names.currentText()
        ddmode = self.Dispersion_Mode.currentText()
        bw = self.Band_Width.currentText()
        nchan = self.Nchan.currentText()
        #nwin = 
        obsmode = self.Observation_Mode.currentText()
        Config_Name = "config_vpm_{}_{}{}x{}x{}_{}".format(Rcvr_Dict[rcvr], ddmode, bw, nchan, nwin, obsmode)
        self.Display_Script.append(Config_Name)

        for Command_List_Index, Widget_Text in enumerate(Command_List):
            print(Command_List)
            Generate_Command(Widget_Text, Command_List_Index)
            #print(Widget_Text, Command - List)

    def Polarization_Mode(self):
        ObsMode_Search = ["Total Intensity","Full Stokes"]
        ObsMode_Other  = ["Full Stokes", "Total Intensity"]
        DdMode = self.Dispersion_Mode.currentText()
        ObsMode = self.Observation_Mode.currentText()
        if ObsMode == "Search":
            if DdMode == "Inchoherent":
                self.Polarization_Products.clear()
                self.Polarization_Products.addItems(ObsMode_Search)

            else:
                None

        else:
            self.Polarization_Products.clear()
            self.Polarization_Products.addItems(ObsMode_Other)
            self.Polarization_Products.model().item(1).setEnabled(False)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
