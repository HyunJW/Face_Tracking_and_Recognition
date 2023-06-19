import mediapipe as mp

class FacePositionDetect():
    def __init__(self):
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_face_mesh = mp.solutions.face_mesh
        
        self.face_detection = self.mp_face_detection.FaceDetection()
        self.face_mesh = self.mp_face_mesh.FaceMesh()

    def estimate_face_direction(self, face_landmarks):
        left_eye = face_landmarks.landmark[133]
        right_eye = face_landmarks.landmark[362]
        nose = face_landmarks.landmark[1]
        mouth_left = face_landmarks.landmark[61]
        mouth_right = face_landmarks.landmark[291]
        
        # 눈과 코의 상대적인 위치를 분석하여 얼굴 방향을 추정합니다.
        eye_distance = right_eye.x - left_eye.x
        nose_position = nose.x
        mouth_width = mouth_right.x - mouth_left.x

        # 얼굴 방향 추정 로직을 구현합니다.
        if eye_distance < 0.17 and nose_position < 0.45 and mouth_width < 0.24:
            face_direction = "left"
        elif eye_distance < 0.17 and nose_position > 0.6 and mouth_width < 0.24:
            face_direction = "right"
        else:
            face_direction = "front"

        return face_direction

    def face_position(self, img):
        results_detection = self.face_detection.process(img)

        if results_detection.detections:
            results_mesh = self.face_mesh.process(img)

            if results_mesh.multi_face_landmarks:
                for face_landmarks in results_mesh.multi_face_landmarks:
                    face_direction = self.estimate_face_direction(face_landmarks)
        return face_direction