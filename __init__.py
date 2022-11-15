from EventBus import EventBus
from Wolke import Wolke
import Definitionen
import Objekte
import os
import re
import json
from CharakterPrintUtility import CharakterPrintUtility
import random

__version__ = "3.2.2.a"

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
    # dropped infos:
    # wafNode.set('id',waff.name)
    #     wafNode.set('kampfstil',waff.kampfstil)
    #         wafNode.set('lz',str(waff.lz))
    # print(w)
    wdata = {
        "haerte": w.haerte,
        "beschaedigung": 0,
        "dice_anzahl": w.W6,
        "dice_plus": w.plus,
        "fertigkeit": w.fertigkeit,
        "talent": "",
        "rw": w.rw,
        "hauptwaffe": False,
        "nebenwaffe": False,
        # TODO: make this a list in Foundry and write getters/checks if bools are required! #14
        # 'eigenschaften': w.eigenschaften,  # TODO: list of strings?
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
        # TODO: is wm same for at/vt?
        "wm_at": w.wm,
        "wm_vt": w.wm,
        "mod_at": None,
        "mod_vt": None,
        "mod_schaden": ""
    }
    if type(w) is Objekte.Nahkampfwaffe:
        # w.anzeigename  -> is empty
        waffe = create_item(w.anzeigename, "nahkampfwaffe")
    else:
        waffe = create_item(w.anzeigename, "fernkampfwaffe")
        wdata['lz'] = w.lz  # TODO: this correct for FK?
    waffe['data'] = wdata
    return waffe


class Plugin:
    def __init__(self):
        # EventBus.addAction("pdf_geschrieben", self.pdfGeschriebenHook)
        EventBus.addFilter("charakter_xml_schreiben", self.json_schreiben)

    def speichernHook(self, val, params):
        print(params['charakter'])
        return val

    @staticmethod
    def getDescription():
        return "Dieses Plugin speichert die Charakterwerte beim PDF-Export \
            zusätzlich als JSON-Datei ab.Wenn das Ilaris-System für FoundryVTT \
            aktiv ist können Charaktere so direkt als Actors importiert werden."

    def get_token(self):
        token = {
            "name": self.char.name,
            "img": "systems/Ilaris/assets/images/token/kreaturentypen/humanoid.png",
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
        return token

    def get_items(self):
        """ The data models defined in the Foundry system are called items.
        They use templates and are collected in a huge list with unique random id's.
        This function creates such items for:
        - Vorteil
        - Fertigkeit
        - Eigenheit
        - Waffe
        - Talent
        """
        items = []
        # -- Vorteile -- #
        # for v in CharakterPrintUtility.getVorteile(self.char):
        for v in self.char.vorteile:
            vorteil = Wolke.DB.vorteile[v]
            # self.kosten = -1
            # self.variableKosten = False
            # self.kommentarErlauben = False
            # self.linkKategorie = VorteilLinkKategorie.NichtVerknüpfen
            # self.linkElement = ''
            # self.script = None
            # self.scriptPrio = 0
            # self.isUserAdded = True
            name = vorteil.name
            if v in self.char.vorteileVariable:
                name += f" ({self.char.vorteileVariable[v].kommentar})"
            if name == "Minderpakt":
                name += f" ({self.char.minderpakt})"
            item = create_item(name, "vorteil")
            item["data"] = {
                # "voraussetzung": ", ".join(vorteil.voraussetzungen),
                "voraussetzung": vorteil.voraussetzungen,
                "gruppe": vorteil.typ,  # TODO: vorteil.gruppe == vorteil.typ??
                "text": vorteil.text
            }
            # print(self.char.vorteileVariable)
            items.append(item)
        # # -- Eigenheiten -- #
        for e in self.char.eigenheiten:
            if e:
                item = create_item(e, "eigenheit")
                items.append(item)
        # # -- Fertigkeiten -- #
        for k, f in self.char.fertigkeiten.items():
            # ist das jetzt ein dict?
            item = create_item(f.name, "fertigkeit")
            item["data"] = {
                "basis": 0,
                "fw": f.wert,
                "pw": f.probenwert,
                "pwt": f.probenwertTalent,
                "attribut_0": f.attribute[0],
                "attribut_1": f.attribute[1],
                "attribut_2": f.attribute[2],
                "gruppe": f.printclass,
                "text": f.text
            }
            items.append(item)
        # -- Talente -- #
        for k, f in self.char.fertigkeiten.items():
            for talent in f.gekaufteTalente:
                item = create_item(talent, "talent")
                item["data"] = {
                    "fertigkeit": k,
                }
                items.append(item)
        # -- Freie Fertigkeiten -- #
        for ff in self.char.freieFertigkeiten:
            if not ff.name:
                continue
            item = create_item(ff.name, "freie_fertigkeit")
            item['data'] = {
                "stufe": ff.wert,
                "text": ff.name,
                "gruppe": "1"
            }
            items.append(item)
        # -- Übernatürliche Fertigkeiten -- #
            # for f in CharakterPrintUtility.getÜberFertigkeiten(char):
        #     fert = char.übernatürlicheFertigkeiten[f]
        #     content.append(fert.name + " " + str(fert.probenwertTalent))

        # content.append("\nÜbernatürliche Talente:")
        # for talent in CharakterPrintUtility.getÜberTalente(char):
        #     content.append(talent.anzeigeName + " " + str(talent.pw))
        for uef in self.char.übernatürlicheFertigkeiten.values():
            # print(uef)
            item = create_item(uef.name, "uebernatuerliche_fertigkeit")
            item["data"] = {
                "basis": uef.basiswert,
                "fw": uef.probenwert-uef.basiswert,
                "pw": uef.probenwertTalent,  # eigentlich pwt.. aber ist in fvtt einfach pw für übernat
                "attribut_0": uef.attribute[0],
                "attribut_1": uef.attribute[1],
                "attribut_2": uef.attribute[2],
                "gruppe": uef.printclass,
                "text": uef.text,
                "voraussetzung": uef.voraussetzungen,
            }
            items.append(item)
        # -- Zauber -- #
        talente = set()
        for k, f in self.char.übernatürlicheFertigkeiten.items():
            for t in f.gekaufteTalente:  # list of strings
                talente.add(t)
        for t in talente:
            talent = Wolke.DB.talente[t]
            item = create_item(t, "zauber")
            item["data"] = {
                "fertigkeit_ausgewaehlt": "auto",
                "fertigkeiten": ", ".join(talent.fertigkeiten),
                "text": talent.text,
                "gruppe": talent.printclass,  # TODO: ist das das selbe?
                "pw": -1  # TODO: warum hat talent/zauber ein pw?? sollte aus fertigkeit kommen
            }
            res = re.findall('Vorbereitungszeit:(.*?)(?:$|\n)',
                             talent.text, re.UNICODE)
            if len(res) == 1:
                item["data"]["vorbereitung"] = res[0].strip()
            res = re.findall('Reichweite:(.*?)(?:$|\n)',
                             talent.text, re.UNICODE)
            if len(res) == 1:
                item["data"]["reichweite"] = res[0].strip()
            res = re.findall('Wirkungsdauer:(.*?)(?:$|\n)',
                             talent.text, re.UNICODE)
            if len(res) == 1:
                item["data"]["wirkungsdauer"] = res[0].strip()
            res = re.findall('Kosten:(.*?)(?:$|\n)', talent.text, re.UNICODE)
            if len(res) == 1:
                item["data"]["kosten"] = res[0].strip()
            items.append(item)

        # # -- Waffen -- #
        for w in self.char.waffen:
            if not w.anzeigename:
                continue
            item = waffe_item(w)
            items.append(item)
        # -- Rüstung -- #
        for r in self.char.rüstung:
            if not r.name:
                continue
            item = create_item(r.name, "ruestung")
            item["data"] = {
                "rs": r.getRSGesamtInt(),
                "be": r.be,
                "rs_beine": r.rs[0],
                "rs_larm": r.rs[1],
                "rs_rarm": r.rs[2],
                "rs_bauch": r.rs[3],
                "rs_brust": r.rs[4],
                "rs_kopf": r.rs[5],
                "aktiv": False,
                "text": r.text
            }
            items.append(item)
        # -- Inventar -- #
        for a in self.char.ausrüstung:
            if not a:
                continue
            item = create_item(a, "gegenstand")
            item["data"] = {}
            items.append(item)
        return items

    def get_abgeleitet(self):
        return {  # updated by foundry
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
            # "gasp": None,
            # "asp_stern": None,
            # "asp_zugekauft": self.char.aspMod,  # TODO: sind aspMod == zugekauft??
            # "gkap": None,
            # "kap_stern": None,
            # "kap_zugekauft": self.char.kapMod,
        }

    def json_schreiben(self, val, params):
        """Funktion wird als Filter in charakter_xml_schreiben (speichern)
        angewendet. `val` wird unverändert zurückgegeben wärend aus params['charakter']
        die json file für foundry generiert und gespeichert wird.
        """
        # self.char = Wolke.Char
        self.char = params['charakter']
        self.actor = {}

        # direct keys
        attribute = {attr: {
            "wert": self.char.attribute[attr].wert, "pw": 0} for attr in Definitionen.Attribute}
        notes = self.char.kurzbeschreibung + "\n\n" + self.char.notiz
        data = {
            "gesundheit": {
                "erschoepfung": 0,
                "wunden": 0,
                "wundabzuege": 0,
                "wundenignorieren": 0,
                "display": "Volle Gesundheit",
                "hp": {
                    "max": 9,
                    "value": 9,
                    "threshold": 0
                }
            },
            "attribute": attribute,
            "abgeleitete": self.get_abgeleitet(),
            "schips": {
                "schips": self.char.schipsMax,
                "schips_stern": self.char.schipsMax
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
        }
        actor = {
            # TODO: include base encoded character image?
            # "_id": random_foundry_id(),
            "name": self.char.name,
            "type": "held",
            "img": "systems/Ilaris/assets/images/token/kreaturentypen/humanoid.png",
            "data": data,
            "token": self.get_token(),
            "items": self.get_items(),
            "effects": []
        }
        # Dropped Infos
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

        # content.append("\nÜbernatürliche Fertigkeiten:")
        # for f in CharakterPrintUtility.getÜberFertigkeiten(char):
        #     fert = char.übernatürlicheFertigkeiten[f]
        #     content.append(fert.name + " " + str(fert.probenwertTalent))

        # content.append("\nÜbernatürliche Talente:")
        # for talent in CharakterPrintUtility.getÜberTalente(char):
        #     content.append(talent.anzeigeName + " " + str(talent.pw))

        path = os.path.splitext(params["filepath"])[0] + "_foundryvtt.json"
        with open(path, 'w', encoding="utf-8") as f:
            json.dump(actor, f, indent=2)
        return val
