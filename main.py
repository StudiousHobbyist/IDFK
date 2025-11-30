import random

rooms = {}
current_room = "main"

def create_room(name):
    """Create a room with no connections yet if it doesn't exist."""
    if name not in rooms:
        rooms[name] = {"name": name, "connections": [], "enemies": []}
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

# entity class and related functions
class Entity:
    def __init__(self, name, health, max_health, base_attack_power, base_defense, status_effects=list):
        self.name = name
        self.health = health
        self.max_health = max_health
        self.base_attack_power = base_attack_power
        self.base_defense = base_defense
        self.status_effects = status_effects

    def __repr__(self):
        """String representation of the Enemy object."""

        Name = f"Name: {self.name}"
        Health = f", Health: {self.health}/{self.max_health}"
        AP = f", Attack Power: {self.base_attack_power}"
        Defense = f", Defense: {self.base_defense}\n"
        StatusEffects = f", Status Effects: " + "; ".join(se.name for se in 
                                                          self.status_effects) if self.status_effects else ", No Status Effects"

        return Name + Health + AP + Defense + StatusEffects


statuseffects = []
class StatusEffect:
    def __init__(self, name, duration, base_scale, factor, effect):
        self.name = name
        self.duration = duration #measured in turns
        self.base_scale = base_scale
        self.factor = factor
        self.effect = effect

    def __repr__(self):
        """String representation of the Debuff object."""

        Name = f"Debuff Name: {self.name}"
        Duration = f", Duration: {self.duration}"
        Base_Scale = f", Base Scale: {self.base_scale}"
        Factor = f", Factor: {self.factor}"
        Effect = f", Effect: {self.effect}"

        return Name + Duration + Effect

def create_status_effect(name, duration, effect):
    se = StatusEffect(name, duration, effect)
    statuseffects.append(se)
    return se
def list_status_effects():
    for se in statuseffects:
        print(se)
def get_status_effect_by_name(name):
    for se in statuseffects:
        if se.name == name:
            return se
    print(f"Status effect '{name}' not found.")
    return None
def debug_status_effects():
    print("Debugging Status Effects:")
    Poison = create_status_effect("Poison", 3, 1, 1,"Lose 5 health each turn")
    Stun = create_status_effect("Stun", 1, 1, 1,"Skip next turn")
    Regeneration = create_status_effect("Regeneration", 4, 1, 1,"Gain 3 health each turn")
    list_status_effects()
    return Poison, Stun, Regeneration

moves = []
class AttackMove:
    def __init__(self, name, attack, heal, accuracy,crit_factor, status_effects=list):
        self.name = name
        self.attack = attack
        self.heal = heal
        self.accuracy = accuracy
        self.crit_factor = crit_factor
        self.status_effects = status_effects
        
    def __repr__(self):
        """String representation of the AttackMove object."""
        Name = f"Move Name: {self.name}"
        Attack = f", Attack: {self.attack}"
        Heal = f", Heal: {self.heal}"
        Accuracy = f", Accuracy: {self.accuracy}%"
        Crit_factor = f", Crit Factor: {self.crit_factor}"  

        # Build status effects string
        if self.status_effects:
            StatusEffects = ", Status Effects: " + "; ".join(se.name for se in self.status_effects)
        else:
            StatusEffects = "No Status Effects"

        return Name + Attack + Heal + Accuracy + Crit_factor + StatusEffects
def create_move(name, attack, heal, accuracy, status_effects=list):
    am = AttackMove(name, attack, heal, accuracy, status_effects)
    moves.append(am)
    return am
def list_moves():
    for move in moves:
        print(move)
def get_move_by_name(name):
    for move in moves:
        if move.name == name:
            return move
    print(f"Move '{name}' not found.")
    return None
def debug_moves():
    Poison, Stun, Regeneration = debug_status_effects()
    create_move("Slash", 10, 0, 90, [Poison])
    create_move("Heal", 0, 15, 100, [Regeneration]) 
    create_move("Stunning Blow", 8, 0, 80, [Stun])
    list_moves()
    print("Debugging Moves:")

# IDK features
def apply_damage(attacker: Entity, defender: Entity, move: AttackMove):
    """Calculate and apply damage from attacker to defender."""
    
    critical_factor = AttackMove.crit_factor
    critical_hit = False
    damage = 0
    accolades= []
    if random.randint(1, 100) == move.accuracy:
        accolades.append("Perfect Hit")
        critical_hit = True
    if random.randint(1, 100) < move.accuracy:
        if AttackMove.attack > 0:
            if critical_hit:
                damage = attacker.base_attack_power * critical_factor - defender.base_defense
            else:
                damage = attacker.base_attack_power - defender.base_defense

            if damage < 0:
                damage = 0  # No negative damage
            elif damage == 0:
                accolades.append("Graceful Miss")
            elif damage >= defender.health * 10:
                accolades.append("Overkill")

            defender.health -= damage

        if AttackMove.heal > 0:
            if attacker.health == attacker.max_health:
                accolades.append("Full Health Heal Waste")
            if attacker.health == attacker.max_health - move.heal:
                accolades.append("Perfect Heal")
            if attacker.health == 1:
                accolades.append("Clutch Heal")
                if attacker.health + move.heal >= attacker.max_health:
                    accolades.append("Clutch Full Heal")
            heal_amount = move.heal
            attacker.health += heal_amount
            if attacker.health > attacker.max_health:
                attacker.health = attacker.max_health

            

        

    return attacker, defender, damage, accolades 

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
    # main()
    _e = Entity("Goblin", 30, 5, 2)
    print(_e)
