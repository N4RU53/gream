#config: utf-8

'''
[pyinstaller install command]
pyinstaller main.py --onefile --name GREAM --icon data\image\n4ru53_alpha_2_red.png --noconsole --clean

'''

'''
GREAM -- GREEN TERMINAL

Copyright (c) 2022 N4RU53
Released under the MIT license
https://opensource.org/licenses/mit-license.php

'''


import subprocess
import PySimpleGUI as sg
from PIL import Image, ImageTk
import io

import threading
import time



#======================== Define functions ==========================
def make_dpi_aware():
  import ctypes
  import platform
  if int(platform.release()) >= 8:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
make_dpi_aware()



def get_img(path=r'data\image\n4ru53_alpha_2_red.png', maxsize=(380,360), first=False):

    img = Image.open(path)
    img.thumbnail(size=maxsize)
    if first:
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()

    return ImageTk.PhotoImage(img)



def command(text):

    global helps, task_update_flag, prompt, shell_flag, command_list

    print(text)
    window['-INPUT-'].update('')

    if text == 'exit':
        window.close()


    elif text == 'help':
        print(' ===================================================================')
        print('   **** helps for commands ****')
        for commands in command_list:
            print(' ' + commands, end='\n\n')
        print(' ===================================================================')
    

    elif text == 'taskswitch':
        task_update_flag = not task_update_flag
        window['-TASK_TITLE-'].update('      -- TASK LIST --      UPDATE = ' + str(task_update_flag))
        print(f' task_update switchd {task_update_flag}')


    elif text == 'shell':
        shell_flag = True
        print(subprocess.run('chdir', shell=True, stdout=subprocess.PIPE, text=True).stdout.split('\n', 1)[0] + ' ', end='')


    elif text == '':
        pass

    else:
        print(' Invalid Command. Type help to check commands.\n')

    print(' ' + prompt + '  ', end='')



def tasklist():
    global task_update_flag
    while task_update_flag == True:
        window['-TASKS-'].update(subprocess.run('tasklist', shell=True, stdout=subprocess.PIPE).stdout.decode('shift-jis').rsplit('=', 1)[1])
        time.sleep(1)



def shell(text):
    global shell_flag
    print(text)
    window['-INPUT-'].update('')
    try:
        sh = subprocess.run(text, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        print(sh.stdout)
    except:
        pass
    finally:
        print(' ' + prompt + '  ', end='')
        shell_flag = False



#==========================================MAIN================================================
# define Variables
task_update_flag = True
shell_flag = False

prompt = '>>>'

IF_green = '#54fa33'

command_dic = {
                'help':'check command list and how to',
                'taskswitch':'switch tasklist update mode',
                'shell':'you can use shell command',
                'exit':'close this window',
              }

command_list = [command + ' - ' + command_dic[command] for command in command_dic.keys()]



#-------------------------------- define layout ------------------------------------

right_col = sg.Frame('',
                     [
                        [sg.Text('      -- TASK LIST --      UPDATE = ' + str(task_update_flag),
                                font=('Arial',16),
                                text_color=IF_green,
                                background_color='black',
                                expand_x=True,
                                pad=((3,3),(3,1)),
                                key='-TASK_TITLE-'
                                )],

                        [sg.Multiline('',
                                      key='-TASKS-',
                                      background_color='black',
                                      text_color=IF_green,
                                      sbar_background_color=IF_green,
                                      sbar_frame_color=IF_green,
                                      sbar_trough_color='black',
                                      no_scrollbar=True,
                                      expand_y=True,
                                      expand_x=True,
                                      pad=((2,2),(2,2))
                                     )],

                        [sg.Text('      -- COMMAND LIST -- ',
                                font=('Arial',15),
                                text_color=IF_green,
                                background_color='black',
                                expand_x=True,
                                pad=((3,3),(1,1)),
                                key='-TASK_TITLE-'
                                )],

                        [sg.Listbox(command_list,
                                    key='-TASKMENU-',
                                    font=('Arial',11),
                                    background_color='black',
                                    text_color=IF_green,
                                    sbar_background_color=IF_green,
                                    sbar_frame_color=IF_green,
                                    sbar_trough_color='black',
                                    no_scrollbar=True,
                                    expand_x=True,
                                    size=(1,13),
                                    pad=((2,2),(2,2))
                                    )],

                        [sg.Button('APPLY',
                                font=('Arial',12),
                                button_color='black',
                                expand_x=True,
                                use_ttk_buttons=True,
                                mouseover_colors=('black','white'),
                                key='-APPLY-',
                                pad=((2,2),(2,2))
                                )],
                     ],
                     key='-RIGHT-',
                     background_color=IF_green,
                     pad=((0,0),(30,30)),
                     size=(480,1),
                    )


term = sg.Frame('',
                [
                    [sg.Text('      -- COMMAND_LINE AND STDOUT --  ',
                             font=('Arial',16),
                             text_color=IF_green,
                             background_color='black',
                             expand_x=True,
                             pad=((3,3),(3,1))
                             )],

                    [sg.Output(key='-OUTPUT-',
                               pad=((2,2),(2,2)),
                               text_color=IF_green,
                               background_color='black',
                               sbar_background_color=IF_green,
                               sbar_frame_color=IF_green,
                               sbar_trough_color='black',
                               sbar_width=1,
                               echo_stdout_stderr=True
                               )],
                               
                    [sg.Text('  INPUT >>> ', font=('Arial',12), background_color='black'),
                     sg.Input(key='-INPUT-',
                              expand_x=True,
                              focus=True,
                              background_color='black',
                              text_color=IF_green
                              )]
                    ],
                    key='-TERM-',
                    background_color=IF_green,
                    pad=((0,0),(30,30))
                )


layout = [  [sg.Text(' ',
                     size=(0,1),
                     background_color='#c70000',
                     pad=((0,0),(0,0)),
                     expand_x=True)],

            [sg.Image(data=get_img(first=True),
                      background_color='black',
                      pad=((20,0),(250,0))),
             term,
             right_col
            ],

            [sg.Text(' ',
                     size=(0,1),
                     background_color=IF_green,
                     expand_x=True)]
         ]




#--------------------------------- Generate window ---------------------------------------
window = sg.Window('GRERM',
                   layout,
                   size=(835,690),
                   background_color='black',
                   resizable=True,
                   keep_on_top=False,
                   no_titlebar=True
                  ).Finalize()

window.maximize()

window['-RIGHT-'].expand(expand_x=False, expand_y=True)
window['-TERM-'].expand(expand_x=True, expand_y=True)
window['-OUTPUT-'].expand(expand_x=True, expand_y=True)
window['-INPUT-'].bind("<Return>", "_Enter")


print(''' #############################################################

       GREAM by N4RU53.
       Version 0.0.1 all right reserved.

 #############################################################\n
 Type \'help\' to refer command list.\n\n''')
print(' ' + prompt + '  ', end='')



threading.Thread(target=tasklist, daemon=True).start()

#------------------------------------- Main roop ------------------------------------------
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    elif event == '-INPUT-' + '_Enter':
        if shell_flag == False:
            command(values['-INPUT-']) 
        else:
            shell(values['-INPUT-'])

    elif event == '-APPLY-':
        if shell_flag == False:
            command(str(values['-TASKMENU-']).split(' ', 1)[0].split('\'')[1])
        else:
            continue
        

window.close()