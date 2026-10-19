import datetime
import sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)


# ---------------------------------------------------------
# 1. 8-MONTH CHRONOLOGICAL BIBLE READING PLAN DATA (DAYS 1 - 231)
# ---------------------------------------------------------
READING_PLAN = {
    1: {"passage": "ዘፍጥረት 1-3", "eth_date": "ጥቅምት 1"},
    2: {"passage": "ዘፍጥረት 4-7", "eth_date": "ጥቅምት 2"},
    3: {"passage": "ዘፍጥረት 8-11", "eth_date": "ጥቅምት 3"},
    4: {"passage": "ኢዮብ 1-5", "eth_date": "ጥቅምት 4"},
    5: {"passage": "ኢዮብ 6-9", "eth_date": "ጥቅምት 5"},
    6: {"passage": "ኢዮብ 10-13", "eth_date": "ጥቅምት 6"},
    7: {"passage": "ኢዮብ 14-16", "eth_date": "ጥቅምት 7"},
    8: {"passage": "ኢዮብ 17-20", "eth_date": "ጥቅምት 8"},
    9: {"passage": "ኢዮብ 21-23", "eth_date": "ጥቅምት 9"},
    10: {"passage": "ኢዮብ 24-28", "eth_date": "ጥቅምት 10"},
    11: {"passage": "ኢዮብ 29-31", "eth_date": "ጥቅምት 11"},
    12: {"passage": "ኢዮብ 32-34", "eth_date": "ጥቅምት 12"},
    13: {"passage": "ኢዮብ 35-37", "eth_date": "ጥቅምት 13"},
    14: {"passage": "ኢዮብ 38-39", "eth_date": "ጥቅምት 14"},
    15: {"passage": "ኢዮብ 40-42", "eth_date": "ጥቅምት 15"},
    16: {"passage": "ዘፍጥረት 12-15", "eth_date": "ጥቅምት 16"},
    17: {"passage": "ዘፍጥረት 16-18", "eth_date": "ጥቅምት 17"},
    18: {"passage": "ዘፍጥረት 19-21", "eth_date": "ጥቅምት 18"},
    19: {"passage": "ዘፍጥረት 22-24", "eth_date": "ጥቅምት 19"},
    20: {"passage": "ዘፍጥረት 25-26", "eth_date": "ጥቅምት 20"},
    21: {"passage": "ዘፍጥረት 27-29", "eth_date": "ጥቅምት 21"},
    22: {"passage": "ዘፍጥረት 30-31", "eth_date": "ጥቅምት 22"},
    23: {"passage": "ዘፍጥረት 32-34", "eth_date": "ጥቅምት 23"},
    24: {"passage": "ዘፍጥረት 35-37", "eth_date": "ጥቅምት 24"},
    25: {"passage": "ዘፍጥረት 38-40", "eth_date": "ጥቅምት 25"},
    26: {"passage": "ዘፍጥረት 41-42", "eth_date": "ጥቅምት 26"},
    27: {"passage": "ዘፍጥረት 43-45", "eth_date": "ጥቅምት 27"},
    28: {"passage": "ዘፍጥረት 46-47", "eth_date": "ጥቅምት 28"},
    29: {"passage": "ዘፍጥረት 48-50", "eth_date": "ጥቅምት 29"},
    30: {"passage": "ዘፀአት 1-3", "eth_date": "ጥቅምት 30"},
    31: {"passage": "ዘፀአት 4-6", "eth_date": "ኅዳር 1"},
    32: {"passage": "ዘፀአት 7-9", "eth_date": "ኅዳር 2"},
    33: {"passage": "ዘፀአት 10-12", "eth_date": "ኅዳር 3"},
    34: {"passage": "ዘፀአት 13-15", "eth_date": "ኅዳር 4"},
    35: {"passage": "ዘፀአት 16-18", "eth_date": "ኅዳር 5"},
    36: {"passage": "ዘፀአት 19-21", "eth_date": "ኅዳር 6"},
    37: {"passage": "ዘፀአት 22-24", "eth_date": "ኅዳር 7"},
    38: {"passage": "ዘፀአት 25-27", "eth_date": "ኅዳር 8"},
    39: {"passage": "ዘፀአት 28-29", "eth_date": "ኅዳር 9"},
    40: {"passage": "ዘፀአት 30-32", "eth_date": "ኅዳር 10"},
    41: {"passage": "ዘፀአት 33-35", "eth_date": "ኅዳር 11"},
    42: {"passage": "ዘፀአት 36-38", "eth_date": "ኅዳር 12"},
    43: {"passage": "ዘፀአት 39-40", "eth_date": "ኅዳር 13"},
    44: {"passage": "ዘሌዋውያን 1-4", "eth_date": "ኅዳር 14"},
    45: {"passage": "ዘሌዋውያን 5-7", "eth_date": "ኅዳር 15"},
    46: {"passage": "ዘሌዋውያን 8-10", "eth_date": "ኅዳር 16"},
    47: {"passage": "ዘሌዋውያን 11-13", "eth_date": "ኅዳር 17"},
    48: {"passage": "ዘሌዋውያን 14-15", "eth_date": "ኅዳር 18"},
    49: {"passage": "ዘሌዋውያን 16-18", "eth_date": "ኅዳር 19"},
    50: {"passage": "ዘሌዋውያን 19-21", "eth_date": "ኅዳር 20"},
    51: {"passage": "ዘሌዋውያን 22-23", "eth_date": "ኅዳር 21"},
    52: {"passage": "ዘሌዋውያን 24-25", "eth_date": "ኅዳር 22"},
    53: {"passage": "ዘሌዋውያን 26-27", "eth_date": "ኅዳር 23"},
    54: {"passage": "ዘኍልቁ 1-2", "eth_date": "ኅዳር 24"},
    55: {"passage": "ዘኍልቁ 3-4", "eth_date": "ኅዳር 25"},
    56: {"passage": "ዘኍልቁ 5-6", "eth_date": "ኅዳር 26"},
    57: {"passage": "ዘኍልቁ 7", "eth_date": "ኅዳር 27"},
    58: {"passage": "ዘኍልቁ 8-10", "eth_date": "ኅዳር 28"},
    59: {"passage": "ዘኍልቁ 11-13", "eth_date": "ኅዳር 29"},
    60: {"passage": "ዘኍልቁ 14-15 & መዝሙረ ዳዊት 90", "eth_date": "ኅዳር 30"},
    61: {"passage": "ዘኍልቁ 16-17", "eth_date": "ታኅሣሥ 1"},
    62: {"passage": "ዘኍልቁ 18-20", "eth_date": "ታኅሣሥ 2"},
    63: {"passage": "ዘኍልቁ 21-22", "eth_date": "ታኅሣሥ 3"},
    64: {"passage": "ዘኍልቁ 23-25", "eth_date": "ታኅሣሥ 4"},
    65: {"passage": "ዘኍልቁ 26-27", "eth_date": "ታኅሣሥ 5"},
    66: {"passage": "ዘኍልቁ 28-30", "eth_date": "ታኅሣሥ 6"},
    67: {"passage": "ዘኍልቁ 31-32", "eth_date": "ታኅሣሥ 7"},
    68: {"passage": "ዘኍልቁ 33-34", "eth_date": "ታኅሣሥ 8"},
    69: {"passage": "ዘኍልቁ 35-36", "eth_date": "ታኅሣሥ 9"},
    70: {"passage": "ዘዳግም 1-2", "eth_date": "ታኅሣሥ 10"},
    71: {"passage": "ዘዳግም 3-4", "eth_date": "ታኅሣሥ 11"},
    72: {"passage": "ዘዳግም 5-7", "eth_date": "ታኅሣሥ 12"},
    73: {"passage": "ዘዳግም 8-10", "eth_date": "ታኅሣሥ 13"},
    74: {"passage": "ዘዳግም 11-13", "eth_date": "ታኅሣሥ 14"},
    75: {"passage": "ዘዳግም 14-16", "eth_date": "ታኅሣሥ 15"},
    76: {"passage": "ዘዳግም 17-20", "eth_date": "ታኅሣሥ 16"},
    77: {"passage": "ዘዳግም 21-23", "eth_date": "ታኅሣሥ 17"},
    78: {"passage": "ዘዳግም 24-27", "eth_date": "ታኅሣሥ 18"},
    79: {"passage": "ዘዳግም 28", "eth_date": "ታኅሣሥ 19"},
    80: {"passage": "ዘዳግም 29-31", "eth_date": "ታኅሣሥ 20"},
    81: {"passage": "ዘዳግም 32-34", "eth_date": "ታኅሣሥ 21"},
    82: {"passage": "ኢያሱ 1-4", "eth_date": "ታኅሣሥ 22"},
    83: {"passage": "ኢያሱ 5-8", "eth_date": "ታኅሣሥ 23"},
    84: {"passage": "ኢያሱ 9-11", "eth_date": "ታኅሣሥ 24"},
    85: {"passage": "ኢያሱ 12-15", "eth_date": "ታኅሣሥ 25"},
    86: {"passage": "ኢያሱ 16-18", "eth_date": "ታኅሣሥ 26"},
    87: {"passage": "ኢያሱ 19-21", "eth_date": "ታኅሣሥ 27"},
    88: {"passage": "ኢያሱ 22-24", "eth_date": "ታኅሣሥ 28"},
    89: {"passage": "መሳፍንት 1-2", "eth_date": "ታኅሣሥ 29"},
    90: {"passage": "መሳፍንት 3-5", "eth_date": "ታኅሣሥ 30"},
    91: {"passage": "መሳፍንት 6-7", "eth_date": "ጥር 1"},
    92: {"passage": "መሳፍንት 8-9", "eth_date": "ጥር 2"},
    93: {"passage": "መሳፍንት 10-12", "eth_date": "ጥር 3"},
    94: {"passage": "መሳፍንት 13-15", "eth_date": "ጥር 4"},
    95: {"passage": "መሳፍንት 16-18", "eth_date": "ጥር 5"},
    96: {"passage": "መሳፍንት 19-21", "eth_date": "ጥር 6"},
    97: {"passage": "ሩት 1-4", "eth_date": "ጥር 7"},
    98: {"passage": "1 ሳሙኤል 1-3", "eth_date": "ጥር 8"},
    99: {"passage": "1 ሳሙኤል 4-8", "eth_date": "ጥር 9"},
    100: {"passage": "1 ሳሙኤል 9-12", "eth_date": "ጥር 10"},
    101: {"passage": "1 ሳሙኤል 13-14", "eth_date": "ጥር 11"},
    102: {"passage": "1 ሳሙኤል 15-17", "eth_date": "ጥር 12"},
    103: {"passage": "1 ሳሙኤል 18-20 & መዝሙረ ዳዊት 11/59", "eth_date": "ጥር 13"},
    104: {"passage": "1 ሳሙኤል 21-24", "eth_date": "ጥር 14"},
    105: {"passage": "መዝሙረ ዳዊት 7/27/31/52/56", "eth_date": "ጥር 15"},
    106: {"passage": "1 ሳሙኤል 25-27", "eth_date": "ጥር 16"},
    107: {"passage": "መዝሙረ ዳዊት 34/54/63/142", "eth_date": "ጥር 17"},
    108: {"passage": "1 ሳሙኤል 28-31 & መዝሙረ ዳዊት 18", "eth_date": "ጥር 18"},
    109: {"passage": "2 ሳሙኤል 1-4", "eth_date": "ጥር 19"},
    110: {"passage": "መዝሙረ ዳዊት 6/9/10/14/16", "eth_date": "ጥር 20"},
    111: {"passage": "1 ዜና መዋዕል 1-2", "eth_date": "ጥር 21"},
    112: {"passage": "1 ዜና መዋዕል 3-5", "eth_date": "ጥር 22"},
    113: {"passage": "2 ሳሙኤል 5 & 1 ዜና መዋዕል 11-12", "eth_date": "ጥር 23"},
    114: {"passage": "መዝሙረ ዳዊት 133", "eth_date": "ጥር 24"},
    115: {"passage": "2 ሳሙኤል 6 & 1 ዜና መዋዕል 13-16", "eth_date": "ጥር 25"},
    116: {"passage": "መዝሙረ ዳዊት 15/24/68/105", "eth_date": "ጥር 26"},
    117: {"passage": "2 ሳሙኤል 7 & 1 ዜና መዋዕል 17", "eth_date": "ጥር 27"},
    118: {"passage": "መዝሙረ ዳዊት 2/22/45/110", "eth_date": "ጥር 28"},
    119: {"passage": "2 ሳሙኤል 8-9 & 1 ዜና መዋዕል 18", "eth_date": "ጥር 29"},
    120: {"passage": "መዝሙረ ዳዊት 60/108", "eth_date": "ጥር 30"},
    121: {"passage": "2 ሳሙኤል 10 & 1 ዜና መዋዕል 19 & መዝሙረ ዳዊት 20", "eth_date": "የካቲት 1"},
    122: {"passage": "መዝሙረ ዳዊት 21/53/70", "eth_date": "የካቲት 2"},
    123: {"passage": "2 ሳሙኤል 11-12 & 1 ዜና መዋዕል 20", "eth_date": "የካቲት 3"},
    124: {"passage": "መዝሙረ ዳዊት 32/51/103", "eth_date": "የካቲት 4"},
    125: {"passage": "2 ሳሙኤል 13-14", "eth_date": "የካቲት 5"},
    126: {"passage": "2 ሳሙኤል 15-17", "eth_date": "የካቲት 6"},
    127: {"passage": "መዝሙረ ዳዊት 3/4/42/55", "eth_date": "የካቲት 7"},
    128: {"passage": "2 ሳሙኤል 18-20", "eth_date": "የካቲት 8"},
    129: {"passage": "መዝሙረ ዳዊት 41/61/62", "eth_date": "የካቲት 9"},
    130: {"passage": "2 ሳሙኤል 21-23", "eth_date": "የካቲት 10"},
    131: {"passage": "መዝሙረ ዳዊት 57/95/97-99", "eth_date": "የካቲት 11"},
    132: {"passage": "2 ሳሙኤል 24 & 1 ዜና መዋዕል 21-22 & መዝሙረ ዳዊት 30", "eth_date": "የካቲት 12"},
    133: {"passage": "1 ዜና መዋዕል 23-26", "eth_date": "የካቲት 13"},
    134: {"passage": "መዝሙረ ዳዊት 131/138/139/143", "eth_date": "የካቲት 14"},
    135: {"passage": "1 ዜና መዋዕል 27-29", "eth_date": "የካቲት 15"},
    136: {"passage": "መዝሙረ ዳዊት 68/72/86", "eth_date": "የካቲት 16"},
    137: {"passage": "1 ነገሥት 1-2", "eth_date": "የካቲት 17"},
    138: {"passage": "መዝሙረ ዳዊት 37/71/94", "eth_date": "የካቲት 18"},
    139: {"passage": "1 ነገሥት 3-4 & 2 ዜና መዋዕል 1", "eth_date": "የካቲት 19"},
    140: {"passage": "ምሳሌ 1-4", "eth_date": "የካቲት 20"},
    141: {"passage": "ምሳሌ 5-9", "eth_date": "የካቲት 21"},
    142: {"passage": "ምሳሌ 10-15", "eth_date": "የካቲት 22"},
    143: {"passage": "ምሳሌ 16-22", "eth_date": "የካቲት 23"},
    144: {"passage": "ምሳሌ 23-24", "eth_date": "የካቲት 24"},
    145: {"passage": "1 ነገሥት 5-6 & 2 ዜና መዋዕል 2-3", "eth_date": "የካቲት 25"},
    146: {"passage": "1 ነገሥት 7 & 2 ዜና መዋዕል 4", "eth_date": "የካቲት 26"},
    147: {"passage": "1 ነገሥት 8 & 2 ዜና መዋዕል 5-7", "eth_date": "የካቲት 27"},
    148: {"passage": "መዝሙረ ዳዊት 47/97/100/135", "eth_date": "የካቲት 28"},
    149: {"passage": "1 ነገሥት 9 & 2 ዜና መዋዕል 8 & ምሳሌ 25-26", "eth_date": "የካቲት 29"},
    150: {"passage": "ምሳሌ 27-29", "eth_date": "የካቲት 30"},
    151: {"passage": "መክብብ 1-6", "eth_date": "መጋቢት 1"},
    152: {"passage": "መክብብ 7-12", "eth_date": "መጋቢት 2"},
    153: {"passage": "1 ነገሥት 10-11 & 2 ዜና መዋዕል 9 & ማኅልየ ማኅልይ 1-3", "eth_date": "መጋቢት 3"},
    154: {"passage": "ማኅልየ ማኅልይ 4-8", "eth_date": "መጋቢት 4"},
    155: {"passage": "1 ነገሥት 12-14 & 2 ዜና መዋዕል 10-12", "eth_date": "መጋቢት 5"},
    156: {"passage": "1 ነገሥት 15 & 2 ዜና መዋዕል 13-16", "eth_date": "መጋቢት 6"},
    157: {"passage": "1 ነገሥት 16 & 2 ዜና መዋዕል 17", "eth_date": "መጋቢት 7"},
    158: {"passage": "1 ነገሥት 17-19", "eth_date": "መጋቢት 8"},
    159: {"passage": "1 ነገሥት 20-21", "eth_date": "መጋቢት 9"},
    160: {"passage": "1 ነገሥት 22 & 2 ዜና መዋዕል 18-20", "eth_date": "መጋቢት 10"},
    161: {"passage": "2 ነገሥት 1-4", "eth_date": "መጋቢት 11"},
    162: {"passage": "አብድዩ 1 & 2 ነገሥት 5-8", "eth_date": "መጋቢት 12"},
    163: {"passage": "2 ዜና መዋዕል 21-24", "eth_date": "መጋቢት 13"},
    164: {"passage": "ኢዩኤል 1-3", "eth_date": "መጋቢት 14"},
    165: {"passage": "2 ነገሥት 9-11", "eth_date": "መጋቢት 15"},
    166: {"passage": "2 ነገሥት 12-13 & 2 ዜና መዋዕል 25", "eth_date": "መጋቢት 16"},
    167: {"passage": "ዮናስ 1-4", "eth_date": "መጋቢት 17"},
    168: {"passage": "2 ነገሥት 14 & 2 ዜና መዋዕል 26 & አሞጽ 1-5", "eth_date": "መጋቢት 18"},
    169: {"passage": "አሞጽ 6-9", "eth_date": "መጋቢት 19"},
    170: {"passage": "2 ነገሥት 15 & 2 ዜና መዋዕል 27 & ኢሳይያስ 1-4", "eth_date": "መጋቢት 20"},
    171: {"passage": "ኢሳይያስ 5-8", "eth_date": "መጋቢት 21"},
    172: {"passage": "ሚክያስ 1-4", "eth_date": "መጋቢት 22"},
    173: {"passage": "2 ነገሥት 16-17 & 2 ዜና መዋዕል 28", "eth_date": "መጋቢት 23"},
    174: {"passage": "ኢሳይያስ 1-5", "eth_date": "መጋቢት 24"},
    175: {"passage": "ኢሳይያስ 6-10", "eth_date": "መጋቢት 25"},
    176: {"passage": "ኢሳይያስ 11-14", "eth_date": "መጋቢት 26"},
    177: {"passage": "2 ነገሥት 18 & 2 ዜና መዋዕል 29-31 & መዝሙረ ዳዊት 48", "eth_date": "መጋቢት 27"},
    178: {"passage": "ኢሳይያስ 9-12", "eth_date": "መጋቢት 28"},
    179: {"passage": "ኢሳይያስ 13-17", "eth_date": "መጋቢት 29"},
    180: {"passage": "ኢሳይያስ 18-22", "eth_date": "መጋቢት 30"},
    181: {"passage": "ኢሳይያስ 23-27", "eth_date": "ሚያዝያ 1"},
    182: {"passage": "2 ነገሥት 19 & ኢሳይያስ 36-37 & መዝሙረ ዳዊት 76", "eth_date": "ሚያዝያ 2"},
    183: {"passage": "2 ነገሥት 20 & 2 ዜና መዋዕል 32 & ኢሳይያስ 38-39", "eth_date": "ሚያዝያ 3"},
    184: {"passage": "ኢሳይያስ 40-44", "eth_date": "ሚያዝያ 4"},
    185: {"passage": "ኢሳይያስ 45-48", "eth_date": "ሚያዝያ 5"},
    186: {"passage": "ኢሳይያስ 49-53", "eth_date": "ሚያዝያ 6"},
    187: {"passage": "ኢሳይያስ 54-58", "eth_date": "ሚያዝያ 7"},
    188: {"passage": "ኢሳይያስ 59-63", "eth_date": "ሚያዝያ 8"},
    189: {"passage": "ኢሳይያስ 64-66", "eth_date": "ሚያዝያ 9"},
    190: {"passage": "2 ነገሥት 21 & 2 ዜና መዋዕል 33", "eth_date": "ሚያዝያ 10"},
    191: {"passage": "ናሆም 1-3 & 2 ነገሥት 22-23", "eth_date": "ሚያዝያ 11"},
    192: {"passage": "2 ዜና መዋዕል 34-35 & ሶፎንያስ 1-3", "eth_date": "ሚያዝያ 12"},
    193: {"passage": "ዕንባቆም 1-3", "eth_date": "ሚያዝያ 13"},
    194: {"passage": "ኤርምያስ 1-4", "eth_date": "ሚያዝያ 14"},
    195: {"passage": "ኤርምያስ 5-8", "eth_date": "ሚያዝያ 15"},
    196: {"passage": "ኤርምያስ 9-12", "eth_date": "ሚያዝያ 16"},
    197: {"passage": "ኤርምያስ 13-16", "eth_date": "ሚያዝያ 17"},
    198: {"passage": "ኤርምያስ 17-20", "eth_date": "ሚያዝያ 18"},
    199: {"passage": "ኤርምያስ 21-24", "eth_date": "ሚያዝያ 19"},
    200: {"passage": "ኤርምያስ 25-28", "eth_date": "ሚያዝያ 20"},
    201: {"passage": "2 ነገሥት 24 & 2 ዜና መዋዕል 36 & ኤርምያስ 29-32", "eth_date": "ሚያዝያ 21"},
    202: {"passage": "ኤርምያስ 33-36", "eth_date": "ሚያዝያ 22"},
    203: {"passage": "ኤርምያስ 37-39 & 2 ነገሥት 25", "eth_date": "ሚያዝያ 23"},
    204: {"passage": "ኤርምያስ 40-44", "eth_date": "ሚያዝያ 24"},
    205: {"passage": "ሰቆቃው ኤርምያስ 1-5", "eth_date": "ሚያዝያ 25"},
    206: {"passage": "ኤርምያስ 45-48", "eth_date": "ሚያዝያ 26"},
    207: {"passage": "ኤርምያስ 49-52", "eth_date": "ሚያዝያ 27"},
    208: {"passage": "ሕዝቅኤል 1-4", "eth_date": "ሚያዝያ 28"},
    209: {"passage": "ሕዝቅኤል 5-8", "eth_date": "ሚያዝያ 29"},
    210: {"passage": "ሕዝቅኤል 9-12", "eth_date": "ሚያዝያ 30"},
    211: {"passage": "ሕዝቅኤል 13-16", "eth_date": "ግንቦት 1"},
    212: {"passage": "ሕዝቅኤል 17-20", "eth_date": "ግንቦት 2"},
    213: {"passage": "ሕዝቅኤል 21-24", "eth_date": "ግንቦት 3"},
    214: {"passage": "ሕዝቅኤል 25-28", "eth_date": "ግንቦት 4"},
    215: {"passage": "ሕዝቅኤል 29-32", "eth_date": "ግንቦት 5"},
    216: {"passage": "ሕዝቅኤል 33-36", "eth_date": "ግንቦት 6"},
    217: {"passage": "ሕዝቅኤል 37-40", "eth_date": "ግንቦት 7"},
    218: {"passage": "ሕዝቅኤል 41-44", "eth_date": "ግንቦት 8"},
    219: {"passage": "ሕዝቅኤል 45-48", "eth_date": "ግንቦት 9"},
    220: {"passage": "ዳንኤል 1-3", "eth_date": "ግንቦት 10"},
    221: {"passage": "ዳንኤል 4-6", "eth_date": "ግንቦት 11"},
    222: {"passage": "ዳንኤል 7-9", "eth_date": "ግንቦት 12"},
    223: {"passage": "ዳንኤል 10-12", "eth_date": "ግንቦት 13"},
    224: {"passage": "ዕዝራ 1-3 & መዝሙረ ዳዊት 85 / 126", "eth_date": "ግንቦት 14"},
    225: {"passage": "ዕዝራ 4-6 & ሐጌ 1-2 & ዘካርያስ 1-4", "eth_date": "ግንቦት 15"},
    226: {"passage": "ዘካርያስ 5-9", "eth_date": "ግንቦት 16"},
    227: {"passage": "ዘካርያስ 10-14 & አስቴር 1-5", "eth_date": "ግንቦት 17"},
    228: {"passage": "አስቴር 6-10 & ዕዝራ 7-10", "eth_date": "ግንቦት 18"},
    229: {"passage": "ነህምያ 1-5", "eth_date": "ግንቦት 19"},
    230: {"passage": "ነህምያ 6-9", "eth_date": "ግንቦት 20"},
    231: {"passage": "ነህምያ 10-13 & ሚልክያስ 1-4", "eth_date": "ግንቦት 21"}
}

# ---------------------------------------------------------
# 2. DATABASE SETUP (Defaulting new users to Day 9)
# ---------------------------------------------------------
def init_db():
    conn = sqlite3.connect("bible_study.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            chat_id INTEGER NOT NULL,
            current_day INTEGER DEFAULT 9,
            calendar_pref TEXT DEFAULT 'ethiopian'
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS completion_log (
            user_id INTEGER,
            day_number INTEGER,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, day_number)
        )
    """)
    conn.commit()
    conn.close()

# ---------------------------------------------------------
# 3. HANDLERS
# ---------------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    conn = sqlite3.connect("bible_study.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id, chat_id, current_day) VALUES (?, ?, 9)",
        (user_id, chat_id)
    )
    conn.commit()
    conn.close()

    keyboard = [
        [InlineKeyboardButton("🇪🇹 Ethiopian Calendar", callback_data="pref_ethiopian"),
         InlineKeyboardButton("🌍 Gregorian Calendar", callback_data="pref_gregorian")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"እንኳን ደህና መጡ, {update.effective_user.first_name}! 📖\n\n"
        "የቅዱስ መጽሐፍ የዘመን ቅደም ተከተል የንባብ ቦት ተጀምሯል። "
        "አሁን ከ **ቀን 9** ጀምሮ ተስተካክሏል።\n\n"
        "እባክዎ የሚፈልጉትን የቀን አቆጣጠር ይምረጡ:",
        reply_markup=reply_markup
    )

async def set_calendar_preference(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    pref = "ethiopian" if "ethiopian" in query.data else "gregorian"

    conn = sqlite3.connect("bible_study.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET calendar_pref = ? WHERE user_id = ?", (pref, user_id))
    conn.commit()
    conn.close()

    await query.edit_message_text(f"✅ የቀን አቆጣጠር ምርጫዎ ወደ {'የኢትዮጵያ' if pref == 'ethiopian' else 'ግሪጎሪያን'} ተስተካክሏል። /today በመጫን የዕለቱን ንባብ ማግኘት ይችላሉ።")

async def today_reading(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conn = sqlite3.connect("bible_study.db")
    cursor = conn.cursor()
    cursor.execute("SELECT current_day, calendar_pref FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        await update.message.reply_text("እባክዎ መጀመሪያ /start በመጫን ይመዝገቡ።")
        return

    current_day, pref = row
    plan_item = READING_PLAN.get(current_day)

    if plan_item:
        passage = plan_item["passage"]
        eth_date_str = plan_item["eth_date"]
        
        if pref == 'ethiopian':
            date_display = f"📅 ቀን {current_day} ({eth_date_str})"
        else:
            date_display = f"📅 ቀን {current_day} (Ethiopian: {eth_date_str})"

        keyboard = [[InlineKeyboardButton("✅ አንብቤአለሁ (Mark as Read)", callback_data=f"done_{current_day}")]]
        await update.message.reply_text(
            f"📖 *የዛሬው የንባብ ዕቅድ*\n\n{date_display}\n\nክፍል: *{passage}*",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text("🎉 እንኳን ደስ አሎት! የንባብ ዕቅዱን ሙሉ በሙሉ ጨርሰዋል።")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("pref_"):
        await set_calendar_preference(update, context)
        return

    if query.data.startswith("done_"):
        day_num = int(query.data.split("_")[1])
        user_id = query.from_user.id

        conn = sqlite3.connect("bible_study.db")
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO completion_log (user_id, day_number) VALUES (?, ?)", (user_id, day_num))
        cursor.execute("UPDATE users SET current_day = current_day + 1 WHERE user_id = ?", (user_id,))
        conn.commit()
        
        cursor.execute("SELECT current_day FROM users WHERE user_id = ?", (user_id,))
        next_day = cursor.fetchone()[0]
        conn.close()

        await query.edit_message_text(
            text=f"አሪፍ ስራ! ቀን {day_num}ን አጠናቀዋል። 🎉\nቀጣይ የንባብ ቀን: *ቀን {next_day}*.",
            parse_mode="Markdown"
        )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conn = sqlite3.connect("bible_study.db")
    cursor = conn.cursor()
    cursor.execute("SELECT current_day FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        current_day = row[0]
        total_days = len(READING_PLAN)
        completed = current_day - 1
        pct = round((completed / total_days) * 100, 1)
        
        await update.message.reply_text(
            f"📊 *የሂደት ሪፖርት (Progress Report)*\n\n"
            f"• አሁን ያለበት ቀን: ቀን {current_day} (ከ {total_days} ውስጥ)\n"
            f"• የተጠናቀቀ: {completed} ቀናት ({pct}%)\n",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text("እባክዎ መጀመሪያ /start በመጫን ይመዝገቡ።")

# ---------------------------------------------------------
# 4. MAIN ENTRY POINT
# ---------------------------------------------------------
def main():
    init_db()
    BOT_TOKEN = "8816106682:AAF9MGlCM9lvxSCnVDvkRdbN1bdTESBTrKo"

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("today", today_reading))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot is up and listening with Ethiopian schedule mapping...")
    app.run_polling()
from telegram.request import HTTPXRequest

# Increase connect and read timeouts to 30 seconds
custom_request = HTTPXRequest(connect_timeout=30.0, read_timeout=30.0)

app = Application.builder().token("8816106682:AAF9MGlCM9lvxSCnVDvkRdbN1bdTESBTrKo").request(custom_request).build()
if __name__ == "__main__":
    main()