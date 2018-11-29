import web_func as wf
import base_func as bf



bf.get_to_dnl_folder()
manga = wf.search_for_manga()
chapters = wf.select_chapters(manga)
wf.download_chapters(chapters)