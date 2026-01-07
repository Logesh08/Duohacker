import requests

# URL and headers
url = 'https://www.duolingo.com/2017-06-30/friends/nudge'
headers = {
    'Accept': 'application/json; charset=UTF-8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjYzMDcyMDAwMDAsImlhdCI6MCwic3ViIjoxMTk3NjQ3MjI3fQ.HsnIqHOtidQC6i-1rwAWfTQR_mOGBBmNZpd1TA6OyJw',
    'Content-Type': 'application/json; charset=UTF-8',
    'Origin': 'https://www.duolingo.com',
    'Priority': 'u=1, i',
    'Referer': 'https://www.duolingo.com/profile/bhVn15_?via=friends',
    'Sec-CH-UA': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'Sec-CH-UA-Mobile': '?0',
    'Sec-CH-UA-Platform': '"Linux"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'X-Amzn-Trace-Id': 'User=1197647227',
    'X-Requested-With': 'XMLHttpRequest',
}

# Cookies
cookies = {
    'lang': 'en',
    'lu': 'https://www.duolingo.com/leaderboard',
    'initial_referrer': '$direct',
    'lr': '',
    'lp': 'splash',
    'csrf_token': 'IjZjMjU5MzRiOGI2NDQ0Y2Y5MzU2ZmRmY2Y1ZTRiMDdlIg==',
    'logged_out_uuid': '1197647227',
    'logged_in': 'true',
    'wuuid': 'bb7e0c1f-0a78-4483-9d6a-5ff191fe6691',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Thu+May+22+2025+11%3A12%3A11+GMT%2B0530+(India+Standard+Time)&version=202404.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=fc7d21e5-1bfa-41d4-b3db-ae3a510d33af&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false',
    'jwt_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjYzMDcyMDAwMDAsImlhdCI6MCwic3ViIjoxMTk3NjQ3MjI3fQ.HsnIqHOtidQC6i-1rwAWfTQR_mOGBBmNZpd1TA6OyJw',
    'tsl': '1747892531286',
    'AWSALB': '3n0Gd14Korxpyy5rp588UliwMLndny3cW69zygNf1oSwkRZzPzsP7/XyBcEXehzVa1VejPAw0cEkHXgx+E8uRfzQhcoWHNMBt9E7HWHwghWodX1nLImQSrp5I+yt',
    'AWSALBCORS': '3n0Gd14Korxpyy5rp588UliwMLndny3cW69zygNf1oSwkRZzPzsP7/XyBcEXehzVa1VejPAw0cEkHXgx+E8uRfzQhcoWHNMBt9E7HWHwghWodX1nLImQSrp5I+yt',
}

# JSON payload
payload = {
    'data': {'streakLength': 18},
    'nudgeType': 'eyes',
    'source': 'friends_streak',
    'targetUserIds': [614221014],
    'userId': 1197647227,
    'via': 'streak_page'
}

# nudgeType Options
["eyes", "dumpster_fire", "heart_without_you", "shadow_duo"] 


# Sending the POST request
response = requests.post(url, headers=headers, cookies=cookies, json=payload)

# Output the response
print(response.status_code)
print(response.json())
