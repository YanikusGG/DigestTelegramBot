from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

chosed = dict()


def button_creation(who):
    q1 = InlineKeyboardButton(text=f"{chosed[who][0]} bestmemes", callback_data='r1')
    q2 = InlineKeyboardButton(text=f"{chosed[who][1]} itmemlib", callback_data='r2')
    q3 = InlineKeyboardButton(text=f"{chosed[who][2]} thedankestmemes", callback_data='r3')
    q4 = InlineKeyboardButton(text=f"{chosed[who][3]} ithumor", callback_data='r4')
    q5 = InlineKeyboardButton(text=f"{chosed[who][4]} LaQeque", callback_data='r5')
    q6 = InlineKeyboardButton(text=f"{chosed[who][5]} howdyho_official", callback_data='r6')
    q7 = InlineKeyboardButton(text=f"{chosed[who][6]} sarcasm_orgasm", callback_data='r7')
    q8 = InlineKeyboardButton(text=f"{chosed[who][7]} prg_memes", callback_data='r8')
    menu = InlineKeyboardMarkup(row_width=1).insert(q1).insert(q2).insert(q3).insert(q4).insert(q5).insert(q6).insert(
        q7).insert(q8)
    return menu


def make_me(callback, who):
    if who in chosed and callback != '':

        if callback == "r1":
            if chosed[who][0] == '✅':
                chosed[who][0] = '—'
            else:
                chosed[who][0] = '✅'
        if callback == "r2":
            if chosed[who][1] == '✅':
                chosed[who][1] = '—'
            else:
                chosed[who][1] = '✅'
        if callback == "r3":
            if chosed[who][2] == '✅':
                chosed[who][2] = '—'
            else:
                chosed[who][2] = '✅'
        if callback == "r4":
            if chosed[who][3] == '✅':
                chosed[who][3] = '—'
            else:
                chosed[who][3] = '✅'
        if callback == "r5":
            if chosed[who][4] == '✅':
                chosed[who][4] = '—'
            else:
                chosed[who][4] = '✅'
        if callback == "r6":
            if chosed[who][5] == '✅':
                chosed[who][5] = '—'
            else:
                chosed[who][5] = '✅'
        if callback == "r7":
            if chosed[who][6] == '✅':
                chosed[who][6] = '—'
            else:
                chosed[who][6] = '✅'
        if callback == "r8":
            if chosed[who][7] == '✅':
                chosed[who][7] = '—'
            else:
                chosed[who][7] = '✅'

        menu = button_creation(who)

        # back = json.dumps(menu)+':'+'|'.join(array)
        back = menu
        return back

    else:
        chosed[who] = ['—', '—', '—', '—', '—', '—', '—', '—']
        menu = button_creation(who)
        return menu


def array_with_chanels(who):
    array = []
    if chosed[who][0] == '✅':
        array.append('bestmemes')
    if chosed[who][1] == '✅':
        array.append('itmemlib')
    if chosed[who][2] == '✅':
        array.append('thedankestmemes')
    if chosed[who][3] == '✅':
        array.append('ithumor')
    if chosed[who][4] == '✅':
        array.append('LaQeque')
    if chosed[who][5] == '✅':
        array.append('howdyho_official')
    if chosed[who][6] == '✅':
        array.append('sarcasm_orgasm')
    if chosed[who][7] == '✅':
        array.append('prg_memes')

    return array





