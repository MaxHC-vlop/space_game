import time
import curses
import asyncio
import random


TIC_TIMEOUT = 0.1


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


async def blink(canvas, row, column, symbol):
    difference_blink = random.randint(1, 10)
    for tic in range(difference_blink):
        await asyncio.sleep(0)

    while True:
        canvas.refresh()
        for tic in range(20):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        canvas.refresh()
        for tic in range(3):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        canvas.refresh()
        for tic in range(5):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        canvas.refresh()
        for tic in range(3):
            await asyncio.sleep(0)


def draw(canvas, star='*'):
    canvas.border()
    height, width = canvas.getmaxyx()
    coroutines = [
        blink(canvas, row, column, symbol)
        for row, column, symbol in stars_generator(height, width)
    ]
    shot = fire(canvas, 2, width / 2)
    coroutines.append(shot)
    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
            if len(coroutines) == 0:
                break

        time.sleep(TIC_TIMEOUT)


def stars_generator(height, width):
    count_stars = random.randint(20, 60)
    for number_star in range(count_stars):
        row = random.randint(1, height - 2)
        column = random.randint(1, width - 2)
        symbol = random.choice(['+', '*', '.', ':'])
        star = (row, column, symbol)
        yield star


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
    curses.curs_set(False)
