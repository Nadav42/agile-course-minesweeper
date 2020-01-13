import unittest

from GameManager import GameManager, Lobby

class LobbyTests(unittest.TestCase):

    # when I create a new GameManager then the lobby list is empty
    def test_no_lobbies(self):
        game_manager = GameManager()
        lobbies = game_manager.get_lobbies_list()

        self.assertTrue(len(lobbies) == 0)

    # when I create a new lobby then it is added to the lobby list with the same name
    def test_lobby_create(self):
        game_manager = GameManager()
        lobby_key = game_manager.create_lobby("TEST")

        lobbies = game_manager.get_lobbies_list()

        self.assertTrue(len(lobbies) == 1)
        self.assertEqual(lobbies[0]["key"], lobby_key)
        self.assertEqual(lobbies[0]["name"], "TEST")

    # when I create a new lobby with password it is marked as has password
    def test_lobby_password(self):
        game_manager = GameManager()
        game_manager.create_lobby("TEST", password="test")

        lobbies = game_manager.get_lobbies_list()

        self.assertTrue(lobbies[0]["hasPassword"])

    # test check_password_correct method - when I create a lobby with password test then checking same password will work
    def test_check_password_correct(self):
        game_manager = GameManager()
        lobby_key = game_manager.create_lobby("TEST", password="test")
        lobby: Lobby = game_manager.get_lobby(lobby_key)

        # password is encrypted
        self.assertNotEqual(lobby.password_encrypted, "test")

        # correct password is working and others are not
        self.assertTrue(lobby.check_password_correct("test"))
        self.assertFalse(lobby.check_password_correct("test1"))
        self.assertFalse(lobby.check_password_correct("1234"))

    # when I create a new lobby with password it is encrypted
    def test_lobby_password_encrypted(self):
        game_manager = GameManager()
        lobby_key = game_manager.create_lobby("TEST", password="test")

        lobby: Lobby = game_manager.get_lobby(lobby_key)

        self.assertNotEqual(lobby.password_encrypted, "test")
        self.assertTrue(lobby.check_password_correct("test"))

    # when I create two lobbies each lobby gets random salt and the encrypted password is different
    def test_lobby_random_salt(self):
        game_manager = GameManager()
        lobby_key1 = game_manager.create_lobby("TEST1", password="test")
        lobby_key2 = game_manager.create_lobby("TEST2", password="test")

        lobby1: Lobby = game_manager.get_lobby(lobby_key1)
        lobby2: Lobby = game_manager.get_lobby(lobby_key2)

        # each lobby has different salt, passwords are the same but encrypted values are not
        self.assertNotEqual(lobby1.salt, lobby2.salt)
        self.assertNotEqual(lobby1.password_encrypted, lobby2.password_encrypted)

        # both lobbies have same password
        self.assertTrue(lobby1.check_password_correct("test"))
        self.assertTrue(lobby2.check_password_correct("test"))

    # when I create X lobbies each lobby gets a random key
    def test_lobby_random_salt(self):
        game_manager = GameManager()
        all_keys = []

        for i in range(10):
            lobby_key = game_manager.create_lobby("TEST{}".format(i))
            all_keys.append(lobby_key)

        # remove duplicates with set, it should be equal
        removed_duplicates = list(set(all_keys))
        self.assertEqual(sorted(all_keys), sorted(removed_duplicates))

if __name__ == '__main__':
    unittest.main()
