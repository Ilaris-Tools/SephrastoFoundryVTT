from EventBus import EventBus
from Wolke import Wolke
import Definitionen
import os
import json
from CharakterPrintUtility import CharakterPrintUtility
import random


def random_foundry_id():
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    return "".join(random.choices(chars, k=16))


def create_item(name, type):
    return {
        "_id": random_foundry_id(),
        "name": name,
        "type": type,
        "img": "icons/svg/item-bag.svg",
        "data": {},
        "effects": [],
        "folder": None,
        "sort": 0,
        "permission": {},
        "flags": {}
    }


def waffe_item(w):
    waffe = create_item(w["name"], "nahkampfwaffe") # TODO if/else nah/fern
    waffe["data"] = {
        "haerte": 5,
        "beschaedigung": 0,
        "dice_anzahl": 1,
        "dice_plus": 2,
        "fertigkeit": "Hiebwaffen",
        "talent": "Einhandhiebwaffen",
        "rw": 1,
        "hauptwaffe": False,
        "nebenwaffe": False,
        "eigenschaften": {
          "kopflastig": True,
          "niederwerfen": False,
          "parierwaffe": False,
          "reittier": False,
          "ruestungsbrechend": False,
          "schild": False,
          "schwer_4": False,
          "schwer_8": False,
          "stumpf": True,
          "unberechenbar": False,
          "unzerstoerbar": False,
          "wendig": False,
          "zerbrechlich": False,
          "zweihaendig": False,
          "kein_malus_nebenwaffe": False
        },
        "text": "",
        "aufbewahrungs_ort": "mitführend",
        "bewahrt_auf": [],
        "gewicht_summe": 0,
        "gewicht": 1,
        "preis": 0,
        "wm_at": -1,
        "wm_vt": -1,
        "mod_at": None,
        "mod_vt": None,
        "mod_schaden": ""
    }
#     return {
#         "_id": random_foundry_id(),
#         "name": w['name'],
#         "type": "angriff",
#         "data": {
#             "tp": self.tp,
#             "haerte": self.haerte,
#             "rw": self.rw,
#             "lz": self.lz,
#             "wm": self.wm,
#             "typ": self.typ,
#             "at": self.at,
#             "vt": self.vt,
#             "eigenschaften": [{
#                 "name": we.name,
#                 "text": we.text
#             } for we in self.eigenschaften.all()]
#         }
#     }




class Plugin:
    def __init__(self):
        EventBus.addAction("pdf_geschrieben", self.pdfGeschriebenHook)

    @staticmethod
    def getDescription():
        return "Dieses Plugin speichert die Charakterwerte beim PDF-Export zusätzlich als JSON-Datei ab. Wenn das Ilaris-System für FoundryVTT aktiv ist können Charaktere so direkt als Actors importiert werden."


    def pdfGeschriebenHook(self, params):
        char = Wolke.Char
        # actor = {}
        # actor['name'] = char.name

        items = []
        # for obj in char.waffen.all():
        #     items.append(obj.as_item())
        # for obj in char.cfertigkeiten.all():
        #     items.append(obj.as_item())
        #     for tal in obj.talente.all():
        #         items.append(tal.as_item())
        # TODO: übernat. fertigkeiten.. (export beispiel held magier)
        # for obj in instance.ctalente.all():
        #     items.append(obj.as_item())
        # for obj in instance.ctalente.all():
        #     items.append(obj.as_item())
        # for obj in char.freiefertigkeiten.all():
        #     items.append(obj.as_item())

        for v in CharakterPrintUtility.getVorteile(char):
            item = create_item(v, "vorteil")
            item["data"] = {
                "voraussetzung": "",  # TODO: vorteil.vorraussetzung
                "gruppe": 0,  # TODO: vorteil.gruppe
                "text": ""  # TODO: vorteil.text
            }
            items.append(item)
        for e in char.eigenheiten:
            if e:
                item = create_item(e, "eigenheit")
                items.append(item)
        for f in char.fertigkeiten:
            item = create_item(f.name, "fertigkeit")
            item["data"] = {       
                "basis": 0,
                "fw": f.wert,
                "pw": 0,
                "attribut_0": f.attribute[0],
                "attribut_1": f.attribute[1],
                "attribut_2": f.attribute[2],
                "gruppe": f.printclass,
                "text": f.text
            }
            items.append(item)
        # TODO: more items

        # direct keys
        attribute = { attr : {"wert": char.attribute[attr].wert, "pw": 0} for attr in Definitionen.Attribute}
        notes = char.kurzbeschreibung # + "\n\n" + char.notizen
        data = {
            "gesundheit": {
                "erschoepfung": 0,
                "wunden": 0,
                "wundabzuege": 0,
                "display": "Volle Gesundheit",
                "hp": {
                    "max": 9,
                    "value": 9,
                    "threshold": 0
                }
            },
            "attribute": attribute,
            "abgeleitete": {  # updated by foundry
                "globalermod": 0,
                "ws": 0,
                "ws_stern": 0,
                "be": 0,
                "be_traglast": 0,
                "ws_beine": 0,
                "ws_larm": 0,
                "ws_rarm": 0,
                "ws_bauch": 0,
                "ws_brust": 0,
                "ws_kopf": 0,
                "mr": 0,
                "gs": 0,
                "ini": 0,
                "dh": 0,
                "traglast_intervall": 0,
                "traglast": 0,
                # TODO: folgende werte werden nicht abgeleitet
                "gasp": None,
                "asp_stern": None,
                "asp_zugekauft": char.aspMod,  # TODO: sind aspMod == zugekauft??
                "gkap": None,
                "kap_stern": None,
                "kap_zugekauft": char.kapMod,
            },
            "schips": {
                "schips": char.schipsMax ,
                "schips_stern": char.schipsMax 
            },
            "initiative": 0,
            "furcht": {
                "furchtstufe": 0,
                "furchtabzuege": 0,
                "display": ""
            },
            "modifikatoren": {
                "manuellermod": 0,
                "nahkampfmod": 0
            },
            "geld": {
                "dukaten": 0,
                "silbertaler": 0,
                "heller": 0,
                "kreuzer": 0
            },
            "getragen": 0,
            "notes": notes,
            "misc": {
                "selected_kampfstil": "kvk"
            }
        },
        token = {
            "name": char.name,
            "img": "systems/Ilaris/assets/images/token/kreaturentypen/hummanoid.png",
            "displayName": 20,
            "actorLink": False,
            "width": 1,
            "height": 1,
            "scale": 1,
            "mirrorX": False,
            "mirrorY": False,
            "lockRotation": False,
            "rotation": 0,
            "alpha": 1,
            "vision": False,
            "dimSight": 0,
            "brightSight": 0,
            "sightAngle": 0,
            "light": {
                "alpha": 0.5,
                "angle": 0,
                "bright": 0,
                "coloration": 1,
                "dim": 0,
                "gradual": True,
                "luminosity": 0.5,
                "saturation": 0,
                "contrast": 0,
                "shadows": 0,
                "animation": {
                    "speed": 5,
                    "intensity": 5,
                    "reverse": False
                },
                "darkness": {
                    "min": 0,
                    "max": 1
                }
            },
            "disposition": 1,
            "displayBars": 50,
            "bar1": {
                "attribute": "gesundheit.hp"
            },
            "bar2": {
                "attribute": None
            },
            "flags": {},
            "randomImg": False
        }
        actor = {
            "_id": random_foundry_id(),
            "name": char.name,
            "type": "held",
            "img": "systems/Ilaris/assets/images/token/kreaturentypen/hummanoid.png",
            # TODO: include base encoded character image?
            "data": data,
            "token": token,
            "items": items,
            "effects": []
        }



        # content.append("Spezies: " + char.rasse)
        # content.append("Status: " + Definitionen.Statusse[char.status])
        # content.append("Heimat: " + char.heimat)





        # content.append("\n=== Allgemeine und Profane Vorteile === ")
        # vorteile = CharakterPrintUtility.getVorteile(char)
        # (vorteileAllgemein, vorteileKampf, vorteileUeber) = CharakterPrintUtility.groupVorteile(char, vorteile, link = True)
        # for v in vorteileAllgemein:
        #     content.append(v)

        # content.append("\n=== Profane Fertigkeiten === ")

        # fertigkeitsTypen = Wolke.DB.einstellungen["Fertigkeiten: Typen profan"].toTextList()
        # lastType = -1
        # for f in CharakterPrintUtility.getFertigkeiten(char):
        #     fert = char.fertigkeiten[f]
        #     if lastType != fert.printclass:
        #         content.append("\n" + fertigkeitsTypen[fert.printclass] + ":")
        #         lastType = fert.printclass

        #     talente = CharakterPrintUtility.getTalente(char, fert)
        #     talentStr = " "
        #     if len(talente) > 0:
        #         talentStr = " (" + ", ".join([t.anzeigeName for t in talente]) + ") "
        #     content.append(fert.name + talentStr + str(fert.probenwert) + "/" + str(fert.probenwertTalent))

        # content.append("\nFreie Fertigkeiten:")
        # for fert in CharakterPrintUtility.getFreieFertigkeiten(char):
        #     content.append(fert)


        # content.append("\nVorteile:")
        # for v in vorteileKampf:
        #     content.append(v)

        # content.append("\nRüstungen:")
        # for rüstung in char.rüstung:
        #     if not rüstung.name:
        #         continue
        #     content.append(rüstung.name + " RS " + str(int(rüstung.getRSGesamt())) + " BE " + str(rüstung.be))

        # content.append("\nWaffen:")
        # count = 0
        # for waffe in char.waffen:
        #     if not waffe.name:
        #         continue

        #     werte = char.waffenwerte[count]
        #     keinSchaden = waffe.W6 == 0 and waffe.plus == 0
        #     sg = ""
        #     if waffe.plus >= 0:
        #         sg = "+"
        #     content.append(waffe.anzeigename + " AT " + str(werte.AT) + " VT " + str(werte.VT) + " " + ("-" if keinSchaden else str(werte.TPW6) + "W6" + sg + str(werte.TPPlus)))
        #     if len(waffe.eigenschaften) > 0:
        #         content.append(", ".join(waffe.eigenschaften))
        #     content.append("")
        #     count += 1
        # content.pop()

        # content.append("\n=== Übernatürliche Fertigkeiten und Talente ===")

        # content.append("\nVorteile:")
        # for v in vorteileUeber:
        #     content.append(v)

        # content.append("\nÜbernatürliche Fertigkeiten:")
        # for f in CharakterPrintUtility.getÜberFertigkeiten(char):
        #     fert = char.übernatürlicheFertigkeiten[f]
        #     content.append(fert.name + " " + str(fert.probenwertTalent))

        # content.append("\nÜbernatürliche Talente:")
        # for talent in CharakterPrintUtility.getÜberTalente(char):
        #     content.append(talent.anzeigeName + " " + str(talent.pw))

        path = os.path.splitext(params["filename"])[0] + "_foundryvtt.json"
        with open(path, 'w', encoding="utf-8") as f:
            json.dump(actor, f, indent=2)

