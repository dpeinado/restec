import gtk
import time
from timeclock.defs import *

__all__ = ['Punch']

class Punch(object):
    def __init__(self):
        builder = gtk.Builder()
        builder.add_from_file(UI_DIR + 'punch.ui')
        builder.connect_signals(self)
        self.win = builder.get_object('window1')
        self.win.set_modal(True)
        self.who = builder.get_object('who')
        self.when = builder.get_object('when')
        self.what = builder.get_object('what')
        self.comment = builder.get_object('comment')
        
    def run(self, pown, pid):
        self.owner = pown
        self.now = time.localtime()
        cur = db().cursor()
        #print "id {0} owner {1}".format(pid,pown)
        cur.execute('''UPDATE print SET print_trials = print_trials+1
WHERE print_owner = ?''',
                    (pown,))
        cur.execute('''UPDATE print SET print_hits = print_hits+1
WHERE print_id = ?''', (pid,))
        cur.execute('''DELETE FROM print
WHERE print_trials > 36 AND print_hits*1.0/print_trials < .05''')
        db().commit()

        self.prev_what = DEPART_CODE

        cur.execute('''SELECT punch_when, punch_what FROM punch
WHERE punch_who = ?
ORDER BY punch_when DESC LIMIT 1''', (pown,))
        prev = cur.fetchone()
        if prev:
            prev_when = time.strptime(prev['punch_when'], '%Y-%m-%dT%H:%M')
            if (prev_when.tm_year == self.now.tm_year and
                prev_when.tm_yday == self.now.tm_yday):
                self.prev_what = prev['punch_what']

        if self.prev_what == DEPART_CODE:
            self.what.set_text('Arrive')
        else:
            self.what.set_text('Depart')

        cur.execute('select name from person where id = ?', (pown,))
        self.who.set_text(cur.fetchone()['name'])
        self.when.set_text(time.strftime('%I:%M %p', self.now))
        self.comment.set_text('')
        self.win.show()

    def on_record_clicked(self, ign):
        cur = db().cursor()
        tm = time.strftime('%Y-%m-%dT%H:%M', self.now)
        if self.prev_what == ARRIVE_CODE:
            what = DEPART_CODE
        else:
            what = ARRIVE_CODE
        cur.execute('''
insert into punch (punch_who, punch_when, punch_what, punch_comment)
values (?,?,?,?)''', (self.owner, tm, what, self.comment.get_text()))
        db().commit()
        self.win.hide()

    def on_cancel_clicked(self, ign):
        self.win.hide()

    def on_window1_delete_event(self, ign1, ign2):
        self.win.hide()
        return True
