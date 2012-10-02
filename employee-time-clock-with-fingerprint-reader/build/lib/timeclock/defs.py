import sys, os.path
from pysqlite2 import dbapi2 as sqlite3

__all__ = ['DEPART_CODE', 'ARRIVE_CODE', 'UI_DIR',
           'XDG_DATA_HOME', 'XDG_CONFIG_HOME', 'install_schema', 'db',
           'DEFAULT_LEAVE_TIME']

DEFAULT_LEAVE_TIME = 17*60

def install_schema(path):
    global DB
    if path == None:
        path = XDG_DATA_HOME + 'timeclock.db'
    DB = sqlite3.connect(path, detect_types = sqlite3.PARSE_DECLTYPES)
    DB.row_factory = sqlite3.Row
    cur = DB.cursor()
    try:
        cur.execute('select v from state where k = ?', ('version',))
        version = cur.fetchone()['v']
    except sqlite3.OperationalError:
        version = 0
    if version == 0:
        cur.execute('CREATE TABLE state (k text, v integer)')
        cur.execute('INSERT INTO state (k,v) values (?,?)', ('version',0))
        version = 1
    if version == 1:
        cur.execute('create table person (id integer primary key, name text not null)')
        cur.execute('''CREATE TABLE print (
    id integer PRIMARY KEY,
    owner integer NOT NULL,
    fp blob NOT NULL,
    trials integer NOT NULL DEFAULT 0,
    hits integer NOT NULL DEFAULT 0
)''')
        version = 2
    if version == 2:
        cur.execute('''CREATE TABLE punch (
    punch_who integer NOT NULL,
    punch_when text NOT NULL,
    punch_what text NOT NULL,
    punch_comment text
)''')
        version = 3
    if version == 3:
        cur.execute('ALTER TABLE print RENAME TO print_old')
        cur.execute('''CREATE TABLE print (
    print_id integer PRIMARY KEY,
    print_owner integer NOT NULL,
    print_data blob NOT NULL,
    print_minutiae integer,
    print_trials integer NOT NULL DEFAULT 0,
    print_hits integer NOT NULL DEFAULT 0
)''')
        cur.execute('''INSERT INTO print (print_id, print_owner,
print_data, print_trials, print_hits)
SELECT id, owner, fp, trials, hits FROM print_old''')
        cur.execute('DROP TABLE print_old')
        version = 4
    cur.execute('UPDATE state SET v = ? WHERE k = ?', (version,'version'))
    DB.commit()

def db():
    global DB
    return DB

DEPART_CODE = 'd'
ARRIVE_CODE = 'a'

UI_DIR = os.path.dirname(__file__) + '/ui/'

# From pyxdg
_home = os.environ.get('HOME', '/')
XDG_DATA_HOME = os.environ.get('XDG_DATA_HOME',
            os.path.join(_home, '.local', 'share')+'/')
XDG_CONFIG_HOME = os.environ.get('XDG_CONFIG_HOME',
            os.path.join(_home, '.config')+'/')
