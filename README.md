# Face_Tracking_and_Recognition

### 안면인식 및 안면매칭 영상처리 프로젝트

<hr>

### 수행 기간 : 2023.06.12 - 2023.07.10

## 주제
 - 학원의 출석과 퇴실 시간에 카드 태깅 혹은 어플을 이용한 출결 체크로 인한 혼잡한 상황을 예방하기 위해 안면 인식을 통한 출석 관리 서비스 구축

## 데이터 출처
- AI Hub: 마스크 착용 한국인 안면 이미지 데이터 (https://aihub.or.kr/aihubdata/data/view.do?currMenu=&topMenu=&aihubDataSe=realm&dataSetSn=469)

## 사용한 언어 및 라이브러리, 프레임워크
#### 언어
<div align="left">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white"/>
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white"/>
  <img src="https://img.shields.io/badge/JavaScript-323330?style=flat-square&logo=javascript&logoColor=F7DF1E"/> 
</div>

#### 데이터베이스
<div align="left">
  <img src="https://img.shields.io/badge/MySQL-005C84?style=flat-square&logo=mysql&logoColor=white"/>
</div>

#### 프레임워크
<div align="left">
  <img src="https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=green"/>
  <img src="https://img.shields.io/badge/Bootstrap-563D7C?style=flat-square&logo=bootstrap&logoColor=white"/>
  <img src="https://img.shields.io/badge/conda-342B029.svg?&style=flat-square&logo=anaconda&logoColor=white"/>
  <img src="https://img.shields.io/badge/Jupyter-F37626.svg?&style=flat-square&logo=Jupyter&logoColor=white"/>
</div>

#### 라이브러리
<div align="left">
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white"/>
  <img src="https://img.shields.io/badge/Keras-FF0000?style=flat-square&logo=keras&logoColor=white"/>
  <img src="https://img.shields.io/badge/OpenCV-27338e?style=flat-square&logo=OpenCV&logoColor=white"/>
  <img src="https://img.shields.io/badge/Mediapipe?&style=flat-square&logo=Mediapipe&logoColor=white"/>
</div>
<div align="left">
  <img src="https://img.shields.io/badge/Pandas-2C2D72?style=flat-square&logo=pandas&logoColor=white"/>
  <img src="https://img.shields.io/badge/Numpy-777BB4?style=flat-square&logo=numpy&logoColor=white"/>
  <img src="https://img.shields.io/badge/json-5E5C5C?style=flat-square&logo=json&logoColor=white"/>
  <img src="https://img.shields.io/badge/pillow?&style=flat-square&logo=pillow&logoColor=white"/>
  <img src="https://img.shields.io/badge/os?&style=flat-square&logo=os&logoColor=white"/>
</div>
<div align="left">
  <img src="https://img.shields.io/badge/itertools?style=flat-square&logo=itertools&logoColor=green"/>
  <img src="https://img.shields.io/badge/math?style=flat-square&logo=math&logoColor=white"/>
  <img src="https://img.shields.io/badge/threading?&style=flat-square&logo=threading&logoColor=white"/>
  <img src="https://img.shields.io/badge/apscheduler?&style=flat-square&logo=apscheduler&logoColor=white"/>
  <img src="https://img.shields.io/badge/datetime?&style=flat-square&logo=datetime&logoColor=white"/>
</div>

## 순서
#### 1. 모델 학습용 데이터 수집 및 처리
  - 악세사리(모자, 마스크 등)를 착용하지 않은 컬러 데이터만 사용
  - 정면사진 1장 + 다각도 스튜디오 사진 8장 사용

#### 2. 얼굴 인식 모델을 이용한 이미지 전처리
  - 영상에서 안면만 추출
  - 배경 제거

#### 3. 얼굴 매칭 모델 학습 및 구축
  - SiameseNetwork 모델 채택
  - Triplet Loss 및 Contrastive Loss 채택

#### 4. 데이터베이스 구축
  - 회원 정보 테이블
  - 전체 출결 테이블
  - 학원 정보 테이블
  - 수업 정보 테이블
  - 수업 시간표 테이블
  - 수강 목록 테이블

#### 5. Django를 이용한 서비스 구현
  - 회원 관리 기능 추가
  - 회원 정보와 학원, 수업 정보 연결
  - 회원 정보와 특정 날짜의 출결 정보 연결


## 개선사항
- 회원 정보에 입력된 사진과 CCTV 상의 사진의 매칭 정확도 개선
- CCTV 에 인식되는 시간과 순서에 따라 자동으로 출결 외에 외출, 조퇴, 지각등 여러가지 사유 추가 필요
- 악세사리(모자, 마스크 등) 착용 여부와 상관없이 인식 가능한 모델 구축 필요

