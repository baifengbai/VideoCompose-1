import requests
import random
from threading import Thread
import sys

url = "http://video-compose:9515/api/video/"
payload = {
    'length': '20',
    'size': '720X1280',
    'start': '10',
    'end': '30'
}
with open('pictures1.png', 'rb') as f:
    p1 = f.read()
with open('pictures2.JPG', 'rb') as f:
    p2 = f.read()
with open('pictures3', 'rb') as f:
    p3 = f.read()
with open('music.mp3', 'rb') as f:
    m = f.read()
files = [
    ('pictures', ('pictures1-kg.png', p1, 'image/png')),
    ('pictures', ('pictures2.JPG', p2, 'application/octet-stream')),
    ('pictures', ('pictures3.JPG', p3, 'application/octet-stream')),
    ('pictures', ('pictures1-kg.png', p1, 'image/png')),
    ('pictures', ('pictures2.JPG', p2, 'application/octet-stream')),
    ('pictures', ('pictures3.JPG', p3, 'application/octet-stream')),
    ('pictures', ('pictures1-kg.png', p1, 'image/png')),
    ('pictures', ('pictures2.JPG', p2, 'application/octet-stream')),
    ('pictures', ('pictures3.JPG', p3, 'application/octet-stream')),
    ('audio', (
        'Otis McDonald-BirdBrainz II.mp3', m, 'audio/mpeg'))
]

def test_post(worker_id):
    sys.stdout.write('worker {} processing\n'.format(worker_id))
    response = requests.request("POST", url, data=payload, files=files, timeout=1000)
    sys.stdout.write('worker {} cost {} seconds\n'.format(worker_id, response.elapsed.seconds))

def thread_post(n=10):
    workers = []
    for i in range(1, n+1):
        workers.append(Thread(target=test_post, args=(i,)))
        workers[-1].start()
    for _ in workers:
        _.join()

thread_post(8)