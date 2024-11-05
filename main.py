import kaggle_crawling as kg
import justwatch_crawling as jw
import pandas as pd
import logger

def get_kaggle_data():
    # Kaggle 데이터 가져오기
    kg.download_kaggle_dataset()
    # 필요 없는 데이터 제거
    kg.delete_URL_row()
    kg.extract_data_availableCountries_KR()

def get_justwatch_data():
    # JustWatch 데이터 가져오기
    # web-driver 세팅
    driver = jw.set_webDriver()
    
    # url-list 뽑기
    url_data = jw.save_contents_url(driver)
    valid_url_data = [url for url in url_data if jw.is_valid_url(url)]
    jw.save_data_into_CSV(valid_url_data, 'data_CSV/url_list.csv', isDataDict=False)
    
    # url-list 기반 데이터 추출
    #테스트를 위해 일정 개수만 읽는 경우 set read_limit = True and 원하는 limit_num (0부터 시작)
    jw_data, read_error_urls = jw.crawl_justWatch(driver, read_limit=False, limit_num = 5, request_wait=10) 
    jw.save_data_into_CSV(jw_data, 'data_CSV/justwatch_data.csv', isDataDict=True)
    logger.logging.info(f"크롤링 하지 못한 컨텐츠 {len(read_error_urls)}개 나왔습니다.")
    
    driver.quit()

def create_merge_data(): # key 값 매칭 확인 용 함수
    df1 = pd.read_csv('data_CSV/justwatch_data.csv', encoding='utf-8-sig')  
    df2 = pd.read_csv('data_CSV/kaggle_data_avaliable_in_KR.csv', encoding='utf-8-sig')  

    # 'title' 열과 'title_ORG' 열을 기준으로 두 DataFrame을 병합
    merged_df = pd.merge(df1, df2, left_on='title_ORG', right_on='title', how='inner')

    # 결과를 새로운 Excel 파일로 저장
    merged_df.to_csv('data_CSV/merged_output.csv', index=False, encoding='utf-8-sig')

    logger.logging.info("두 데이터를 병합한 파일이 저장되었습니다.")

def add_running_time_mins_coloum():
    df = pd.read_csv('data_CSV/justwatch_data.csv', encoding='utf-8-sig') 

    # 'length' 열에 time_to_minutes 함수 적용하여 새로운 열 'length_in_minutes' 추가
    df['length_in_minutes'] = df['length'].apply(jw.convert_length_in_mins)

    # 결과를 새로운 Excel 파일로 저장
    df.to_csv('data_CSV/justwatch_data_edited.csv', index=False, encoding='utf-8-sig')

    logger.logging.info("length 열을 분으로 치환한 데이터가 저장되었습니다.")

def choose_crawl_option():
    # 사용자 입력 받기
    print("어떤 작업을 수행하시겠습니까?")
    print("1: Kaggle 데이터 가져오기")
    print("2: JustWatch 데이터 가져오기")
    print("3: 두 가지 모두 수행하기")
    print("4: 두 개의 데이터 병합 확인하기")
    print("5: 러닝 타임 분(minutes) 값으로 치환한 열 추가하기")
    
    choice = int(input("번호를 입력하세요 (1/2/3/4/5): ").strip())

    if choice == 1:
        get_kaggle_data()
    
    elif choice == 2:
        get_justwatch_data()
    
    elif choice == 3:
        get_kaggle_data()
        get_justwatch_data()

    elif choice == 4:
        create_merge_data()
    
    elif choice == 5:
        add_running_time_mins_coloum()

    else:
        logger.logging.error("잘못된 입력입니다. 올바른 숫자를 입력해주세요.")

if __name__ == "__main__":
    choose_crawl_option()
