"""read CU dataset reader to identify council name and dataset id"""

import pandas as pd
from PyPDF2 import PdfReader

def remove_texts(text: str, texts_to_remove: list[str]):
    """remove texts from text"""
    for text_to_remove in texts_to_remove:
        text = text.replace(text_to_remove, '')

    return text

def read_cu_dataset_settings_pdf(file_path: str, return_dataframe=False):
    """read CU dataset: CU datasets settings _ SAcommunity - Connecting Up Australia.pdf"""
    row_identifier = 'support@sacommu'
    page_header_identifier = 'https://sacommunity.org/admin/settings/datasets'
    texts_to_remove = [
        row_identifier,
        page_header_identifier,
        'nity.org',
        'support@sacommu'
    ]

    reader = PdfReader(file_path)
    total_pages = len(reader.pages)
    datasets = []
    for i, page in enumerate(reader.pages):
        page_extract = page.extract_text()
        page_lines = page_extract.splitlines()

        for pl in page_lines:
            if page_header_identifier in pl:
                page_number = f'{i+1}/{total_pages}'
                texts_to_remove.append(page_number)
            if row_identifier in pl:
                pps = remove_texts(pl, texts_to_remove)
                pps_split = pps.split()
                pps_split = [s.strip() for s in pps_split]
                dataset_id = pps_split[0]
                council_name = ' '.join(pps_split[1:])
                datasets.append({'dataset_id': dataset_id,
                                'council_name': council_name})

    if return_dataframe:
        return pd.DataFrame(datasets)

    return datasets

# remove_texts('fdas', ['d'])
