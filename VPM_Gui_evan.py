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
    'coherent' : {
        '100' : {
            '64' : 820, '128' : 595, '256' : 1650, '512' : 2355,
            },
        '200' : {
            '64' : 605, '128' : 865, '256' : 620, '512' : 1720, '1024' : 2430,
            },
        '800' : {
            '32':375, '64':420, '128':800, '256':940, '512':1585, '1024':880, '2048':3155, '4096':4550,
            },
        '1500' : {
            '32':365, '64':530, '128':730, '256':1070, '512':1450, '1024':1085, '2048':3000, '4096':3750,
            },
        },
    'incoherent' : {
        '100' : {
            '512' : 1875, '1024' : 4010, '2048' : 550, '4096' : 990, '8192' : 580,
            },
        '200' : {
            '1024' : 1920, '2048' : 1030, '4096' : 540, '8192' : 1045,
            },
        '800' : {
            '32':14380, '64':7240, '128':14690, '256':7340, '512':15320, '1024':7495, '2048':14300, '4096':7450, '8192':24725,
            },
        '1500' : {
            '32':14675, '64':6835, '128':13485, '256':6750, '512':13345, '1024':6655, '2048':13035, '4096':6595, '8192':13500,
            },
        },
    }


#conversion gui -> internal variable names
Diode_Scheme = {'Low Power':"'lo'", 'High Power':"'hi'", 'Off':"'off'"}
Stokes_Scheme= {'Total Intensity':"'total_intensity'", 'Full Stokes':"'full_stokes'"}

#derived stuff specific to each receiver
#nwin, restfreq, bw, dopplertrackfreq, deltafreq
Rcvr_specific = {
    'Rcvr_342' : [1, 350, 100, 0, 350, 0.0],
    'Rcvr_800' : [1, 820, 200, 1, 820, 0.0],
    'Rcvr1_2'  : [1, 1500, 800, 2, 1500, 0.0, 'In'],
    'Rcvr2_3'  : [1, 2165, 1500, 3, 2165, 0.0],
    'Rcvr4_6'  : [4, """[{'bank':'A','restfreq':7687.5},\n\t{'bank':'B','restfreq':6562.5},\n\t{'bank':'C','restfreq':5437.5},\n\t{'bank':'D','restfreq':4312.5}]""", 1500, 3, 5637.5, "0.0,0.0,0.0,0.0"],
    'Rcvr8_10' : [4, """[{'bank':'A','restfreq':11506.8359375},\n\t{'bank':'B','restfreq':10504.8828125},\n\t{'bank':'C','restfreq':9502.9296875},\n\t{'bank':'D','restfreq':8500.9765625}]""", 1500, 3, 9702.9296875, "0.0,0.0,0.0,0.0"],
    'Rcvr_2500': [3, "1225.0, 2350.0, 3475.0", 1500, 3, 6875.0, 0.0],
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
        self.Observation_Mode.activated.connect(self.DisEnable_Fold_Options)
        self.Dispersion_Mode.activated.connect(self.DisEnable_Fold_Options)

        #things to default on start
        default_grayout = Nchan_Grayout_Scheme['coherent/100']
        for i in default_grayout:
                    self.Nchan.model().item(i).setEnabled(False)
        self.Nchan.setCurrentIndex(1)
        self.Receiver_Names.setCurrentIndex(2)
        self.Parfile.setEnabled(False)
        rx = 'Rcvr1_2'
        self.RestFrequency.setText(str(Rcvr_specific[rx][1]))
        self.Band_Width.setCurrentIndex(Rcvr_specific[rx][3])
        self.DopplerTrackFreq.insert(str(Rcvr_specific[rx][4]))
        self.DeltaFreq.insert(str(Rcvr_specific[rx][5]))
        self.Fold_Bins.insert('2048')
        self.Fold_Time.insert('10.0')

    #Gray out nchan values based on the coherent/incoherent and bandwaidth selected
    def Combo_Box_Bw_Nchan(self):
        Count_Nchan = self.Nchan.count()
        for contents in range(Count_Nchan):
            self.Nchan.model().item(contents).setEnabled(True)
            #self.Tint.model().item(contents).setEnabled(True)

        def Gray_Out_Bw_Nchan(grayout_index,Band_Width_Item):
            Band_Width_Selected_Item  = self.Band_Width.currentText()

            if Band_Width_Selected_Item == Band_Width_Item:
                self.Nchan.model().item(1).setEnabled(False)
                #self.Tint.model().item(1).setEnabled(False)

                for i in range(9):
                    self.Nchan.model().item(i).setEnabled(True)
                for i in grayout_index:
                    self.Nchan.model().item(i).setEnabled(False)
                    #self.Tint.model().item(i).setEnabled(False)

        current_mode = f'{self.Dispersion_Mode.currentText()}/{self.Band_Width.currentText()}'
        
        Gray_Out_Bw_Nchan( Nchan_Grayout_Scheme[current_mode], self.Band_Width.currentText() )

    #need to autofill the Rx specific options
    #Rx specific things
    #nwin, restfreq, bw, bw_index, dopplertrackfreq, deltafreq
    def Auto_Select_Rx_specifics(self):
        rx = Rcvr_Dict[self.Receiver_Names.currentText()]

        #self.Rest_Frequency.clear()
        self.DopplerTrackFreq.clear()
        self.DeltaFreq.clear()

        self.Num_Win.setCurrentIndex(Rcvr_specific[rx][0]-1)
        #self.Rest_Frequency.insert(str(Rcvr_specific[rx][1]))
        self.RestFrequency.setText(str(Rcvr_specific[rx][1]))
        self.Band_Width.setCurrentIndex(Rcvr_specific[rx][3])
        self.DopplerTrackFreq.insert(str(Rcvr_specific[rx][4]))
        self.DeltaFreq.insert(str(Rcvr_specific[rx][5]))
        

    #not sure what this does
    def Auto_Select_Nchan_Tint(self):
        #Tint_Count = self.Tint.count()
        #Item       = self.Nchan.currentIndex()
        #self.Tint.setCurrentIndex(Item)
        #for j in range(Tint_Count):
        #    if j == Item:
        #        None
        #    else:
        #        self.Tint.model().item(j).setEnabled(False)
        pass

    #select scale based on bw, nchan, mode
    def Auto_Select_Tint_and_Scale(self):
        bw = self.Band_Width.currentText()
        mode = self.Dispersion_Mode.currentText()
        nchan = self.Nchan.currentText()
        
        scale = Scale_Scheme[mode][bw][nchan]

        print(float(nchan), (float(bw)*1e6))
    
        tint = f'{self.Accum_Len.currentText()}*nchan / bw)'

        return tint,scale

    #Enable/Disable parfile and DM options based on ddmode and obsmode
    #no checking of valid DM and parfiles here, this will be done in Generate_Script()
    def DisEnable_Fold_Options(self):
        ddmode = self.Dispersion_Mode.currentText()
        obsmode = self.Observation_Mode.currentText()

        if obsmode in ['cal','search']:
            self.Parfile.setEnabled(False)
        if obsmode == 'fold':
            self.Parfile.setEnabled(True)
        if ddmode == 'coherent':
            self.Dispersion_Measure.setEnabled(True)
        if ddmode == 'incoherent':
            self.Dispersion_Measure.setEnabled(False)


    #make config variable name
    def Create_Name(self):
        rcvr    = Rcvr_Dict[self.Receiver_Names.currentText()]
        ddmode  = self.Dispersion_Mode.currentText()
        bw      = self.Band_Width.currentText()
        nchan   = self.Nchan.currentText()
        nwin    = self.Num_Win.currentText()
        obsmode = self.Observation_Mode.currentText()
        Config_Name = f"config_vpm_{rcvr}_{ddmode[0]}{bw}x{nchan}_{obsmode}"
        #self.Display_Script.append(Config_Name)
        return Config_Name

    #make the configuration dictionary
    #need to make new function that turns the dictionary into a string,
    #   with different things in there based on the mode
    def Generate_Script(self):
        self.Display_Script.clear()
        Config_dict = {}
        #set obvious things
        Config_dict['obstype'] = "'Pulsar'"
        Config_dict['backend'] = "'VEGAS'"
        Config_dict['vframe'] = "'topo'"
        Config_dict['vdef'] = "'Radio'"
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

        if self.Dispersion_Mode.currentText() == 'incoherent':
            obsmode = f'{self.Observation_Mode.currentText}'
        else:
            obsmode = f'{self.Dispersion_Mode.currentText()}_{self.Observation_Mode.currentText()}'
        Config_dict['vegas.obsmode'] = obsmode

        #obsmode specific things
        if obsmode in ['cal','coherent_cal']:
            Config_dict['vegas.fold_bins'] = 2048
            Config_dict['vegas.fold_dumptime'] = 10.0
            Config_dict['swmode'] = "'tp'"
        elif obsmode in ['fold','coherent_fold']:
            Config_dict['vegas.fold_bins'] = 2048
            Config_dict['vegas.fold_dumptime'] = 10.0
            Config_dict['swmode'] = "'tp_nocal'"
            #check for fold parameters?
        elif obsmode in ['search','coherent_search']:
            Config_dict['swmode'] = "'tp_nocal'"


        #check for fold/dm parameters here
        if obsmode[-4:] == 'fold':
            valid_par = os.path.isfile(self.Parfile.text())
            print('Valid parfile:',valid_par)
        else:
               valid_par = True
        Config_dict['vegas.fold_parfile'] = self.Parfile.text()

        #warn user if they intend to leave dm=0/blank for coh dd
        ddmode = self.Dispersion_Mode.currentText()
        dm = self.Dispersion_Measure.text()
        if dm =='':
            dm = '0'
        if (ddmode == 'coherent') and (dm == '0'):
            valid_dm = False
        else:
            valid_dm = True
        print('Valid DM',valid_dm)
        Config_dict['vegas.dm'] = self.Dispersion_Measure.text()



        if obsmode[-3:] == 'cal':
            Config_dict['swmode'] = "'tp_cal'"
        else:
            Config_dict['swmode'] = "'tp_nocal'"
        

        #unpickable things
        tint,scale = self.Auto_Select_Tint_and_Scale()
        Config_dict['vegas.scale'] = scale
        Config_dict['tint'] = tint#f'{tint*1e6}e-6'


        #Rx specific things
        #nwin, restfreq, bw, dopplertrackfreq, deltafreq
        #these are grabbed from the gui, which are set automatically via Auto_Select_Rx_specifics()
        Config_dict['nwin'] = self.Num_Win.currentText()
        Config_dict['restfreq'] = self.RestFrequency.toPlainText()
        Config_dict['bandwidth'] = self.Band_Width.currentText()
        Config_dict['dopplertrackfreq'] = self.DopplerTrackFreq.text()
        Config_dict['deltafreq'] = self.DeltaFreq.text()
        if rx == 'Rcvr1_2':
            Config_dict['notchfilter'] = "'In'"
        
        print(Config_dict)

        for key in Config_dict.keys():
            print(f'{key} = {Config_dict[key]}')

        #now print the things to the display
        
        output_str = """"""

        output_str += f'{time.time()}\n'

        #errors first
        if not valid_par:
            output_str += 'ERROR: Invalid Parfile. Please double check your filename.\n'
        

        #warnings:
        if not valid_dm:
            output_str +=  'WARNING: DM set to 0 or blank. Did you intend to leave that as is?\n'

        #now config statements
        output_str += '========================================\n'

        output_str += f'{self.Create_Name()} = """\n'
        
        output_str += f"obstype = {Config_dict['obstype']}\n"
        output_str += f"backend = {Config_dict['backend']}\n"
        output_str += f"receiver = {Config_dict['receiver']}\n"
        if Config_dict['receiver'] == 'Rcvr1_2':
            output_str += f"notchfilter = {Config_dict['notchfilter']}\n"
        output_str += f"restfreq = {Config_dict['restfreq']}\n"
        output_str += f"nwin = {Config_dict['nwin']}\n"
        output_str += f"deltafreq = {Config_dict['deltafreq']}\n"
        output_str += f"swtype = {Config_dict['swtype']}\n"
        output_str += f"swper = {Config_dict['swper']}\n"
        output_str += f"swfreq = {Config_dict['swfreq']}\n"
        output_str += f"vlow = {Config_dict['vlow']}\n"
        output_str += f"vhigh = {Config_dict['vhigh']}\n"
        output_str += f"vframe = {Config_dict['vframe']}\n"
        output_str += f"vdef = {Config_dict['vdef']}\n"
        output_str += f"vegas.polnmode = {Config_dict['vegas.polnmode']}\n"
        output_str += f"vegas.numchan = {Config_dict['vegas.numchan']}\n"
        output_str += f"vegas.outbits = {Config_dict['vegas.outbits']}\n"
        output_str += f"vegas.scale = {Config_dict['vegas.scale']}\n"
        if Config_dict['vegas.obsmode'][-4:] == 'fold':
            output_str += f"vegas.fold_dumptime = {Config_dict['vegas.fold_dumptime']}\n"
            output_str += f"vegas.fold_bins = {Config_dict['vegas.fold_bins']}\n"
            output_str += f"vegas.fold_parfile = '{Config_dict['vegas.fold_parfile']}'\n"
        
        output_str += '"""'

        if not valid_par:
            output_str = output_str[:output_str.index('\n')]

        self.Display_Script.append(output_str)


        def Generate_Command(Widget_Input, Widget_List):
            print(Widget_List,Widget_Input)
            Full_Command_Statement = Command[Widget_List].replace("null", Widget_Input)
            return self.Display_Script.append(Full_Command_Statement)



        #for Command_List_Index, Widget_Text in enumerate(Command_List):
        #    print(Command_List)
        #    Generate_Command(Widget_Text, Command_List_Index)
            #print(Widget_Text, Command - List)

    #not sure what this does
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
