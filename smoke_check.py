import urllib.request, json, sys

urls = [
    'http://127.0.0.1:5000/',
    'http://127.0.0.1:5000/products',
    'http://127.0.0.1:5000/suppliers',
    'http://127.0.0.1:5000/icecream',
    'http://127.0.0.1:5000/api/products'
]

for u in urls:
    print('\nGET', u)
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'smoke-check/1.0'})
        with urllib.request.urlopen(req, timeout=5) as r:
            body = r.read().decode('utf-8')
            print('Status:', r.status)
            try:
                parsed = json.loads(body)
                print(json.dumps(parsed, indent=2))
            except Exception:
                print(body[:1000])
    except Exception as e:
        print('Error:', e)
        sys.exit(1)
print('\nSmoke check finished')
