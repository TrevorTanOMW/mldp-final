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

# Enhanced CSS for full-screen interactive panels
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
    padding: 0;
}

/* Hero section with call-to-action */
.hero-section {
    background: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.6)), 
                radial-gradient(circle at 50% 50%, #d32f2f 0%, #000000 70%);
    padding: 6rem 2rem;
    text-align: center;
    margin-bottom: 0;
    position: relative;
    overflow: hidden;
    min-height: 60vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.hero-title {
    font-family: 'Orbitron', monospace;
    font-size: 4.5rem;
    font-weight: 900;
    background: linear-gradient(45deg, #d32f2f, #ff6b6b, #d32f2f);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1.5rem;
    text-transform: uppercase;
    letter-spacing: 3px;
    animation: glow 2s ease-in-out infinite alternate;
}

.hero-subtitle {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2rem;
    color: #cccccc;
    margin-bottom: 3rem;
    font-weight: 400;
    letter-spacing: 1px;
}

.hero-cta {
    background: linear-gradient(135deg, #d32f2f 0%, #8b0000 100%);
    color: white;
    padding: 1.5rem 4rem;
    border: none;
    border-radius: 50px;
    font-family: 'Orbitron', monospace;
    font-size: 1.3rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 10px 30px rgba(211, 47, 47, 0.4);
    text-decoration: none;
    display: inline-block;
}

.hero-cta:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(211, 47, 47, 0.6);
    background: linear-gradient(135deg, #ff1744 0%, #d32f2f 100%);
}

/* Interactive panel cards */
.panel-card {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 25px;
    padding: 3rem;
    margin: 2rem 0;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
    transition: all 0.3s ease-in-out;
}

.panel-card:hover {
    border-color: rgba(211, 47, 47, 0.3);
    box-shadow: 0 25px 80px rgba(211, 47, 47, 0.2);
    transform: translateY(-5px);
}

.panel-title {
    font-family: 'Orbitron', monospace;
    font-size: 2.2rem;
    color: #d32f2f;
    margin-bottom: 2.5rem;
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 2px;
    position: relative;
}

.panel-title::after {
    content: "";
    position: absolute;
    bottom: -10px;
    left: 50%;
    transform: translateX(-50%);
    width: 100px;
    height: 3px;
    background: linear-gradient(90deg, transparent, #d32f2f, transparent);
}

/* Enhanced input styling */
.stSlider > div > div > div {
    background: rgba(28, 28, 28, 0.8) !important;
    border-radius: 15px !important;
}

.stSlider > div > div > div > div {
    background: linear-gradient(135deg, #d32f2f, #8b0000) !important;
    height: 8px !important;
    border-radius: 4px !important;
}

.stRadio > div {
    background: rgba(28, 28, 28, 0.6) !important;
    padding: 1rem !important;
    border-radius: 15px !important;
    border: 1px solid rgba(142, 142, 142, 0.3) !important;
}

.stRadio > div > label {
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    margin-bottom: 1rem !important;
}

.stRadio > div > div > div {
    display: flex !important;
    gap: 1rem !important;
    flex-wrap: wrap !important;
}

.stRadio > div > div > div > label {
    background: rgba(211, 47, 47, 0.1) !important;
    border: 2px solid rgba(211, 47, 47, 0.3) !important;
    border-radius: 12px !important;
    padding: 0.8rem 1.5rem !important;
    margin: 0.3rem !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
    font-size: 1.1rem !important;
    font-weight: 500 !important;
}

.stRadio > div > div > div > label:hover {
    border-color: #d32f2f !important;
    background: rgba(211, 47, 47, 0.2) !important;
    transform: translateY(-2px) !important;
}

.stSelectbox > div > div {
    background-color: rgba(28, 28, 28, 0.8) !important;
    border: 2px solid rgba(142, 142, 142, 0.3) !important;
    border-radius: 15px !important;
    color: #ffffff !important;
    font-size: 1.2rem !important;
    padding: 0.8rem !important;
    transition: all 0.2s ease-in-out !important;
}

.stSelectbox > div > div:hover {
    border-color: rgba(211, 47, 47, 0.6) !important;
    box-shadow: 0 0 20px rgba(211, 47, 47, 0.3) !important;
}

.stCheckbox > label {
    background: rgba(28, 28, 28, 0.6) !important;
    border: 2px solid rgba(142, 142, 142, 0.3) !important;
    border-radius: 15px !important;
    padding: 1.2rem 1.5rem !important;
    margin: 0.5rem 0 !important;
    transition: all 0.2s ease !important;
    font-size: 1.3rem !important;
    font-weight: 600 !important;
    cursor: pointer !important;
}

.stCheckbox > label:hover {
    border-color: #d32f2f !important;
    background: rgba(211, 47, 47, 0.1) !important;
    transform: translateY(-2px) !important;
}

/* Prediction panel styling */
.prediction-panel {
    position: sticky;
    bottom: 0;
    background: linear-gradient(145deg, rgba(28, 28, 28, 0.95), rgba(33, 33, 33, 0.95));
    backdrop-filter: blur(25px);
    border-top: 3px solid #d32f2f;
    padding: 2rem;
    margin-top: 3rem;
    z-index: 1000;
    box-shadow: 0 -10px 40px rgba(211, 47, 47, 0.3);
}

.stButton > button {
    background: linear-gradient(135deg, #d32f2f 0%, #8b0000 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 20px !important;
    padding: 1.5rem 4rem !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    font-family: 'Orbitron', monospace !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    transition: all 0.3s ease-in-out !important;
    box-shadow: 0 10px 30px rgba(211, 47, 47, 0.4) !important;
    width: 100% !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #ff1744 0%, #d32f2f 100%) !important;
    box-shadow: 0 15px 50px rgba(211, 47, 47, 0.6) !important;
    transform: translateY(-3px) !important;
}

/* Result styling */
.result-card {
    background: linear-gradient(145deg, rgba(28, 28, 28, 0.9), rgba(33, 33, 33, 0.9));
    backdrop-filter: blur(20px);
    padding: 3rem;
    border-radius: 25px;
    text-align: center;
    border: 3px solid #d32f2f;
    box-shadow: 0 25px 80px rgba(211, 47, 47, 0.5);
    margin: 2rem 0;
    animation: resultSlideUp 0.8s ease-out;
}

.result-price {
    font-family: 'Orbitron', monospace;
    font-size: 4.5rem;
    font-weight: 900;
    background: linear-gradient(45deg, #d32f2f, #ff6b6b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 1rem 0 2rem 0;
    animation: priceGlow 2s ease-in-out infinite alternate;
}

@keyframes resultSlideUp {
    0% { opacity: 0; transform: translateY(50px); }
    100% { opacity: 1; transform: translateY(0); }
}

@keyframes priceGlow {
    from { filter: drop-shadow(0 0 10px rgba(211, 47, 47, 0.5)); }
    to { filter: drop-shadow(0 0 20px rgba(211, 47, 47, 0.8)); }
}

@keyframes glow {
    from { text-shadow: 0 0 20px rgba(211, 47, 47, 0.5); }
    to { text-shadow: 0 0 30px rgba(211, 47, 47, 0.8); }
}

/* Mobile optimization */
@media (max-width: 768px) {
    .hero-title { font-size: 2.8rem; }
    .hero-subtitle { font-size: 1.4rem; }
    .panel-title { font-size: 1.8rem; }
    .result-price { font-size: 3rem; }
    .panel-card { padding: 2rem 1.5rem; }
}
</style>
""", unsafe_allow_html=True)

# Hero Section with CTA
st.markdown("""
<div class="hero-section">
    <div class="hero-title">🏁 Predict Your Dream Car's MSRP</div>
    <div class="hero-subtitle">Enter your specs. We'll simulate the value.</div>
    <div class="hero-cta" onclick="document.getElementById('engine-panel').scrollIntoView({behavior: 'smooth'})">
        🚀 START PREDICTION
    </div>
</div>
""", unsafe_allow_html=True)

# Engine Performance Panel
st.markdown('<div id="engine-panel"></div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">⚙️ Engine Performance</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        year = st.slider("📅 Year", min_value=1990, max_value=2026, value=2021, step=1)
        horsepower = st.slider("⚡ Horsepower", min_value=100, max_value=1200, value=450, step=10)
        highway_mpg = st.slider("🛣️ Highway MPG", min_value=10, max_value=50, value=25, step=1)
    
    with col2:
        engine_cylinders = st.radio("🔩 Engine Cylinders", [4, 6, 8, 10, 12], index=2, horizontal=True)
        fuel_type = st.selectbox("⛽ Fuel Type", fuel_types, index=fuel_types.index('premium unleaded (required)') if 'premium unleaded (required)' in fuel_types else 0)
        city_mpg = st.slider("🏙️ City MPG", min_value=8, max_value=40, value=18, step=1)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Body & Configuration Panel
with st.container():
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">🚗 Body & Configuration</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        make = st.selectbox("🏷️ Brand", makes, index=makes.index('BMW') if 'BMW' in makes else 0)
        num_doors = st.radio("🚪 Number of Doors", [2, 4], index=0, horizontal=True)
        vehicle_size = st.selectbox("📏 Vehicle Size", vehicle_sizes, index=vehicle_sizes.index('Midsize') if 'Midsize' in vehicle_sizes else 0)
    
    with col2:
        transmission = st.selectbox("⚙️ Transmission", transmissions, index=transmissions.index('AUTOMATIC') if 'AUTOMATIC' in transmissions else 0)
        driven_wheels = st.selectbox("🛞 Drivetrain", drivetrains, index=drivetrains.index('rear wheel drive') if 'rear wheel drive' in drivetrains else 0)
        vehicle_style = st.selectbox("🎨 Style", vehicle_styles, index=vehicle_styles.index('Coupe') if 'Coupe' in vehicle_styles else 0)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Market Category Tags Panel
with st.container():
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">🏆 Market Category Tags</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        luxury = st.checkbox("✨ Luxury", value=True)
    with col2:
        performance = st.checkbox("🏁 Performance", value=True)
    with col3:
        green = st.checkbox("🌱 Green Vehicle")
        diesel = st.checkbox("⛽ Diesel")
    with col4:
        crossover = st.checkbox("🔄 Crossover")
        compact = st.checkbox("📦 Compact")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Prediction Panel (Sticky)
with st.container():
    st.markdown('<div class="prediction-panel">', unsafe_allow_html=True)
    
    if st.button("🚀 Predict MSRP", use_container_width=True):
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

        # Use Make_encoded with brand average values
        if 'Make_encoded' in model.feature_names_in_:
            input_data['Make_encoded'] = brand_avg.get(make, sum(brand_avg.values()) / len(brand_avg))
        else:
            # Fallback to one-hot encoding if Make_encoded doesn't exist
            make_col = f"Make_{make}"
            if make_col in model.feature_names_in_:
                input_data[make_col] = 1

        # Fix one-hot encoding for categorical variables
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

        # Fix performance tag checkboxes
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
        
        # Ensure columns are in the exact order the model expects
        input_df = input_df[model.feature_names_in_]
        
        prediction = model.predict(input_df)[0]

        # Display result
        st.markdown(f"""
        <div class="result-card">
            <div class="result-price">${prediction:,.2f}</div>
            <div style="font-family: 'Rajdhani', sans-serif; font-size: 1.2rem; color: #cccccc; font-style: italic;">
                This estimate is based on historical prices and car specifications. 
                Prices may vary with brand prestige and market fluctuations.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
