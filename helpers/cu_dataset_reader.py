"""read CU dataset reader to identify council name and dataset id"""

import pandas as pd
from PyPDF2 import PdfReader

CU_DATASET_ROW_IDENTIFIER = 'support@sacommu'
CU_DATASET_PAGE_HEADER_IDENTIFIER = 'https://sacommunity.org/admin/settings/datasets'

def remove_texts(text: str, texts_to_remove: list[str]):
    """remove texts from text"""
    for text_to_remove in texts_to_remove:
        text = text.replace(text_to_remove, '')

    return text

def read_cu_dataset_settings_pdf(file_path: str, return_dataframe=False):
    """read CU dataset: CU datasets settings _ SAcommunity - Connecting Up Australia.pdf"""
    texts_to_remove = [
        CU_DATASET_ROW_IDENTIFIER,
        CU_DATASET_PAGE_HEADER_IDENTIFIER,
        'nity.org',
        'support@sacommu'
    ]

    reader = PdfReader(file_path)
    total_pages = len(reader.pages)
    datasets = []
    for i, page in enumerate(reader.pages):
        page_lines = page.extract_text().splitlines()

        for page_line in page_lines:
            if CU_DATASET_PAGE_HEADER_IDENTIFIER in page_line:
                page_number = f'{i+1}/{total_pages}'
                texts_to_remove.append(page_number)
            if CU_DATASET_ROW_IDENTIFIER in page_line:
                row_text = remove_texts(page_line, texts_to_remove)
                row_text = row_text.split()
                row_text = [s.strip() for s in row_text]
                dataset_id = row_text[0]
                council_name = ' '.join(row_text[1:])
                datasets.append({'dataset_id': dataset_id,
                                'council_name': council_name})

    if return_dataframe:
        return pd.DataFrame(datasets)

    return datasets
