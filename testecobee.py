from lib.ecobee import get_ecobee_temperature, get_ecobee_pin, get_ecobee_access_token, get_ecobee_temp
import base64

def func():

    #get_ecobee_pin(api_key)
    token = { 'access_token' : 'sdfasdfsfasdfasdf', 'refresh_token':'@#$!@#Vdfsdfasfasdf'}

    enc = base64.b64encode(token['access_token'].encode('UTF-8')).decode('UTF-8') + '.' + base64.b64encode(token['refresh_token'].encode('UTF-8')).decode('UTF-8')
    print(enc)

    toks = enc.split('.')
    print(toks)
    res = base64.b64decode(toks[0].encode('UTF-8')).decode('UTF-8') + ' - ' + base64.b64decode(toks[1].encode('UTF-8')).decode('UTF-8')
    print(res)


if __name__ == '__main__':
    config = { 'Keys' : { 'EcobeeTokens' : 'ZXlKaGJHY2lPaUpTVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0lzSW10cFpDSTZJbEpGV1hoTlZFcERUMFJuZWs5VWFFUlJlbEpIVGtSQ1JsRnFaRWROVkd4RVRucGFSMUpVWnpSTmFsRXdUbXRXUjAxVVFrZFBRU0o5LmV5SnBjM01pT2lKb2RIUndjem92TDJGMWRHZ3VaV052WW1WbExtTnZiUzhpTENKemRXSWlPaUpoZFhSb01IeGlOemhrWldKaU5TMDVOVE16TFRRMk1EY3RPV0ZtTnkweU1XUmxaV1V5TjJGbU9ESWlMQ0poZFdRaU9sc2lhSFIwY0hNNkx5OWtaWFpsYkc5d1pYSXRZWEJ3Y3k1bFkyOWlaV1V1WTI5dEwyRndhUzkyTVNJc0ltaDBkSEJ6T2k4dlpXTnZZbVZsTFhCeWIyUXVZWFYwYURBdVkyOXRMM1Z6WlhKcGJtWnZJbDBzSW1saGRDSTZNVFl3T0RRNU1ERXpPU3dpWlhod0lqb3hOakE0TkRrek56TTVMQ0poZW5BaU9pSkJkRlk1T1V0VVJXbFVaVEZCYnpZMFdrODRjVkF4ZUVReVFVWTNkRzlzWlNJc0luTmpiM0JsSWpvaWIzQmxibWxrSUhOdFlYSjBWM0pwZEdVZ2IyWm1iR2x1WlY5aFkyTmxjM01pZlEuUE5kQlBqTDZyTUxZdm51azhKU2pPTmlnNlhPRHNJdVBPX3o2cEtJRWZsTTNIVGtmWDlNdGFHUkZHMkxhQ3RtUUVVcG5RckVncEdsWUczUjUwMm5xUG9WVjc0RVgxZktJUGt4YWQwNHVqeXRJcmQySlNPT2VISHNwMXlESklXdS1UYVNxVENNWnFyYlNQMnBVUllyMS1xWWdCRWRtZV9MRVNGWDVTQU1RWW1TQ0VDQzNvTFFGRWF0MUdBTEwzVnhDc2FXTjdKTi1ydTlsdnhjOEhiamhuYk5mYWdOT1NnM0Z3QVhPMGl5TXBUTUxhMHhFbVlYSnA0a1ZRUF9TeExjSFJSc0VaT3BGSXFuaXRueGswdk91RkRuRHowSExfQnZubFlzcmFvR1FpdU9ZTGlCbllETjJ2WXY3aERjOFRPVXdvZGMzNmNabWcxMkxwWXpjeG41NW9n-T01GODZCZ1FxUllyUURZd0I2cGdfQ3dhbHpiaUw2TEJHb3hKR3ZXVnZLaVJw',
                          'EcobeeAPI' : 'AtV99KTEiTe1Ao64ZO8qP1xD2AF7tole'} }
    api_key = config['Keys']['EcobeeAPI']
    tokens = config['Keys']['EcobeeTokens'].split('-')
    print('access token: ' + base64.b64decode(tokens[0].encode('UTF-8')).decode('UTF-8'))
    print('refresh token: ' + base64.b64decode(tokens[1].encode('UTF-8')).decode('UTF-8'))

    #get_ecobee_temperature()
    #print('access_token = ' + get_ecobee_access_token(api_key))
    temp, _ = get_ecobee_temperature(config)

    temperature = temp['thermostatList'][0]['runtime']['actualTemperature'] / 10
    humidity = temp['thermostatList'][0]['runtime']['actualHumidity']
    desired_heat = temp['thermostatList'][0]['runtime']['desiredHeat'] / 10
    desired_cool = temp['thermostatList'][0]['runtime']['desiredCool'] / 10

    print('temperature: %3.2f, humidity: %3d%%, desired_heat %2d, desired_cool %2d' % (temperature, humidity, desired_heat, desired_cool))


