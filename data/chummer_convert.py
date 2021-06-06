# pyChummer Data Converter
# Convert Chummer XML Data and German Translation File to YAML format for pyChummer

import untangle
import yaml
import pprint
import re
from distutils.util import strtobool


# A Dumper to ignore aliasing so that copied data becomes "unpacked" on write.
class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


# What to generate:
GENERATE = ['metatypes']

LANGDATAXML = 'clang/de-munifix_data.xml'

print('CHUMMER XML DATA CONVERSION')
print()
print(f"Load Main Translation File: '{LANGDATAXML}'")
transd = untangle.parse(LANGDATAXML)


def GetTranslationBlock(file):
    """Gets the respective XML sublock out of the translation corresponing to the given XML file."""

    for block in transd.chummer.chummer:
        if block['file'] == file:
            print(f"Load translation data for file {file}")
            return block

    print(f'ERROR: No translation for {file} found.')


# Empty categories dictionary for category data.
categories = dict()


# ----------------------------------------------------------------------
# METATYPES
if 'metatypes' in GENERATE:
    print()
    print('METATYPES')

    DATAFILE = 'cdata/metatypes.xml'
    print(f"Load Data from '{DATAFILE}'")
    unt = untangle.parse(DATAFILE)
    xmld = unt.chummer

    trans = GetTranslationBlock(DATAFILE.split('/')[-1])

    # Categories
    categories['metatypes'] = dict()
    for ch in xmld.categories.category:
        # Find Translation:
        for elem in trans.categories.category:
            if elem.cdata == ch.cdata:
                translation = elem['translate']
                categories['metatypes'][elem.cdata] = translation
                break

    # TODO Special Characters (AI and Free Spirit) are not yet supported
    categories['metatypes'].pop('Special', None)
    # We flatten Metavariants, so we need a separate category.
    categories['metatypes']['Metavariant'] = 'Metavarianten'

    # Metatypes
    metatypes = dict()
    for dp in xmld.metatypes.metatype:
        # TODO Special Characters (AI and Free Spirit) are not yet supported
        # TODO Shapeshifters are not yet supported
        if dp.category.cdata == 'Special':
            continue

        metatypes[dp.name.cdata] = dict()
        # Find translation element
        for elem in trans.metatypes.metatype:
            if dp.name.cdata == elem.name.cdata:
                tp = elem
                break
        if dp.category.cdata == 'Shapeshifter':
            # Change Stupid Names
            metatypes[dp.name.cdata]['text'] = f"{tp.translate.cdata.split('-')[0]} ({tp.translate.cdata.split('-')[1]})"
        else:
            metatypes[dp.name.cdata]['text'] = tp.translate.cdata
        metatypes[dp.name.cdata]['basetype'] = dp.name.cdata
        metatypes[dp.name.cdata]['category'] = dp.category.cdata
        metatypes[dp.name.cdata]['bp'] = int(dp.bp.cdata)
        metatypes[dp.name.cdata]['source'] = dp.source.cdata
        metatypes[dp.name.cdata]['source_page'] = tp.page.cdata

        # Racial Attribute Modifiers
        # Guessed from metatype min and max if they are not 1 / 6
        attribtbl = {
            'KON': {'min': dp.bodmin.cdata, 'max': dp.bodmax.cdata},
            'GES': {'min': dp.agimin.cdata, 'max': dp.agimax.cdata},
            'REA': {'min': dp.reamin.cdata, 'max': dp.reamax.cdata},
            'STR': {'min': dp.strmin.cdata, 'max': dp.strmax.cdata},
            'CHA': {'min': dp.chamin.cdata, 'max': dp.chamax.cdata},
            'INT': {'min': dp.intmin.cdata, 'max': dp.intmax.cdata},
            'LOG': {'min': dp.logmin.cdata, 'max': dp.logmax.cdata},
            'WIL': {'min': dp.wilmin.cdata, 'max': dp.wilmax.cdata},
            'EDG': {'min': dp.edgmin.cdata, 'max': dp.edgmax.cdata},
        }
        metatypes[dp.name.cdata]['attribute_racials'] = dict()
        for attrib in attribtbl:
            vrac = 0
            if int(attribtbl[attrib]['min']) > 1:
                vrac = int(attribtbl[attrib]['min']) - 1
            elif int(attribtbl[attrib]['max']) != 6:
                vrac = int(attribtbl[attrib]['max']) - 6
            metatypes[dp.name.cdata]['attribute_racials'][attrib] = vrac

        # Movement needs to be parsed
        metatypes[dp.name.cdata]['movement'] = {'fly': None, 'swim': None}
        match = re.search(r'(\d+)/(\d+), (\w+) (\S+)', dp.movement.cdata)
        if match:  # has swim or Fly
            metatypes[dp.name.cdata]['movement']['walk'] = int(match.group(1))
            metatypes[dp.name.cdata]['movement']['run'] = int(match.group(2))
            if match.group(4).find('/') == -1:  # only one value for alternative movements
                metatypes[dp.name.cdata]['movement'][match.group(3).lower()] = int(match.group(4))
            else:  # Walk and run for alternative Movement
                metatypes[dp.name.cdata]['movement'][match.group(3).lower()] = match.group(4)
        match = re.search(r'(\d+)/(\d+)', dp.movement.cdata)
        if match:  # does not swim or Fly
            metatypes[dp.name.cdata]['movement']['walk'] = int(match.group(1))
            metatypes[dp.name.cdata]['movement']['run'] = int(match.group(2))

        # Qualities
        metatypes[dp.name.cdata]['qualities'] = dict()
        if hasattr(dp, 'qualities'):
            if hasattr(dp.qualities, 'positive'):
                for pq in dp.qualities.positive.quality:
                    metatypes[dp.name.cdata]['qualities'][pq.cdata] = {
                        'removable': bool(strtobool(pq._attributes.get('removable', 'false'))),
                        'select': pq._attributes.get('select', None),
                        'innate': True,
                        'category': 'positive'
                    }
            if hasattr(dp.qualities, 'negative'):
                for pq in dp.qualities.negative.quality:
                    metatypes[dp.name.cdata]['qualities'][pq.cdata] = {
                        'removable': bool(strtobool(pq._attributes.get('removable', 'false'))),
                        'select': pq._attributes.get('select', None),
                        'innate': True,
                        'category': 'negative'
                    }

        # Powers
        if hasattr(dp, 'powers'):
            metatypes[dp.name.cdata]['powers'] = dict()
            for pw in dp.powers.power:
                metatypes[dp.name.cdata]['powers'][pw.cdata] = {
                    'select': pw._attributes.get('select', None),
                    'innate': True,
                }
        else:
            metatypes[dp.name.cdata]['powers'] = None

        # Bonus -> Improvements
        metatypes[dp.name.cdata]['improvements'] = dict()
        if hasattr(dp, 'bonus'):
            for bn in dp.bonus.children:
                if bn._name == 'addattribute':
                    if dp.bonus.addattribute.name.cdata == 'MAG':
                        metatypes[dp.name.cdata]['improvements']['metatype.magic'] = {
                            'type': 'special',
                            'innate': True,
                            'text': 'Metatyp',
                            'effect': 'enable_magic'
                        }
                    elif dp.bonus.addattribute.name.cdata == 'RES':
                        metatypes[dp.name.cdata]['improvements']['metatype.resonance'] = {
                            'type': 'special',
                            'innate': True,
                            'text': 'Metatyp',
                            'effect': 'enable_resonance'
                        }
                    else:
                        raise ValueError(f'addattribute has unsupported attribute value {dp.bonus.addattribute.name.cdata}.')
                elif bn._name == 'enabletab':
                    if dp.bonus.enabletab.name.cdata == 'critter':
                        metatypes[dp.name.cdata]['improvements']['metatype.critter'] = {
                            'type': 'special',
                            'innate': True,
                            'text': 'Metatyp',
                            'effect': 'crittertab'
                        }
                    else:
                        raise ValueError(f'enabletab has unsupported attribute value {dp.bonus.enabletab.name.cdata}.')
                elif bn._name == 'reach':
                    metatypes[dp.name.cdata]['improvements']['metatype.reach'] = {
                        'type': 'derived',
                        'innate': True,
                        'text': 'Metatyp',
                        'property': 'reach',
                        'value': int(dp.bonus.reach.cdata)
                    }
                elif bn._name == 'armor':
                    metatypes[dp.name.cdata]['improvements']['metatype.armor.ballistic'] = {
                        'type': 'derived',
                        'innate': True,
                        'text': 'Metatyp',
                        'property': 'armor_ballistic',
                        'value': int(dp.bonus.armor.b.cdata)
                    }
                    metatypes[dp.name.cdata]['improvements']['metatype.armor.impact'] = {
                        'type': 'derived',
                        'innate': True,
                        'text': 'Metatyp',
                        'property': 'armor_impact',
                        'value': int(dp.bonus.armor.i.cdata)
                    }
                elif bn._name == 'lifestylecost':
                    metatypes[dp.name.cdata]['improvements']['metatype.lifestylecost'] = {
                        'type': 'lifestyle',
                        'innate': True,
                        'text': 'Metatyp',
                        'property': 'cost_increase',
                        'value': int(dp.bonus.lifestylecost.cdata)
                    }
                else:
                    print(f'WARNING: Unknown Bonus "{bn._name}"')

        # Metavariants
        # Ignored for Shapeshifters, because stupid.
        if hasattr(dp, 'metavariants') and dp.category.cdata != 'Shapeshifter':
            for mv in dp.metavariants.metavariant:
                # We flatten the Chummer Data here.
                # Copy base variant:
                metatypes[mv.name.cdata] = {}
                for key, val in metatypes[dp.name.cdata].items():
                    if key in ['attribute_racials', 'basetype', 'movement', 'improvements', 'powers']:
                        metatypes[mv.name.cdata][key] = metatypes[dp.name.cdata][key]
                # Find translation element
                for elem in tp.metavariants.metavariant:
                    if mv.name.cdata == elem.name.cdata:
                        tpp = elem
                        break
                # Get Specific Scalar Data
                metatypes[mv.name.cdata]['text'] = tpp.translate.cdata
                metatypes[mv.name.cdata]['category'] = 'Metavariant'
                metatypes[mv.name.cdata]['bp'] = mv.bp.cdata
                metatypes[mv.name.cdata]['source'] = mv.source.cdata
                metatypes[mv.name.cdata]['source_page'] = tpp.page.cdata

                # Qualities are NOT copied, but have a distinct set
                metatypes[mv.name.cdata]['qualities'] = dict()
                if hasattr(mv, 'qualities'):
                    if hasattr(mv.qualities, 'positive'):
                        for pq in mv.qualities.positive.quality:
                            metatypes[mv.name.cdata]['qualities'][pq.cdata] = {
                                'removable': bool(strtobool(pq._attributes.get('removable', 'false'))),
                                'select': pq._attributes.get('select', None),
                                'category': 'positive'
                            }
                    if hasattr(mv.qualities, 'negative'):
                        for pq in mv.qualities.negative.quality:
                            metatypes[mv.name.cdata]['qualities'][pq.cdata] = {
                                'removable': bool(strtobool(pq._attributes.get('removable', 'false'))),
                                'select': pq._attributes.get('select', None),
                                'category': 'negative'
                            }

    # Write Metatypes File
    pprint.pprint(metatypes.keys())
    OUTFILE = 'metatypes.yaml'
    with open(OUTFILE, mode='w') as fp:
        yaml.dump(metatypes, fp, Dumper=NoAliasDumper)
    print(f"Wrote Data to '{OUTFILE}'")


print()
print('Category Dictionary:')
pprint.pprint(categories)

