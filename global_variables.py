# 전역 변수 초기화
clicked_save_button = False 
valid_categories = ["%EC%98%81%ED%99%94", "TV-%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%A8"] #영화, TV-프로그램
genre_en = ['Crime', 'History', 'Fantasy', 'Sci-Fi', 'Western', 'Anime', 'Horror', 'Comedy', 'Reality-TV', 'Dramas', 'Romance', 'Family', 'Sport', 'War', 'Action', 'Documentary', 'Music', 'Thriller']
genre_kr = ['범죄', '역사', '판타지', 'SF', '서부', '애니메이션', '공포', '코미디', 'Reality TV', '드라마', '로맨스', '가족', '스포츠', '전쟁', '액션', '다큐멘터리', '음악', '스릴러']
# 한국어 장르와 영어 장르를 매핑하는 딕셔너리 생성
genre_mapping = dict(zip(genre_kr, genre_en))