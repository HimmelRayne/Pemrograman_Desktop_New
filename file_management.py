import tkinter as tk
from tkinter import filedialog, messagebox
import os
from datetime import datetime
import fitz
from PIL import Image, ImageTk
from io import BytesIO


class FileExplorer:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("File Explorer - File Management Demo")
        self.window.geometry("1000x650")
        self.window.minsize(750, 450)
        self.window.configure(bg="lightsteelblue")

        self.current_file = None
        self.current_directory = os.getcwd()
        self.selected_files = []
        self.pdf_preview_image = None

        self.buat_interface()
        self.show_directory_contents(self.current_directory)

    def buat_interface(self):
        header_frame = tk.Frame(
            self.window, bg="darkblue", height=60
        )
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="FILE EXPLORER",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="darkblue"
        ).pack(pady=15)

        nav_frame = tk.Frame(
            self.window, bg="lightgray", height=40
        )
        nav_frame.pack(fill=tk.X)
        nav_frame.pack_propagate(False)

        tk.Label(
            nav_frame,
            text="Current Directory:",
            font=("Arial", 10, "bold"),
            bg="lightgray"
        ).pack(side=tk.LEFT, padx=10, pady=10)

        self.path_label = tk.Label(
            nav_frame,
            text=self.current_directory,
            font=("Arial", 10),
            bg="lightgray",
            fg="blue",
            anchor="w"
        )
        self.path_label.pack(
            side=tk.LEFT, fill=tk.X, expand=True, pady=10
        )

        toolbar = tk.Frame(
            self.window,
            bg="lightgray",
            relief=tk.RAISED,
            bd=1
        )
        toolbar.pack(fill=tk.X, padx=2, pady=2)

        buttons = [
            ("📁Open File", "lightblue", self.open_file, 12),
            ("📂Open Directory", "lightgreen", self.open_directory, 15),
            ("📄Create File", "lightyellow", self.create_file, 12),
            ("🗑️Delete", "lightcoral", self.delete_file, 10),
            ("🔄Refresh", "lightcyan", self.refresh_view, 10)
        ]

        for text, color, command, width in buttons:
            tk.Button(
                toolbar,
                text=text,
                font=("Arial", 10),
                bg=color,
                command=command,
                width=width
            ).pack(side=tk.LEFT, padx=2, pady=2)

        content_frame = tk.Frame(
            self.window, bg="lightsteelblue"
        )
        content_frame.pack(
            fill=tk.BOTH, expand=True, padx=5, pady=5
        )

        left_frame = tk.LabelFrame(
            content_frame,
            text="File Information",
            font=("Arial", 12, "bold"),
            bg="lightsteelblue"
        )
        left_frame.pack(
            side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5
        )

        self.info_text = tk.Text(
            left_frame,
            font=("Courier New", 10),
            bg="white",
            wrap=tk.WORD,
            height=15
        )

        info_scrollbar = tk.Scrollbar(
            left_frame,
            orient=tk.VERTICAL,
            command=self.info_text.yview
        )
        self.info_text.configure(
            yscrollcommand=info_scrollbar.set
        )

        self.info_text.pack(
            side=tk.LEFT, fill=tk.BOTH, expand=True,
            padx=5, pady=5
        )
        info_scrollbar.pack(
            side=tk.RIGHT, fill=tk.Y, pady=5
        )

        right_frame = tk.LabelFrame(
            content_frame,
            text="File Preview",
            font=("Arial", 12, "bold"),
            bg="lightsteelblue"
        )
        right_frame.pack(
            side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5
        )

        self.preview_text = tk.Text(
            right_frame,
            font=("Courier New", 9),
            bg="lightyellow",
            wrap=tk.WORD,
            height=15,
            state=tk.DISABLED
        )

        preview_scrollbar = tk.Scrollbar(
            right_frame,
            orient=tk.VERTICAL,
            command=self.preview_text.yview
        )
        self.preview_text.configure(
            yscrollcommand=preview_scrollbar.set
        )

        self.preview_text.pack(
            side=tk.LEFT, fill=tk.BOTH, expand=True,
            padx=5, pady=5
        )
        preview_scrollbar.pack(
            side=tk.RIGHT, fill=tk.Y, pady=5
        )

        self.status_label = tk.Label(
            self.window,
            text="Ready",
            anchor="w",
            bg="lightgray",
            padx=8
        )
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)

    def set_text(self, widget, content, readonly=False):
        widget.config(state=tk.NORMAL)
        widget.delete("1.0", tk.END)
        widget.insert("1.0", content)

        if readonly:
            widget.config(state=tk.DISABLED)

    def set_status(self, message):
        self.status_label.config(text=message)

    def update_directory_info(self):
        self.path_label.config(text=self.current_directory)

    def format_file_size(self, size_bytes):
        if size_bytes < 1024:
            return f"{size_bytes} bytes"
        elif size_bytes < 1024 ** 2:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 ** 3:
            return f"{size_bytes / 1024 ** 2:.1f} MB"
        else:
            return f"{size_bytes / 1024 ** 3:.1f} GB"

    def get_file_type(self, filepath):
        extension = os.path.splitext(filepath)[1].lower()

        file_types = {
            ".txt": "Text Document",
            ".py": "Python Script",
            ".json": "JSON Data",
            ".csv": "CSV Data",
            ".html": "HTML Document",
            ".css": "CSS Stylesheet",
            ".js": "JavaScript",
            ".jpg": "JPEG Image",
            ".jpeg": "JPEG Image",
            ".png": "PNG Image",
            ".gif": "GIF Image",
            ".pdf": "PDF Document",
            ".docx": "Word Document",
            ".xlsx": "Excel Spreadsheet",
            ".exe": "Executable File",
            ".zip": "ZIP Archive"
        }

        return file_types.get(
            extension, "Unknown File Type"
        )

    def show_file_info(self, filepath):
        try:
            stat_info = os.stat(filepath)
            file_size = stat_info.st_size

            modified_time = datetime.fromtimestamp(
                stat_info.st_mtime
            )
            created_time = datetime.fromtimestamp(
                stat_info.st_ctime
            )

            info = f"""FILE INFORMATION
{'=' * 45}

File Name: {os.path.basename(filepath)}
Full Path: {filepath}
Directory: {os.path.dirname(filepath)}

File Size: {self.format_file_size(file_size)}
Extension: {os.path.splitext(filepath)[1] or 'No extension'}

Created: {created_time.strftime('%Y-%m-%d %H:%M:%S')}
Modified: {modified_time.strftime('%Y-%m-%d %H:%M:%S')}

Permissions:
- Readable: {'Yes' if os.access(filepath, os.R_OK) else 'No'}
- Writable: {'Yes' if os.access(filepath, os.W_OK) else 'No'}
- Executable: {'Yes' if os.access(filepath, os.X_OK) else 'No'}

File Type: {self.get_file_type(filepath)}
"""

            self.set_text(self.info_text, info)
            self.set_status(
                f"Selected file: {os.path.basename(filepath)}"
            )

        except OSError as e:
            self.set_text(
                self.info_text,
                f"Error getting file information:\n{e}"
            )

    def open_file(self):
        file_types = [
            ("Text files", "*.txt"),
            ("Python files", "*.py"),
            ("JSON files", "*.json"),
            ("CSV files", "*.csv"),
            ("PDF files", "*.pdf"),
            ("All files", "*.*")
        ]

        filename = filedialog.askopenfilename(
            title="Select a file to open",
            filetypes=file_types,
            initialdir=self.current_directory
        )

        if not filename:
            return

        try:
            if not os.path.isfile(filename):
                raise OSError("The selected path is not a file.")

            self.current_file = filename
            self.current_directory = os.path.dirname(filename)

            self.update_directory_info()
            self.show_file_info(filename)
            self.preview_file(filename)

            messagebox.showinfo(
                "Success",
                f"File opened: {os.path.basename(filename)}"
            )

        except (OSError, ValueError) as e:
            messagebox.showerror(
                "Error", f"Cannot open file:\n{e}"
            )

    
    def preview_file(self, filepath):
        try:
            extension = os.path.splitext(filepath)[1].lower()

            if extension == ".pdf":
                self.preview_pdf(filepath)
                return

            file_size = os.path.getsize(filepath)

            if file_size > 1024 * 1024:
                preview_content = (
                    "File too large for preview "
                    f"({self.format_file_size(file_size)})\n\n"
                    "Please use an appropriate application "
                    "to view this file."
                )
            else:
                try:
                    with open(filepath, "r", encoding="utf-8-sig") as file:
                        content = file.read(5001)

                    if len(content) > 5000:
                        preview_content = (
                            content[:5000]
                            + "\n\n... (Content truncated for preview)"
                        )
                    else:
                        preview_content = content

                except UnicodeDecodeError:
                    with open(filepath, "rb") as file:
                        binary_content = file.read(500)

                    preview_content = (
                        "Binary file detected. "
                        "Showing first 500 bytes as hex:\n\n"
                        + " ".join(
                            f"{byte:02x}" for byte in binary_content
                        )
                    )

            self.pdf_preview_image = None
            self.set_text(
                self.preview_text,
                preview_content,
                readonly=True
            )

        except Exception as e:
            self.pdf_preview_image = None
            self.set_text(
                self.preview_text,
                f"Error previewing file:\n{e}",
                readonly=True
            )


    def preview_pdf(self, filepath):
        try:
            with fitz.open(filepath) as document:
                if document.page_count == 0:
                    self.set_text(
                        self.preview_text,
                        "This PDF contains no pages.",
                        readonly=True
                    )
                    return

                page = document.load_page(0)

                # Ekstrak teks dari halaman pertama
                extracted_text = page.get_text("text")

                # Render halaman pertama menjadi gambar
                pixmap = page.get_pixmap(
                    matrix=fitz.Matrix(1.2, 1.2),
                    alpha=False
                )

                image_data = pixmap.tobytes("png")
                image = Image.open(BytesIO(image_data))

                # Batasi lebar gambar agar sesuai panel preview
                max_width = 420

                if image.width > max_width:
                    new_height = int(
                        image.height * max_width / image.width
                    )
                    image = image.resize(
                        (max_width, new_height),
                        Image.Resampling.LANCZOS
                    )

                self.pdf_preview_image = ImageTk.PhotoImage(image)

                self.preview_text.config(state=tk.NORMAL)
                self.preview_text.delete("1.0", tk.END)

                self.preview_text.insert(
                    tk.END,
                    f"PDF PREVIEW\n"
                    f"{'=' * 35}\n"
                    f"File: {os.path.basename(filepath)}\n"
                    f"Total pages: {document.page_count}\n"
                    f"Showing page: 1\n\n"
                )

                # Tampilkan gambar halaman PDF
                self.preview_text.image_create(
                    tk.END,
                    image=self.pdf_preview_image,
                    align="center"
                )

                self.preview_text.insert(
                    tk.END,
                    "\n\nEXTRACTED TEXT - PAGE 1\n"
                    f"{'=' * 35}\n\n"
                )

                if extracted_text.strip():
                    self.preview_text.insert(
                        tk.END,
                        extracted_text[:5000]
                    )

                    if len(extracted_text) > 5000:
                        self.preview_text.insert(
                            tk.END,
                            "\n\n... (Text truncated)"
                        )
                else:
                    self.preview_text.insert(
                        tk.END,
                        "No extractable text found. "
                        "This page may contain a scanned image."
                    )

                self.preview_text.config(state=tk.DISABLED)

        except Exception as e:
            self.set_text(
                self.preview_text,
                f"Cannot preview PDF:\n{e}",
                readonly=True
            )


    def open_directory(self):
        directory = filedialog.askdirectory(
            title="Select a directory",
            initialdir=self.current_directory
        )

        if not directory:
            return

        try:
            self.current_directory = directory
            self.current_file = None

            self.update_directory_info()
            self.show_directory_contents(directory)

            self.set_status(f"Directory: {directory}")

        except OSError as e:
            messagebox.showerror(
                "Error", f"Cannot open directory:\n{e}"
            )

    def show_directory_contents(self, directory):
        try:
            items = os.listdir(directory)

            folders = []
            files = []

            for item in items:
                item_path = os.path.join(directory, item)

                try:
                    if os.path.isdir(item_path):
                        folders.append(item)
                    else:
                        files.append(item)
                except OSError:
                    files.append(item)

            folders.sort(key=str.lower)
            files.sort(key=str.lower)

            dir_info = f"""DIRECTORY CONTENTS
{'=' * 45}

Directory: {directory}
Total Items: {len(items)} ({len(folders)} folders, {len(files)} files)

FOLDERS ({len(folders)}):
{'-' * 30}
"""

            for folder in folders:
                folder_path = os.path.join(directory, folder)

                try:
                    folder_size = self.get_directory_size(
                        folder_path
                    )
                    dir_info += (
                        f"[DIR] {folder} "
                        f"({self.format_file_size(folder_size)})\n"
                    )
                except OSError:
                    dir_info += f"[DIR] {folder} (Size unknown)\n"

            dir_info += (
                f"\nFILES ({len(files)}):\n"
                f"{'-' * 30}\n"
            )

            for filename in files:
                file_path = os.path.join(directory, filename)

                try:
                    file_size = os.path.getsize(file_path)
                    file_ext = (
                        os.path.splitext(filename)[1]
                        or "No extension"
                    )

                    dir_info += (
                        f"[FILE] {filename} "
                        f"({self.format_file_size(file_size)}) "
                        f"{file_ext}\n"
                    )
                except OSError:
                    dir_info += f"[FILE] {filename} (Size unknown)\n"

            self.set_text(self.info_text, dir_info)

            self.set_text(
                self.preview_text,
                "Select a file using Open File to preview its contents.",
                readonly=True
            )

            self.update_directory_info()

        except OSError as e:
            self.set_text(
                self.info_text,
                f"Error reading directory:\n{e}"
            )

            messagebox.showerror(
                "Error", f"Cannot read directory:\n{e}"
            )

    def get_directory_size(self, directory):
        total_size = 0

        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)

                try:
                    if not os.path.islink(filepath):
                        total_size += os.path.getsize(filepath)
                except OSError:
                    continue

        return total_size

    def create_file(self):
        filename = filedialog.asksaveasfilename(
            title="Create new file",
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("Python files", "*.py"),
                ("JSON files", "*.json"),
                ("All files", "*.*")
            ],
            initialdir=self.current_directory
        )

        if not filename:
            return

        try:
            if os.path.exists(filename):
                overwrite = messagebox.askyesno(
                    "File Exists",
                    f"'{os.path.basename(filename)}' already exists.\n"
                    "Do you want to overwrite it?"
                )

                if not overwrite:
                    return

            with open(filename, "w", encoding="utf-8") as file:
                file.write("")

            self.current_file = filename
            self.current_directory = os.path.dirname(filename)

            self.update_directory_info()
            self.show_file_info(filename)
            self.preview_file(filename)
            self.set_status(
                f"Created file: {os.path.basename(filename)}"
            )

            messagebox.showinfo(
                "Success",
                f"File created: {os.path.basename(filename)}"
            )

        except OSError as e:
            messagebox.showerror(
                "Error", f"Cannot create file:\n{e}"
            )

    def delete_file(self):
        if (
            not self.current_file
            or not os.path.isfile(self.current_file)
        ):
            messagebox.showwarning(
                "Warning",
                "Open or create a file before deleting it."
            )
            return

        filename = os.path.basename(self.current_file)

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{filename}'?\n\n"
            "This action cannot be undone."
        )

        if not confirm:
            return

        try:
            os.remove(self.current_file)

            deleted_file = filename
            self.current_file = None

            self.set_text(
                self.info_text,
                f"File '{deleted_file}' deleted successfully."
            )

            self.set_text(
                self.preview_text,
                "No file selected.",
                readonly=True
            )

            self.set_status(f"Deleted file: {deleted_file}")

            messagebox.showinfo(
                "Success",
                f"File '{deleted_file}' has been deleted."
            )

        except OSError as e:
            messagebox.showerror(
                "Error", f"Cannot delete file:\n{e}"
            )

    def refresh_view(self):
        if (
            self.current_file
            and os.path.isfile(self.current_file)
        ):
            self.show_file_info(self.current_file)
            self.preview_file(self.current_file)

        elif os.path.isdir(self.current_directory):
            self.show_directory_contents(
                self.current_directory
            )

        else:
            self.current_file = None
            self.current_directory = os.path.expanduser("~")
            self.update_directory_info()
            self.show_directory_contents(
                self.current_directory
            )

        self.set_status("View refreshed successfully.")

    def jalankan(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = FileExplorer()
    app.jalankan()
