import cv2
import mediapipe as mp
import matplotlib.pyplot as plt
import os

class FaceDetect():
    def __init__(self):
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
    
    def mp4_to_avi(self, input_video, output_video):
        # 원본 mp4 파일을 읽기 위한 비디오 캡처 객체 생성
        cap = cv2.VideoCapture(input_video)

        # 원본 mp4 파일의 속성 정보 가져오기
        fps = cap.get(cv2.CAP_PROP_FPS)  # 프레임 속도
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 프레임 너비
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 프레임 높이

        # avi 형식으로 변환하기 위한 비디오 라이터 객체 생성
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # 코덱 설정 (여기서는 MJPG 코덱 사용)
        out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

        # mp4 파일의 각 프레임을 읽어서 avi 파일에 쓰기
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # avi 파일에 프레임 쓰기
            out.write(frame)

        # 사용한 객체 해제
        cap.release()
        out.release()

        print(f'mp4 파일을 avi 형식으로 변환하여 {output_video}에 저장')
        return output_video

    def draw_box(self, frame, detection, boxColor=(255,0,0), thickness=2):
        # 랜드마크 점의 스타일 변경
        landmark_drawing_spec = self.mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=0, circle_radius=0)
            
        # 얼굴 박스의 스타일 변경
        bbox_drawing_spec = self.mp_drawing.DrawingSpec(color=boxColor, thickness=thickness)
        self.mp_drawing.draw_detection(frame, detection, landmark_drawing_spec, bbox_drawing_spec)

    def detection_to_image(self, frame, detection, boxSize=200):
        # 얼굴 부분만 잘라내기
        relative_bounding_box = detection.location_data.relative_bounding_box
        ymin = int(relative_bounding_box.ymin * frame.shape[0])
        xmin = int(relative_bounding_box.xmin * frame.shape[1])
        ymax = int((relative_bounding_box.ymin + relative_bounding_box.height) * frame.shape[0])
        xmax = int((relative_bounding_box.xmin + relative_bounding_box.width) * frame.shape[1])
        face = frame[ymin - boxSize:ymax + boxSize, xmin - boxSize:xmax + boxSize]
        return face
    
    def detect_face(self, frame, minDetectionConfidence=1, boxColor=(255,0,0)):
        face_lis = []
        
        # 얼굴 인식 모델 초기화
        face_detection = self.mp_face_detection(min_detection_confidence=minDetectionConfidence)
            
        # 프레임을 RGB로 변환
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 얼굴 인식 실행
        results = face_detection.process(rgb_frame)

        # 얼굴 인식 결과 그리기
        if results.detections:
            for detection in results.detections:
                # 경계 상자 그리기
                self.draw_box(frame, detection, box_color=boxColor)
                face_lis.append(self.detection_to_image(frame, detection))
        return face_lis
    
