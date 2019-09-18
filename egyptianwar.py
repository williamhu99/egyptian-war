import sys
import pygame
import pygame.locals
from random import shuffle

pygame.init()

# Defines a Card class with a suit and rank
class Card:
	def __init__(self, suit, rank):
		self.suit = suit
		self.rank = rank
	# Turns 1, 11, 12, 13 to their proper ranks
	def __str__(self):
		if self.rank == 1:
			return self.suit + "A"
		elif self.rank == 11:
			return self.suit + "J"
		elif self.rank == 12:
			return self.suit + "Q"
		elif self.rank == 13:
			return self.suit + "K"
		else:
			return self.suit + str(self.rank)

# Defines the match function which checks if one of the players made a valid slap
def match(seen):
	length = len(seen)
	if (length <= 1):
		return False
	# Two in a row
	if (seen[length - 1].rank == seen[length - 2].rank):
		return True
	# Marriage
	elif (seen[length - 1].rank + seen[length - 2].rank == 25):
		return True
	# Sums to 10
	elif (seen[length - 1].rank + seen[length - 2].rank == 10):
		return True
	# Sandwich
	elif (length >= 3 and seen[length - 1].rank == seen[length - 3].rank):
		return True
	# Top-bottom
	elif (seen[0].rank == seen[length - 1].rank):
		return True
	# Four-in-a-row
	elif (length >= 4):
		# Four of the same suit
		if (seen[length - 1].suit == seen[length - 2].suit and
			seen[length - 2].suit == seen[length - 3].suit and
			seen[length - 3].suit == seen[length - 4].suit):
			return True
		# Ascending order
		elif (seen[length - 1].rank % 13 == (seen[length - 2].rank + 1) % 13 and
			seen[length - 2].rank % 13 == (seen[length - 3].rank + 1) % 13 and
			seen[length - 3].rank % 13 == (seen[length - 4].rank + 1) % 13):
			return True
	return False

# Creates the standard 52 card deck
deck = []
for suit in ["♠", "♥", "♦", "♣"]:
	for rank in range(1, 14):
		deck.append(Card(suit, rank))

print("Welcome to Egyptian War!")
print("Please read the rules if this is your first time playing.")
print("The game reads your keyboard inputs, so do not click the terminal window!")
print("Press 'X' to quit and 'B' to begin!")

# Initializes variables for the game
started = 0					# started tracks whether the game has started
turn = 0					# turn indicates which player moves next
shuffle(deck)				# shuffles the deck
player1 = deck[0:26]		# player1's deck
player2 = deck[26:52]		# player2's deck
card = 0					# current card (initially initialized to 0)
seen = []					# cards that have been seen in the current round

while True:
	# Reads keyboard input
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if not started:
				# 'X' exits an unstarted game
				if event.key == pygame.K_x:
					sys.exit(0)
				# 'B' starts the game
				elif not started and event.key == pygame.K_b:
					print(str(len(player1)) + "\tCurrent Card: N/A\t" +
						str(len(player2)) + "\t" + str(turn + 1))
					started = 1
			elif started:
				# 'A' reveals the top card of Player 1's deck
				if turn == 0 and event.key == pygame.K_a:
					card = player1.pop()
					seen.append(card)
					turn = 1
					print(str(len(player1)) + "\tCurrent Card: " + str(card) +
						"\t" + str(len(player2)) + "\t" + str(turn + 1))
				# 'K' reveals the top card of Player 2's deck
				elif started and turn == 1 and event.key == pygame.K_k:
					card = player2.pop()
					seen.append(card)
					turn = 0
					print(str(len(player1)) + "\tCurrent Card: " + str(card) +
						"\t" + str(len(player2)) + "\t" + str(turn + 1))
				# 'S' is Player 1's way of slapping the deck
				elif card != 0 and event.key == pygame.K_s:
					if match(seen):
						# Adds the seen cards to Player 1's deck if the slap was valid
						player1 = seen[::-1] + player1
						seen = []
						print("Nice slap Player 1!")
						print(str(len(player1)) + "\tCurrent Card: N/A\t" +
							str(len(player2)) + "\t" + str(turn + 1))
						card = "N/A"
					else:
						# Burns the top three cards if the slap was not valid
						print("Sorry! That was not a match.")
						for i in range(3):
							if (len(player1) == 0):
								print("Player 2 wins!")
								sys.exit(0)
							player1.pop()
						print(str(len(player1)) + "\tCurrent Card: " + str(card) +
							"\t" + str(len(player2)) + "\t" + str(turn + 1))
				# 'L' is Player 2's way of slapping the deck
				elif card != 0 and started and event.key == pygame.K_l:
					if match(seen):
						# Adds the seen cards to Player 2's deck if the slap was valid
						player2 = seen[::-1] + player2
						seen = []
						print("Nice slap Player 2!")
						print(str(len(player1)) + "\tCurrent Card: N/A\t" +
							str(len(player2)) + "\t" + str(turn + 1))
						card = "N/A"
					else:
						# Burns the top three cards if the slap was not valid
						print("Sorry! That was not a match.")
						for i in range(3):
							if (len(player2) == 0):
								print("Player 1 wins!")
								sys.exit(0)
							player2.pop()
						print(str(len(player1)) + "\tCurrent Card: " + str(card) +
							"\t" + str(len(player2)) + "\t" + str(turn + 1))

	# If either player's decks hit 0, then the other player wins
	if (len(player1) == 0):
		print("Player 2 wins!")
		sys.exit(0)
	elif (len(player2) == 0):
		print("Player 1 wins!")
		sys.exit(0)