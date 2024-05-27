import pandas as pd

class CountryDataProcessor:
    def __init__(self, file_path, delimiter=',', has_headers=True):
        try:
            self.dataframe = pd.read_csv(file_path, delimiter=delimiter, header=0 if has_headers else None)
        except FileNotFoundError as e:
            raise Exception(f"Не вдалося прочитати файл: {e}")
        except pd.errors.ParserError as e:
            raise Exception(f"Помилка парсингу файлу: {e}")

    def list_all_countries(self):
        return self.dataframe['Country'].tolist()

    def countries_larger_than_ukraine(self):
        if 'Ukraine' not in self.dataframe['Country'].values:
            raise Exception("Країна 'Ukraine' не знайдена в даних.")
        ukraine_area = self.dataframe[self.dataframe['Country'] == 'Ukraine']['Area (sq. mi.)'].values[0]
        larger_countries = self.dataframe[self.dataframe['Area (sq. mi.)'] > ukraine_area]
        return larger_countries[['Country', 'Area (sq. mi.)']]

    def countries_population_greater_than_10m_and_larger_than_ukraine(self):
        if 'Ukraine' not in self.dataframe['Country'].values:
            raise Exception("Країна 'Ukraine' не знайдена в даних.")
        ukraine_area = self.dataframe[self.dataframe['Country'] == 'Ukraine']['Area (sq. mi.)'].values[0]
        filtered_countries = self.dataframe[(self.dataframe['Population'] > 10000000) &
                                            (self.dataframe['Area (sq. mi.)'] > ukraine_area)]
        return filtered_countries[['Country', 'Population', 'Area (sq. mi.)']]

    def top_10_countries_by_gdp(self):
        top_countries = self.dataframe.nlargest(10, 'GDP ($ per capita)')
        return top_countries[['Country', 'GDP ($ per capita)']]

    def countries_without_sea_access(self):
        landlocked_countries = self.dataframe[self.dataframe['Coastline (coast/area ratio)'] == 0]
        return landlocked_countries[['Country', 'Coastline (coast/area ratio)']]

file_path = 'D:/countries_of_the_world.csv'
processor = CountryDataProcessor(file_path)


print("Список всіх країн:")
print(processor.list_all_countries())


try:
    print("\nКраїни з більшою площею ніж в Україні:")
    print(processor.countries_larger_than_ukraine())
except Exception as e:
    print(f"Помилка: {e}")


try:
    print("\nКраїни з населенням понад 10 млн та з більшою площею ніж в Україні:")
    print(processor.countries_population_greater_than_10m_and_larger_than_ukraine())
except Exception as e:
    print(f"Помилка: {e}")


print("\nТоп 10 країн за ВВП:")
print(processor.top_10_countries_by_gdp())


print("\nКраїни, які не мають доступу до моря:")
print(processor.countries_without_sea_access())
