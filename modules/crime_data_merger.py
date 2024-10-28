# modules/crime_data_merger.py

import pandas as pd

class CrimeDataMerger:
    """
    범죄 데이터와 인구 데이터를 병합하는 클래스입니다.
    이를 통해 인구 대비 범죄 발생률을 분석할 수 있습니다.
    """
    def __init__(self, gu_df, population_file):
        self.gu_df = gu_df                      # 범죄 데이터 DataFrame
        self.population_file = population_file  # 인구 데이터 CSV 파일 경로

    def load_population_data(self):
        """CSV 파일에서 구별 인구 데이터를 불러옵니다."""
        # 인구 데이터를 읽어 DataFrame으로 저장 (인덱스는 '구별')

    def merge_data(self):
        """범죄 데이터와 인구 데이터를 병합합니다."""
        # 인구 데이터 로드

        # 범죄 데이터와 인구 데이터 병합 (인덱스 기준)

        # 병합된 데이터를 CSV 파일로 저장

