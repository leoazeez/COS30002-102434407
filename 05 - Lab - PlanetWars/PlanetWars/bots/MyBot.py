from math import sqrt

class MyBot(object):
    def update(self, gameinfo):
        print("MyBot Called")
        #pass
        # only send one fleet at a time
        if gameinfo.my_fleets:
            return 
        else:
            # check if we should attack
       
            if gameinfo.my_planets and gameinfo.not_my_planets:
                # sorting targets by num_ships (the weakest targets to strongest target)
                sorted_targets = sorted(gameinfo.not_my_planets.values(), key=lambda  p: p.num_ships)
                for elem in sorted_targets:
                    print("numer of ships::", elem.num_ships)

                best5targets = sorted_targets[:5]
                print("best 5 Targets", best5targets)

                #sort best targets by distance (so we can attack avoiding long fleet travel)
                my_planet =  list(gameinfo.my_planets.values())[0]
                print("my planet", my_planet)

                distance_target = {}
                for target in sorted_targets:
                    print("target ::{} my_planet:: {}".format(target,my_planet))
                    print("dist", my_planet.distance_to(target))
                    distance_target[target] = my_planet.distance_to(target)
                distance_sorted_targets = sorted(distance_target.items(), key=lambda kv: kv[1])
                print("final result === ", distance_sorted_targets)
          
                #Starting the attack
                gameinfo.log("Starting the Attack")
                gameinfo.log("-------------------------------------------------------------------------")
              
                for target in distance_sorted_targets:
                    gameinfo.log("New Turn :")
                    dest = target[0]
                    src = my_planet
                    gameinfo.planet_order(src, dest, src.num_ships)
                    print("sent {} ships from {} to {}".format(src.num_ships, src,dest))
                    
                gameinfo.log("-------------------------------------------------------------------------")
                gameinfo.log("End Of the Attack the Attack")

    def distance(self,planet1, planet2):
        if planet1.id == planet2.id:
            return 0.0
        dx = planet1.x - planet2.x
        dy = planet1.y - planet2.y
        return sqrt(dx * dx + dy * dy)