import cv2
import numpy as np
from deepface import DeepFace
import os

class CatEmotionDisplay:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.emotion_to_cat = {
            'happy': 'happy_cat.jpg',
            'sad': 'sad_cat.jpg',
            'angry': 'angry_cat.jpg',
            'surprise': 'surprised_cat.jpg',
            'neutral': 'neutral_cat.jpg',
            'fear': 'scared_cat.jpg',
            'disgust': 'disgusted_cat.jpg'
        }
        self.cat_images = {}
        self.load_cat_images()
        print("모델을 로딩하는 중입니다...")
        
    def load_cat_images(self):
        cat_folder = 'cat_images'
        if not os.path.exists(cat_folder):
            os.makedirs(cat_folder)
            print(f"'{cat_folder}' 폴더를 생성했습니다. 표정별 고양이 이미지를 추가해주세요:")
            for emotion, filename in self.emotion_to_cat.items():
                print(f"  - {filename} ({emotion})")
        
        for emotion, filename in self.emotion_to_cat.items():
            filepath = os.path.join(cat_folder, filename)
            if os.path.exists(filepath):
                img = cv2.imread(filepath)
                if img is not None:
                    self.cat_images[emotion] = cv2.resize(img, (300, 300))
        
        if not self.cat_images:
            print("고양이 이미지를 찾을 수 없습니다. 기본 텍스트로 표시합니다.")
    
    def create_cat_display(self, emotion, confidence):
        if emotion in self.cat_images:
            cat_img = self.cat_images[emotion].copy()
            text = f"{emotion.upper()} ({confidence:.1f}%)"
            cv2.putText(cat_img, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.7, (255, 255, 255), 2)
            return cat_img
        else:
            blank = np.ones((300, 300, 3), dtype=np.uint8) * 100
            cv2.putText(blank, emotion.upper(), (50, 150), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
            cv2.putText(blank, f"{confidence:.1f}%", (80, 200), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            return blank
    
    def run(self):
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("웹캠을 열 수 없습니다.")
            return
        
        cap.set(cv2.CAP_PROP_BRIGHTNESS, 0.5)
        
        print("프로그램이 시작되었습니다. 'q'를 눌러 종료하세요.")
        frame_count = 0
        current_emotion = 'neutral'
        current_confidence = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            frame = cv2.convertScaleAbs(frame, alpha=2, beta=10)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            if len(faces) > 0 and frame_count % 30 == 0:
                try:
                    result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
                    
                    if isinstance(result, list):
                        result = result[0]
                    
                    current_emotion = result['dominant_emotion']
                    current_confidence = result['emotion'][current_emotion]
                except Exception as e:
                    print(f"표정 감지 오류: {e}")
            
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, f"{current_emotion}", (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            cat_display = self.create_cat_display(current_emotion, current_confidence)
            
            if len(faces) == 0:
                blank = np.ones((300, 300, 3), dtype=np.uint8) * 100
                cv2.putText(blank, "No face", (80, 150), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cat_display = blank
            
            frame_resized = cv2.resize(frame, (640, 480))
            cat_resized = cv2.resize(cat_display, (640, 480))
            combined = np.hstack([frame_resized, cat_resized])
            
            cv2.imshow('Cat Emotion Display', combined)
            
            frame_count += 1
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = CatEmotionDisplay()
    app.run()
