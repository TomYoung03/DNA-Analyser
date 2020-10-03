from DNA_GUI import GUI
from DNA import DNA,DNA_exceptions
import PySimpleGUI as sg
from datetime import datetime
import PIL.Image
import io
import base64

def convert_to_bytes(file_or_bytes, resize=None):
    #Function copied from PysimpleGUI website
    '''
    Will convert into bytes and optionally resize an image that is a file or a base64 bytes object.
    Turns into  PNG format in the process so that can be displayed by tkinter
    :param file_or_bytes: either a string filename or a bytes base64 image object
    :type file_or_bytes:  (Union[str, bytes])
    :param resize:  optional new size
    :type resize: (Tuple[int, int] or None)
    :return: (bytes) a byte-string object
    :rtype: (bytes)
    '''
    if isinstance(file_or_bytes, str):
        img = PIL.Image.open(file_or_bytes)
    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = PIL.Image.open(dataBytesIO)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize((int(cur_width*scale), int(cur_height*scale)), PIL.Image.ANTIALIAS)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()

def update_function(new_function):
    global function
    program.window["function_display"].update("Function: "+ new_function)
    function = new_function

def notify_popup(message_text,good):
    '''
    Produces a notification on screen
    :param message_text: Text for notification
    :param good: if good == True then shows a green tick else shows a red cross
    :return: None
    '''
    assert type(message_text) == str
    assert type(good) == bool
    if good:
        sg.popup_notify(message_text, icon=GREEN_TICK, location=(CENTER_X, CENTER_Y), fade_in_duration=0)
    else:
        sg.popup_notify(message_text, icon=RED_X, location=(CENTER_X, CENTER_Y), fade_in_duration=0)

#GUI values
program = GUI("DNA Program")
sequence_1_input = False
sequence_1 = None
sequence_2 = None
sequence_2_input = None
function = None

#Screen dimensions:
SCREEN_X, SCREEN_Y =program.window.GetScreenDimensions()
CENTER_X, CENTER_Y = SCREEN_X // 2, SCREEN_Y // 2

#Icons:
RED_X = convert_to_bytes("Images/red_x.png", resize=(50, 55))
GREEN_TICK = convert_to_bytes("Images/green_tick.png", resize=(50, 55))

while True:

    event,values = program.window.read()

    # Stops program if X button is clicked
    if event == sg.WIN_CLOSED or event == "Exit":
        break

    #File events:
    if event == "Clear":
        program.window["output"].update("")

    if event == "Save":
        #Gets text from output
        output_text = program.window["output"].Get()
        #Gets current time and formats
        now = datetime.now()
        time = now.strftime("%H.%M.%S")

        #Opens DNA_results file with time and writes contents of output
        file_name = str("DNA_results " + time)
        file = open(file_name,"w")
        file.write(output_text)
        file.close()

    if event == "Save as":
        try:
            #Popup that allows user to browse files
            file_name = sg.popup_get_file("Select a file")

            output_text = program.window["output"].Get()
            file = open(file_name, "w")
            file.write(output_text)
            file.close()
            notify_popup("File saved as: "+ file_name,True)
        except:
            notify_popup("No file name given",False)

    if event == "Enable debugging" or event == "Disable debugging":
        if not program.debug_mode :
            program.debug_mode = True
            program.window["menu"].update([["File",["Save","Save as","Clear","Disable debugging"]],
                                     ["Functions",["Format","Produce information","Reverse compliment","Sequence search","Translate"]]])
            notify_popup("Debugging Enabled",True)
        else:
            program.debug_mode = False
            program.window["menu"].update([["File",["Save","Save as","Clear","Enable debugging"]],
                                     ["Functions",["Format","Produce information","Reverse compliment","Sequence search","Translate"]]])
            notify_popup("Debugging Disabled",False)

    #Function events:
    if event == "Format":
        update_function("Format")

    if event == "Produce information":
        update_function("Produce information")

    if event == "Reverse compliment":
        update_function("Reverse compliment")

    if event == "Sequence search":
        update_function("Sequence search")

    if event == "Translate":
        update_function("Translate")

    if event == "Mutate codon":
        if values["RNA_box"]:
            notify_popup("Does not work with RNA please disable RNA mode",False)
        else:
            update_function("Mutate codon")
            program.window["mut_col"].update(visible = True)
            program.window["RNA_box"].update(disabled = True)
    elif function != "Mutate codon":
        program.window["mut_col"].update(visible=False)
        program.window["RNA_box"].update(disabled=False)

    if event == "Sequence search":
        update_function("Sequence search")
        program.window["sequence_2_text"].update("Sequence to search for")
        program.window["sequence_2_text"].update(visible = True)
        program.window["sequence_2"].update(visible = True)

    elif function != "Sequence search":
        program.window["sequence_2_text"].update(visible=False)
        program.window["sequence_2"].update(visible=False)

    #Triggers whatever function is selected
    if event == "go":
        program.debug("Go button pressed")
        # Gets the value of sequence 1 input box unless empty
        if values["sequence_1"] != "":
            try:
                RNA_mode = values["RNA_box"]
                sequence_1 = DNA(values["sequence_1"]) if not RNA_mode else DNA(values["sequence_1"], RNA=True)
                sequence_1_input = True
            except DNA_exceptions as e:
                notify_popup(e.message, False)
            except:
                notify_popup("Unknown Error", False)
        else:
            sequence_1_input = False
        # Gets the value of sequence 2 input box unless empty
        if values["sequence_2"] != "":
            try:
                RNA_mode = values["RNA_box"]
                sequence_2 = DNA(values["sequence_2"]) if not RNA_mode else DNA(values["sequence_2"], RNA=True)
                sequence_2_input = True
            except DNA_exceptions as e:
                notify_popup(e.message, False)
            except:
                notify_popup("Unknown Error", False)
        else:
            sequence_2_input = False

        if sequence_1_input:
            if function == "Format":
                print(sequence_1.formatted_sequence)
                sequence_1 = None

            if function == "Produce information":
                print(sequence_1.full_info())
                sequence_1 = None

            if function == "Reverse compliment":
                print(sequence_1.reverse_comp_sequence)
                sequence_1 = None

            if function == "Translate":
                print(sequence_1.translate())
                sequence_1 = None

            if function == "Sequence search" and sequence_2_input == True:
                print(sequence_1.sequence_search(sequence_2))
                sequence_1 = None
                sequence_2 = None

            if function == "Mutate codon":
                    AA_location = int(values["AA_location"])-1
                    new_AA = values["AA_box"]
                    if AA_location > len(sequence_1)-2:
                        notify_popup("Location out of range",False)
                    else:
                        print(sequence_1.modify(new_AA,AA_location))

program.debug("Program closed")







