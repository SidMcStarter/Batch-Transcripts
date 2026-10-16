# Transcript Splitter

A small Windows desktop app for splitting a batch transcript PDF into individual student PDFs. Select a PDF by dragging it into the window or clicking the drop area, choose an output folder, then click **Split Transcripts**.

## Build the Windows EXE

Install Python (tested with Python 3.12). After cloning the repository or downloading and extracting its ZIP, open PowerShell in the folder containing `app.py` and run:

```powershell
py -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m PyInstaller --noconfirm --onefile --windowed --name TranscriptSplitter --collect-all tkinterdnd2 app.py
```

The executable will be at `dist\TranscriptSplitter.exe`. The `--collect-all tkinterdnd2` option includes the files needed for drag-and-drop. PyInstaller also creates `build\` and `TranscriptSplitter.spec`; these are generated build files.

## Run the app

Double-click `dist\TranscriptSplitter.exe`, or from the same PowerShell window run:

```powershell
.\dist\TranscriptSplitter.exe
```

You can also run the Python version after installing the requirements:

```powershell
.\venv\Scripts\python.exe app.py
```

The app asks you to choose an output folder; it does not require an input folder. PDF files and generated transcripts stay in the locations you select. The built EXE can run on a Windows computer without installing Python.
