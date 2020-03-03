# Part 1: Data Exploration
# 1.2.
import exam
year_to_anomaly_dict = exam.read_year_to_anomaly_data('data/Land_and_Ocean_summary.txt')
print(year_to_anomaly_dict)
print(f'The anomaly value for 2018 is: {year_to_anomaly_dict[2018]}')

# 1.3.
exam.create_line_plot(year_to_anomaly_dict, 'anomalies_per_year.png')

# Part 2: Stripes
# 2.1
color_mapper = exam.ColorMapper(year_to_anomaly_dict)
print(color_mapper.get_color(0.0))

# 2.2
year_blocks = exam.construct_blocks(year_to_anomaly_dict)
exam.plot_blocks(year_blocks, color_mapper,colorbar=True,figure_width=20, figure_height=5)

# 2.3
anomalies_per_decade = exam.calculate_anomalies_per_decade(year_to_anomaly_dict)
print(anomalies_per_decade)

# Part 3: Looking at Latitudes
# 3.1. 
latitude_year_to_anomaly_dict = exam.read_latitude_year_to_anomaly_data('data/anomalies_per_latitude.txt')
print(latitude_year_to_anomaly_dict)
print(f'The anomaly value for latitude 87.5, year 2018 is: {latitude_year_to_anomaly_dict[87.5][2018]}')

# 3.2
latitude_year_anomalies = exam.get_values_from_nested_dict(latitude_year_to_anomaly_dict)
print(latitude_year_anomalies)
color_mapper_latitudes = exam.ColorMapper(latitude_year_anomalies)
print(color_mapper_latitudes)

# 3.3
year_latitude_blocks = exam.construct_latitude_blocks(latitude_year_to_anomaly_dict)
print(year_latitude_blocks)

# 4.2
top10_emitting_countries = exam.find_top10_emitting_countries('data/annual-co-emissions-by-region.csv')
print(top10_emitting_countries)
exam.plot_emissions(top10_emitting_countries, population_dict=None, figure_width=15, figure_height=5)

# 4.3
population_dict = exam.read_population_data('data/population.csv', 1850)
print(population_dict)
