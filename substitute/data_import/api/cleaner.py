class Cleaner:
    def __init__(self):
        """clean all products imported from the api"""
        self.imported_file = None
        self.cleaned_list = []

    def get_imported_file(self, file_to_get, status_code):
        """get previous import from api--> attribut and check status code"""
        if status_code == 200:
            self.imported_file = file_to_get

    @staticmethod
    def __cleaner_mono_entry(text_to_check):
        """clean 1 element without split"""
        return str(text_to_check).lower().strip()

    @staticmethod
    def __cleaner_multiples_entry(product_to_clean):
        """clean x elements with split (list)"""
        mini_str = str(product_to_clean).lower()
        mini_list = mini_str.split(",")
        cleaned_list = [elt.strip() for elt in mini_list]
        return cleaned_list

    def spliter(self):
        """split and clean all products from api"""
        if self.imported_file is not None:
            for product in self.imported_file:
                try:
                    if (
                        product["product_name"]
                        and product["nutrition_grades"]
                        and product["stores"]
                        and product["categories"]
                        and product["url"]
                        and product["image_url"]
                    ):
                        new_name = self.__cleaner_mono_entry(product["product_name"])
                        new_nutrition_grades = self.__cleaner_mono_entry(
                            product["nutrition_grades"]
                        )
                        new_stores = self.__cleaner_mono_entry(product["stores"])
                        new_categories = self.__cleaner_multiples_entry(
                            product["categories"]
                        )
                        new_url = product["url"]
                        new_img = product["image_url"]
                        self.cleaned_list.append(
                            {
                                "name": new_name,
                                "nutriscore": new_nutrition_grades,
                                "store": new_stores,
                                "categories": new_categories,
                                "url": new_url,
                                "img": new_img,
                            }
                        )

                except KeyError:
                    pass

    def get_cleaned_list(self):
        """return the list after split & clean"""
        return self.cleaned_list

    def delete_cleaned_list(self):
        """delete the attribut with le list cleaned"""
        self.cleaned_list = []
