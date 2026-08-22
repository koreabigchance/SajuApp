import os
from datetime import datetime
from korean_lunar_calendar import KoreanLunarCalendar

class SajuLogic:
    def __init__(self):
        self.CHEONGAN = ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계']
        self.JIJI = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해']
        
        self.STEM_OHAENG = ['wood', 'wood', 'fire', 'fire', 'earth', 'earth', 'metal', 'metal', 'water', 'water']
        self.BRANCH_OHAENG = ['water', 'earth', 'wood', 'wood', 'earth', 'fire', 'fire', 'earth', 'metal', 'metal', 'earth', 'water']
        
        self.ELEMENT_MAP = {
            '갑': 'wood', '을': 'wood', '병': 'fire', '정': 'fire', '무': 'earth',
            '기': 'earth', '경': 'metal', '신': 'metal', '임': 'water', '계': 'water',
            '인': 'wood', '묘': 'wood', '사': 'fire', '오': 'fire', '진': 'earth',
            '미': 'earth', '술': 'earth', '축': 'earth', '신': 'metal', '유': 'metal',
            '해': 'water', '자': 'water'
        }

    def get_gan_zhi(self, year, month, day, hour, minute):
        calendar = KoreanLunarCalendar()
        calendar.setSolarDate(year, month, day)
        gapja_str = calendar.getGapJaString()
        if not gapja_str:
            # Fallback if invalid
            return self._fallback_gan_zhi()
            
        parts = gapja_str.split()
        if len(parts) < 3:
            return self._fallback_gan_zhi()
            
        # 자시(23:00~01:00) 처리를 위해 분 단위 환산
        h_idx = (hour * 60 + minute + 30) // 120 % 12
        d_gan_idx = self.CHEONGAN.index(parts[2][0])
        h_gan_idx = ({0:0, 5:0, 1:2, 6:2, 2:4, 7:4, 3:6, 8:6, 4:8, 9:8}[d_gan_idx % 10] + h_idx) % 10
        
        data = [
            (parts[0][0], parts[0][1]), # 년
            (parts[1][0], parts[1][1]), # 월
            (parts[2][0], parts[2][1]), # 일
            (self.CHEONGAN[h_gan_idx], self.JIJI[h_idx]) # 시
        ]
        
        keys = ['year', 'month', 'day', 'hour']
        pillars = {}
        for k, (g, z) in zip(keys, data):
            pillars[k] = {
                'gan': g, 
                'zhi': z, 
                'gan_idx': self.CHEONGAN.index(g), 
                'zhi_idx': self.JIJI.index(z), 
                'gan_element': self.ELEMENT_MAP[g], 
                'zhi_element': self.ELEMENT_MAP[z]
            }
        return pillars
        
    def _fallback_gan_zhi(self):
        # Default mock if calendar fails
        return {
            'year': {'gan': '갑', 'zhi': '자', 'gan_idx': 0, 'zhi_idx': 0, 'gan_element': 'wood', 'zhi_element': 'water'},
            'month': {'gan': '병', 'zhi': '인', 'gan_idx': 2, 'zhi_idx': 2, 'gan_element': 'fire', 'zhi_element': 'wood'},
            'day': {'gan': '무', 'zhi': '진', 'gan_idx': 4, 'zhi_idx': 4, 'gan_element': 'earth', 'zhi_element': 'earth'},
            'hour': {'gan': '경', 'zhi': '신', 'gan_idx': 6, 'zhi_idx': 8, 'gan_element': 'metal', 'zhi_element': 'metal'}
        }

    def get_ohaeng_distribution(self, pillars):
        counts = {'wood': 0, 'fire': 0, 'earth': 0, 'metal': 0, 'water': 0}
        for p in pillars.values():
            counts[p['gan_element']] += 1
            counts[p['zhi_element']] += 1
        return counts

    def _determine_god(self, me_idx, target_idx, me_pol, target_pol):
        diff = (target_idx - me_idx) % 5
        is_same_polarity = (me_pol == target_pol)
        
        if diff == 0: return "비견" if is_same_polarity else "겁재"
        if diff == 1: return "식신" if is_same_polarity else "상관"
        if diff == 2: return "편재" if is_same_polarity else "정재"
        if diff == 3: return "편관" if is_same_polarity else "정관"
        if diff == 4: return "편인" if is_same_polarity else "정인"
        return ""

    def _get_all_sip_seong(self, pillars):
        # 오행 인덱스: wood=0, fire=1, earth=2, metal=3, water=4
        element_to_idx = {'wood': 0, 'fire': 1, 'earth': 2, 'metal': 3, 'water': 4}
        
        me_element = pillars['day']['gan_element']
        me_idx = element_to_idx[me_element]
        me_pol = pillars['day']['gan_idx'] % 2 # 0: 양, 1: 음
        
        # 지지 음양: 자(음), 축(음), 인(양), 묘(음), 진(양), 사(양), 오(음), 미(음), 신(양), 유(음), 술(양), 해(양)
        zhi_polarities = [1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0]
        
        ten_gods = {}
        for key in ['year', 'month', 'day', 'hour']:
            # 천간 십성
            target_gan_idx = element_to_idx[pillars[key]['gan_element']]
            target_gan_pol = pillars[key]['gan_idx'] % 2
            gan_god = self._determine_god(me_idx, target_gan_idx, me_pol, target_gan_pol)
            
            # 지지 십성
            target_zhi_idx = element_to_idx[pillars[key]['zhi_element']]
            target_zhi_pol = zhi_polarities[pillars[key]['zhi_idx']]
            zhi_god = self._determine_god(me_idx, target_zhi_idx, me_pol, target_zhi_pol)
            
            ten_gods[key] = {
                'gan': gan_god,
                'zhi': zhi_god
            }
        
        # 일간은 '나'
        ten_gods['day']['gan'] = '나'
        return ten_gods

    def _get_core_trait(self, master, element):
        traits = {
            '갑': '곧게 뻗은 소나무처럼 리더십과 추진력이 강하며 자존심이 높습니다.',
            '을': '비바람에 꺾이지 않는 잡초처럼 적응력이 뛰어나고 실속을 챙깁니다.',
            '병': '세상을 비추는 태양처럼 열정적이고 솔직하며 화려함을 좋아합니다.',
            '정': '어둠을 밝히는 촛불처럼 따뜻하고 섬세하며 헌신적인 면모가 있습니다.',
            '무': '묵묵한 태산처럼 믿음직스럽고 포용력이 있으며 신중합니다.',
            '기': '비옥한 텃밭처럼 현실 감각이 뛰어나고 수용력이 강합니다.',
            '경': '단단한 원석처럼 의리와 결단력이 있으며 신념이 확고합니다.',
            '신': '반짝이는 보석처럼 섬세하고 미적 감각이 뛰어나며 자존심이 셉니다.',
            '임': '드넓은 바다처럼 지혜롭고 유연하며 창의력이 풍부합니다.',
            '계': '만물을 적시는 단비처럼 섬세하고 친화력이 좋으며 상황 파악이 빠릅니다.'
        }
        return f"🌲 **{master}기운의 소유자**\n" + traits.get(master, "")

    def get_daewoon(self, year_gan_idx, gender, day):
        is_yang_year = (year_gan_idx % 2 == 0)
        is_male = (gender == 'male')
        is_forward = (is_yang_year and is_male) or (not is_yang_year and not is_male)
        daewoon_num = (day % 10) if (day % 10) != 0 else 10
        return is_forward, daewoon_num

    def calculate_daewoon_list(self, pillars, gender):
        year_gan_idx = pillars['year']['gan_idx']
        month_gan_idx = pillars['month']['gan_idx']
        month_zhi_idx = pillars['month']['zhi_idx']
        # For simplicity, using day=15
        is_forward, daewoon_num = self.get_daewoon(year_gan_idx, gender, 15)
        
        step = 1 if is_forward else -1
        
        daewoons = []
        for i in range(8):
            current_gan = (month_gan_idx + step * (i+1)) % 10
            current_zhi = (month_zhi_idx + step * (i+1)) % 12
            start_age = daewoon_num + (i * 10)
            
            gan_char = self.CHEONGAN[current_gan]
            zhi_char = self.JIJI[current_zhi]
            
            # Simple advice string format for UI
            advice = f"[대운의 변화] {start_age}세부터 시작되는 {gan_char}{zhi_char} 대운은 당신에게 새로운 환경과 기회를 가져다 줍니다."
            
            daewoons.append({
                'age': start_age,
                'gan': gan_char,
                'zhi': zhi_char,
                'gan_element': self.ELEMENT_MAP[gan_char],
                'zhi_element': self.ELEMENT_MAP[zhi_char],
                'text': advice
            })
            
        return daewoons

    def analyze_ohaeng_balance(self, dist):
        total = sum(dist.values())
        if total == 0: total = 1
        percentages = {k: (v / total) * 100 for k, v in dist.items()}
        details = []
        for el, p in percentages.items():
            if p >= 35: details.append({'element': el, 'status': 'excess', 'msg': f'{el} 기운이 매우 강합니다.'})
            elif p == 0: details.append({'element': el, 'status': 'missing', 'msg': f'{el} 기운이 부족합니다.'})
        return {
            'percentages': percentages, 
            'details': details, 
            'balance_text': "오행이 골고루 갖춰져 있습니다." if not details else "특정 오행의 편중이 있어 보완이 필요합니다."
        }

    def get_today_fortune(self, day_master_element, gender):
        now = datetime.now()
        # Mock logic
        return {
            'date': now.strftime('%Y년 %m월 %d일'),
            'pillar': '오늘의 일진',
            'title': '🤝 평온하고 무난한 하루',
            'desc': '자신에게 주어진 일에 집중하며 하루를 보내시면 좋습니다.'
        }

    def get_geun_myo_hwa_sil(self, pillars):
        return {
            'year': {'period': '초년기 (0~19세)', 'desc': '부모와 조상의 영향을 받는 시기입니다.', 'pillar': pillars['year']},
            'month': {'period': '청년기 (20~39세)', 'desc': '사회생활을 시작하고 자아를 확립하는 시기입니다.', 'pillar': pillars['month']},
            'day': {'period': '중년기 (40~59세)', 'desc': '가정을 꾸리고 인생의 주체가 되어 결실을 맺는 시기입니다.', 'pillar': pillars['day']},
            'hour': {'period': '말년기 (60세~)', 'desc': '자식과의 관계와 노후의 안정성을 보여주는 시기입니다.', 'pillar': pillars['hour']}
        }

    def interpret(self, pillars, dist, user_info):
        day_master_gan = pillars['day']['gan']
        day_master_element = pillars['day']['gan_element']
        gender = user_info.get('gender', 'male')
        
        ohaeng_analysis = self.analyze_ohaeng_balance(dist)
        daewoon_list = self.calculate_daewoon_list(pillars, gender)
        gmhs = self.get_geun_myo_hwa_sil(pillars)
        ten_gods = self._get_all_sip_seong(pillars)
        
        interp = {
            'core': self._get_core_trait(day_master_gan, day_master_element),
            'advice': "💡 **강점 활용**: 본인이 가진 장점을 십분 발휘하세요.",
            'wealth': "재물운이 대체로 안정적입니다.",
            'love': "인연을 소중히 여길 필요가 있습니다.",
            'career': "표현력과 기획력이 필요한 분야가 적합합니다.",
            'total_summary': "사주 전반의 기운이 조화로우며 발전 가능성이 높습니다.",
            'personality_deep': "내면의 깊이가 있으며 타인을 이해하려는 성향이 강합니다.",
            'social_analysis': "사회적 관계망 안에서 든든한 조력자 역할을 할 수 있습니다.",
            'health_analysis': "균형 잡힌 식단과 가벼운 운동이 큰 도움이 됩니다.",
            'daewoon_trend': "앞으로의 10년은 중요한 변화의 기점을 맞이하게 될 것입니다.",
            'wealth_strategy': "안정적인 분산 투자가 유리합니다.",
            'today_luck': self.get_today_fortune(day_master_element, gender),
            'gmhs': gmhs,
            'ohaeng_analysis': ohaeng_analysis,
            'daewoon': daewoon_list,
            'ten_gods': ten_gods
        }
        
        return interp
