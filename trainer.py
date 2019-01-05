#!/usr/bin/python
#-*-coding: utf-8 -*-
import json
import sys
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

BOT_NAME = "Bot"

chatbot = ChatBot(
                    BOT_NAME,
                    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
                    database="chatterbot-database",
                    logic_adapters=[
                      "chatterbot.logic.MathematicalEvaluation",
                      "chatterbot.logic.TimeLogicAdapter",
                      "chatterbot.logic.ClosestMatchAdapter"
                    ],
                    filters=[
                      'chatterbot.filters.RepetitiveResponseFilter'
                    ],
                  )

conversation_file = sys.argv[1]

conversations = json.loads(open(conversation_file).read())

print ("[-] Start training bot")
chatbot.set_trainer(ListTrainer)
chatbot.train(conversations)
print ("[-] Train success")
