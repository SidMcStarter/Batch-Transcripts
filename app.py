import tkinter as tk

from tkinterdnd2 import TkinterDnD


def main():
    window = TkinterDnD.Tk()
    window.title('Batch Transcripts')
    window.geometry('480x310')

    content = tk.Frame(window, padx=20, pady=20)
    content.pack(fill='both', expand=True)

    # This area will accept a PDF when drag-and-drop is added.
    drop_area = tk.Label(content, text='Drop a transcript PDF here', relief='groove', height=6)
    drop_area.pack(fill='x')

    tk.Label(content, text='Selected file: None', anchor='w').pack(fill='x', pady=(12, 0))
    tk.Label(content, text='Output folder: None', anchor='w').pack(fill='x', pady=(8, 0))

    # These controls will be enabled when their actions are connected.
    tk.Button(content, text='Choose output folder', state='disabled').pack(pady=(16, 8))
    tk.Button(content, text='Split Transcripts', state='disabled').pack()

    window.mainloop()


if __name__ == '__main__':
    main()
