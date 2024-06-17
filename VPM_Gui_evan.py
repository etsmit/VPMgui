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
Nchan_Grayout_Scheme = {'Coherent/100' : np.r_[0,5:9], 'Coherent/200' : np.r_[0,6:9], 'Coherent/800' : np.r_[8], 'Coherent/1500' : np.r_[8], 'Incoherent/100' : np.r_[0:4,8], 'Incoherent/200' : np.r_[0:5], 'Incoherent/800' : np.r_[9], 'Incoherent/1500' : np.r_[8]}




class App(QMainWindow, Ui_MainWindow):
    def __init__(self):
        # Do QMainWindow stuff
        QMainWindow.__init__(self)
        # Set up the UI file
        self.setupUi(self)
        self.Band_Width.activated.connect(self.Combo_Box_Bw_Nchan)
        self.Nchan.activated.connect(self.Auto_Select_Nchan_Tint)
        self.Nchan.activated.connect(self.Auto_Select_Tint_and_Scale)
        #self.Create_Script.clicked.connect(self.Create_Name)
        self.Create_Script.clicked.connect(self.Generate_Script)
        self.Observation_Mode.activated.connect(self.Polarization_Mode)

    #
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

                for i in grayout_index:
                    self.Nchan.model().item(i).setEnabled(False)
                    self.Tint.model().item(i).setEnabled(False)

        current_mode = f'{self.Dispersion_Mode.currentText()}/{self.Band_Width.currentText()}'
        print(current_mode, Nchan_Grayout_Scheme[current_mode])
        
        Gray_Out_Bw_Nchan( Nchan_Grayout_Scheme[current_mode], self.Band_Width.currentText() )

        #if self.Dispersion_Mode.currentText() == "Coherent":
        #    Gray_Out_Bw_Nchan(, "100")
        #    Gray_Out_Bw_Nchan(, "200")
        #    Gray_Out_Bw_Nchan(, "1500")



        #elif self.Dispersion_Mode.currentText() == "Incoherent":
        #    Gray_Out_Bw_Nchan(, "100")
        #    Gray_Out_Bw_Nchan(, "200")

    def Auto_Select_Nchan_Tint(self):
        Tint_Count = self.Tint.count()
        Item       = self.Nchan.currentIndex()
        self.Tint.setCurrentIndex(Item)
        for j in range(Tint_Count):
            if j == Item:
                None
            else:
                self.Tint.model().item(j).setEnabled(False)

    def Auto_Select_Tint_and_Scale(self):
        Band_Width_Item = self.Band_Width.currentText()
        Count_Scale = self.Scale.count()

        def Auto_select_Scale(Scale_Range,Item_Tint,Selected_Scale):
            if self.Tint.currentText() == Item_Tint:
                Scale_Item_Index = self.Scale.findText(Selected_Scale)
                self.Scale.setCurrentIndex(Scale_Item_Index)

                for k in range(Scale_Range):
                    if k == Scale_Item_Index:
                        None
                    else:
                        self.Scale.model().item(k).setEnabled(False)
        if self.Dispersion_Mode.currentText() == "Coherent":
            if Band_Width_Item == "100":
                Auto_select_Scale(Count_Scale,"64" ,"820")
                Auto_select_Scale(Count_Scale,"128" ,"595")
                Auto_select_Scale(Count_Scale,"256" ,"1650")
                Auto_select_Scale(Count_Scale,"512" ,"2355")

            elif Band_Width_Item == "200":
                Auto_select_Scale(Count_Scale, "64", "605")
                Auto_select_Scale(Count_Scale, "128", "865")
                Auto_select_Scale(Count_Scale, "256", "620")
                Auto_select_Scale(Count_Scale, "512", "1720")
                Auto_select_Scale(Count_Scale, "1024", "2430")

            elif Band_Width_Item == "800":
                Auto_select_Scale(Count_Scale, "32", "375")
                Auto_select_Scale(Count_Scale, "64", "420")
                Auto_select_Scale(Count_Scale, "128", "800")
                Auto_select_Scale(Count_Scale, "256", "940")
                Auto_select_Scale(Count_Scale, "512", "1585")
                Auto_select_Scale(Count_Scale, "1024", "880")
                Auto_select_Scale(Count_Scale, "2048", "3155")
                Auto_select_Scale(Count_Scale, "4096", "4550")

            elif Band_Width_Item == "1500":
                Auto_select_Scale(Count_Scale, "32", "365")
                Auto_select_Scale(Count_Scale, "64", "530")
                Auto_select_Scale(Count_Scale, "128", "730")
                Auto_select_Scale(Count_Scale, "256", "1070")
                Auto_select_Scale(Count_Scale, "512", "1450")
                Auto_select_Scale(Count_Scale, "1024", "1085")
                Auto_select_Scale(Count_Scale, "2048", "3000")
                Auto_select_Scale(Count_Scale, "4096", "3750")

        elif self.Dispersion_Mode.currentText() == "Incoherent":
            if Band_Width_Item == "100":
                Auto_select_Scale(Count_Scale, "512", "1875")
                Auto_select_Scale(Count_Scale, "1024", "4010")
                Auto_select_Scale(Count_Scale, "2048", "550")
                Auto_select_Scale(Count_Scale, "4096", "990")
                Auto_select_Scale(Count_Scale, "8192", "580")

            elif Band_Width_Item == "200":
                Auto_select_Scale(Count_Scale, "1024", "1920")
                Auto_select_Scale(Count_Scale, "2048", "1030")
                Auto_select_Scale(Count_Scale, "4096", "540")
                Auto_select_Scale(Count_Scale, "8192", "1045")

            elif Band_Width_Item == "800":
                Auto_select_Scale(Count_Scale, "32", "14830")
                Auto_select_Scale(Count_Scale, "64", "7240")
                Auto_select_Scale(Count_Scale, "128", "14690")
                Auto_select_Scale(Count_Scale, "256", "7340")
                Auto_select_Scale(Count_Scale, "512", "15320")
                Auto_select_Scale(Count_Scale, "1024", "7495")
                Auto_select_Scale(Count_Scale, "2048", "14300")
                Auto_select_Scale(Count_Scale, "4096", "7545")
                Auto_select_Scale(Count_Scale, "8192", "14725")

            elif Band_Width_Item == "1500":
                Auto_select_Scale(Count_Scale, "32", "14675")
                Auto_select_Scale(Count_Scale, "64", "6835")
                Auto_select_Scale(Count_Scale, "128", "13485")
                Auto_select_Scale(Count_Scale, "256", "6750")
                Auto_select_Scale(Count_Scale, "512", "13345")
                Auto_select_Scale(Count_Scale, "1024", "6655")
                Auto_select_Scale(Count_Scale, "2048", "13035")
                Auto_select_Scale(Count_Scale, "4096", "6595")
                Auto_select_Scale(Count_Scale, "8192", "13500")

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
        Config_dict['receiver'] = Rcvr_Dict[self.Receiver_Names.currentText()]
        Config_dict['nchan'] = self.Nchan.currentText()
        Config_dict['noisecal'] = self.Noise_Diode_State.currentText()
        Config_dict['noisecal'] = self.Noise_Diode_State.currentText()


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

        Rcvr_Dict = {"PF342 (Rcvr_342)": "Rcvr_342", "PF800 (Rcvr_800)": "Rcvr_800", "L-Band (Rcvr1_2)": "Rcvr1_2", "S-Band (Rcvr2_3)": "Rcvr2_3", "C-Band (Rcvr4_6)": "Rcvr4_6", "X-Band (Rcvr8_10)": "Rcvr8_10", "UWBR (Rcvr_2500)": "Rcvr_2500"}
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
