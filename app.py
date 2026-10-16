from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from tkinterdnd2 import COPY, DND_FILES, TkinterDnD

from batch_transcripts import divide_transcripts


def main():
    window = TkinterDnD.Tk()
    window.title('Batch Transcripts')
    window.geometry('540x380')
    window.configure(bg='#f6f8fb')

    # The built-in clam theme lets the small set of colors work consistently.
    style = ttk.Style(window)
    style.theme_use('clam')
    style.configure('TFrame', background='#f6f8fb')
    style.configure('TLabel', background='#f6f8fb', foreground='#334155', font=('Segoe UI', 10))
    style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'), foreground='#0f172a')
    style.configure('Hint.TLabel', foreground='#64748b')
    style.configure('Drop.TLabel', background='white', foreground='#2563eb',
                    padding=(16, 34), relief='solid', borderwidth=1)
    style.configure('TButton', padding=(10, 7), font=('Segoe UI', 10))
    style.configure('Primary.TButton', background='#2563eb', foreground='white',
                    padding=(16, 10), font=('Segoe UI', 10, 'bold'), borderwidth=0)
    style.map('Primary.TButton', background=[('pressed', '#1e40af'), ('active', '#1d4ed8')])

    content = ttk.Frame(window, padding=24)
    content.pack(fill='both', expand=True)

    ttk.Label(content, text='Batch Transcripts', style='Title.TLabel',
              anchor='w').pack(fill='x')
    ttk.Label(content, text='Choose a PDF and where to save the split files.',
              style='Hint.TLabel', anchor='w').pack(fill='x', pady=(4, 0))

    drop_area = ttk.Label(content, text='Drop a transcript PDF here or click to browse',
                          style='Drop.TLabel', anchor='center', cursor='hand2')
    drop_area.pack(fill='x', pady=(20, 0))

    file_label = ttk.Label(content, text='Selected file: None', anchor='w',
                           justify='left', wraplength=480)
    file_label.pack(fill='x', pady=(16, 0))

    output_row = ttk.Frame(content)
    output_row.pack(fill='x', pady=(12, 0))
    output_label = ttk.Label(output_row, text='Output folder: None', anchor='w',
                             justify='left', wraplength=300)
    output_label.pack(side='left', fill='x', expand=True)

    selected_pdf = None
    output_folder = None

    def select_pdf(path):
        nonlocal selected_pdf
        pdf_path = Path(path)
        if pdf_path.is_dir():
            messagebox.showwarning('Folder selected', 'Choose a PDF file, not a folder.')
            return False
        if not pdf_path.is_file():
            messagebox.showwarning('File not found', 'That file is not available. Choose an existing PDF.')
            return False
        if pdf_path.suffix.lower() != '.pdf':
            messagebox.showwarning('Not a PDF', f'{pdf_path.name} is not a PDF. Choose a .pdf file.')
            return False

        selected_pdf = pdf_path
        file_label.config(text=f'Selected file: {selected_pdf.name}')
        return True

    def choose_pdf(event):
        options = {}
        if selected_pdf and selected_pdf.parent.is_dir():
            options['initialdir'] = str(selected_pdf.parent)
        filename = filedialog.askopenfilename(
            parent=window, title='Choose transcript PDF',
            filetypes=[('PDF files', '*.pdf')], **options
        )
        if filename:  # Cancelling keeps the current selection.
            select_pdf(filename)

    drop_area.bind('<Button-1>', choose_pdf)

    def on_drop(event):
        # Tcl lists preserve file paths containing spaces.
        files = window.tk.splitlist(event.data)
        if not files:
            messagebox.showwarning('No file dropped', 'Drop one PDF file or click to browse.')
            return 'none'
        if len(files) > 1:
            messagebox.showwarning('Too many files', f'You dropped {len(files)} files. Drop one PDF at a time.')
            return 'none'

        return COPY if select_pdf(files[0]) else 'none'

    drop_area.drop_target_register(DND_FILES)
    drop_area.dnd_bind('<<Drop>>', on_drop)

    def choose_output_folder():
        nonlocal output_folder
        options = {}
        if output_folder and output_folder.is_dir():
            options['initialdir'] = str(output_folder)
        folder = filedialog.askdirectory(parent=window, title='Choose output folder', **options)
        if folder:  # Keep the previous choice if the dialog is cancelled.
            output_folder = Path(folder)
            output_label.config(text=f'Output folder: {output_folder}')

    ttk.Button(output_row, text='Choose output folder', command=choose_output_folder).pack(
        side='right', padx=(12, 0)
    )

    def split_transcripts():
        if selected_pdf is None:
            messagebox.showwarning('No PDF selected', 'Drop a transcript PDF or click the drop area to browse.')
            return
        if output_folder is None:
            messagebox.showwarning('No output folder selected', 'Click Choose output folder before splitting.')
            return
        if not selected_pdf.is_file():
            messagebox.showerror('PDF not found', 'The selected PDF is no longer available. Choose it again.')
            return
        if not output_folder.is_dir():
            messagebox.showerror('Output folder not found', 'The output folder is no longer available. Choose another folder.')
            return

        try:
            divide_transcripts(selected_pdf, output_folder)
        except Exception as error:
            messagebox.showerror('Split failed',
                                 f'Could not split {selected_pdf.name}.\n\nReason: {error}\n\n'
                                 'Check the PDF and that you can save files in the output folder.')
            return

        messagebox.showinfo('Finished', f'Transcripts saved to:\n{output_folder}')

    ttk.Button(content, text='Split Transcripts', command=split_transcripts,
               style='Primary.TButton').pack(
        side='bottom', anchor='e'
    )

    window.mainloop()


if __name__ == '__main__':
    main()
