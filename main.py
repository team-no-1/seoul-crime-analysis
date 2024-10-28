# main.py

# 각 클래스 임포트
from modules.crime_data_loader import CrimeDataLoader
from modules.crime_data_merger import CrimeDataMerger
from modules.crime_data_analyzer import CrimeDataAnalyzer
from modules.crime_data_visualizer import CrimeDataVisualizer

def main():
    # 1. 데이터 로드 및 전처리
    data_loader = CrimeDataLoader('data/관서별 5대범죄 발생 및 검거.xlsx')
    data_loader.load_data()
    data_loader.map_police_to_district()
    data_loader.create_pivot_table()

    # 2. 데이터 병합
    data_merger = CrimeDataMerger(data_loader.gu_df, 'data/pop_kor.csv')
    gu_df = data_merger.merge_data()

    # 3. 데이터 분석
    data_analyzer = CrimeDataAnalyzer(gu_df)
    data_analyzer.calculate_arrest_rates()
    data_analyzer.clean_data()
    data_analyzer.normalize_crime_data()
    data_analyzer.calculate_crime_ratio()

    # 4. 데이터 시각화
    data_visualizer = CrimeDataVisualizer(data_analyzer.crime_ratio, data_analyzer.gu_df)
    data_visualizer.setup_korean_font()
    data_visualizer.create_heatmap()
    data_visualizer.create_folium_map()

if __name__ == '__main__':
    main()
