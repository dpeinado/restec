# -*- coding: UTF-8 -*-
from distutils.core import setup
import py2exe

setup(name="TrackProjectsClient",
      version="2.0",
      author="Diego Peinado Martín",
      author_email="dpeinad@gmail.com",
      license="GNU General Public License (GPL)",      
      windows=[{"script": "MainForm.pyw"}],
      options={"py2exe": {"skip_archive": True, "includes": ["sip"]}})