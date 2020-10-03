import PySimpleGUI as sg
from datetime import datetime

class GUI:

    def __init__(self,program_name):



        self.tooltips = {}

        self.amino_acid_list = sorted(["I","T","M","S","L","P","H","R","V","D","G","F","Y","C","A","Q","E","M","W","STOP"])

        self.lines = {   1:[sg.Menu([["File",["Save","Save as","Clear","Enable debugging"]],
                                     ["Functions",["Format","Produce information","Reverse compliment","Sequence search","Translate","Mutate codon"]]],
                                    key= "menu")],
                         2:[sg.Text("Function: None selected ",key= "function_display",size= (50,0))],
                         3:[sg.Text("Sequence:")],
                         4:[sg.InputText(key= "sequence_1"),sg.Checkbox("RNA",key= "RNA_box")],
                         5:[sg.Text("",key="sequence_2_text",visible= False, size= (50,0)),
                            self.place([sg.T("Change amino acid at location: "),
                                        sg.InputText(size=(5, 20), key="AA_location"),
                                        sg.T("into amino acid: "),
                                        sg.InputCombo(self.amino_acid_list, size=(7, 0),key= "AA_box")], "mut_col", False)],
                         6:[sg.InputText(key= "sequence_2",visible= False)],
                         7:[sg.B("Go!",key = "go")],
                         8:[sg.Output(size= (50,20) ,key = "output")],
                         }

        self.layout = [self.lines[i] for i in self.lines.keys()]

        self.window = sg.Window(program_name,self.layout,)

        self.debug_mode = False

    def debug(self,debug_message):
        now = datetime.now()
        time = now.strftime("%H.%M.%S")
        if self.debug_mode:
            sg.easy_print(time + " "+ debug_message)
        else:
            pass

    def place(self,elem,key = "default",visible = True):
        return sg.Column([elem],visible= visible,key= key,pad=(0,0))