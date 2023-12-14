import logging
import json
import os
import boto3
from botocore.exceptions import ClientError
from boto3.exceptions import Boto3Error
import random

class S3:
    BUCKET_NAME = ""
    boto3_resource = boto3.resource('s3',
        aws_access_key_id="",
        aws_secret_access_key=""
    )

    def get_item(self, key, bucket=BUCKET_NAME) -> str:
        try:
            info_file = self.boto3_resource.Object(bucket, key)
            info = info_file.get()["Body"].read()
            return info
        except Exception as e:
            return "Unable to delete object: %s"%(e)
        return None


    def put_item(self, key, content, bucket=BUCKET_NAME):
        try:
            self.boto3_resource.Object(bucket, key).put(Body=content)
        except:
            print("Unable to create text file")

s3 = S3()


class Room:

    def get(self, room_id):
        return json.loads(s3.get_item("room-%s.json"%room_id))

    def save(self, room):
        s3.put_item("room-%s.json"%room["pin"], json.dumps(room))

    def create_room(self):
        random_id = str(random.randint(10000,99999))[1:]
        room = {
            "pin": random_id,
            "players": [],
            "player_mimic": None,
            "player_guess": None,
            "current_card": None,
            "card_deck": [],
            "couples": [],
            "turn": None,
        }
        self.save(room)
        return room

    def add_user(self, room_id, name):
        room = self.get(room_id)
        if not room:
            return None
        player = {
           "name": name,
           "id": len(room["players"]),
           "points": 0
        }
        room["players"].append(player)
        self.save(room)
        return room

    def start_game(self, room_id):
        room = self.get(room_id)
        if room:

            n_players = len(room["players"])
            if n_players <= 1:
                return None
            room["turn"] = n_players-1
            room["couples"] = self.comb(n_players)
            room["card_deck"] = Person().get_people()
            random.shuffle(room["card_deck"])
            (p1, p2) = room["couples"].pop(0)
            room["player_mimic"] = p1
            room["player_guess"] = p2
            room["current_card"] = room["card_deck"].pop(0)
            self.save(room)
            return room
        else:
            return None

    def get_winner(self, room_id):
        room = self.get(room_id)
        max_score = 0
        players = []
        for i in room["players"]:
            if max_score < i["points"]:
                max_score = i["points"]
        for i in room["players"]:
            if i["points"] == max_score:
                players.append(i["name"])

        return (max_score,players)

    def next_couple(self, room_id):

        room = self.get(room_id)
        (p1, p2) = room["couples"].pop(0)
        room["player_mimic"] = p1
        room["player_guess"] = p2
        n_players = len(room["players"])
        if len(room["couples"]) == 0:
            room["couples"] = self.comb(n_players)

        room["current_card"] = room["card_deck"].pop(0)
        if len(room["card_deck"]) == 0:
            room["card_deck"] = Person().get_people()
            random.shuffle(room["card_deck"])

        if room["turn"] == 0:
            room["turn"] = len(room["players"])
        else:
            room["turn"] -= 1
        self.save(room)
        return room

    def add_points(self, room_id, points):
        room = self.get(room_id)
        room["players"][room["player_mimic"]]["points"] += points
        room["players"][room["player_guess"]]["points"] += points
        self.save(room)
        return room

    def new_round(self, room_id):
        room = self.get(room_id)
        room["turn"] = len(room["players"])
        self.save(room)
        return room

    def comb(self, n):
        all_combs = [(x,y) for y in range(n) for x in range(n) if x != y]
        random.shuffle(all_combs)
        users = list(range(n))
        random.shuffle(users)
        couples = []
        while len(all_combs) > 0:
            for i in users:
                for j in all_combs:
                    if j[0] == i:
                        couples.append(j)
                        all_combs.remove(j)
                        break
        return couples

class Person:

    def get_people(self):
        return json.loads(s3.get_item("people.json"))["mujeres"]

    def filter(self, key, value):
        f = []
        for person in self.get_people():
            if person[key] == value:
                f.append(person)
        return f

























