import streamlit as st
import pandas as pd
import joblib

# Configure page settings
st.set_page_config(
    page_title="Performance Car Price Estimator",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load the trained model
model = joblib.load("luxuryCar.pkl")

# Updated column list
columns = [
    'Year', 'Horsepower', 'Engine Cylinders', 'Number of Doors', 'Highway MPG', 'City MPG',
 
    'Engine Fuel Type_diesel', 'Engine Fuel Type_flex-fuel (unleaded/E85)', 
    'Engine Fuel Type_premium unleaded (recommended)', 'Engine Fuel Type_premium unleaded (required)',
    'Engine Fuel Type_regular unleaded',

    'Transmission Type_AUTOMATED_MANUAL', 'Transmission Type_AUTOMATIC', 'Transmission Type_MANUAL',

    'Driven Wheels_all wheel drive', 'Driven Wheels_four wheel drive', 'Driven Wheels_front wheel drive', 'Driven Wheels_rear wheel drive',
    
    'Vehicle Size_Compact', 'Vehicle Size_Large', 'Vehicle Size_Midsize',
    
    'Vehicle Style_Convertible', 'Vehicle Style_Coupe', 'Vehicle Style_Hatchback', 'Vehicle Style_Pickup', 'Vehicle Style_SUV',
    'Vehicle Style_Sedan', 'Vehicle Style_Van', 'Vehicle Style_Wagon',
    
    'Market Category Simplified_compact', 'Market Category Simplified_crossover', 'Market Category Simplified_diesel',
    'Market Category Simplified_green', 'Market Category Simplified_luxury',
    'Market Category Simplified_performance'
]

brand_avg = {'Acura': 35344.18407960199,
 'Alfa Romeo': 61025.0,
 'Aston Martin': 196135.02631578947,
 'Audi': 53234.13409961686,
 'BMW': 61792.86055776892,
 'Bentley': 251977.28813559323,
 'Bugatti': 1757223.6666666667,
 'Buick': 29298.218543046358,
 'Cadillac': 56154.78658536585,
 'Chevrolet': 28288.620283018867,
 'Chrysler': 27226.766233766233,
 'Dodge': 25328.797647058822,
 'FIAT': 21689.761904761905,
 'Ferrari': 235356.57692307694,
 'Ford': 28353.208841463416,
 'GMC': 32295.108465608464,
 'Genesis': 46616.666666666664,
 'HUMMER': 37384.09090909091,
 'Honda': 26483.925501432666,
 'Hyundai': 24860.28502415459,
 'Infiniti': 42482.9094488189,
 'Kia': 25302.36526946108,
 'Lamborghini': 329095.55555555556,
 'Land Rover': 69151.67226890757,
 'Lexus': 48406.346153846156,
 'Lincoln': 44031.62903225807,
 'Lotus': 67144.13043478261,
 'Maserati': 114751.55555555556,
 'Maybach': 578815.3846153846,
 'Mazda': 20488.4375,
 'McLaren': 217766.66666666666,
 'Mercedes-Benz': 72131.4513618677,
 'Mitsubishi': 20724.679012345678,
 'Nissan': 28460.852193995383,
 'Oldsmobile': 12289.145454545454,
 'Plymouth': 2813.4166666666665,
 'Pontiac': 20085.601398601397,
 'Porsche': 103097.90384615384,
 'Rolls-Royce': 348603.4,
 'Saab': 27840.532608695652,
 'Scion': 19957.448979591838,
 'Spyker': 219990.0,
 'Subaru': 24281.75,
 'Suzuki': 17830.045801526718,
 'Toyota': 29028.739894551847,
 'Volkswagen': 28800.742489270386,
 'Volvo': 29815.327188940093}


# Extract dropdown options from column names
makes = sorted(brand_avg.keys())
fuel_types = sorted([col.replace("Engine Fuel Type_", "") for col in columns if col.startswith("Engine Fuel Type_")])
transmissions = sorted([col.replace("Transmission Type_", "") for col in columns if col.startswith("Transmission Type_")])
drivetrains = sorted([col.replace("Driven Wheels_", "") for col in columns if col.startswith("Driven Wheels_")])
vehicle_sizes = sorted([col.replace("Vehicle Size_", "") for col in columns if col.startswith("Vehicle Size_")])
vehicle_styles = sorted([col.replace("Vehicle Style_", "") for col in columns if col.startswith("Vehicle Style_")])

# Custom CSS for performance-tech theme
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');

/* Global styling */
.stApp {
    background: linear-gradient(135deg, #0a0a0a 0%, #1c1c1c 30%, #212121 100%);
    color: #ffffff;
}

/* Main container */
.main > div {
    padding-top: 1rem;
    padding-bottom: 2rem;
}

/* Hero section with startup animation */
.hero-section {
    background: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.6)), 
                radial-gradient(circle at 50% 50%, #d32f2f 0%, #000000 70%);
    padding: 4rem 2rem;
    text-align: center;
    margin-bottom: 3rem;
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(211, 47, 47, 0.3);
    position: relative;
    overflow: hidden;
    animation: heroFadeIn 1.5s ease-in-out;
}

.hero-section::before {
    content: "";
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    animation: shine 3s infinite;
}

@keyframes heroFadeIn {
    0% { opacity: 0; transform: translateY(30px); }
    100% { opacity: 1; transform: translateY(0); }
}

@keyframes shine {
    0% { left: -100%; }
    100% { left: 100%; }
}

.hero-title {
    font-family: 'Orbitron', monospace;
    font-size: 4rem;
    font-weight: 900;
    background: linear-gradient(45deg, #d32f2f, #ff6b6b, #d32f2f);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1rem;
    text-transform: uppercase;
    letter-spacing: 3px;
    animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
    from { text-shadow: 0 0 20px rgba(211, 47, 47, 0.5); }
    to { text-shadow: 0 0 30px rgba(211, 47, 47, 0.8); }
}

.hero-subtitle {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.6rem;
    color: #8e8e8e;
    margin-bottom: 2rem;
    font-weight: 400;
    letter-spacing: 1px;
}

/* Section styling */
.section-header {
    font-family: 'Orbitron', monospace;
    font-size: 2rem;
    color: #d32f2f;
    margin: 3rem 0 2rem 0;
    padding: 1rem 0;
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 2px;
    position: relative;
}

.section-header::after {
    content: "";
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 100px;
    height: 3px;
    background: linear-gradient(90deg, transparent, #d32f2f, transparent);
}

/* Glassmorphism cards */
.element-container > div > div[data-testid="stHorizontalBlock"] {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 2.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
    transition: all 0.3s ease-in-out;
    position: relative;
    overflow: hidden;
}

.element-container > div > div[data-testid="stHorizontalBlock"]:hover {
    border-color: rgba(211, 47, 47, 0.3);
    box-shadow: 0 20px 50px rgba(211, 47, 47, 0.2);
    transform: translateY(-5px);
}

/* Column styling */
div[data-testid="column"] {
    background: transparent;
    padding: 0.5rem;
}

/* Input field styling with hover effects */
.stSelectbox > div > div {
    background-color: rgba(28, 28, 28, 0.8) !important;
    border: 2px solid rgba(142, 142, 142, 0.3) !important;
    border-radius: 12px !important;
    color: #ffffff !important;
    transition: all 0.2s ease-in-out !important;
}

.stSelectbox > div > div:hover {
    border-color: rgba(211, 47, 47, 0.6) !important;
    box-shadow: 0 0 15px rgba(211, 47, 47, 0.3) !important;
}

.stSelectbox > div > div:focus-within {
    border-color: #d32f2f !important;
    box-shadow: 0 0 20px rgba(211, 47, 47, 0.5) !important;
}

.stNumberInput > div > div > input {
    background-color: rgba(28, 28, 28, 0.8) !important;
    border: 2px solid rgba(142, 142, 142, 0.3) !important;
    border-radius: 12px !important;
    color: #ffffff !important;
    transition: all 0.2s ease-in-out !important;
}

.stNumberInput > div > div > input:hover {
    border-color: rgba(211, 47, 47, 0.6) !important;
    box-shadow: 0 0 15px rgba(211, 47, 47, 0.3) !important;
}

.stNumberInput > div > div > input:focus {
    border-color: #d32f2f !important;
    box-shadow: 0 0 20px rgba(211, 47, 47, 0.5) !important;
}

/* Checkbox styling with glow effects */
.stCheckbox > label {
    color: #ffffff !important;
    font-weight: 500 !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.1rem !important;
    transition: all 0.2s ease-in-out !important;
}

.stCheckbox > label:hover {
    color: #d32f2f !important;
}

.stCheckbox > label > span {
    background-color: rgba(28, 28, 28, 0.8) !important;
    border: 2px solid #d32f2f !important;
    border-radius: 6px !important;
    transition: all 0.2s ease-in-out !important;
}

.stCheckbox > label > span:hover {
    box-shadow: 0 0 10px rgba(211, 47, 47, 0.5) !important;
}

/* High-performance button styling */
.stButton > button {
    background: linear-gradient(135deg, #d32f2f 0%, #8b0000 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 15px !important;
    padding: 1rem 4rem !important;
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    font-family: 'Orbitron', monospace !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    transition: all 0.3s ease-in-out !important;
    box-shadow: 0 8px 25px rgba(211, 47, 47, 0.4) !important;
    width: 100% !important;
    margin-top: 2rem !important;
    position: relative !important;
    overflow: hidden !important;
}

.stButton > button::before {
    content: "";
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.5s;
}

.stButton > button:hover::before {
    left: 100%;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #ff1744 0%, #d32f2f 100%) !important;
    box-shadow: 0 15px 40px rgba(211, 47, 47, 0.6) !important;
    transform: translateY(-3px) !important;
}

/* Result card with performance styling */
.result-card {
    background: linear-gradient(145deg, rgba(28, 28, 28, 0.9), rgba(33, 33, 33, 0.9));
    backdrop-filter: blur(20px);
    padding: 3rem;
    border-radius: 20px;
    text-align: center;
    border: 2px solid #d32f2f;
    box-shadow: 0 25px 60px rgba(211, 47, 47, 0.4);
    margin-top: 3rem;
    position: relative;
    overflow: hidden;
    animation: resultSlideUp 0.8s ease-out;
}

@keyframes resultSlideUp {
    0% { opacity: 0; transform: translateY(50px); }
    100% { opacity: 1; transform: translateY(0); }
}

.result-title {
    font-family: 'Orbitron', monospace;
    font-size: 1.8rem;
    color: #d32f2f;
    margin-bottom: 1.5rem;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.result-price {
    font-family: 'Orbitron', monospace;
    font-size: 4rem;
    font-weight: 900;
    background: linear-gradient(45deg, #d32f2f, #ff6b6b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 2rem;
    animation: priceGlow 2s ease-in-out infinite alternate;
}

@keyframes priceGlow {
    from { filter: drop-shadow(0 0 10px rgba(211, 47, 47, 0.5)); }
    to { filter: drop-shadow(0 0 20px rgba(211, 47, 47, 0.8)); }
}

.result-disclaimer {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1rem;
    color: #8e8e8e;
    font-style: italic;
    margin-top: 1.5rem;
    line-height: 1.6;
}

/* Performance tier badges */
.tier-badge {
    display: inline-block;
    padding: 0.8rem 1.5rem;
    border-radius: 25px;
    font-family: 'Orbitron', monospace;
    font-weight: 700;
    font-size: 1.1rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 1rem 0;
    animation: badgePulse 2s infinite;
}

@keyframes badgePulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

.tier-hypercar { background: linear-gradient(45deg, #d32f2f, #8b0000); color: white; }
.tier-supercar { background: linear-gradient(45deg, #ff9800, #f57c00); color: white; }
.tier-luxury { background: linear-gradient(45deg, #ffc107, #ff8f00); color: black; }
.tier-entry { background: linear-gradient(45deg, #4caf50, #2e7d32); color: white; }

/* Labels styling */
label {
    font-family: 'Rajdhani', sans-serif !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    letter-spacing: 0.5px !important;
}

/* Mobile optimization */
@media (max-width: 768px) {
    .hero-title {
        font-size: 2.5rem;
        letter-spacing: 1px;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
    }
    
    .section-header {
        font-size: 1.5rem;
        letter-spacing: 1px;
    }
    
    .result-price {
        font-size: 2.5rem;
    }
    
    .element-container > div > div[data-testid="stHorizontalBlock"] {
        padding: 1.5rem;
    }
}

/* Performance specs summary */
.specs-summary {
    background: rgba(211, 47, 47, 0.1);
    border: 1px solid rgba(211, 47, 47, 0.3);
    border-radius: 15px;
    padding: 1.5rem;
    margin: 2rem 0;
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.2rem;
    color: #ffffff;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section" style="max-width: 1200px; margin: 0 auto;">
    <div class="hero-title" style="font-size:5rem;">Luxury Car Price Predictor</div>
    <div class="hero-subtitle">Enter specs. Get accurate predictions. Unleash the value.</div>
</div>
<div style="height: 3.5rem;"></div>
""", unsafe_allow_html=True)

# Center all input sections using a centered container and equal columns
center_style = "max-width: 700px; margin-left: auto; margin-right: auto;"

# Engine Specifications Section
st.markdown(f'<div class="section-header" style="{center_style}">Engine Specifications</div>', unsafe_allow_html=True)
with st.container():
    col1, col2, col3 = st.columns([1, 1, 1], gap="large")
    with col1:
        year = st.slider("Year", min_value=1990, max_value=2026, value=2021, step=1)
        horsepower = st.slider("Horsepower", min_value=100, max_value=1200, value=400, step=10)
    with col2:
        engine_cylinders_options = [3, 4, 5, 6, 8, 10, 12, 16]
        engine_cylinders_idx = engine_cylinders_options.index(8) if 8 in engine_cylinders_options else 0
        engine_cylinders = st.select_slider(
            "Engine Cylinders",
            options=engine_cylinders_options,
            value=engine_cylinders_options[engine_cylinders_idx]
        )
        fuel_type = st.selectbox("Engine Fuel Type", fuel_types)
    with col3:
        highway_mpg = st.slider("Highway MPG", min_value=10, max_value=50, value=25, step=1)
        city_mpg = st.slider("City MPG", min_value=8, max_value=40, value=18, step=1)

# Vehicle Details Section
st.markdown(f'<div class="section-header" style="{center_style}">Body Style & Configuration</div>', unsafe_allow_html=True)
with st.container():
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        make = st.selectbox("Make", makes)
        num_doors = st.selectbox("Number of Doors", [2, 3, 4])
        transmission = st.selectbox("Transmission Type", transmissions)
    with col2:
        driven_wheels = st.selectbox("Driven Wheels", drivetrains)
        vehicle_size = st.selectbox("Vehicle Size", vehicle_sizes)
        vehicle_style = st.selectbox("Vehicle Style", vehicle_styles)

# Market Categories Section
st.markdown(f'<div class="section-header" style="{center_style}">Market Categories</div>', unsafe_allow_html=True)
with st.container():
    col1, col2, col3 = st.columns([1, 1, 1], gap="large")
    with col1:
        luxury = st.checkbox("Luxury", value=True)
        performance = st.checkbox("Performance", value=True)
    with col2:
        green = st.checkbox("Green Vehicle")
        diesel = st.checkbox("Diesel")
    with col3:
        crossover = st.checkbox("Crossover")
        compact = st.checkbox("Compact")

# Prediction logic
if st.button("Predict MSRP"):
    # Initialize input data with zeros for all model features
    input_data = {col: 0 for col in model.feature_names_in_}
    
    # Set the basic numerical features
    input_data.update({
        'Year': year,
        'Horsepower': horsepower,
        'Engine Cylinders': engine_cylinders,
        'Number of Doors': num_doors,
        'Highway MPG': highway_mpg,
        'City MPG': city_mpg,
    })

    # Step 1: Use Make_encoded with brand average values
    if 'Make_encoded' in model.feature_names_in_:
        input_data['Make_encoded'] = brand_avg.get(make, sum(brand_avg.values()) / len(brand_avg))
    else:
        # Fallback to one-hot encoding if Make_encoded doesn't exist
        make_col = f"Make_{make}"
        if make_col in model.feature_names_in_:
            input_data[make_col] = 1

    # Step 2: Fix one-hot encoding for categorical variables
    for prefix, value in [
        ('Engine Fuel Type_', fuel_type),
        ('Transmission Type_', transmission),
        ('Driven Wheels_', driven_wheels),
        ('Vehicle Size_', vehicle_size),
        ('Vehicle Style_', vehicle_style)
    ]:
        col_name = f"{prefix}{value}"
        if col_name in model.feature_names_in_:
            input_data[col_name] = 1

    # Step 3: Fix performance tag checkboxes
    if luxury and "Market Category Simplified_luxury" in model.feature_names_in_:
        input_data['Market Category Simplified_luxury'] = 1
    if performance and "Market Category Simplified_performance" in model.feature_names_in_:
        input_data['Market Category Simplified_performance'] = 1
    if green and "Market Category Simplified_green" in model.feature_names_in_:
        input_data['Market Category Simplified_green'] = 1
    if diesel and "Market Category Simplified_diesel" in model.feature_names_in_:
        input_data['Market Category Simplified_diesel'] = 1
    if crossover and "Market Category Simplified_crossover" in model.feature_names_in_:
        input_data['Market Category Simplified_crossover'] = 1
    if compact and "Market Category Simplified_compact" in model.feature_names_in_:
        input_data['Market Category Simplified_compact'] = 1

    input_df = pd.DataFrame([input_data])
    
    # Step 4: Ensure columns are in the exact order the model expects
    input_df = input_df[model.feature_names_in_]
    
    prediction = model.predict(input_df)[0]

    # Display result in luxury styled card
    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">Predicted MSRP</div>
        <div class="result-price">${prediction:,.2f}</div>
        <div class="result-disclaimer">
            This estimate is based on historical prices and car specifications. 
            Prices may vary with brand prestige and market fluctuations.
        </div>
    </div>
    """, unsafe_allow_html=True)
