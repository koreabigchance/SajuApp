import urllib.request
import urllib.parse

url = 'http://127.0.0.1:5000/result'
data = urllib.parse.urlencode({
    'name': '테스트',
    'gender': 'male',
    'birth_date': '1990-01-01',
    'birth_time': '12:00'
}).encode('utf-8')

req = urllib.request.Request(url, data=data)
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        with open('result_output.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("HTML saved to result_output.html")
except Exception as e:
    print("Error:", e)
