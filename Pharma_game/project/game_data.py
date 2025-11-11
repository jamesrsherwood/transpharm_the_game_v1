NPC_DATA = {
	'random1': {
		'dialog': {
			'default': ['When I was young this was all fields. Now we have a chemical plant polluting the river.',
               'I\'ve forgotton where I live...'
               ],
			'visited': None,
            'return': ['The water is still green!',
                       'If the pharmaceuticals in the river do not rapidly biodegrade they can accumulate.',
                       'The risk to the environment from a chemical depends on how much and how potent it is.',
                       'The worst case scenerio is very persistent and very toxic pollution.',
                       'Please help save the environment!'],
            'endgame': ['I knew you could do it!']},
		'directions': ['left', 'right'],
		'look_around': False, # if False only the player can talk to them, but if radius = 0 I think that stops them anyway
		'patrol': True, # Enable patrol movement
		'patrol_distance': 400, # Distance to patrol in pixels
		'visited': False,
        'return': False,
        'endgame': False,
		'biome': None
		},
	'random2': {
		'dialog': {
			'default': ['Like I\'ve always said, progress at any cost.', 'Yes I heard the river turned green, but I kinda like it!'], 
			'visited': None,
            'return': ['Hello again.', 'I don\'t feel well.'],
            'endgame': ['I feel much better now I\'m not burdened by the psychological torment of living beyond the Planetary Boundaries!']},
		'directions': ['left', 'down'],
		'look_around': False,
        'patrol': True, # Enable patrol movement
		'patrol_distance': 160, # Distance to patrol in pixels
		'visited': False,
        'return': False,
        'endgame': False,
		'biome': None
		},
	'environmentalist': {
		'dialog': {
			'default': ['Thank goodness you are here!',
               'I am an environmental scientist from the University.',
               'The water quality is very poor. Please ask around and find out the cause of the problem.',
               'I need to take some more samples now.',
               'Feel free to come back and chat with me anytime!',
			   ], 
			'visited': None,
            'return': ['Are you making progress?',
				'Pharmaceuticals mostly enter the environment because we excrete them and their by-products.',
                'The waste water from the factory should be purified before being released.',
                'Maybe you should go and check that...',
                'Now hurry, before it\'s too late!'
                ],
            'endgame': ['I knew I could count on you!', 'You saved the fish and preserved the environment for generations to come!']},
		'directions': ['up', 'left', 'right', 'down'],
		'look_around': True,
		'visited': False,
        'return': False,
        'endgame': False,
		'biome': None
		},
	'patient1': {
		'dialog': {
			'default': ['What are you in for?', 'This is an excellent hospital.'], 
			'visited': None,
            'return': ['My doctor has me taking so many pills!',
                       'Some medicines are not as effective in combination with other drugs.', 
                       'Over time, patients can accumulate different treatments.',
                       'I should get the doctor to review my prescriptions.'
                       ],
            'endgame': ['These new tablets make me feel much better.']},
		'directions': ['right'],
		'look_around': True,
		'visited': False,
        'return': False,
        'endgame': False,
		'biome': None
		},
	'patient2': {
		'dialog': {
			'default': ['My kidneys hurt! Ow ow ow!',
               			'My friends told me not to drink the river water, but I was so thirsty!',
                        'I\'m waiting for some Chloripenzaminophen for the pain.'], 
			'visited': None,
            'return': ['I think this hospital is only concerned with short term cost saving measures.',
                       'Why did they give me my pills in a single use plastic cup!?!?',
                       'There are probably cheaper medicines that do a better job too, if they would only invest the effort to find out!',
                       'Just by avoiding the pollution fines they would save some money.',
                       'Then they could use the savings they make to install a water fountain or two.',
					   ],
            'endgame': ['What a star you are!']},
		'directions': ['up', 'right'],
		'look_around': True,
		'visited': False,
        'return': False,
        'endgame': False,
		'biome': None
		},
	'factory0': {
		'safety': {0: ('Standard PPE', 14), 1: ('PPE and extra ventilation', 8), 2: ('No PPE', 5), 3: ('Closed reactor system', 5)},
        'emissions': {0: ('No wastewater treatment', 4), 1: ('Basic water treatment', 5), 2: ('Advanced water treatment', 5)},
        'energy': {0: ('Standard energy', 41), 1: ('Green energy', 25)},
		'dialog': {
			'default': ['I heard about you.',
               'Our manufacturing processes conform to all regulations!',
               'Oh, you\'ve got some ideas to optimise the drug production process? Let\'s hear it then!'], 
			'visited': ['Thank you for that insight.', 'If you have more ideas we are happy to try them.'],
            'return': ['Do you want to change your mind?'],
			'endgame': ['Good doing business with you!']},
		'directions': ['down'],
		'look_around': False,
		'visited': False,
        'return': False,
        'endgame': False,
		'biome': 'industrial'
		},
	'factory1': {
		'dialog': {
			'default': ['This is definately a safe working environment. I haven\'t been seriously injuried for 2 weeks now!',
               			'A few Chloripenzaminophen pills and I\'m back on my feet!',
                        'We make that here don\'t you know?'
						], 
			'visited': None,
            'return': ['We currently use the standard issue personal protective equipment, or PPE',
                       'It is sufficient for most things but particularly hazardous substances require more safety measures.',
                       'Where I used to work, we had extra ventiliation to reduce exposure to toxic chemicals.',
                       'I also heard about closed reactors that once the chemicals are put inside, there is no exposure to workers like me!',
                       'That equipment is expensive though.'
                       ],
            'endgame': ['The plant is so much more productive and safer these days!']},
		'directions': ['right'],
		'look_around': False,
		'patrol': True, # Enable patrol movement
		'patrol_distance': 70, # Distance to patrol in pixels
		'visited': False,
        'return': False,
        'endgame': False,
		'biome': None
		},
	'factory2': {
		'dialog': {
			'default': ['We need help optimizing our reaction conditions.',
               'Hotter reactions need more energy per hour, but will be completed sooner.',
               'The necessary reaction duration depends on the reactivity of the chemicals we use.',
               'Ideally we can use readily reactive chemicals that make lots of the intended product quickly without too much energy.',
               'So what temperature and duration should we try next?'
               ], 
			'visited': ['Thanks for setting those parameters. We\'ll run the reaction now.'],
			'return': ['Do you want to adjust the reaction conditions?',
              			'Remember, we want to make as much medicine as possible!',
                        'Waste costs us money...but so does heating the reactors for long periods of time.'
						],
			'endgame': ['You should be very proud of what you achieved. I\'m embarrassed we caused so much pollution.']},
		'directions': ['right'],
		'look_around': False,
		'visited': False,
		'return': False,
		'endgame': False,
		'biome': 'industrial'
		},		
	'medic': {
		'cups': {0: ('Reusable dispensing cup', 14), 1: ('Single use dispensing cup', 12)},
        'deprescribe': {0: ('Prescribe as required', 4), 1: ('Deprescribing Program', 5)},
		'dialog': {
			'default': ['How can I help you?', 'You have some advice about medication practices for me?'], 
			'visited': ['I\'m exicited to try out your ideas!'],
            'return': ['I heard that using single use dispensing cups for our patients medicines is accumulating a lot of waste',
                       'And costing us money!',
                       'Reusable cups will reduce the costs and climate change impact of the hospital.',
                       'So do you want to adjust our medication strategy again?'
                       ],
			'endgame': ['I cannot believe the difference around this place!']},
		'directions': ['right'],
		'look_around': False,
		'visited': False,
        'return': False,
        'endgame': False,
		'biome': 'medical'
		},
	'scientist': {
		'FG_left': {0: ('molecule_C1', 4), 1: ('molecule_C2', 5), 2: ('molecule_C3', 15)},
		'molecule_template_left': {0: ('molecule_A1', 4), 1: ('molecule_A2', 5), 2: ('molecule_A3', 15)},
        'molecule_template_right': {0: ('molecule_B1', 4), 1: ('molecule_B2', 5), 2: ('molecule_B3', 15)},
        'FG_right': {0: ('molecule_D1', 4), 1: ('molecule_D2', 5), 2: ('molecule_D3', 15)},
		'dialog': {
			'default': ['Hello! I am the Professor here in the chemistry department.',
               'Yes, I invented Chloripenzaminophen, the drug produced at the factory down the road.',
               'What! That\'s why the river turned green! Oh my!',
               'We must fix this!',
               'This class of medicine is composed of 4 segments that are created from 4 corresponding reactants.',
               'Slight adjustments to the atomic arrangement in each reactant produces different properties.',
               'Some properties are benefical, such as efficacy, meaning how effective the medicine is',
               'Other properties are bad, such as ecotoxicity.',
               'We must find the correct balance!'
               ], 
			'visited': ['Let\'s get this bad boy tested and into production!',
               			'Now we\'ve done the preliminary testing, it only takes another 10 years to get to market!'],
            'return': ['Do you want to redesign the drug molecule?',
                       'Remember, subtle changes in the molecular structure change the efficacy, biodegradability and ecotoxicity',
                       'Each reactant has a quite different cost, carbon footprint, and amount of waste associated with it.'],
			'endgame': ['I\'ve been nominated for the Nobel Prize!',
               			'No, we can\'t share the prize money.',
                        'Do you want to help design a new medicine?']},
		'directions': ['right'],
		'look_around': False,
		'visited': False,
		'return': False,
        'endgame': False,
		'biome': 'laborious'
		},
	'ngo': {
		'procurement': {0: ('No procurement rules', 9), 1: ('Bio-procurement', 15), 2: ('Sustainable procurement', 14)},
		'pollution_standards': {0: ('No water quality standards', 4), 1: ('Lenient water quality standards', 5), 2: ('Strict water quality standards', 5)},
        'biodegradation_standards': {0: ('Biodegradation standard', 4), 1: ('No biodegradation standard', 5)},
		'dialog': {
			'default': ['We need to push for stronger regulation.',
               			'We have been working on two ideas.',
               			'Firstly, a rule that public sector procurement must prioritise biodegradable products.',
                        'A minimum biodegradability of 50 percent has been suggested.',
                        'Secondly, we are developing rules for low-carbon footprint products.',
                        'Considering how much carbon-offsetting is being practiced, we can calculate a carbon budget for products.',
                        'If enforced by law, the economy would be carbon neutral overall.',
                        'It is still in the early stages of development but we could push it through quicker if needs be.'], 
			'visited': ['The fight never ends!'],
            'return': ['Do you want to change the procurement strategy?',
                       'We can also change the water regulations.',
                       'We set limits for pollution entering the river.'
                       ],
			'endgame': ['Triumph! Our work is done.']},
		'directions': ['down'],
		'look_around': False,
		'visited': False,
        'return': False,
        'endgame': False,
		'biome': 'business'
		},
	'boss': {
		'dialog': {
			'default': ['You - come here!',
               'What\'s all this about pharmaceuticals destroying the environment?',
               'Go and fix this then report back to me!'
               ],
			'visited': None,
            'return': ['Help us!'],
            'endgame': ['We thank you for implementing new measures to protect the environment.',
                        'Please collect feedback from our residents.',
                        'I\'ll put the OBE in the post. Now begone!']},
		'directions': ['up', 'down', 'left', 'right'],
		'look_around': True,  # Enable for endgame auto-approach
		'visited': False,
        'return': False,
        'endgame': False,
		'biome': None
		},
	'man1': { #man looking out to sea
		'dialog': {
			'default': ['I remember when this water was clean enough to bathe in!', 'Oh how we frolicked.'], 
			'visited': None,
            'return': ['You know, it\'s not just the pollution in the water that\'s the issue?',
                       'The pharmaceutical supply chain causes lots of carbon dioxide emissions resulting in climate change!',
                       'Some drug molecules are inherently more energy intensive to make, and energy is a big source of carbon emissions.',
                       'We can use renewable sources of energy with much lower carbon emissions, but some companies won\'t pay any extra!',
                       'Maybe you can convince them?'
					   ],
            'endgame': ['Ahh, time for a dip!']},
		'directions': ['up', 'left', 'right', 'down'],
		'look_around': True,
		'visited': False,
        'return': False,
        'endgame': False,
		'biome': None
		},
	'man2': { #rear student scientist
		'dialog': {
			'default': ['Hi! I study biodegradable drugs.', 'I think I\'m onto something good here.'], 
			'visited': None,
            'return': ['I\'ve developed this great chemical precursor that imparts rapid biodegradability into the final product.',
                       'It has the shape of a pentagon!', 'Help me convince the boss to use it!'],
            'endgame': ['Thanks for putting a word in with the boss!']},
		'directions': ['up', 'left', 'right', 'down'],
		'look_around': True,
		'visited': False,
        'return': False,
        'endgame': False,
		'biome': None
		},
	'student': { #front student scientist
		'dialog': {
			'default': ['Hello! I am a student here in the university labs!',
               'I helped develop Chloripenzaminophen.'
			   'But we have a lot more drug candidates available here.',
               'By changing the arrangement of atoms we can impart different properties...',
               '...and not just medical efficacy but also environmental performance.',
               'You just need to convince the Prof to commercialise them.'], 
			'visited': None,
            'return': ['Explore the different molecular combinations to propose a safe and effective medicine.'],
            'endgame': ['Thank you for your help.', 'Now I must get on and finish this work.']},
		'directions': ['up', 'left', 'right', 'down'],
		'look_around': True,
		'visited': False,
        'return': False,
        'endgame': False,
		'biome': None
		},
  	'woman1': { #aide in the palace
		'dialog': {
			'default': ['Yes?', 'Oh, you want to know what regulations need updating to preserve the environment?',
               'We can introduce a minimum biodegradability standard for pharmaceuticals!',
               'That would limit the effects of persistent pollution.',
               'There is also the possibility to change procurement rules.',
               'That means hospitals could only buy biodegradable or low carbon footprint products.',
               'A procurement strategy to promote biodegradable pharmaceuticals only works if we can certify if a chemical is biodegradable.',
               'You\'ll need to work with the NGO to push these policies through.'], 
			'visited': None,
            'return': ['Any progress?', 'You can get an overview from the Queen.', 'She will see you now.'],
            'endgame': ['All\'s well that ends well.']},
		'directions': ['up', 'left', 'right', 'down'],
		'look_around': True,
		'visited': False,
        'return': False,
        'endgame': False,
		'biome': None
		},
	'woman2': { #retired nurse
		'dialog': {
			'default': ['Do I know you?',
               'Oh, that\'s OK then.',
               'I used to be a nurse you know.',
               'Back in my day, we reused things. Now everything gets thrown away.',
               'Have you seen my Chloripenzaminophen anywhere aroung here?'],
			'visited': None,
            'return': ['How are the doctors down at the hospital?',
                       'So much pressure to prescribe drugs that some people suffer side effects from multiple treatments.',
                       'In some cases, re-evaluating prescriptions leads to fewer drugs with better outcomes.'],
            'endgame': ['Do I know you?', 'That\'s right, I remember now.', 'How did you get in here?']},
		'directions': ['up', 'left', 'right', 'down'],
		'look_around': True,
		'visited': False,
        'return': False,
        'endgame': False,
		'biome': None
		},
	'safesage': {
		'dialog': {
			'default': ['Hello! I am the safety officer, but I am interested in chemical engineering too!',
               			'Dynamic dialog generated in get_safesage_dialog() method'],
			'visited': None,
            'return': ['Dynamic dialog generated in get_safesage_dialog() method'],
            'endgame': ['We have a good balance between the environmental, social, and economic pillars of sustainability now.'
                       ]},
		'directions': ['up', 'left', 'right', 'down'],
		'look_around': True,
		'visited': False,
        'return': False,
        'endgame': False,
		'biome': None
		},
	'envirosage': {
		'dialog': {
			'default': ['Welcome, I am the head of ecological stewardship here.',
               			'Dynamic dialog generated in get_envirosage_dialog() method',
						],
			'visited': None,
            'return': ['Dynamic dialog generated in get_envirosage_dialog() method'],
            'endgame': ['The waters run clear once more!']},
		'directions': ['up', 'left', 'right', 'down'],
		'look_around': True,
		'visited': False,
        'return': False,
        'endgame': False,
		'biome': None
		},
	'chemsage': {
		'dialog': {
			'default': ['Greetings!',
               			'Dynamic dialog generated in get_chemsage_dialog() method'],
			'visited': None,
            'return': ['Dynamic dialog generated in get_chemsage_dialog() method'],
            'endgame': ['Good work!']},
		'directions': ['up', 'left', 'right', 'down'],
		'look_around': True,
		'visited': False,
        'return': False,
        'endgame': False,
		'biome': None
		}
}

MONSTER_DATA = { # legacy of template game but simplified to only essential fields used in pharmaceutical game
    'molecule_A1': {'stats': {'max_health': 3, 'max_energy': 2, 'speed': 1.1}, 'abilities': None},
	'molecule_A2': {'stats': {'max_health': 2, 'max_energy': 2, 'speed': 1.1}, 'abilities': None},
	'molecule_A3': {'stats': {'max_health': 1, 'max_energy': 2, 'speed': 1.1}, 'abilities': None},
	'molecule_B1': {'stats': {'max_health': 2, 'max_energy': 6, 'speed': 1.1}, 'abilities': None},
	'molecule_B2': {'stats': {'max_health': 1, 'max_energy': 4, 'speed': 1.1}, 'abilities': None},
	'molecule_B3': {'stats': {'max_health': 1, 'max_energy': 5, 'speed': 1.1}, 'abilities': None},
    'molecule_C1': {'stats': {'max_health': 3, 'max_energy': 1, 'speed': 1.1}, 'abilities': None},
	'molecule_C2': {'stats': {'max_health': 3, 'max_energy': 1, 'speed': 1.1}, 'abilities': None},
	'molecule_C3': {'stats': {'max_health': 3, 'max_energy': 4, 'speed': 1.1}, 'abilities': None},
	'molecule_D1': {'stats': {'max_health': 2, 'max_energy': 3, 'speed': 1.1}, 'abilities': None},
	'molecule_D2': {'stats': {'max_health': 1, 'max_energy': 2, 'speed': 1.1}, 'abilities': None},
	'molecule_D3': {'stats': {'max_health': 2, 'max_energy': 8, 'speed': 1.1}, 'abilities': None},
	'Standard PPE': {'stats': {'max_health': 2, 'max_energy': 8, 'speed': 1.1}, 'abilities': None},
	'PPE and extra ventilation': {'stats': {'max_health': 2, 'max_energy': 8, 'speed': 1.1}, 'abilities': None},
	'No PPE': {'stats': {'max_health': 2, 'max_energy': 8, 'speed': 1.1}, 'abilities': None},
	'Closed reactor system': {'stats': {'max_health': 2, 'max_energy': 8, 'speed': 1.1}, 'abilities': None},
	'No wastewater treatment': {'stats': {'max_health': 2, 'max_energy': 8, 'speed': 1.1}, 'abilities': None},
	'Basic water treatment': {'stats': {'max_health': 2, 'max_energy': 8, 'speed': 1.1}, 'abilities': None},
	'Advanced water treatment': {'stats': {'max_health': 2, 'max_energy': 8, 'speed': 1.1}, 'abilities': None},
	'Reusable dispensing cup': {'stats': {'max_health': 2, 'max_energy': 8, 'speed': 1.1}, 'abilities': None},
	'Single use dispensing cup': {'stats': {'max_health': 2, 'max_energy': 8, 'speed': 1.1}, 'abilities': None},
	'Prescribe as required': {'stats': {'max_health': 2, 'max_energy': 8, 'speed': 1.1}, 'abilities': None},
	'Deprescribing Program': {'stats': {'max_health': 2, 'max_energy': 8, 'speed': 1.1}, 'abilities': None},
	'No procurement rules': {'stats': {'max_health': 2, 'max_energy': 8, 'speed': 1.1}, 'abilities': None},
	'Bio-procurement': {'stats': {'max_health': 2, 'max_energy': 8, 'speed': 1.1}, 'abilities': None},
	'Sustainable procurement': {'stats': {'max_health': 2, 'max_energy': 8, 'speed': 1.1}, 'abilities': None},
	'No water quality standards': {'stats': {'max_health': 2, 'max_energy': 8, 'speed': 1.1}, 'abilities': None},
	'Lenient water quality standards': {'stats': {'max_health': 2, 'max_energy': 8, 'speed': 1.1}, 'abilities': None},
	'Strict water quality standards': {'stats': {'max_health': 2, 'max_energy': 8, 'speed': 1.1}, 'abilities': None},
	'Biodegradation standard': {'stats': {'max_health': 2, 'max_energy': 8, 'speed': 1.1}, 'abilities': None},
	'No biodegradation standard': {'stats': {'max_health': 2, 'max_energy': 8, 'speed': 1.1}, 'abilities': None},
	'Standard energy': {'stats': {'max_health': 2, 'max_energy': 8, 'speed': 1.1}, 'abilities': None},
	'Green energy': {'stats': {'max_health': 2, 'max_energy': 8, 'speed': 1.1}, 'abilities': None},
	'reaction_temperature': {'stats': {'max_health': 0, 'max_energy': 0, 'speed': 0}, 'abilities': None},
	'reaction_hours': {'stats': {'max_health': 0, 'max_energy': 0, 'speed': 0}, 'abilities': None},
}