import sys
import os
import time
from PyQt5.Qt import QApplication, QMainWindow
from PyQt5.uic import loadUiType
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


qtCreatorFile = r"VPM_Config_evan.ui"
Ui_MainWindow, QtBaseClass = loadUiType(qtCreatorFile)
path = r"/users/esmith/VPMgui/"
os.chdir(path)
Config_Commands = open("Config_commands.txt")
Command = Config_Commands.readlines()

global Rcvr_Dict = {"L-Band (Rcvr1_2)": "Rcvr1_2", "S-Band (Rcvr2_3)": "Rcvr2_3",
                     "C-Band (Rcvr4_6)": "Rcvr4_6", "X-Band (Rcvr8_10)": "Rcvr8_10"}


class App(QMainWindow, Ui_MainWindow):
    def __init__(self):
        # Do QMainWindow stuff
        QMainWindow.__init__(self)
        # Set up the UI file
        self.setupUi(self)
        self.Band_Width.activated.connect(self.Combo_Box_Bw_Nchan)
        self.Nchan.activated.connect(self.Auto_Select_Nchan_Tint)
        self.Nchan.activated.connect(self.Auto_Select_Tint_Scale)
        #self.Create_Script.clicked.connect(self.Create_Name)
        self.Create_Script.clicked.connect(self.Generate_Script)
        self.Observation_Mode.activated.connect(self.Polarization_Mode)

    def Combo_Box_Bw_Nchan(self):
        Count_Nchan = self.Nchan.count()
        for contents in range(Count_Nchan):
            self.Nchan.model().item(contents).setEnabled(True)
            self.Tint.model().item(contents).setEnabled(True)

        def Gray_Out_Bw_Nchan(Range_Gray_Out,Start_Gray_Out,Band_Width_Item):
            Band_Width_Selected_Item  = self.Band_Width.currentText()

            if Band_Width_Selected_Item == Band_Width_Item:
                self.Nchan.model().item(1).setEnabled(False)
                self.Tint.model().item(1).setEnabled(False)

                for i in range(Range_Gray_Out):
                    self.Nchan.model().item(i + Start_Gray_Out).setEnabled(False)
                    self.Tint.model().item(i + Start_Gray_Out).setEnabled(False)

        if self.Dispersion_Mode.currentText() == "Coherent":
            Gray_Out_Bw_Nchan(4, 6, "100")
            Gray_Out_Bw_Nchan(3, 7, "200")
            Gray_Out_Bw_Nchan(2, 8, "1500")



        elif self.Dispersion_Mode.currentText() == "Incoherent":
            Gray_Out_Bw_Nchan(4, 1, "100")
            Gray_Out_Bw_Nchan(5, 1, "200")

    def Auto_Select_Nchan_Tint(self):
        Tint_Count = self.Tint.count()
        Item       = self.Nchan.currentIndex()
        self.Tint.setCurrentIndex(Item)
        for j in range(Tint_Count):
            if j == Item:
                None
            else:
                self.Tint.model().item(j).setEnabled(False)

    def Auto_Select_Tint_Scale(self):
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
                Auto_select_Scale(Count_Scale,"64" ,"1500")
                Auto_select_Scale(Count_Scale,"128" ,"1000")
                Auto_select_Scale(Count_Scale,"256" ,"2500")
                Auto_select_Scale(Count_Scale,"512" ,"3750")

            elif Band_Width_Item == "200":
                Auto_select_Scale(Count_Scale, "64", "1000")
                Auto_select_Scale(Count_Scale, "128", "1500")
                Auto_select_Scale(Count_Scale, "256", "1000")
                Auto_select_Scale(Count_Scale, "512", "2500")
                Auto_select_Scale(Count_Scale, "1024", "3750")

            elif Band_Width_Item == "800":
                Auto_select_Scale(Count_Scale, "32", "300")
                Auto_select_Scale(Count_Scale, "64", "450")
                Auto_select_Scale(Count_Scale, "128", "675")
                Auto_select_Scale(Count_Scale, "256", "1000")
                Auto_select_Scale(Count_Scale, "512", "1500")
                Auto_select_Scale(Count_Scale, "1024", "1000")
                Auto_select_Scale(Count_Scale, "2048", "2500")
                Auto_select_Scale(Count_Scale, "4096", "3750")

            elif Band_Width_Item == "1500":
                Auto_select_Scale(Count_Scale, "32", "300")
                Auto_select_Scale(Count_Scale, "64", "500")
                Auto_select_Scale(Count_Scale, "128", "700")
                Auto_select_Scale(Count_Scale, "256", "1000")
                Auto_select_Scale(Count_Scale, "512", "1375")
                Auto_select_Scale(Count_Scale, "1024", "1000")
                Auto_select_Scale(Count_Scale, "2048", "2800")

        elif self.Dispersion_Mode.currentText() == "Incoherent":
            if Band_Width_Item == "100":
                Auto_select_Scale(Count_Scale, "512", "4000")
                Auto_select_Scale(Count_Scale, "1024", "4000")
                Auto_select_Scale(Count_Scale, "2048", "4000")
                Auto_select_Scale(Count_Scale, "4096", "4000")
                Auto_select_Scale(Count_Scale, "8192", "600")

            elif Band_Width_Item == "200":
                Auto_select_Scale(Count_Scale, "1024", "1000")
                Auto_select_Scale(Count_Scale, "2048", "1300")
                Auto_select_Scale(Count_Scale, "4096", "500")
                Auto_select_Scale(Count_Scale, "8192", "1000")

            elif Band_Width_Item == "800":
                Auto_select_Scale(Count_Scale, "32", "10000")
                Auto_select_Scale(Count_Scale, "64", "10000")
                Auto_select_Scale(Count_Scale, "128", "12500")
                Auto_select_Scale(Count_Scale, "256", "5000")
                Auto_select_Scale(Count_Scale, "512", "10000")
                Auto_select_Scale(Count_Scale, "1024", "5000")
                Auto_select_Scale(Count_Scale, "2048", "10000")
                Auto_select_Scale(Count_Scale, "4096", "5000")
                Auto_select_Scale(Count_Scale, "8192", "10000")

            elif Band_Width_Item == "1500":
                Auto_select_Scale(Count_Scale, "32", "13500")
                Auto_select_Scale(Count_Scale, "64", "65000")
                Auto_select_Scale(Count_Scale, "128", "13500")
                Auto_select_Scale(Count_Scale, "256", "6500")
                Auto_select_Scale(Count_Scale, "512", "13500")
                Auto_select_Scale(Count_Scale, "1024", "6500")
                Auto_select_Scale(Count_Scale, "2048", "13500")
                Auto_select_Scale(Count_Scale, "4096", "6500")
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
        Config_dict['deltafreq'] = "0.0"

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

        Rcvr_Dict = {"L-Band (Rcvr1_2)": "Rcvr1_2", "S-Band (Rcvr2_3)": "Rcvr2_3",
                     "C-Band (Rcvr4_6)": "Rcvr4_6", "X-Band (Rcvr8_10)": "Rcvr8_10"}
        rcvr = self.Receiver_Names.currentText()
        ddmode = self.Dispersion_Mode.currentText()
        bw = self.Band_Width.currentText()
        nchan = self.Nchan.currentText()
        nwin = 1
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
