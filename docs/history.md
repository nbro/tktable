# History

## Tcl/Tk

[Tcl](https://www.tcl-lang.org/) (Tool Command Language) is a programming language designed by
[John Ousterhout](https://wiki.tcl-lang.org/page/John+Ousterhout), which first appeared in
1988[^tcl]. Tk is its GUI toolkit, which Ousterhout also created: he started it in late 1988 and
[first released it publicly in 1991](https://en.wikipedia.org/wiki/Tk_(software))[^tk]. Tcl is
mainly known for Tk, so people often write Tcl/Tk.

## tkinter

Python's [`tkinter`](https://docs.python.org/3/library/tkinter.html), which stands for Tk
interface, is a wrapper around Tk. It was
[written by Steen Lumholt and Guido van Rossum](https://docs.python.org/3.9/library/tkinter.html#tkinter-life-preserver),
and in June 1994 Guido van Rossum already
[announced a new version of it](https://legacy.python.org/search/hypermail/python-1994q2/1022.html),
so it's at least from 1994[^lumholt]. Python itself is older: Guido van Rossum
[started it](https://docs.python.org/3/faq/general.html#why-was-python-created-in-the-first-place)
in December 1989 and first released it in February 1991[^python].

`tkinter` has no table widget, which is why this library exists.

## Tktable

The Tcl/Tk Tktable widget was originally created by Roland King, who
[released its first version](https://github.com/bohagan1/TkTable/commit/318b6e4249016434cce8991455d15b1686daceb0)
in 1994, as a table widget for Tk[^king]. Jeffrey Hobbs then took it over,
[released version 1.0](https://github.com/bohagan1/TkTable/commit/59d40a11bf082017865a3ae5f02d4d1f22111fc8)
in 1996[^hobbs] and maintained it for many years, so it's mostly known as his work.

The first version on [SourceForge](https://sourceforge.net/projects/tktable/files/tktable/) is
1.82, from 1998[^v182], and the latest one there, 2.10, is from November 2008[^v210]. Today,
[bohagan1/TkTable](https://github.com/bohagan1/TkTable), by Brian O'Hagan, continues it, and
[pytktable-binaries](https://github.com/nbro/pytktable-binaries) is built from its releases.

[^tcl]: See [Tcl on Wikipedia](https://en.wikipedia.org/wiki/Tcl_(programming_language)) and the
    [Tcl chronology](https://wiki.tcl-lang.org/page/Tcl+chronology) on the Tcler's wiki, which says
    that Ousterhout first used Tcl in 1988 and presented it at the USENIX conference in 1990.

[^tk]: According to the [Tcl chronology](https://wiki.tcl-lang.org/page/Tcl+chronology),
    Ousterhout began Tk in late 1988 and presented it in 1991.

[^lumholt]: The [`tkinter` documentation of Python 3.9](https://docs.python.org/3.9/library/tkinter.html#tkinter-life-preserver)
    says "Tkinter was written by Steen Lumholt and Guido van Rossum", and in his
    [post of 1994/06/28](https://legacy.python.org/search/hypermail/python-1994q2/1022.html)
    Guido van Rossum announces "a new version of Steen Lumholt's Tk interface".

[^python]: See [Why was Python created in the first place?](https://docs.python.org/3/faq/general.html#why-was-python-created-in-the-first-place)
    in Python's FAQ: Guido van Rossum started it during the 1989 Christmas holidays and posted it to
    USENET in February 1991.

[^king]: Roland King's first release is dated 1994/09/22 in the history of Tktable, imported from
    the original SourceForge CVS repository into
    [bohagan1/TkTable](https://github.com/bohagan1/TkTable), whose
    [README](https://github.com/bohagan1/TkTable/blob/master/README.txt) still says "Conceptually
    based on Tk3 table widget by Roland King".

[^hobbs]: tkTable v1.0 is dated 1996/12/19 and was committed by Jeffrey Hobbs. The
    [README](https://github.com/bohagan1/TkTable/blob/master/README.txt) says
    "Copyright 1997-2002, Jeffrey Hobbs".

[^v182]: The [tktable-1-82-0](https://github.com/bohagan1/TkTable/tree/tktable-1-82-0) tag is
    dated 1998/04/03.

[^v210]: The [tktable-2-10-0](https://github.com/bohagan1/TkTable/tree/tktable-2-10-0) tag is
    dated 2008/11/15.
