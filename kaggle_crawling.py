import kaggle
import os
import pandas as pd
import logger

def download_kaggle_dataset():
    # automatically find credential file for authentication
    kaggle.api.authenticate()

    # API를 통해 제공하는 String에 있는 dataset을 다운로드
    # 파일을 저장할 PATH와 데이터파일이 zip인 경우 unzip 옵션 선택
    dataset_path = 'octopusteam/full-netflix-dataset'
    kaggle.api.dataset_download_files(dataset_path, force=True, path='data_CSV', unzip=True)

    # 파일 이름명 변경
    os.replace('data_CSV/data.csv', 'data_CSV/kaggle_data.csv')

    logger.logging.info("kaggle 데이터 파일이 저장되었습니다.")

def delete_URL_row():
    #CSV 파일 읽어오기
    file_path = 'data_CSV/kaggle_data.csv'
    df = pd.read_csv(file_path)

    # 삭제할 행의 인덱스를 지정합니다. 0부터 시작
    index_to_delete = 0  

    # 해당 행을 삭제합니다.
    df = df.drop(index_to_delete)

    # 삭제된 데이터를 새로운 CSV 파일로 저장합니다.
    df.to_csv(file_path, index=False)

    logger.logging.info(f"{index_to_delete + 1}번째 행이 삭제되고 '{file_path}'로 저장되었습니다.")

def extract_data_availableCountries_KR():
    # CSV 파일 읽기
    df = pd.read_csv('data_CSV/kaggle_data.csv') 

    # 'title' 열에서 값이 없는 행 제거
    df = df.dropna(subset=['title'])  # 'title' 열에 값이 없는 행 제거

    # 'availableCountries' 열 찾기
    if 'availableCountries' in df.columns:
        # 'availableCountries' 열에서 각 나라 코드가 있는 셀을 가져옴
        countries_column = df['availableCountries']
        
        # 'KR'을 포함하는 행 찾기
        kr_rows = countries_column.str.contains('KR', na=False)  # 'KR'이 포함된 행 찾기
        
        # 필터링된 DataFrame 생성
        filtered_df = df[kr_rows]  # 'KR'이 포함된 행만 선택

        # 결과를 새로운 CSV 파일로 저장
        filtered_df.to_csv('data_CSV/kaggle_data_avaliable_in_KR.csv', index=False)
        
        logger.logging.info("필터링 된 kaggle data 파일이 저장되었습니다.")
    else:
        logger.logging.error("availableCountries 열을 찾을 수 없습니다.")