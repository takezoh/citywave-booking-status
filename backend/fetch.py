import requests
import datetime
import json
import concurrent.futures

MAX = {
    1: 10,
    2: 12,
    3: 10,
}

DAYS = 3
LEVELS = (1, 2, 3)


def fetch(date, level):
    times = []
    date_str = "{:04d}-{:02d}-{:02d}".format(date.year, date.month, date.day)
    r = requests.get("https://citywave-tokyo.jp/enable_time/{}/{}".format(level, date_str))
    r.raise_for_status()
    ctx = r.json()
    for e in ctx['times']:
        times.append({
            'time': e['from_to'],
            'qty': MAX[level] - int(e['enable_qty']),
            'level': level,
            })

    return {
        'date': date_str,
        'times': times,
        }


def lambda_handler(event, context):
    results = []
    today = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).date()
    with concurrent.futures.ThreadPoolExecutor(max_workers=DAYS * len(LEVELS)) as executor:
        for level in LEVELS:
            for i in range(DAYS):
                date = today + datetime.timedelta(days=i)
                results.append(executor.submit(fetch, date=date, level=level))

    times = {}
    for r in results:
        r = r.result()
        if not r['date'] in times:
            times[r['date']] = []
        node = times[r['date']]
        node[len(node):] = r['times']

    context = [{'date': k, 'times': sorted(v, key=lambda x: x['time'])} for k, v in times.items()]
    context = sorted(context, key=lambda x: x['date'])
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': 'https://cw.takezo.dev',
            'Access-Control-Allow-Credentials': 'true',
            'Content-Type': 'application/json',
        },
        'body': json.dumps(context),
    }


if __name__ == '__main__':
    r = lambda_handler(None, None)
    print(json.dumps(json.loads(r['body']), indent=4))
