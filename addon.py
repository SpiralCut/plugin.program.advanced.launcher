"""
    Plugin for Launching programs
"""

# -*- coding: UTF-8 -*-
# main imports
import sys
import os

# plugin constants
__plugin__ = "Advanced Launcher"
__author__ = "Angelscry"
__url__ = "http://sourceforge.net/projects/advlauncher/"
__git_url__ = "http://sourceforge.net/p/advlauncher/git/?source=navbar"
__credits__ = "Leo212 CinPoU, JustSomeUser, Zerqent, Zosky, Atsumori, SpiralCut"
__version__ = "1.13.2"

if ( __name__ == "__main__" ):
    import resources.lib.launcher_plugin as plugin
    plugin.Main()

