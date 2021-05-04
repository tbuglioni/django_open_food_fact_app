import requests


class ImportApi:
    """ import french products from api openfoodfact"""

    def __init__(self):
        self._page = None
        self._page_size = None
        self._actual_request = None
        self._status_code = None
        self._imported_file = None

    @property
    def page(self):
        return self._page

    @page.setter
    def page(self, new_value):
        self._page = new_value

    @property
    def page_size(self):
        return self._page_size

    @page_size.setter
    def page_size(self, new_value):
        self._page_size = new_value

    @property
    def actual_request(self):
        return self._actual_request

    @actual_request.setter
    def actual_request(self, new_value):
        self._actual_request = new_value

    @property
    def status_code(self):
        return self._status_code

    @status_code.setter
    def status_code(self, new_value):
        self._status_code = new_value

    @property
    def imported_file(self):
        return self._imported_file

    @imported_file.setter
    def imported_file(self, new_value):
        self._imported_file = new_value

    def __api_parameters(self, nbr_page=1, size_page=1000):
        """ define number of page and products to import"""
        self.page = nbr_page
        self.page_size = size_page

    def __api_connexion(self):
        """ create the connexion with the api"""
        try:
            payload = {
                "action": "process",
                "sort_by": "unique_scans_n",
                "page_size": self.page_size,
                "page": self.page,
                "json": 1,
            }
            self.actual_request = requests.get(
                "https://fr.openfoodfacts.org/cgi/search.pl?", params=payload
            )
            self.status_code = self.actual_request.status_code
        except requests.exceptions.ConnectionError:
            print(
                "connexion : Ooops there some troubles with the app, "
                "check internet connexion please"
            )

    def __import_products(self):
        """ import products from the api if connexion is OK"""
        if self.status_code == 200:
            results = self.actual_request.json()
            products = results["products"]
            self.imported_file = products
        else:
            print("get file : there no file to get, status code : ", self.status_code)

    def execute_import(self, nbr_page=1, size_page=1000):
        self.__api_parameters(nbr_page, size_page)
        self.__api_connexion()
        self.__import_products()
