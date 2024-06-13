from pathlib import Path

import json

folder_path = Path('./transcriptions')

all_transcriptions = dict()

for transcription_file in folder_path.iterdir():
    with transcription_file.open('r') as file:
        quadro = transcription_file.stem
        all_transcriptions[quadro] = json.load(file)
        
total = 0
for quadro, transcriptions in all_transcriptions.items():
    total += len(transcriptions)
print(f'Total transcriptions: {total}')