from DNA import DNA
import PySimpleGUI as sg

#tooltips
reverse_comp_tooltip = "Produces the reverse compliment of the sequence"
info_tooltip = "Produces basic information about this sequence"
clear_tooltip = "Clears all data from output"
search_tooltip = "Searches for one sequence within another"
save_tooltip = "Saves all information currently in the window"

layout = [[sg.Text("DNA sequence:")],
          [sg.Input(key="DNA sequence 1"),sg.B("Info",key= "DNA_1_info",tooltip= info_tooltip),sg.B("Reverse Compliment",tooltip= reverse_comp_tooltip)],
          [sg.Text("DNA sequence to look for:")],
          [sg.Input(key= "DNA sequence 2"),sg.B("Info",key= "DNA_2_info",tooltip= info_tooltip)],
          [sg.B("Search",tooltip= search_tooltip),sg.B("Clear",tooltip= clear_tooltip ),sg.B("Save", tooltip= save_tooltip)],
          [sg.Text("File Name"),sg.Input(key ="File name input")],
          [sg.Output(size=(80,30),key = "Output")]
          ]

window = sg.Window("DNA Program",layout)
output_list = []
DNA_1,DNA_2 = None,None

while True:
    event,values = window.read()
    #true when something is in input boxes
    DNA_1_use = True if values["DNA sequence 1"] != "" else False
    DNA_2_use = True if values["DNA sequence 2"] != "" else False

    if event == sg.WIN_CLOSED or event == "Exit":
        break
    if event == "Clear":
        #clears all input and output as well as output list
        window["Output"].update("")
        output_list = []

    if event == "Save":
        if values["File name input"] == "":
            sg.popup("Please provide a file name")
        else:
            try:
                #saves all info in output list
                file_name = values["File name input"]
                file = open(file_name,"w")
                file.write("\n\n".join(output_list))
                file.close()
                sg.popup("You file has been saved!")
                #clears output window
                window["Output"].update("")
                output_list = []
            except:
                sg.popup('There was an error saving your file \n File names cannot contain: \ / ? % * : ; " | < > . , = ')


    if DNA_1_use or DNA_2_use == True:
        if DNA_1_use:
            try:
                DNA_1 = DNA(values["DNA sequence 1"])
            except:
                sg.popup("A character in your DNA sequence is not a,t,c,g")
        if DNA_2_use:
            try:
                DNA_2 = DNA(values["DNA sequence 2"])
            except:
                sg.popup("A character in your search sequence is not a,t,c,g")

        if event == "Search" and (DNA_1_use and DNA_2_use) == True:
                search = DNA_1.sequence_search(DNA_2)
                if not search:
                    sg.popup("The sequence " + str(DNA_2) + " was not found in " + str(DNA_1))
                else:
                    if search not in output_list:
                        output_list.append(search)
                    print("\n"+search)

        if event == "DNA_1_info" and DNA_1_use and DNA_1 is not None:
           print("\n"+DNA_1.full_info())
           if DNA_1.full_info() not in output_list:
               output_list.append(DNA_1.full_info())

        if event == "DNA_2_info" and DNA_2_use and DNA_2 is not None:
            if DNA_2.full_info() not in output_list:
                output_list.append(DNA_2.full_info())
            print("\n"+DNA_2.full_info())

        if event == "Reverse Compliment" and DNA_1_use:
            if "Reverse compliment:\n" + DNA_1.raw_sequence + "\n\n" + DNA_1.reverse_comp_sequence not in output_list:
                output_list.append("Reverse compliment:\n"+DNA_1.raw_sequence + "\n\n" + DNA_1.reverse_comp_sequence)
            print("\nReverse compliment:\n"+DNA_1.raw_sequence + "\n\n" + DNA_1.reverse_comp_sequence)



