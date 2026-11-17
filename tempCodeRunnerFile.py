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