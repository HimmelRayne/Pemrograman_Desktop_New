
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime
import os
import re


class AdvancedTextEditor:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Advanced Text Editor - Untitled")
        self.window.geometry("1000x700")
        self.window.minsize(700, 450)

        self.current_file = None
        self.is_modified = False
        self.recent_files = []
        self.max_recent_files = 10
        self.current_font = ("Consolas", 12)
        self.word_wrap = True
        self.show_line_numbers = True

        self.find_dialog = None
        self.replace_dialog = None
        self.find_tag_active = False

        self.buat_interface()
        self.buat_menu_system()
        self.buat_toolbar_buttons()
        self.bind_events()
        self.update_title()
        self.update_status("Ready")
        self.update_cursor_position()

    def buat_interface(self):
        self.toolbar = tk.Frame(
            self.window, bg="lightgray", relief=tk.RAISED, bd=1
        )
        self.toolbar.pack(fill=tk.X)

        editor_frame = tk.Frame(self.window)
        editor_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.line_numbers = tk.Text(
            editor_frame,
            width=5,
            padx=5,
            takefocus=0,
            borderwidth=0,
            background="#eeeeee",
            foreground="#666666",
            font=self.current_font,
            state=tk.DISABLED,
            wrap=tk.NONE
        )
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        self.text_area = tk.Text(
            editor_frame,
            wrap=tk.WORD,
            undo=True,
            maxundo=-1,
            font=self.current_font,
            bg="white",
            fg="black",
            insertbackground="black",
            selectbackground="lightblue",
            padx=5,
            pady=5
        )

        self.scrollbar = tk.Scrollbar(
            editor_frame,
            orient=tk.VERTICAL,
            command=self.scroll_text
        )
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.text_area.configure(yscrollcommand=self.sync_scrollbar)

        self.status_bar = tk.Frame(
            self.window, relief=tk.SUNKEN, bd=1
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        self.status_label = tk.Label(
            self.status_bar, text="Ready",
            anchor=tk.W, font=("Arial", 9)
        )
        self.status_label.pack(side=tk.LEFT, padx=5)

        self.position_label = tk.Label(
            self.status_bar,
            text="Line: 1, Column: 1",
            anchor=tk.E,
            font=("Arial", 9)
        )
        self.position_label.pack(side=tk.RIGHT, padx=5)

        self.file_info_label = tk.Label(
            self.status_bar,
            text="Untitled | UTF-8",
            anchor=tk.CENTER,
            font=("Arial", 9)
        )
        self.file_info_label.pack(side=tk.RIGHT, padx=20)

        self.update_line_numbers()

    def buat_toolbar_buttons(self):
        buttons = [
            ("📄 New", self.new_file),
            ("📁 Open", self.open_file),
            ("💾 Save", self.save_file)
        ]

        for text, command in buttons:
            tk.Button(
                self.toolbar,
                text=text,
                command=command,
                relief=tk.FLAT,
                bg="lightgray",
                font=("Arial", 9)
            ).pack(side=tk.LEFT, padx=2, pady=2)

        self.add_separator()

        for text, command in [
            ("↶ Undo", self.undo_action),
            ("↷ Redo", self.redo_action)
        ]:
            tk.Button(
                self.toolbar,
                text=text,
                command=command,
                relief=tk.FLAT,
                bg="lightgray",
                font=("Arial", 9)
            ).pack(side=tk.LEFT, padx=2, pady=2)

        self.add_separator()

        for text, command in [
            ("🔍 Find", self.show_find_dialog),
            ("🔤 Font", self.change_font)
        ]:
            tk.Button(
                self.toolbar,
                text=text,
                command=command,
                relief=tk.FLAT,
                bg="lightgray",
                font=("Arial", 9)
            ).pack(side=tk.LEFT, padx=2, pady=2)

    def add_separator(self):
        tk.Frame(
            self.toolbar,
            width=2,
            bg="gray",
            relief=tk.SUNKEN,
            bd=1
        ).pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=2)

    def buat_menu_system(self):
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(
            label="New", command=self.new_file,
            accelerator="Ctrl+N"
        )
        file_menu.add_command(
            label="Open...", command=self.open_file,
            accelerator="Ctrl+O"
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Save", command=self.save_file,
            accelerator="Ctrl+S"
        )
        file_menu.add_command(
            label="Save As...", command=self.save_as_file,
            accelerator="Ctrl+Shift+S"
        )
        file_menu.add_separator()

        self.recent_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(
            label="Recent Files", menu=self.recent_menu
        )
        self.update_recent_menu()

        file_menu.add_separator()
        file_menu.add_command(
            label="Exit", command=self.on_closing,
            accelerator="Ctrl+Q"
        )

        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        edit_menu.add_command(
            label="Undo", command=self.undo_action,
            accelerator="Ctrl+Z"
        )
        edit_menu.add_command(
            label="Redo", command=self.redo_action,
            accelerator="Ctrl+Y"
        )
        edit_menu.add_separator()
        edit_menu.add_command(
            label="Cut", command=self.cut_text,
            accelerator="Ctrl+X"
        )
        edit_menu.add_command(
            label="Copy", command=self.copy_text,
            accelerator="Ctrl+C"
        )
        edit_menu.add_command(
            label="Paste", command=self.paste_text,
            accelerator="Ctrl+V"
        )
        edit_menu.add_separator()
        edit_menu.add_command(
            label="Select All", command=self.select_all,
            accelerator="Ctrl+A"
        )
        edit_menu.add_command(
            label="Find...", command=self.show_find_dialog,
            accelerator="Ctrl+F"
        )
        edit_menu.add_command(
            label="Replace...", command=self.show_replace_dialog,
            accelerator="Ctrl+H"
        )

        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)

        self.wrap_var = tk.BooleanVar(value=self.word_wrap)
        view_menu.add_checkbutton(
            label="Word Wrap",
            variable=self.wrap_var,
            command=self.toggle_word_wrap
        )

        self.line_numbers_var = tk.BooleanVar(
            value=self.show_line_numbers
        )
        view_menu.add_checkbutton(
            label="Show Line Numbers",
            variable=self.line_numbers_var,
            command=self.toggle_line_numbers
        )

        view_menu.add_separator()
        view_menu.add_command(
            label="Change Font...", command=self.change_font
        )

        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(
            label="Word Count", command=self.show_word_count
        )
        tools_menu.add_command(
            label="Character Count", command=self.show_char_count
        )
        tools_menu.add_separator()
        tools_menu.add_command(
            label="Insert Date/Time", command=self.insert_datetime
        )

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def bind_events(self):
        file_shortcuts = {
            "<Control-n>": self.new_file,
            "<Control-o>": self.open_file,
            "<Control-s>": self.save_file,
            "<Control-Shift-S>": self.save_as_file,
            "<Control-q>": self.on_closing,
            "<Control-f>": self.show_find_dialog,
            "<Control-h>": self.show_replace_dialog
        }

        for sequence, command in file_shortcuts.items():
            self.window.bind(
                sequence,
                lambda event, cmd=command: self.run_shortcut(cmd)
            )

        edit_shortcuts = {
            "<Control-z>": self.undo_action,
            "<Control-y>": self.redo_action,
            "<Control-x>": self.cut_text,
            "<Control-c>": self.copy_text,
            "<Control-v>": self.paste_text,
            "<Control-a>": self.select_all
        }

        for sequence, command in edit_shortcuts.items():
            self.text_area.bind(
                sequence,
                lambda event, cmd=command: self.run_shortcut(cmd)
            )

        self.text_area.bind("<<Modified>>", self.on_text_change)
        self.text_area.bind("<KeyRelease>", self.on_cursor_move)
        self.text_area.bind("<ButtonRelease-1>", self.on_cursor_move)
        self.text_area.bind("<Configure>", self.on_cursor_move)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def run_shortcut(self, command):
        command()
        return "break"

    def on_text_change(self, event=None):
        if self.text_area.edit_modified():
            self.text_area.edit_modified(False)

            if not self.is_modified:
                self.is_modified = True
                self.update_title()

            self.update_line_numbers()
            self.update_cursor_position()

    def on_cursor_move(self, event=None):
        self.update_cursor_position()
        self.update_line_numbers()

    def update_cursor_position(self):
        try:
            position = self.text_area.index(tk.INSERT)
            line, column = position.split(".")
            self.position_label.config(
                text=f"Line: {line}, Column: {int(column) + 1}"
            )
        except tk.TclError:
            pass

    def sync_scrollbar(self, first, last):
        self.scrollbar.set(first, last)

        if hasattr(self, "line_numbers"):
            self.line_numbers.yview_moveto(first)

    def scroll_text(self, *args):
        self.text_area.yview(*args)
        self.line_numbers.yview(*args)

    def update_line_numbers(self):
        if not hasattr(self, "line_numbers"):
            return

        content = self.text_area.get("1.0", "end-1c")
        total_lines = max(1, content.count("\n") + 1)

        numbers = "\n".join(
            str(number) for number in range(1, total_lines + 1)
        )

        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete("1.0", tk.END)
        self.line_numbers.insert("1.0", numbers)
        self.line_numbers.config(state=tk.DISABLED)
        self.line_numbers.configure(
            width=max(4, len(str(total_lines)) + 2)
        )

        if self.show_line_numbers:
            if not self.line_numbers.winfo_manager():
                self.line_numbers.pack(
                    side=tk.LEFT,
                    fill=tk.Y,
                    before=self.text_area
                )
        else:
            self.line_numbers.pack_forget()

    def update_title(self):
        name = (
            os.path.basename(self.current_file)
            if self.current_file else "Untitled"
        )
        marker = " *" if self.is_modified else ""

        self.window.title(
            f"Advanced Text Editor - {name}{marker}"
        )
        self.file_info_label.config(text=f"{name} | UTF-8")

    def update_status(self, message):
        self.status_label.config(text=message)

        if hasattr(self, "_status_after"):
            self.window.after_cancel(self._status_after)

        self._status_after = self.window.after(
            3000,
            lambda: self.status_label.config(text="Ready")
        )

    def confirm_save(self):
        if not self.is_modified:
            return True

        response = messagebox.askyesnocancel(
            "Save Changes",
            "Do you want to save changes to the current document?",
            parent=self.window
        )

        if response is True:
            return self.save_file()
        if response is False:
            return True

        return False

    def on_closing(self):
        if self.confirm_save():
            self.window.destroy()

    def new_file(self):
        if not self.confirm_save():
            return

        self.text_area.delete("1.0", tk.END)
        self.text_area.edit_reset()
        self.text_area.edit_modified(False)

        self.current_file = None
        self.is_modified = False
        self.update_title()
        self.update_line_numbers()
        self.update_status("New file created")
        self.text_area.focus_set()

    def open_file(self):
        if not self.confirm_save():
            return

        filename = filedialog.askopenfilename(
            title="Open File",
            filetypes=[
                ("Text files", "*.txt"),
                ("Python files", "*.py"),
                ("JavaScript files", "*.js"),
                ("HTML files", "*.html"),
                ("CSS files", "*.css"),
                ("JSON files", "*.json"),
                ("All files", "*.*")
            ]
        )

        if filename:
            self.load_file(filename)

    def load_file(self, filename):
        try:
            with open(filename, "r", encoding="utf-8-sig") as file:
                content = file.read()

            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", content)
            self.text_area.edit_reset()
            self.text_area.edit_modified(False)

            self.current_file = filename
            self.is_modified = False
            self.add_to_recent_files(filename)
            self.update_title()
            self.update_line_numbers()
            self.update_cursor_position()
            self.update_status(
                f"Opened: {os.path.basename(filename)}"
            )
            self.text_area.focus_set()

        except (OSError, UnicodeError) as error:
            messagebox.showerror(
                "Error", f"Cannot open file:\n{error}"
            )

    def save_file(self):
        if not self.current_file:
            return self.save_as_file()

        try:
            content = self.text_area.get("1.0", "end-1c")

            with open(
                self.current_file, "w", encoding="utf-8"
            ) as file:
                file.write(content)

            self.is_modified = False
            self.text_area.edit_modified(False)
            self.update_title()
            self.add_to_recent_files(self.current_file)
            self.update_status(
                f"Saved: {os.path.basename(self.current_file)}"
            )
            return True

        except OSError as error:
            messagebox.showerror(
                "Error", f"Cannot save file:\n{error}"
            )
            return False

    def save_as_file(self):
        filename = filedialog.asksaveasfilename(
            title="Save As",
            filetypes=[
                ("Text files", "*.txt"),
                ("Python files", "*.py"),
                ("JavaScript files", "*.js"),
                ("HTML files", "*.html"),
                ("CSS files", "*.css"),
                ("JSON files", "*.json"),
                ("All files", "*.*")
            ],
            defaultextension=".txt"
        )

        if not filename:
            return False

        previous_file = self.current_file
        self.current_file = filename

        if self.save_file():
            return True

        self.current_file = previous_file
        self.update_title()
        return False

    def add_to_recent_files(self, filename):
        filename = os.path.abspath(filename)

        if filename in self.recent_files:
            self.recent_files.remove(filename)

        self.recent_files.insert(0, filename)
        self.recent_files = self.recent_files[:self.max_recent_files]
        self.update_recent_menu()

    def update_recent_menu(self):
        if not hasattr(self, "recent_menu"):
            return

        self.recent_menu.delete(0, tk.END)

        if not self.recent_files:
            self.recent_menu.add_command(
                label="No recent files", state=tk.DISABLED
            )
            return

        for index, filename in enumerate(self.recent_files):
            display_name = os.path.basename(filename)

            if len(display_name) > 30:
                display_name = display_name[:27] + "..."

            self.recent_menu.add_command(
                label=f"{index + 1}. {display_name}",
                command=lambda f=filename: self.open_recent_file(f)
            )

        self.recent_menu.add_separator()
        self.recent_menu.add_command(
            label="Clear Recent Files",
            command=self.clear_recent_files
        )

    def open_recent_file(self, filename):
        if not os.path.exists(filename):
            messagebox.showerror(
                "Error", f"File not found:\n{filename}"
            )
            if filename in self.recent_files:
                self.recent_files.remove(filename)
            self.update_recent_menu()
            return

        if self.confirm_save():
            self.load_file(filename)

    def clear_recent_files(self):
        if messagebox.askyesno(
            "Clear Recent Files",
            "Clear all recent files from the list?"
        ):
            self.recent_files.clear()
            self.update_recent_menu()

    def undo_action(self):
        try:
            self.text_area.edit_undo()
            self.update_status("Undo performed")
        except tk.TclError:
            self.update_status("Nothing to undo")

    def redo_action(self):
        try:
            self.text_area.edit_redo()
            self.update_status("Redo performed")
        except tk.TclError:
            self.update_status("Nothing to redo")

    def cut_text(self):
        try:
            start = self.text_area.index(tk.SEL_FIRST)
            end = self.text_area.index(tk.SEL_LAST)
            selected = self.text_area.get(start, end)

            self.window.clipboard_clear()
            self.window.clipboard_append(selected)
            self.text_area.delete(start, end)

            self.update_status("Text cut to clipboard")
        except tk.TclError:
            self.update_status("Select text to cut first")

    def copy_text(self):
        try:
            start = self.text_area.index(tk.SEL_FIRST)
            end = self.text_area.index(tk.SEL_LAST)
            selected = self.text_area.get(start, end)

            self.window.clipboard_clear()
            self.window.clipboard_append(selected)

            self.update_status("Text copied")
        except tk.TclError:
            self.update_status("Select text to copy first")

    def paste_text(self):
        try:
            content = self.window.clipboard_get()

            try:
                start = self.text_area.index(tk.SEL_FIRST)
                end = self.text_area.index(tk.SEL_LAST)
                self.text_area.delete(start, end)
            except tk.TclError:
                pass

            self.text_area.insert(tk.INSERT, content)
            self.update_status("Text pasted")

        except tk.TclError:
            self.update_status("Clipboard is empty or unavailable")

    def select_all(self):
        self.text_area.tag_add(tk.SEL, "1.0", "end-1c")
        self.text_area.mark_set(tk.INSERT, "1.0")
        self.text_area.see(tk.INSERT)
        self.text_area.focus_set()
        self.update_status("All text selected")

    def show_find_dialog(self):
        if (
            self.find_dialog
            and self.find_dialog.winfo_exists()
        ):
            self.find_dialog.lift()
            self.find_entry.focus_set()
            return

        self.find_dialog = tk.Toplevel(self.window)
        self.find_dialog.title("Find")
        self.find_dialog.geometry("400x170")
        self.find_dialog.transient(self.window)
        self.find_dialog.grab_set()

        tk.Label(self.find_dialog, text="Find:").pack(pady=5)

        self.find_entry = tk.Entry(self.find_dialog, width=40)
        self.find_entry.pack(pady=5)
        self.find_entry.focus_set()

        options = tk.Frame(self.find_dialog)
        options.pack(pady=5)

        self.case_sensitive_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            options,
            text="Case sensitive",
            variable=self.case_sensitive_var
        ).pack(side=tk.LEFT, padx=5)

        self.whole_word_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            options,
            text="Whole word",
            variable=self.whole_word_var
        ).pack(side=tk.LEFT, padx=5)

        buttons = tk.Frame(self.find_dialog)
        buttons.pack(pady=10)

        tk.Button(
            buttons, text="Find Next", command=self.find_next
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            buttons, text="Find All", command=self.find_all
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            buttons,
            text="Close",
            command=self.find_dialog.destroy
        ).pack(side=tk.LEFT, padx=5)

        self.find_entry.bind(
            "<Return>", lambda event: self.find_next()
        )

    def search_occurrences(self, search_text):
        matches = []
        position = "1.0"
        content_end = self.text_area.index("end-1c")

        while self.text_area.compare(position, "<", content_end):
            count = tk.IntVar(master=self.window)

            found = self.text_area.search(
                search_text,
                position,
                tk.END,
                nocase=not self.case_sensitive_var.get(),
                count=count
            )

            if not found:
                break

            length = count.get()

            if length <= 0:
                break

            end = f"{found}+{length}c"
            valid = True

            if self.whole_word_var.get():
                before = self.text_area.get(
                    f"{found}-1c", found
                )
                after = self.text_area.get(
                    end, f"{end}+1c"
                )

                if before and (
                    before.isalnum() or before == "_"
                ):
                    valid = False

                if after and (
                    after.isalnum() or after == "_"
                ):
                    valid = False

            if valid:
                matches.append((found, end))

            position = end

        return matches

    def find_next(self):
        search_text = self.find_entry.get()

        if not search_text:
            return

        matches = self.search_occurrences(search_text)
        cursor = self.text_area.index(tk.INSERT)

        found = next(
            (
                match for match in matches
                if self.text_area.compare(
                    match[0], ">=", cursor
                )
            ),
            None
        )

        if found is None and matches:
            found = matches[0]

        if found:
            start, end = found
            self.text_area.tag_remove(tk.SEL, "1.0", tk.END)
            self.text_area.tag_add(tk.SEL, start, end)
            self.text_area.mark_set(tk.INSERT, end)
            self.text_area.see(start)
            self.text_area.focus_set()
            self.update_status(f"Found: {search_text}")
        else:
            messagebox.showinfo(
                "Find", f"'{search_text}' not found"
            )

    def find_all(self):
        search_text = self.find_entry.get()

        if not search_text:
            return

        self.text_area.tag_remove("found", "1.0", tk.END)
        matches = self.search_occurrences(search_text)

        for start, end in matches:
            self.text_area.tag_add("found", start, end)

        self.text_area.tag_config(
            "found", background="yellow", foreground="black"
        )

        if matches:
            self.update_status(
                f"Found {len(matches)} occurrences of '{search_text}'"
            )
        else:
            messagebox.showinfo(
                "Find All", f"'{search_text}' not found"
            )

    def show_replace_dialog(self):
        if (
            self.replace_dialog
            and self.replace_dialog.winfo_exists()
        ):
            self.replace_dialog.lift()
            self.replace_find_entry.focus_set()
            return

        self.replace_dialog = tk.Toplevel(self.window)
        self.replace_dialog.title("Replace")
        self.replace_dialog.geometry("400x230")
        self.replace_dialog.transient(self.window)
        self.replace_dialog.grab_set()

        tk.Label(self.replace_dialog, text="Find:").pack(pady=4)
        self.replace_find_entry = tk.Entry(
            self.replace_dialog, width=40
        )
        self.replace_find_entry.pack(pady=4)

        tk.Label(
            self.replace_dialog, text="Replace with:"
        ).pack(pady=4)
        self.replace_with_entry = tk.Entry(
            self.replace_dialog, width=40
        )
        self.replace_with_entry.pack(pady=4)

        options = tk.Frame(self.replace_dialog)
        options.pack(pady=4)

        self.replace_case_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            options,
            text="Case sensitive",
            variable=self.replace_case_var
        ).pack(side=tk.LEFT, padx=5)

        buttons = tk.Frame(self.replace_dialog)
        buttons.pack(pady=10)

        tk.Button(
            buttons, text="Replace",
            command=self.replace_current
        ).pack(side=tk.LEFT, padx=3)

        tk.Button(
            buttons, text="Replace All",
            command=self.replace_all
        ).pack(side=tk.LEFT, padx=3)

        tk.Button(
            buttons,
            text="Close",
            command=self.replace_dialog.destroy
        ).pack(side=tk.LEFT, padx=3)

        self.replace_find_entry.focus_set()

    def replace_current(self):
        find_text = self.replace_find_entry.get()
        replace_text = self.replace_with_entry.get()

        if not find_text:
            return

        try:
            start = self.text_area.index(tk.SEL_FIRST)
            end = self.text_area.index(tk.SEL_LAST)
            selected = self.text_area.get(start, end)

            if self.replace_case_var.get():
                matches = selected == find_text
            else:
                matches = selected.casefold() == find_text.casefold()

            if matches:
                self.text_area.delete(start, end)
                self.text_area.insert(start, replace_text)
                self.update_status("Text replaced")
            else:
                messagebox.showinfo(
                    "Replace",
                    "Selected text does not match the search text"
                )

        except tk.TclError:
            messagebox.showinfo(
                "Replace", "Select a matching occurrence first"
            )

    def replace_all(self):
        find_text = self.replace_find_entry.get()
        replace_text = self.replace_with_entry.get()

        if not find_text:
            return

        content = self.text_area.get("1.0", "end-1c")

        if self.replace_case_var.get():
            count = content.count(find_text)
            new_content = content.replace(find_text, replace_text)
        else:
            pattern = re.compile(re.escape(find_text), re.IGNORECASE)
            new_content, count = pattern.subn(
                lambda match: replace_text, content
            )

        if count:
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", new_content)
            self.update_status(f"Replaced {count} occurrences")

            messagebox.showinfo(
                "Replace All",
                f"Replaced {count} occurrences of '{find_text}'"
            )
        else:
            messagebox.showinfo(
                "Replace All", f"'{find_text}' not found"
            )

    def toggle_word_wrap(self):
        self.word_wrap = self.wrap_var.get()
        self.text_area.config(
            wrap=tk.WORD if self.word_wrap else tk.NONE
        )
        self.update_status(
            f"Word wrap {'enabled' if self.word_wrap else 'disabled'}"
        )

    def toggle_line_numbers(self):
        self.show_line_numbers = self.line_numbers_var.get()
        self.update_line_numbers()
        self.update_status(
            f"Line numbers {'enabled' if self.show_line_numbers else 'disabled'}"
        )

    def change_font(self):
        dialog = tk.Toplevel(self.window)
        dialog.title("Change Font")
        dialog.geometry("320x210")
        dialog.transient(self.window)
        dialog.grab_set()

        tk.Label(dialog, text="Font Family:").pack(pady=5)

        families = [
            "Arial", "Times New Roman", "Courier New",
            "Consolas", "Verdana"
        ]

        font_var = tk.StringVar(value=self.current_font[0])
        ttk.Combobox(
            dialog,
            textvariable=font_var,
            values=families,
            state="readonly"
        ).pack(pady=5)

        tk.Label(dialog, text="Font Size:").pack(pady=5)

        size_var = tk.IntVar(value=self.current_font[1])
        tk.Spinbox(
            dialog, from_=8, to=72, textvariable=size_var
        ).pack(pady=5)

        def apply_font():
            try:
                size = int(size_var.get())

                if not 8 <= size <= 72:
                    raise ValueError

                self.current_font = (font_var.get(), size)
                self.text_area.config(font=self.current_font)
                self.line_numbers.config(font=self.current_font)
                self.update_line_numbers()
                self.update_status(
                    f"Font changed to {font_var.get()} {size}"
                )
                dialog.destroy()

            except (ValueError, tk.TclError):
                messagebox.showerror(
                    "Invalid Font Size",
                    "Enter a font size between 8 and 72."
                )

        buttons = tk.Frame(dialog)
        buttons.pack(pady=10)

        tk.Button(
            buttons, text="Apply", command=apply_font
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            buttons, text="Cancel", command=dialog.destroy
        ).pack(side=tk.LEFT, padx=5)

    def show_word_count(self):
        content = self.text_area.get("1.0", "end-1c")
        words = len(content.split())
        lines = len(content.splitlines()) if content else 0

        messagebox.showinfo(
            "Word Count",
            f"Words: {words}\nLines: {lines}"
        )

    def show_char_count(self):
        content = self.text_area.get("1.0", "end-1c")
        chars = len(content)
        chars_no_spaces = len(re.sub(r"\s", "", content))

        messagebox.showinfo(
            "Character Count",
            f"Characters: {chars}\n"
            f"Characters (no whitespace): {chars_no_spaces}"
        )

    def insert_datetime(self):
        value = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.text_area.insert(tk.INSERT, value)
        self.text_area.focus_set()
        self.update_status("Date/time inserted")

    def show_about(self):
        messagebox.showinfo(
            "About",
            "Advanced Text Editor\n"
            "Version 1.0\n\n"
            "A text editor built with Python Tkinter.\n\n"
            "Features:\n"
            "- File operations and recent files\n"
            "- Undo and redo\n"
            "- Find and replace\n"
            "- Word wrap and line numbers\n"
            "- Font customization\n"
            "- Word and character count\n"
            "- Date/time insertion\n\n"
            "Created for educational purposes."
        )

    def jalankan(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = AdvancedTextEditor()
    app.jalankan()
