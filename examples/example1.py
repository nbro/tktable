# pylint: disable=missing-module-docstring, missing-function-docstring
import sys
from tkinter import Button, Label, Tk

from tktable import ArrayVar, Table


def main():
    def test_cmd(event):
        if event.i == 0:
            return f"{event.r:d}, {event.c:d}"
        return "set"

    def browsecmd(event):
        print("event:", event.__dict__)
        print("curselection:", test.curselection())
        print("active cell index:", test.index("active"))
        print("active:", test.index("active", "row"))
        print("anchor:", test.index("anchor", "row"))

    root = Tk()

    var = ArrayVar(root)
    for y in range(-1, 4):
        for x in range(-1, 5):
            index = f"{y:d},{x:d}"
            var[index] = index

    label = Label(root, text="Proof-of-existence test for Tktable")
    label.pack(side="top", fill="x")

    quit_ = Button(root, text="QUIT", command=root.destroy)
    quit_.pack(side="bottom", fill="x")

    test = Table(
        root,
        rows=10,
        cols=5,
        state="disabled",
        width=6,
        height=6,
        titlerows=1,
        titlecols=1,
        roworigin=-1,
        colorigin=-1,
        selectmode="browse",
        selecttype="row",
        rowstretch="unset",
        colstretch="last",
        browsecmd=browsecmd,
        flashmode="on",
        variable=var,
        usecommand=0,
        command=test_cmd,
    )
    test.pack(expand=1, fill="both")
    test.tag_configure("sel", background="yellow")
    test.tag_configure("active", background="blue")
    test.tag_configure("title", anchor="w", bg="red", relief="sunken")

    if "-test" in sys.argv:
        root.after(1000, lambda: root.destroy())  # pylint: disable=unnecessary-lambda

    root.mainloop()


if __name__ == "__main__":
    main()
