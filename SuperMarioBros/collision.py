from pico2d import *
import server
import game_world
import cItem


def check_collision(o1, o2, index1=0, index2=0):
    a1, a2, a3, a4 = o1.get_bb(index1)
    b1, b2, b3, b4 = o2.get_bb(index2)

    if a1 > b3 or a3 < b1:  # x축
        return False
    if a4 < b2 or a2 > b4:  # y축
        return False

    return True


def collide_update():
    # mario and enemy
    for enemy in server.enemies:
        if check_collision(server.mario, enemy) and enemy.state == 0:
            if server.mario.yPos > enemy.yPos:
                enemy.state = 1
                server.mario.jump(1)
            else:
                if server.mario.trans >= 0 and not server.mario.invincibility:
                    server.mario.trans -= 1
                    if server.mario.trans == 0 or server.mario.trans == 1:
                        server.mario.hit_sound.play()
                    server.mario.invincibility = True
                    break

    # mario and block
    for block in server.floorBlocks:
        if check_collision(server.mario, block):
            server.mario.fall_speed = 0
            server.mario.yPos = block.yPos + 15 + 16

    for block in server.itemBlocks:
        if check_collision(server.mario, block):
            server.mario.fall_speed = 0
            server.mario.yPos = block.yPos + 15 + 16
        elif check_collision(server.mario, block, 0, 1):
            if block.item == 1 and block.frame != 3:
                server.items += [cItem.Mushroom(block.xPos, block.yPos)]
                game_world.add_objects(server.items, 1)
                server.mario.block_sound.play()
            elif block.item == 2 and block.frame != 3:
                server.items += [cItem.Flower(block.xPos, block.yPos)]
                game_world.add_objects(server.items, 1)
                server.mario.block_sound.play()
            server.mario.yPos = block.yPos - 15 - 16
            block.frame = 3

    for block in server.brickBlocks:
        if check_collision(server.mario, block):
            server.mario.fall_speed = 0
            server.mario.yPos = block.yPos + 15 + 16
        elif check_collision(server.mario, block, 0, 1):
            server.mario.yPos = block.yPos - 15 - 16

    # mario and pipe
    for pipe in server.pipes:
        if check_collision(server.mario, pipe):
            server.mario.fall_speed = 0
            server.mario.yPos = pipe.yPos + 48 + 16
        elif check_collision(server.mario, pipe, 0, 1):
            server.mario.xPos = pipe.xPos - 28 - 13
        elif check_collision(server.mario, pipe, 0, 2):
            server.mario.xPos = pipe.xPos + 28 + 13

    # enemy and pipe
    for enemy in server.enemies:
        for pipe in server.pipes:
            if check_collision(enemy, pipe, 0, 1):
                enemy.dir *= -1
            elif check_collision(enemy, pipe, 0, 2):
                enemy.dir *= -1

    # mushroom and block
    for block in server.floorBlocks:
        for mushroom in server.items:
            if check_collision(mushroom, block):
                mushroom.fall_speed = 0
                mushroom.yPos = block.yPos + 15 + 16

    for block in server.itemBlocks:
        for mushroom in server.items:
            if check_collision(mushroom, block):
                mushroom.fall_speed = 0
                mushroom.yPos = block.yPos + 15 + 16

    for block in server.brickBlocks:
        for mushroom in server.items:
            if check_collision(mushroom, block):
                mushroom.fall_speed = 0
                mushroom.yPos = block.yPos + 15 + 16

    # mario and item
    for item in server.items:
        if check_collision(server.mario, item):
            if server.mario.trans < item.type:
                server.mario.trans = item.type
                server.mario.bebig_sound.play()
            server.items.remove(item)
            game_world.remove_object(item)

    # mario and castle
    if check_collision(server.mario, server.castle):
        server.mario.trans = -2  # 안보이게


def check_win():
    # mario and flag
    if check_collision(server.mario, server.flag):
        # server.gaming = False
        return True

