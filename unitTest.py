import unittest
import flaskServer

server = flaskServer.Server()


class FlagTest(unittest.TestCase):
    def test_flags(self):
        self.assertEqual(server.check_flag_test('http://www.clipartbest.com/cliparts/7Ta/ojG/7TaojGyEc.png'), 'england')
        self.assertEqual(server.check_flag_test('http://www.all-flags-world.com/country-flag/Italy/flag-italy-XL.jpg'), 'italy')
        self.assertEqual(server.check_flag_test('https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/Civil_and_Naval_Ensign_of_France.svg/2000px-Civil_and_Naval_Ensign_of_France.svg.png'), 'france')
        self.assertEqual(server.check_flag_test('http://wallpapercave.com/wp/4bVDS7e.jpg'), 'france')
        self.assertEqual(server.check_flag_test('https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Flag_of_Chile.svg/1500px-Flag_of_Chile.svg.png'), 'chile')


if __name__ == '__main__':
    unittest.main()