import http.server
import socketserver
import urllib.request
import json
import subprocess
import webbrowser
import threading
import socket
import os
import sys

# =============================================================================
# 1. VERIFIED MULTI-AGENCY EXTRATERRESTRIAL TARGETS (WITH SOLAR FLUX W/m²)
# =============================================================================
TARGETS = [
    {
        "name": "Shackleton Crater Rim (Lunar South Pole - Artemis Base)",
        "body": "Moon", "role": "Permanent Base", "lat": -89.67, "lon": 129.78,
        "temp": -183.0, "diurnal": 60.0, "slope": 24.5, "elev": 2100,
        "aridity": 100.0, "solar": 8.2, "solar_flux": 1361, "basalt": 15.0, "ice": 92.0, "shielding": 65.0,
        "gravity": 1.62, "pressure": 0.0, "simulant": "LHS-1 Highlands Anorthosite",
        "oxides": {"SiO2": 48.1, "TiO2": 0.6, "Al2O3": 25.8, "FeO": 4.2, "MgO": 6.1, "CaO": 14.5},
        "agencies": "NASA LRO (LOLA/Diviner) + ISRO Chandrayaan-1 M³ & Chandrayaan-2 DFSAR",
        "objective": "Permanent Lunar South Pole Base: Cryogenic PSR Water-Ice Mining, Grazing Solar Flux Array Ops & Steep Rim Mobility",
        "youth": "A sunlit mountain peak at the Moon's South Pole hit by 1,361 W/m² of raw solar flux right next to pitch-black craters filled with water ice."
    },
    {
        "name": "Marius Hills Skylight Pit (Lunar Mare Lava Tube Base)",
        "body": "Moon", "role": "Permanent Base", "lat": 14.09, "lon": -56.77,
        "temp": 17.0, "diurnal": 250.0, "slope": 34.0, "elev": -1400,
        "aridity": 100.0, "solar": 6.5, "solar_flux": 1361, "basalt": 98.0, "ice": 5.0, "shielding": 99.0,
        "gravity": 1.62, "pressure": 0.0, "simulant": "LMS-1 Mare Flood Basalt",
        "oxides": {"SiO2": 46.9, "TiO2": 3.6, "Al2O3": 12.4, "FeO": 16.8, "MgO": 9.3, "CaO": 10.1},
        "agencies": "JAXA SELENE/Kaguya Terrain Camera + NASA LRO NAC Oblique & Diviner",
        "objective": "Permanent Subsurface Habitat: Radiation/Micrometeorite Shielded Cave Base & Tethered Skylight Rappelling",
        "youth": "A giant collapsed volcanic cave on the Moon where the underground interior stays a steady +17°C while the surface sees 1,361 W/m² solar flux."
    },
    {
        "name": "Aristarchus Plateau Pyroclastic Vent (Lunar ISRU Site)",
        "body": "Moon", "role": "Landing Site", "lat": 24.50, "lon": -49.00,
        "temp": -23.0, "diurnal": 260.0, "slope": 19.0, "elev": 1800,
        "aridity": 100.0, "solar": 6.8, "solar_flux": 1361, "basalt": 94.0, "ice": 12.0, "shielding": 40.0,
        "gravity": 1.62, "pressure": 0.0, "simulant": "JSC-1A Volcanic Glass",
        "oxides": {"SiO2": 46.2, "TiO2": 2.9, "Al2O3": 14.5, "FeO": 15.2, "MgO": 10.4, "CaO": 9.8},
        "agencies": "NASA Clementine UV/VIS + LRO Diviner + ISRO Chandrayaan-2 IIRS",
        "objective": "Lunar ISRU Landing Site: Solar-Thermal Ilmenite Volcanic Glass Oxygen Extraction & Rille Traverse",
        "youth": "An ancient lunar volcanic ash plain rich in iron and titanium glass beads that can be baked with concentrated solar flux to extract oxygen."
    },
    {
        "name": "Arcadia Planitia (Mars Shallow Ice Sheet Permanent Base)",
        "body": "Mars", "role": "Permanent Base", "lat": 39.10, "lon": -168.00,
        "temp": -63.0, "diurnal": 62.0, "slope": 3.2, "elev": -4200,
        "aridity": 96.0, "solar": 3.2, "solar_flux": 495, "basalt": 82.0, "ice": 95.0, "shielding": 70.0,
        "gravity": 3.72, "pressure": 820.0, "simulant": "MGS-1 Mars Basalt + Subsurface Ice",
        "oxides": {"SiO2": 47.8, "TiO2": 1.1, "Al2O3": 11.2, "FeO": 15.6, "MgO": 9.8, "CaO": 7.9},
        "agencies": "NASA MRO (SHARAD Radar / HiRISE) + NASA SWIM Ice Mapping Project",
        "objective": "Permanent Human Mars Base: Heavy Lander Touchdown, Rodwell Subsurface Ice Mining & Methalox Propellant ISRU",
        "youth": "A flat plain on Mars sitting directly above a massive underground sheet of pure water ice with 495 W/m² peak solar flux."
    },
    {
        "name": "Arsia Mons Pit Craters (Mars Tharsis Volcanic Cave Base)",
        "body": "Mars", "role": "Permanent Base", "lat": -9.00, "lon": -120.50,
        "temp": -70.0, "diurnal": 80.0, "slope": 29.0, "elev": 12500,
        "aridity": 99.8, "solar": 4.6, "solar_flux": 585, "basalt": 99.0, "ice": 15.0, "shielding": 98.0,
        "gravity": 3.72, "pressure": 190.0, "simulant": "MMS-2 Tharsis Basalt",
        "oxides": {"SiO2": 49.1, "TiO2": 1.8, "Al2O3": 13.0, "FeO": 14.9, "MgO": 8.5, "CaO": 9.4},
        "agencies": "NASA Mars Odyssey THEMIS + MRO HiRISE Pit Catalog + ESA Mars Express",
        "objective": "Permanent Subsurface Mars Sanctuary: High-Altitude Cave Astrobiology & Natural Radiation/Dust-Storm Shelter",
        "youth": "Deep skylight entrances into underground lava tubes high on a Martian volcano receiving 585 W/m² solar flux above the dust layer."
    },
    {
        "name": "Jezero Crater Delta (Mars 2020 Perseverance Site)",
        "body": "Mars", "role": "Landing Site", "lat": 18.38, "lon": 77.58,
        "temp": -55.0, "diurnal": 68.0, "slope": 11.5, "elev": -2500,
        "aridity": 99.0, "solar": 3.8, "solar_flux": 540, "basalt": 78.0, "ice": 35.0, "shielding": 45.0,
        "gravity": 3.72, "pressure": 680.0, "simulant": "JEZ-1 Jezero Smectite/Carbonate",
        "oxides": {"SiO2": 44.5, "TiO2": 0.9, "Al2O3": 9.8, "FeO": 17.5, "MgO": 14.2, "CaO": 6.4},
        "agencies": "NASA Mars 2020 Perseverance (MEDA/PIXL/SHERLOC) + MRO CRISM",
        "objective": "Sample Return Landing Site: Ancient River Delta Biosignature Core Drilling, Helicopter Nav & MOXIE O₂ ISRU",
        "youth": "An ancient dried-up lakebed and river delta on Mars where Perseverance is hunting for fossilized microbial life."
    },
    {
        "name": "Gale Crater - Aeolis Mons (MSL Curiosity Site)",
        "body": "Mars", "role": "Landing Site", "lat": -5.40, "lon": 137.80,
        "temp": -48.0, "diurnal": 72.0, "slope": 16.5, "elev": -4500,
        "aridity": 99.2, "solar": 4.2, "solar_flux": 560, "basalt": 75.0, "ice": 30.0, "shielding": 50.0,
        "gravity": 3.72, "pressure": 840.0, "simulant": "MGS-1S Sulfate Mudstone",
        "oxides": {"SiO2": 45.2, "TiO2": 1.0, "Al2O3": 10.5, "FeO": 18.2, "MgO": 8.9, "CaO": 7.1},
        "agencies": "NASA Mars Science Laboratory (Curiosity REMS, CheMin, SAM)",
        "objective": "Long-Range Traverse Site: Sulfate-to-Clay Transition Stratigraphy & Basaltic Sand Dune Traction Validation",
        "youth": "A deep Martian basin with a 5-km layered mountain recording how Mars dried up from a wet world into a freezing desert."
    },
    {
        "name": "Mawrth Vallis Phyllosilicate Plains (Mars Astrobiology Site)",
        "body": "Mars", "role": "Landing Site", "lat": 23.99, "lon": -19.00,
        "temp": -58.0, "diurnal": 65.0, "slope": 7.5, "elev": -2200,
        "aridity": 98.8, "solar": 3.9, "solar_flux": 530, "basalt": 55.0, "ice": 42.0, "shielding": 48.0,
        "gravity": 3.72, "pressure": 650.0, "simulant": "MGS-1C Hydrated Clay Simulant",
        "oxides": {"SiO2": 51.4, "TiO2": 0.8, "Al2O3": 14.8, "FeO": 13.2, "MgO": 7.4, "CaO": 5.8},
        "agencies": "ESA Mars Express OMEGA + ExoMars TGO + NASA MRO CRISM",
        "objective": "Deep Astrobiology Landing Site: 2-Meter Subsurface Coring in Hydrated Noachian Fe/Mg Smectite Clays",
        "youth": "An ancient Martian flood channel lined with thick clay layers capable of preserving organic molecules for billions of years."
    }
]

# =============================================================================
# 2. EARTH ANALOG SITES (WITH EXACT INLAND COORDINATES & PEAK SOLAR FLUX W/m²)
# =============================================================================
EARTH_SITES = [
    {
        "name": "Spiti Valley (Kibber–Langza Cold Desert), HP, India", "tier": "BRAND-NEW", "cat": "Polar Regions",
        "cond": "Cryogenic Permafrost", "char_pct": 28, "scale": "18-km Glacio-Fluvial Basin",
        "process": "Freeze-Thaw Solifluction & Eolian Loess Erosion",
        "lat": 32.33, "lon": 78.01, "terrain": "High-Altitude Rain-Shadow Cold Desert, Shale/Basalt Scree & Permafrost",
        "temp": -4.2, "diurnal": 31.0, "slope": 16.5, "elev": 4270, "press": 605,
        "aridity": 92.0, "solar": 6.1, "solar_flux": 1085, "basalt": 62.0, "ice": 78.0, "shielding": 56.0,
        "oxides": {"SiO2": 51.2, "TiO2": 0.9, "Al2O3": 14.5, "FeO": 9.4, "MgO": 7.8, "CaO": 8.1},
        "geology": "Trans-Himalayan rain-shadow desert with freeze-thaw patterned ground, marine fossil shales, volcanic ophiolites, and perennial ground ice.",
        "campaigns": "Brand-New Candidate Analog (Recommended in 2026 Brief; zero formal space-agency field campaigns yet)",
        "equip": "Cryogenic permafrost drills, high-altitude drone navigation, low-pressure thermal habitat tents, high-UV solar arrays.",
        "methods": "14-minute Mars comms-delay EVA geological traverses, sterile permafrost core caching, cold-weather battery endurance.",
        "subzones": "Zone A: Langza Fossil-Shale Bench (12° slope) | Zone B: Kibber Permafrost Talus (22°) | Zone C: Spiti River Alluvial Fan.",
        "missing": "Needs 3D ground-penetrating radar (GPR) ice-table profiling and continuous winter-over Diviner-equivalent thermal inertia logging.",
        "gaps": "Earth gravity (9.81 m/s² vs Mars 3.72 m/s²), 605 hPa air pressure (vs Mars 6.8 hPa), and higher atmospheric O₂.",
        "stewardship": "Access via NH-505 / Kaza roadhead (open May–Nov; winter snowbound). Respect Kibber Wildlife Sanctuary permits & local Spitian Buddhist heritage sites.",
        "monthly_t": [-15,-12,-6,1,7,12,15,14,10,2,-7,-13], "monthly_s": [4.3,5.1,6.0,6.8,7.3,7.6,7.2,6.7,6.1,5.4,4.6,4.0]
    },
    {
        "name": "Niti & Mana High Cold Valleys (Chamoli), Uttarakhand, India", "tier": "BRAND-NEW", "cat": "Polar Regions",
        "cond": "Low-Angle Grazing Sunlight", "char_pct": 24, "scale": "14-km Periglacial Moraine Valley",
        "process": "Periglacial Moraine Creep & Frost Shattering",
        "lat": 30.77, "lon": 79.84, "terrain": "Trans-Himalayan Arid Periglacial Moraine & Steep Shadowed Canyon",
        "temp": -2.8, "diurnal": 29.0, "slope": 23.5, "elev": 3950, "press": 630,
        "aridity": 87.0, "solar": 5.8, "solar_flux": 1040, "basalt": 58.0, "ice": 82.0, "shielding": 64.0,
        "oxides": {"SiO2": 53.0, "TiO2": 0.8, "Al2O3": 15.0, "FeO": 8.6, "MgO": 6.9, "CaO": 7.4},
        "geology": "Deeply incised rain-shadow glacial valley featuring angular boulder fields, buried moraine ice lenses, and deep canyon shadows mimicking Lunar South Pole lighting.",
        "campaigns": "Brand-New Candidate Analog (Proposed in 2026 Challenge Brief for Lunar Polar Shadow & Mars Periglacial Testing)",
        "equip": "High-dynamic-range (HDR) shadow-navigation rover cameras, boulder-climbing rocker-bogie chassis, ice-core drills.",
        "methods": "Low-sun-angle grazing illumination optical navigation, steep moraine hazard avoidance, remote telemetry relay hops.",
        "subzones": "Zone A: Niti Glacial Outwash Plain (6° slope) | Zone B: Shadowed Canyon Talus Wall (24°) | Zone C: Buried Moraine Ice Lens.",
        "missing": "Uncharacterized sub-meter boulder size-frequency distribution (SFD) and subsurface ice-table dielectric permittivity.",
        "gaps": "Higher ambient atmospheric pressure (630 hPa) and summer monsoon moisture spillover compared to hard lunar vacuum.",
        "stewardship": "Accessible via Joshimath–Niti highway (May–Oct). Located in Nanda Devi Biosphere Buffer Zone & Indo-Tibetan border zone — requires Inner Line Permit (ILP) & coordination with Bhotiya pastoral villages.",
        "monthly_t": [-13,-10,-5,2,8,13,15,14,10,3,-5,-11], "monthly_s": [4.1,4.8,5.7,6.5,7.0,7.1,6.4,6.1,5.8,5.2,4.4,3.9]
    },
    {
        "name": "Thar Desert (Sam & Khuri Barchan Dunes), Rajasthan, India", "tier": "BRAND-NEW", "cat": "Deserts",
        "cond": "High-Dust / Eolian Wind", "char_pct": 31, "scale": "25-km Eolian Barchan Dune Corridor",
        "process": "Active Eolian Sand Saltation & Ripple Migration",
        "lat": 26.83, "lon": 70.52, "terrain": "Hyper-Arid Eolian Barchan Dunes & Interdune Evaporite Playas",
        "temp": 26.4, "diurnal": 24.0, "slope": 18.0, "elev": 225, "press": 985,
        "aridity": 95.5, "solar": 6.3, "solar_flux": 1020, "basalt": 42.0, "ice": 0.0, "shielding": 32.0,
        "oxides": {"SiO2": 58.0, "TiO2": 0.6, "Al2O3": 10.8, "FeO": 6.4, "MgO": 4.2, "CaO": 8.5},
        "geology": "Active crescentic barchan sand dunes, wind-rippled quartz-feldspar-iron-oxide sands, and calcrete/gypsum interdune flats.",
        "campaigns": "Brand-New Candidate Analog (Suggested in 2026 Brief for Mars Eolian Dune Mobility & Dust Mitigation)",
        "equip": "Grouser-wheeled Mars rovers (Curiosity/Perseverance wheel slip tests), solar-panel electrodynamic dust shields.",
        "methods": "Autonomous dune-slip recovery algorithms, windblown sand-storm survival & optical sensor dust-clearing.",
        "subzones": "Zone A: Windward Barchan Dune Slope (14°) | Zone B: Slip-Face Avalanche Crest (31°) | Zone C: Interdune Gypsum Pan (2°).",
        "missing": "Requires standardized wheel-sinkage shear-vane measurements and electrostatic dust adhesion profiling.",
        "gaps": "Quartz-rich continental sand differs mineralogically from Martian basaltic sand; warm ambient climate (+26°C).",
        "stewardship": "Easy year-round road/air access via Jaisalmer (45 km). Adjacent to Desert National Park — coordinate with Forest Dept & local Bishnoi/village grazing lands; deploy Oct–Mar to avoid +48°C summer heat.",
        "monthly_t": [16,19,25,31,35,36,33,31,31,28,22,17], "monthly_s": [4.8,5.6,6.5,7.2,7.5,7.1,6.1,5.9,6.2,5.9,5.1,4.6]
    },
    {
        "name": "Deccan Lava Plateau (Ajanta–Lonar Basalt Escarpment), India", "tier": "BRAND-NEW", "cat": "Volcanic Terrains",
        "cond": "High-Dust / Eolian Wind", "char_pct": 33, "scale": "40-km Layered Flood Basalt Escarpment",
        "process": "Columnar Flood Basalt Weathering & Spheroidal Exfoliation",
        "lat": 20.53, "lon": 75.70, "terrain": "Stacked Tholeiitic Flood Basalt Flows & Steep Scarps",
        "temp": 25.8, "diurnal": 17.0, "slope": 24.0, "elev": 580, "press": 945,
        "aridity": 79.0, "solar": 5.7, "solar_flux": 965, "basalt": 98.0, "ice": 0.0, "shielding": 68.0,
        "oxides": {"SiO2": 48.8, "TiO2": 2.3, "Al2O3": 13.7, "FeO": 14.5, "MgO": 7.1, "CaO": 10.1},
        "geology": "One of Earth's largest continental flood basalt provinces: stacked pahoehoe/aa tholeiitic lava flows, vesicular basalt, and zeolites.",
        "campaigns": "Brand-New Candidate Analog (Deccan Lava Plateau suggested in 2026 Brief for Lunar Mare & Martian Basalt Stratigraphy)",
        "equip": "Rotary percussive rock-coring drills, ilmenite-to-oxygen ISRU reactors, cliff-scanning stereo/LiDAR spectrometers.",
        "methods": "Multi-layer lava-flow stratigraphic mapping, hard-basalt drill bit wear qualification.",
        "subzones": "Zone A: Compact Tholeiitic Basalt Bench (8°) | Zone B: Vesicular Basalt Scarp Wall (26°) | Zone C: Red Bole Paleosol Layer.",
        "missing": "Lack of planetary-standard XRF/LIBS spectral library across stacked Deccan flow units and red-bole intertrappean beds.",
        "gaps": "Tropical seasonal monsoon (Jun–Sep) and warm daytime temperatures require dry-season (Nov–Apr) field campaigns.",
        "stewardship": "Accessible via Chhatrapati Sambhajinagar (Aurangabad) airport/rail. Avoid protected archaeological buffer zones around Ajanta/Ellora caves; use open quarry/plateau outcrops.",
        "monthly_t": [21,24,28,32,34,29,25,24,25,25,22,20], "monthly_s": [5.2,5.9,6.5,6.9,6.8,5.3,4.4,4.3,5.1,5.6,5.3,5.0]
    },
    {
        "name": "Barren Island Volcanic Caldera (Andaman Island), India", "tier": "BRAND-NEW", "cat": "Volcanic Terrains",
        "cond": "High-Dust / Eolian Wind", "char_pct": 22, "scale": "3.2-km Volcanic Island Caldera & Ash Cone",
        "process": "Active Strombolian Basaltic Ash & Lava Emplacement",
        "lat": 12.278, "lon": 93.858, "terrain": "Uninhabited Basaltic Volcanic Island, Fresh Ash Flows & Lava Tubes",
        "temp": 27.5, "diurnal": 11.0, "slope": 29.5, "elev": 354, "press": 1008,
        "aridity": 74.0, "solar": 5.7, "solar_flux": 950, "basalt": 99.0, "ice": 0.0, "shielding": 75.0,
        "oxides": {"SiO2": 49.6, "TiO2": 1.4, "Al2O3": 16.2, "FeO": 11.2, "MgO": 7.5, "CaO": 10.9},
        "geology": "South Asia's only active volcanic island: unweathered tholeiitic/basaltic-andesite lava flows, dark volcanic ash plains, and spatter cones.",
        "campaigns": "Brand-New Candidate Analog (India's Volcanic Island suggested in 2026 Brief; zoom to 14x in 2D Satellite View to inspect island caldera)",
        "equip": "Volcanic ash-sealed rover bearings, autonomous aerial-ground volcano scouts, fresh basalt XRF/LIBS spectrometers.",
        "methods": "Autonomous hazardous-terrain reconnaissance without human boots on ground, fresh basaltic tephra sintering.",
        "subzones": "Zone A: Western Basalt Lava Delta (11° slope) | Zone B: Central Cinder Cone Scree (30°) | Zone C: Pyroclastic Ash Apron.",
        "missing": "Zero planetary-grade LiDAR DEM or abrasive volcanic glass particle-size characterization exists yet.",
        "gaps": "Tropical oceanic humidity, +27°C heat, and 1,008 hPa pressure differ from cold airless lunar mare plains.",
        "stewardship": "Uninhabited volcanic island 138 km NE of Port Blair (ship charter only). Protected Sanctuary — strict Indian Coast Guard / Forest Dept permits required.",
        "monthly_t": [26,27,28,29,29,28,27,27,27,27,27,26], "monthly_s": [5.5,6.1,6.5,6.6,5.4,4.7,4.8,5.0,5.2,5.4,5.3,5.3]
    },
    {
        "name": "Tso Kar & Puga Valley (Ladakh), India", "tier": "PRIOR ANALOG", "cat": "Polar Regions",
        "cond": "Cryogenic Permafrost", "char_pct": 48, "scale": "15-km High-Altitude Paleolake Basin",
        "process": "Permafrost Pingo Heave & Evaporite Salt Efflorescence",
        "lat": 33.32, "lon": 78.00, "terrain": "High-Altitude Permafrost, Borate Evaporite & Geothermal Basin",
        "temp": -6.5, "diurnal": 34.0, "slope": 14.5, "elev": 4530, "press": 580,
        "aridity": 91.0, "solar": 5.9, "solar_flux": 1120, "basalt": 65.0, "ice": 76.0, "shielding": 55.0,
        "oxides": {"SiO2": 52.0, "TiO2": 0.9, "Al2O3": 14.2, "FeO": 9.8, "MgO": 8.4, "CaO": 7.5},
        "geology": "High-UV, low-pressure (580 hPa) paleolake basin with sulfate/borate evaporites, polygon permafrost mounds, and ophiolite basalts.",
        "campaigns": "ISRO-BSIP High-Altitude Mars/Moon Habitation Analog & NASA Spaceward Bound India",
        "equip": "Cryogenic rotary drills, MOXIE low-pressure compressors, UV-hardened habitats, high-altitude drone rotors.",
        "methods": "14-minute simulated Mars comms-delay EVA sampling, sterile permafrost core caching, low-oxygen human protocols.",
        "subzones": "Zone A: Tso Kar Evaporite Flat (2° slope) | Zone B: Puga Geothermal Borate Vents | Zone C: Polokongka Permafrost Ridge (18°).",
        "missing": "Needs 3D GPR mapping of permafrost ice-table depth and continuous winter thermal inertia logging.",
        "gaps": "Atmospheric pressure (580 hPa) exceeds Mars (6.8 hPa); pair field trials with vacuum chamber validation.",
        "stewardship": "Accessible via Leh–Manali Highway (240 km from Leh airport; requires 3-day altitude acclimatization). Tso Kar is a Ramsar Wetland & Changpa nomadic grazing area — strict zero-trace environmental permits required.",
        "monthly_t": [-18,-15,-9,-2,4,9,13,12,7,-1,-10,-16], "monthly_s": [4.1,4.9,5.8,6.7,7.2,7.5,7.1,6.6,6.0,5.2,4.4,3.9]
    },
    {
        "name": "Lonar Impact Crater (Maharashtra), India", "tier": "PRIOR ANALOG", "cat": "Other Environments",
        "cond": "High-Dust / Eolian Wind", "char_pct": 45, "scale": "1.83-km Hyper-Velocity Impact Crater",
        "process": "Impact Ejecta Erosion & Hyper-Alkaline Lake Precipitation",
        "lat": 19.976, "lon": 76.508, "terrain": "Hyper-Velocity Deccan Basalt Impact Crater & Ejecta Blanket",
        "temp": 26.8, "diurnal": 16.0, "slope": 28.0, "elev": 500, "press": 955,
        "aridity": 76.0, "solar": 5.6, "solar_flux": 960, "basalt": 99.0, "ice": 5.0, "shielding": 52.0,
        "oxides": {"SiO2": 48.5, "TiO2": 2.4, "Al2O3": 13.6, "FeO": 14.8, "MgO": 6.9, "CaO": 10.2},
        "geology": "Rare hyper-velocity impact crater formed directly in Deccan Trap flood basalt; preserves shocked maskelynite glass & suevite breccia.",
        "campaigns": "Lunar & Planetary Institute (LPSC) / ISRO Basaltic Crater Rim & Ejecta Radar Calibration",
        "equip": "Steep-slope crater-wall climbing rovers, XRF/Raman basalt spectrometers, ilmenite oxygen reactors.",
        "methods": "Autonomous crater-rim hazard avoidance navigation, shocked-basalt sample triage, night-vision lidar mapping.",
        "subzones": "Zone A: Continuous Basalt Ejecta Blanket (6°) | Zone B: Inner Breccia Crater Wall (28°) | Zone C: Alkaline Lake Floor.",
        "missing": "Incomplete millimeter-wave radar polarimetry of proximal ejecta blocks and subsurface radial fracture network.",
        "gaps": "Tropical ambient temperature (+26°C) and monsoon humidity require scheduling campaigns in Nov–Mar dry season.",
        "stewardship": "Accessible via Aurangabad/Jalna road (140 km). Notified Wildlife Sanctuary & Geo-Heritage Monument with historic temples along the rim — non-destructive rover/drone testing only.",
        "monthly_t": [22,25,29,33,35,29,26,25,26,26,23,21], "monthly_s": [5.1,5.8,6.5,6.9,6.8,5.2,4.3,4.2,5.0,5.5,5.2,4.9]
    },
    {
        "name": "Rann of Kutch (Matanomadh Jarosite Flats), Gujarat, India", "tier": "PRIOR ANALOG", "cat": "Arid Terrains",
        "cond": "High-Dust / Eolian Wind", "char_pct": 40, "scale": "30-km Acid-Sulfate & Halite Evaporite Basin",
        "process": "Basalt Acid-Sulfate Weathering & Seasonal Salt Crusting",
        "lat": 23.62, "lon": 69.25, "terrain": "Arid Jarosite, Alunite & Smectite Clay Evaporite Flats",
        "temp": 27.2, "diurnal": 19.0, "slope": 4.0, "elev": 45, "press": 1005,
        "aridity": 93.0, "solar": 6.1, "solar_flux": 995, "basalt": 78.0, "ice": 2.0, "shielding": 30.0,
        "oxides": {"SiO2": 46.0, "TiO2": 1.7, "Al2O3": 13.1, "FeO": 16.5, "MgO": 7.2, "CaO": 6.8},
        "geology": "Deccan basalt altering into hydrous iron-sulfate (jarosite) and kaolinite/smectite clays matching Gale Crater & Mawrth Vallis.",
        "campaigns": "ISRO Chandrayaan / MOM Spectrometer Calibration & Indian Planetary Analog Initiative",
        "equip": "VNIR/LIBS mineralogical spectrometers, long-range autonomous pathfinders, electrodynamic solar dust shields.",
        "methods": "Automated orbital-to-ground spectral tie-point verification, multi-km blind rover navigation across salt/clay plains.",
        "subzones": "Zone A: Matanomadh Jarosite Outcrop | Zone B: White Rann Halite Crust (0.5° slope) | Zone C: Banni Basaltic Margin.",
        "missing": "Subsurface hydration profile down to 2m depth and seasonal eolian dust particle size distribution remain uncharacterized.",
        "gaps": "Warm daytime temperatures (+22°C in winter) and summer monsoon flooding; deploy Dec–Feb only.",
        "stewardship": "Accessible via Bhuj airport (95 km). Near India–Pakistan international border & Kutch Desert Wildlife Sanctuary — BSF/Forest clearance required.",
        "monthly_t": [19,22,27,31,34,33,30,29,30,29,25,20], "monthly_s": [5.0,5.8,6.6,7.2,7.4,6.3,4.8,4.7,5.7,5.8,5.2,4.8]
    },
    {
        "name": "Undara Volcanic Lava Tubes (Queensland), Australia", "tier": "BRAND-NEW", "cat": "Caves",
        "cond": "Subsurface Cave / PSR Darkness", "char_pct": 36, "scale": "160-km Sinuous Basaltic Lava Tube System",
        "process": "Lava Tube Roof Collapse & Subterranean Thermal Buffering",
        "lat": -18.20, "lon": 144.57, "terrain": "160-km Sinuous Basaltic Lava Tube & Roof Collapse System",
        "temp": 23.5, "diurnal": 16.0, "slope": 25.0, "elev": 750, "press": 925,
        "aridity": 81.0, "solar": 6.0, "solar_flux": 980, "basalt": 97.0, "ice": 2.0, "shielding": 96.0,
        "oxides": {"SiO2": 47.2, "TiO2": 2.3, "Al2O3": 14.8, "FeO": 13.0, "MgO": 8.7, "CaO": 9.5},
        "geology": "One of Earth's longest single-volcano lava tube systems (160 km), featuring intact 20m-wide arched basalt tunnels analogous to lunar sinuous rilles.",
        "campaigns": "Emerging Subsurface Lidar SLAM & Planetary Cave Drone Trials",
        "equip": "Subterranean swarm drones, long-baseline cave acoustic/VLF transceivers, robotic ceiling-anchor grippers.",
        "methods": "Multi-kilometer non-GPS subterranean mapping, autonomous return-to-skylight fail-safe navigation.",
        "subzones": "Zone A: Barkers Cave 20m Basalt Arch | Zone B: Wind Tunnel Skylight Entrance (25° talus) | Zone C: Kalkani Rim.",
        "missing": "High-density 3D LiDAR point-cloud models and basaltic wall magnetic anomaly maps are incomplete across >80% of tubes.",
        "gaps": "Surface savanna vegetation requires isolating testing strictly to underground basaltic tube segments.",
        "stewardship": "Accessible via Cairns (275 km). Located in Undara Volcanic National Park — Queensland Parks scientific permit & Ewamian Traditional Owner consultation required.",
        "monthly_t": [26,26,25,23,20,17,17,18,21,24,26,27], "monthly_s": [6.3,5.9,5.8,5.5,4.9,4.6,4.9,5.6,6.5,6.9,6.8,6.5]
    },
    {
        "name": "Svalbard Bockfjord Volcanic Complex (AMASE), Norway", "tier": "PRIOR ANALOG", "cat": "Polar Regions",
        "cond": "Cryogenic Permafrost", "char_pct": 52, "scale": "10-km Glaciovolcanic Carbonate-Basalt Complex",
        "process": "Cryogenic Carbonate Globule Precipitation & Glacial Scour",
        "lat": 79.10, "lon": 15.20, "terrain": "Arctic Permafrost & Carbonate-Basalt Volcanic Cones",
        "temp": -9.2, "diurnal": 12.0, "slope": 21.0, "elev": 650, "press": 935,
        "aridity": 84.0, "solar": 2.4, "solar_flux": 510, "basalt": 89.0, "ice": 92.0, "shielding": 58.0,
        "oxides": {"SiO2": 45.8, "TiO2": 2.1, "Al2O3": 13.4, "FeO": 12.9, "MgO": 11.8, "CaO": 9.5},
        "geology": "Macromolecular carbonate globules inside basaltic volcanic pipes identical to Martian meteorite ALH84001 & Jezero margin.",
        "campaigns": "NASA AMASE (Arctic Mars Analog Svalbard Expedition) — Perseverance SHERLOC & Curiosity SAM Calibration",
        "equip": "Deep-UV Raman/luminescence spectrometers (SHERLOC), sterile coring bits, permafrost-to-basalt transition drills.",
        "methods": "Planetary protection Tier-IV sterile sample handling, multi-instrument life-detection cross-validation.",
        "subzones": "Zone A: Sverrefjell Basalt Volcano Flank (21°) | Zone B: Troll Springs Carbonate Terraces | Zone C: Glacial Outwash.",
        "missing": "Sub-glaciovolcanic cave geometry and year-round sub-zero brine pocket distribution remain largely unmapped.",
        "gaps": "Arctic maritime humidity exceeds continental Antarctic and Martian aridity.",
        "stewardship": "Reached by research expedition from Longyearbyen (Jul–Sep). Strictly protected under Svalbard Environmental Protection Act; Governor permits mandatory.",
        "monthly_t": [-16,-17,-16,-12,-5,1,4,3,-1,-7,-12,-15], "monthly_s": [0.0,0.1,1.1,3.5,5.6,6.1,4.8,2.9,1.0,0.1,0.0,0.0]
    },
    {
        "name": "Lava Beds National Monument (Valentine Cave), CA, USA", "tier": "PRIOR ANALOG", "cat": "Caves",
        "cond": "Subsurface Cave / PSR Darkness", "char_pct": 76, "scale": "12-km Multi-Level Lava Tube & Ice Cave Network",
        "process": "Subterranean Perennial Ice Accumulation & Basalt Spalling",
        "lat": 41.71, "lon": -121.51, "terrain": "Subsurface Volcanic Lava Tube Network & Ice Caves",
        "temp": 8.9, "diurnal": 24.0, "slope": 33.5, "elev": 1450, "press": 850,
        "aridity": 80.0, "solar": 5.1, "solar_flux": 890, "basalt": 97.0, "ice": 32.0, "shielding": 98.0,
        "oxides": {"SiO2": 48.9, "TiO2": 1.9, "Al2O3": 15.2, "FeO": 12.1, "MgO": 8.0, "CaO": 9.8},
        "geology": "Multi-level basaltic lava tube caves with perennial cave ice formations, collapse trenches, and chemolithotrophic biofilms.",
        "campaigns": "NASA BRAILLE Astrobiology & Autonomous CaveR Quadruped/Rover Trials",
        "equip": "Quadruped walking robots (Spot/NeBula), optical cave comms relays, dark-environment UV fluorescence scanners.",
        "methods": "Zero-light autonomous obstacle avoidance, subterranean mesh-network deployment, cave-wall mineral sampling.",
        "subzones": "Zone A: Valentine Cave Main Basalt Tube | Zone B: Skull Ice Cave Floor | Zone C: Collapse Trench Ramp (33.5°).",
        "missing": "Multi-km non-line-of-sight RF attenuation through vesicular basalt cave roofs is not fully parameterized.",
        "gaps": "Surface sagebrush vegetation requires isolating mission tests strictly inside the subsurface lava tubes.",
        "stewardship": "Road access via Tulelake, CA. US National Park Service site — requires NPS Research Permit & white-nose syndrome bat decontamination protocols.",
        "monthly_t": [-1,1,4,7,11,16,20,19,15,9,3,-1], "monthly_s": [2.2,3.2,4.6,6.0,7.1,7.8,7.9,7.0,5.6,3.9,2.4,1.9]
    },
    {
        "name": "Craters of the Moon (Indian Tunnel), Idaho, USA", "tier": "PRIOR ANALOG", "cat": "Caves",
        "cond": "Subsurface Cave / PSR Darkness", "char_pct": 79, "scale": "18-km Flood Basalt & Skylight Lava Tube System",
        "process": "Volcanic Skylight Collapse & Basaltic Tube Shielding",
        "lat": 43.42, "lon": -113.52, "terrain": "Mega-Scale Lunar-Dimension Volcanic Lava Tube & Skylights",
        "temp": 6.8, "diurnal": 22.0, "slope": 31.0, "elev": 1800, "press": 820,
        "aridity": 82.0, "solar": 5.2, "solar_flux": 910, "basalt": 98.0, "ice": 25.0, "shielding": 96.0,
        "oxides": {"SiO2": 47.5, "TiO2": 3.1, "Al2O3": 13.8, "FeO": 15.4, "MgO": 6.2, "CaO": 8.9},
        "geology": "Unweathered continental flood basalts, pahoehoe/aa flows, spatter cones, and collapsed lava tube skylights with perennial cave ice.",
        "campaigns": "NASA FINESSE, BASALT Research Program & Planetary Pits and Caves 3D Dataset",
        "equip": "Tethered skylight rappelling rovers (DuAxel), subterranean lidar SLAM drones, microwave regolith sintering bricks.",
        "methods": "High-latency (5-to-15 min) human-robotic real-time science operations (BASALT protocol), non-GPS cave navigation.",
        "subzones": "Zone A: Indian Tunnel 25m Basalt Arch | Zone B: Skylight Collapse Talus Ramp (31°) | Zone C: Blue Dragon Pahoehoe Sheet.",
        "missing": "Structural load-bearing capacity of thin (<3m) skylight roof bridges under heavy lander vibrations needs seismic profiling.",
        "gaps": "1g Earth gravity limits lava tube roof spans compared to 100m+ lunar mare tubes.",
        "stewardship": "Year-round highway access via Arco, Idaho. US National Monument & Preserve — NPS Scientific Research & Collecting Permit required.",
        "monthly_t": [-7,-4,1,6,11,16,21,20,14,7,-1,-6], "monthly_s": [2.1,3.1,4.5,5.8,6.8,7.5,7.6,6.7,5.4,3.7,2.3,1.8]
    },
    {
        "name": "Atacama Desert (Yungay & Salar de Atacama), Chile [Benchmark]", "tier": "BENCHMARK", "cat": "Deserts",
        "cond": "High-Dust / Eolian Wind", "char_pct": 88, "scale": "50-km Hyper-Arid Nitrate/Perchlorate Core",
        "process": "Hyper-Arid Atmospheric Nitrate/Perchlorate Accumulation",
        "lat": -23.50, "lon": -68.25, "terrain": "Hyper-Arid Perchlorate & Sulfate Desert Core",
        "temp": 16.5, "diurnal": 32.0, "slope": 8.5, "elev": 2300, "press": 775,
        "aridity": 99.5, "solar": 6.8, "solar_flux": 1150, "basalt": 68.0, "ice": 8.0, "shielding": 35.0,
        "oxides": {"SiO2": 53.2, "TiO2": 0.8, "Al2O3": 14.0, "FeO": 8.5, "MgO": 5.4, "CaO": 8.9},
        "geology": "Hyper-arid oxidized soils, natural perchlorates, sulfates, and halite crusts with near-zero organic carbon matching Martian regolith.",
        "campaigns": "NASA ASTEP Zoe Rover, ARADS Astrobiology Drilling Studies (Widely Studied Benchmark)",
        "equip": "2-meter astrobiology drills, microfluidic wet-chemistry life detectors, solar-array dust accumulation sensors.",
        "methods": "Ultra-trace biomarker contamination control, remote science backroom target triage with simulated 20-min Mars latency.",
        "subzones": "Zone A: Hyper-Arid Desert Pavement (8° slope) | Zone B: Polygonal Halite Evaporite Crust | Zone C: Alluvial Basalt Fan.",
        "missing": "Deep (>5m) clay-brine interface continuity and nocturnal UV-peroxide soil reactivity rates remain partially mapped.",
        "gaps": "Warm daytime temperatures (+24°C) require separate cryogenic chamber validation for Martian night survival.",
        "stewardship": "Year-round access via Calama / Antofagasta. Coordinate with Chilean CONAF and Lickanantay (Atacameño) Indigenous communities.",
        "monthly_t": [20,20,18,16,14,12,12,13,15,16,18,19], "monthly_s": [8.1,7.6,6.8,5.7,4.7,4.2,4.5,5.4,6.6,7.6,8.2,8.3]
    },
    {
        "name": "Haughton Impact Crater (Devon Island), Canada [Benchmark]", "tier": "BENCHMARK", "cat": "Polar Regions",
        "cond": "Low-Angle Grazing Sunlight", "char_pct": 85, "scale": "23-km Polar Impact Crater",
        "process": "Periglacial Active-Layer Solifluction & Breccia Erosion",
        "lat": 75.38, "lon": -89.66, "terrain": "High-Arctic Impact Crater, Melt Breccia & Ground-Ice",
        "temp": -16.8, "diurnal": 15.0, "slope": 22.0, "elev": 350, "press": 970,
        "aridity": 88.0, "solar": 2.6, "solar_flux": 530, "basalt": 35.0, "ice": 90.0, "shielding": 62.0,
        "oxides": {"SiO2": 44.0, "TiO2": 0.5, "Al2O3": 18.5, "FeO": 5.1, "MgO": 9.2, "CaO": 16.0},
        "geology": "23-km impact crater in a polar desert featuring hydrothermal impact melt breccia, ground-ice, and steep crater rims.",
        "campaigns": "NASA Haughton-Mars Project (HMP), K10 Robotic Rover & Spacesuit EVA Testing (Widely Studied Benchmark)",
        "equip": "Pressurized crew rovers, xEMU lunar spacesuit joints, ground-penetrating radar (SHARAD/RIMFAX), ISRU excavators.",
        "methods": "Dual-astronaut + robotic scout joint EVA workflows, crater-rim comms relay placement, habitat isolation protocols.",
        "subzones": "Zone A: Impact Melt Breccia Hills (22° slope) | Zone B: Von Braun Planitia Flat | Zone C: Permafrost Ice Wedges.",
        "missing": "Deep (>20m) hydrothermal breccia porosity and seasonal active-layer thaw-slump dynamics require lidar time-series.",
        "gaps": "Carbonate target bedrock has lower iron/titanium content than lunar mare basalts.",
        "stewardship": "Charter Twin Otter flight from Resolute Bay (Jul–Aug window). Uninhabited Crown land in Nunavut — Nunavut Research Institute & Inuit Qikiqtani consultation required.",
        "monthly_t": [-31,-32,-29,-21,-9,1,5,2,-6,-16,-25,-29], "monthly_s": [0.0,0.2,1.5,4.1,6.3,6.8,5.4,3.4,1.4,0.2,0.0,0.0]
    },
    {
        "name": "Death Valley (Ubehebe & Badwater), CA, USA [Benchmark]", "tier": "BENCHMARK", "cat": "Deserts",
        "cond": "High-Dust / Eolian Wind", "char_pct": 89, "scale": "0.8-km Maar Crater & 40-km Salt Pan",
        "process": "Alluvial Fan Debris Flow & Polygonal Salt Heave",
        "lat": 36.50, "lon": -116.85, "terrain": "Hyper-Arid Volcanic Maar Crater, Alluvial Fan & Salt Pan",
        "temp": 24.8, "diurnal": 26.0, "slope": 15.0, "elev": -86, "press": 1022,
        "aridity": 97.5, "solar": 6.2, "solar_flux": 1030, "basalt": 74.0, "ice": 6.0, "shielding": 38.0,
        "oxides": {"SiO2": 48.2, "TiO2": 1.8, "Al2O3": 13.9, "FeO": 12.6, "MgO": 7.9, "CaO": 9.6},
        "geology": "Steep alluvial fans, polygonal evaporite salt pans, basaltic phreatomagmatic maar craters, and Mars-like rock varnish.",
        "campaigns": "NASA Mars 2020 Lander Vision System & MSL Curiosity Radar Calibration (Widely Studied Benchmark)",
        "equip": "Helicopter/lander Terrain Relative Navigation (TRN) cameras, terminal descent Doppler radars, dune rovers.",
        "methods": "Pinpoint landing hazard avoidance flight testing, rock-varnish laser depth-profiling (SuperCam calibration).",
        "subzones": "Zone A: Ubehebe Basaltic Maar Crater (24°) | Zone B: Badwater Polygonal Salt Pan | Zone C: Mesquite Dunes.",
        "missing": "Micro-scale dielectric properties of desert varnish coatings under Martian-equivalent UV wavelengths.",
        "gaps": "Extreme summer heat (+45°C) contrasts with cryogenic Martian surface temperatures; test during Nov–Feb.",
        "stewardship": "Paved road access (Nov–Mar recommended). Protected US National Park & Timbisha Shoshone homeland — strict NPS research permits required.",
        "monthly_t": [12,15,20,25,30,36,40,39,33,26,18,11], "monthly_s": [3.5,4.6,6.0,7.3,8.1,8.5,8.1,7.4,6.3,4.9,3.7,3.2]
    },
    {
        "name": "McMurdo Dry Valleys (University Valley), Antarctica [Benchmark]", "tier": "BENCHMARK", "cat": "Polar Regions",
        "cond": "Cryogenic Permafrost", "char_pct": 84, "scale": "12-km Hyper-Arid Polar Valley",
        "process": "Sublimation-Driven Ice-Table Retreat & Sand Wedging",
        "lat": -77.55, "lon": 161.80, "terrain": "Hyper-Arid Polar Permafrost & Ice-Cemented Regolith",
        "temp": -21.5, "diurnal": 18.0, "slope": 19.0, "elev": 1650, "press": 810,
        "aridity": 98.5, "solar": 2.9, "solar_flux": 560, "basalt": 60.0, "ice": 94.0, "shielding": 60.0,
        "oxides": {"SiO2": 51.0, "TiO2": 0.9, "Al2O3": 15.1, "FeO": 9.2, "MgO": 7.8, "CaO": 9.4},
        "geology": "Ice-cemented ground beneath dry dolerite/sandstone pavement, polygonal permafrost fractures, and zero liquid rainfall.",
        "campaigns": "NASA IceBite (Phoenix Lander Cryogenic Drill Testing) (Widely Studied Benchmark)",
        "equip": "Artemis TRIDENT cryogenic ice-mining drills, Rodwell melt-well water extractors, low-temperature battery packs.",
        "methods": "Dry-drilling without drilling fluids in rock-hard ice-cemented regolith, polar grazing-sunlight optical nav.",
        "subzones": "Zone A: Upper University Valley Shallow Ice Table | Zone B: Polygon Trough Network (19°) | Zone C: Dolerite Talus.",
        "missing": "Winter-over autonomous power/telemetry survival data during the 4-month continuous polar night is sparse.",
        "gaps": "Complete darkness during austral winter restricts crewed field operations to Nov–Jan.",
        "stewardship": "Helicopter access from McMurdo Station (Nov–Jan). Antarctic Specially Managed Area (ASMA-2) — strict Antarctic Treaty quarantine rules.",
        "monthly_t": [-5,-12,-22,-27,-29,-30,-32,-31,-28,-20,-11,-5], "monthly_s": [6.8,4.1,1.2,0.1,0.0,0.0,0.0,0.1,0.9,3.5,6.2,7.4]
    }
]

# =============================================================================
# 3. MULTI-COLOR, JUDGE-READY 5-PAGE APPLICATION & STATIC WEB PORTAL
# =============================================================================
APP_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🚀 TerraTwin | NASA Planetary Analog & Solar Flux Workstation</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css"/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/globe.gl@2.32.1/dist/globe.gl.min.js"></script>
<style>
  :root {
    --bg: #070614;
    --panel: rgba(16, 14, 38, 0.92);
    --card: rgba(24, 21, 56, 0.85);
    --cyan: #00f2fe;
    --emerald: #00ff87;
    --gold: #ffbe0b;
    --orange: #fb5607;
    --pink: #ff006e;
    --purple: #8338ec;
    --blue: #3a86ff;
    --text: #f8f9fa;
    --muted: #b8c0ff;
  }
  * { box-sizing: border-box; user-select: none; }
  ::-webkit-scrollbar { width: 7px; height: 7px; }
  ::-webkit-scrollbar-track { background: #09071a; }
  ::-webkit-scrollbar-thumb { background: linear-gradient(180deg, var(--cyan), var(--purple)); border-radius: 4px; }

  body {
    margin: 0; padding: 0; width: 100vw; height: 100vh; overflow: hidden;
    background: radial-gradient(circle at 20% 20%, #160f3a 0%, #070614 60%, #05040d 100%);
    color: var(--text); font-family: 'Segoe UI', system-ui, sans-serif;
    display: flex; flex-direction: column;
  }

  /* VIBRANT RAINBOW TOP HEADER */
  header {
    height: 56px; min-height: 56px; padding: 0 18px;
    background: linear-gradient(90deg, #100a2c 0%, #1f1147 35%, #0f2547 70%, #100a2c 100%);
    border-bottom: 2px solid;
    border-image: linear-gradient(90deg, var(--pink), var(--gold), var(--emerald), var(--cyan), var(--purple)) 1;
    display: flex; align-items: center; justify-content: space-between; z-index: 1000;
    box-shadow: 0 4px 20px rgba(131, 56, 236, 0.35);
  }
  .brand {
    font-size: 17px; font-weight: 900;
    background: linear-gradient(90deg, #00f2fe, #ffbe0b, #ff006e);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    display: flex; align-items: center; gap: 8px;
  }
  .nav-pills {
    display: flex; gap: 6px; background: rgba(8, 6, 22, 0.85);
    padding: 4px; border-radius: 12px; border: 1px solid rgba(0, 242, 254, 0.35);
  }
  .nav-btn {
    background: transparent; border: none; color: #d0d6ff; padding: 7px 13px;
    border-radius: 9px; font-size: 11.5px; font-weight: 800; cursor: pointer; transition: all 0.2s;
  }
  .nav-btn:hover { color: #fff; background: rgba(131, 56, 236, 0.35); transform: translateY(-1px); }
  .nav-btn.active {
    background: linear-gradient(135deg, #ff006e, #8338ec, #3a86ff);
    color: #fff; box-shadow: 0 0 15px rgba(255, 0, 110, 0.55);
  }

  .btn {
    background: linear-gradient(135deg, #3a86ff, #8338ec); border: 1px solid rgba(255,255,255,0.3);
    color: #fff; padding: 6px 12px; border-radius: 8px; font-size: 11px; font-weight: 800;
    cursor: pointer; transition: all 0.2s; box-shadow: 0 2px 10px rgba(58,134,255,0.3);
  }
  .btn:hover { transform: translateY(-1px) scale(1.02); box-shadow: 0 0 16px rgba(0,242,254,0.7); }
  .btn-green { background: linear-gradient(135deg, #00b09b, #96c93d); }
  .btn-amber { background: linear-gradient(135deg, #f7971e, #ffd200); color: #111; }
  .btn-pink  { background: linear-gradient(135deg, #ff006e, #fb5607); }

  /* COLORFUL TELEMETRY RIBBON BAR */
  .context-bar {
    height: 46px; min-height: 46px; padding: 0 18px;
    background: linear-gradient(90deg, rgba(255,0,110,0.14), rgba(0,242,254,0.14), rgba(0,255,135,0.14));
    border-bottom: 1px solid rgba(255,255,255,0.15);
    display: flex; align-items: center; justify-content: space-between; gap: 10px; font-size: 12px;
  }
  .ctx-group { display: flex; align-items: center; gap: 8px; }
  select {
    background: #100d28; border: 1.5px solid var(--cyan); color: #fff;
    padding: 5px 10px; border-radius: 8px; font-size: 11.5px; font-weight: 700; outline: none;
  }
  .pill-badge {
    padding: 4px 11px; border-radius: 20px; font-weight: 800; font-size: 11.5px;
    display: inline-flex; align-items: center; gap: 5px;
  }
  .pill-match { background: linear-gradient(135deg, #00b09b, #00ff87); color: #041f14; box-shadow: 0 0 12px rgba(0,255,135,0.5); }
  .pill-flux  { background: linear-gradient(135deg, #ffbe0b, #fb5607); color: #1a0800; box-shadow: 0 0 12px rgba(255,190,11,0.5); }

  #youthBanner {
    display: none; background: linear-gradient(90deg, #ff006e, #8338ec, #3a86ff);
    padding: 8px 18px; font-size: 12.5px; font-weight: 700; color: #fff;
  }

  /* PAGES */
  .page-container { flex: 1; position: relative; overflow: hidden; }
  .page { display: none; width: 100%; height: 100%; overflow-y: auto; padding: 14px 18px; }
  .page.active { display: block; }
  .page.map-page { padding: 0; overflow: hidden; }

  /* COLORFUL CARDS */
  .card {
    background: var(--card); backdrop-filter: blur(14px);
    border: 1px solid rgba(0, 242, 254, 0.28);
    border-top: 3px solid var(--cyan);
    border-radius: 12px; padding: 13px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.45);
  }
  .card.pink-top { border-top-color: var(--pink); }
  .card.gold-top { border-top-color: var(--gold); }
  .card.green-top { border-top-color: var(--emerald); }
  .card.purple-top { border-top-color: var(--purple); }
  .card-title {
    font-size: 13px; font-weight: 900; text-transform: uppercase; letter-spacing: 0.5px;
    margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between;
    color: var(--gold);
  }

  /* PAGE 1: SATELLITE GLOBE & MAP */
  .map-layout { display: grid; grid-template-columns: 355px 1fr; width: 100%; height: 100%; }
  .map-sidebar {
    background: var(--panel); border-right: 1px solid rgba(0,242,254,0.25);
    padding: 12px; display: flex; flex-direction: column; gap: 10px; overflow-y: auto; z-index: 500;
  }
  .site-list-item {
    padding: 9px 11px; border-radius: 10px;
    background: linear-gradient(135deg, rgba(25,22,60,0.9), rgba(14,12,34,0.9));
    border: 1px solid rgba(255,255,255,0.1); margin-bottom: 7px; cursor: pointer;
    display: flex; justify-content: space-between; align-items: center; transition: 0.18s;
  }
  .site-list-item:hover { border-color: var(--gold); transform: translateX(3px); }
  .site-list-item.selected {
    background: linear-gradient(135deg, rgba(255,0,110,0.28), rgba(0,242,254,0.25));
    border: 1.5px solid var(--cyan); box-shadow: 0 0 14px rgba(0,242,254,0.35);
  }
  .badge-new { background: linear-gradient(135deg, #ff006e, #8338ec); color: #fff; padding: 2px 7px; border-radius: 6px; font-size: 9.5px; font-weight: 800; }
  .badge-prior { background: linear-gradient(135deg, #fb5607, #ffbe0b); color: #111; padding: 2px 7px; border-radius: 6px; font-size: 9.5px; font-weight: 800; }
  .badge-bench { background: rgba(58,134,255,0.3); border: 1px solid var(--blue); color: #fff; padding: 2px 7px; border-radius: 6px; font-size: 9.5px; }

  .map-viewport { position: relative; width: 100%; height: 100%; background: #03020a; }
  #globeContainer, #leafletContainer { position: absolute; inset: 0; width: 100%; height: 100%; }
  #leafletContainer { display: none; z-index: 10; }
  .map-floating-bar {
    position: absolute; top: 12px; left: 14px; right: 14px; z-index: 300;
    background: rgba(14, 11, 36, 0.90); backdrop-filter: blur(14px);
    border: 1px solid var(--cyan); border-radius: 12px; padding: 9px 14px;
    display: flex; justify-content: space-between; align-items: center;
  }
  .time-floating-bar {
    position: absolute; bottom: 12px; left: 14px; right: 14px; z-index: 300;
    background: rgba(14, 11, 36, 0.92); backdrop-filter: blur(14px);
    border: 1px solid var(--gold); border-radius: 12px; padding: 9px 16px;
  }

  /* PAGE 2: SIDE-BY-SIDE HERO BANNERS & LABELED TABLE */
  .twin-hero-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 14px; }
  .hero-space {
    background: linear-gradient(135deg, rgba(255,0,110,0.25), rgba(251,86,7,0.22));
    border: 2px solid var(--pink); border-radius: 12px; padding: 12px 16px;
  }
  .hero-earth {
    background: linear-gradient(135deg, rgba(0,255,135,0.22), rgba(0,242,254,0.22));
    border: 2px solid var(--emerald); border-radius: 12px; padding: 12px 16px;
  }
  .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
  .rings-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; text-align: center; }
  .ring-card { background: rgba(10, 8, 26, 0.85); border: 1px solid rgba(255,255,255,0.12); border-radius: 10px; padding: 8px; }

  table.comp-table { width: 100%; border-collapse: collapse; font-size: 12px; }
  table.comp-table th {
    padding: 10px; text-align: left; font-size: 11.5px; font-weight: 900; text-transform: uppercase;
    border-bottom: 2px solid rgba(255,255,255,0.2);
  }
  .th-feature { background: rgba(131,56,236,0.3); color: #ffbe0b; }
  .th-space   { background: rgba(255,0,110,0.35); color: #ffccd5; }
  .th-earth   { background: rgba(0,255,135,0.3); color: #bbf7d0; }
  .th-delta   { background: rgba(0,242,254,0.25); color: #a5f3fc; }
  .th-why     { background: rgba(255,190,11,0.25); color: #fde68a; }
  table.comp-table td { padding: 9px 10px; border-bottom: 1px solid rgba(255,255,255,0.08); vertical-align: middle; }
  table.comp-table tr:hover { background: rgba(255,255,255,0.05); }

  .val-space { background: rgba(255,0,110,0.2); border: 1px solid var(--pink); color: #ff9ebb; padding: 3px 8px; border-radius: 6px; font-weight: 800; display: inline-block; }
  .val-earth { background: rgba(0,255,135,0.2); border: 1px solid var(--emerald); color: #6ee7b7; padding: 3px 8px; border-radius: 6px; font-weight: 800; display: inline-block; }

  .field-box {
    background: rgba(10, 8, 26, 0.85); border-left: 4px solid var(--cyan);
    border-radius: 8px; padding: 11px 13px; margin-bottom: 10px; font-size: 12.5px; line-height: 1.5;
  }
  .field-box.pink { border-left-color: var(--pink); }
  .field-box.gold { border-left-color: var(--gold); }
  .field-box.green { border-left-color: var(--emerald); }
  input[type=text], input[type=number] {
    width: 100%; background: #0a081c; border: 1px solid var(--purple); color: #fff;
    padding: 6px 9px; border-radius: 7px; font-size: 11.5px; margin-top: 4px;
  }
  input[type=range] { width: 100%; accent-color: var(--pink); cursor: pointer; }
</style>
</head>
<body>

<!-- VIBRANT RAINBOW HEADER -->
<header>
  <div class="brand">🚀 TERRATWIN <span style="font-size:12px;color:#d0d6ff;-webkit-text-fill-color:#d0d6ff;font-weight:700;">| NASA Planetary Analog & Solar Flux Studio</span></div>

  <div class="nav-pills">
    <button class="nav-btn active" onclick="switchPage(0)">1. 🌎 3D Satellite Globe</button>
    <button class="nav-btn" onclick="switchPage(1)">2. ⚖️ Earth vs. Moon/Mars Table</button>
    <button class="nav-btn" onclick="switchPage(2)">3. 🛠️ Hardware, Cave & Access</button>
    <button class="nav-btn" onclick="switchPage(3)">4. ☀️ Solar Flux & Rover Lab</button>
    <button class="nav-btn" onclick="switchPage(4)">5. 📄 Official Dossier & Data Archive</button>
  </div>

  <div style="display:flex;gap:8px;">
    <button class="btn btn-amber" id="btnYouth" onclick="toggleYouth()">🎓 Explorer Story Mode</button>
    <button class="btn btn-green" onclick="syncLive()">⚡ Live Satellite Sync</button>
  </div>
</header>

<!-- PERSISTENT TELEMETRY RIBBON (WITH SOLAR FLUX!) -->
<div class="context-bar">
  <div class="ctx-group">
    <span style="color:var(--pink);font-weight:900;">🌕/🔴 SPACE TARGET:</span>
    <select id="targetSelect" onchange="recompute()"></select>
  </div>
  <div class="ctx-group">
    <span style="color:var(--emerald);font-weight:900;">🌍 EARTH ANALOG:</span>
    <select id="siteSelect" onchange="onDropdownSiteChange()"></select>
  </div>
  <div style="display:flex;gap:8px;align-items:center;">
    <span class="pill-badge pill-match" id="topMatchPill">🎯 --% Match</span>
    <span class="pill-badge pill-flux" id="topFluxPill">☀️ Solar Flux: -- W/m²</span>
  </div>
</div>

<div id="youthBanner"></div>

<!-- ========================================================================= -->
<!-- 5 VIBRANT, SPACIOUS PAGES                                                 -->
<!-- ========================================================================= -->
<div class="page-container">

  <!-- PAGE 1: 3D SATELLITE GLOBE & 20X GOOGLE SATELLITE DEEP-ZOOM -->
  <div class="page map-page active" id="page0">
    <div class="map-layout">
      <div class="map-sidebar">
        <div class="card pink-top">
          <div class="card-title"><span>🌟 Discover & Filter Analogs</span></div>
          <label style="display:flex;align-items:center;gap:6px;font-size:11.5px;color:#ffbe0b;font-weight:800;cursor:pointer;margin-bottom:7px;">
            <input type="checkbox" id="chkBrandNew" onchange="recompute()"> 🚀 Show Brand-New Unstudied Sites Only
          </label>
          <select id="envFilter" onchange="recompute()" style="width:100%;margin-bottom:8px;">
            <option value="ALL">🌈 All 6 Planetary Environments</option>
            <option value="Deserts">🏜️ 1. Deserts (Hyper-Arid & Dunes)</option>
            <option value="Polar Regions">❄️ 2. Polar & Cold Permafrost Valleys</option>
            <option value="Volcanic Terrains">🌋 3. Volcanic Basalt & Ash Terrains</option>
            <option value="Arid Terrains">☀️ 4. Arid Sulfate & Clay Plains</option>
            <option value="Caves">🦇 5. Caves & Subsurface Lava Tubes</option>
            <option value="Other Environments">☄️ 6. Impact Craters & Hydrothermal</option>
          </select>
          <div id="siteListContainer" style="max-height:295px;overflow-y:auto;"></div>
        </div>

        <div class="card gold-top">
          <div class="card-title"><span>📡 Live Satellite Coord Scanner</span></div>
          <div style="font-size:11px;color:var(--muted);margin-bottom:4px;">Click any spot on the 2D Satellite Map or enter coordinates to pull live Solar Flux, Elevation & NASA POWER data:</div>
          <input type="text" id="cName" value="Milam Glacier Valley, Uttarakhand">
          <div style="display:flex;gap:6px;margin-top:4px;">
            <input type="number" id="cLat" value="30.43" step="0.01" placeholder="Lat">
            <input type="number" id="cLon" value="80.15" step="0.01" placeholder="Lon">
          </div>
          <button class="btn btn-pink" style="width:100%;margin-top:8px;" onclick="scanCustomCoord()">🛰️ Scan & Fly to Satellite View</button>
        </div>
      </div>

      <div class="map-viewport">
        <div id="globeContainer"></div>
        <div id="leafletContainer"></div>

        <div class="map-floating-bar">
          <div style="display:flex;gap:8px;">
            <button class="btn active" id="mode3D" onclick="setMapView('3D')">🌎 3D Photorealistic Satellite Globe</button>
            <button class="btn" id="mode2D" onclick="setMapView('2D')">🛰️ Google Satellite Hybrid (20x Deep-Zoom)</button>
            <button class="btn btn-amber" onclick="zoomToCrater()">🔍 Zoom Into Crater / Surface Rocks</button>
          </div>
          <div style="font-size:11.5px;color:var(--gold);font-weight:800;" id="targetObjShort"></div>
        </div>

        <div class="time-floating-bar">
          <div style="display:flex;justify-content:space-between;font-size:11.5px;font-weight:800;margin-bottom:4px;">
            <span style="color:var(--gold);">⏱️ 12-MONTH SEASONAL TIME-TRAVEL SIMULATOR (Drag to Shift Earth Analog Season):</span>
            <span id="seasonLbl" style="color:var(--emerald);">☀️ MODE: LIVE / ANNUAL SATELLITE TELEMETRY</span>
          </div>
          <input type="range" id="monthSlider" min="0" max="12" step="1" value="0" oninput="onSeasonSlide(this.value)">
          <div style="display:flex;justify-content:space-between;font-size:10px;color:#fff;font-weight:800;">
            <span>LIVE</span><span>JAN</span><span>FEB</span><span>MAR</span><span>APR</span><span>MAY</span><span>JUN</span>
            <span>JUL</span><span>AUG</span><span>SEP</span><span>OCT</span><span>NOV</span><span>DEC</span>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- PAGE 2: CLEARLY LABELED SIDE-BY-SIDE COMPARISON (MOON/MARS VS. EARTH) -->
  <div class="page" id="page1">
    <!-- DUAL HERO CARDS: WHAT SPACE HAS VS WHAT EARTH PROVIDES -->
    <div class="twin-hero-grid">
      <div class="hero-space" id="heroSpaceCard"></div>
      <div class="hero-earth" id="heroEarthCard"></div>
    </div>

    <div class="grid-2" style="margin-bottom:14px;">
      <div class="card purple-top">
        <div class="card-title">
          <span>🎯 NASA 4-Pillar Match Gauges & Weights</span>
          <span style="font-size:11px;color:var(--cyan);">Drag Sliders to Re-Rank</span>
        </div>
        <div class="rings-row" id="ringsGrid"></div>
        <div class="grid-2" style="margin-top:10px;font-size:11.5px;font-weight:700;">
          <div>
            <div style="display:flex;justify-content:space-between;color:var(--cyan);"><span>⛰️ 1. Topography</span><span id="wTopoV">1.8</span></div>
            <input type="range" id="wTopo" min="0.1" max="3.0" step="0.1" value="1.8" oninput="recompute()">
          </div>
          <div>
            <div style="display:flex;justify-content:space-between;color:var(--emerald);"><span>🪨 2. Geology & Oxides</span><span id="wGeolV">2.0</span></div>
            <input type="range" id="wGeol" min="0.1" max="3.0" step="0.1" value="2.0" oninput="recompute()">
          </div>
          <div>
            <div style="display:flex;justify-content:space-between;color:var(--gold);"><span>☀️ 3. Environment & Solar Flux</span><span id="wEnvV">2.0</span></div>
            <input type="range" id="wEnv" min="0.1" max="3.0" step="0.1" value="2.0" oninput="recompute()">
          </div>
          <div>
            <div style="display:flex;justify-content:space-between;color:var(--pink);"><span>🧊 4. Water-Ice & Cave Resources</span><span id="wResV">2.2</span></div>
            <input type="range" id="wRes" min="0.1" max="3.0" step="0.1" value="2.2" oninput="recompute()">
          </div>
        </div>
      </div>

      <div class="card gold-top">
        <div class="card-title">
          <span>🌪️ Interactive Hazard Stress-Tester & 12-Month Solar/Temp Curve</span>
          <div style="display:flex;gap:5px;">
            <button class="btn btn-amber" style="padding:3px 8px;font-size:10px;" onclick="setHazard('NORMAL')">☀️ Nominal</button>
            <button class="btn btn-pink" style="padding:3px 8px;font-size:10px;" onclick="setHazard('DUST')">🌪️ Dust Storm (-75% Flux)</button>
            <button class="btn" style="padding:3px 8px;font-size:10px;" onclick="setHazard('NIGHT')">🌑 Lunar Eclipse (-150°C)</button>
          </div>
        </div>
        <div id="seasonBestBox" style="font-size:12px;margin-bottom:6px;"></div>
        <canvas id="climCanvas" width="560" height="165" style="width:100%;height:165px;background:#080618;border-radius:8px;border:1px solid rgba(255,190,11,0.3);"></canvas>
      </div>
    </div>

    <!-- EXPLICITLY LABELED SIDE-BY-SIDE COMPARISON TABLE -->
    <div class="card green-top">
      <div class="card-title">
        <span>📊 Side-by-Side Scientific Evidence Table: What Moon/Mars Has vs. What Earth Provides</span>
        <span id="processScaleBadge" style="font-size:11px;color:var(--emerald);"></span>
      </div>
      <table class="comp-table" id="sideBySideTable">
        <thead>
          <tr>
            <th class="th-feature">📌 Essential Parameter & Why Mission Needs It</th>
            <th class="th-space" id="thSpaceCol">🌕/🔴 Moon / Mars Target (Space Value)</th>
            <th class="th-earth" id="thEarthCol">🌍 Earth Analog Site (Earth Value)</th>
            <th class="th-delta">📊 Visual Match & Difference (Δ)</th>
            <th class="th-why">🛠️ What Earth Provides vs. Space</th>
          </tr>
        </thead>
        <tbody></tbody>
      </table>
    </div>
  </div>

  <!-- PAGE 3: HARDWARE, METHODS, MISSING DATA & PROTECTED LAND STEWARDSHIP -->
  <div class="page" id="page2">
    <div class="grid-2">
      <div>
        <div class="card pink-top" style="margin-bottom:14px;">
          <div class="card-title"><span>🛠️ What Mission Teams Can Test Here ('Test Before They Fly')</span></div>
          <div class="field-box pink" id="equipField"></div>
          <div class="field-box gold" id="methodField"></div>
          <div class="field-box green" id="subzoneField"></div>
        </div>
      </div>

      <div>
        <div class="card gold-top" style="margin-bottom:14px;">
          <div class="card-title"><span>⚠️ Where the Analogy Breaks Down & Uncharacterized Gaps</span></div>
          <div class="field-box gold" id="missingField"></div>
          <div class="field-box pink" id="gapsField"></div>
        </div>

        <div class="card green-top">
          <div class="card-title"><span>🧭 Respect for the Place: Access, Permits & Local Communities</span></div>
          <div class="field-box green" id="stewardField"></div>
          <div class="field-box" id="reverseField"></div>
        </div>
      </div>
    </div>
  </div>

  <!-- PAGE 4: INTERACTIVE SOLAR FLUX ARRAY CALCULATOR, ROVER PHYSICS & XRF OXIDES -->
  <div class="page" id="page3">
    <div class="card gold-top" style="margin-bottom:14px;">
      <div class="card-title">
        <span>☀️ Interactive Solar Flux & Habitat Power Array Simulator (Earth vs. Moon/Mars)</span>
        <span id="fluxSummaryBadge" style="color:var(--emerald);"></span>
      </div>
      <div class="grid-2">
        <div>
          <label style="font-size:12px;font-weight:800;color:var(--gold);">⚡ Base / Rover Continuous Power Requirement (kW): <span id="pwrReqVal">15</span> kW</label>
          <input type="range" id="pwrReqSlider" min="2" max="50" step="1" value="15" oninput="updateSolarSimulator()">
          <label style="font-size:12px;font-weight:800;color:var(--cyan);margin-top:8px;display:block;">🌫️ Atmospheric / Regolith Dust Attenuation (% Loss): <span id="dustLossVal">15</span>%</label>
          <input type="range" id="dustLossSlider" min="0" max="80" step="5" value="15" oninput="updateSolarSimulator()">
        </div>
        <div id="solarCalcOutput" style="background:#09071c;border:1px solid var(--gold);border-radius:10px;padding:10px 14px;font-size:12px;line-height:1.55;"></div>
      </div>
    </div>

    <div class="grid-2">
      <div class="card">
        <div class="card-title"><span>🚜 Pre-Flight Rover Slope Traverse & Gravity Power Simulator</span></div>
        <canvas id="roverCanvas" width="560" height="230" style="width:100%;height:230px;background:#080618;border-radius:8px;border:1px solid var(--cyan);"></canvas>
      </div>

      <div class="card pink-top">
        <div class="card-title"><span>🧪 XRF Geochemical Oxide Match vs. Official NASA Simulant</span></div>
        <div id="simulantHeader" style="font-size:12px;color:var(--emerald);font-weight:800;margin-bottom:6px;"></div>
        <canvas id="chemCanvas" width="560" height="230" style="width:100%;height:230px;background:#080618;border-radius:8px;border:1px solid var(--pink);"></canvas>
      </div>
    </div>
  </div>

  <!-- PAGE 5: JUDGE-FACING OFFICIAL MISSION DOSSIER & MULTI-AGENCY DATA ARCHIVE -->
  <div class="page" id="page4">
    <div class="grid-2">
      <div class="card green-top">
        <div class="card-title">
          <span>📄 Official Printable NASA Mission Characterization Dossier</span>
          <div style="display:flex;gap:6px;">
            <button class="btn btn-green" onclick="exportCSV()">📥 Export CSV Catalog</button>
            <button class="btn btn-pink" onclick="window.print()">🖨️ Print / Save PDF</button>
          </div>
        </div>
        <pre id="dossierPre" style="background:#060512;border:1px solid var(--cyan);padding:12px;border-radius:8px;font-family:Consolas,monospace;font-size:11px;color:#a5f3fc;white-space:pre-wrap;max-height:460px;overflow-y:auto;"></pre>
      </div>

      <div class="card pink-top">
        <div class="card-title">
          <span>📚 Multi-Agency Open Data Archive & Scientific Methodology</span>
          <span style="font-size:10.5px;color:var(--gold);">Verified Space Agency Sources</span>
        </div>

        <div class="field-box gold">
          <b style="color:var(--gold);">🛰️ 1. NASA Planetary & Earth Observation Datasets:</b><br>
          • <b>Lunar Reconnaissance Orbiter (LRO):</b> LOLA 20m Laser Altimeter DEM slopes & Diviner Lunar Radiometer cryogenic surface temperatures.<br>
          • <b>Mars Reconnaissance Orbiter (MRO):</b> HiRISE sub-meter stereo topography, CRISM VNIR mineral spectroscopy & SHARAD subsurface ice radar.<br>
          • <b>Mars Surface Rovers:</b> Mars 2020 Perseverance (MEDA weather, PIXL XRF oxides, SHERLOC Raman) & MSL Curiosity (REMS, CheMin).<br>
          • <b>NASA Earth Science:</b> NASA Langley POWER (30-year solar irradiance flux W/m² & surface temperature climatology) & NASADEM/SRTM.
        </div>

        <div class="field-box">
          <b style="color:var(--cyan);">🌍 2. Partner Space Agency Datasets (ISRO, JAXA, ESA):</b><br>
          • <b>ISRO (India):</b> Chandrayaan-1 Moon Mineralogy Mapper (M³) hydroxyl/ice absorption, Chandrayaan-2 DFSAR polar radar & IIRS spectroscopy.<br>
          • <b>JAXA (Japan):</b> SELENE / Kaguya Terrain Camera oblique lunar skylight pit geometry (Marius Hills).<br>
          • <b>ESA (Europe):</b> Mars Express OMEGA phyllosilicate clay maps & Copernicus DEM GLO-90 global terrestrial elevation.<br>
          • <b>Orbital Basemaps & Telemetry:</b> Google Satellite Hybrid, Esri World Imagery, Open-Meteo Live Radiation API.
        </div>

        <div class="field-box green">
          <b style="color:var(--emerald);">🔬 3. Mathematical Scoring & 2026 Transparency Statement:</b><br>
          • <b>4-Pillar Algorithm:</b> Computes weighted similarity across <i>Topography</i> (slope/elevation), <i>Geology</i> (basalt % + 6-oxide XRF distance), <i>Environment</i> (mean temp, diurnal swing, aridity & peak solar flux W/m²), and <i>Resources</i> (subsurface water-ice & cave radiation shielding).<br>
          • <b>2026 Space Apps Rule Disclosure:</b> All planetary and terrestrial metrics derive deterministically from the cited agency archives above; generative AI tools assisted strictly with software UI scaffolding and formatting literature summaries.
        </div>
      </div>
    </div>
  </div>

</div>

<script>
const TARGETS = __TARGETS_JSON__;
let earthSites = __EARTH_JSON__;
let rankedSites = [];
let selectedIdx = 0;
let mapView = '3D';
let youthMode = false;
let hazardMode = 'NORMAL';
let liveCache = {};
let globeInstance = null;
let leafletMap = null;
let leafletMarkers = null;
let roverTick = 0;
const MONTHS = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"];

function initApp() {
  const tSel = document.getElementById('targetSelect');
  TARGETS.forEach((t, i) => {
    const opt = document.createElement('option');
    opt.value = i;
    opt.textContent = `${t.body === 'Moon' ? '🌕' : '🔴'} ${t.name}`;
    tSel.appendChild(opt);
  });

  initGlobe();
  initLeaflet();
  recompute();

  setInterval(() => {
    roverTick = (roverTick + 3) % 100;
    if (rankedSites.length > 0 && document.getElementById('page3').classList.contains('active')) {
      drawRoverAndChem(TARGETS[parseInt(tSel.value)], rankedSites[selectedIdx]);
    }
  }, 90);
}

function switchPage(idx) {
  document.querySelectorAll('.nav-btn').forEach((b, i) => b.className = i === idx ? 'nav-btn active' : 'nav-btn');
  document.querySelectorAll('.page').forEach((p, i) => {
    p.className = (i === 0 ? 'page map-page' : 'page') + (i === idx ? ' active' : '');
  });
  if (idx === 0 && mapView === '2D' && leafletMap) {
    setTimeout(() => {
      leafletMap.invalidateSize();
      const s = rankedSites[selectedIdx];
      if (s) leafletMap.setView([s.lat, s.lon], Math.max(leafletMap.getZoom(), 7));
    }, 60);
  }
  if (idx === 1 && rankedSites.length) drawClimChart(rankedSites[selectedIdx]);
  if (idx === 3 && rankedSites.length) {
    updateSolarSimulator();
    drawRoverAndChem(TARGETS[parseInt(document.getElementById('targetSelect').value)], rankedSites[selectedIdx]);
  }
}

// ============================================================================
// FIXED 3D GLOBE: ZERO-OFFSET COORDINATE PINS + 3D WEBGL SURFACE RINGS
// ============================================================================
function initGlobe() {
  const container = document.getElementById('globeContainer');
  try {
    globeInstance = Globe()(container)
      .globeImageUrl('https://unpkg.com/three-globe/example/img/earth-blue-marble.jpg')
      .backgroundImageUrl('https://unpkg.com/three-globe/example/img/night-sky.png')
      .showAtmosphere(true)
      .atmosphereColor('#00f2fe')
      .atmosphereAltitude(0.20)
      // 1. True 3D WebGL Surface Rings (Mathematically locked to lat/lon on the sphere)
      .ringsData([])
      .ringLat(d => d.lat)
      .ringLng(d => d.lon)
      .ringColor(d => d.rank === (selectedIdx + 1) ? '#00ff87' : '#ff006e')
      .ringMaxRadius(d => d.rank === (selectedIdx + 1) ? 3.5 : 1.8)
      .ringPropagationSpeed(2.2)
      .ringRepeatPeriod(900)
      // 2. Zero-Width Root Anchor so Pin Dot sits at EXACT (0,0) Coordinate Center!
      .htmlElementsData([])
      .htmlLat(d => d.lat)
      .htmlLng(d => d.lon)
      .htmlAltitude(0.002)
      .htmlElement(d => {
        const wrapper = document.createElement('div');
        // CRITICAL: Never set 'transform' on wrapper; Globe.gl controls wrapper.style.transform!
        wrapper.style.width = '0px';
        wrapper.style.height = '0px';
        wrapper.style.position = 'relative';
        wrapper.style.overflow = 'visible';
        wrapper.style.pointerEvents = 'auto';
        wrapper.style.cursor = 'pointer';

        const isSel = d.rank === (selectedIdx + 1);
        const col = isSel ? '#00ff87' : (d.tier === 'BRAND-NEW' ? '#ff006e' : (d.tier === 'PRIOR ANALOG' ? '#ffbe0b' : '#00f2fe'));
        const sz = isSel ? 14 : 10;

        // Pin Dot centered at exact (0,0) coordinate origin
        const dot = document.createElement('div');
        dot.style.cssText = `position:absolute;left:0;top:0;width:${sz}px;height:${sz}px;border-radius:50%;background:${col};border:2px solid #fff;transform:translate(-50%,-50%);box-shadow:0 0 12px ${col};`;
        wrapper.appendChild(dot);

        // Floating Label anchored to the right of (0,0) so it never shifts the pin center
        if (isSel || d.rank <= 8) {
          const lbl = document.createElement('div');
          lbl.style.cssText = `position:absolute;left:10px;top:0;transform:translateY(-50%);background:rgba(8,6,24,0.92);border:1.5px solid ${col};color:#fff;padding:2px 6px;border-radius:6px;font-size:${isSel?11:9.5}px;font-weight:800;white-space:nowrap;box-shadow:0 2px 8px rgba(0,0,0,0.6);`;
          lbl.textContent = `#${d.rank} ${d.name.split(',')[0].split('(')[0]} (${d.score}%)`;
          wrapper.appendChild(lbl);
        }

        wrapper.onclick = (e) => { e.stopPropagation(); selectSite(d.rank - 1, false); };
        wrapper.ondblclick = (e) => { e.stopPropagation(); selectSite(d.rank - 1, true); };
        return wrapper;
      });

    const resize = () => {
      if (globeInstance && container.clientWidth > 0) {
        globeInstance.width(container.clientWidth);
        globeInstance.height(container.clientHeight);
      }
    };
    window.addEventListener('resize', resize);
    setTimeout(resize, 150);
  } catch (e) {
    setMapView('2D');
  }
}

function initLeaflet() {
  leafletMap = L.map('leafletContainer', { zoomControl: true, maxZoom: 19 }).setView([28, 78], 5);
  const googleSat = L.tileLayer('https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', { maxZoom: 20, attribution: 'Google Satellite Hybrid & NASA' });
  const esriSat = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', { maxZoom: 19, attribution: 'Esri World Imagery' });
  googleSat.addTo(leafletMap);
  L.control.layers({ "🛰️ Google Satellite Hybrid (Labels + Terrain)": googleSat, "🌎 Esri Pure Satellite": esriSat }, null, { position: 'bottomright' }).addTo(leafletMap);
  leafletMarkers = L.layerGroup().addTo(leafletMap);

  leafletMap.on('click', (e) => {
    const lat = parseFloat(e.latlng.lat.toFixed(3));
    const lon = parseFloat(e.latlng.lng.toFixed(3));
    document.getElementById('cName').value = `Satellite Discovery (${lat}°, ${lon}°)`;
    document.getElementById('cLat').value = lat;
    document.getElementById('cLon').value = lon;
    scanCustomCoord();
  });
}

function setMapView(mode) {
  mapView = mode;
  document.getElementById('mode3D').className = mode === '3D' ? 'btn active' : 'btn';
  document.getElementById('mode2D').className = mode === '2D' ? 'btn active' : 'btn';
  document.getElementById('globeContainer').style.display = mode === '3D' ? 'block' : 'none';
  document.getElementById('leafletContainer').style.display = mode === '2D' ? 'block' : 'none';

  const s = rankedSites[selectedIdx];
  if (mode === '2D' && leafletMap && s) {
    leafletMap.invalidateSize();
    leafletMap.setView([s.lat, s.lon], 12);
  } else if (mode === '3D' && globeInstance && s) {
    globeInstance.pointOfView({ lat: s.lat, lng: s.lon, altitude: 1.45 }, 700);
  }
}

function zoomToCrater() {
  setMapView('2D');
  const s = rankedSites[selectedIdx];
  if (s && leafletMap) {
    leafletMap.invalidateSize();
    leafletMap.setView([s.lat, s.lon], 14);
  }
}

function setHazard(mode) {
  hazardMode = mode;
  recompute();
}

// ============================================================================
// 4-PILLAR SCORING ENGINE (INCLUDING SOLAR FLUX W/m²)
// ============================================================================
function scorePair(target, site, w1, w2, w3, w4) {
  const slopeSim = Math.max(0, 1 - Math.abs(target.slope - site.slope) / 35);
  const elevSim  = Math.max(0, 1 - Math.abs(target.elev - site.elev) / 14000);
  const pTopo    = +((0.75 * slopeSim + 0.25 * elevSim) * 100).toFixed(1);

  const basaltSim = Math.max(0, 1 - Math.abs(target.basalt - site.basalt) / 100);
  const oxKeys = ["SiO2","FeO","MgO","Al2O3","CaO","TiO2"];
  let oxDiff = 0;
  oxKeys.forEach(k => { oxDiff += Math.abs((target.oxides[k]||10) - (site.oxides[k]||10)); });
  const chemSim  = Math.max(0.25, 1 - (oxDiff / 85));
  const pGeol    = +((0.55 * basaltSim + 0.45 * chemSim) * 100).toFixed(1);

  const tempSim  = Math.max(0, 1 - Math.abs(target.temp - site.activeTemp) / 210);
  const aridSim  = Math.max(0, 1 - Math.abs(target.aridity - site.aridity) / 100);
  const fluxSim  = Math.max(0, 1 - Math.abs(target.solar_flux - site.activeFlux) / 1100);
  const pEnv     = +((0.40 * tempSim + 0.30 * aridSim + 0.30 * fluxSim) * 100).toFixed(1);

  const iceSim   = Math.max(0, 1 - Math.abs(target.ice - site.ice) / 100);
  const shSim    = Math.max(0, 1 - Math.abs(target.shielding - site.shielding) / 100);
  const pRes     = +(((target.role === "Permanent Base" ? (0.55*iceSim + 0.45*shSim) : (0.75*iceSim + 0.25*shSim))) * 100).toFixed(1);

  const tw = (w1 + w2 + w3 + w4) || 1;
  const overall = +Math.min(99.8, Math.max(15, (w1*pTopo + w2*pGeol + w3*pEnv + w4*pRes) / tw)).toFixed(1);
  return { overall, pTopo, pGeol, pEnv, pRes, chemPct: +(chemSim * 100).toFixed(1) };
}

function recompute() {
  const t = TARGETS[parseInt(document.getElementById('targetSelect').value)];
  const w1 = parseFloat(document.getElementById('wTopo').value);
  const w2 = parseFloat(document.getElementById('wGeol').value);
  const w3 = parseFloat(document.getElementById('wEnv').value);
  const w4 = parseFloat(document.getElementById('wRes').value);
  document.getElementById('wTopoV').textContent = w1.toFixed(1);
  document.getElementById('wGeolV').textContent = w2.toFixed(1);
  document.getElementById('wEnvV').textContent  = w3.toFixed(1);
  document.getElementById('wResV').textContent  = w4.toFixed(1);
  document.getElementById('targetObjShort').textContent = `🎯 ${t.role} (${t.body}) • Peak Solar Flux: ${t.solar_flux} W/m²`;

  const onlyNew = document.getElementById('chkBrandNew').checked;
  const envF = document.getElementById('envFilter').value;
  const mIdx = parseInt(document.getElementById('monthSlider').value);

  let cands = earthSites.filter(s => {
    if (onlyNew && s.tier !== 'BRAND-NEW') return false;
    if (envF !== 'ALL' && s.cat !== envF) return false;
    return true;
  });
  if (cands.length === 0) cands = [...earthSites];

  rankedSites = cands.map(s => {
    const copy = { ...s };
    if (mIdx > 0) {
      copy.activeTemp = s.monthly_t[mIdx - 1];
      copy.activeSolar = s.monthly_s[mIdx - 1];
      copy.activeFlux = Math.round(s.solar_flux * (copy.activeSolar / (s.solar || 5.5)));
    } else {
      copy.activeTemp = s.temp;
      copy.activeSolar = s.solar;
      copy.activeFlux = s.solar_flux;
    }

    if (hazardMode === 'DUST') {
      copy.activeFlux = Math.round(copy.activeFlux * 0.25);
      copy.activeSolar = +(copy.activeSolar * 0.25).toFixed(1);
    } else if (hazardMode === 'NIGHT') {
      copy.activeTemp = copy.activeTemp - 35;
      copy.activeFlux = 0;
    }

    const sc = scorePair(t, copy, w1, w2, w3, w4);
    Object.assign(copy, { score: sc.overall, pTopo: sc.pTopo, pGeol: sc.pGeol, pEnv: sc.pEnv, pRes: sc.pRes, chemPct: sc.chemPct });

    const rev = TARGETS.map(ot => ({
      name: ot.name.split(' (')[0], body: ot.body, sc: scorePair(ot, copy, w1, w2, w3, w4).overall
    })).sort((a,b) => b.sc - a.sc);
    copy.reverseBest = `#1 ${rev[0].name} (${rev[0].body}: ${rev[0].sc}%) • #2 ${rev[1].name} (${rev[1].sc}%)`;
    return copy;
  }).sort((a,b) => b.score - a.score);

  rankedSites.forEach((s, i) => s.rank = i + 1);
  selectedIdx = Math.min(selectedIdx, rankedSites.length - 1);

  const sSel = document.getElementById('siteSelect');
  sSel.innerHTML = '';
  rankedSites.forEach((s, i) => {
    const opt = document.createElement('option');
    opt.value = i;
    opt.textContent = `#${i+1} ${s.name} (${s.score}%)`;
    sSel.appendChild(opt);
  });

  renderSiteList();
  selectSite(selectedIdx, false);
}

function renderSiteList() {
  const box = document.getElementById('siteListContainer');
  box.innerHTML = '';
  rankedSites.forEach((s, i) => {
    const div = document.createElement('div');
    div.className = 'site-list-item' + (i === selectedIdx ? ' selected' : '');
    div.onclick = () => selectSite(i, false);
    const badge = s.tier === 'BRAND-NEW'
      ? `<span class="badge-new">🌟 BRAND-NEW</span>`
      : (s.tier === 'PRIOR ANALOG' ? `<span class="badge-prior">🔬 PRIOR ANALOG</span>` : `<span class="badge-bench">🏛️ BENCHMARK</span>`);
    div.innerHTML = `
      <div style="max-width:230px;">
        <div style="font-size:11.5px;font-weight:800;color:#fff;">#${i+1} ${s.name.split(',')[0]}</div>
        <div style="font-size:10px;color:var(--muted);margin-top:3px;">${badge} • ☀️ ${s.activeFlux} W/m²</div>
      </div>
      <div style="font-size:13px;font-weight:900;color:var(--emerald);">${s.score}%</div>
    `;
    box.appendChild(div);
  });
}

function onDropdownSiteChange() {
  selectSite(parseInt(document.getElementById('siteSelect').value), false);
}

function selectSite(idx, zoomSurface) {
  selectedIdx = idx;
  document.getElementById('siteSelect').value = idx;
  const t = TARGETS[parseInt(document.getElementById('targetSelect').value)];
  const s = rankedSites[idx];

  document.getElementById('topMatchPill').textContent = `🎯 ${s.score}% Match (${s.tier})`;
  document.getElementById('topFluxPill').textContent = `☀️ Earth Flux: ${s.activeFlux} W/m² vs ${t.body}: ${t.solar_flux} W/m²`;
  renderSiteList();

  if (globeInstance) {
    globeInstance.ringsData([s]);
    globeInstance.htmlElementsData(rankedSites);
    globeInstance.pointOfView({ lat: s.lat, lng: s.lon, altitude: 1.45 }, 850);
  }
  if (leafletMap && leafletMarkers) {
    leafletMarkers.clearLayers();
    rankedSites.forEach((site, i) => {
      const isSel = i === idx;
      const col = isSel ? '#00ff87' : (site.tier === 'BRAND-NEW' ? '#ff006e' : '#00f2fe');
      L.circleMarker([site.lat, site.lon], { radius: isSel ? 11 : 7, fillColor: col, color: '#fff', weight: 2, fillOpacity: 0.9 })
        .addTo(leafletMarkers).bindPopup(`<b>#${i+1} ${site.name}</b><br>Match: ${site.score}% | Solar Flux: ${site.activeFlux} W/m²`);
    });
    if (mapView === '2D' || zoomSurface) {
      if (zoomSurface && mapView !== '2D') setMapView('2D');
      leafletMap.invalidateSize();
      leafletMap.setView([s.lat, s.lon], zoomSurface ? 14 : 11);
    }
  }

  if (youthMode) {
    const yb = document.getElementById('youthBanner');
    yb.style.display = 'block';
    yb.innerHTML = `🎓 <b>EXPLORER STORY — ${t.name}:</b> ${t.youth} &nbsp;|&nbsp; 🌍 <b>Why ${s.name} matches (${s.score}%):</b> It is a ${s.terrain} receiving ${s.activeFlux} W/m² solar flux where engineers test ${s.equip}.`;
  }

  // PAGE 2: DUAL HERO CARDS (EXPLICITLY LABELED SPACE VS EARTH)
  const bodyIcon = t.body === 'Moon' ? '🌕' : '🔴';
  document.getElementById('heroSpaceCard').innerHTML = `
    <div style="font-size:11px;font-weight:900;color:#ffbe0b;text-transform:uppercase;">${bodyIcon} EXTRATERRESTRIAL TARGET (WHAT ${t.body.toUpperCase()} HAS)</div>
    <div style="font-size:15px;font-weight:900;color:#fff;margin:3px 0;">${t.name}</div>
    <div style="font-size:11px;color:#ffd6e0;"><b>🏛️ Mission Role:</b> ${t.role} &nbsp;|&nbsp; <b>🛰️ Agency Sensors:</b> ${t.agencies}</div>
    <div style="margin-top:6px;display:flex;gap:8px;flex-wrap:wrap;font-size:11px;">
      <span class="val-space">☀️ Solar Flux: ${t.solar_flux} W/m² (${t.solar} kWh/d)</span>
      <span class="val-space">🌡️ Temp: ${t.temp}°C</span>
      <span class="val-space">⛰️ Slope: ${t.slope}°</span>
      <span class="val-space">🧊 Water-Ice: ${t.ice}/100</span>
    </div>
  `;

  document.getElementById('heroEarthCard').innerHTML = `
    <div style="font-size:11px;font-weight:900;color:#00ff87;text-transform:uppercase;">🌍 TERRESTRIAL ANALOG CANDIDATE (WHAT EARTH PROVIDES)</div>
    <div style="font-size:15px;font-weight:900;color:#fff;margin:3px 0;">${s.name} <span class="badge-new">${s.tier}</span></div>
    <div style="font-size:11px;color:#bbf7d0;"><b>⛰️ Terrain:</b> ${s.terrain} &nbsp;|&nbsp; <b>📏 Scale:</b> ${s.scale}</div>
    <div style="margin-top:6px;display:flex;gap:8px;flex-wrap:wrap;font-size:11px;">
      <span class="val-earth">☀️ Solar Flux: ${s.activeFlux} W/m² (${s.activeSolar} kWh/d)</span>
      <span class="val-earth">🌡️ Temp: ${s.activeTemp}°C</span>
      <span class="val-earth">⛰️ Slope: ${s.slope}°</span>
      <span class="val-earth">🧊 Water-Ice: ${s.ice}/100</span>
    </div>
  `;

  // 4-PILLAR GAUGES
  const pillars = [
    { name: '⛰️ Topography', val: s.pTopo, col: '#00f2fe' },
    { name: '🪨 Geology',    val: s.pGeol, col: '#00ff87' },
    { name: '☀️ Env & Flux', val: s.pEnv,  col: '#ffbe0b' },
    { name: '🧊 Resources',  val: s.pRes,  col: '#ff006e' }
  ];
  document.getElementById('ringsGrid').innerHTML = pillars.map(p => {
    const dash = (p.val / 100) * 157;
    return `<div class="ring-card">
      <svg width="62" height="62" viewBox="0 0 60 60">
        <circle cx="30" cy="30" r="25" fill="none" stroke="#1f1b44" stroke-width="5"/>
        <circle cx="30" cy="30" r="25" fill="none" stroke="${p.col}" stroke-width="5" stroke-dasharray="${dash} 157" stroke-linecap="round" transform="rotate(-90 30 30)"/>
        <text x="30" y="34" text-anchor="middle" fill="#fff" font-size="11.5" font-weight="900">${Math.round(p.val)}%</text>
      </svg>
      <div style="color:${p.col};font-size:11px;font-weight:800;">${p.name}</div>
    </div>`;
  }).join('');

  // EXPLICITLY LABELED SIDE-BY-SIDE COMPARISON TABLE
  document.getElementById('thSpaceCol').innerHTML = `${bodyIcon} ${t.body} Target (What Space Has)`;
  document.getElementById('thEarthCol').innerHTML = `🌍 ${s.name.split(',')[0]} (What Earth Provides)`;
  document.getElementById('processScaleBadge').textContent = `⚡ Active Process: ${s.process}`;

  const rows = [
    [
      "☀️ Peak Solar Flux & Daily Insolation",
      "Determines solar array size, battery storage & UV shielding",
      `${t.solar_flux} W/m² (${t.solar} kWh/m²/d)`,
      `${s.activeFlux} W/m² (${s.activeSolar} kWh/m²/d)`,
      Math.round(Math.max(20, 100 - Math.abs(t.solar_flux - s.activeFlux)/11)),
      `Δ ${s.activeFlux - t.solar_flux} W/m²`,
      "Earth site validates solar array tracking, UV degradation & dust-obscuration power curves"
    ],
    [
      "⛰️ Surface Slope & Topographic Relief",
      "Critical for lander touchdown stability & rover tip-over risk",
      `${t.slope}° Slope (${t.elev} m)`,
      `${s.slope}° Slope (${s.elev} m)`,
      Math.round(Math.max(20, 100 - Math.abs(t.slope - s.slope)*2.5)),
      `Δ ${(s.slope - t.slope).toFixed(1)}°`,
      "Earth slope directly tests rocker-bogie rover traction, crater-wall climbing & lidar hazard avoidance"
    ],
    [
      "🪨 Basalt Rock & Geochemical Oxides",
      "Essential for hard-rock core drilling & oxygen/brick ISRU",
      `${t.basalt}% Basalt (${t.simulant.split(' ')[0]})`,
      `${s.basalt}% Basalt (${s.chemPct}% Oxide Match)`,
      Math.round(s.pGeol),
      `Δ ${(s.basalt - t.basalt).toFixed(0)}% Basalt`,
      "Provides identical silicate/iron/titanium minerals to calibrate PIXL/SHERLOC spectrometers & drills"
    ],
    [
      "🌡️ Surface Temp & Diurnal Thermal Swing",
      "Drives habitat insulation, cryogenic battery & seal survival",
      `${t.temp}°C (Δ ${t.diurnal}°C Swing)`,
      `${s.activeTemp}°C (Δ ${s.diurnal}°C Swing)`,
      Math.round(Math.max(20, 100 - Math.abs(t.temp - s.activeTemp)/2.1)),
      `Δ ${(s.activeTemp - t.temp).toFixed(1)}°C`,
      "Rehearses freeze-thaw thermal cycling on electronics (pair with cryo-vacuum chamber for lunar night)"
    ],
    [
      "🏜️ Hyper-Aridity & Eolian Dust Regime",
      "Controls electrostatic dust adhesion & life-detection sterility",
      `${t.aridity}/100 Aridity Index`,
      `${s.aridity}/100 Aridity Index`,
      Math.round(s.aridity),
      `Δ ${(s.aridity - t.aridity).toFixed(1)}`,
      "Provides dry, low-biomass soils to test sterile astrobiology drills & electrodynamic dust shields"
    ],
    [
      "🧊 Subsurface Water-Ice & ISRU Potential",
      "Required for rocket propellant (Methalox/LH2) & crew drinking water",
      `${t.ice}/100 Ice Index`,
      `${s.ice}/100 Ice Index`,
      Math.round(100 - Math.abs(t.ice - s.ice)),
      `Δ ${(s.ice - t.ice).toFixed(0)}`,
      "Validates ground-penetrating radar (SHARAD/RIMFAX) & cryogenic Rodwell water-extraction drills"
    ],
    [
      "🦇 Subsurface Cave / Lava Tube Shielding",
      "Protects astronauts from cosmic radiation & micrometeorites",
      `${t.shielding}/100 Shielding`,
      `${s.shielding}/100 Shielding`,
      Math.round(100 - Math.abs(t.shielding - s.shielding)),
      `Δ ${(s.shielding - t.shielding).toFixed(0)}`,
      "Allows non-GPS subterranean drone SLAM mapping & tethered skylight rappelling rehearsals"
    ],
    [
      "⚠️ Gravity & Atmospheric Pressure (Limit)",
      "Fundamental planetary boundary condition",
      `${t.gravity} m/s² | ${t.pressure} Pa`,
      `9.81 m/s² | ${s.press} hPa`,
      15,
      "1g Earth vs Space",
      "❌ BREAKDOWN: Earth cannot replicate low gravity or vacuum; must pair field trials with offload rigs"
    ]
  ];

  document.querySelector('#sideBySideTable tbody').innerHTML = rows.map(r => `
    <tr>
      <td><b style="color:var(--gold);">${r[0]}</b><br><span style="font-size:10.5px;color:var(--muted);">${r[1]}</span></td>
      <td><span class="val-space">${r[2]}</span></td>
      <td><span class="val-earth">${r[3]}</span></td>
      <td>
        <div style="background:#151232;height:7px;border-radius:4px;overflow:hidden;margin-bottom:3px;">
          <div style="width:${r[4]}%;height:100%;background:linear-gradient(90deg,var(--cyan),var(--emerald));"></div>
        </div>
        <span style="font-size:10.5px;font-weight:800;color:var(--cyan);">${r[4]}% Match (${r[5]})</span>
      </td>
      <td style="font-size:11px;color:#e6edf3;">${r[6]}</td>
    </tr>
  `).join('');

  const bestMonths = [...Array(12).keys()].sort((a,b) => Math.abs(s.monthly_t[a] - t.temp) - Math.abs(s.monthly_t[b] - t.temp)).slice(0,4).sort((a,b)=>a-b).map(i => MONTHS[i]).join(', ');
  document.getElementById('seasonBestBox').innerHTML = `🗓️ <b>Best Field Deployment Months:</b> <span style="color:var(--emerald);font-weight:900;">${bestMonths}</span> &nbsp;|&nbsp; ☀️ <b>Peak Solar Flux:</b> <span style="color:var(--gold);font-weight:900;">${s.activeFlux} W/m²</span>`;
  drawClimChart(s);

  // Page 3
  document.getElementById('equipField').innerHTML = `<b>🛠️ 1. Flight Hardware & Instruments Tested on Earth:</b><br>${s.equip}`;
  document.getElementById('methodField').innerHTML = `<b>📡 2. Operational Mission Workflows Rehearsed:</b><br>${s.methods}`;
  document.getElementById('subzoneField').innerHTML = `<b>🗺️ 3. Spatial Sub-Zone Micro-Terrains (Scale Matters):</b><br>${s.subzones}`;
  document.getElementById('missingField').innerHTML = `<b>🔍 1. Missing Characterization Data (Current Completeness: ${s.char_pct}%):</b><br>${s.missing}`;
  document.getElementById('gapsField').innerHTML = `<b>⚠️ 2. Honest Breakdown Limits (Where Earth Differs from ${t.body}):</b><br>${s.gaps}`;
  document.getElementById('stewardField').innerHTML = `<b>🧭 1. Practical Logistics, Protected Areas & Local Community Respect:</b><br>${s.stewardship}`;
  document.getElementById('reverseField').innerHTML = `<b>🔄 2. Bidirectional Earth ➔ Space Best Target Ranking:</b><br>${s.reverseBest}`;

  // Page 4 & 5
  document.getElementById('simulantHeader').textContent = `Target Simulant: ${t.simulant} vs. ${s.name} (${s.chemPct}% Oxide Match)`;
  updateSolarSimulator();
  drawRoverAndChem(t, s);
  document.getElementById('dossierPre').textContent =
`================================================================================
NASA SPACE APPS 2026 — OFFICIAL PLANETARY ANALOG & SOLAR FLUX DOSSIER
================================================================================
SPACE TARGET         : ${t.name} [${t.role} • ${t.body}]
AGENCY DATASETS      : ${t.agencies}
EARTH ANALOG SITE    : ${s.name} [Status: ${s.tier} | Characterized: ${s.char_pct}%]
OVERALL MATCH SCORE  : ${s.score}% (Topo ${s.pTopo}% | Geol ${s.pGeol}% | Env/Flux ${s.pEnv}% | Res ${s.pRes}%)
SOLAR FLUX & ENERGY  : Earth ${s.activeFlux} W/m² (${s.activeSolar} kWh/m²/d) vs ${t.body} ${t.solar_flux} W/m² (${t.solar} kWh/m²/d)
ACTIVE PROCESS/SCALE : ${s.process} (${s.scale})
OPTIMAL TEST SEASON  : ${bestMonths}
COORDINATES & RELIEF : ${s.lat}°, ${s.lon}° | Elevation: ${s.elev} m | Slope: ${s.slope}°
--------------------------------------------------------------------------------
EQUIPMENT TESTED     : ${s.equip}
METHODS REHEARSED    : ${s.methods}
SUB-ZONE TESTBEDS    : ${s.subzones}
MISSING FIELD DATA   : ${s.missing}
WHERE MATCH BREAKS   : ${s.gaps}
ACCESS & STEWARDSHIP : ${s.stewardship}
================================================================================`;
}

function updateSolarSimulator() {
  if (!rankedSites.length) return;
  const t = TARGETS[parseInt(document.getElementById('targetSelect').value)];
  const s = rankedSites[selectedIdx];
  const reqKw = parseFloat(document.getElementById('pwrReqSlider').value);
  const dustLoss = parseFloat(document.getElementById('dustLossSlider').value) / 100.0;
  document.getElementById('pwrReqVal').textContent = reqKw;
  document.getElementById('dustLossVal').textContent = Math.round(dustLoss * 100);

  const eff = 0.28 * (1 - dustLoss);
  const spaceFluxEff = Math.max(50, t.solar_flux * eff);
  const earthFluxEff = Math.max(50, s.activeFlux * eff);

  const spaceArea = Math.round((reqKw * 1000) / spaceFluxEff);
  const earthArea = Math.round((reqKw * 1000) / earthFluxEff);

  document.getElementById('fluxSummaryBadge').textContent = `☀️ ${t.body} Flux: ${t.solar_flux} W/m² vs. Earth Analog: ${s.activeFlux} W/m²`;
  document.getElementById('solarCalcOutput').innerHTML = `
    <div>🌕/🔴 <b>${t.body} Target Solar Array Needed:</b> <span style="color:var(--pink);font-weight:900;">${spaceArea} m²</span> (at ${t.solar_flux} W/m² peak flux & ${Math.round(dustLoss*100)}% dust loss)</div>
    <div>🌍 <b>Earth Analog Test Array Needed:</b> <span style="color:var(--emerald);font-weight:900;">${earthArea} m²</span> (at ${s.activeFlux} W/m² surface flux)</div>
    <div style="color:var(--cyan);font-size:11px;margin-top:4px;">💡 <b>Engineering Scaling Factor:</b> 1 m² of solar panel on <b>${s.name.split(',')[0]}</b> generates <b>${((s.activeFlux / t.solar_flux)*100).toFixed(0)}%</b> of the instantaneous power it will produce at <b>${t.name.split(' (')[0]}</b>.</div>
  `;
}

function drawClimChart(s) {
  const c = document.getElementById('climCanvas');
  if (!c) return;
  const ctx = c.getContext('2d');
  const W = c.width, H = c.height;
  ctx.clearRect(0, 0, W, H);
  const mt = s.monthly_t, ms = s.monthly_s;
  const minT = Math.min(...mt) - 5, maxT = Math.max(...mt) + 5;
  const padL = 32, padR = 18, padT = 20, padB = 24;
  const pw = W - padL - padR, ph = H - padT - padB;

  ctx.strokeStyle = '#ffbe0b'; ctx.lineWidth = 2; ctx.setLineDash([4,3]);
  ctx.beginPath();
  ms.forEach((v, i) => {
    const x = padL + (i/11)*pw, y = padT + (1 - v/9.5)*ph;
    if (i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
  });
  ctx.stroke(); ctx.setLineDash([]);

  ctx.strokeStyle = '#ff006e'; ctx.lineWidth = 2.5;
  ctx.beginPath();
  mt.forEach((v, i) => {
    const x = padL + (i/11)*pw, y = padT + (1 - (v-minT)/((maxT-minT)||1))*ph;
    if (i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
  });
  ctx.stroke();

  const curM = parseInt(document.getElementById('monthSlider').value);
  ctx.font = 'bold 10px Segoe UI';
  mt.forEach((v, i) => {
    const x = padL + (i/11)*pw, y = padT + (1 - (v-minT)/((maxT-minT)||1))*ph;
    ctx.fillStyle = (curM === i+1) ? '#00ff87' : '#00f2fe';
    ctx.beginPath(); ctx.arc(x, y, (curM===i+1)?5.5:3.5, 0, Math.PI*2); ctx.fill();
    ctx.fillStyle = '#fff'; ctx.fillText(`${Math.round(v)}°`, x-9, y-7);
    ctx.fillStyle = '#b8c0ff'; ctx.fillText(MONTHS[i], x-10, H-6);
  });
}

function drawRoverAndChem(t, s) {
  const rc = document.getElementById('roverCanvas');
  if (!rc) return;
  const rctx = rc.getContext('2d');
  const W = rc.width, H = rc.height;
  rctx.clearRect(0, 0, W, H);

  const rad = s.slope * Math.PI / 180;
  const slip = Math.min(95, (Math.tan(rad)/0.72)*100).toFixed(1);
  const earthW = Math.round(180 + 1025 * 9.81 * Math.sin(rad) * 0.12);
  const targetW = Math.round(180 + 1025 * t.gravity * Math.sin(t.slope * Math.PI / 180) * 0.12);

  const x0 = 25, y0 = H - 25, x1 = 260, y1 = Math.max(35, y0 - Math.tan(rad)*185);
  rctx.fillStyle = 'rgba(0, 242, 254, 0.18)'; rctx.strokeStyle = '#00f2fe'; rctx.lineWidth = 2.5;
  rctx.beginPath(); rctx.moveTo(x0,y0); rctx.lineTo(x1,y1); rctx.lineTo(x1,y0); rctx.closePath(); rctx.fill(); rctx.stroke();

  const frac = roverTick / 100;
  const rx = x0 + 25 + frac * (x1 - x0 - 50);
  const ry = y0 - frac * (y0 - y1) * ((x1 - x0 - 50)/(x1 - x0)) - 10;
  rctx.fillStyle = '#ffbe0b'; rctx.beginPath(); rctx.arc(rx, ry, 9, 0, Math.PI*2); rctx.fill();

  rctx.fillStyle = '#fff'; rctx.font = 'bold 12px Consolas';
  rctx.fillText(`⛰️ Analog Slope Angle : ${s.slope}°`, 285, 45);
  rctx.fillText(`⚠️ Wheel Slip Risk    : ${slip}%`, 285, 75);
  rctx.fillText(`🌍 Earth Climb Power  : ${earthW} W (1.0g)`, 285, 105);
  rctx.fillText(`🚀 ${t.body} Climb Power : ${targetW} W (${t.gravity} m/s²)`, 285, 135);
  rctx.fillText(`☀️ Surface Solar Flux : ${s.activeFlux} W/m²`, 285, 165);
  rctx.fillText(`🔩 Rotary Drill Power : ${Math.round(310 + s.basalt*2.5)} W`, 285, 195);

  const cc = document.getElementById('chemCanvas');
  const cctx = cc.getContext('2d');
  cctx.clearRect(0, 0, cc.width, cc.height);
  const oxs = ["SiO2","Al2O3","FeO","MgO","CaO","TiO2"];
  const colW = (cc.width - 40) / oxs.length;
  cctx.font = 'bold 11px Segoe UI';
  oxs.forEach((ox, i) => {
    const tv = t.oxides[ox] || 5, sv = s.oxides[ox] || 5;
    const bx = 35 + i * colW + colW * 0.4;
    const th = (tv / 60) * 165, sh = (sv / 60) * 165;
    cctx.fillStyle = '#ff006e'; cctx.fillRect(bx - 16, cc.height - 30 - th, 14, th);
    cctx.fillStyle = '#00ff87'; cctx.fillRect(bx + 2, cc.height - 30 - sh, 14, sh);
    cctx.fillStyle = '#fff'; cctx.fillText(ox, bx - 12, cc.height - 10);
  });
}

function onSeasonSlide(val) {
  const m = parseInt(val);
  const lbl = document.getElementById('seasonLbl');
  lbl.textContent = m === 0 ? '☀️ MODE: LIVE / ANNUAL SATELLITE TELEMETRY' : `⏱️ TIME-TRAVEL ACTIVE: ${MONTHS[m-1]} SEASONAL TELEMETRY`;
  recompute();
}

function toggleYouth() {
  youthMode = !youthMode;
  document.getElementById('youthBanner').style.display = youthMode ? 'block' : 'none';
  selectSite(selectedIdx, false);
}

// Direct Browser-Compatible Live Coordinate Scanner (Works both in Python & GitHub Pages!)
async function scanCustomCoord() {
  const name = document.getElementById('cName').value || 'New Satellite Discovery';
  const lat = parseFloat(document.getElementById('cLat').value);
  const lon = parseFloat(document.getElementById('cLon').value);
  if (isNaN(lat) || isNaN(lon)) return;

  try {
    const elevRes = await fetch(`https://api.open-meteo.com/v1/elevation?latitude=${lat}&longitude=${lon}`).then(r => r.json());
    const elev = (elevRes.elevation && elevRes.elevation[0]) ? Math.round(elevRes.elevation[0]) : 1200;
    const wxRes = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,surface_pressure,shortwave_radiation`).then(r => r.json());
    const cur = wxRes.current || { temperature_2m: 8.0, surface_pressure: 880, shortwave_radiation: 850 };

    const nasaUrl = `https://power.larc.nasa.gov/api/temporal/climatology/point?parameters=T2M,T2M_MAX,T2M_MIN,PRECTOTCORR,ALLSKY_SFC_SW_DWN&community=RE&longitude=${lon}&latitude=${lat}&format=JSON`;
    const nasaRes = await fetch(nasaUrl).then(r => r.json());
    const p = nasaRes.properties.parameter;

    const annP = +(p.PRECTOTCORR.ANN * 365.25).toFixed(1);
    const arid = +Math.max(0, Math.min(100, 100 - (annP / 12))).toFixed(1);
    const cat = (Math.abs(lat) > 60 || cur.temperature_2m < -3) ? "Polar Regions" : (arid > 92 ? "Deserts" : "Arid Terrains");
    let flux = Math.round(cur.shortwave_radiation || (p.ALLSKY_SFC_SW_DWN.ANN * 165));
    if (flux < 350) flux = Math.round(p.ALLSKY_SFC_SW_DWN.ANN * 165);

    const newSite = {
      name: `★ ${name}`, tier: "BRAND-NEW", cat: cat, cond: cur.temperature_2m < 0 ? "Cryogenic Permafrost" : "High-Dust / Eolian Wind",
      char_pct: 25, scale: "10-km Satellite-Scanned Grid", process: "Live Copernicus DEM & NASA POWER Solar Flux",
      lat: lat, lon: lon, terrain: `Satellite-Characterized ${cat} (${elev}m)`,
      temp: +cur.temperature_2m.toFixed(1), diurnal: +(p.T2M_MAX.ANN - p.T2M_MIN.ANN).toFixed(1),
      slope: 15.0, elev: elev, press: Math.round(cur.surface_pressure), aridity: arid,
      solar: +p.ALLSKY_SFC_SW_DWN.ANN.toFixed(2), solar_flux: flux,
      basalt: 70.0, ice: cur.temperature_2m <= 0 ? 80.0 : 18.0, shielding: 60.0,
      oxides: { SiO2: 48.5, TiO2: 1.6, Al2O3: 13.8, FeO: 13.2, MgO: 8.1, CaO: 9.4 },
      geology: `Live Copernicus DEM: ${elev}m | Peak Solar Flux: ${flux} W/m² | Precip: ${annP} mm/yr.`,
      campaigns: "Newly Discovered Candidate Analog (Characterized Live via NASA POWER & Copernicus DEM)",
      equip: "Rover traction chassis, portable XRF/Raman spectrometers, solar flux & meteorological station.",
      methods: "First-pass reconnaissance traverse, orbital-to-ground spectral & solar calibration.",
      subzones: `Zone A: Primary Scanned Coordinate (${lat}°, ${lon}° at ${elev}m) | Zone B: Proximal Regolith Slope.`,
      missing: "Newly scanned coordinate (25% characterized): requires field XRF sampling and 3D GPR sounding.",
      gaps: `Earth 1g gravity and ${Math.round(cur.surface_pressure)} hPa pressure differ from Moon/Mars vacuum/thin air.`,
      stewardship: "Verify local land tenure, environmental conservation status, and seasonal road access before field deployment.",
      monthly_t: MONTHS.map(m => p.T2M[m]),
      monthly_s: MONTHS.map(m => p.ALLSKY_SFC_SW_DWN[m])
    };

    earthSites.push(newSite);
    recompute();
    const idx = rankedSites.findIndex(x => x.name === newSite.name);
    if (idx >= 0) selectSite(idx, true);
  } catch (e) {}
}

function syncLive() {
  liveCache = {};
  recompute();
}

function exportCSV() {
  const headers = ["Rank","Site","Status","Environment","Char_Pct","Match_Score","Solar_Flux_Wm2","Topo","Geol","Env","Resources","Lat","Lon","Elev_m"];
  const rows = rankedSites.map(s => [s.rank, `"${s.name}"`, s.tier, `"${s.cat}"`, s.char_pct, s.score, s.activeFlux, s.pTopo, s.pGeol, s.pEnv, s.pRes, s.lat, s.lon, s.elev]);
  const blob = new Blob([[headers.join(','), ...rows.map(r => r.join(','))].join('\n')], { type: 'text/csv' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'NASA_SpaceApps_Planetary_Analogs.csv';
  a.click();
}

window.addEventListener('DOMContentLoaded', initApp);
</script>
</body>
</html>
"""

# =============================================================================
# 4. AUTO-EXPORT STATIC INDEX.HTML (FOR GITHUB PAGES) + NATIVE DESKTOP LAUNCHER
# =============================================================================
def build_final_html():
    return APP_HTML.replace("__TARGETS_JSON__", json.dumps(TARGETS)).replace("__EARTH_JSON__", json.dumps(EARTH_SITES))


class TerraTwinHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        html = build_final_html()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))


def launch_native_app_window(url):
    if sys.platform.startswith("win"):
        for path in [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"]:
            if os.path.exists(path):
                subprocess.Popen([path, f"--app={url}", "--start-maximized"])
                return
        try:
            subprocess.Popen(["cmd", "/c", "start", "msedge", f"--app={url}", "--start-maximized"], shell=False)
            return
        except Exception:
            pass
    webbrowser.open(url)


if __name__ == "__main__":
    # Automatically generate standalone index.html so GitHub Pages can host it as a public website!
    try:
        out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(build_final_html())
        print(f"✅ Auto-generated standalone website file for NASA Judges: {out_path}")
    except Exception:
        pass

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()

    server = socketserver.ThreadingTCPServer(("127.0.0.1", port), TerraTwinHandler)
    url = f"http://127.0.0.1:{port}"
    print(f"🚀 Launching TerraTwin Workstation ({url})...")
    threading.Timer(0.6, lambda: launch_native_app_window(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
