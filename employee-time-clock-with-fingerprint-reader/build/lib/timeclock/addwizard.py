import gtk
import time
import pyfprint
from timeclock.defs import *
from timeclock.fprint import *

__all__ = ['AddWizard']

class AddWizard(object):
    def __init__(self):
        builder = gtk.Builder()
        builder.add_from_file(UI_DIR+'add_wizard.ui')
        self.win = builder.get_object('assistant1')
        self.win.set_modal(True)
        self.wiz_entry = builder.get_object('wiz_name_entry')
        self.add_scan_button = builder.get_object('wiz_add_scan_button')
        self.scan_status = builder.get_object('wiz_scan_status')
        self.confirm_name = builder.get_object('wiz_confirm_name')
        self.confirm_scans = builder.get_object('wiz_confirm_scans')
        builder.connect_signals(self)

    def show(self):
        self.fprint = []
        self.win.set_current_page(0)
        self.scan_status.set_text("0 scans completed")
        self.add_scan_button.set_sensitive(True)
        self.wiz_entry.set_text('')
        self.win.set_page_complete(self.win.get_nth_page(1), False)
        self.win.set_page_complete(self.win.get_nth_page(2), True)
        self.wiz_entry.grab_focus()
        self.win.show()

    def validate_new_name(self, ign):
        name = self.wiz_entry.get_text()
        self.win.set_page_complete(self.win.get_nth_page(0),
                                   len(name) != 0)

    def cancel(self, ign):
        self.win.hide()

    def go(self, ign):
        cur = db().cursor()
        try:
            cur.execute('insert into person(name) values (?)',
                        (self.wiz_entry.get_text(),))
            id = cur.lastrowid
            for x in self.fprint:
                insert_scan(id, x[0], x[1])
            db().commit()
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])
        self.win.hide()

    def add_scan(self, ign):
        fp, img = safe_enroll()
        pl = self.fprint
        if isinstance(fp, pyfprint.Fprint):
            pl.append((fp,img))
            self.scan_status.set_text("{0} scans completed" . format(len(pl)))
            self.confirm_scans.set_text("{0}" . format(len(pl)))
        self.win.set_page_complete(self.win.get_nth_page(1),
                                   len(pl) >= 3)
        self.add_scan_button.set_sensitive(len(pl) < 8)
        self.confirm_name.set_text(self.wiz_entry.get_text())
