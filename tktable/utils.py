# pylint: disable=protected-access

"""Internal helpers shared by the modules of this package."""

import logging
import os
import tkinter

logger = logging.getLogger(__name__)

#: Environment variable that can point to the directory containing Tktable's pkgIndex.tcl.
TKTABLE_LIBRARY_ENV_VAR = "TKTABLE_LIBRARY"


def _setup_master(master: tkinter.Misc | None) -> tkinter.Misc:
    if master is None:
        if tkinter._support_default_root:  # type: ignore[attr-defined]
            master = tkinter._default_root or tkinter.Tk()  # type: ignore[attr-defined]
        else:
            raise RuntimeError(
                "No master specified and Tkinter is configured to not support default master"
            )
    return master


def _bundled_library() -> str | None:
    """The folder of the Tktable of pytktable-binaries, if that package is installed."""
    try:
        # pylint: disable-next=import-outside-toplevel
        import tktable_binaries
    except ImportError:
        return None
    return str(tktable_binaries.library_dir())


def extend_auto_path(interp: tkinter.Misc) -> None:
    """Append to Tcl's ``auto_path`` of ``interp`` the folders where Tktable may be.

    These are ``$TKTABLE_LIBRARY`` (if set), and the Tktable of pytktable-binaries (if installed).
    """
    library = os.environ.get(TKTABLE_LIBRARY_ENV_VAR)
    if library:
        logger.debug("Add %s to auto_path", library)
        interp.tk.call("lappend", "auto_path", library)
    else:
        logger.debug("The environment variable %s is not defined.", TKTABLE_LIBRARY_ENV_VAR)

    bundled = _bundled_library()
    if bundled:
        logger.debug("Add the Tktable of pytktable-binaries, %s, to auto_path", bundled)
        interp.tk.call("lappend", "auto_path", bundled)


def find_tktable(interp: tkinter.Misc) -> list[str]:
    """Return the versions of Tktable that Tcl can find, without loading it.

    This does not need Tk (or a display), so it works in headless environments.
    """
    extend_auto_path(interp)
    # Requiring a non-existent package makes Tcl scan auto_path for every pkgIndex.tcl.
    interp.tk.eval("catch {package require __tktable_probe__}")
    return [str(v) for v in interp.tk.splitlist(interp.tk.call("package", "versions", "Tktable"))]


def load_tktable(master: tkinter.Misc) -> str:
    """Load the Tcl/Tk extension Tktable into the Tk interpreter of ``master``.

    :return: the version of Tktable that was loaded.
    :raise tkinter.TclError: if Tktable cannot be found or loaded.
    """
    extend_auto_path(master)
    # https://wiki.tcl-lang.org/page/package+require
    logger.debug("Require the Tcl/Tk extension Tktable.")
    return str(master.tk.call("package", "require", "Tktable"))
