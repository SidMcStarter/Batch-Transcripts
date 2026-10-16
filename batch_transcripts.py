import pymupdf
from pathlib import Path
import re
import os

def get_batch_transcript(folder):
    files = os.listdir(folder)
    for file in files:
        if file.lower().endswith('.pdf'):
            pdf_path = os.path.join(folder, file)
            doc = pymupdf.open(pdf_path)
            return doc

def return_adjusted_name(name):
    name_parts = name.split()
    first_name = name_parts[0]
    last_name = name_parts[-1]
    name = f"{last_name.upper()} {first_name}"
    return name


def get_student_information(input_folder):
    doc = get_batch_transcript(input_folder)
    id_list = []
    student_information = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        student_id = re.findall(r'\b\d{7}\b', text)
        start = None
        end = None
        name = None
        if page_num > -1:
            start = text.find('Student Name:') + len('Student Name:')
            end = text.find('(Surname last)')
            name = text[start:end].strip()
            name = return_adjusted_name(name)
            #print(name)
        if student_id:
            student_id = student_id[0]
            if student_id not in id_list:
                id_list.append(student_id)
                student_information.append({'id': student_id, 'name': name})
    #print(student_information)
    return student_information

#get_ids()


def divide_transcripts(input_folder, output_folder):
    doc = get_batch_transcript(input_folder)
    student_information = get_student_information(input_folder)
    file_number = 0

    for student in student_information:
        id = student['id']
        file_number += 1
        start_page = None
        transcript_name = student['name'] + ' ' + id
        count = 0
        
        for page_num in range(len(doc)):
            page = doc[page_num] 
            text = page.get_text()

            if id in text:
                count += 1
                start_page = page_num

        output_pdf = pymupdf.open()
        output_pdf.insert_pdf(
            doc,
            from_page=start_page - count + 1,
            to_page=start_page
        )
        file_name = f"{transcript_name}.pdf"
        output_pdf.save(str(output_folder / file_name))
        output_pdf.close()
    doc.close()

def main():
    data_folder = Path(__file__).resolve().parent / 'data'
    input_folder = data_folder / 'input'
    output_folder = data_folder / 'output'
    divide_transcripts(input_folder, output_folder)


if __name__ == '__main__':
    main()
