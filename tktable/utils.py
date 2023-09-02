# pylint: disable=missing-module-docstring, protected-access

import tkinter


def _setup_master(master):
    if master is None:
        if tkinter._support_default_root:
            master = tkinter._default_root or tkinter.Tk()
        else:
            raise RuntimeError(
                "No master specified and Tkinter is "
                "configured to not support default master"
            )
    return master
