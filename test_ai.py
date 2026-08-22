import sys
from saju_logic import SajuLogic
from ai_analysis import AIAnalysis
import json

saju = SajuLogic()
ai = AIAnalysis()

pillars = saju.get_gan_zhi(1990, 1, 1, 12, 0)
ohaeng = saju.get_ohaeng_distribution(pillars)
interp = saju.interpret(pillars, ohaeng, {'gender': 'male'})

ten_gods_all = []
for p_key in interp['ten_gods']:
    ten_gods_all.append(interp['ten_gods'][p_key]['gan'])
    ten_gods_all.append(interp['ten_gods'][p_key]['zhi'])

from collections import Counter
counts = Counter(ten_gods_all)
ten_stars_list = ", ".join([f"{k} {v}" for k, v in counts.items()])

current_daewun = f"{interp['daewoon'][0]['age']}세 대운 ({interp['daewoon'][0]['gan']}{interp['daewoon'][0]['zhi']})"
birth_context = "1990년생 (36세)"

ai_data = ai.get_deep_analysis(
    "테스트", "male", pillars, interp['ohaeng_analysis'], ten_stars_list, current_daewun, birth_context
)

print(json.dumps(ai_data, ensure_ascii=False, indent=2))
