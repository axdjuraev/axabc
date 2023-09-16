from autopass import AutoPass

def a(a: int, b, c):
    print('   ', [1, 2, 3])

AutoPass.pass_(a, kwargs={'b': 2, 'c': 3})
