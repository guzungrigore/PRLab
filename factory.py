from player import Player
import xml.etree.ElementTree as ET
import player_pb2


class PlayerFactory:
    def to_json(self, players):
        player_list = []
        for player in players:
            player_dict = {"nickname": player.nickname, "email": player.email,
                           "date_of_birth": player.date_of_birth.strftime("%Y-%m-%d"), "xp": player.xp,
                           "class": player.cls}
            player_list.append(player_dict)
        return player_list

    def from_json(self, list_of_dict):
        players = []
        for player_dict in list_of_dict:
            player = Player(player_dict["nickname"], player_dict["email"], player_dict["date_of_birth"],
                            player_dict["xp"], player_dict["class"])
            players.append(player)
        return players

    def from_xml(self, xml_string):
        players = []
        root = ET.fromstring(xml_string)
        for player_elem in root.findall('player'):
            nickname = player_elem.findtext('nickname')
            email = player_elem.findtext('email')
            date_of_birth = player_elem.findtext('date_of_birth')
            xp = int(player_elem.findtext('xp'))
            cls = player_elem.findtext('class')
            player = Player(nickname, email, date_of_birth, xp, cls)
            players.append(player)
        return players

    def to_xml(self, list_of_players):
        root = ET.Element('data')

        for player in list_of_players:
            player_elm = ET.SubElement(root, 'player')
            ET.SubElement(player_elm, 'nickname').text = player.nickname
            ET.SubElement(player_elm, 'email').text = player.email
            ET.SubElement(player_elm, 'date_of_birth').text = player.date_of_birth.strftime("%Y-%m-%d")
            ET.SubElement(player_elm, 'xp').text = str(player.xp)
            ET.SubElement(player_elm, 'class').text = player.cls

        xml_string = ET.tostring(root)
        return xml_string

    def from_protobuf(self, binary):
        '''
            This function should transform a binary protobuf string into a list with Player objects.
        '''
        players_message = player_pb2.PlayersList()
        players = []

        for player_message in players_message.player:
            player = Player(
                nickname=player_message.nickname,
                email=player_message.email,
                date_of_birth=player_message.date_of_birth,
                xp=player_message.xp,
                cls=players_message.cls
            )
            players.append(player)
        return players

    def to_protobuf(self, list_of_players):
        '''
            This function should transform a list with Player objects into a binary protobuf string.
        '''
        players_list = player_pb2.PlayersList()

        for player in list_of_players:
            player_message = players_list.player.add()
            player_message.nickname = player.nickname
            player_message.email = player.email
            player_message.date_of_birth = player.date_of_birth.strftime("%Y-%m-%d")
            player_message.xp = player.xp
            player_message.cls = player.cls

        return players_list.SerializeToString()
