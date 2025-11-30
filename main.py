rooms = {}
current_room = "main"

def create_room(name):
    """Create a room with no connections yet if it doesn't exist."""
    if name not in rooms:
        rooms[name] = {"name": name, "connections": []}
def connect_rooms(room1: str, room2: str):
    """
    Connect two rooms to each other (inverted connections).
    This ensures both sides update automatically.
    """
    create_room(room1.lower())
    create_room(room2.lower())

    if room2.lower() not in rooms[room1.lower()]["connections"]:
        rooms[room1.lower()]["connections"].append(room2.lower())

    if room1.lower() not in rooms[room2.lower()]["connections"]:
        rooms[room2.lower()]["connections"].append(room1.lower())
def list_rooms():
    for room in rooms.values():
        print(f"Room Name: {room['name']}, Connections: {room['connections']}")
def list_connections_to_room(room_name):
    print(f"Rooms connected to '{room_name}': {rooms[room_name]['connections']}")
def debug_rooms():
    print("Debugging Rooms:")
    connect_rooms("Main", "Lobby")
    connect_rooms("Main", "Game Room")
    connect_rooms("Lobby", "Cafeteria")
    connect_rooms("Game Room", "Cafeteria")
    connect_rooms("Cafeteria", "Garden")
    connect_rooms("Main", "Hallway 1")
    connect_rooms("Hallway 1", "Garden")

    list_rooms()

def main():
    # Room navigation loop

    
    global current_room

    debug_rooms()
    _LOOP = True
    while _LOOP:

        _SELCTROOM = True
        while _SELCTROOM:
            selectable_rooms = rooms[current_room]["connections"]

            choice = input(
                f"\nCurrent room: '{current_room}'\n"
                f"Select a room: {selectable_rooms}\n"
                f"Or type 'exit' to quit: "
            ).lower()

            if choice.lower() == 'exit':
                print("Exiting program.")
                break
            if choice in selectable_rooms:
                current_room = choice
                _SELCTROOM = False
            else:
                print("Invalid room selection. Please try again.")
        

    

if __name__ == "__main__":
    main()
