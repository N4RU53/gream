#config: utf-8

# pyinstaller main.py --onefile --name GREAM --icon data\image\n4ru53_alpha_2_red.png --noconsole --clean

# GREAM -- GREEN TERM


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

    global helps, task_update_flag, prompt, shell_flag

    print(text)
    window['-INPUT-'].update('')

    if text == 'exit':
        window.close()

    elif text == 'help':
        print(helps)
    
    elif text == 'taskswitch':
        task_update_flag = not task_update_flag
        window['-TASK_TITLE-'].update('      -- TASK LIST --      UPDATE = ' + str(task_update_flag))
        print(f'task_update switchd {task_update_flag}')

    elif text == 'shell':
        shell_flag = True
        print(subprocess.run('chdir', shell=True, stdout=subprocess.PIPE, text=True).stdout.split('\n', 1)[0] + ' ', end='')

    elif text == '':
        pass
    else:
        print(' Invalid Command. /help to check commands.\n')

    print(' ' + prompt + '  ', end='')



def tasklist():
    global task_update_flag
    while task_update_flag == True:
        window['-TASKS-'].update(subprocess.run('tasklist', stdout=subprocess.PIPE, text=True).stdout.rsplit('=', 1)[1])
        time.sleep(3)



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

helps = '''
 ===================================================================
  **** helps for commands ****

   help - check command list and how to

   exit - close this app

   taskswitch - switch tasklist update mode

 ===================================================================


'''



#-------------------------------- define layout ------------------------------------

left_col = sg.Column(
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
                                      size=(65,58),
                                      enable_events=True,
                                      background_color='black',
                                      text_color=IF_green,
                                      sbar_background_color=IF_green,
                                      sbar_frame_color=IF_green,
                                      sbar_trough_color='black',
                                      expand_y=True,
                                      expand_x=True,
                                      pad=((2,2),(2,2))
                                     )]
                     ],
                     key='-LEFT-',
                     background_color=IF_green,
                     pad=((15,20),(30,30))
                    )


term = sg.Column([
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
                    pad=((5,5),(30,30))
                )


layout = [
            [sg.Image(data=get_img(first=True),
                      background_color='black',
                      pad=((20,0),(250,0))),
             term,
             left_col
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
                   resizable=False,
                   keep_on_top=True,
                   use_custom_titlebar=True,
                   titlebar_background_color='red'
                  ).Finalize()

window.maximize()

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


window.close()