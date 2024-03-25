import shutil
import getopt
import sys
import yaml

#Grabs the template txt files.
def get_templates():
	f = open("template.txt", "r")
	main_template = f.read()
	f = open("stat_template.txt", "r")
	stat_template = f.read()

	print('Templates grabbed.')
	return main_template, stat_template

#Grab the settings file
def get_settings():
	with open('settings.yml', 'r') as file:
		settings = yaml.safe_load(file)
	print('Settings grabbed.')
	return settings

#Get the stat reference file that we request.
def get_stat_ref(stat_name):
	with open('scaling/' + stat_name + '.yml', 'r') as file:
		stat_ref = yaml.safe_load(file)
	return stat_ref

#Returns the format for the gem part
def get_gem_format(gem_count):
	socket_count = int(gem_count)
	gem_format = '\n    gem-sockets:\n    - Red'

	if socket_count > 1:
		gem_format = gem_format + '\n    - Blue'
	if socket_count > 2:
		gem_format = gem_format + '\n    - Gold'

	return gem_format

#Returns the modifier part format
def get_modifier_format(modifier_count, weapon_type):
	modifier_groups = int(modifier_count)
	modifier_format = '  modifiers:\n    elemental_damage_group:\n        min: 0\n        max: 1'

	if modifier_groups > 1:
		modifier_format = modifier_format + '\n    basic_damage_group:\n        min: 0\n        max: 1'
	if modifier_groups > 2:
		modifier_format = modifier_format + '\n    ' + weapon_type + '_auxilery_damage_group:\n        min: 0\n        max: 1'

	return modifier_format

#A bunch of dictionaries that keep track of stuff for the various tiers.
#Not the best way to do this probably but it changes a lot and this is easy
def get_references():
	upgrade_reference = {'common': '3', 'uncommon': '5', 'rare': '5', 'epic': '7', 'legendary': '7', 'mythic': '10'}
	color_reference = {'common': '&7', 'uncommon': '&2', 'rare': '&9', 'epic': '&5', 'legendary': '&6', 'mythic': '&d'}
	tier_reference = {
						'Tier1_1': 'common', 'Tier1_2': 'uncommon', 'Tier1_3': 'rare',
						'Tier2_1': 'common', 'Tier2_2': 'uncommon', 'Tier2_3': 'rare',
						'Tier3_1': 'common', 'Tier3_2': 'uncommon', 'Tier3_3': 'rare', 'Tier3_4': 'epic',
						'Tier4_1': 'uncommon', 'Tier4_2': 'rare', 'Tier4_3': 'epic', 'Tier4_4': 'legendary',
						'Tier5_1': 'uncommon', 'Tier5_2': 'rare', 'Tier5_3': 'epic', 'Tier5_4': 'legendary', 'Tier5_5': 'mythic'
					 }
	level_reference = {
						'Tier1_1': '1', 'Tier1_2': '3', 'Tier1_3': '6',
						'Tier2_1': '7', 'Tier2_2': '11', 'Tier2_3': '14',
						'Tier3_1': '15', 'Tier3_2': '20', 'Tier3_3': '25', 'Tier3_4': '29',
						'Tier4_1': '30', 'Tier4_2': '33', 'Tier4_3': '36', 'Tier4_4': '40',
						'Tier5_1': '41', 'Tier5_2': '43', 'Tier5_3': '46', 'Tier5_4': '48', 'Tier5_5': '50'
					 }
	stat_reference = {
						'Tier1_1': '0', 'Tier1_2': '1', 'Tier1_3': '3',
						'Tier2_1': '4', 'Tier2_2': '6', 'Tier2_3': '7',
						'Tier3_1': '11', 'Tier3_2': '16', 'Tier3_3': '21', 'Tier3_4': '25',
						'Tier4_1': '26', 'Tier4_2': '29', 'Tier4_3': '32', 'Tier4_4': '36',
						'Tier5_1': '40', 'Tier5_2': '40', 'Tier5_3': '40', 'Tier5_4': '40', 'Tier5_5': '40'
					 }
	gem_reference = {
						'Tier4_1': '1', 'Tier4_2': '1', 'Tier4_3': '1', 'Tier4_4': '2',
						'Tier5_1': '1', 'Tier5_2': '1', 'Tier5_3': '1', 'Tier5_4': '2', 'Tier5_5': '3'
					}
	modifier_reference = {
						'Tier3_3': '1', 'Tier3_4': '1',
						'Tier4_1': '1', 'Tier4_2': '1', 'Tier4_3': '1', 'Tier4_4': '2',
						'Tier5_1': '1', 'Tier5_2': '1', 'Tier5_3': '1', 'Tier5_4': '2', 'Tier5_5': '3'
					 }
	return upgrade_reference, color_reference, tier_reference, level_reference, stat_reference, gem_reference,modifier_reference

#The main thing that takes care of creating the actual file
def format_output(main_template, stat_template, settings):
	print('Startting Format.')

	#Not the best way to do this but is easy
	upgrade_reference, color_reference, tier_reference, level_reference, stat_reference, gem_reference, modifier_reference = get_references()
	weapon_type = settings['TYPE']

	#Create/Open the output file
	f = open('output/' + weapon_type.lower() + '.yml', 'w')
	
	#Loop through every tier
	for i in tier_reference:
		#Set up some variables
		rarity = tier_reference[i]
		tier = i.split('_')[0]
		scale_ref = tier + '_' + rarity
		new_stats = ''
		required_class = ''
		class_list = settings['REQUIRED_CLASS']
		stat_settings = settings['STATS']
		
		#Handful of things that might show up on an item based off of the tier
		if stat_reference[i] != '0':
			required_stat = '\n    required_' + settings['REQUIRED_STAT'] + ': ' + stat_reference[i]
		else:
			required_stat = ''

		if i in gem_reference:
			gem_format = get_gem_format(gem_reference[i])
		else:
			gem_format = ''
		if i in modifier_reference:
			modifier_format = get_modifier_format(modifier_reference[i], weapon_type.lower())
		else:
			modifier_format = ''

		#Start Replacing text
		new_format = main_template.replace('TYPEU', weapon_type.upper())
		new_format = new_format.replace('TYPE', weapon_type)
		new_format = new_format.replace('MATERIAL', settings['MATERIAL'])
		new_format = new_format.replace('TEMPLATE', settings['TEMPLATE'])
		new_format = new_format.replace('SPEED_STAT', settings['SPEED'])
		new_format = new_format.replace('UPGRADES', upgrade_reference[rarity])
		new_format = new_format.replace('RARITYL', rarity)
		new_format = new_format.replace('RARITY', rarity.upper())
		new_format = new_format.replace('TIER', tier.upper())	
		new_format = new_format.replace('|GEM', gem_format)
		new_format = new_format.replace('|MODIFIER', modifier_format)
		new_format = new_format.replace('LEVEL', level_reference[i])
		new_format = new_format.replace('|REQUIRED_STAT', required_stat)
		new_format = new_format.replace('LORE_PLACEHOLDER', settings['REQUIRED_CLASS_LORE'])
		new_format = new_format.replace('NAME_COLOR', color_reference[rarity])

		#Stats need to be looped through
		for j in stat_settings:
			stats = stat_template.replace('STAT_NAME', j)
			stat_ref = get_stat_ref(j + '_' + stat_settings[j])
			scale_point = stat_ref[scale_ref]
			for h in scale_point:
				stats = stats.replace(h, scale_point[h])

			new_stats = new_stats + stats + '\n'

		new_format = new_format.replace('STATS', new_stats)

		#Same with classes.
		for c in class_list:
			formated_class = c.replace('\\', '')
			required_class = required_class + '\n    - ' + formated_class

		new_format = new_format.replace('REQUIRED_CLASSES', required_class)

		f.write(new_format)
		f.write("\n")

	f.close()

def main():
	try:
		main_template, stat_template = get_templates()
		settings = get_settings()
		format_output(main_template, stat_template, settings)
		print('Format Done.')
	except Exception as e:
		print("Something broke: " + str(e))

if __name__ == "__main__":
	main()
