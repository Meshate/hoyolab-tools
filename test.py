def a(func):
    def w(t:int):
        if t != 1:
            print('None')
            raise Exception('None')
        print('n')
        return func(t)
    return w


from utils import log
@a
def test(t: int):
    print(t)

class t:
    def __init__(self):
        self.a = 1

if __name__ == '__main__':
    d = {
        1: 1
    }
    print(d.get(2))
