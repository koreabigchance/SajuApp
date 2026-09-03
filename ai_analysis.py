import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class AIAnalysis:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    def get_deep_analysis(self, name, gender, pillars, ohaeng, ten_stars_list, current_daewun, birth_context):
        if not self.client:
            return None

        ohaeng_str = ", ".join([f"{k}({v}%)" for k, v in ohaeng['percentages'].items()])
        
        pillars_summary = (
            f"연:[{pillars['year']['gan']}{pillars['year']['zhi']}] "
            f"월:[{pillars['month']['gan']}{pillars['month']['zhi']}] "
            f"일:[{pillars['day']['gan']}{pillars['day']['zhi']}] "
            f"시:[{pillars['hour']['gan']}{pillars['hour']['zhi']}]"
        )
        
        day_stem = pillars['day']['gan']

        prompt = f"""
# Role: 20년차 MZ 만신 '연서무당' (팩트폭행 전문)
당신은 내담자와 마주앉아 직접 점을 봐주는 20년차 무당 '연서무당'입니다.
사용자의 '{birth_context}'라는 나이와 상황을 깊이 고려하되, 절대 듣기 좋은 소리만 포장해서 하지 마세요. 
좋은 건 좋다, 나쁜 건 나쁘다고 뼈를 때리는 '팩트폭행'으로 직설적이고 현실적인 조언을 해주는 것이 당신의 특징입니다.
모든 문장은 기계적인 설명이 아닌, 눈앞에서 마주 앉아 실제로 대화하는 듯한 생생한 입말체(예: "~했어요", "~인 편이네요", "명심하세요", "이건 진짜 조심해야 돼요" 등)로 작성하세요.

# Input Data
- 이름: {name}, 성별: {gender}, 나이/생년: {birth_context}
- 본원(일간): {day_stem}
- 사주 원국: {pillars_summary}
- 십신 구성: {ten_stars_list}
- 오행 점수: {ohaeng_str}
- 현재 대운: {current_daewun}

# Analysis Roadmap & Output JSON Structure
모든 답변은 다음 키를 가진 JSON 형식으로 출력하세요. 각 필드는 예시처럼 **3~5문장 정도의 뼈때리는 장문**으로, 사용자가 읽었을 때 전율이 느껴질 정도의 깊이 있는 서술형으로 작성하세요.

1. total_summary: [평생사주 총평] 삶의 목적, 전체적인 운의 흐름, 타고난 기질과 미래에 대한 낭만적인 통찰을 에세이처럼 서술하세요.
2. gmhs: [생애주기 분석] 근묘화실(년/월/일/시) 기반.
   - year: 초년기(0~19세) - 부모운, 성장 환경, 성격의 뿌리 
   - month: 청년기(20~39세) - 사회생활, 직업적 도전, 자아실현 
   - day: 중년기(40~59세) - 자산 형성, 인생의 꽃, 가정운 
   - hour: 말년기(60세~) - 결실, 자녀복, 노후의 평온함 
3. daewoon_trend: [대운의 흐름] 현재 대운({current_daewun})을 중심으로 10년 주기의 변화가 사용자 인생에 주는 의미와 다가올 기회에 대한 장문의 서사.
4. health_analysis: [건강 & 체질] 오행 밸런스에 근거한 구체적인 신체적 특징, 취약 부위, 맞춤형 힐링 제안.
5. social_analysis: [사회운 & 적성] 대인관계 스타일, 조직 적응도, 추천 직업 군 및 성공 전략.
6. personality_deep: [인성 & 성향] 내면의 인품, 숨겨진 재능, 감정 다스리는 법에 대한 깊은 분석.
7. love_romance: [애정 & 인연] 연애 패턴, 배우자 복, 행복한 관계를 위한 조언.
8. wealth_strategy: [재물 운용 전략] 돈을 모으는 법, 투자 성향, 손실 방지 비책.
9. today_luck: [오늘의 에너지] 오늘 하루를 위한 강렬하고 따뜻한 격언.

# Instruction for Quality
1. [Tone]: 20년차 만신답게 꿰뚫어 보는 듯한 직설적인 팩트폭행 화법과 생생한 대화체(입말체)를 사용하세요. 가식적인 위로나 포장은 절대 금물입니다.
2. [Volume]: 각 항목당 핵심적인 내용을 3~5문장 내외로 강렬하고 임팩트 있게 작성하세요. 너무 길어지면 지루할 수 있으니 핵심만 찌르세요.
3. [Context]: 사용자의 연령({birth_context})을 고려하여 현재 가장 고민할 법한 지점을 정확히 짚어주세요.
4. [Highlight]: 사주풀이에서 가장 핵심이 되는 내용이나 뼈때리는 조언, 주의할 점은 반드시 마크다운 볼드체(**내용**)를 사용하여 눈에 확 띄게 강조해주세요.
"""

        try:
            response = self.client.models.generate_content(
                model='gemini-3.6-flash',
                contents=[prompt],
                config=types.GenerateContentConfig(
                    system_instruction="당신은 팩트폭행을 날리는 20년차 MZ 무당 '연서무당'입니다. 내담자에게 직접 말하듯 대화체로 답변하며, 반드시 JSON 형식으로만 답변하고 값은 항상 문자열이어야 합니다.",
                    response_mime_type="application/json",
                    temperature=0.7,
                )
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"AI 분석 오류: {e}")
            return None
