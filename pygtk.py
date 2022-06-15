from dotenv import load_dotenv
import os
import pyttsx3
from gi.repository import Gtk, Pango
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import LanguageTranslatorV3
import gi
gi.require_versions({
    'Gtk':  '3.0',
    'Wnck': '3.0',
    'Gst':  '1.0',
    'AppIndicator3': '0.1',
})

load_dotenv()
gi.require_version('Gtk', '3.0')
win = Gtk.Window()
maingrid = Gtk.Grid()
win.set_icon_from_file("web.png")
win.set_title("Translator")
win.add(maingrid)
win.border_width = 50
a = ""
text1 = ""


def SpeakText(widget):
    engine = pyttsx3.init()
    engine.setProperty("rate", 135)
    engine.say(text1)
    engine.runAndWait()
    engine.stop()


def onclickedbutton(widget):
    global text1
    text1 = Gtk.Entry.get_text(entry1)
    text2 = Gtk.Entry.get_text(entry2)
    if text2 == "":
        text2 = "en-ta"
    # print(text1,text2)

    # button1.connect("clicked",SpeakText)
    authenticator1 = IAMAuthenticator(os.environ.get("authenticator"))
    language_translator = LanguageTranslatorV3(
        version='2018-05-01', authenticator=authenticator1)
    language_translator.set_service_url(os.environ.get("web"))
    translation = language_translator.translate(
        text=text1, model_id=text2).get_result()
    global a
    a = translation["translations"][0]["translation"]
    # print(a)
    b = ''''''
    ky = 0
    while (ky < len(a)):
        for i in a:
            if (ky % 100 == 0):
                b += '\n'
            b += i
            ky += 1
    textbuffer.set_text(b)


label1 = Gtk.Label.new_with_mnemonic("Text ")
maingrid.attach(label1, 0, 0, 1, 1)
entry1 = Gtk.Entry()
maingrid.attach(entry1, 1, 0, 1, 1)
entry1.set_width_chars(50)
label2 = Gtk.Label.new_with_mnemonic("Language ")
maingrid.attach(label2, 0, 1, 1, 1)
entry2 = Gtk.Entry()
maingrid.attach(entry2, 1, 1, 1, 1)
entry2.set_width_chars(20)
button = Gtk.Button(label="Done! ")
button.connect("clicked", onclickedbutton)
maingrid.attach(button, 3, 0, 1, 1)
# result=Gtk.Box()
button1 = Gtk.Button(label="Speak! ")
button1.connect("clicked", SpeakText)
maingrid.attach(button1, 3, 1, 1, 1)
label3 = Gtk.Label.new_with_mnemonic("\nTranslated Text ")
maingrid.attach(label3, 0, 2, 1, 1)
# maingrid.attach(result,1,2,1,1)
# result.set_width_chars(125)
scrolledwindow = Gtk.ScrolledWindow()
scrolledwindow.set_hexpand(True)
scrolledwindow.set_vexpand(True)
maingrid.attach(scrolledwindow, 1, 2, 1, 1)
textview = Gtk.TextView()
textbuffer = textview.get_buffer()

scrolledwindow.add(textview)
tag_bold = textbuffer.create_tag("bold", weight=Pango.Weight.BOLD)
tag_italic = textbuffer.create_tag("italic", style=Pango.Style.ITALIC)
tag_underline = textbuffer.create_tag(
    "underline", underline=Pango.Underline.SINGLE
)
tag_found = textbuffer.create_tag("found", background="yellow")
win.set_default_size(1920, 1080)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
