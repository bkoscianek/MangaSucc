import base_func as bf
import web_func as wf
import PySimpleGUI as sg

rows = []
rows.append([sg.Text("Enter manga name:")])
rows.append([sg.Input(do_not_clear=True, key='_MANGA_NAME_'), sg.Button('SEARCH')])
rows.append([])
rows.append([sg.Text("Select your manga:")])
rows.append(
    [sg.Listbox(values=[], size=(30, 5), key='_MANGAS_', select_mode='single'), sg.Button('NEXT')])
rows.append([sg.OK()])

layout = rows

app = sg.Window('MangaSucc').Layout(layout).Finalize()

while True:
    event, values = app.Read()

    if event is None:
        break
    elif event == 'SEARCH':
        manga = wf.search_for_manga(values['_MANGA_NAME_'])
        app.FindElement('_MANGAS_').Update(values=manga.keys())
        app.Refresh()
    elif event == 'NEXT':
        choice = app.FindElement('_MANGAS_')

    event, values = app.Read()
    print(values)

app.Close()

chapters = wf.get_chapters(manga)
chapters = wf.get_list_of_chapters(chapters, 'first', 'last')
wf.download_chapters(chapters)
