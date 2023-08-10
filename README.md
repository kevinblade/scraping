# WSL2 + Docker + Python + Scraping (BeautifulSoap4, Playwright)

## 프로젝트 목적
- 개발 운영체계: WSL2 Ubuntu 20.04
- Docker 컨테이너에 Python 개발 환경을 설치
- WSL3 VSCode로 편집, 디버깅, 로컬 프로젝트 폴더와 컨테이더 프로젝트 폴더의 동기화
- 매번 Build 과정없이 로컬에서 변경된 소스를 컨테이너 내부의 debugpy로 원격 디버깅
- Python으로 개발 가능한 다양한 스크래핑 패키지들을 테스트

## 디버깅 방법
- 리포지토리 폴더에서
$ docker compose build
- VSCode 상에서 "Python: Attach BS4" 또는 "Python: Attach Playwright"를 선택 후 디버깅 진행
