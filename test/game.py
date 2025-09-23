from Controller import Uno


game = Uno(2)




def test_shuffle():
    prev=game.deck.__hash__
    game.test()
    assert( game.deck.__hash__!=prev,"game stack not shuffled ")
