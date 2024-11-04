import logging
import sys

# 로깅 설정
logging.basicConfig(
    level=logging.DEBUG,  # 로깅 레벨 설정
    format='%(asctime)s - %(levelname)s - %(message)s',  # 로그 포맷 설정
    handlers=[
        logging.FileHandler('log/output.log'),  # 기본 로그 파일 핸들러
        logging.StreamHandler(sys.stdout)     # 터미널 출력 핸들러
    ]
)

# 추가적인 핸들러 설정
file_handler1 = logging.FileHandler('log/program_info.log')
file_handler2 = logging.FileHandler('log/program_error.log')
file_handler3 = logging.FileHandler('log/program_debug.log')

# 각각의 핸들러에 대한 레벨 설정 (선택 사항)
file_handler1.setLevel(logging.INFO)
file_handler2.setLevel(logging.ERROR)
file_handler3.setLevel(logging.DEBUG)

# 핸들러를 로거에 추가
logger = logging.getLogger()
logger.addHandler(file_handler1)
logger.addHandler(file_handler2)
logger.addHandler(file_handler3)