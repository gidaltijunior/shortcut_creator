#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ShortcutCreator(object):

    SUCCESS = "Shortcut created successfully!"
    ERROR_DESKTOP = "An error occurred while creating the shortcut on the Desktop..."
    ERROR_DASHBOARD = "An error occurred while creating the shortcut on the Dashboard..."
    UNABLE_DESKTOP_PATH = "Unable to find desktop path"

    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("shortcutcreator.glade")
        self.window = builder.get_object("mainwindow")
        self.name = builder.get_object("name")
        self.version = builder.get_object("version")
        self.execpre = builder.get_object("execpre")
        self.execu = builder.get_object("exec")
        self.execpos = builder.get_object("execpos")
        self.path = builder.get_object("path")
        self.icon = builder.get_object("icon")
        self.type = builder.get_object("type")
        self.startup = builder.get_object("startup")
        self.terminal = builder.get_object("terminal")
        self.categories = builder.get_object("categories")
        self.comments = builder.get_object("comments")
        self.desktop = builder.get_object("desktop")
        self.dashboard = builder.get_object("dashboard")
        self.create = builder.get_object("create")
        self.dialogwarning = builder.get_object("dialogwarning")
        self.dialogdone = builder.get_object("dialogdone")
        self.aboutdialog = builder.get_object("aboutdialog")
        self.dialogerror = builder.get_object("dialogerror")
        self.window.show()
        builder.connect_signals({"gtk_main_quit": Gtk.main_quit,
                                 "on_create_clicked": self.create_shortcut,
                                 "on_about_activate": self.showabout})

    def create_shortcut(self, widget):
        v_name = self.name.get_text()
        v_version = self.version.get_text()
        v_execpre = self.execpre.get_text()
        v_execu = self.execu.get_filename()
        v_execpos = self.execpos.get_text()
        v_path = self.path.get_filename()
        v_icon = self.icon.get_filename()
        v_type = self.type.get_text()
        v_startup = self.startup.get_active()
        v_terminal = self.terminal.get_active()
        v_categories = self.categories.get_text()
        v_comments = self.comments.get_text()
        v_desktop = self.desktop.get_active()
        v_dashboard = self.dashboard.get_active()
        self.print_all_values(v_name, v_version, v_execpre, v_execu, v_execpos, v_path, v_icon, v_type, v_startup,
                              v_terminal, v_categories, v_comments, v_desktop, v_dashboard)
        prepared_file = self.prepare_file(v_name, v_version, v_execpre, v_execu, v_execpos, v_path, v_icon, v_type,
                                          v_startup, v_terminal, v_categories, v_comments)
        if v_desktop is False and v_dashboard is False:
            self.dialogwarning.run()
            self.dialogwarning.hide()
        else:
            self.create_file(prepared_file, v_name, v_desktop, v_dashboard)

    @staticmethod
    def print_all_values(n1, v1, e1, e2, e3, p1, i1, t1, s1, t2, c1, c2, d1, d2):
        print("\nPRINTING ALL VALUES:\n")
        print("name: " + n1)
        print("version: " + v1)
        print("execpre: " + e1)
        print("exec: " + str(e2))
        print("execpos: " + e3)
        print("path: " + str(p1))
        print("icon: " + str(i1))
        print("type: " + t1)
        print("startup: " + str(s1))
        print("terminal: " + str(t2))
        print("categories: " + c1)
        print("comments: " + c2)
        print("desktop: " + str(d1))
        print("dashboard: " + str(d2))

    @staticmethod
    def prepare_file(n1, v1, e1, e2, e3, p1, i1, t1, s1, t2, c1, c2):
        # Desktop Entry - mandatory
        content = "[Desktop Entry]"
        # Name - String
        if n1 != "":
            content += "\nName=" + n1
        # Version - String
        if v1 != "":
            content += "\nVersion=" + v1
        # Exec - e1 e2 e3 or any combination between them
        # example: Exec=python /mnt/extension/python/script.py -debug (e1 e2 e3)
        # example: Exec=/home/myuser/application/app.bin (e2 only)
        # example: Exec=gksudo nautilus (e1 and e3, or only e1, or only e3)
        if e1 != "":
            content += "\nExec=" + e1
            if e2 is not None:
                content += " " + str(e2).replace(" ", "\\ ")
                if e3 != "":
                    content += " " + e3
            else:
                if e3 != "":
                    content += " " + e3
        else:
            if e2 is not None:
                content += "\nExec=" + str(e2).replace(" ", "\\ ")
                if e3 != "":
                    content += " " + e3
            else:
                if e3 != "":
                    content += "\nExec=" + e3
        if p1 is not None:
            content += "\nPath=" + p1
        if i1 is not None:
            content += "\nIcon=" + i1
        if t1 != "":
            content += "\nType=" + t1
        # StartupNotify
        content += "\nStartupNotify=" + str(s1).lower()
        # Terminal
        content += "\nTerminal=" + str(t2).lower()
        if c1 != "":
            content += "\nCategories=" + c1
        if c2 != "":
            content += "\nComments=" + c2

        print("\nFILE CONTENT:\n\n" + content)

        return content
    
    def create_file(self, content, filename, desktop, dashboard):
        messagecontrol = 0
        if desktop is True:
            try:
                desktoppath = self.get_desktop_directory()
                shortcut = open(os.path.expanduser(desktoppath)+filename+".desktop", "w")
                shortcut.write(content)
                shortcut.close()
                os.chmod(os.path.expanduser(desktoppath) + filename + ".desktop", 0o750)
                messagecontrol += 1
            except Exception:
                self.errormessage(self.ERROR_DESKTOP, "There was one or more errors. The file may have not been "
                                                      "created or the permission was not applied correctly. Please "
                                                      "check your desktop and grant permission to the file if "
                                                      "the case.")
        if dashboard is True:
            try:
                dashboardpath = "~/.local/share/applications/"
                shortcut = open(os.path.expanduser(dashboardpath)+filename+".desktop", "w")
                shortcut.write(content)
                shortcut.close()
                os.chmod(os.path.expanduser(dashboardpath) + filename + ".desktop", 0o750)
                messagecontrol += 2
            except Exception:
                self.errormessage(self.ERROR_DASHBOARD, "There was one or more errors. The file may have not been "
                                                        "created or the permission was not applied correctly. "
                                                        "Please check your ~/.local/share/applications folder and "
                                                        "grant permission to the file if the case.")
        if messagecontrol == 1:
            self.successmessage(self.SUCCESS, "The shortcut was created as specified on your Desktop.")
        if messagecontrol == 2:
            self.successmessage(self.SUCCESS, "The shortcut was created as specified on your Dashboard.")
        if messagecontrol == 3:
            self.successmessage(self.SUCCESS, "The shortcut was created as specified on your Desktop and Dashboard.")

    def successmessage(self, header, body):
        self.dialogdone.set_property("text", header)
        self.dialogdone.set_property("secondary_text", body)
        self.dialogdone.run()
        self.dialogdone.hide()
    
    def errormessage(self, header, body):
        self.dialogerror.set_property("text", header)
        self.dialogerror.set_property("secondary_text", body)
        self.dialogerror.run()
        self.dialogerror.hide()

    def get_desktop_directory(self):
        try:
            desktoppath = str()
            user_dirs = open(os.path.expanduser("~/.config/user-dirs.dirs"), "r")
            for line in user_dirs:
                if line.find("XDG_DESKTOP_DIR=") != -1:
                    equalpos = line.find("=")
                    desktoppath = line[equalpos+1:len(line)].replace("$HOME", "~")
                    desktoppath = desktoppath.replace("\"", "")
                    desktoppath = desktoppath.replace("\n", "")
                    desktoppath += "/"
                    print("\nDESKTOP PATH IS: "+desktoppath)
                    break
            return desktoppath
        except Exception:
            self.errormessage("Unable to find desktop path",
                              "The desktop path could not be found. Make sure this file exists: "
                              "~/.config/user-dirs.dirs")

    def showabout(self, widget):
        self.aboutdialog.run()
        self.aboutdialog.hide()


if __name__ == "__main__":
    app = ShortcutCreator()
    Gtk.main()
