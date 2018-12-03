import PySimpleGUI as sg

import base_func as bf
import web_func as wf

rows = []
rows.append([sg.Text("Enter manga name:")])
rows.append([sg.Input(do_not_clear=True, key='_MANGA_NAME_'), sg.Button('SEARCH')])
rows.append([])
rows.append([sg.Text("Select your manga:")])
rows.append(
    [sg.Listbox(values=[], size=(30, 5), key='_MANGAS_', select_mode=sg.SELECT_MODE_SINGLE), sg.Button('NEXT')])
rows.append([sg.Text('Select a single chapter or first and last chapter that you want to download:')])
rows.append(
    [sg.Listbox(values=[], size=(30, 5), key='_CHAPTERS_', select_mode=sg.SELECT_MODE_EXTENDED), sg.Button('DOWNLOAD')])

layout = rows

manga = {}
chapters = {}

app = sg.Window('MangaSucc').Layout(layout).Finalize()

while True:
    event, values = app.Read()

    if event is None:
        break
    elif event == 'SEARCH':
        manga = wf.search_for_manga(values['_MANGA_NAME_'])
        app.FindElement('_MANGAS_').Update(values=list(manga.keys()))
        app.Refresh()
    elif event == 'NEXT':
        choice = values['_MANGAS_']
        choice = choice[0]

        chapters = wf.get_chapters(manga[choice])
        app.FindElement('_CHAPTERS_').Update(values=list(chapters.keys()))
        app.Refresh()
    elif event == 'DOWNLOAD':
        first_chapter = values['_CHAPTERS_'][1]
        last_chapter = values['_CHAPTERS_'][0]
        chapters_to_dnl = wf.get_list_of_chapters(chapters, first_chapter, last_chapter)

        manga_choice = str(choice)
        bf.get_to_manga_folder(manga_choice)
        wf.download_chapters(chapters_to_dnl)
        app.Refresh()

    print(values)

app.Close()
