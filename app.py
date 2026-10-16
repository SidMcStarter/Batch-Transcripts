import tkinter as tk
from pathlib import Path
from tkinter import messagebox

from tkinterdnd2 import COPY, DND_FILES, TkinterDnD


def main():
    window = TkinterDnD.Tk()
    window.title('Batch Transcripts')
    window.geometry('480x310')

    content = tk.Frame(window, padx=20, pady=20)
    content.pack(fill='both', expand=True)

    drop_area = tk.Label(content, text='Drop a transcript PDF here', relief='groove', height=6)
    drop_area.pack(fill='x')

    file_label = tk.Label(content, text='Selected file: None', anchor='w')
    file_label.pack(fill='x', pady=(12, 0))
    tk.Label(content, text='Output folder: None', anchor='w').pack(fill='x', pady=(8, 0))

    selected_pdf = None

    def on_drop(event):
        nonlocal selected_pdf
        # Tcl lists preserve file paths containing spaces.
        files = window.tk.splitlist(event.data)
        if len(files) != 1:
            messagebox.showwarning('Invalid file', 'Please drop exactly one PDF file.')
            return 'none'

        pdf_path = Path(files[0])
        if not pdf_path.is_file() or pdf_path.suffix.lower() != '.pdf':
            messagebox.showwarning('Invalid file', 'Please drop exactly one PDF file.')
            return 'none'

        selected_pdf = pdf_path
        file_label.config(text=f'Selected file: {selected_pdf.name}')
        return COPY

    drop_area.drop_target_register(DND_FILES)
    drop_area.dnd_bind('<<Drop>>', on_drop)

    # These controls will be enabled when their actions are connected.
    tk.Button(content, text='Choose output folder', state='disabled').pack(pady=(16, 8))
    tk.Button(content, text='Split Transcripts', state='disabled').pack()

    window.mainloop()


if __name__ == '__main__':
    main()
