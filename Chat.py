# TODO: Group chat

from collections import defaultdict
from uuid import uuid4


class User:
    def __init__(self, uid, name, service):
        self.uid = uid
        self.name = name
        self.service = service
        self.friends = []

    def send_friend_request(self, id):
        self.service.handle_friend_request(self.uid, id)

    def notify_friend_acceptance(self, result, friend):
        if result:
            print('Hey, {0}, {1} has accepted you a friend request'.format(
                self.name, friend.name))
            print('Why not send a message?')
            message = input()
            self.send_message(friend.uid, message)
        else:
            print('Hey, {0}, {1} has rejected you a friend request'.format(
                self.name, friend.name))

    def accept_friend_request(self, name):
        print('Hey, {0}, {1} has sent you a friend request. Accept or Reject?'.format(
            self.name, name))
        answer = input()
        return answer.lower() == 'accept'

    def open_chat(self, friend_id):
        self.service.open_chat(self.uid, friend_id)

    def send_message(self, friend_id, message):
        self.service.deliver_message(self.uid, friend_id, message)

    def read_chat(self, friend_id):
        self.service.lookup_chat(self.uid, friend_id)

    def notify_new_message(self, sender):
        print('Hey, {0}, {1} has sent you a new message. Want to check it out? Yes or No'.format(
            self.name, sender.name))
        check = input()
        if check.lower() == 'yes':
            self.read_chat(sender.uid)


class Message:
    def __init__(self, uid, content):
        self.uid = uid
        self.content = content


class Chat:
    def __init__(self, uid1, uid2):
        self.users = [uid1, uid2]
        self.messages = []

    def add_message(self, new_message):
        self.messages.append(new_message)

    def read_messages(self):
        for message in self.messages:
            print(message.content)


class Service:
    def __init__(self):
        self.users = defaultdict()
        self.chats = defaultdict()

    def register_user(self, name):
        uid = str(uuid4())
        new_user = User(uid, name, self)
        self.users[uid] = new_user
        return new_user

    def show_users(self):
        for v in self.users.values():
            print(v.uid, v.name)

    def handle_friend_request(self, uid, id):
        sender = self.users[uid]
        responder = self.users[id]
        if responder.accept_friend_request(sender.name):
            responder.friends.append(uid)
            sender.friends.append(id)
            sender.notify_friend_acceptance(True, responder)
        else:
            sender.notify_friend_acceptance(False, responder)

    def chat_key_generate(self, id1, id2):
        return "".join(sorted([id1, id2]))

    def open_chat(self, uid, friend_id):
        key = self.chat_key_generate(uid, friend_id)
        if not key in self.chats:
            self.chats[key] = Chat(uid, friend_id)

    def deliver_message(self, uid, friend_id, message):
        new_message = Message(uid, message)
        key = self.chat_key_generate(uid, friend_id)
        if key not in self.chats:
            self.open_chat(uid, friend_id)
        self.chats[key].add_message(new_message)
        self.users[friend_id].notify_new_message(self.users[uid])

    def lookup_chat(self, uid, friend_id):
        key = self.chat_key_generate(uid, friend_id)
        if key in self.chats:
            self.chats[key].read_messages()


service = Service()
user1 = service.register_user('Tetsuya')
user2 = service.register_user('Yayoi')
user3 = service.register_user('Ganko')
service.show_users()
friend = input()
user1.send_friend_request(friend)
