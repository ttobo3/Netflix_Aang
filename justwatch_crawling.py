from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import re
import csv
import global_variables as gv
import logger

def set_webDriver():
    # Selenium WebDriver 설정 
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu') # GPU 가속 비활성화
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--enable-unsafe-swiftshader")
    options.add_argument("--use-gl=swiftshader")  # 소프트웨어 렌더링 사용
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    options.add_experimental_option("detach", True)

    # ChromeDriver 경로 설정 (필요 시 수정)
    driver = webdriver.Chrome(options=options)

    return driver

def scroll_down_page(driver, program_num, use_key):
    url_set = set()  # 중복 방지를 위한 집합
    actions = ActionChains(driver)
    body = driver.find_element(By.TAG_NAME, 'body')
    
    while True:
        if use_key:
            # PAGE_DOWN 키를 이용해 스크롤 내리기
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(10)  # 스크롤 후 잠시 대기
        else:
            # 스크롤 내리기
            actions.scroll_by_amount(0, 1000).perform()
            time.sleep(10)  # 페이지 로딩 시간 대기
        
        # 스크롤 중 URL을 실시간으로 수집
        programs = driver.find_elements(By.TAG_NAME, 'a')
        url_set.update([a.get_attribute('href') for a in programs if a.get_attribute('href')])
        logger.logging.info(f"수집된 URL 개수: {len(url_set)}")
        
        # 'timeline__end-of-timeline' 요소가 있는지 확인
        if use_key:
            if len(url_set) >= program_num:
                logger.logging.info("End of timeline reached.")
                break
        else:
            try:
                driver.find_element(By.CLASS_NAME, 'timeline__end-of-timeline')
                logger.logging.info("End of timeline reached.")
                break  # 요소가 있으면 종료
            except:
                pass  # 요소가 없으면 계속 진행   
    
    return list(url_set)

def close_setting_window(driver, url):
    # 해당 url로 이동
    driver.get(url)

    # 페이지 로딩 대기
    time.sleep(3)

    try:
        # shadow DOM에 접근하여 버튼 클릭
        shadow_host = driver.find_element(By.ID, 'usercentrics-root')
        shadow_root = driver.execute_script('return arguments[0].shadowRoot', shadow_host)
        # 설정 저장 버튼 확인
        save_button = shadow_root.find_element(By.CLASS_NAME, "sc-dcJsrY.dQaUXI")
        save_button.click()

        time.sleep(3)

        gv.clicked_save_button = True

    except Exception as e:
        if gv.clicked_save_button:
            logger.logging.info("이미 설정이 저장되어있습니다.")
        else:
            logger.logging.error(f"설정 저장에 오류가 있습니다. {e}")

def save_contents_url(driver):
    url = "https://www.justwatch.com/kr/%EB%8F%99%EC%98%81%EC%83%81%EC%84%9C%EB%B9%84%EC%8A%A4/netflix"
    close_setting_window(driver, url)

    wait = WebDriverWait(driver, 60)

    # 페이지가 로드될 때까지 대기
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'title-poster')))

    # 예시 클래스명 "mx-2" 요소 찾기
    program_num_element = driver.find_element(By.CLASS_NAME, "mx-2")

    # 요소의 텍스트 가져오기
    program_num_text = program_num_element.text

    # 숫자만 추출하기
    program_num = int(re.sub(r'[^\d]', '', program_num_text))
    logger.logging.info(f"총 영상 개수: {program_num}개")

    # URL 크롤링 시작
    logger.logging.info("컨텐츠 링크를 크롤링 중...")
    #Scroll down 하는게 page-down 키 누르는 것보다 효율적인듯
    url_list = scroll_down_page(driver, program_num, use_key = False)
    logger.logging.info(f"수집된 URL 개수: {len(url_list)}")

    logger.logging.info("URL 크롤링 완료")
    return url_list

def is_valid_url(url):
    # URL을 슬래시로 분리
    parts = url.split('/')

    # 마지막 부분이 유효한 카테고리인지 확인
    if len(parts) >= 3:  # 최소 3개의 부분이 있어야 함
        category = parts[-2]  # 마지막 카테고리 부분 추출
        return category in gv.valid_categories
        
    return False

def get_type_from_website(driver): 
    # just watch category -> kaggle type
    # 드라마 -> tv, 영화 -> movie
    categories = driver.find_elements(By.CLASS_NAME, 'title-detail__title')
    category = 'N/A'
    for cate in categories:
        if cate.text.endswith('정보'):
            category = cate.text.split()[0]
            if category == '영화':
                category = 'movie'
            elif category == '드라마':
                category = 'tv'
            return category
    return category

def get_type_n_ENtitle_from_url(url):
    # URL을 슬래시로 분리
    parts = url.split('/')
    ctgy = parts[-2]  # 마지막 카테고리 부분 추출
    if ctgy == gv.valid_categories[0]:
        ctgy = 'movie'
    else:
        ctgy =  'tv'
    
    enTitle = parts[-1]

    return ctgy, enTitle

def get_KOtitle_n_ORGtitle(driver):
    title_element = driver.find_element(By.CLASS_NAME, 'title-detail-hero__details__title')
    koTitle = title_element.text[:-7] if title_element else 'N/A'

    original_title_element = driver.find_elements(By.CLASS_NAME, 'original-title')
    orgTitle = original_title_element[0].text.replace("원제: ", "") if original_title_element else 'N/A'

    return koTitle, orgTitle

def get_release_year(driver):
    yr = 'N/A'
    try:
        yr = driver.find_element(By.CLASS_NAME, 'release-year').text[1:5]
    except:
        pass
    return yr

def get_detail_infos(driver):
    koGenres, runtime, age_rating, ctry, dirc = 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'
    details = driver.find_elements(By.CLASS_NAME, "detail-infos")
    for detail in details:
        if '장르' in detail.text:
            koGenres = detail.text[3:]
        elif '재생 시간' in detail.text:
            runtime = detail.text[6:]
        elif '연령 등급' in detail.text:
            age_rating = detail.text[6:]
        elif '제작 국가' in detail.text:
            ctry = detail.text[6:]
        elif '감독' in detail.text:
            dirc = detail.text[3:]
    
    # 장르 kaggle과 매칭되도록 영어로 변경
    input_genres_list = [genre.strip() for genre in koGenres.split(',')]
    mapped_genres_en = [gv.genre_mapping.get(genre, "Unknown") for genre in input_genres_list]
    enGenres = ', '.join(mapped_genres_en)

    return koGenres, enGenres, runtime, age_rating, ctry, dirc

def convert_length_in_mins(length):
    # 값이 NaN 또는 float일 경우 None을 반환
    if not isinstance(length, str) or length == 'N/A':
        return None  # NaN 또는 숫자형이 있을 경우 None 처리
    
    # 시간과 분을 추출하는 정규식 패턴
    time_pattern = re.compile(r'(?:(\d+)\s*시간\s*)?(\d+)\s*분')
    
    # 입력 문자열에서 시간과 분을 추출
    match = time_pattern.match(length.strip())
    
    if match:
        # 시간과 분을 추출
        hours = match.group(1)  # 시간 부분
        minutes = match.group(2)  # 분 부분
        
        # 시간 부분이 None이면 0시간으로 처리
        hours = int(hours) if hours else 0
        minutes = int(minutes)
        
        # 총 분으로 계산 (시간 * 60 + 분)
        total_minutes = hours * 60 + minutes
        return total_minutes
    
    else:
        # 유효하지 않은 형식의 경우 None을 반환
        return None

def get_imbd_rates(driver):
    score, votes = 'N/A', 'N/A'
    try:
        imdb_text = driver.find_element(By.CLASS_NAME, 'imdb-score').text.strip()
        imdb_match = re.match(r'([\d.]+)\s+\(([\dk]+)\)', imdb_text)
        score = imdb_match.group(1) if imdb_match else 'N/A'
        votes = imdb_match.group(2) if imdb_match else 'N/A'
    except:
        pass

    return score, votes

def get_avaliable_platforms(driver):
    isAvaliable = False
    platforms = set()
    offer_options = driver.find_elements(By.CLASS_NAME, "offer__icon")
    platforms.update([o.get_attribute('alt') for o in offer_options if o.get_attribute('alt')])
    if len(platforms - {"Netflix", "Netflix basic with Ads"}) > 0:
        isAvaliable = True
    platformLists = ', '.join(platforms)

    return isAvaliable, platformLists

def get_ranking_data(driver):
    bestRank, top10, top100, top1000 = 'N/A', 'N/A', 'N/A', 'N/A'
    chart_info = driver.find_elements(By.CLASS_NAME, "title-chart-info__item")
    for info in chart_info:
        info_text = info.text
        if "최고 순위:" in info_text:
            bestRank = int(info_text.split(":\n")[1].strip().rstrip('.'))
        elif "Top 10:" in info_text:
            top10 = info_text.split(":\n")[1].strip()
        elif "Top 100:" in info_text:
            top100 = info_text.split(":\n")[1].strip()
        elif "Top 1000:" in info_text:
            top1000 = info_text.split(":\n")[1].strip()

    return bestRank, top10, top100, top1000

def crawl_justWatch(driver, read_limit, limit_num, request_wait):
    wait = WebDriverWait(driver, 20)

    # 데이터 저장을 위한 리스트
    data = []
    # 에러가 난 url 저장을 위한 리스트
    error_url = []

    # URL 파일 로드
    with open('data_CSV/url_list.csv', 'r') as url_file:
        urls = set([line.strip() for line in url_file])
    
    # 각 컨텐츠 url에서 데이터 저장
    for index, url in enumerate(urls):
        try:
            # URL 접근
            driver.get(url)
            time.sleep(1)  # 페이지 로드 시간을 위해 짧은 대기

            # "설정 저장" 버튼 처리 여부 확인
            if not gv.clicked_save_button:
                close_setting_window(driver, url)
                gv.clicked_save_button = True

            # 페이지 로드 대기
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'title-detail-hero__details__title')))

            # 0. 타입 (영화 또는 TV)
            #category = get_type_from_website(driver)

            # 0-1. 타입 & 제목_EN
            category, en_title = get_type_n_ENtitle_from_url(url)

            # 1. 제목_KO, 원제
            ko_title, original_title = get_KOtitle_n_ORGtitle(driver)
            
            # 2. 제작 연도
            year = get_release_year(driver)

            # 3-6. 세부 정보
            genres_KO, genres_EN, length, rating, country, director = get_detail_infos(driver)
            # 재생 시간 min 값으로 변경


            # 7. IMDb 스코어
            imdb_score, imdb_votes = get_imbd_rates(driver)

            # 8. 타플랫폼 시청 가능 여부
            isAvaliable, platform_lists = get_avaliable_platforms(driver)

            # 9. Ranking
            best_rank, top10_period, top100_period, top1000_period = get_ranking_data(driver)

            # 수집된 데이터 저장
            row = {
                'title': en_title,
                'title_KO': ko_title,
                'title_ORG': original_title,
                'type': category,
                'genres': genres_EN,
                'genres_KO': genres_KO,
                'releaseYear': year,
                'length': length,
                'ratings': rating,
                'production_countries': country,
                'imdbAverageRating': imdb_score,
                'imdbNumVotes': imdb_votes,
                'isAvaliableInDifferentPlatform': isAvaliable,
                'platforms': platform_lists,
                'director': director,
                'best_rank': best_rank,
                'top10_period' : top10_period,
                'top100_period' : top100_period,
                'top1000_period' : top1000_period
            }
            
            data.append(row)
            logger.logging.info(f"{index + 1}. '{en_title}' 데이터 수집 완료.")
            
        except Exception as e:
            error_url.append(url)
            logger.logging.error(f"{index + 1}번째 URL에서 오류 발생: {e}")
            continue
        
        # 테스트를 위해 일정 데이터만 읽는 경우
        if read_limit and index == limit_num:
            break

        # Too many request error 방지
        if index !=0 and index % request_wait == 0:
            # driver.quit()
            # time.sleep(5)
            # driver = set_webDriver()
            # gv.clicked_save_button = False
            time.sleep(60)
            
    return data, error_url

def save_data_into_CSV(data, file_path, isDataDict):
    # 데이터 저장
    if data:
        with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
            if isDataDict:
                keys = data[0].keys()
                dict_writer = csv.DictWriter(csvfile, fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(data)
            else:
                writer = csv.writer(csvfile)
                writer.writerow(['url'])  # 헤더 작성
                for d in data:
                    writer.writerow([d])  # 각 data를 개별 셀로 저장
        logger.logging.info("데이터가 CSV 파일로 저장되었습니다.")
    else:
        logger.logging.error("수집된 데이터가 없습니다.")
