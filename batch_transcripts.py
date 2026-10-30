import pymupdf
from pathlib import Path
import csv
import re
import os

def get_batch_transcript(pdf_path):
    return pymupdf.open(str(pdf_path))

def return_adjusted_name(name):
    name_parts = name.split()
    first_name = name_parts[0]
    last_name = name_parts[-1]
    name = f"{last_name.upper()} {first_name}"
    return name


def get_student_information(pdf_path, courses_csv_path=None):
    doc = get_batch_transcript(pdf_path)
    id_list = []
    student_information = []
    student_courses = {}

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        student_id = re.findall(r'\b\d{7}\b', text)
        transfer_courses = re.findall(r'Granted credit\s*([\s\S]*?)\s*for\s+work\s+completed', text)
        if student_id:
            courses = student_courses.setdefault(student_id[0], [])
            if transfer_courses:
                courses.append(transfer_courses[0])
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
    doc.close()
    if courses_csv_path:
        get_transfer_credit(student_courses, courses_csv_path)
    return student_information

#get_ids()


def get_transfer_credit(student_courses, csv_path):
    pattern = r'\b(?:[A-Z]{4}|[A-Z]{2}[ \t]+[A-Z]{2}|[A-Z]{5})\s+\d{3}\b'
    rows = []

    for student_id, text_list in student_courses.items():
        combined_text = ' '.join(text_list)
        courses = [re.sub(r'\s+', ' ', match) for match in re.findall(pattern, combined_text)]

        for index, course in enumerate(courses):
            rows.append({'ID': student_id if index == 0 else '', 'Course': course})

    with open(csv_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['ID', 'Course'])
        writer.writeheader()
        writer.writerows(rows)


def divide_transcripts(pdf_path, output_folder, export_courses=False):
    doc = get_batch_transcript(pdf_path)
    courses_csv_path = output_folder / 'courses.csv' if export_courses else None
    student_information = get_student_information(pdf_path, courses_csv_path)
    if not student_information:
        doc.close()
        raise ValueError('No seven-digit student IDs were found. Choose a batch transcript PDF.')
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
    for file in os.listdir(input_folder):
        if file.lower().endswith('.pdf'):
            divide_transcripts(input_folder / file, output_folder, export_courses=True)
            break


if __name__ == '__main__':
    main()
