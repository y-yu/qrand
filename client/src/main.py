from .service import quantum
from random import Random
import requests

if __name__ == '__main__':
    gen = quantum.GenerateQRandService(Random())
    (a, x, vec) = gen.generate()

    r1 = requests.post('http://localhost:5000/measure', json = {'psi': [str(vec[0]), str(vec[1])]})
    r2 = requests.post('http://localhost:5000/verify', json={'a': a, 'x': x}, cookies = r1.cookies)