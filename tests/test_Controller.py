from Controller import Uno
from hashlib import md5
from player import Player
game = Uno(2)


TOTAL_CARDS=108

def test_shuffle():
    before=list_getHash(game.deck)
    game.shuffle_deck()
    after=list_getHash(game.deck)
    assert before!=after,"game stack not shuffled "
def test_generate_deck():
    assert len(game.generate_deck())==TOTAL_CARDS,"invalid number of Cards Generated"
def list_getHash(data):
    encode ="".join(data).encode()
    return md5(encode).digest()



#test ability for card to recycle played cards once card dealer depletes
def test_EndOFDeckTest():
    test_set=['B|7','Y|9','G|3',"R|1"]
    game.deck=[]
    game.prevUsedCards=test_set 
    game.recycleUsedCards() 
    for cards in test_set:
        assert cards in game.deck,"Card Failed To repopulate"

def test_player_init():
    test_count=5
    players =game.initPlayers(test_count)
    assert len(players)==test_count ,"Invalid Number of players bieng generated"
    for player in players:
        assert type(player) == Player ,"List of Players not bieng return from Player_init"
