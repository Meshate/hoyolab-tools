def a(func):
    def w(t:int):
        if t != 1:
            print('None')
            raise Exception('None')
        print('n')
        return func(t)
    return w

def c(func):
    def w(*argc):



@a
def test(t: int):
    print(t)

if __name__ == '__main__':
    test(2)