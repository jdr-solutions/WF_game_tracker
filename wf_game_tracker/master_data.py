# master_data.py

import copy

###############################################################################
# 1) Master Factions/Warlords Table (Blank)
#
#   This is the "template" for creating new decks. Each new deck is a copy of
#   this data, so that all factions/warlords are present with zeroed stats.
###############################################################################
MASTER_TABLE = [
    {
        "faction_name": "Ultramarines",
        "warlords": [
            {"warlord_name": "Marneus Calgar",    "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0},
            {"warlord_name": "Chaplain Letharius","off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0},
            {"warlord_name": "Lieutenant Titus",  "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0},
            {"warlord_name": "Varro Tigurius",    "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0},
            {"warlord_name": "Uriel Ventris",     "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0}
        ]
    },
    {
        "faction_name": "Orks (Goff Klan)",
        "warlords": [
            {"warlord_name": "Ghazghkull Thraka", "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0},
            {"warlord_name": "Warboss Gordrang",  "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0},
            {"warlord_name": "Boss Zaastruk",     "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0},
            {"warlord_name": "Grukk Face-Rippa",  "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0}
        ]
    },
    {
        "faction_name": "Eldar (Saim-Hann)",
        "warlords": [
            {"warlord_name": "Jain Zar",          "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0},
            {"warlord_name": "Anvirr Keltoc",     "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0},
            {"warlord_name": "Medreyal Ghaeyln",  "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0},
            {"warlord_name": "Eliac Zephyrblade", "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0}
        ]
    },
    {
        "faction_name": "Necron (Sautekh Dynasty)",
        "warlords": [
            {"warlord_name": "Imotekh the Stormlord", "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0},
            {"warlord_name": "Orikan the Diviner",    "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0},
            {"warlord_name": "Nemesor Zahndrekh",     "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0},
            {"warlord_name": "Ramatekh the Cruel",    "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0}
        ]
    },
    {
        "faction_name": "Tyranids (Hive Fleet Leviathan)",
        "warlords": [
            {"warlord_name": "Swarmlord",          "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0},
            {"warlord_name": "Terror of Vardenhast","off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0},
            {"warlord_name": "Neurothrope",        "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0},
            {"warlord_name": "Tervigon",           "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0}
        ]
    },
    {
        "faction_name": "Chaos (Black Legion)",
        "warlords": [
            {"warlord_name": "Abaddon the Despoiler","off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0},
            {"warlord_name": "Ghallaron",            "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0},
            {"warlord_name": "Svlar Hexscorn",       "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0},
            {"warlord_name": "Haarken Worldclaimer", "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0}
        ]
    },
    {
        "faction_name": "Tau Empire",
        "warlords": [
            {"warlord_name": "Commander O' Maiss", "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0},
            {"warlord_name": "Aun'va",             "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0},
            {"warlord_name": "War Shaper",         "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0},
            {"warlord_name": "Shadowsun",          "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0}
        ]
    },
    {
        "faction_name": "Sisters of Battle (Adepta Sororitas)",
        "warlords": [
            {"warlord_name": "Morvenn Vahl",              "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0},
            {"warlord_name": "Celestian Sacresant Aveline","off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0},
            {"warlord_name": "Junith Eruita",             "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0},
            {"warlord_name": "Erika Luminas",             "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0}
        ]
    },
    {
        "faction_name": "Genestealer Cults",
        "warlords": [
            {"warlord_name": "Primus Saffa Rhiannor", "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0},
            {"warlord_name": "Magus Uthrel Naas",     "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0},
            {"warlord_name": "Iconward Malak Vorenth","off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0},
            {"warlord_name": "Lhaska Szenari",        "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0}
        ]
    },
    {
        "faction_name": "Astra Militarum",
        "warlords": [
            {"warlord_name": "Lord Solar Leontus", "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0},
            {"warlord_name": "Ursula Creed",       "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0},
            {"warlord_name": "Commissar Denkler",  "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0}
        ]
    },
    {
        "faction_name": "Dark Angels",
        "warlords": [
            {"warlord_name": "Azrael", "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0},
            {"warlord_name": "Belial", "off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0},
            {"warlord_name": "Asmodai","off_wins": 0, "off_losses": 0, "def_wins": 0, "def_losses": 0}
        ]
    }
]


def deep_copy_master_table():
    """
    Return a fresh deep copy of MASTER_TABLE 
    so that each new deck starts with 0 in all stats.
    """
    return copy.deepcopy(MASTER_TABLE)
