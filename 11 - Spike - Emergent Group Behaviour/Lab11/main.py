'''Autonomous Agent Movement: Paths and Wandering

Created for COS30002 AI for Games by Clinton Woodward <cwoodward@swin.edu.au>

For class use only. Do not publically share or post this code without permission.

This code is essentially the same as the base for the previous steering lab
but with additional code to support this lab.

'''
from graphics import egi, KEY
from pyglet import window, clock
from pyglet.gl import *

from vector2d import Vector2D
from world import World
from agent import Agent, AGENT_MODES  # Agent with seek, arrive, flee and pursuit


def on_mouse_press(x, y, button, modifiers):
    if button == 1:  # left
        world.target = Vector2D(x, y)


def on_key_press(symbol, modifiers):
    if symbol == KEY.P:
        world.paused = not world.paused
    elif symbol in AGENT_MODES:
        for agent in world.agents:
            agent.mode = AGENT_MODES[symbol]
    # Toggle debug force line info on the agent
    elif symbol == KEY.I:
        for agent in world.agents:
            agent.show_info = not agent.show_info

    #multiple agents
    elif symbol == KEY.M:
        for i in range(10):
            #creating 10agents
            agent = Agent(world)
            agent.color = "AQUA"
            world.agents.append(agent)

    elif symbol == KEY.S:
        world.separation_param += 20
        print("separation parameter increased by 20")
    elif symbol == KEY.E:
        if(world.separation_param>20):
            world.separation_param -= 20
            print("separation parameter decreased by 20")

    elif symbol == KEY.C:
        world.cohesion_param += 20
        print("cohesion parameter increased by 20")
    elif symbol == KEY.O:
        if(world.cohesion_param>20):
            world.cohesion_param -= 20
            print("cohesion parameter decreased by 20")

    elif symbol == KEY.A:
        world.alignment_param += 20
        print("alignment parameter increased by 20")
    elif symbol == KEY.L:
        if(world.alignment_param>20):
            world.alignment_param -= 20
            print("alignment parameter decreased by 20")


def on_resize(cx, cy):
    world.cx = cx
    world.cy = cy


if __name__ == '__main__':

    # create a pyglet window and set glOptions
    win = window.Window(width=500, height=500, vsync=True, resizable=True)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # needed so that egi knows where to draw
    egi.InitWithPyglet(win)
    # prep the fps display
    fps_display = window.FPSDisplay(win)
    # register key and mouse event handlers
    win.push_handlers(on_key_press)
    win.push_handlers(on_mouse_press)
    win.push_handlers(on_resize)

    # create a world for agents
    world = World(500, 500)
    # add one agent
    master_agent = Agent(world)
    master_agent.is_master_agent = True
    world.agents.append(master_agent)
    # unpause the world ready for movement
    world.paused = False

    while not win.has_exit:
        win.dispatch_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # show nice FPS bottom right (default)
        delta = clock.tick()
        world.update(delta)
        world.render()
        fps_display.draw()
        # swap the double buffer
        win.flip()

