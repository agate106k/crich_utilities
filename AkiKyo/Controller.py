import sqlite3

class Controller:
    WEEKDAY = {
            "月": 1,
            "火": 2,
            "水": 3,
            "木": 4,
            "金": 5,
            "土": 6,
            "日": 7
    }

    UNAVROOM = ['325', '326', '327', '328', '329', '701', '702', '703', '704', '831', 'DB105', 'DB106', 'DB107', 'DB108', 'DB109', 'DB110', 'DB111', 'DB112', 'DB113', 'F01']
    HIDEROOM = ['304', 'D201', 'D305', 'D311', 'J431A', 'J444', 'J611', 'J634']

    def __init__(self):
        self.connection = sqlite3.connect("syllabus.db", check_same_thread=False)
        self.cursor = self.connection.cursor()

    def _filterRoom(self, roomTuple:tuple, showAll:bool=False) -> tuple:
        roomList = list(roomTuple)
        roomList = [room for room in roomList if not(len(room) == 3 and room[0] == '2')]
        roomList = [room for room in roomList if not(room[0] == 'C')]
        roomList = [room for room in roomList if room not in Controller.UNAVROOM]
        if not showAll:
            roomList = [room for room in roomList if room not in Controller.HIDEROOM]

        return tuple(sorted(roomList))

    def _parseHourText(self, hour: str) -> tuple:
        if len(hour) != 2:
            raise ValueError("Hour must be a string composed of WEEKDAY and TIME")
        
        try:
            day = Controller.WEEKDAY[hour[0]]
            time = int(hour[1])
        except KeyError:
            raise ValueError("WEEKDAY must be one of 月火水木金土日")
        except ValueError:
            raise ValueError("TIME must be an integer 1-7")

        return (day, time)

    def _sortRoom(self, rooms: tuple) -> dict:
        builds = {
            "第3校舎": [],
            "第4校舎A棟": [],
            "第4校舎B棟": [],
            "第4校舎独立館": [],
            "第6校舎": [],
            "第7校舎": [],
            "第8校舎": []
        }

        for room in rooms:
            if len(room) == 2 or len(room.strip('J')) == 2:
                builds["第4校舎B棟"].append(room)
            elif room.startswith("J4"):
                builds["第4校舎A棟"].append(room)
            elif room.startswith("D"):
                builds["第4校舎独立館"].append(room)
            else:
                builds[f"第{room[0] if not room.startswith('J6') else '6'}校舎"].append(room)

        return builds

    def getRoomInUse(self, hour: str) -> tuple:
        hour = self._parseHourText(hour)
        
        self.cursor.execute(f"SELECT room FROM items WHERE weekday={hour[0]} AND hour={hour[1]}")
        usedRoom = self.cursor.fetchall()
        usedRoom = tuple(item for sublist in usedRoom for item in sublist)

        return usedRoom

    def getRoomNotInUse(self, hour:str, showAll:bool=False) -> tuple:        
        usedRoom = self.getRoomInUse(hour)
        allRoom = self.getRoomTuple()

        hour = self._parseHourText(hour)

        unusedRoom = set(usedRoom) ^ set(allRoom)
        emptyRoom = []
        for room in unusedRoom:
            if room.isalnum() and room.isascii():
                emptyRoom.append(room)
        
        return self._filterRoom(emptyRoom, showAll)

    def getRoomTuple(self) -> tuple:
        self.cursor.execute("SELECT room FROM items")
        roomTuple = self.cursor.fetchall()
        roomTuple = tuple(item for sublist in roomTuple for item in sublist)

        return roomTuple

    def sendMessage(self, hour: str) -> str:
        showAll = False
        if "supeniki" in hour:
            showAll = True
            hour = hour.strip("supeniki").strip(" ").strip("　")

        if hour[1] == "曜" and hour[3] == "限" and len(hour) == 4:
            hour = hour[0] + hour[2]
        
        usedRoom = self.getRoomNotInUse(hour, showAll)
        sortedRoom = self._sortRoom(usedRoom)

        roomString = ""

        for i in sortedRoom:
            if sortedRoom[i] != []:
                roomString += f"""【{i}】
{', '.join(sortedRoom[i])}

"""

        return f"""{hour[0]}曜{hour[1]}限の空き教室はこちらです👇👇

{roomString}教室への行き方は教室名を送信すると見る事ができますので是非ご活用ください！"""
