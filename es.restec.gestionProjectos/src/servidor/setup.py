# -*- coding: UTF-8 -*-
from distutils.core import setup
import py2exe

setup(name="TrackProjectsServer",
      version="0.1",
      author="Diego Peinado Mart�n",
      author_email="dpeinad@gmail.com",
      license="GNU General Public License (GPL)",   
      windows=[{"script": "TrackProjectsServer.pyw"}],
      options={"py2exe": {"skip_archive": True, "includes": ["sip"]}})