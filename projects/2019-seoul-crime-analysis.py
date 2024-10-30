# main.py

# 각 클래스 임포트
import matplotlib.pyplot as plt
import seaborn as sns
import json
import folium
from matplotlib import font_manager, rc
import pandas as pd
import numpy as np

class CrimeDataLoader:
    def __init__(self, crime_file):
        self.crime_file = crime_file
        self.df = None
        self.df_cleaned = None
        self.gu_df = None

    def load_data(self):
        self.df = pd.read_csv(self.crime_file)

    def map_police_to_district(self):
        self.df = self.df.drop(index=[0,1,2])
        self.df = self.df.drop(columns=["자치구별(1)"])
        self.df.columns = [
            "자치구", "전체(발생)", "전체(검거)",
            "살인(발생)", "살인(검거)",
            "강도(발생)", "강도(검거)",
            "강간·추행(발생)", "강간·추행(검거)",
            "절도(발생)", "절도(검거)",
            "폭력(발생)", "폭력(검거)"
        ]

        self.df = self.df.reset_index(drop=True)
        self.df_cleaned = self.df.drop([0]).copy()
        for col in self.df_cleaned.columns[1:]:
            self.df_cleaned[col] = pd.to_numeric(self.df_cleaned[col], errors='coerce')

        self.df_cleaned.set_index('자치구')

    def create_pivot_table(self):
        self.gu_df = pd.pivot_table(self.df_cleaned, index="자치구", aggfunc="sum")
        return self.gu_df

class CrimeDataMerger:
    def __init__(self, gu_df, population_file):
        self.gu_df = gu_df
        self.popul_df = None
        self.population_file = population_file

    def load_population_data(self):
        self.popul_df = pd.read_csv(self.population_file, encoding="utf-8")
        self.popul_df.rename(columns={"구별":"자치구"},inplace=True)
        self.popul_df = self.popul_df.set_index("자치구")

    def merge_data(self):
        self.gu_df = pd.merge(self.gu_df, self.popul_df, left_index=True, right_index=True)
        return self.gu_df

class CrimeDataAnalyzer:
    def __init__(self, gu_df):
        self.gu_df = gu_df
        self.weight_col = None# 병합된 데이터 DataFrame
        self.crime_count_norm = None    # 정규화된 범죄 발생 건수 DataFrame
        self.crime_ratio = None         # 인구 대비 범죄 비율 DataFrame

    def calculate_arrest_rates(self):
        self.gu_df['강간·추행(검거율)'] = self.gu_df['강간·추행(검거)'] / self.gu_df['강간·추행(발생)'] * 100
        self.gu_df['강도(검거율)'] = self.gu_df['강도(검거)']/self.gu_df['강도(발생)']*100
        self.gu_df['살인(검거율)'] = self.gu_df['살인(검거)']/self.gu_df['살인(발생)']*100
        self.gu_df['절도(검거율)'] = self.gu_df['절도(검거)']/self.gu_df['절도(발생)']*100
        self.gu_df['폭력(검거율)'] = self.gu_df['폭력(검거)']/self.gu_df['폭력(발생)']*100
        self.gu_df['전체(검거율)'] = self.gu_df['전체(검거)']/self.gu_df['전체(발생)']*100

    def clean_data(self):
        del self.gu_df['강간·추행(검거)']
        del self.gu_df['강도(검거)']
        del self.gu_df['살인(검거)']
        del self.gu_df['절도(검거)']
        del self.gu_df['폭력(검거)']
        del self.gu_df['전체(발생)']
        del self.gu_df['전체(검거)']

        self.gu_df[self.gu_df[["강간·추행(검거율)", "강도(검거율)", "살인(검거율)", "절도(검거율)", "폭력(검거율)", "전체(검거율)"]] > 100] = 100

        self.gu_df.rename(columns={'강간·추행(발생)': '강간·추행', '강도(발생)': '강도', '살인(발생)': '살인', '절도(발생)': '절도', '폭력(발생)': '폭력'}, inplace=True)  # inplace 옵션 == 덮어쓰기 여부

        self.gu_df.sort_values(by='전체(검거율)', ascending=False, inplace=True)

    def normalize_crime_data(self):
        self.weight_col = self.gu_df[['강간·추행', '강도', '살인', '절도', '폭력']].max()
        self.crime_count_norm = self.gu_df[['강간·추행', '강도', '살인', '절도', '폭력']] / self.weight_col

    def calculate_crime_ratio(self):
        self.crime_ratio = self.crime_count_norm.div(self.gu_df['인구수'], axis=0) * 100000

class CrimeDataVisualizer:
    def __init__(self, crime_ratio, gu_df):
        self.crime_ratio = crime_ratio
        self.font_name = None
        self.geo_path = None
        self.geo_str = None
        self.map = None
        self.gu_df = gu_df

    def setup_korean_font(self):
        self.font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
        rc('font', family=self.font_name)

    def create_heatmap(self):
        plt.figure(figsize=(10,10))
        self.crime_ratio['전체발생비율'] = self.crime_ratio.mean(axis=1)
        sns.heatmap(self.crime_ratio.sort_values(by="전체발생비율", ascending=False), annot=True, fmt="f", linewidths=.5, cmap="Reds")

        plt.title('범죄 발생(전체발생비율로 정렬) - 각 항목을 정규화한 후 인구로 나눔')
        plt.show()

    def create_folium_map(self):
        self.geo_path = "../data/skorea_municipalities_geo_simple.json"

        with open (self.geo_path, encoding='utf-8') as f:
            self.geo_str = json.load(f)

        self.map = folium.Map(location=[37.5502, 126.982], zoom_start=11, tiles='Cartodb Positron')

        folium.Choropleth(geo_data= self.geo_str, data=self.crime_ratio["전체발생비율"], columns=[self.crime_ratio.index, self.crime_ratio["전체발생비율"]],
                          fill_color= 'PuRd', key_on='feature.id').add_to(self.map)

        self.map.save("seoul_crime.map.html")



#
def main():
    # 1. 데이터 로드 및 전처리
    data_loader = CrimeDataLoader('../data/2019_관서별_5대범죄.csv')
    data_loader.load_data()
    data_loader.map_police_to_district()
    data_loader.create_pivot_table()

    # 2. 데이터 병합
    data_merger = CrimeDataMerger(data_loader.gu_df, '../data/pop_kor.csv')
    data_merger.load_population_data()
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