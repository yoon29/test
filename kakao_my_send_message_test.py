'''
https://cocoabba.tistory.com/15

[Python] 카카오톡 : 메시지 (1/3 - 나에게 메시지 보내기)

1. 카카오 개발자센터 가입 및 앱 등록 (https://developers.kakao.com/)
이 부분은 다른 블로그 혹은 해당사이트 안내를 따라 쉽게 따라 할 수 있는 부분이라 본 글에서는 PASS !!

2. 개발을 위한 Access Token 발급
    (https://developers.kakao.com/tool/rest-api/open/get/v1-user-access_token_info)
경로 : 도구> REST API 테스트> 토큰 정보 보기

이 경로를 찾는데 많은 시간을 보냈다. 다른 블로그등을 보면 [내 애플리케이션] 등을 통해 토큰 발급을 받으라고 했지만, 어디에서도 토큰 발급 경로를 찾기 어려웠고, 위 메뉴를 누르다 경로를 확인하게 되었다.
여기서 기본적으로 제공되는 developers-sample 앱으로 토근 발급 시,

{"msg":"ip mismatched! callerIp=221.139.xxx.xxx. check out registered ips.","code":-401}
에러가 발생한다. 위의 ip mismatched! callerIp 에러 시 대부분 해결책으로 [내 애플리케이션] > [고급설정] > [허용 IP 주소]를 알려주지만, 이는 다른 앱에서 등록한 토큰을 사용하여 발생한 오류이기 때문에 위 그림처럼 앱을 선택하여, 내가 개발하고 있는 앱을 선택해야 한다. ;;물론 동시에 허용 IP 주소도 등록해줘야 한다.
정상적으로 토큰 발급 시, 52자리의 String 값을 발급 받을 수 있다.

3. REST API 사용 방법 확인 (https://developers.kakao.com/docs/latest/ko/message/rest-api)
경로 : 문서>메시지>REST API

API 사용방법이 나오며, Sample 코드가지 친절하게 제공하여 준다.
우선 코드는 curl을 통해 요청하는 POST 구문으로  아래와 같이 제공한다.

#참고 : https://developers.kakao.com/docs/latest/ko/message/rest-api#send-me
curl -v -X POST "https://kapi.kakao.com/v2/api/talk/memo/default/send" \
    -H "Authorization: Bearer {USER_ACCESS_TOKEN}" \
    -d 'template_object={
        "object_type": "text",
        "text": "텍스트 영역입니다. 최대 200자 표시 가능합니다.",
        "link": {
            "web_url": "https://developers.kakao.com",
            "mobile_web_url": "https://developers.kakao.com"
        },
        "button_title": "바로 확인"
    }'

헤더로 Authorization 값으로 "Bearer "뒤에 2번에서 받은 Access Token 을 넣으면 되고,
나머지 데이터 파라미터는 이대로 전달하면 된다.

카카오의 POST 메시지는 template_object 파라미터로 구성한 메시지를 전달해야 하며, 타입은 JSON 으로 보내야 한다.

JSON Object 타입으로 파라미터 구성
data = {"template_object": json.dumps(post)} 코드는 샘플에서 제공한 메시지 형태로 구성했을 때, json 타입으로 변환하는 코드이며, requests.post 를 통해 메시지를 나에게 전송할 수 있다.

샘플코드를 활용하면 쉽게 구현할 수 있는 부분이지만, 사소한 실수가 많을 수 있다.
예를 들어 Authorization 의 값으로 "Bearer 토큰"을 넣어야 하지만, Bearer과 토큰 사이 공백이 없다면,
아래와 같은 에러가 발생한다.

{"msg":"access token should not be null or empty","code":-2}

'''

import os
import json
import requests

def sendToMeMessage(text):
    header = {"Authorization": 'Bearer ' + KAKAO_TOKEN}

    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send" #나에게 보내기 주소

    post = {
        "object_type": "text",
        "text": text,
        "link": {
            "web_url": "https://developers.kakao.com",
            "mobile_web_url": "https://developers.kakao.com"
        },
        "button_title": "바로 확인"
    }
    data = {"template_object": json.dumps(post)}
    return requests.post(url, headers=header, data=data)

text = "Hello, This is KaKao Message Test!!("+os.path.basename(__file__).replace(".py", ")")
KAKAO_TOKEN = "TFS_000000000000000000000000000000000000000_sQ"

print(sendToMeMessage(text).text)

