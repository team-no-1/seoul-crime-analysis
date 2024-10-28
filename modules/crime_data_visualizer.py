# modules/crime_data_visualizer.py

import matplotlib.pyplot as plt
import seaborn as sns
import json
import folium
from matplotlib import font_manager, rc

class CrimeDataVisualizer:
    """
    분석된 범죄 데이터를 시각화하는 클래스입니다.
    히트맵과 지도를 생성하여 데이터를 직관적으로 이해할 수 있게 합니다.
    """
    def __init__(self, crime_ratio, gu_df):
        self.crime_ratio = crime_ratio      # 인구 대비 범죄 비율 DataFrame
        self.gu_df = gu_df                  # 분석된 범죄 데이터 DataFrame

    def setup_korean_font(self):
        """그래프에서 한글이 깨지지 않도록 폰트를 설정합니다."""
        # 시스템에 설치된 한글 폰트 경로 설정

        # 폰트 이름 가져오기

        # 폰트 설정 적용

    def create_heatmap(self, sort_by='전체발생비율'):
        """범죄 발생 비율을 히트맵으로 시각화합니다."""

        # 정렬된 데이터를 기반으로 히트맵 생성

    def create_folium_map(self):
        """Folium을 사용하여 범죄 데이터를 지도에 시각화합니다."""
        # GeoJSON 파일 경로

        # GeoJSON 파일 로드

        # 지도 생성 (서울 중심) location 37.5802, 126.982 zoom_start = 11 tiles = 'Cartodb Positron'

        # Choropleth 맵 생성 (살인 발생 건수 기준)

        # 지도 저장(seoul_crime_map.html)
