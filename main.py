import base_func as bf
import web_func as wf
import PySimpleGUI as sg

# rows = []
# rows.append([sg.Text("Enter manga name:")])
# rows.append([sg.Input(do_not_clear=True), sg.OK()])
#
# layout = rows
#
# app = sg.Window('example').Layout(layout)
#
# while True:
#     event, val = app.Read()
#     if event is None:
#         break
#     print(val)
#
# app.close()

manga = wf.search_for_manga()
chapters = wf.get_chapters(manga)
chapters = wf.get_list_of_chapters(chapters, 'first', 'last')
wf.download_chapters(chapters)