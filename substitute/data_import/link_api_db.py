from substitute.data_import.api.cleaner import Cleaner
from substitute.data_import.api.import_api import ImportApi
from substitute.data_import.database.adder import Adder


class LinkApiDb:
    """manager to : API and DATABASE
    make a link between them"""

    def __init__(self):
        self.importer = ImportApi()
        self.cleaner = Cleaner()
        self.adder = Adder()

    def add_in_table(self, page_min, nbr_of_page):
        """download, clean and add in db, product from api"""

        for elt in range(nbr_of_page):
            # download
            self.importer.execute_import(page_min)
            imported_file_status = self.importer.status_code
            imported_file = self.importer.imported_file

            # clean
            self.cleaner.get_imported_file(imported_file, imported_file_status)
            self.cleaner.spliter()
            cleaned_file = self.cleaner.get_cleaned_list()

            # add in db
            self.adder.get_cleaned_list(cleaned_file)
            self.adder.add_in_all_tables(page_min, nbr_of_page)
            self.cleaner.delete_cleaned_list()
            page_min += 1
