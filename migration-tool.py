import PySimpleGUI as sg
import csv
import shutil

sg.theme('DarkAmber')


event, values = sg.Window('S Drive Migration Tool',
                [[sg.Text('CSV Location:')],
                [sg.In(), sg.FileBrowse()],
                [sg.Text('Log Directory:')],
                [sg.In(), sg.FolderBrowse()],
                [sg.Text('Robocopy Script Location:')],
                [sg.In(), sg.FolderBrowse()],
                [sg.Button("Export Script!")]]).read(close=True)
inputfile = values[0]
logpath = values[1]
scriptpath = values[2]

if event == sg.WIN_CLOSED or event == 'Quit':
    exit
elif not inputfile or not logpath or not scriptpath:
    sg.popup("Cancelled.", "Missing field(s).")
    raise SystemExit("ERROR!")
else:
    # saving double quotes into a variable for readability
    dq = '"'
    # these are the flags added to the end of the robocopy output, logs is incomplete because we append to its name something we can reference later
    flags = ' /e /mt:8 /r:1 /w:1 /v /TEE /ETA /FP /LOG+:' + logpath

    outfilename = inputfile.replace(".csv", ".cmd")

    # reads csv into a variable
    with open(inputfile) as dbfile:
        reader = csv.reader(dbfile)
        database = list(reader)

    # range(start, stop, step)
    for i in range(0, len(database)):
        # logs do not like having spaces in their name, so those have been removed
        logname = database[i][1].rsplit('\\', 1)[-1]
        logname = logname.replace(" ","")
        logname = '/' + logname
        # this crazy thing below writes a whole robocopy script to one variable. line by line: robocopy.exe "source" "destination" flags+logname
        output = 'robocopy.exe ' + dq + database[i][0] + dq + ' ' + dq + database[i][1] + dq + flags + logname + '_' + str(i+1) + '_log.txt' + "\n"
        # visual feedback is nice
        print(output)
        # prints the robocopy scripts to output.cmd
        with open(outfilename, 'a') as outfile:
            outfile.write(output)

    #pauses at the end so the cmd window doesn't
    with open(outfilename, 'a') as outfile:
            outfile.write('pause')
    
    #moves robocopyscript to destination
    shutil.move(outfilename, scriptpath)
    sg.popup("Complete. Robocopy script can be found at: "+scriptpath)
    raise SystemExit("Complete.")