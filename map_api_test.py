import unittest
import requests

BASE_URL = "https://regions-test.2gis.com/1.0/regions"


class TestRegionsAPI(unittest.TestCase):

    def make_request(self, params=None):
        response = requests.get(BASE_URL, params=params)
        self.assertEqual(response.status_code, 200)
        return response.json()

    # Тест получения всех регионов
    def test_get_all_regions(self):
        response_data = self.make_request()
        self.assertIn("total", response_data)
        self.assertIn("items", response_data)
        self.assertIsInstance(response_data["items"], list)

    # Тест значения 'page_size' по умолчанию
    # Проверяет, что по умолчанию значение параметра page_size=15
    def test_default_page_size(self):
        response_data = self.make_request()
        self.assertEqual(len(response_data["items"]), 15)

    # Тест фильтрации регионов по коду страны
    # Проверяет, что все регионы в ответе принадлежат указанной стране
    def test_filter_by_country(self):
        params = {"country_code": "ru"}
        response_data = self.make_request(params)
        for item in response_data["items"]:
            self.assertEqual(item["country"]["code"], "ru")

    # Тест поиска регионов по названию.
    def test_search_by_name(self):
        params = {"q": "нов"}
        response_data = self.make_request(params)
        for item in response_data["items"]:
            self.assertIn("нов", item["name"].lower())

    # Тест поиска при пустом параметре 'q'
    # Проверяет, что API корректно обрабатывает пустые строки в параметре 'q'
    def test_search_nothing_name(self):
        params = {"q": ""}
        response_data = self.make_request(params)
        self.assertIn("Параметр 'q' должен быть не менее 3 символов",
                      response_data["error"]["message"])

    # Тест постраничного вывода
    # Проверяет, что количество элементов на странице не превышает указанное значение
    def test_pagination(self):
        params = {"page": 1, "page_size": 5}
        response_data = self.make_request(params)
        self.assertLessEqual(len(response_data["items"]), 5)

    # Тест обработки неправильных параметров
    # Проверяет, что при неправильном значении параметра 'country_code' возвращается ошибка с описанием
    def test_invalid_params(self):
        params = {"country_code": "asd"}
        response_data = self.make_request(params)
        self.assertIn("Параметр 'country_code' может быть одним из следующих значений: ru, kg, kz, cz",
                      response_data["error"]["message"])

    # Тест минимального значения параметра 'page'.
    def test_min_page_value(self):
        params = {"page": 1}
        response_data = self.make_request(params)
        self.assertIn("items", response_data)

    # Тест максимального значения параметра 'page_size'
    def test_max_page_size_value(self):
        params = {"page_size": 15}
        response_data = self.make_request(params)
        self.assertLessEqual(len(response_data["items"]), 15)

    # Тест фильтрации регионов по коду страны 'kz'
    # Проверяет, что все регионы в ответе принадлежат указанной стране 'kz'
    def test_kz_region(self):
        params = {"country_code": "kz"}
        response_data = self.make_request(params)
        for item in response_data["items"]:
            self.assertEqual(item["country"]["code"], "kz")

    # Тест максимального значения параметра 'q'.
    # Проверяет, что API корректно обрабатывает длинные строки в параметре 'q'
    def test_max_length_search_query(self):
        params = {"q": "a" * 31}
        response_data = self.make_request(params)
        self.assertIn("Параметр 'q' должен быть не более 30 символов",
                      response_data["error"]["message"])

    # Тест меньше минимального значения параметра 'q'.
    # Проверяет, что API корректно обрабатывает короткие строки в параметре 'q'
    def test_min_length_search_query(self):
        params = {"q": "a" * 2}
        response_data = self.make_request(params)
        self.assertIn("Параметр 'q' должен быть не менее 3 символов",
                      response_data["error"]["message"])

    #  Тест отсутствия результатов по параметру 'q'
    #  Проверяет, что ответ содержит пустой список 'items'
    def test_no_results_for_query(self):
        params = {"q": "zzz"}
        response_data = self.make_request(params)
        self.assertEqual(len(response_data["items"]), 0)

    # Тест нулевого значения параметра 'page'
    # Проверяет, что API возвращает ошибку с описанием при значении 'page' равному 0
    def test_zero_page_value(self):
        params = {"page": 0}
        response_data = self.make_request(params)
        self.assertIn("Параметр 'page' должен быть больше 0",
                      response_data["error"]["message"])

    # Тест отрицательного значения параметра 'page'
    # Проверяет, что API возвращает ошибку с описанием при значении 'page' меньше 0
    def test_negative_page_value(self):
        params = {"page": -1}
        response_data = self.make_request(params)
        self.assertIn("Параметр 'page' должен быть больше 0",
                      response_data["error"]["message"])

    # Тест вещественного значения параметра 'page'
    # Проверяет, что API возвращает ошибку с описанием при нецелочисленном значении 'page'
    def test_int_page_value(self):
        params = {"page": 1.5}
        response_data = self.make_request(params)
        self.assertIn("Параметр 'page' должен быть целым числом",
                      response_data["error"]["message"])

    # Тест неправильного значения параметра 'page_size'
    # Проверяет, что API возвращает ошибку с описанием при значении 'page_size' отличным от 5, 10, 15
    def test_invalid_page_size_value(self):
        params = {"page_size": 20}
        response_data = self.make_request(params)
        self.assertIn("Параметр 'page_size' может быть одним из следующих значений: 5, 10, 15",
                      response_data["error"]["message"])


if __name__ == "__main__":
    unittest.main()
