from settings import *
import math


# ===== GAME CONSTANTS =====

# Energy costs and emissions
green_energy_gwp = 50  # gCO2 per kWh
normal_energy_gwp = 250  # gCO2 per kWh
cost_green_energy = 0.45  # $ per kWh
cost_normal_energy = 0.40  # $ per kWh

# Safety equipment costs
cost_no_safety = 0  # $ per day
cost_basic_safety = 5  # $ per day
cost_vent_safety = 15  # $ per day
cost_closed_safety = 75  # $ per day

# Waste management costs
cost_solid_waste = 0.4  # $ per day
cost_waste = 0  # $ per day
cost_minor_treatment = 0.05  # $ per day
cost_major_treatment = 0.75  # $ per day

# Factory emissions
factory_api_emissions = 0.02  # g/g
factory_api_emissions_minor_treatment = 0.005
factory_api_emissions_major_treatment = 0.02
factory_meta_emissions = 0
factory_meta_emissions_minor_treatment = 0
factory_meta_emissions_major_treatment = 0.005

# Hospital emissions
hospital_api_emissions = 0  # g/g
hospital_meta_emissions = 1

# Medicine cup costs and emissions
cost_cup1 = 0.25  # $ per day
cost_cup2 = 0.5  # $ per day
gwp_cup1 = 9.2  # g CO2 per use
gwp_cup2 = 13.3  # g CO2 per use

# Patient numbers
total_patients = 60
total_patient_deprescribe = 52

# Price caps
price_cap_free = 90  # $ per day
price_cap_pwes = 100  # $ per day
price_cap_biopref = 120  # $ per day

# Pollution limits
pollution_limit_none = 1000000
pollution_limit_basic = 4
pollution_limit_harsh = 2
penalty_basic = 40
penalty_harsh = 40

# Biodegradation targets
biodeg_target_none = 0.0
biodeg_target_biopref = 0.7

# PWES (Pharmaceutical Waste Emission System)
pwes_alloc = 50000000
pwes_demand = 1000000




# ===== MOLECULE STATISTICS DATABASE =====
# Each molecule code (e.g., 'AAAA') represents a different drug formulation

molecule_stats = {
    'AAAA': {'waste': 7.1,  'impact': 178, 'cost': 4.04, 'efficacy': 2.7,  'biodegAPI': 0.429, 'toxAPI': 1,     'biodegMeta': 0.517, 'toxMeta': 0.61,  'exposureNo': 20,     'exposureBasic': 5,     'exposureVent': 2,     'exposureClosed': 0.1,   'rateConst': 0.000087, 'biobased': 0.271},
    'AAAB': {'waste': 7.6,  'impact': 169, 'cost': 4.06, 'efficacy': 3.14, 'biodegAPI': 0.543, 'toxAPI': 0.399, 'biodegMeta': 0.655, 'toxMeta': 0.06,  'exposureNo': 7.98,   'exposureBasic': 1.995, 'exposureVent': 0.798, 'exposureClosed': 0.04,  'rateConst': 0.000091, 'biobased': 0.234},
    'AAAC': {'waste': 8.8,  'impact': 159, 'cost': 4.08, 'efficacy': 2.48, 'biodegAPI': 0.5,   'toxAPI': 0.421, 'biodegMeta': 0.621, 'toxMeta': 0.082, 'exposureNo': 8.425,  'exposureBasic': 2.106, 'exposureVent': 0.843, 'exposureClosed': 0.042, 'rateConst': 0.000101, 'biobased': 0.538},
    'AABA': {'waste': 7.68, 'impact': 138, 'cost': 3.74, 'efficacy': 2.74, 'biodegAPI': 0.443, 'toxAPI': 0.816, 'biodegMeta': 0.517, 'toxMeta': 0.577, 'exposureNo': 16.327, 'exposureBasic': 4.082, 'exposureVent': 1.633, 'exposureClosed': 0.082, 'rateConst': 0.000107, 'biobased': 0.385},
    'AABB': {'waste': 8.18, 'impact': 129, 'cost': 3.76, 'efficacy': 3.18, 'biodegAPI': 0.557, 'toxAPI': 0.215, 'biodegMeta': 0.655, 'toxMeta': 0.026, 'exposureNo': 4.307,  'exposureBasic': 1.077, 'exposureVent': 0.431, 'exposureClosed': 0.022, 'rateConst': 0.000111, 'biobased': 0.328},
    'AABC': {'waste': 9.38, 'impact': 119, 'cost': 3.78, 'efficacy': 2.52, 'biodegAPI': 0.514, 'toxAPI': 0.238, 'biodegMeta': 0.621, 'toxMeta': 0.048, 'exposureNo': 4.752,  'exposureBasic': 1.188, 'exposureVent': 0.475, 'exposureClosed': 0.024, 'rateConst': 0.000121, 'biobased': 0.635},
    'AACA': {'waste': 6.6,  'impact': 143, 'cost': 3.72, 'efficacy': 3.08, 'biodegAPI': 0.457, 'toxAPI': 0.95,  'biodegMeta': 0.552, 'toxMeta': 0.594, 'exposureNo': 18.998, 'exposureBasic': 4.75,  'exposureVent': 1.9,   'exposureClosed': 0.095, 'rateConst': 0.000157, 'biobased': 0.276},
    'AACB': {'waste': 7.1,  'impact': 134, 'cost': 3.74, 'efficacy': 3.52, 'biodegAPI': 0.571, 'toxAPI': 0.349, 'biodegMeta': 0.69,  'toxMeta': 0.043, 'exposureNo': 6.978,  'exposureBasic': 1.745, 'exposureVent': 0.698, 'exposureClosed': 0.035, 'rateConst': 0.000161, 'biobased': 0.238},
    'AACC': {'waste': 8.3,  'impact': 124, 'cost': 3.76, 'efficacy': 2.86, 'biodegAPI': 0.529, 'toxAPI': 0.371, 'biodegMeta': 0.655, 'toxMeta': 0.065, 'exposureNo': 7.423,  'exposureBasic': 1.856, 'exposureVent': 0.742, 'exposureClosed': 0.037, 'rateConst': 0.000171, 'biobased': 0.544},
    'ABAA': {'waste': 5.58, 'impact': 156, 'cost': 3.16, 'efficacy': 2.57, 'biodegAPI': 0.543, 'toxAPI': 0.75,  'biodegMeta': 0.724, 'toxMeta': 0.56, 'exposureNo': 14.992,  'exposureBasic': 3.748, 'exposureVent': 1.499, 'exposureClosed': 0.075, 'rateConst': 0.000292, 'biobased': 0.471},
    'ABAB': {'waste': 5.94, 'impact': 143, 'cost': 3.22, 'efficacy': 3,    'biodegAPI': 0.686, 'toxAPI': 0.194, 'biodegMeta': 0.862, 'toxMeta': 0.009, 'exposureNo': 3.873,  'exposureBasic': 0.968, 'exposureVent': 0.387, 'exposureClosed': 0.019, 'rateConst': 0.000246, 'biobased': 0.412},
    'ABAC': {'waste': 6.72, 'impact': 133, 'cost': 3.28, 'efficacy': 2.33, 'biodegAPI': 0.629, 'toxAPI': 0.216, 'biodegMeta': 0.828, 'toxMeta': 0.032, 'exposureNo': 4.318,  'exposureBasic': 1.08,  'exposureVent': 0.432, 'exposureClosed': 0.022, 'rateConst': 0.000256, 'biobased': 0.667},
    'ABBA': {'waste': 6.16, 'impact': 116, 'cost': 2.86, 'efficacy': 2.61, 'biodegAPI': 0.557, 'toxAPI': 0.566, 'biodegMeta': 0.724, 'toxMeta': 0.527, 'exposureNo': 11.319, 'exposureBasic': 2.83,  'exposureVent': 1.132, 'exposureClosed': 0.057, 'rateConst': 0.000312, 'biobased': 0.599},
    'ABBB': {'waste': 6.52, 'impact': 103, 'cost': 2.92, 'efficacy': 3.04, 'biodegAPI': 0.7,   'toxAPI': 0.01,  'biodegMeta': 0.862, 'toxMeta': -0.024, 'exposureNo': 0.2,   'exposureBasic': 0.05,  'exposureVent': 0.02,  'exposureClosed': 0.001, 'rateConst': 0.000266, 'biobased': 0.516},
    'ABBC': {'waste': 7.3,  'impact': 93,  'cost': 2.98, 'efficacy': 2.37, 'biodegAPI': 0.643, 'toxAPI': 0.032, 'biodegMeta': 0.828, 'toxMeta': -0.002, 'exposureNo': 0.646, 'exposureBasic': 0.161, 'exposureVent': 0.065, 'exposureClosed': 0.003, 'rateConst': 0.000276, 'biobased': 0.769},
    'ABCA': {'waste': 5.08, 'impact': 121, 'cost': 2.84, 'efficacy': 2.95, 'biodegAPI': 0.571, 'toxAPI': 0.699, 'biodegMeta': 0.759, 'toxMeta': 0.544, 'exposureNo': 13.99,  'exposureBasic': 3.497, 'exposureVent': 1.399, 'exposureClosed': 0.07,  'rateConst': 0.000362, 'biobased': 0.479},
    'ABCB': {'waste': 5.44, 'impact': 108, 'cost': 2.9,  'efficacy': 3.38, 'biodegAPI': 0.714, 'toxAPI': 0.144, 'biodegMeta': 0.897, 'toxMeta': -0.007, 'exposureNo': 2.871, 'exposureBasic': 0.718, 'exposureVent': 0.287, 'exposureClosed': 0.014, 'rateConst': 0.000316, 'biobased': 0.418},
    'ABCC': {'waste': 6.22, 'impact': 98,  'cost': 2.96, 'efficacy': 2.71, 'biodegAPI': 0.657, 'toxAPI': 0.166, 'biodegMeta': 0.862, 'toxMeta': 0.015, 'exposureNo': 3.317,  'exposureBasic': 0.829, 'exposureVent': 0.332, 'exposureClosed': 0.017, 'rateConst': 0.000326, 'biobased': 0.675},
    'ACAA': {'waste': 7.44, 'impact': 139, 'cost': 2.9,  'efficacy': 2.44, 'biodegAPI': 0.529, 'toxAPI': 0.866, 'biodegMeta': 0.552, 'toxMeta': 0.588, 'exposureNo': 17.329, 'exposureBasic': 4.332, 'exposureVent': 1.733, 'exposureClosed': 0.087, 'rateConst': 0.000102, 'biobased': 0.098},
    'ACAB': {'waste': 7.82, 'impact': 132, 'cost': 2.94, 'efficacy': 2.86, 'biodegAPI': 0.729, 'toxAPI': 0.29,  'biodegMeta': 0.69,  'toxMeta': 0.037, 'exposureNo': 5.81,   'exposureBasic': 1.452, 'exposureVent': 0.581, 'exposureClosed': 0.029, 'rateConst': 0.000106, 'biobased': 0.086},
    'ACAC': {'waste': 8.66, 'impact': 122, 'cost': 2.98, 'efficacy': 2.18, 'biodegAPI': 0.643, 'toxAPI': 0.313, 'biodegMeta': 0.655, 'toxMeta': 0.06, 'exposureNo': 6.255,   'exposureBasic': 1.564, 'exposureVent': 0.625, 'exposureClosed': 0.031, 'rateConst': 0.000116, 'biobased': 0.395},
    'ACBA': {'waste': 8.02, 'impact': 99,  'cost': 2.6,  'efficacy': 2.48, 'biodegAPI': 0.543, 'toxAPI': 0.683, 'biodegMeta': 0.552, 'toxMeta': 0.555, 'exposureNo': 13.656, 'exposureBasic': 3.414, 'exposureVent': 1.366, 'exposureClosed': 0.068, 'rateConst': 0.000122, 'biobased': 0.181},
    'ACBB': {'waste': 8.4,  'impact': 92,  'cost': 2.64, 'efficacy': 2.9,  'biodegAPI': 0.743, 'toxAPI': 0.107, 'biodegMeta': 0.69,  'toxMeta': 0.004, 'exposureNo': 2.137,  'exposureBasic': 0.534, 'exposureVent': 0.214, 'exposureClosed': 0.011, 'rateConst': 0.000126, 'biobased': 0.156},
    'ACBC': {'waste': 9.24, 'impact': 82,  'cost': 2.68, 'efficacy': 2.22, 'biodegAPI': 0.657, 'toxAPI': 0.129, 'biodegMeta': 0.655, 'toxMeta': 0.026, 'exposureNo': 2.582,  'exposureBasic': 0.646, 'exposureVent': 0.258, 'exposureClosed': 0.013, 'rateConst': 0.000136, 'biobased': 0.475},
    'ACCA': {'waste': 6.94, 'impact': 104, 'cost': 2.58, 'efficacy': 2.82, 'biodegAPI': 0.557, 'toxAPI': 0.816, 'biodegMeta': 0.586, 'toxMeta': 0.572, 'exposureNo': 16.327, 'exposureBasic': 4.082, 'exposureVent': 1.633, 'exposureClosed': 0.082, 'rateConst': 0.000172, 'biobased': 0.099},
    'ACCB': {'waste': 7.32, 'impact': 97,  'cost': 2.62, 'efficacy': 3.24, 'biodegAPI': 0.757, 'toxAPI': 0.24,  'biodegMeta': 0.724, 'toxMeta': 0.021, 'exposureNo': 4.808,  'exposureBasic': 1.202, 'exposureVent': 0.481, 'exposureClosed': 0.024, 'rateConst': 0.000176, 'biobased': 0.087},
    'ACCC': {'waste': 8.16, 'impact': 87,  'cost': 2.66, 'efficacy': 2.56, 'biodegAPI': 0.671, 'toxAPI': 0.263, 'biodegMeta': 0.69,  'toxMeta': 0.043, 'exposureNo': 5.253,  'exposureBasic': 1.313, 'exposureVent': 0.525, 'exposureClosed': 0.026, 'rateConst': 0.000186, 'biobased': 0.4},
    'BAAA': {'waste': 4.6,  'impact': 130, 'cost': 3.54, 'efficacy': 2.98, 'biodegAPI': 0.457, 'toxAPI': 0.699, 'biodegMeta': 0.586, 'toxMeta': 0.633, 'exposureNo': 13.99,  'exposureBasic': 3.497, 'exposureVent': 1.399, 'exposureClosed': 0.07,  'rateConst': 0.000065, 'biobased': 0.393},
    'BAAB': {'waste': 5.1,  'impact': 121, 'cost': 3.56, 'efficacy': 3.42, 'biodegAPI': 0.571, 'toxAPI': 0.098, 'biodegMeta': 0.724, 'toxMeta': 0.082, 'exposureNo': 1.97,   'exposureBasic': 0.492, 'exposureVent': 0.197, 'exposureClosed': 0.01,  'rateConst': 0.000069, 'biobased': 0.345},
    'BAAC': {'waste': 6.3,  'impact': 111, 'cost': 3.58, 'efficacy': 2.76, 'biodegAPI': 0.529, 'toxAPI': 0.121, 'biodegMeta': 0.69,  'toxMeta': 0.104, 'exposureNo': 2.415,  'exposureBasic': 0.604, 'exposureVent': 0.242, 'exposureClosed': 0.012, 'rateConst': 0.000079, 'biobased': 0.603},
    'BABA': {'waste': 5.25, 'impact': 102, 'cost': 3.24, 'efficacy': 2.99, 'biodegAPI': 0.471, 'toxAPI': 0.661, 'biodegMeta': 0.586, 'toxMeta': 0.599, 'exposureNo': 13.222, 'exposureBasic': 3.306, 'exposureVent': 1.322, 'exposureClosed': 0.066, 'rateConst': 0.000069, 'biobased': 0.505},
    'BABB': {'waste': 5.75, 'impact': 93,  'cost': 3.26, 'efficacy': 3.43, 'biodegAPI': 0.586, 'toxAPI': 0.06,  'biodegMeta': 0.724, 'toxMeta': 0.048, 'exposureNo': 1.202,  'exposureBasic': 0.301, 'exposureVent': 0.12,  'exposureClosed': 0.006, 'rateConst': 0.000073, 'biobased': 0.438},
    'BABC': {'waste': 6.95, 'impact': 83,  'cost': 3.28, 'efficacy': 2.77, 'biodegAPI': 0.543, 'toxAPI': 0.082, 'biodegMeta': 0.69,  'toxMeta': 0.071, 'exposureNo': 1.647,  'exposureBasic': 0.412, 'exposureVent': 0.165, 'exposureClosed': 0.008, 'rateConst': 0.000083, 'biobased': 0.698},
    'BACA': {'waste': 4.1,  'impact': 111, 'cost': 3.08, 'efficacy': 3.35, 'biodegAPI': 0.486, 'toxAPI': 0.682, 'biodegMeta': 0.621, 'toxMeta': 0.616, 'exposureNo': 13.634, 'exposureBasic': 3.408, 'exposureVent': 1.363, 'exposureClosed': 0.068, 'rateConst': 0.000087, 'biobased': 0.399},
    'BACB': {'waste': 4.6,  'impact': 102, 'cost': 3.1,  'efficacy': 3.79, 'biodegAPI': 0.6,   'toxAPI': 0.081, 'biodegMeta': 0.759, 'toxMeta': 0.065, 'exposureNo': 1.614,  'exposureBasic': 0.403, 'exposureVent': 0.161, 'exposureClosed': 0.008, 'rateConst': 0.000091, 'biobased': 0.35},
    'BACC': {'waste': 5.8,  'impact': 92,  'cost': 3.12, 'efficacy': 3.13, 'biodegAPI': 0.557, 'toxAPI': 0.103, 'biodegMeta': 0.724, 'toxMeta': 0.087, 'exposureNo': 2.059,  'exposureBasic': 0.515, 'exposureVent': 0.206, 'exposureClosed': 0.01,  'rateConst': 0.000101, 'biobased': 0.61},
    'BBAA': {'waste': 3.57, 'impact': 100, 'cost': 2.94, 'efficacy': 2.84, 'biodegAPI': 0.571, 'toxAPI': 0.594, 'biodegMeta': 0.793, 'toxMeta': 0.583, 'exposureNo': 11.886, 'exposureBasic': 2.972, 'exposureVent': 1.189, 'exposureClosed': 0.059, 'rateConst': 0.00019,  'biobased': 0.565},
    'BBAB': {'waste': 3.93, 'impact': 87,  'cost': 3,    'efficacy': 3.27, 'biodegAPI': 0.714, 'toxAPI': 0.038, 'biodegMeta': 0.931, 'toxMeta': 0.032, 'exposureNo': 0.768,  'exposureBasic': 0.192, 'exposureVent': 0.077, 'exposureClosed': 0.004, 'rateConst': 0.000144, 'biobased': 0.5},
    'BBAC': {'waste': 4.71, 'impact': 77,  'cost': 3.06, 'efficacy': 2.6,  'biodegAPI': 0.657, 'toxAPI': 0.061, 'biodegMeta': 0.897, 'toxMeta': 0.054, 'exposureNo': 1.213,  'exposureBasic': 0.303, 'exposureVent': 0.121, 'exposureClosed': 0.006, 'rateConst': 0.000154, 'biobased': 0.72},
    'BBBA': {'waste': 4.22, 'impact': 72,  'cost': 2.64, 'efficacy': 2.85, 'biodegAPI': 0.586, 'toxAPI': 0.556, 'biodegMeta': 0.793, 'toxMeta': 0.549, 'exposureNo': 11.119, 'exposureBasic': 2.78,  'exposureVent': 1.112, 'exposureClosed': 0.056, 'rateConst': 0.000194, 'biobased': 0.687},
    'BBBB': {'waste': 4.58, 'impact': 59,  'cost': 2.7,  'efficacy': 3.28, 'biodegAPI': 0.729, 'toxAPI': 0,     'biodegMeta': 0.931, 'toxMeta': -0.002, 'exposureNo': 0,     'exposureBasic': 0,     'exposureVent': 0,     'exposureClosed': 0,     'rateConst': 0.000148, 'biobased': 0.601},
    'BBBC': {'waste': 5.36, 'impact': 49,  'cost': 2.76, 'efficacy': 2.61, 'biodegAPI': 0.671, 'toxAPI': 0.022, 'biodegMeta': 0.897, 'toxMeta': 0.021, 'exposureNo': 0.445,  'exposureBasic': 0.111, 'exposureVent': 0.045, 'exposureClosed': 0.002, 'rateConst': 0.000158, 'biobased': 0.818},
    'BBCA': {'waste': 3.07, 'impact': 81,  'cost': 2.48, 'efficacy': 3.21, 'biodegAPI': 0.6,   'toxAPI': 0.577, 'biodegMeta': 0.828, 'toxMeta': 0.566, 'exposureNo': 11.53,  'exposureBasic': 2.883, 'exposureVent': 1.153, 'exposureClosed': 0.058, 'rateConst': 0.000212, 'biobased': 0.573},
    'BBCB': {'waste': 3.43, 'impact': 68,  'cost': 2.54, 'efficacy': 3.64, 'biodegAPI': 0.743, 'toxAPI': 0.021, 'biodegMeta': 0.966, 'toxMeta': 0.015, 'exposureNo': 0.412,  'exposureBasic': 0.103, 'exposureVent': 0.041, 'exposureClosed': 0.002, 'rateConst': 0.000166, 'biobased': 0.507},
    'BBCC': {'waste': 4.21, 'impact': 58,  'cost': 2.6,  'efficacy': 2.97, 'biodegAPI': 0.686, 'toxAPI': 0.043, 'biodegMeta': 0.931, 'toxMeta': 0.037, 'exposureNo': 0.857,  'exposureBasic': 0.214, 'exposureVent': 0.086, 'exposureClosed': 0.004, 'rateConst': 0.000176, 'biobased': 0.728},
    'BCAA': {'waste': 5.36, 'impact': 95,  'cost': 2.54, 'efficacy': 2.7,  'biodegAPI': 0.557, 'toxAPI': 0.647, 'biodegMeta': 0.621, 'toxMeta': 0.61, 'exposureNo': 12.933,  'exposureBasic': 3.233, 'exposureVent': 1.293, 'exposureClosed': 0.065, 'rateConst': 0.00008,  'biobased': 0.227},
    'BCAB': {'waste': 5.74, 'impact': 88,  'cost': 2.58, 'efficacy': 3.12, 'biodegAPI': 0.757, 'toxAPI': 0.071, 'biodegMeta': 0.759, 'toxMeta': 0.06, 'exposureNo': 1.413,   'exposureBasic': 0.353, 'exposureVent': 0.141, 'exposureClosed': 0.007, 'rateConst': 0.000084, 'biobased': 0.201},
    'BCAC': {'waste': 6.58, 'impact': 78,  'cost': 2.62, 'efficacy': 2.44, 'biodegAPI': 0.671, 'toxAPI': 0.093, 'biodegMeta': 0.724, 'toxMeta': 0.082, 'exposureNo': 1.859,  'exposureBasic': 0.465, 'exposureVent': 0.186, 'exposureClosed': 0.009, 'rateConst': 0.000094, 'biobased': 0.468},
    'BCBA': {'waste': 6.01, 'impact': 67,  'cost': 2.24, 'efficacy': 2.71, 'biodegAPI': 0.571, 'toxAPI': 0.608, 'biodegMeta': 0.621, 'toxMeta': 0.577, 'exposureNo': 12.165, 'exposureBasic': 3.041, 'exposureVent': 1.216, 'exposureClosed': 0.061, 'rateConst': 0.000084, 'biobased': 0.313},
    'BCBB': {'waste': 6.39, 'impact': 60,  'cost': 2.28, 'efficacy': 3.13, 'biodegAPI': 0.771, 'toxAPI': 0.032, 'biodegMeta': 0.759, 'toxMeta': 0.026, 'exposureNo': 0.646,  'exposureBasic': 0.161, 'exposureVent': 0.065, 'exposureClosed': 0.003, 'rateConst': 0.000088, 'biobased': 0.275},
    'BCBC': {'waste': 7.23, 'impact': 50,  'cost': 2.32, 'efficacy': 2.45, 'biodegAPI': 0.686, 'toxAPI': 0.055, 'biodegMeta': 0.724, 'toxMeta': 0.048, 'exposureNo': 1.091,  'exposureBasic': 0.273, 'exposureVent': 0.109, 'exposureClosed': 0.005, 'rateConst': 0.000098, 'biobased': 0.546},
    'BCCA': {'waste': 4.86, 'impact': 76,  'cost': 2.08, 'efficacy': 3.07, 'biodegAPI': 0.586, 'toxAPI': 0.629, 'biodegMeta': 0.655, 'toxMeta': 0.594, 'exposureNo': 12.577, 'exposureBasic': 3.144, 'exposureVent': 1.258, 'exposureClosed': 0.063, 'rateConst': 0.000102, 'biobased': 0.23},
    'BCCB': {'waste': 5.24, 'impact': 69,  'cost': 2.12, 'efficacy': 3.49, 'biodegAPI': 0.786, 'toxAPI': 0.053, 'biodegMeta': 0.793, 'toxMeta': 0.043, 'exposureNo': 1.057,  'exposureBasic': 0.264, 'exposureVent': 0.106, 'exposureClosed': 0.005, 'rateConst': 0.000106, 'biobased': 0.204},
    'BCCC': {'waste': 6.08, 'impact': 59,  'cost': 2.16, 'efficacy': 2.81, 'biodegAPI': 0.7,   'toxAPI': 0.075, 'biodegMeta': 0.759, 'toxMeta': 0.065, 'exposureNo': 1.503,  'exposureBasic': 0.376, 'exposureVent': 0.15,  'exposureClosed': 0.008, 'rateConst': 0.000116, 'biobased': 0.473},
    'CAAA': {'waste': 5.2,  'impact': 147, 'cost': 3.34, 'efficacy': 2.62, 'biodegAPI': 0.557, 'toxAPI': 0.827, 'biodegMeta': 0.621, 'toxMeta': 0.661, 'exposureNo': 16.55,  'exposureBasic': 4.137, 'exposureVent': 1.655, 'exposureClosed': 0.083, 'rateConst': 0.000117, 'biobased': 0.668},
    'CAAB': {'waste': 5.7,  'impact': 138, 'cost': 3.36, 'efficacy': 3.06, 'biodegAPI': 0.671, 'toxAPI': 0.226, 'biodegMeta': 0.759, 'toxMeta': 0.11, 'exposureNo': 4.53,    'exposureBasic': 1.132, 'exposureVent': 0.453, 'exposureClosed': 0.023, 'rateConst': 0.000121, 'biobased': 0.592},
    'CAAC': {'waste': 6.9,  'impact': 128, 'cost': 3.38, 'efficacy': 2.4,  'biodegAPI': 0.629, 'toxAPI': 0.249, 'biodegMeta': 0.724, 'toxMeta': 0.132, 'exposureNo': 4.975,  'exposureBasic': 1.244, 'exposureVent': 0.497, 'exposureClosed': 0.025, 'rateConst': 0.000131, 'biobased': 0.793},
    'CABA': {'waste': 5.88, 'impact': 116, 'cost': 3.04, 'efficacy': 2.54, 'biodegAPI': 0.6,   'toxAPI': 0.744, 'biodegMeta': 0.621, 'toxMeta': 0.627, 'exposureNo': 14.88,  'exposureBasic': 3.72,  'exposureVent': 1.488, 'exposureClosed': 0.074, 'rateConst': 0.000137, 'biobased': 0.798},
    'CABB': {'waste': 6.38, 'impact': 107, 'cost': 3.06, 'efficacy': 2.98, 'biodegAPI': 0.714, 'toxAPI': 0.143, 'biodegMeta': 0.759, 'toxMeta': 0.076, 'exposureNo': 2.86,   'exposureBasic': 0.715, 'exposureVent': 0.286, 'exposureClosed': 0.014, 'rateConst': 0.000141, 'biobased': 0.7},
    'CABC': {'waste': 7.58, 'impact': 97,  'cost': 3.08, 'efficacy': 2.32, 'biodegAPI': 0.671, 'toxAPI': 0.165, 'biodegMeta': 0.724, 'toxMeta': 0.098, 'exposureNo': 3.306,  'exposureBasic': 0.826, 'exposureVent': 0.331, 'exposureClosed': 0.017, 'rateConst': 0.000151, 'biobased': 0.895},
    'CACA': {'waste': 4.7,  'impact': 124, 'cost': 2.94, 'efficacy': 2.96, 'biodegAPI': 0.614, 'toxAPI': 0.8,   'biodegMeta': 0.655, 'toxMeta': 0.644, 'exposureNo': 15.993, 'exposureBasic': 3.998, 'exposureVent': 1.599, 'exposureClosed': 0.08,  'rateConst': 0.000187, 'biobased': 0.678},
    'CACB': {'waste': 5.2,  'impact': 115, 'cost': 2.96, 'efficacy': 3.4,  'biodegAPI': 0.729, 'toxAPI': 0.199, 'biodegMeta': 0.793, 'toxMeta': 0.093, 'exposureNo': 3.973,  'exposureBasic': 0.993, 'exposureVent': 0.397, 'exposureClosed': 0.02,  'rateConst': 0.000191, 'biobased': 0.6},
    'CACC': {'waste': 6.4,  'impact': 105, 'cost': 2.98, 'efficacy': 2.74, 'biodegAPI': 0.686, 'toxAPI': 0.221, 'biodegMeta': 0.759, 'toxMeta': 0.115, 'exposureNo': 4.418,  'exposureBasic': 1.105, 'exposureVent': 0.442, 'exposureClosed': 0.022, 'rateConst': 0.000201, 'biobased': 0.802},
    'CBAA': {'waste': 4.38, 'impact': 119, 'cost': 2.62, 'efficacy': 2.45, 'biodegAPI': 0.7,   'toxAPI': 0.677, 'biodegMeta': 0.828, 'toxMeta': 0.61, 'exposureNo': 13.545,  'exposureBasic': 3.386, 'exposureVent': 1.354, 'exposureClosed': 0.068, 'rateConst': 0.000322, 'biobased': 0.812},
    'CBAB': {'waste': 4.74, 'impact': 106, 'cost': 2.68, 'efficacy': 2.88, 'biodegAPI': 0.843, 'toxAPI': 0.121, 'biodegMeta': 0.966, 'toxMeta': 0.06, 'exposureNo': 2.426,   'exposureBasic': 0.607, 'exposureVent': 0.243, 'exposureClosed': 0.012, 'rateConst': 0.000276, 'biobased': 0.725},
    'CBAC': {'waste': 5.52, 'impact': 96,  'cost': 2.74, 'efficacy': 2.21, 'biodegAPI': 0.786, 'toxAPI': 0.144, 'biodegMeta': 0.931, 'toxMeta': 0.082, 'exposureNo': 2.871,  'exposureBasic': 0.718, 'exposureVent': 0.287, 'exposureClosed': 0.014, 'rateConst': 0.000286, 'biobased': 0.896},
    'CBBA': {'waste': 5.06, 'impact': 88,  'cost': 2.32, 'efficacy': 2.37, 'biodegAPI': 0.743, 'toxAPI': 0.594, 'biodegMeta': 0.828, 'toxMeta': 0.577, 'exposureNo': 11.875, 'exposureBasic': 2.969, 'exposureVent': 1.188, 'exposureClosed': 0.059, 'rateConst': 0.000342, 'biobased': 0.948},
    'CBBB': {'waste': 5.42, 'impact': 75,  'cost': 2.38, 'efficacy': 2.8,  'biodegAPI': 0.886, 'toxAPI': 0.038, 'biodegMeta': 0.966, 'toxMeta': 0.026, 'exposureNo': 0.757,  'exposureBasic': 0.189, 'exposureVent': 0.076, 'exposureClosed': 0.004, 'rateConst': 0.000296, 'biobased': 0.838},
    'CBBC': {'waste': 6.2,  'impact': 65,  'cost': 2.44, 'efficacy': 2.13, 'biodegAPI': 0.829, 'toxAPI': 0.06,  'biodegMeta': 0.931, 'toxMeta': 0.048, 'exposureNo': 1.202,  'exposureBasic': 0.301, 'exposureVent': 0.12,  'exposureClosed': 0.006, 'rateConst': 0.000306, 'biobased': 1},
    'CBCA': {'waste': 3.88, 'impact': 96,  'cost': 2.22, 'efficacy': 2.79, 'biodegAPI': 0.757, 'toxAPI': 0.649, 'biodegMeta': 0.862, 'toxMeta': 0.594, 'exposureNo': 12.988, 'exposureBasic': 3.247, 'exposureVent': 1.299, 'exposureClosed': 0.065, 'rateConst': 0.000392, 'biobased': 0.824},
    'CBCB': {'waste': 4.24, 'impact': 83,  'cost': 2.28, 'efficacy': 3.22, 'biodegAPI': 0.9,   'toxAPI': 0.093, 'biodegMeta': 1,     'toxMeta': 0.043, 'exposureNo': 1.87,   'exposureBasic': 0.467, 'exposureVent': 0.187, 'exposureClosed': 0.009, 'rateConst': 0.000346, 'biobased': 0.734},
    'CBCC': {'waste': 5.02, 'impact': 73,  'cost': 2.34, 'efficacy': 2.55, 'biodegAPI': 0.843, 'toxAPI': 0.116, 'biodegMeta': 0.966, 'toxMeta': 0.065, 'exposureNo': 2.315,  'exposureBasic': 0.579, 'exposureVent': 0.231, 'exposureClosed': 0.012, 'rateConst': 0.000356, 'biobased': 0.905},
    'CCAA': {'waste': 6.14, 'impact': 111, 'cost': 2.28, 'efficacy': 2.28, 'biodegAPI': 0.743, 'toxAPI': 0.75,  'biodegMeta': 0.655, 'toxMeta': 0.638, 'exposureNo': 14.992, 'exposureBasic': 3.748, 'exposureVent': 1.499, 'exposureClosed': 0.075, 'rateConst': 0.000132, 'biobased': 0.49},
    'CCAB': {'waste': 6.52, 'impact': 104, 'cost': 2.32, 'efficacy': 2.7,  'biodegAPI': 0.943, 'toxAPI': 0.174, 'biodegMeta': 0.793, 'toxMeta': 0.087, 'exposureNo': 3.472,  'exposureBasic': 0.868, 'exposureVent': 0.347, 'exposureClosed': 0.017, 'rateConst': 0.000136, 'biobased': 0.439},
    'CCAC': {'waste': 7.36, 'impact': 94,  'cost': 2.36, 'efficacy': 2.02, 'biodegAPI': 0.857, 'toxAPI': 0.196, 'biodegMeta': 0.759, 'toxMeta': 0.11, 'exposureNo': 3.918,   'exposureBasic': 0.979, 'exposureVent': 0.392, 'exposureClosed': 0.02,  'rateConst': 0.000146, 'biobased': 0.653},
    'CCBA': {'waste': 6.82, 'impact': 80,  'cost': 1.98, 'efficacy': 2.2,  'biodegAPI': 0.786, 'toxAPI': 0.666, 'biodegMeta': 0.655, 'toxMeta': 0.605, 'exposureNo': 13.322, 'exposureBasic': 3.331, 'exposureVent': 1.332, 'exposureClosed': 0.067, 'rateConst': 0.000152, 'biobased': 0.593},
    'CCBB': {'waste': 7.2,  'impact': 73,  'cost': 2.02, 'efficacy': 2.62, 'biodegAPI': 0.986, 'toxAPI': 0.09,  'biodegMeta': 0.793, 'toxMeta': 0.054, 'exposureNo': 1.803,  'exposureBasic': 0.451, 'exposureVent': 0.18,  'exposureClosed': 0.009, 'rateConst': 0.000156, 'biobased': 0.526},
    'CCBC': {'waste': 8.04, 'impact': 63,  'cost': 2.06, 'efficacy': 1.94, 'biodegAPI': 0.9,   'toxAPI': 0.112, 'biodegMeta': 0.759, 'toxMeta': 0.076, 'exposureNo': 2.248,  'exposureBasic': 0.562, 'exposureVent': 0.225, 'exposureClosed': 0.011, 'rateConst': 0.000166, 'biobased': 0.739},
    'CCCA': {'waste': 5.64, 'impact': 88,  'cost': 1.88, 'efficacy': 2.62, 'biodegAPI': 0.8,   'toxAPI': 0.722, 'biodegMeta': 0.69,  'toxMeta': 0.622, 'exposureNo': 14.435, 'exposureBasic': 3.609, 'exposureVent': 1.444, 'exposureClosed': 0.072, 'rateConst': 0.000202, 'biobased': 0.497},
    'CCCB': {'waste': 6.02, 'impact': 81,  'cost': 1.92, 'efficacy': 3.04, 'biodegAPI': 1,     'toxAPI': 0.146, 'biodegMeta': 0.828, 'toxMeta': 0.071, 'exposureNo': 2.916,  'exposureBasic': 0.729, 'exposureVent': 0.292, 'exposureClosed': 0.015, 'rateConst': 0.000206, 'biobased': 0.444},
    'CCCC': {'waste': 6.86, 'impact': 71,  'cost': 1.96, 'efficacy': 2.36, 'biodegAPI': 0.914, 'toxAPI': 0.168, 'biodegMeta': 0.793, 'toxMeta': 0.093, 'exposureNo': 3.361,  'exposureBasic': 0.84,  'exposureVent': 0.336, 'exposureClosed': 0.017, 'rateConst': 0.000216, 'biobased': 0.66}
}






def get_drug_code_from_choices(player_monsters):
    """
    Generate drug code (like 'AAAA', 'BBAC', etc.) from player monster choices.
    
    Args:
        player_monsters: Dictionary containing monster choices in slots 0-3
        
    Returns:
        Four-letter drug code string
    """
    molecule_to_letter = {
        'molecule_A1': 'A', 'molecule_A2': 'B', 'molecule_A3': 'C',
        'molecule_B1': 'A', 'molecule_B2': 'B', 'molecule_B3': 'C',
        'molecule_C1': 'A', 'molecule_C2': 'B', 'molecule_C3': 'C',
        'molecule_D1': 'A', 'molecule_D2': 'B', 'molecule_D3': 'C',
    }
    
    # Get the four molecule choices (slots 0-3)
    drug_code = ''
    for i in range(4):
        if i in player_monsters:
            monster_name = player_monsters[i].name
            drug_code += molecule_to_letter.get(monster_name, 'A')
        else:
            drug_code += 'A'  # Default to 'A' if slot is missing
    
    return drug_code


def get_reaction_parameters(player_monsters):
    """
    Extract temperature and duration from player choices.
    
    Args:
        player_monsters: Dictionary containing player choices
        
    Returns:
        tuple: (temperature in °C, duration in hours)
    """
    # Slots 12 and 13 store temperature and duration
    # The level attribute is used to store these values
    temperature = 75  # Default temperature in °C
    duration = 6  # Default duration in hours
    
    if 12 in player_monsters:
        temperature = player_monsters[12].level
    if 13 in player_monsters:
        duration = player_monsters[13].level
    
    return temperature, duration


def calculate_k(rate_const, temperature):
    """
    Calculate the reaction rate constant k at a given temperature.
    
    Args:
        rate_const: Base rate constant at 298K
        temperature: Temperature in Celsius
        
    Returns:
        Adjusted rate constant k
    """
    import math
    k = math.exp(math.log(rate_const) * (298 / (temperature + 273)))
    return k


def calculate_c_values(k, rxn_time):
    """
    Calculate c values for all conversion percentages.
    
    Args:
        k: Reaction rate constant
        rxn_time: Reaction time in hours
        
    Returns:
        Dictionary mapping conversion percentages to c values
    """
    # Conversion constants for each percentage
    conversion_constants = {
        5:  0.0000146103,
        10: 0.0000308427,
        15: 0.0000489833,
        20: 0.0000693894,
        25: 0.0000925135,
        30: 0.000118937,
        35: 0.00014942,
        40: 0.000184976,
        45: 0.000226984,
        50: 0.000277374,
        55: 0.000338932,
        60: 0.000415825,
        65: 0.000514591,
        70: 0.000646083,
        75: 0.000829738,
        80: 0.001104086,
        85: 0.001557601,
        90: 0.00244649,
        95: 0.004915626,
    }
    
    c_values = {}
    for percent, const in conversion_constants.items():
        c_values[percent] = (const / k) - rxn_time
    
    return c_values


def calculate_conversion(rate_const, temperature, rxn_time):
    """
    Calculate the conversion percentage based on reaction parameters.
    
    This mimics XLOOKUP(0, ABS(c5:c95), conversions, 0, 1) by finding
    the conversion with c value closest to 0.
    
    Args:
        rate_const: Base rate constant
        temperature: Temperature in Celsius
        rxn_time: Reaction time in hours
        
    Returns:
        Conversion percentage (5-95)
    """
    # Calculate k
    k = calculate_k(rate_const, temperature)
    
    # Calculate all c values
    c_values = calculate_c_values(k, rxn_time)
    
    # Find conversion with c value closest to 0
    min_abs_c = float('inf')
    conversion = 50  # Default
    
    for percent, c_value in c_values.items():
        abs_c = abs(c_value)
        if abs_c < min_abs_c:
            min_abs_c = abs_c
            conversion = percent
    
    return conversion


def get_conversion_from_player_choices(player_monsters):
    """
    Get the conversion percentage based on player's molecule and reaction choices.
    
    Args:
        player_monsters: Dictionary containing all player choices
        
    Returns:
        Conversion percentage (5-95)
    """
    # Get drug code and its stats
    drug_code = get_drug_code_from_choices(player_monsters)
    if drug_code not in molecule_stats:
        return 50  # Default if drug code not found
    
    rate_const = molecule_stats[drug_code]['rateConst']
    
    # Get reaction parameters
    temperature, rxn_time = get_reaction_parameters(player_monsters)
    
    # Calculate and return conversion
    return calculate_conversion(rate_const, temperature, rxn_time)


def calculate_doses_per_gram(efficacy):
    """
    Calculate doses per gram based on drug efficacy.
    
    Formula: 2 + ROUNDUP(3 * (efficacy - 1.94) / 1.85, 0)
    
    Args:
        efficacy: Drug efficacy value from molecule_stats
        
    Returns:
        Number of doses per gram (integer)
    """
    import math
    doses = 2 + math.ceil(3 * (efficacy - 1.94) / 1.85)
    return doses


def get_doses_per_gram_from_choices(player_monsters):
    """
    Get doses per gram based on player's molecule choices.
    
    Args:
        player_monsters: Dictionary containing all player choices
        
    Returns:
        Number of doses per gram (integer)
    """
    # Get drug code and its stats
    drug_code = get_drug_code_from_choices(player_monsters)
    if drug_code not in molecule_stats:
        return 2  # Default minimum doses
    
    efficacy = molecule_stats[drug_code]['efficacy']
    return calculate_doses_per_gram(efficacy)


def get_patient_count(player_monsters):
    """
    Get the number of patients based on deprescribing choice.
    
    Args:
        player_monsters: Dictionary containing all player choices
        
    Returns:
        Number of patients (60 if prescription1, 52 if prescription2)
    """
    # Slot 8 contains the deprescribing choice
    if 8 in player_monsters:
        prescription_type = player_monsters[8].name
        if prescription_type == 'Prescribe as required':
            return total_patients  # 60
        elif prescription_type == 'Deprescribing Program':
            return total_patient_deprescribe  # 52
    
    # Default to full patient count
    return total_patients


def calculate_factory_waste_per_gram(player_monsters):
    """
    Calculate factory waste per gram of API produced.
    
    Formula: waste + (1 / conversion)
    
    Args:
        player_monsters: Dictionary containing all player choices
        
    Returns:
        Factory waste per gram (float)
    
    Note: This formula may be refined later
    """
    # Get drug code and waste value
    drug_code = get_drug_code_from_choices(player_monsters)
    if drug_code not in molecule_stats:
        return 0  # Default
    
    waste = molecule_stats[drug_code]['waste']
    
    # Get conversion percentage
    conversion = get_conversion_from_player_choices(player_monsters)
    
    # Calculate waste: waste + (1 / conversion)
    # Note: conversion is a percentage, so we need to convert to decimal
    factory_waste = waste + (1 / (conversion / 100))
    
    return factory_waste


def calculate_factory_costs(player_monsters):
    """
    Calculate total factory costs per gram of API.
    
    Includes:
    - Base cost from molecule_stats
    - Solid waste disposal costs
    - Energy costs (varies with temperature and duration)
    
    Args:
        player_monsters: Dictionary containing all player choices
        
    Returns:
        Total factory cost per gram (float)
    """
    # Get drug code and base cost
    drug_code = get_drug_code_from_choices(player_monsters)
    if drug_code not in molecule_stats:
        return 0  # Default
    
    base_cost = molecule_stats[drug_code]['cost']
    
    # Get factory waste for solid waste cost
    factory_waste = calculate_factory_waste_per_gram(player_monsters)
    solid_waste_cost = cost_solid_waste * factory_waste
    
    # Get reaction parameters
    temperature, reaction_duration = get_reaction_parameters(player_monsters)
    
    # Calculate energy consumption (kWh per gram)
    # Formula: 0.001 * [(8 * (temp - 20)) + (1.33 * (temp - 20) * duration)]
    energy_factory = 0.001 * ((8 * (temperature - 20)) + (1.33 * (temperature - 20) * reaction_duration))
    
    # Determine energy type from player choice (slot 6)
    energy_type = 'normal'  # Default
    if 6 in player_monsters:
        energy_choice = player_monsters[6].name
        if energy_choice == 'Standard energy':
            energy_type = 'normal'
        elif energy_choice == 'Green energy':
            energy_type = 'green'
    
    # Calculate energy cost
    if energy_type == 'green':
        energy_cost = energy_factory * cost_green_energy
    else:
        energy_cost = energy_factory * cost_normal_energy
    
    # Total factory cost
    total_cost = base_cost + solid_waste_cost + energy_cost
    
    return total_cost


def calculate_factory_impact(player_monsters):
    """
    Calculate total factory impact (CO2 emissions) per gram of API.
    
    Includes:
    - Base impact from molecule_stats (gCO2 per gram)
    - Energy-related emissions (varies with energy type)
    
    Args:
        player_monsters: Dictionary containing all player choices
        
    Returns:
        Total factory impact in gCO2 per gram (float)
    """
    # Get drug code and base impact
    drug_code = get_drug_code_from_choices(player_monsters)
    if drug_code not in molecule_stats:
        return 0  # Default
    
    base_impact = molecule_stats[drug_code]['impact']
    
    # Get reaction parameters
    temperature, reaction_duration = get_reaction_parameters(player_monsters)
    
    # Calculate energy consumption (kWh per gram)
    # Formula: 0.001 * [(8 * (temp - 20)) + (1.33 * (temp - 20) * duration)]
    energy_factory = 0.001 * ((8 * (temperature - 20)) + (1.33 * (temperature - 20) * reaction_duration))
    
    # Determine energy type from player choice (slot 6)
    energy_type = 'normal'  # Default
    if 6 in player_monsters:
        energy_choice = player_monsters[6].name
        if energy_choice == 'Standard energy':
            energy_type = 'normal'
        elif energy_choice == 'Green energy':
            energy_type = 'green'
    
    # Calculate energy impact (convert kWh to gCO2)
    if energy_type == 'green':
        energy_impact = energy_factory * green_energy_gwp
    else:
        energy_impact = energy_factory * normal_energy_gwp
    
    # Total factory impact
    total_impact = base_impact + energy_impact
    
    return total_impact


def calculate_water_emissions(player_monsters):
    """
    Calculate water emissions of API and metabolites per gram of API.
    
    Includes:
    - Factory emissions (varies with treatment level)
    - Hospital emissions
    - Biodegradation effects
    
    Args:
        player_monsters: Dictionary containing all player choices
        
    Returns:
        Tuple of (api_emissions, metabolite_emissions) in g per gram of API
    """
    # Get drug code and biodegradation values
    drug_code = get_drug_code_from_choices(player_monsters)
    if drug_code not in molecule_stats:
        return 0, 0  # Default
    
    biodeg_api = molecule_stats[drug_code]['biodegAPI']
    biodeg_meta = molecule_stats[drug_code]['biodegMeta']
    
    # Determine factory emissions based on treatment level (slot 5)
    factory_api_emis = factory_api_emissions  # Default: emissions1
    factory_meta_emis = factory_meta_emissions
    
    if 5 in player_monsters:
        emissions_choice = player_monsters[5].name
        if emissions_choice == 'No wastewater treatment':
            factory_api_emis = factory_api_emissions  # 0.02
            factory_meta_emis = factory_meta_emissions  # 0
        elif emissions_choice == 'Basic water treatment':
            factory_api_emis = factory_api_emissions_minor_treatment  # 0.005
            factory_meta_emis = factory_meta_emissions_minor_treatment  # 0
        elif emissions_choice == 'Advanced water treatment':
            factory_api_emis = factory_api_emissions_major_treatment  # 0.02
            factory_meta_emis = factory_meta_emissions_major_treatment  # 0.005
    
    # Total raw API emissions (factory + hospital)
    raw_api_emissions = factory_api_emis + hospital_api_emissions
    
    # Total raw metabolite emissions (factory + hospital)
    raw_meta_emissions = factory_meta_emis + hospital_meta_emissions
    
    # Calculate final API emissions after biodegradation
    # API emissions = raw_api_emissions × (1 - biodegAPI)
    final_api_emissions = raw_api_emissions * (1 - biodeg_api)
    
    # Calculate final metabolite emissions after biodegradation
    # Metabolite emissions = [(API emissions × biodegAPI) + raw_meta_emissions] × (1 - biodegMeta)
    final_meta_emissions = ((raw_api_emissions * biodeg_api) + raw_meta_emissions) * (1 - biodeg_meta)
    
    return final_api_emissions, final_meta_emissions


def calculate_city_daily_costs(player_monsters):
    """
    Calculate total city-scale daily costs (not per gram).
    
    Includes:
    - Safety equipment costs (varies with safety level)
    - Medicine cup costs (varies with cup type × number of patients)
    - Regulatory fines (if pollution limits exceeded)
    
    Args:
        player_monsters: Dictionary containing all player choices
        
    Returns:
        Total daily cost in dollars per day (float)
    """
    # (1) Safety equipment costs - based on slot 4
    safety_cost = cost_basic_safety  # Default: safety1
    
    if 4 in player_monsters:
        safety_choice = player_monsters[4].name
        if safety_choice == 'Standard PPE':
            safety_cost = cost_basic_safety  # 5
        elif safety_choice == 'PPE and extra ventilation':
            safety_cost = cost_vent_safety  # 15
        elif safety_choice == 'No PPE':
            safety_cost = cost_no_safety  # 0
        elif safety_choice == 'Closed reactor system':
            safety_cost = cost_closed_safety  # 75
    
    # (2) Medicine cup costs - based on slot 7 and number of patients
    cup_cost_per_patient = cost_cup1  # Default: cup1
    
    if 7 in player_monsters:
        cup_choice = player_monsters[7].name
        if cup_choice == 'Reusable dispensing cup':
            cup_cost_per_patient = cost_cup1  # 0.25
        elif cup_choice == 'Single use dispensing cup':
            cup_cost_per_patient = cost_cup2  # 0.5
    
    # Get number of patients
    num_patients = get_patient_count(player_monsters)
    total_cup_cost = cup_cost_per_patient * num_patients
    
    # (3) Regulatory fines - calculate based on pollution compliance
    regulatory_fines = 0
    
    # Determine pollution policy (slot 10)
    pollution_policy = 'No water quality standards'  # Default: no limit
    if 10 in player_monsters:
        pollution_policy = player_monsters[10].name
    
    if pollution_policy == 'Lenient water quality standards':
        pollution_limit = pollution_limit_basic  # 4
    elif pollution_policy == 'Strict water quality standards':
        pollution_limit = pollution_limit_harsh  # 2
    else:  # pollution1
        pollution_limit = pollution_limit_none  # 1000000 (effectively no limit)
    
    # Calculate total pollution (scaled up)
    api_emis_per_g, meta_emis_per_g = calculate_water_emissions(player_monsters)
    doses_per_g = get_doses_per_gram_from_choices(player_monsters)
    scale_factor = num_patients / doses_per_g
    total_pollution = (api_emis_per_g + meta_emis_per_g) * scale_factor
    
    # Apply fine if limit exceeded
    if total_pollution > pollution_limit and pollution_limit < pollution_limit_none:
        regulatory_fines = penalty_basic  # 40
    
    # Total daily costs
    total_daily_cost = safety_cost + total_cup_cost + regulatory_fines
    
    return total_daily_cost


def calculate_cup_impact(player_monsters):
    """
    Calculate daily CO2 impact from medicine cups.
    
    Args:
        player_monsters: Dictionary containing all player choices
        
    Returns:
        Daily cup impact in gCO2 per day (float)
    """
    # Determine cup type from slot 7
    cup_gwp = gwp_cup1  # Default: cup1
    
    if 7 in player_monsters:
        cup_choice = player_monsters[7].name
        if cup_choice == 'Reusable dispensing cup':
            cup_gwp = gwp_cup1  # 9.2 gCO2 per use
        elif cup_choice == 'Single use dispensing cup':
            cup_gwp = gwp_cup2  # 13.3 gCO2 per use
    
    # Get number of patients
    num_patients = get_patient_count(player_monsters)
    
    # Total cup impact per day
    total_cup_impact = cup_gwp * num_patients
    
    return total_cup_impact


def calculate_worker_risk(player_monsters):
    """
    Calculate worker exposure risk based on safety equipment level.
    
    Args:
        player_monsters: Dictionary containing all player choices
        
    Returns:
        Tuple of (exposure_value, is_safe) where:
        - exposure_value: Worker exposure level (float)
        - is_safe: Boolean indicating if exposure is safe (True if <= 1)
    """
    # Get drug code and exposure values
    drug_code = get_drug_code_from_choices(player_monsters)
    if drug_code not in molecule_stats:
        return 0, True  # Default safe
    
    stats = molecule_stats[drug_code]
    
    # Determine exposure based on safety level (slot 4)
    exposure = stats['exposureBasic']  # Default: safety1
    
    if 4 in player_monsters:
        safety_choice = player_monsters[4].name
        if safety_choice == 'Standard PPE':
            exposure = stats['exposureBasic']  # Basic safety
        elif safety_choice == 'PPE and extra ventilation':
            exposure = stats['exposureVent']  # Ventilation
        elif safety_choice == 'No PPE':
            exposure = stats['exposureNo']  # No safety
        elif safety_choice == 'Closed reactor system':
            exposure = stats['exposureClosed']  # Closed system
    
    # Risk is too high if exposure > 1
    is_safe = exposure <= 1
    
    return exposure, is_safe


def calculate_ecotoxicity(player_monsters):
    """
    Calculate ecotoxicity based on water emissions and toxicity values.
    
    Formula: (final_api_emissions × toxAPI) + (final_meta_emissions × toxMeta)
    
    Args:
        player_monsters: Dictionary containing all player choices
        
    Returns:
        Ecotoxicity value (float)
    """
    # Get drug code and toxicity values
    drug_code = get_drug_code_from_choices(player_monsters)
    if drug_code not in molecule_stats:
        return 0  # Default
    
    stats = molecule_stats[drug_code]
    tox_api = stats['toxAPI']
    tox_meta = stats['toxMeta']
    
    # Get water emissions
    api_emissions, meta_emissions = calculate_water_emissions(player_monsters)
    
    # Calculate ecotoxicity
    ecotoxicity = (api_emissions * tox_api) + (meta_emissions * tox_meta)
    
    return ecotoxicity


def calculate_city_scale_indicators(player_monsters):
    """
    Calculate all city-scale indicators for game progress tracking.
    
    This scales up per-gram values to city scale using:
    scale_factor = patients / doses_per_gram
    
    Args:
        player_monsters: Dictionary containing all player choices
        
    Returns:
        Dictionary containing all scaled indicators:
        - city_waste: Total waste per day (g/day)
        - city_cost: Total cost per day ($/day)
        - city_impact: Total CO2 impact per day (gCO2/day)
        - city_api_emissions: Total API emissions per day (g/day)
        - city_meta_emissions: Total metabolite emissions per day (g/day)
        - city_ecotoxicity: Total ecotoxicity per day (per day)
        - scale_factor: The multiplier used (patients/doses_per_gram)
    """
    # Calculate scale factor: patients / doses per gram
    num_patients = get_patient_count(player_monsters)
    doses_per_g = get_doses_per_gram_from_choices(player_monsters)
    scale_factor = num_patients / doses_per_g
    
    # Get per-gram values
    factory_waste_per_g = calculate_factory_waste_per_gram(player_monsters)
    factory_cost_per_g = calculate_factory_costs(player_monsters)
    factory_impact_per_g = calculate_factory_impact(player_monsters)
    api_emis_per_g, meta_emis_per_g = calculate_water_emissions(player_monsters)
    ecotox_per_g = calculate_ecotoxicity(player_monsters)
    
    # Get daily values (not per gram)
    daily_cost = calculate_city_daily_costs(player_monsters)
    cup_impact_daily = calculate_cup_impact(player_monsters)
    
    # Scale up to city level
    city_waste = factory_waste_per_g * scale_factor
    city_cost = (factory_cost_per_g * scale_factor) + daily_cost
    city_impact = (factory_impact_per_g * scale_factor) + cup_impact_daily
    city_api_emissions = api_emis_per_g * scale_factor
    city_meta_emissions = meta_emis_per_g * scale_factor
    city_ecotoxicity = ecotox_per_g * scale_factor
    
    return {
        'city_waste': city_waste,
        'city_cost': city_cost,
        'city_impact': city_impact,
        'city_api_emissions': city_api_emissions,
        'city_meta_emissions': city_meta_emissions,
        'city_ecotoxicity': city_ecotoxicity,
        'scale_factor': scale_factor,
        'num_patients': num_patients,
        'doses_per_gram': doses_per_g
    }


def check_compliance_thresholds(player_monsters):
    """
    Check if all regulatory and procurement thresholds are met.
    
    Args:
        player_monsters: Dictionary containing all player choices
        
    Returns:
        Dictionary containing compliance status for each threshold:
        - worker_safety: {'compliant': bool, 'exposure': float, 'threshold': 1}
        - biodegradation: {'compliant': bool, 'biodeg_api': float, 'threshold': float, 'required': bool, 'has_certification': bool}
        - pollution: {'compliant': bool, 'total_pollution': float, 'limit': float}
        - co2_impact: {'compliant': bool, 'total_impact': float, 'target': float, 'required': bool}
        - price: {'compliant': bool, 'total_cost': float, 'price_cap': float}
        - factory_at_risk: bool (True if worker safety fails)
        - meets_procurement: bool (True if all procurement requirements met)
        - regulatory_fine: float (40 if pollution limit exceeded, else 0)
    """
    # Get drug code and stats
    drug_code = get_drug_code_from_choices(player_monsters)
    if drug_code not in molecule_stats:
        return {}
    
    stats = molecule_stats[drug_code]
    
    # Get city-scale indicators
    indicators = calculate_city_scale_indicators(player_monsters)
    
    # (1) Worker Safety - factory at risk of closure if exposure > 1
    exposure, is_safe = calculate_worker_risk(player_monsters)
    worker_safety = {
        'compliant': is_safe,
        'exposure': exposure,
        'threshold': 1,
        'status': 'SAFE' if is_safe else 'FACTORY AT RISK'
    }
    
    # Determine procurement policy (slot 9)
    procurement_policy = 'No procurement rules'  # Default: free market
    if 9 in player_monsters:
        procurement_policy = player_monsters[9].name

    # Determine biodegradation standard (slot 11) - certification system
    biodeg_standard = 'No biodegradation standard'  # Default: no certification
    if 11 in player_monsters:
        biodeg_standard = player_monsters[11].name

    # (2) Biodegradation - required if Bio-procurement policy is active
    biodeg_required = (procurement_policy == 'Bio-procurement')
    biodeg_threshold = 0.5 if biodeg_required else 0.0
    biodeg_api = stats['biodegAPI']

    # Check if both policy and certification exist
    has_certification = (biodeg_standard == 'Biodegradation standard')

    # Determine compliance status
    if biodeg_required and not has_certification:
        # Policy requires biodegradability but no certification system exists
        biodeg_status = 'FAIL (no certification scheme)'
        biodeg_compliant = False
    elif biodeg_required and has_certification:
        # Both policy and certification exist - check if molecule meets threshold
        biodeg_compliant = biodeg_api >= biodeg_threshold
        biodeg_status = 'PASS' if biodeg_compliant else 'FAIL (does not meet procurement policy)'
    else:
        # No biodegradation requirement
        biodeg_compliant = biodeg_api >= biodeg_threshold
        biodeg_status = 'PASS' if biodeg_compliant else 'N/A'

    biodegradation = {
        'compliant': biodeg_compliant,
        'biodeg_api': biodeg_api,
        'threshold': biodeg_threshold,
        'required': biodeg_required,
        'has_certification': has_certification,
        'status': biodeg_status
    }
    
    # (3) Pollution Limits - based on slot 10
    pollution_policy = 'No water quality standards'  # Default: no limit
    if 10 in player_monsters:
        pollution_policy = player_monsters[10].name
    
    if pollution_policy == 'Lenient water quality standards':
        pollution_limit = pollution_limit_basic  # 0.2
    elif pollution_policy == 'Strict water quality standards':
        pollution_limit = pollution_limit_harsh  # 0.05
    else:  # pollution1
        pollution_limit = pollution_limit_none  # 1000000 (effectively no limit)
    
    total_pollution = indicators['city_api_emissions'] + indicators['city_meta_emissions']
    pollution_compliant = total_pollution <= pollution_limit
    regulatory_fine = penalty_basic if not pollution_compliant and pollution_limit < pollution_limit_none else 0
    
    pollution = {
        'compliant': pollution_compliant,
        'total_pollution': total_pollution,
        'limit': pollution_limit,
        'policy': pollution_policy,
        'fine': regulatory_fine,
        'status': 'PASS' if pollution_compliant else f'FAIL (fine ${regulatory_fine}/day)'
    }
    
    # (4) CO2 Impact - target is 50 × doses per gram, required if procurement3
    co2_required = (procurement_policy == 'Sustainable procurement')
    co2_target = 50 * total_patients
    co2_impact = {
        'compliant': indicators['city_impact'] <= co2_target,
        'total_impact': indicators['city_impact'],
        'target': co2_target,
        'required': co2_required,
        'status': 'PASS' if indicators['city_impact'] <= co2_target else 'FAIL (does not meet procurement policy)'
    }
    
    # (5) Price - depends on procurement policy
    if procurement_policy == 'No procurement rules':
        price_cap = price_cap_free  # 90
    elif procurement_policy == 'Bio-procurement':
        price_cap = price_cap_biopref  # 120
    elif procurement_policy == 'Sustainable procurement':
        price_cap = price_cap_pwes  # 100
    else:
        price_cap = price_cap_free
    
    price = {
        'compliant': indicators['city_cost'] <= price_cap,
        'total_cost': indicators['city_cost'],
        'price_cap': price_cap,
        'procurement_policy': procurement_policy,
        'status': 'PASS' if indicators['city_cost'] <= price_cap else 'FAIL (too expensive)'
    }
    
    # Overall status
    factory_at_risk = not worker_safety['compliant']
    
    # Check if procurement requirements are met
    procurement_requirements_met = True
    if procurement_policy == 'Bio-procurement':
        # Biopreference: needs biodeg >= 50% AND price <= 120
        procurement_requirements_met = biodegradation['compliant'] and price['compliant']
    elif procurement_policy == 'Sustainable procurement':
        # PWES: needs CO2 <= target AND price <= 100
        procurement_requirements_met = co2_impact['compliant'] and price['compliant']
    else:
        # Free market: only needs price <= 90
        procurement_requirements_met = price['compliant']
    
    return {
        'worker_safety': worker_safety,
        'biodegradation': biodegradation,
        'pollution': pollution,
        'co2_impact': co2_impact,
        'price': price,
        'factory_at_risk': factory_at_risk,
        'meets_procurement': procurement_requirements_met,
        'regulatory_fine': regulatory_fine,
        'overall_compliant': (not factory_at_risk) and pollution['compliant'] and procurement_requirements_met
    }



# Test the functions
if __name__ == '__main__':
    import math
    
    # Example test
    class MockMonster:
        def __init__(self, name, level=1):
            self.name = name
            self.level = level
    
    test_monsters = {
        0: MockMonster('molecule_C1'),
        1: MockMonster('molecule_A1'),
        2: MockMonster('molecule_B1'),
        3: MockMonster('molecule_D1'),
        4: MockMonster('Standard PPE'),  # Basic safety
        5: MockMonster('No wastewater treatment'),  # No treatment
        6: MockMonster('Standard energy'),  # Normal energy
        7: MockMonster('Reusable dispensing cup'),  # Standard cup
        8: MockMonster('Prescribe as required'),  # No deprescribing
        9: MockMonster('No procurement rules'),  # Free market
        10: MockMonster('No water quality standards'),  # No pollution limit
        12: MockMonster('reaction_temperature', 75),  # 75°C
        13: MockMonster('reaction_hours', 6),  # 6 hours
    }
    
    code = get_drug_code_from_choices(test_monsters)
    print(f"Drug code: {code}")
    
    if code in molecule_stats:
        stats = molecule_stats[code]
        print(f"Stats: {stats}")
        
        # Test conversion calculation
        conversion = get_conversion_from_player_choices(test_monsters)
        print(f"\nReaction conversion: {conversion}%")
        
        # Show the parameters used
        temp, duration = get_reaction_parameters(test_monsters)
        print(f"Temperature: {temp}°C")
        print(f"Duration: {duration} hours")
        print(f"Rate constant: {stats['rateConst']}")
        
        # Test doses per gram calculation
        doses = get_doses_per_gram_from_choices(test_monsters)
        print(f"\nEfficacy: {stats['efficacy']}")
        print(f"Doses per gram: {doses}")
        
        # Test patient count
        patient_count = get_patient_count(test_monsters)
        print(f"\nPrescription type: {test_monsters[8].name}")
        print(f"Patient count: {patient_count}")
        
        # Test factory waste per gram
        factory_waste = calculate_factory_waste_per_gram(test_monsters)
        print(f"\nFactory waste calculation:")
        print(f"  Base waste: {stats['waste']} g/g")
        print(f"  Conversion inefficiency: {1 / (conversion / 100):.2f} g/g")
        print(f"  Total factory waste: {factory_waste:.2f} g/g")
        
        # Test factory costs with normal energy
        factory_cost = calculate_factory_costs(test_monsters)
        print(f"\nFactory costs (Normal Energy):")
        print(f"  Base cost: ${stats['cost']:.2f}/g")
        print(f"  Solid waste cost: ${cost_solid_waste * factory_waste:.2f}/g")
        energy_kwh = 0.001 * ((8 * (temp - 20)) + (1.33 * (temp - 20) * duration))
        print(f"  Energy consumption: {energy_kwh:.4f} kWh/g")
        print(f"  Energy cost: ${energy_kwh * cost_normal_energy:.4f}/g")
        print(f"  Total factory cost: ${factory_cost:.4f}/g")
        
        # Test factory impact with normal energy
        factory_impact = calculate_factory_impact(test_monsters)
        print(f"\nFactory impact (Normal Energy):")
        print(f"  Base impact: {stats['impact']} gCO2/g")
        print(f"  Energy impact: {energy_kwh * normal_energy_gwp:.2f} gCO2/g")
        print(f"  Total factory impact: {factory_impact:.2f} gCO2/g")
        
        # Test water emissions with emissions1 (no treatment)
        api_emis, meta_emis = calculate_water_emissions(test_monsters)
        print(f"\nWater emissions (No treatment):")
        print(f"  biodegAPI: {stats['biodegAPI']}, biodegMeta: {stats['biodegMeta']}")
        print(f"  Raw factory API: {factory_api_emissions} g/g, Raw hospital API: {hospital_api_emissions} g/g")
        print(f"  Raw factory Meta: {factory_meta_emissions} g/g, Raw hospital Meta: {hospital_meta_emissions} g/g")
        print(f"  Final API emissions: {api_emis:.4f} g/g")
        print(f"  Final Metabolite emissions: {meta_emis:.4f} g/g")
        
        # Test with minor treatment (emissions2)
        print("\n--- With minor treatment ---")
        test_monsters[5] = MockMonster('Basic water treatment')
        api_emis2, meta_emis2 = calculate_water_emissions(test_monsters)
        print(f"Water emissions (Minor treatment):")
        print(f"  Raw factory API: {factory_api_emissions_minor_treatment} g/g, Raw hospital API: {hospital_api_emissions} g/g")
        print(f"  Raw factory Meta: {factory_meta_emissions_minor_treatment} g/g, Raw hospital Meta: {hospital_meta_emissions} g/g")
        print(f"  Final API emissions: {api_emis2:.4f} g/g")
        print(f"  Final Metabolite emissions: {meta_emis2:.4f} g/g")
        
        # Test with major treatment (emissions3)
        print("\n--- With major treatment ---")
        test_monsters[5] = MockMonster('Advanced water treatment')
        api_emis3, meta_emis3 = calculate_water_emissions(test_monsters)
        print(f"Water emissions (Major treatment):")
        print(f"  Raw factory API: {factory_api_emissions_major_treatment} g/g, Raw hospital API: {hospital_api_emissions} g/g")
        print(f"  Raw factory Meta: {factory_meta_emissions_major_treatment} g/g, Raw hospital Meta: {hospital_meta_emissions} g/g")
        print(f"  Final API emissions: {api_emis3:.4f} g/g")
        print(f"  Final Metabolite emissions: {meta_emis3:.4f} g/g")
        
        # Reset to emissions1 for remaining tests
        test_monsters[5] = MockMonster('No wastewater treatment')
        
        # Test city daily costs
        daily_cost = calculate_city_daily_costs(test_monsters)
        print(f"\nCity daily costs (Standard PPE + Reusable dispensing cup + 60 patients):")
        print(f"  Safety cost: ${cost_basic_safety}/day")
        print(f"  Cup cost: ${cost_cup1} × {patient_count} patients = ${cost_cup1 * patient_count}/day")
        print(f"  Regulatory fines: $0/day (placeholder)")
        print(f"  Total daily cost: ${daily_cost:.2f}/day")
        
        # Test cup impact
        cup_impact = calculate_cup_impact(test_monsters)
        print(f"\nCup impact (Reusable dispensing cup + 60 patients):")
        print(f"  Cup GWP: {gwp_cup1} gCO2 per use")
        print(f"  Total cup impact: {gwp_cup1} × {patient_count} = {cup_impact:.2f} gCO2/day")
        
        # Test worker risk
        exposure, is_safe = calculate_worker_risk(test_monsters)
        print(f"\nWorker risk (Standard PPE - Basic safety):")
        print(f"  Exposure level: {exposure}")
        print(f"  Is safe: {is_safe} (safe if ≤ 1)")
        print(f"  Risk status: {'SAFE ✓' if is_safe else 'TOO HIGH ✗'}")
        
        # Test ecotoxicity
        ecotox = calculate_ecotoxicity(test_monsters)
        print(f"\nEcotoxicity (No treatment):")
        print(f"  toxAPI: {stats['toxAPI']}, toxMeta: {stats['toxMeta']}")
        print(f"  API emissions: {api_emis:.4f} g/g")
        print(f"  Meta emissions: {meta_emis:.4f} g/g")
        print(f"  Ecotoxicity: ({api_emis:.4f} × {stats['toxAPI']}) + ({meta_emis:.4f} × {stats['toxMeta']})")
        print(f"  Ecotoxicity: {ecotox:.4f}")
        
        # Test with different safety levels
        print(f"\n--- With different safety equipment ---")
        for safety_name, safety_cost_val in [('PPE and extra ventilation', cost_vent_safety), ('No PPE', cost_no_safety), ('Closed reactor system', cost_closed_safety)]:
            test_monsters[4] = MockMonster(safety_name)
            daily_cost_safety = calculate_city_daily_costs(test_monsters)
            exposure_safety, is_safe_safety = calculate_worker_risk(test_monsters)
            risk_status = 'SAFE ✓' if is_safe_safety else 'TOO HIGH ✗'
            print(f"{safety_name}: Safety ${safety_cost_val}/day → Total ${daily_cost_safety:.2f}/day, Exposure {exposure_safety} ({risk_status})")
        
        # Reset to safety1
        test_monsters[4] = MockMonster('Standard PPE')
        
        # Test ecotoxicity with different treatment levels
        print(f"\n--- Ecotoxicity with different treatment levels ---")
        for emis_name in ['No wastewater treatment', 'Basic water treatment', 'Advanced water treatment']:
            test_monsters[5] = MockMonster(emis_name)
            api_e, meta_e = calculate_water_emissions(test_monsters)
            ecotox_e = calculate_ecotoxicity(test_monsters)
            print(f"{emis_name}: API {api_e:.4f}, Meta {meta_e:.4f} → Ecotox {ecotox_e:.4f}")
        
        # Reset to emissions1
        test_monsters[5] = MockMonster('No wastewater treatment')
        
        # Test with cup2
        print(f"\n--- With premium cups (cup2) ---")
        test_monsters[7] = MockMonster('Single use dispensing cup')
        daily_cost_cup2 = calculate_city_daily_costs(test_monsters)
        cup_impact_cup2 = calculate_cup_impact(test_monsters)
        print(f"Cup cost: ${cost_cup2} × {patient_count} patients = ${cost_cup2 * patient_count}/day")
        print(f"Total daily cost: ${daily_cost_cup2:.2f}/day")
        print(f"Cup impact: {gwp_cup2} × {patient_count} = {cup_impact_cup2:.2f} gCO2/day")
        
        # Test with deprescribing
        print(f"\n--- With deprescribing (52 patients instead of 60) ---")
        test_monsters[7] = MockMonster('Reusable dispensing cup')  # Reset to cup1
        test_monsters[8] = MockMonster('Deprescribing Program')
        daily_cost_deprescribe = calculate_city_daily_costs(test_monsters)
        cup_impact_deprescribe = calculate_cup_impact(test_monsters)
        patient_count_deprescribed = get_patient_count(test_monsters)
        print(f"Cup cost: ${cost_cup1} × {patient_count_deprescribed} patients = ${cost_cup1 * patient_count_deprescribed}/day")
        print(f"Total daily cost: ${daily_cost_deprescribe:.2f}/day")
        print(f"Cup impact: {gwp_cup1} × {patient_count_deprescribed} = {cup_impact_deprescribe:.2f} gCO2/day")
        
        # Reset for green energy test
        test_monsters[8] = MockMonster('Prescribe as required')
        
        # Test with green energy
        print("\n--- With green energy ---")
        test_monsters[6] = MockMonster('Green energy')
        factory_cost_green = calculate_factory_costs(test_monsters)
        factory_impact_green = calculate_factory_impact(test_monsters)
        print(f"Factory costs (Green Energy):")
        print(f"  Energy cost: ${energy_kwh * cost_green_energy:.4f}/g")
        print(f"  Total factory cost: ${factory_cost_green:.4f}/g")
        print(f"Factory impact (Green Energy):")
        print(f"  Energy impact: {energy_kwh * green_energy_gwp:.2f} gCO2/g")
        print(f"  Total factory impact: {factory_impact_green:.2f} gCO2/g")
        
        # Reset to normal energy for final summary
        test_monsters[6] = MockMonster('Standard energy')
        test_monsters[8] = MockMonster('Prescribe as required')
        test_monsters[9] = MockMonster('No procurement rules')  # Free market
        test_monsters[10] = MockMonster('No water quality standards')  # No pollution limit
        
        # Calculate comprehensive city-scale indicators
        print("\n" + "="*60)
        print("COMPREHENSIVE CITY-SCALE INDICATORS")
        print("="*60)
        indicators = calculate_city_scale_indicators(test_monsters)
        
        print(f"\nScaling Information:")
        print(f"  Number of patients: {indicators['num_patients']}")
        print(f"  Doses per gram: {indicators['doses_per_gram']}")
        print(f"  Scale factor: {indicators['scale_factor']:.2f} g/day")
        
        print(f"\nDaily City-Scale Indicators:")
        print(f"  Total waste: {indicators['city_waste']:.2f} g/day")
        print(f"  Total cost: ${indicators['city_cost']:.2f}/day")
        print(f"  Total CO2 impact: {indicators['city_impact']:.2f} gCO2/day")
        print(f"  API emissions to water: {indicators['city_api_emissions']:.4f} g/day")
        print(f"  Metabolite emissions to water: {indicators['city_meta_emissions']:.4f} g/day")
        print(f"  Ecotoxicity: {indicators['city_ecotoxicity']:.4f}/day")
        
        # Check compliance thresholds
        print("\n" + "="*60)
        print("COMPLIANCE THRESHOLDS")
        print("="*60)
        compliance = check_compliance_thresholds(test_monsters)
        
        print(f"\n1. Worker Safety: {compliance['worker_safety']['status']}")
        print(f"   Exposure: {compliance['worker_safety']['exposure']} (threshold ≤ {compliance['worker_safety']['threshold']})")
        
        print(f"\n2. Biodegradation: {compliance['biodegradation']['status']}")
        print(f"   biodegAPI: {compliance['biodegradation']['biodeg_api']*100:.1f}% (threshold ≥ {compliance['biodegradation']['threshold']*100:.0f}%)")
        print(f"   Required: {compliance['biodegradation']['required']}")
        
        print(f"\n3. Pollution: {compliance['pollution']['status']}")
        print(f"   Total pollution: {compliance['pollution']['total_pollution']:.4f} g/day")
        print(f"   Limit: {compliance['pollution']['limit']} g/day ({compliance['pollution']['policy']})")
        
        print(f"\n4. CO2 Impact: {compliance['co2_impact']['status']}")
        print(f"   Total impact: {compliance['co2_impact']['total_impact']:.2f} gCO2/day")
        print(f"   Target: {compliance['co2_impact']['target']:.2f} gCO2/day (50 × {indicators['doses_per_gram']} doses × {indicators['num_patients']} patients)")
        print(f"   Required: {compliance['co2_impact']['required']}")
        
        print(f"\n5. Price: {compliance['price']['status']}")
        print(f"   Total cost: ${compliance['price']['total_cost']:.2f}/day")
        print(f"   Price cap: ${compliance['price']['price_cap']}/day ({compliance['price']['procurement_policy']})")
        
        print(f"\nOVERALL STATUS:")
        print(f"  Factory at risk: {compliance['factory_at_risk']}")
        print(f"  Meets procurement: {compliance['meets_procurement']}")
        print(f"  Overall compliant: {compliance['overall_compliant']}")
        print(f"  Regulatory fine: ${compliance['regulatory_fine']}/day")
        
        # Test with stricter policies
        print("\n" + "="*60)
        print("SCENARIO: Biopreference Policy + Harsh Pollution Standards")
        print("="*60)
        test_monsters[9] = MockMonster('Bio-procurement')  # Biopreference
        test_monsters[10] = MockMonster('Strict water quality standards')  # Harsh pollution limit
        compliance2 = check_compliance_thresholds(test_monsters)
        
        print(f"\nBiodegradation: {compliance2['biodegradation']['status']}")
        print(f"Pollution: {compliance2['pollution']['status']}")
        print(f"Price: {compliance2['price']['status']}")
        print(f"Meets procurement: {compliance2['meets_procurement']}")
        print(f"Regulatory fine: ${compliance2['regulatory_fine']}/day")
        
        # Test with different scenario
        print("\n--- With green energy + deprescribing + premium cups ---")
        test_monsters[6] = MockMonster('Green energy')
        test_monsters[7] = MockMonster('Single use dispensing cup')
        test_monsters[8] = MockMonster('Deprescribing Program')
        test_monsters[9] = MockMonster('No procurement rules')
        test_monsters[10] = MockMonster('No water quality standards')
        indicators2 = calculate_city_scale_indicators(test_monsters)
        
        print(f"Scaling: {indicators2['num_patients']} patients / {indicators2['doses_per_gram']} doses = {indicators2['scale_factor']:.2f} g/day")
        print(f"Total cost: ${indicators2['city_cost']:.2f}/day (vs ${indicators['city_cost']:.2f})")
        print(f"Total CO2: {indicators2['city_impact']:.2f} gCO2/day (vs {indicators['city_impact']:.2f})")
        print(f"Ecotoxicity: {indicators2['city_ecotoxicity']:.4f}/day (vs {indicators['city_ecotoxicity']:.4f})")
    else:
        print(f"Stats: Not found for code {code}")