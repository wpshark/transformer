from transformer.registry import register
from transformer.transforms.base import BaseTransform

import hashlib
import re

def superheroize(name):
    a = ['Admiral', 'Air', 'Alpha', 'Ambush', 'Android', 'Aqua', 'Arch', 'Armadillo', 'Astro', 'Atomic', 'Azure', 'Battle', 'Bee', 'Beta', 'Bionic', 'Blue', 'Brain', 'Bronze', 'Brother', 'Caped', 'Captain', 'Captain', 'Chameleon', 'Cobalt', 'Colossal', 'Comet', 'Commander', 'Commodore', 'Composite', 'Compu', 'Copper', 'Cosmic', 'Crimson', 'Cyber', 'Danger', 'Dare', 'Dark', 'Dawn', 'Death', 'Delta', 'Detective', 'Digi', 'Doc', 'Doctor', 'Dragon', 'Dream', 'Duke', 'Dynamo', 'Earth', 'Elasti', 'Electra', 'Element', 'Emerald', 'Fighting', 'Fire', 'Flaming', 'Fly', 'Flying', 'Forgotten', 'Freedom', 'Frog', 'Future', 'Gamma', 'General', 'Ghost', 'Giant', 'Gold', 'Golden', 'Green', 'Grey', 'Hawk', 'Hour', 'Human', 'Hyper', 'Ice', 'Insect', 'Invisible', 'Iron', 'Jade', 'Jet', 'Karate', 'Laser', 'Lieutenant', 'Light', 'Lightning', 'Lion', 'Living', 'Machine', 'Mad', 'Magna', 'Magnetic', 'Major', 'Mammoth', 'Manga', 'Martian', 'Masked', 'Mega', 'Metal', 'Meteor', 'Micro', 'Mighty', 'Millennium', 'Mind', 'Miracle', 'Moon', 'Night', 'Nuclear', 'Obsidian', 'Omega', 'Onyx', 'Orange', 'Phantom', 'Platinum', 'Platypus', 'Power', 'Psychic', 'Purple', 'Q', 'Quick', 'Quin', 'Racoon', 'Radioactive', 'Rainbow', 'Red', 'Ring', 'Robo', 'Robot', 'Rocket', 'Ruby', 'Samurai', 'Sand', 'Sarge', 'Scarab', 'Scarlet', 'Sea', 'Seagoing', 'Secret', 'Sergeant', 'Shadow', 'Shatter', 'Shining', 'Shrinking', 'Silent', 'Silver', 'Sky', 'Snow', 'Space', 'Speed', 'Spider', 'Squirrel', 'Star', 'Steel', 'Stone', 'Sub', 'Suicide', 'Sun', 'Super', 'Super', 'Supreme', 'Techni', 'Terra', 'Thunder', 'Tiger', 'Time', 'Tomorrow', 'Turbo', 'Ultra', 'Valiant', 'Vector', 'War', 'Warrior', 'Water', 'White', 'Wild', 'Wind', 'Wing', 'Winged', 'Winter', 'Wolf', 'Wombat', 'Wonder', 'X', 'Y', 'Yellow', 'Z']
    b = ['A', 'Aardvark', 'America', 'Android', 'Apostle', 'Armadillo', 'Arrow', 'Atom', 'Avenger', 'Bat', 'Bee', 'Beetle', 'Bird', 'Blade', 'Blaze', 'Blur', 'Bolt', 'Brain', 'Bullet', 'Bulk', 'Canary', 'Carrot', 'Cavalier', 'Centurion', 'Chameleon', 'Champion', 'Claw', 'Comet', 'Condor', 'Corona', 'Crystal', 'Crusader', 'Cyborg', 'Dazzler', 'Defender', 'Detective', 'Dragon', 'Droid', 'Duke', 'Dusk', 'Eagle', 'Engineer', 'Enigma', 'Eye', 'Falcon', 'Fang', 'Flame', 'Flare', 'Flash', 'Flea', 'Fly', 'Fury', 'Fighter', 'Fire', 'Ghost', 'Glider', 'Glory', 'Goliath', 'Guardian', 'Guardsman', 'Giant', 'Hammer', 'Harrier', 'Hawk', 'Hornet', 'Hulk', 'Hurricane', 'Inferno', 'Jet', 'Justice', 'Knight', 'Lantern', 'Liberator', 'Light', 'Lightning', 'Lion', 'Longshore', 'Machine', 'Mariner', 'Marvel', 'Mask', 'Maximus', 'Midget', 'Mime', 'Miracle', 'Mouse', 'Nimbus', 'Ninja', 'Nova', 'One', 'Paladin', 'Panther', 'Person', 'Phantom', 'Photon', 'Platypus', 'Prime', 'Prodigy', 'Protector', 'Q', 'Quasar', 'Racer', 'Racoon', 'Rage', 'Ranger', 'Ray', 'Ricochet', 'Rider', 'Robot', 'Rocket', 'Sailor', 'Samurai', 'Savage', 'Scarab', 'Scout', 'Shadow', 'Shield', 'Shogun', 'Shrike', 'Singer', 'Skier', 'Soarer', 'Spear', 'Specter', 'Speedster', 'Spider', 'Squid', 'Squirrel', 'Stalker', 'Star', 'Storm', 'Surfer', 'Sword', 'Sidekick', 'Torpedo', 'Tiger', 'Titan', 'Torch', 'Tornado', 'Torpedo', 'Valkyrie', 'Victory', 'Viking', 'Virtuoso', 'Vision', 'Walker', 'Warrior', 'Wasp', 'Wave', 'Wing', 'Wizard', 'Wolf', 'Wonder', 'Worm', 'X', 'Y', 'Yak', 'Z', 'Zero']
    if not name:
        return ''

    name = 'zapier-' + re.sub(r'\s|\W|\d', '', name)
    digest = hashlib.md5(name).hexdigest()
    hash = [int(digest[:16], 16), int(digest[16:], 16)]

    x = abs(hash[0])
    y = abs(hash[1])

    return a[x % len(a)] + ' ' + b[y % len(b)]


class StringSuperheroTransform(BaseTransform):

    category = 'string'
    name = 'superhero'
    label = 'Superhero Name'
    help_text = 'Convert a name into the name of a Superhero.'

    noun = 'Name'
    verb = 'convert to a Superhero'

    def transform(self, str_input, **kwargs):
        return superheroize(str_input)

register(StringSuperheroTransform())
