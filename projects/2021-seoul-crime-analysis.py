## crime_data_analyzer

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import json
import folium
from matplotlib import font_manager, rc


class CrimeDataAnalyzer :
    """
    범죄 데이터를 로드하고 전처리하는 클래스입니다.
    여기서는 서울시 관서별 5대 범죄 발생 및 검거 데이터를 불러오고,
    경찰서 정보를 구별로 매핑합니다.
    """
    def __init__(self, crime_file, population_file) :
        self.crime_file = crime_file    #범죄 데이터 엑셀 파일 경로
        self.df = None    #원본 데이터가 저장될 DataFrame
        self.gu_df = None    #구별로 집계된 데이터가 저장될 DataFrame        
        self.population_file = population_file
        self.crime_count_norm = None    #정규화된 범죄 발생 건수 DataFrame
        self.crime_ratio = None    #인구 대비 범죄 비율 DataFrame


    def load_data(self) :
        """CSV 파일에서 범죄 데이터를 불러옵니다."""
        self.df = pd.read_csv(self.crime_file)
        print("\n데이터 로드 완료")
        print(self.df.head())
        print(self.df.info())

    def delete_data(self) :
        """불필요한 컬럼과 행을 삭제합니다."""
        self.gu_df = self.df.drop(columns = '자치구별(1)')    #'자치구별(1)' 컬럼 삭제
        self.gu_df.columns = ['구별', '소계(발생)', '소계(검거)', '살인(발생)', '살인(검거)', '강도(발생)', '강도(검거)', '강간·강제추행(발생)', '강간·강제추행(검거)', '절도(발생)', '절도(검거)', '폭력(발생)', '폭력(검거)']    #컬럼명 수정
        self.gu_df = self.gu_df[~self.gu_df['구별'].isin(['자치구별(2)', '소계'])]    #'구별'컬럼의 값이 '자치구별(2)','소계'인 행을 제외한 값만 남기기
        self.gu_df.set_index('구별', inplace=True)
        print("\n구별 데이터 정리")
        print(self.gu_df.head())
        for column in self.gu_df.columns :
          self.gu_df[column] = pd.to_numeric(self.gu_df[column], errors='coerce')    #컬럼별로 dtype object에서 int로 변환하기
      #  self.gu_df = self.gu_df.apply(pd.to_numeric, errors='coerce')    #방법2
        print("dtype : object -> int")
        print(self.gu_df.info())


## crime_data_merging : 범죄 데이터와 인구 데이터 병합

    def load_population_data(self) :
        """CSV 파일에서 구별 인구 데이터를 불러옵니다."""
        # 인구 데이터를 읽어 Dataframe으로 저장 (인덱스는 '구별')
        self.population_file = pd.read_csv(self.population_file, encoding='utf-8', index_col='구별')
        print("\n서울시 구별 인구 데이터")
        print(self.population_file.head())
        print(self.population_file.info())

    def merge_data(self) :
        """범죄 데이터와 인구 데이터를 병합합니다."""
        # 범죄 데이터와 인구 데이터 병합 (인덱스 기준)
        self.gu_df = self.gu_df.join(self.population_file)
        print("\nMerge data")
        print(self.gu_df.head())
        # 병합된 데이터를 CSV 파일로 저장
        self.gu_df.to_csv('merged_data.csv', encoding='utf-8-sig')


## crime_data_analyzing : 검거율 계산, 데이터 정규화, 인구 대비 범죄 비율 계산

    def calculate_arrest_rates(self) :
        """발생 건수 대비 검거 건수를 통해 검거율을 계산합니다."""
        # 각 범죄 유형벼 검거율 계산
        self.gu_df['살인검거율'] = self.gu_df['살인(검거)']/self.gu_df['살인(발생)']*100
        self.gu_df['강도검거율'] = self.gu_df['강도(검거)']/self.gu_df['강도(발생)']*100
        self.gu_df['강간·강제추행검거율'] = self.gu_df['강간·강제추행(검거)']/self.gu_df['강간·강제추행(발생)']*100
        self.gu_df['절도검거율'] = self.gu_df['절도(검거)']/self.gu_df['절도(발생)']*100
        self.gu_df['폭력검거율'] = self.gu_df['폭력(검거)']/self.gu_df['폭력(발생)']*100
        self.gu_df['검거율'] = self.gu_df['소계(검거)']/self.gu_df['소계(발생)']*100
        print("\n검거율 계산")
        print(self.gu_df.head())

    def clean_data(self) :
        """필요없는 컬럼을 삭제하고(범죄별 발생 건수와 검거율만 남기기) 검거율 데이터를 정리합니다"""
        # 불필요한 컬럼 제거
        #방법1 안되는 이유 찾아내기
        #del self.gu_df[['살인(검거)','강도(검거)','강간·강제추행(검거)','절도(검거)','폭력(검거)','소계(검거)','소계(발생)']]
        del self.gu_df['살인(검거)']
        del self.gu_df['강도(검거)']
        del self.gu_df['강간·강제추행(검거)']
        del self.gu_df['절도(검거)']
        del self.gu_df['폭력(검거)']
        del self.gu_df['소계(검거)']
        del self.gu_df['소계(발생)']
        print("\n범죄별 발생 건수 및 검거율")
        print(self.gu_df.head(10))

        # 검거율이 100%를 초과하면 100%로 수정 : 발생건수는 해당년도이고 그 전에 발생한 범죄에 대한 검거가 해당년도 검거수에 반영된 것
        #방법1
        self.gu_df[self.gu_df[['살인검거율','강도검거율','강간·강제추행검거율','절도검거율','폭력검거율','검거율']] > 100] = 100
        #방법2
        #self.gu_df[(self.gu_df['살인검거율']>100)|(self.gu_df['강도검거율']>100)|(self.gu_df['강간·강제추행검거율']>100)|(self.gu_df['절도검거율']>100)|(self.gu_df['폭력검거율']>100)|(self.gu_df['검거율']>100)] = 100
        print("\n100초과 검거율 확인")
        print(self.gu_df.head(10))

        self.gu_df.rename(columns = {'살인(발생)' : '살인',
                                     '강도(발생)' : '강도',
                                     '강간·강제추행(발생)' : '강간·강제추행',
                                     '절도(발생)' : '절도',
                                     '폭력(발생)' : '폭력'}, inplace = True)    #inplace옵션 == 덮어쓰기 여부
        print("\n컬럼명 수정")
        print(self.gu_df.head())

    def normalize_crime_data(self) :
        """범죄 데이터를 정규화하여 비교하기 쉽게 만듭니다."""
        # 각 범죄 유형별 최대값으로 나누어 정규화
        target_col = ['강간·강제추행', '강도', '살인', '절도', '폭력']
        weight_col = self.gu_df[target_col].max()
        print("\n범죄 유형별 최대값")
        print(weight_col)
        
        self.crime_count_norm = self.gu_df[target_col]/weight_col
        print(self.crime_count_norm)

        # 정규화된 데이터를 csv 파일로 저장
        self.crime_count_norm.to_csv('crime_count_norm.csv', encoding='utf-8-sig')

    def calculate_crime_ratio(self) :
        """인구 대비 범죄 발생 비율을 계산합니다."""
        # 정규화된 범죄 데이터를 인구수로 나누고 100,000을 곱하여 인구 대비 비율 계산
        self.crime_ratio = self.crime_count_norm.div(self.gu_df['인구수'], axis=0) * 100000
        print("\n인구 대비 범죄율")
        print(self.crime_ratio)

        # 전체 발생 비율 계산 (범죄 유형별 평균)
        self.crime_ratio['전체발생비율'] = self.crime_ratio.mean(axis=1)
        print("\n범죄 유형별 전체 발생 비율")
        print(self.crime_ratio.head())

        # 인구 대비 범죄 비율 데이터를 CSV 파일로 저장
        self.crime_ratio.to_csv("crime_ratio.csv", encoding ='utf-8-sig') 


## crime_data_visualizing : 히트맵과 지도 생성
    def setup_korean_font(self) :
        """그래프에서 한글이 깨지지 않도록 폰트를 설정합니다."""
        # 시스템에 설치된 한글 폰트 경로 설정
        font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
        # 폰트 이름 가져오기
        rc('font', family=font_name)

    def create_heatmap(self) :
        """범죄 발생 비율을 히트맵으로 시각화합니다."""
        # 정렬된 데이터를 기반으로 히트맵 생성
        plt.figure(figsize = (10, 10))
        sns.heatmap(self.crime_ratio.sort_values(by='전체발생비율', ascending=False), annot=True, fmt='f', linewidths=.5, cmap='Reds')
        print(plt.title('범죄 발생(전체발생비율로 정렬) - 각 항목을 정규화한 후 인구로 나눔'))
        print(plt.show())

    def create_folium_map(self) :
        """Folium을 사용하여 범죄 데이터를 지도에 시각화합니다."""
        # GeoJSON 파일 경로
        geo_path = '../data/skorea_municipalities_geo_simple.json'
        # GeoJSON 파일 로드
        geo_str = json.load(open(geo_path, encoding='utf-8'))
        # 지도 생성 (서울 중심)
        map = folium.Map(location=[37.5502, 126.982], zoom_start = 11, tiles = 'Cartodb Positron')
        # Choropleth 맵 생성 (살인 발생 건수 기준)
        folium.Choropleth(geo_data = geo_str,    # 서울시 행정구역별 polygon drawing
                          data = self.gu_df['살인'],    # 시각화의 대상이 될 데이터
                          columns = [self.gu_df.index, self.gu_df['살인']],    # df의 index 칼럼을 가져와 인식
                          fill_color = 'PuRd',    # PuRd, YLGnBu
                          key_on = 'feature.id').add_to(map)    # GeoJSON 규약을 따름, json 파일(지도 데이터)의 "feature" type의 "id"에 매칭
        # 지도 출력
        map.save("seoul_crime_map.html")


seoulcrime_2021 = CrimeDataAnalyzer('../data/2021_관서별_5대범죄.csv','../data/pop_kor.csv')
seoulcrime_2021.load_data()
seoulcrime_2021.delete_data()

seoulcrime_2021.load_population_data()
seoulcrime_2021.merge_data()

seoulcrime_2021.calculate_arrest_rates()
seoulcrime_2021.clean_data()
seoulcrime_2021.normalize_crime_data()

seoulcrime_2021.calculate_crime_ratio()

seoulcrime_2021.setup_korean_font()
seoulcrime_2021.create_heatmap()
seoulcrime_2021.create_folium_map()
