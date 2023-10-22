from flask import Flask, render_template
from joplin_wiki import appbase
from datetime import date, timedelta
from loguru import logger
import marko

import time

def load_notes():
    global next_date
    date_str = next_date.strftime("%Y%m%d")
    next_date = next_date - timedelta(days=1)
    logger.error(f"load date {date_str}")
    for note in appbase.all_notes(f"updated:{date_str}"):
        note.fetch()
        ui.html(f"<h1>{note.data.title}</h1>")
        ui.markdown(note.data.body)
        ui.html(f"<br/>")

def load_all_notes(index):
    notes = list(appbase.all_notes(index))
    for note in notes:
        note.fetch()
        if note.data.markup_language == 1:
            note.pyhtml = marko.convert(note.data.body)
        else:
            note.pyhtml = f"<a href=/html/{note.rid}>Content</a>"

    logger.debug( notes )

    return notes

        #  ui.html(f"<h1>{note.data.title}</h1>")
        #  ui.label(f"{note.data.markup_language}")
        #  if note.data.markup_language == 1:
            #  ui.markdown(note.data.body)
        #  else:
            #  ui.link("html", f"/html/{note.rid}")
        #  ui.html(f"<br/>")

    #  ui.link("Next", f"/{next_page+1}")


app = Flask(__name__)

@app.get("/")
@app.get("/<int:index>")
def index(index:int=1):
    return render_template('note.html', notes=load_all_notes(index), index=index)

@app.get("/html/<rid>")
def html_note(rid):
    return appbase.fetch_note_by_id(rid).data.body

@app.get("/html/:/<rid>")
def note_resource(rid):
    logger.debug(f"fetch resource {rid}")
    return appbase.fetch_resource_file_by_id(rid)
