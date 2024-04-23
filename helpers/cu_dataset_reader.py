"""read CU dataset reader to identify council name and dataset id"""

import pandas as pd
from PyPDF2 import PdfReader


class CuDatasetReader():
    """read cu dataset pdf"""

    def __init__(self, file_path='./settings/cu_dataset.pdf') -> None:
        self.file_path = file_path
        self.row_identifier = 'support@sacommu'
        self.page_header_identifier = 'https://sacommunity.org/admin/settings/datasets'

    def remove_texts(self, text: str, texts_to_remove: list[str]):
        """remove texts from text"""
        for text_to_remove in texts_to_remove:
            text = text.replace(text_to_remove, '')

        return text

    def read_cu_dataset_settings_pdf(self, return_dataframe=False):
        """read CU dataset: CU datasets settings _ SAcommunity - Connecting Up Australia.pdf"""
        texts_to_remove = [
            self.row_identifier,
            self.page_header_identifier,
            'nity.org',
            'support@sacommu'
        ]

        reader = PdfReader(self.file_path)
        total_pages = len(reader.pages)
        datasets = []
        for i, page in enumerate(reader.pages):
            page_lines = page.extract_text().splitlines()

            for page_line in page_lines:
                if self.page_header_identifier in page_line:
                    page_number = f'{i+1}/{total_pages}'
                    texts_to_remove.append(page_number)
                if self.row_identifier in page_line:
                    row_text = self.remove_texts(page_line, texts_to_remove)
                    row_text = row_text.split()
                    row_text = [s.strip() for s in row_text]
                    dataset_id = row_text[0]
                    council_name = ' '.join(row_text[1:])
                    datasets.append({'dataset_id': dataset_id,
                                    'council_name': council_name})

        if return_dataframe:
            return pd.DataFrame(datasets)

        return datasets

    def search_dataset_id_from_council_name(self, council_name: str):
        """search dataset pdf for council and returns dataset id"""
        datasets = self.read_cu_dataset_settings_pdf(return_dataframe=False)
        # return datasets_df[datasets_df["council_name"].str.contains(council_name, case=False)]
        datasets = [
            d for d in datasets if council_name in d['council_name'].lower()]
        if len(datasets) == 0:
            return None

        return datasets[0]
