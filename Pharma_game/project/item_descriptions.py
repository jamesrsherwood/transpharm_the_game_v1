# item_descriptions.py
# Descriptions for all player choices displayed in the monster index

# Drug code combinations (molecule_A/B/C/D + 1/2/3 combinations)
# Format: 'AAAA' = molecule_A1 + molecule_A1 + molecule_A1 + molecule_A1 (in slots 0-3)
DRUG_CODE_DESCRIPTIONS = {
    'AAAA': {
        'name': 'Chloripenzaminophen',
        'description': 'A popular treatment but with high environmental impacts and a highly hazardous synthesis.'
    },
    'AAAB': {
        'name': 'Chloripenzoaminatine',
        'description': 'This compound is effective but comes with high production costs and carbon emissions.'
    },
    'AAAC': {
        'name': 'Chloripenzoaminate',
        'description': 'The cost of the ingredients makes this is the most expensive drug candidate.'
    },
    'AABA': {
        'name': 'Chloripenzoflozaphen',
        'description': 'This compound has high emissions and poor biodegradability.'
    },
    'AABB': {
        'name': 'Chloripenzoflozatin',
        'description': 'A potent moelcule with high production costs.'
    },
    'AABC': {
        'name': 'Chloripenzoflozate',
        'description': 'The manufacturing process is the most wasteful and quite expensive.'
    },
    'AACA': {
        'name': 'Chloripenzoninaphen',
        'description': 'The hazard to workers and aquatic organisms is very high.'
    },
    'AACB': {
        'name': 'Chloripenzoninatin',
        'description': 'A very potent medicine associated with quite large emissions and costs.'
    },
    'AACC': {
        'name': 'Chloripenzoninate',
        'description': 'A poorly biodegradable molecule that creates a lot of waste.'
    },
    'ABAA': {
        'name': 'Chlorivaminophen',
        'description': 'This active ingredient has an efficient synthesis.'
    },
    'ABAB': {
        'name': 'Chlorivaminatin',
        'description':  'The metabolites of this medicine are quite to biograde with low toxicity.'
    },
    'ABAC': {
        'name': 'Chlorivaminate',
        'description':  'This compound has a low efficacy.'
    },
    'ABBA': {
        'name': 'Chlorivaflozaphen',
        'description':  'This compound is slowly biodegradable but has an efficient synthesis.'
    },
    'ABBB': {
        'name': 'Chlorivaflozatin',
        'description':  'This medicine has a low impact on water quality.'
    },
    'ABBC': {
        'name': 'Chlorivaflozate',
        'description': 'This bio-based compound has a low impact on water quality.'
    },
    'ABCA': {
        'name': 'Chlorivaninaphen',
        'description': 'With a very effective synthesis, this is an appealing candidate for manufacturers.'
    },
    'ABCB': {
        'name': 'Chlorivaninatin',
        'description': ' A very potent medicine that is straightforward to produce.'
    },
    'ABCC': {
        'name': 'Chlorivaninate',
        'description':  'A drug candidate with decent all-round performance.'
    },
    'ACAA': {
        'name': 'Chloribuminophen',
        'description':  'A low effacacy drug molecule with high environmental toxicity and persistency.'
    },
    'ACAB': {
        'name': 'Chloribuaminatin',
        'description':  'An average performance compound with low bio-based content.'
    },
    'ACAC': {
        'name': 'Chloribuaminate',
        'description':  'A wasteful synthesis to create a low effacacy medicine.'
    },
    'ACBA': {
        'name': 'Chloribuflozaphen',
        'description': 'A molecule with poor performance as a medicine and in the environment.'
    },
    'ACBB': {
        'name': 'Chloribuflozatin',
        'description': 'A low toxicity compound with a wasteful synthesis.'
    },
    'ACBC': {
        'name': 'Chloribuflozate',
        'description': ' A very wasteful production method to yield a low performance medicine.'
    },
    'ACCA': {
        'name': 'Chloribuninophen',
        'description':  'The manufacturing process is dangerous to workers.'
    },
    'ACCB': {
        'name': 'Chloribuninatin',
        'description':  'A very potent medicine with high biodegradability.'
    },
    'ACCC': {
        'name': 'Chloribuninate',
        'description':  'An all-rounder with a somewhat wasteful synthesis.'
    },
    'BAAA': {
        'name': 'Diazopenzoaminophen',
        'description':  'This compound has a high exo-toxicity and is difficult to manufacture.'
    },
    'BAAB': {
        'name': 'Diazopenzoaminatin',
        'description': 'This compound has high efficacy but the reaction to produce it is slow.'
    },
    'BAAC': {
        'name': 'Diazopenzoaminate',
        'description': 'This compound has an expensive and slow manufacturing process.'
    },
    'BABA': {
        'name': 'Diazopenzoflozaphen',
        'description':  'This medicine has poor biodegradability and take a long time to make.'
    },
    'BABB': {
        'name': 'Diazopenzoflozatin',
        'description':  'A low toxicity, high efficacy compound but slow to make.'
    },
    'BABC': {
        'name': 'Diazopenzoflozate',
        'description':  'The manufacturing process has relative low emissions with low risk to workers.'
    },
    'BACA': {
        'name': 'Diazopenzoninaphen',
        'description':  'A potent molecule with high exotoxicity.'
    },
    'BACB': {
        'name': 'Diazopenzoninatin',
        'description': 'A potent molecule with moderate exotoxicity.'
    },
    'BACC': {
        'name': 'Diazopenzoninate',
        'description': 'This molecule has low ecotoxicity and reasonably low carbon emissions.'
    },
    'BBAA': {
        'name': 'Diazorivaminophen',
        'description': 'This compound has an efficient production route with minimal waste.'
    },
    'BBAB': {
        'name': 'Diazorivaminatin',
        'description':  'A low toxicity, potent medicine.'
    },
    'BBAC': {
        'name': 'Diazorivaminate',
        'description':  'A bio-based candidate with low ecotoxicity and low emissions.'
    },
    'BBBA': {
        'name': 'Diazorivaflozaphen',
        'description':  'Mildly ecotoxic with low waste and low carbon emissions.'
    },
    'BBBB': {
        'name': 'Diazorivaflozatin',
        'description':  'A potent medicine with minimal hazards.'
    },
    'BBBC': {
        'name': 'Diazorivaflozate',
        'description': 'A bio-based molecule with very low carbon emissions.'
    },
    'BBCA': {
        'name': 'Diazorivaninophen',
        'description': 'A potent medicinewith some ecotoxicity concerns.'
    },
    'BBCB': {
        'name': 'Diazorivaninatin',
        'description': 'Good production stats with low ecotoxicity.'
    },
    'BBCC': {
        'name': 'Diazorivaninate',
        'description':  'Produced with low emissions with minimal risk and waste.'
    },
    'BCAA': {
        'name': 'Diazibuaminophen',
        'description':  'Ammenable production method but hazardous to the environment.'
    },
    'BCAB': {
        'name': 'Diazibuaminatin',
        'description':  'A molecule with low bio-based content and slow to manufacture.'
    },
    'BCAC': {
        'name': 'Diazibuaminate',
        'description':  'This molecule has very low efficacy, meaning the dose is high.'
    },
    'BCBA': {
        'name': 'Diazibuflozophen',
        'description': 'A low emissions, cost-effective manufacturing process for an ecotoxic molecule.'
    },
    'BCBB': {
        'name': 'Diazibuflozatin',
        'description': 'Good all-round performance but the reaction to make it is sluggish.'
    },
    'BCBC': {
        'name': 'Diazibuflozate',
        'description': 'A low performance medicine with minimal hazards and low emissions.'
    },
    'BCCA': {
        'name': 'Diazoibuninaphen',
        'description':  'An efficient production process but significant environmental hazard.'
    },
    'BCCB': {
        'name': 'Diazoibuninatin',
        'description':  'A potent medicine with low impact production and minimal environmental issues.'
    },
    'BCCC': {
        'name': 'Diazoibuninate',
        'description':  'Low carbon emissions and low aquatic toxicity.'
    },
    'CAAA': {
        'name': 'Adapenzoaminophen',
        'description':  'The metabolites of this compound are very toxic to aquatic organisms.'
    },
    'CAAB': {
        'name': 'Adapenzoaminatin',
        'description': 'This compound results in high carbon emissions and moderate risk to the environment.'
    },
    'CAAC': {
        'name': 'Adapenzoaminate',
        'description': 'A low efficacy medicine with high production emisisons and costs.'
    },
    'CABA': {
        'name': 'Adapenzoflozaphen',
        'description':  'A low efficacy medicine with high ecotoxicity.'
    },
    'CABB': {
        'name': 'Adapenzoflozatin',
        'description':  'An all-round performer, low risk to workers.'
    },
    'CABC': {
        'name': 'Adapenzoflozate',
        'description':  'A bio-based candidate but low efficacy and high waste.'
    },
    'CACA': {
        'name': 'Adapenzoninaphen',
        'description':  'An ecotoxic molecule that is also hazardous to workers.'
    },
    'CACB': {
        'name': 'Adapenzoninatin',
        'description': 'A very potent medicine with reasonble performance in other aspects.'
    },
    'CACC': {
        'name': 'Adapenzoninate',
        'description': 'A bio-based medicine with reasonble performance in other aspects.'
    },
    'CBAA': {
        'name': 'Adarivaminophen',
        'description': 'Efficient to produce but low efficacy as a medicine.'
    },
    'CBAB': {
        'name': 'Adarivaminatin',
        'description':  'Rapidly biodegradable medicine with an efficient synthesis.'
    },
    'CBAC': {
        'name': 'Adarivaminate',
        'description':  'A biodegradable, bio-based medicine.'
    },
    'CBBA': {
        'name': 'Adarivoflozaphen',
        'description':  'The second highest bio-based content, with low impact and minimal ecotoxicity.'
    },
    'CBBB': {
        'name': 'Adarivoflozatin',
        'description':  'A low impact, low hazard candidate.'
    },
    'CBBC': {
        'name': 'Adariviflozate',
        'description': 'The highest bio-based content, very low carbon emisisons.'
    },
    'CBCA': {
        'name': 'Adarivaninophen',
        'description': 'The manufacturing process is the most rapid of all candidates.'
    },
    'CBCB': {
        'name': 'Adarivaninatin',
        'description': 'A potent medicine with rapid biodegradability.'
    },
    'CBCC': {
        'name': 'Adarivaninate',
        'description':  'An efficient production process but low efficacy as a medicine.'
    },
    'CCAA': {
        'name': 'Adibuminaphen',
        'description':  'A low efficacy and toxic molecule.'
    },
    'CCAB': {
        'name': 'Adibuminatin',
        'description':  'A highly biodegradable molecule with low production costs.'
    },
    'CCAC': {
        'name': 'Adibuminaate',
        'description':  'A low efficacy medicine with low production costs.'
    },
    'CCBA': {
        'name': 'Adibuflozaphen',
        'description': 'Low production costs but ecotoxic.'
    },
    'CCBB': {
        'name': 'Adibuflozatin',
        'description': 'A rapidly biodegradable compound with lwo production costs.'
    },
    'CCBC': {
        'name': 'Adibuflozate',
        'description': 'Low therapeutic value but low carbon emissions and cheap to manufacture.'
    },
    'CCCA': {
        'name': 'Adaibuninaphen',
        'description':  'A low cost but exotoxic option.'
    },
    'CCCB': {
        'name': 'Adaibuninatin',
        'description':  'The fastest biodegrading substance with low production cost.'
    },
    'CCCC': {
        'name': 'Adaibuninate',
        'description':  'A cheap and biodegradable medicine.'
    }
}



# Safety equipment choices (slot 4)
ITEM_DESCRIPTIONS = {
    'Standard PPE': {
        'name': 'Basic Safety Equipment',
        'description': 'Standard personal protective equipment consisting of gloves, goggles, and lab coats. Provides moderate worker protection at low cost. Suitable for compounds with low-medium toxicity.',
        'cost': '$5/day',
        'protection_level': 'Moderate (÷4 exposure)'
    },
    'PPE and extra ventilation': {
        'name': 'Ventilation System',
        'description': 'Enhanced air extraction and local exhaust ventilation to minimise airborne exposure. Reduces risk from volatile hazardous compounds.',
        'cost': '$15/day',
        'protection_level': 'Good (÷10 exposure)'
    },
    'No PPE': {
        'name': 'No Safety Equipment',
        'description': 'No protective measures. Only suitable for completely non-hazardous compounds.',
        'cost': '$0/day',
        'protection_level': 'None (full exposure)'
    },
    'Closed reactor system': {
        'name': 'Closed System',
        'description': 'Expensive and partiall automated handling of hazard substances. Negligible expsoure to hazardous compounds.',
        'cost': '$75/day',
        'protection_level': 'Excellent (÷100 exposure)'
    },
    
    # Emissions treatment (slot 5)
    'No wastewater treatment': {
        'name': 'No Treatment',
        'description': 'Wastewaste released directly to the river. Likely to violate water quality standards.',
        'cost': '$0/day',
        'api_removal': '0% (0.02 g/g emitted)',
        'metabolite_effect': 'No metabolite capture'
    },
    'Basic water treatment': {
        'name': 'Basic Treatment',
        'description': 'Simple filtration and settling tanks to remove particulates and some dissolved chemicals.',
        'cost': '$0.05/day',
        'api_removal': '75% (0.005 g/g emitted)',
        'metabolite_effect': 'No metabolite capture'
    },
    'Advanced water treatment': {
        'name': 'Advanced Treatment',
        'description': 'Comprehensive wastewater treatment including activated sludge and chemical oxidation. Removes the majority of chemical contamination.',
        'cost': '$0.75/day',
        'api_removal': '0% API, captures metabolites (0.005 g/g)',
        'metabolite_effect': 'Metabolite capture active'
    },
    
    # Energy choices (slot 6)
    'Standard energy': {
        'name': 'Grid Energy',
        'description': 'Standard electricity from the national grid.',
        'cost': '$0.40/kWh',
        'carbon': '250 gCO₂/kWh',
        'renewable': False
    },
    'Green energy': {
        'name': 'Green Energy',
        'description': 'Renewable electricity from wind and solar origin. More expensive but significantly reduced carbon emissions.',
        'cost': '$0.45/kWh',
        'carbon': '50 gCO₂/kWh',
        'renewable': True
    },
    
    # Medicine cups (slot 7)
    'Reusable dispensing cup': {
        'name': 'Reusable cup',
        'description': 'Plastic medicine cups. Sterilised and reused each day.',
        'cost': '$0.25 per patient/day',
        'carbon': '9.2 gCO₂ per use'
    },
    'Single use dispensing cup': {
        'name': 'Single use cup',
        'description': 'Disposable dispensing cup.',
        'cost': '$0.50 per patient/day',
        'carbon': '13.3 gCO₂ per use'
    },
    
    # Deprescribing (slot 8)
    'Prescribe as required': {
        'name': 'Standard Prescribing',
        'description': 'Maximises treatment but may include patients with marginal benefit.',
        'patients': '60 patients'
    },
    'Deprescribing Program': {
        'name': 'Deprescribing Program',
        'description': 'Patient medicines are reviewed and optimised. Medication is discontinued where benefits are small or interfere with other treatments.',
        'patients': '52 patients'
    },
    
    # Procurement policy (slot 9)
    'No procurement rules': {
        'name': 'Free Market',
        'description': 'Open procurement based primarily on price. The hospital will pay 90 EUR/day for this medicine.',
        'price_cap': '$90/day'
    },
    'Bio-procurement': {
        'name': 'Biopreference Policy',
        'description': 'Procurement favoring biodegradable pharmaceuticals. Requires ≥50% API biodegradation. Higher price cap (120 EUR/day) subsidised by the government to support green chemistry.',
        'price_cap': '$120/day',
        'requirements': 'Biodeg ≥50%'
    },
    'Sustainable procurement': {
        'name': 'Sustainable certified',
        'description': 'Products must meet a carbon footprint target which is adjusted for performance (efficacy). Small price premium (100 EUR/day).',
        'price_cap': '$100/day',
        'requirements': 'CO₂ ≤ target'
    },
    
    # Pollution standards (slot 10)
    'No water quality standards': {
        'name': 'No Standards',
        'description': 'No regulatory limits on water pollution. May harm public health and the environment.',
        'limit': 'Unlimited',
        'penalty': '$0/day'
    },
    'Lenient water quality standards': {
        'name': 'Basic Standards',
        'description': 'Moderate pollution limits (4 g/day total) reflects growing environmental concerns. Violations incur a 40 EUR/day fine.',
        'limit': '0.2 g/day',
        'penalty': '$40/day if exceeded'
    },
    'Strict water quality standards': {
        'name': 'Strict Standards',
        'description': 'Stringent pollution controls (2 g/day) to protect sensitive aquatic ecosystems. Requires advanced treatment of wastes.',
        'limit': '0.05 g/day',
        'penalty': '$40/day if exceeded'
    },
    
    # Biodegradation standards (slot 11)
    'Biodegradation standard': {
        'name': 'Biodegradation Required',
        'description': 'Mandated minimum biodegradability to reduce environmental persistence.',
        'threshold': '≥50% for API'
    },
    'No biodegradation standard': {
        'name': 'No Requirements',
        'description': 'No biodegradability standards. Allows use of persistent pharmaceuticals that accumulate in the environment.',
        'threshold': 'None'
    },

    # Temperature (slot 12) - these are numeric values, describe the concept
    'reaction_temperature': {
        'name': 'Reaction Temperature',
        'description': 'Higher temperatures speed up reactions but require more energy.',
        'range': '25-100°C'
    },
    
    # Duration (slot 13) - these are numeric values, describe the concept
    'reaction_hours': {
        'name': 'Reaction Duration',
        'description': 'Longer reaction times increase conversion but consume more energy.',
        'range': '1-8 hours'
    },
}

def get_item_description(monster_name):
    """Get description for a single item choice"""
    return ITEM_DESCRIPTIONS.get(monster_name, {
        'name': monster_name,
        'description': 'No description available.',
    })

def get_drug_description(drug_code):
    """Get description for a drug code combination"""
    # Try exact match first
    if drug_code in DRUG_CODE_DESCRIPTIONS:
        return DRUG_CODE_DESCRIPTIONS[drug_code]
    
    # Generate generic description based on pattern
    count_a = drug_code.count('A')
    count_b = drug_code.count('B')
    count_c = drug_code.count('C')
    
    if count_a == 4:
        return DRUG_CODE_DESCRIPTIONS['AAAA']
    elif count_b == 4:
        return DRUG_CODE_DESCRIPTIONS['BBBB']
    elif count_c == 4:
        return DRUG_CODE_DESCRIPTIONS['CCCC']
    else:
        # Mixed compound
        return {
            'name': f'Compound {drug_code}',
            'description': f'A custom formulation combining {count_a} Type-A, {count_b} Type-B, and {count_c} Type-C molecular fragments. Properties vary based on specific combination.'
        }