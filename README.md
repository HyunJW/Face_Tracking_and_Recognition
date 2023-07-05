# Face_Tracking_and_Recognition

### 수행 기간 : 2023.06.12 - 2023.07.10

## 데이터 출처
- AI Hub: 마스크 착용 한국인 안면 이미지 데이터 (https://aihub.or.kr/aihubdata/data/view.do?currMenu=&topMenu=&aihubDataSe=realm&dataSetSn=469)

## 사용한 언어 및 라이브러리, 프레임워크
- Python
  - torch, torchvision, PIL, pandas, os, numpy, cv2, module, mediapipe
- HTML, JS
- MySQL
- Django

## 순서
#### 1. 모델 학습용 데이터 수집 및 처리
  - 악세사리(모자, 마스크 등)를 착용하지 않은 컬러 데이터만 사용
  - 정면사진 1장 + 다각도 스튜디오 사진 8장 사용

#### 2. 얼굴 인식 모델을 이용한 이미지 전처리
  - 영상에서 안면만 추출
  - 배경 제거

#### 3. 얼굴 매칭 모델 학습 및 구축
  - SiameseNetwork 모델 채택

#### 4. DB생성
  - 회원 정보 DB
  - 전체 출결 DB
  - 학원 정보 DB
  - 수업 정보 DB 

#### 5. Django를 이용한 서비스 구현
  - 회원 정보와 학원, 수업 정보 연결
  - 회원 정보와 특정 날짜의 출결 정보 연결


## 개선사항
- 회원 정보에 입력된 사진과 CCTV 상의 사진의 매칭 정확도 개선
- CCTV 에 인식되는 시간과 순서에 따라 자동으로 출결 외에 외출, 조퇴, 지각등 여러가지 사유 추가 필요
- 악세사리(모자, 마스크 등) 착용 여부와 상관없이 인식 가능한 모델 구축 필요

