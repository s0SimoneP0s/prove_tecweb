class Duck:

    def verso(self):
        print("QUACK")
    

class Donkey:

    def verso(self):
        print("IOOOOHH")


def fai_verso(a):
    a.verso()

fai_verso(Duck())
fai_verso(Donkey())






