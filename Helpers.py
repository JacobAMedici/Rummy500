from Card import *

def tally_scores(player):
  score = 0
  rank_score = {
    Rank.TWO: 5,
    Rank.THREE: 5,
    Rank.FOUR: 5,
    Rank.FIVE: 5,
    Rank.SIX: 5,
    Rank.SEVEN: 5,
    Rank.EIGHT: 5,
    Rank.NINE: 5,
    Rank.TEN: 10,
    Rank.JACK: 10,
    Rank.QUEEN: 10,
    Rank.KING: 10,
    Rank.ACE: 15
  }
  for card in player.runMelds:
    score += rank_score[card]
  for card in player.setMelds:
    score += rank_score[card]
  for card in player.hand:
    score -= rank_score[card]
  player.score += score