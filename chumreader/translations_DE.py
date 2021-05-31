# Translations of Chummer XML terms to German
# Author: Boris Wezisla

import logging

# Tranlation Files:
translation_dictionary = {
    'metatype': {
        'Human': 'Mensch',
        'Nartaki': 'Nartaki',
        'Ork': 'Ork',
        'Hobgoblin': 'Hobgoblin',
        'Ogre': 'Oger',
        'Satyr': 'Satyr',
        'Dwarf': 'Zwerg',
        'Gnome': 'Gnom',
        'Haruman': 'Haruman',
        'Koborokuru': 'Koborokuru',
        'Menehune': 'Menehune',
        'Elf': 'Elf',
        'Dryad': 'Dryade',
        'Night One': 'Nächtlicher',
        'Wakyambi': 'Wakyambi',
        'Xapiri Thëpë': 'Xapiri Thëpë',
        'Troll': 'Troll',
        'Cyclops': 'Zyklop',
        'Fomori': 'Fomori',
        'Giant': 'Riese',
        'Minotaur': 'Minotaurus',
        'Centaur': 'Zentaur',
        'Naga': 'Naga',
        'Pixie': 'Pixie',
        'Sasquatch': 'Sasquatch',
        'Shapeshifter': 'Gestaltwandler',
        'Fox': 'Fuchs',
        'Wolf': 'Wolf',
        'Eagle': 'Adler',
        'Leopard': 'Leopard',
        'Jaguar': 'Jaguar',
        'Seal': 'Seehund',
        'Tiger': 'Tiger',
        'Lion': 'Löwe',
        'Bear': 'Bär',
        'Free Spirit': 'Freier Geist',
        'A.I.': 'KI',
    },
}


def chum_translate(category, term):
    """Translate a term from a categroy to German."""

    # Logging
    logger = logging.getLogger('chumreader.chum_translate')
    logger.debug(f'Requested Translation: <{term}> from dictionary <{category}>')

    try:
        translation = translation_dictionary[category][term]
    except KeyError:
        logger.error(f'Dictionary <{category}> and/or term <{term}> do not exist!')
        raise

    return translation
