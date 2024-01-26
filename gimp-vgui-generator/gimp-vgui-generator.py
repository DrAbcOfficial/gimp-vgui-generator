#!/usr/bin/env python2

import gtk
from gimpfu import *

AUTHOR           = 'Dr.Abc'
COPYRIGHT        = AUTHOR
COPYRIGHT_YEAR   = '2024'

LOAD_PROC        = 'gimp-vgui-generator'


def caller(image, dummy):
    layers = image.layers
    resultstr = ""
    for layer in reversed(layers):
        if layer.name.find("|") < 0:
            continue
        spl = layer.name.split("|")
        name = spl[0]
        cotl = spl[1]
        resultstr += "\"" + name + "\"\n{\n\t\"ControlName\"\t\"" + cotl + "\"\n\t\"fieldName\"\t\"" + name + "\"\n"
        resultstr += "\t\"wide\"\t\"" + str(layer.width) + "\"\n"
        resultstr += "\t\"tall\"\t\"" + str(layer.height) + "\"\n"
        resultstr += "\t\"xpos\"\t\"" + str(layer.offsets[0]) + "\"\n"
        resultstr += "\t\"ypos\"\t\"" + str(layer.offsets[1]) + "\"\n"
        resultstr += "}\n"
    dialog = gtk.Dialog("Resource", None, gtk.DIALOG_MODAL, (gtk.STOCK_OK, gtk.RESPONSE_OK))
    entry = gtk.TextView()
    entry.set_wrap_mode(gtk.WRAP_WORD)
    text_buffer = entry.get_buffer()
    text_buffer.set_text(resultstr)
    dialog.get_content_area().pack_start(entry, True, True, 0)
    dialog.show_all()
    def on_dialog_close(dialog, response_id):
        dialog.destroy()
    dialog.connect("response", on_dialog_close)
    response = dialog.run()
    if response == gtk.RESPONSE_OK:
        text = entry.get_text()
        return text
    else:
        return ""

register(
    LOAD_PROC,
    'Converts the layer to vgui res',
    '',
    AUTHOR,
    COPYRIGHT,
    COPYRIGHT_YEAR,
    'VGUI res Generator',
    '*',
    [
        (PF_IMAGE, 'image', 'Input image', None),
        (PF_TOGGLE, 'dummy', 'dummy shit, no use', True)
    ],
    [(PF_STRING, 'result', 'Output string', '')],
    caller, 
    menu='<Image>/Image/Half-Life/'
)

main()
