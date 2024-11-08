# Netflix_Aang


### 📝 1. 프로젝트 소개

**프로젝트 목표**
- Netflix 및 기타 OTT 플랫폼에서 제공되고 있는 콘텐츠에 대한 인사이트를 제공할 수 있는 대시보드 구축

**프로젝트 기대 효과**
- 장르, 플랫폼, 감독 등 컨텐츠의 트렌드 파악
- imdb 평가 지표를 활용한 컨텐츠 분석

**프로젝트 요약**
1) 데이터 수집
    - JustWatch와 Kaggle에서 데이터를 수집하고 통합
    - 약 1,000개의 콘텐츠에 대한 포괄적인 데이터셋을 생성

2) 데이터 적재
    - AWS의 다양한 서비스를 활용하여 데이터 파이프라인을 구축

3) 대시보드 생성
    - Preset을 사용하여 다양한 인사이트를 제공하는 대시보드를 개발

4) 데이터 분석
    - 전체 콘텐츠, 국가별, 플랫폼별, 감독별 대시보드를 통해 콘텐츠의 다양한 측면을 분석

<br>

### 🖥️ 2. 활용 기술
|분야|기술|
|--------|----------|
|**Language**|Python, SQL|
|**Crawling**|Selenium, Pandas|
|**Data Pipeline**|AWS S3, Redshift Serverless|
|**BI**|Preset|
|**Collaboration**|Github, Zep, Slack, Notion|

<br>

### 🌳 3. 프로젝트 구조
![](/images/structure.png)
**데이터 수집**
- Kaggle API
- Justwatch Scrapping

**데이터 적재**
- 데이터 레이크: AWS S3
- 데이터 웨어하우스: AWS Redshift

**데이터 시각화**
- Preset.io

<br>

## 🎯 4. 프로젝트 결과
- 장르 분석
![genres](/images/genres.png)

<br>

- 국가 분석
![country](/images/country.png)

<br>

- 플랫폼 분석
![platform](/images/platform.png)

<br>

- 감독 분석
![directors](/images/directors.png)
![directors_zack](/images/directors_zack.png)
*preset의 filter 기능을 사용해 감독별로 대시보드를 확인할 수 있다.*

<br>

- [Canva 최종 결과물 보고서](https://www.canva.com/design/DAGVx9UGsUE/buLpSzDZces6_w0joXTIIQ/edit?utm_content=DAGVx9UGsUE&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)
