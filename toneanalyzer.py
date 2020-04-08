from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json

authenticator = IAMAuthenticator('__8qDmgsE5B8mohlnWvi6laIbsISL9BDHS1WLWhL3by7')
tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    authenticator=authenticator
)

tone_analyzer.set_service_url('https://api.us-east.tone-analyzer.watson.cloud.ibm.com/instances/82f4139d-42b0-436a-9a14-5c6520284a1c')

def analyze(text):
    tone_analysis = tone_analyzer.tone(
        {'text': text},
        content_type='application/json').get_result()

    result = json.dumps(tone_analysis)
    tones = []
    for tone in tone_analysis["document_tone"]["tones"]:
        if(tone["score"] > 0.5):
            tones.append(tone["tone_id"])
    for tone in tones:
        print(tone)
    return tones
