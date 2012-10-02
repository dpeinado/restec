import time
import pyfprint
import gtk
import glib
import random
from timeclock.defs import *

__all__ = ['insert_scan', 'detect_printreader', 'safe_enroll', 'identify_finger',
           'enable_simulation']

FingerDevice = None
Fake = False

def enable_simulation():
    global Fake
    Fake = True

def insert_scan(owner, fp, img):
    cur = db().cursor()
    cur.execute('INSERT INTO print (print_owner, print_data, print_minutiae) VALUES (?,?,?)',
                            (owner, buffer(fp.data()), len(img.minutiae())))

def done_waiting():
    gtk.main_quit()
    return False

def _find_printreader():
    global FingerDevice
    dialog = None
    while not FingerDevice:
        devs = pyfprint.discover_devices()
        if len(devs) == 0:
            if not dialog:
                msg = 'Fingerprint scanner not found'
                dialog = gtk.MessageDialog(type = gtk.MESSAGE_WARNING,
                                           message_format = msg)
                dialog.set_modal(True)
                dialog.show()
        else:
            FingerDevice = devs[0]
            break
        glib.timeout_add_seconds(1, done_waiting)
        gtk.main()

    FingerDevice.open()
    if not FingerDevice.supports_identification():
        raise "Device cannot do identification"
    #print "Found a " + FingerDevice.driver().full_name()
    if dialog:
        dialog.hide()
        dialog.destroy()

# TODO: ought to use a context manager for this
def detect_printreader():
    global FingerDevice
    if not FingerDevice:
        _find_printreader()
    return FingerDevice

def safe_enroll():
    scanner = detect_printreader()
    fp = None
    try:
        fp, img = scanner.enroll_finger()
    except:
        pass
    return fp, img

def identify_finger(gallary):
    global Fake
    if Fake:
        n = random.randint(0, len(gallary)-1)
        fp = gallary[n]
    else:
        scanner = detect_printreader()
        n, fp, img = scanner.identify_finger(gallary)
    return n, fp
