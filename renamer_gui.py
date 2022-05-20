#!/usr/bin/python3
# -*- coding: utf-8 -*-
# created by neo
# Version-1.0

from tkinter import (Frame, Button, Label, Text, Checkbutton, Entry, Toplevel, Listbox,
                     Menu, Tk, IntVar, StringVar, SINGLE, ACTIVE, END, SW, SE,
                     S, UNDERLINE, NORMAL, DISABLED, HORIZONTAL)
import os
import platform
import socket
import sys
import time
import errno
from pathlib import Path
from tkinter.messagebox import showerror
from tkinter.filedialog import askdirectory, askopenfile

operation_platform = platform.system()

username = str(os.getlogin())  # Тут мы получаем имя владельца Компьютера
restore_dir = str(Path('/'))
homedir = str(Path.home())
target_dir = homedir+os.sep+'backup'
# the folder where will be stored backuped files
remarkfile = "remarks.txt"
root_choice = []
root_choice0 = []
root_choice3 = []
user = str(username)  # укажите имя пользователя
prev2 = []
root_2 = []
root2 = [restore_dir]
main_ext = [".mp3", ".mp4", ".avi", ".mkv", ".jpg", ".png", ".pdf", ".m4a"]
ext = []
newext = []


class Renamer(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Renamer")
        self.master.maxsize(1000, 900)
        self.master.minsize(500, 400)
        self.grid(ipadx=15, ipady=15, rowspan=4, columnspan=5)
        self.create_widgets()

    def create_widgets(self):
        '''Выполняется  первым'''
        # Initializing our widgets and Frames
        self.frame = Frame()
        self.frame0 = Frame()
        self.frame1 = Frame()
        self.frame2 = Frame()
        self.frame3 = Frame()
        self.frame4 = Frame()

        self.frame.grid()
        self.frame0.grid()
        self.frame1.grid()
        self.frame2.grid()
        self.frame3.grid()
        self.frame4.grid()

        # Restart button
        restart_btn = Button(
            self.master, text="Restart script",
            command=self.restart,
            bg="#fff255", pady=5,
            padx=5, activebackground='#aa3666'
        )
        restart_btn.grid(sticky=SW, pady=15, padx=10, column=0, row=100)
        
        # Quit button
        self.quit_btn = Button(
            self.master, text="Завершить", command=self.master.quit,
            bg="#ccc255", pady=5, padx=5, activebackground='#aa3776'
        )
        self.quit_btn.grid(sticky=SE, pady=15, padx=10, column=10, row=100)
        
        # Start actually our script
        self.extension_choose()

    # Choose which extension you need to rename
    def extension_choose(self):
        self.list_of_extensions = Label(self.frame0)
        self.list_of_extensions["text"] = (
            "Укажите файлы с каким расширением будете переименовывать:  "+"\n"
        )
        # Проверка кол-ва строк  чтобы сделать правильную высоту Листбокса
        width_listbox = int(len(main_ext))
        self.list_extensions = Listbox(
            self.frame0, height=width_listbox,
            # Кол-ву расширений равно высота listbox
            width=10, selectbackground='#aa3666',
            selectmode=SINGLE
        )
        for item in main_ext:
            # Добавляем все наши расширения в наш listbox
            self.list_extensions.insert(END, item)

        self.button_ext = Button(
            self.frame0, text="Выбрать расширение",
            background='red', foreground='green',
            command=lambda: self.extension_seted()
            # Тут все понятно- выполняется команда после выбора расширения
        )
        # Ниже мы просто выводим все наши виджеты на экран методом .grid
        self.button_ext.grid(row=2, column=0)
        self.list_of_extensions.grid(row=0, column=0)
        self.list_extensions.grid(row=1, column=0)

    def extension_seted(self):
        '''
        Тут выполняется показ того какое расширение файла мы выбрали
        и спрашиваться из какой папки взять файлы с таким расширением
        '''
        self.new = list(self.list_extensions.curselection())
        self.ext_num = int(self.new[0])
        self.newext = (main_ext[(self.ext_num)])
        self.frame0.destroy()
        self.label_files = Label(self.frame1, padx=20)
        ext.append(self.newext)
        newext.append(self.newext)
        self.label_files["text"] = (
            "Вы будете переименовывать" +
            "файлы в формате: " +
            str((ext[0]))+"\n"
            )
        self.button = Button(
            self.frame1, text="Выбрать папкус файлами",
            command=self.openfolder
            )
        self.button.grid(row=1, column=0)
        self.label_files.grid(row=0, column=0)

    # here we show which files you will rename by earlier choosed extension

    def openfolder(self):
        self.frame1.destroy()
        # Спрашивает папку откуда брать файлы
        self.folder = askdirectory(
            title="Выберите папку",
            initialdir=os.sep
            )
        self.folder_for_search = str(self.folder)
        self.listed_folder = os.listdir(self.folder_for_search)
        self.total_files = len(self.listed_folder)  # Считаем сколько всего файлов в папке
        self.num_of_songs = []
        for i, f in enumerate(self.listed_folder):
            if f.endswith(str(ext[0])):
                self.num_of_songs.append(f)
        # Считаем сколько файлов с нужным нам расширением
        self.num_of_songs_with_same_ext = int(len(self.num_of_songs))
        self.label_files = Label(
            self.frame2, padx=20
            )
        self.list = Listbox(
            self.frame2, width=30, selectbackground='#aa3666',
            selectmode=SINGLE
            )
        for j, file in enumerate(self.listed_folder):
            if file.endswith(str(ext[0])):
                self.list.insert(END, file)  # Показываем ф-лы устраивающие нас
        if self.num_of_songs_with_same_ext != 0:
            self.label_files = Label(
                self.frame2, padx=20
            )
            self.label_files["text"] = str(
                "Там есть " +
                str(self.num_of_songs_with_same_ext)+" файлов " +
                "с расширением " + str(ext[0]) + " из " + str(self.total_files)
                # Показываем все наши расчеты на экран
            )
            self.list.grid(row=1, column=0)
            self.label_files.grid(row=0, column=0)
            self.button = Button(
                self.frame2, text="Переименовать",
                command=self.entry_num
                )
            self.button.grid(row=2, column=1)
        else:
            self.label_files["text"] = str(
                "Нет файлов с таким расширением\n" +
                "Попробуйте в другой папке или другое расширение"
            )
            self.list.grid_forget()
            self.label_files.grid(row=0, column=0)
            self.button = Button(
                self.frame2, text="Изменить папку",
                command=self.repeat
                )
            self.button.grid(row=2, column=1)

    def repeat(self):
        self.label_files.grid_forget()
        self.openfolder()

    def entry_num(self):
        self.frame.destroy()
        self.frame2.destroy()
        self.label_num = Label(self.frame3)
        self.label_num["text"] = "Введите номер для начала отчета: "
        self.num_en = Entry(self.frame3)
        self.num_en.focus_set()
        self.num_en.grid(row=1, column=0, pady=15, padx=20)
        self.label_num.grid(row=0, column=0)
        self.button = Button(
            self.frame3, text="Далее",
            command=self.entry_name
            )
        self.button.grid(row=2, column=0)

    def entry_name(self):
        self.num = self.num_en.get()
        try:
            self.num = int(self.num_en.get())
        except ValueError:
            print("Вы что-то попутали с вводом")
            self.textvar = showerror(
                "Error", message=str(
                    "Веедите номер а не букву: " +
                    str(self.num_en.get()))
                )
        else:  # когда в блоке try не возникло исключения
            self.frame3.destroy()
            self.label_name = Label(self.frame4)
            self.label_name["text"] = "Введите название для файла: "
            self.name_en = Entry(self.frame4)
            self.name_en.focus_set()
            self.name_en.grid(row=1, column=0, pady=15, padx=20)
            self.label_name.grid(row=0, column=0)
            self.button = Button(
                self.frame4, text="Далее",
                command=self.perform
                )
            self.button.grid(row=2, column=0)

    def perform(self):
        self.result_list={}

        self.name = str(self.name_en.get())
        self.num_changed = int(self.num)
        self.name_changed = self.name.replace(" ","_")
        for j, file in enumerate(self.listed_folder):
            os.chdir(self.folder_for_search)
            r = self.folder_for_search + os.sep + file
            self.result_list[j]=file
            if file.endswith(str(ext[0])):
                # renaming of file :where "self.num_changed" and
                # "self.name_changed" - are taken from entry form
                t = os.rename(
                    f'{r}',
                    f'{self.num_changed}{"_"}{self.name_changed}{str(newext[0])}'
                    )

                self.num_changed += 1
        print(self.result_list)
        self.quit_app()
        
    def restart(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)

    def quit_app(self):
        self.frame4.destroy()
        self.label_succes = Label(self.frame5)
        self.label_succes["text"] = (
            "Процесс завершен успешно \n Переименовано " +
            str(len(self.num_of_songs))+" файлов."
        )
        self.label_succes.grid(row=10, column =20)
        self.quit_btn.grid(column=20)


if __name__ == "__main__":
    root = Tk()
    app = Renamer(master=root)
    app.mainloop()
