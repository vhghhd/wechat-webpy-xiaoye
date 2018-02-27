#!/usr/bin/python2.4
#
# pylint: disable-msg=C6310

"""Channel Tic Tac Toe
This module demonstrates Sina App Engine Channel API by implementing a
simple tic-tac-toe game.
"""
import web
import datetime
import logging
import os
import random
import re
import json
import uuid

import pylibmc as memcache
from sae import channel

mc = memcache.Client()

class Game:
	"""All the data we store for a game"""
	def __init__(self, key_name, **args):
		self.key_name = key_name
		self.userX = args.get('userX')
		self.userO = args.get('userO')
		self.board = args.get('board')
		self.moveX = args.get('moveX')
		self.winner = args.get('winner')
		self.winning_board = args.get('winning_board')

	@classmethod
	def get_by_key_name(cls, key_name):
		if isinstance(key_name, unicode):
			key_name = key_name.encode('utf8')
		data = mc.get(key_name)
		if data:
			return cls(key_name, **data)

	def put(self):
		mc.set(self.key_name, {
			'userX': self.userX,
			'userO': self.userO,
			'board': self.board,
			'moveX': self.moveX,
			'winner': self.winner,
			'winning_board': self.winning_board,})
  
class Wins():
	x_win_patterns = ['XXX......',
					'...XXX...',
					'......XXX',
					'X..X..X..',
					'.X..X..X.',
					'..X..X..X',
					'X...X...X',
					'..X.X.X..']

	o_win_patterns = map(lambda s: s.replace('X','O'), x_win_patterns)
  
	x_wins = map(lambda s: re.compile(s), x_win_patterns)
	o_wins = map(lambda s: re.compile(s), o_win_patterns)


class GameUpdater():
	game = None

	def __init__(self, game):
		self.game = game

	def get_game_message(self):
		gameUpdate = {"board": self.game.board,"userX": self.game.userX,"userO": "" if not self.game.userO else self.game.userO,"moveX": self.game.moveX,"winner": self.game.winner,"winningBoard": self.game.winning_board}
		return json.dumps(gameUpdate)
		return gameUpdate

	def send_update(self):
		message = self.get_game_message()
		channel.send_message(self.game.userX + self.game.key_name, message)
		if self.game.userO:
			channel.send_message(self.game.userO + self.game.key_name, message)

	def check_win(self):
		if self.game.moveX:
		# O just moved, check for O wins
			wins = Wins().o_wins
			potential_winner = self.game.userO
		else:
			# X just moved, check for X wins
			wins = Wins().x_wins
			potential_winner = self.game.userX
      
		for win in wins:
			if win.match(self.game.board):
				self.game.winner = potential_winner
				self.game.winning_board = win.pattern
				return

	def make_move(self, position, user):
		if position >= 0 and user == self.game.userX or user == self.game.userO:
			if self.game.moveX == (user == self.game.userX):
				boardList = list(self.game.board)
				if (boardList[position] == ' '):
					boardList[position] = 'X' if self.game.moveX else 'O'
					self.game.board = "".join(boardList)
					self.game.moveX = not self.game.moveX
					self.check_win()
					self.game.put()
					self.send_update()
		return

class TheXOGame():
	def __init__(self):
		self.app_root = os.path.dirname(__file__)
		self.templates_root = os.path.join(self.app_root,'template')
		self.render = web.template.render(self.templates_root)

	def GET(self):
		"""Renders the main page. When this page is shown, we create a new
		channel to push asynchronous updates to the client."""
		data = web.input()
		user = web.cookies().get('u')
		#user = self.get_secure_cookie('u')
		user = None
		if user is None:
			user = uuid.uuid4().hex
			#self.set_secure_cookie('u', user)
			web.setcookie('u', user, 600)
		#game_key = self.get_argument('g', None)
		game_key = None
		try:
			game_key = data['g']
		except:
			game_key = None
		if game_key is None:
			game_key = user
			game = Game(key_name = game_key,
				userX = user,
				moveX = True,
				board = "         ")
			game.put()
		else:
			game = Game.get_by_key_name(game_key)
			if game and not game.userO:
				game.userO = user
				game.put()

		game_link = '/firstgame?g=' + game_key

		if game:
			url = channel.create_channel(user + game_key)
			template_values = {'url': url,
						'me': user,
						'game_key': game_key,
						'game_link': game_link,
						'initial_message': GameUpdater(game).get_game_message()
			}
			#path = os.path.join(os.path.dirname(__file__), 'index.html')
			return self.render.firstgame(template_values)
		else:
			return 'No such game'

		pass
	def POST(self,start=None):
		data = web.input()
		print data,start
		if start:
			try:
				game_key = data['g']
				game = Game.get_by_key_name(game_key)
				user = web.cookies().get('u')
				if game and user:
					id = int(data['i'])
					GameUpdater(game).make_move(id, user)
			except:
				return "Post Error"
		else:
			try:
				game_key = data['g']
				game = Game.get_by_key_name(game_key)
				GameUpdater(game).send_update()
			except:
				return "Post Error"
		return self.render.firstgame()
		#game_key = self.get_argument('g')
		#game = Game.get_by_key_name(game_key)
		#user = self.get_secure_cookie('u')
		#if game and user:
		#	id = int(self.get_argument('i'))
		#	GameUpdater(game).make_move(id, user)
