from random import choice

class BestTarget(object):
    def update(self, gameinfo):
        print("BestTarget (target with min number of ships)")
        if gameinfo.my_fleets:
            return 
        else:
            # check if we should attack
            if gameinfo.my_planets and gameinfo.not_my_planets:
                # select the best target as a destination (the one that have the min number of ships)
                dest = min(gameinfo.not_my_planets.values(), key=lambda p: p.num_ships)
                src = choice(list(gameinfo.my_planets.values()))
                # launch new fleet if there's enough ships
                if src.num_ships > 10:
                    gameinfo.planet_order(src, dest, int(src.num_ships * 0.75))