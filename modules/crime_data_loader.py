# modules/crime_data_loader.py

import pandas as pd
import numpy as np

class CrimeDataLoader:
    """
    범죄 데이터를 로드하고 전처리하는 클래스입니다.
    여기서는 서울시 관서별 5대 범죄 발생 및 검거 데이터를 불러오고,
    경찰서 정보를 구별로 매핑합니다.
    """
    def __init__(self, crime_file):
        self.crime_file = crime_file  # 범죄 데이터 엑셀 파일 경로
        self.df = None  # 원본 데이터가 저장될 DataFrame
        self.gu_df = None  # 구별로 집계된 데이터가 저장될 DataFrame

    def load_data(self):
        """엑셀 파일에서 범죄 데이터를 불러옵니다."""

    def map_police_to_district(self):
        """경찰서별 데이터를 구별로 매핑하여 '구별' 컬럼을 추가합니다."""
        # 경찰서와 구의 매핑 정보 딕셔너리

        # '관서명'을 기준으로 구별 매핑 적용

    def create_pivot_table(self):
        """구별로 데이터를 집계하여 피벗 테이블을 생성합니다."""
        # '구별'을 인덱스로 설정하고 데이터 합계 계산

        # 매핑되지 않은 '구 없음' 행 제거
