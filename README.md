# Cat Emotion Display

얼굴 표정을 실시간으로 감지하여 대응하는 고양이 이미지로 표시하는 프로그램입니다.

## 기능
- 웹캠을 통한 실시간 얼굴 감지
- 7가지 표정 인식 (happy, sad, angry, surprise, neutral, fear, disgust)
- 표정에 맞는 고양이 이미지 표시

## 설치 방법

1. 필요한 라이브러리 설치:
```bash
pip install -r requirements.txt
```

## 사용 방법

1. `cat_images` 폴더에 다음 고양이 이미지들을 준비하세요:
   - happy_cat.jpg (행복한 고양이)
   - sad_cat.jpg (슬픈 고양이)
   - angry_cat.jpg (화난 고양이)
   - surprised_cat.jpg (놀란 고양이)
   - neutral_cat.jpg (무표정 고양이)
   - scared_cat.jpg (무서워하는 고양이)
   - disgusted_cat.jpg (혐오하는 고양이)

2. 프로그램 실행:
```bash
python cat_emotion.py
```

3. 'q' 키를 눌러 종료

## 화면 구성
- 왼쪽: 웹캠 화면 + 얼굴 감지 박스 + 감지된 표정
- 오른쪽: 해당 표정의 고양이 이미지 + 신뢰도(%)
