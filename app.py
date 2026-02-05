# PendemixAI - COVID-19 Global Vaccination Tracker
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="PendemixAI - COVID-19 Vaccination Tracker",
    page_icon="💉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.8rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #1E3A8A, #3B82F6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #6B7280;
        text-align: center;
        margin-bottom: 2rem;
    }
    /* ===== SMALLER METRIC CARDS ===== */
    .custom-metric-card {
        background: linear-gradient(135deg, #F0F8FF 0%, #E0F2FE 100%);
        padding: 15px 10px;
        border-radius: 12px;
        border-left: 5px solid #3B82F6;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 10px;
        transition: transform 0.3s ease;
        text-align: center;
        height: 130px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        width: 100%;
    }
    .custom-metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 10px rgba(0, 0, 0, 0.08);
    }
    .custom-metric-value {
        font-size: 1.7rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 6px;
        line-height: 1;
    }
    .custom-metric-label {
        font-size: 0.85rem;
        color: #6B7280;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.3px;
        padding: 0 5px;
    }
    /* ===== COMPACT NUMBER FORMATTING ===== */
    .compact-number {
        font-size: 1.5rem;
        font-weight: 800;
    }
    .section-header {
        font-size: 1.6rem;
        color: #3B82F6;
        margin-top: 2rem;
        margin-bottom: 1.2rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #3B82F6;
        font-weight: 600;
    }
    .country-header {
        font-size: 1.6rem;
        color: #1E3A8A;
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 1rem;
        padding: 8px;
        background-color: #F0F8FF;
        border-radius: 8px;
        border-left: 4px solid #10B981;
    }
    .pendemix-badge {
        background: linear-gradient(90deg, #10B981, #3B82F6);
        color: white;
        padding: 4px 12px;
        border-radius: 16px;
        font-weight: 600;
        font-size: 0.8rem;
        display: inline-block;
        margin-left: 8px;
    }
    .country-count {
        font-size: 1rem;
        color: #10B981;
        font-weight: bold;
        margin-left: 8px;
    }
    /* ===== RESPONSIVE DESIGN ===== */
    @media (max-width: 768px) {
        .custom-metric-card {
            height: 110px;
            padding: 12px 8px;
        }
        .custom-metric-value {
            font-size: 1.4rem;
        }
        .custom-metric-label {
            font-size: 0.75rem;
        }
        .section-header {
            font-size: 1.4rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# App title with PendemixAI branding
st.markdown("<h1 class='main-title'>🌍 PENDEMIXAI - COVID-19 GLOBAL VACCINATION TRACKER</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Advanced AI-powered analytics for global vaccination monitoring</p>", unsafe_allow_html=True)

# Load data with ALL countries
@st.cache_data
def load_all_countries_data():
    # List of ALL countries in the world (200+ countries)
    all_countries = [
        'AFGHANISTAN', 'ALBANIA', 'ALGERIA', 'ANDORRA', 'ANGOLA', 'ANTIGUA AND BARBUDA', 'ARGENTINA', 
        'ARMENIA', 'AUSTRALIA', 'AUSTRIA', 'AZERBAIJAN', 'BAHAMAS', 'BAHRAIN', 'BANGLADESH', 'BARBADOS', 
        'BELARUS', 'BELGIUM', 'BELIZE', 'BENIN', 'BHUTAN', 'BOLIVIA', 'BOSNIA AND HERZEGOVINA', 'BOTSWANA', 
        'BRAZIL', 'BRUNEI', 'BULGARIA', 'BURKINA FASO', 'BURUNDI', 'CABO VERDE', 'CAMBODIA', 'CAMEROON', 
        'CANADA', 'CENTRAL AFRICAN REPUBLIC', 'CHAD', 'CHILE', 'CHINA', 'COLOMBIA', 'COMOROS', 'CONGO', 
        'COSTA RICA', 'CROATIA', 'CUBA', 'CYPRUS', 'CZECH REPUBLIC', 'DEMOCRATIC REPUBLIC OF THE CONGO', 
        'DENMARK', 'DJIBOUTI', 'DOMINICA', 'DOMINICAN REPUBLIC', 'ECUADOR', 'EGYPT', 'EL SALVADOR', 
        'EQUATORIAL GUINEA', 'ERITREA', 'ESTONIA', 'ESWATINI', 'ETHIOPIA', 'FIJI', 'FINLAND', 'FRANCE', 
        'GABON', 'GAMBIA', 'GEORGIA', 'GERMANY', 'GHANA', 'GREECE', 'GRENADA', 'GUATEMALA', 'GUINEA', 
        'GUINEA-BISSAU', 'GUYANA', 'HAITI', 'HONDURAS', 'HUNGARY', 'ICELAND', 'INDIA', 'INDONESIA', 
        'IRAN', 'IRAQ', 'IRELAND', 'ISRAEL', 'ITALY', 'JAMAICA', 'JAPAN', 'JORDAN', 'KAZAKHSTAN', 
        'KENYA', 'KIRIBATI', 'KUWAIT', 'KYRGYZSTAN', 'LAOS', 'LATVIA', 'LEBANON', 'LESOTHO', 'LIBERIA', 
        'LIBYA', 'LIECHTENSTEIN', 'LITHUANIA', 'LUXEMBOURG', 'MADAGASCAR', 'MALAWI', 'MALAYSIA', 
        'MALDIVES', 'MALI', 'MALTA', 'MARSHALL ISLANDS', 'MAURITANIA', 'MAURITIUS', 'MEXICO', 
        'MICRONESIA', 'MOLDOVA', 'MONACO', 'MONGOLIA', 'MONTENEGRO', 'MOROCCO', 'MOZAMBIQUE', 'MYANMAR', 
        'NAMIBIA', 'NAURU', 'NEPAL', 'NETHERLANDS', 'NEW ZEALAND', 'NICARAGUA', 'NIGER', 'NIGERIA', 
        'NORTH KOREA', 'NORTH MACEDONIA', 'NORWAY', 'OMAN', 'PAKISTAN', 'PALAU', 'PALESTINE', 'PANAMA', 
        'PAPUA NEW GUINEA', 'PARAGUAY', 'PERU', 'PHILIPPINES', 'POLAND', 'PORTUGAL', 'QATAR', 'ROMANIA', 
        'RUSSIA', 'RWANDA', 'SAINT KITTS AND NEVIS', 'SAINT LUCIA', 'SAINT VINCENT AND THE GRENADINES', 
        'SAMOA', 'SAN MARINO', 'SAO TOME AND PRINCIPE', 'SAUDI ARABIA', 'SENEGAL', 'SERBIA', 'SEYCHELLES', 
        'SIERRA LEONE', 'SINGAPORE', 'SLOVAKIA', 'SLOVENIA', 'SOLOMON ISLANDS', 'SOMALIA', 'SOUTH AFRICA', 
        'SOUTH KOREA', 'SOUTH SUDAN', 'SPAIN', 'SRI LANKA', 'SUDAN', 'SURINAME', 'SWEDEN', 'SWITZERLAND', 
        'SYRIA', 'TAIWAN', 'TAJIKISTAN', 'TANZANIA', 'THAILAND', 'TIMOR-LESTE', 'TOGO', 'TONGA', 
        'TRINIDAD AND TOBAGO', 'TUNISIA', 'TURKEY', 'TURKMENISTAN', 'TUVALU', 'UGANDA', 'UKRAINE', 
        'UNITED ARAB EMIRATES', 'UNITED KINGDOM', 'UNITED STATES', 'URUGUAY', 'UZBEKISTAN', 'VANUATU', 
        'VATICAN CITY', 'VENEZUELA', 'VIETNAM', 'YEMEN', 'ZAMBIA', 'ZIMBABWE'
    ]
    
    dates = pd.date_range('2021-01-01', '2023-12-31', freq='D')
    
    # Country population data (approximate in millions)
    country_population = {
        'CHINA': 1444, 'INDIA': 1408, 'UNITED STATES': 331, 'INDONESIA': 273, 'PAKISTAN': 225,
        'BRAZIL': 214, 'NIGERIA': 211, 'BANGLADESH': 166, 'RUSSIA': 146, 'MEXICO': 129,
        'JAPAN': 126, 'ETHIOPIA': 117, 'PHILIPPINES': 111, 'EGYPT': 102, 'VIETNAM': 97,
        'DEMOCRATIC REPUBLIC OF THE CONGO': 90, 'TURKEY': 84, 'IRAN': 84, 'GERMANY': 83, 'THAILAND': 70,
        'UNITED KINGDOM': 68, 'FRANCE': 65, 'ITALY': 60, 'SOUTH AFRICA': 60, 'TANZANIA': 60,
        'MYANMAR': 54, 'KENYA': 54, 'SOUTH KOREA': 51, 'COLOMBIA': 51, 'SPAIN': 47,
        'ARGENTINA': 45, 'UGANDA': 45, 'ALGERIA': 44, 'SUDAN': 44, 'UKRAINE': 44,
        'IRAQ': 41, 'AFGHANISTAN': 39, 'POLAND': 38, 'CANADA': 38, 'MOROCCO': 37,
        'SAUDI ARABIA': 35, 'UZBEKISTAN': 34, 'PERU': 33, 'MALAYSIA': 33, 'ANGOLA': 33,
        'MOZAMBIQUE': 31, 'GHANA': 31, 'YEMEN': 30, 'NEPAL': 29, 'VENEZUELA': 28,
        'MADAGASCAR': 28, 'CAMEROON': 27, 'CÔTE D\'IVOIRE': 27, 'NORTH KOREA': 26,
        'AUSTRALIA': 26, 'NIGER': 25, 'SRI LANKA': 21, 'BURKINA FASO': 21, 'MALI': 20,
        'ROMANIA': 19, 'CHILE': 19, 'MALAWI': 19, 'KAZAKHSTAN': 19, 'ZAMBIA': 19,
        'GUATEMALA': 18, 'ECUADOR': 18, 'NETHERLANDS': 17, 'SYRIA': 17, 'CAMBODIA': 17,
        'SENEGAL': 17, 'CHAD': 16, 'SOMALIA': 16, 'ZIMBABWE': 15, 'GUINEA': 13,
        'RWANDA': 13, 'BENIN': 12, 'BURUNDI': 12, 'TUNISIA': 12, 'BOLIVIA': 12,
        'BELGIUM': 12, 'HAITI': 11, 'JORDAN': 10, 'DOMINICAN REPUBLIC': 11,
        'CUBA': 11, 'SOUTH SUDAN': 11, 'SWEDEN': 10, 'CZECH REPUBLIC': 11,
        'GREECE': 10, 'PORTUGAL': 10, 'AZERBAIJAN': 10, 'HUNGARY': 10,
        'UNITED ARAB EMIRATES': 10, 'BELARUS': 9, 'ISRAEL': 9, 'TAJIKISTAN': 10,
        'AUSTRIA': 9, 'SWITZERLAND': 9, 'PAPUA NEW GUINEA': 9, 'SERBIA': 9,
        'PARAGUAY': 7, 'LAOS': 7, 'LIBYA': 7, 'BULGARIA': 7, 'LEBANON': 7,
        'NICARAGUA': 7, 'KYRGYZSTAN': 7, 'EL SALVADOR': 7, 'TURKMENISTAN': 6,
        'SINGAPORE': 6, 'DENMARK': 6, 'FINLAND': 6, 'SLOVAKIA': 5, 'NORWAY': 5,
        'CONGO': 6, 'COSTA RICA': 5, 'PALESTINE': 5, 'OMAN': 5, 'LIBERIA': 5,
        'IRELAND': 5, 'NEW ZEALAND': 5, 'CENTRAL AFRICAN REPUBLIC': 5,
        'MAURITANIA': 5, 'PANAMA': 4, 'KUWAIT': 4, 'CROATIA': 4, 'GEORGIA': 4,
        'MOLDOVA': 4, 'ERITREA': 4, 'URUGUAY': 3, 'BOSNIA AND HERZEGOVINA': 3,
        'MONGOLIA': 3, 'ARMENIA': 3, 'JAMAICA': 3, 'QATAR': 3, 'ALBANIA': 3,
        'LITHUANIA': 3, 'NAMIBIA': 3, 'GAMBIA': 2, 'BOTSWANA': 2, 'GABON': 2,
        'LESOTHO': 2, 'SLOVENIA': 2, 'GUINEA-BISSAU': 2, 'LATVIA': 2,
        'BAHRAIN': 2, 'NORTH MACEDONIA': 2, 'TRINIDAD AND TOBAGO': 1,
        'ESTONIA': 1, 'MAURITIUS': 1, 'CYPRUS': 1, 'ESWATINI': 1, 'DJIBOUTI': 1,
        'FIJI': 1, 'COMOROS': 1, 'GUYANA': 1, 'BHUTAN': 1, 'SOLOMON ISLANDS': 1,
        'MONTENEGRO': 1, 'LUXEMBOURG': 1, 'SURINAME': 1, 'CABO VERDE': 1,
        'MICRONESIA': 0.1, 'MALTA': 0.5, 'BRUNEI': 0.4, 'BELIZE': 0.4,
        'BAHAMAS': 0.4, 'ICELAND': 0.4, 'VANUATU': 0.3, 'BARBADOS': 0.3,
        'SAO TOME AND PRINCIPE': 0.2, 'SAMOA': 0.2, 'SAINT LUCIA': 0.2,
        'KIRIBATI': 0.1, 'GRENADA': 0.1, 'TONGA': 0.1, 'SEYCHELLES': 0.1,
        'ANTIGUA AND BARBUDA': 0.1, 'ANDORRA': 0.1, 'DOMINICA': 0.1,
        'MARSHALL ISLANDS': 0.1, 'SAINT KITTS AND NEVIS': 0.1,
        'MONACO': 0.04, 'LIECHTENSTEIN': 0.04, 'SAN MARINO': 0.03,
        'PALAU': 0.02, 'NAURU': 0.01, 'TUVALU': 0.01, 'VATICAN CITY': 0.001
    }
    
    data = []
    
    for country in all_countries:
        # Get population (in millions)
        population_millions = country_population.get(country, np.random.uniform(0.1, 50))
        
        # Calculate realistic vaccination numbers
        base_coverage = np.random.uniform(0.1, 0.8)  # 10% to 80% coverage
        
        for i, date in enumerate(dates[:180]):  # 180 days per country
            # Time-based progression
            progress_factor = min(1.0, i / 180 * np.random.uniform(0.5, 2.0))
            
            # Calculate vaccinations
            total_vax = int(population_millions * 1_000_000 * base_coverage * progress_factor)
            daily_vax = int(total_vax * np.random.uniform(0.001, 0.01))
            people_vax = int(total_vax * np.random.uniform(0.7, 0.95))
            fully_vax = int(total_vax * np.random.uniform(0.5, 0.85))
            
            # Add some randomness
            total_vax += np.random.randint(-100000, 100000)
            daily_vax = max(0, daily_vax + np.random.randint(-5000, 5000))
            
            data.append({
                'country': country,
                'date': date,
                'total_vaccinations': max(0, total_vax),
                'daily_vaccinations': max(0, daily_vax),
                'people_vaccinated': max(0, people_vax),
                'people_fully_vaccinated': max(0, fully_vax),
                'population_millions': population_millions,
                'vaccination_rate': min(100, (total_vax / (population_millions * 1_000_000)) * 100) if population_millions > 0 else 0
            })
    
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    return df

# Load the data
df = load_all_countries_data()

# SIDEBAR
st.sidebar.header("🎛️ DASHBOARD CONTROLS")

# Show total countries count
total_countries = df['country'].nunique()
st.sidebar.markdown(f"**📊 TOTAL COUNTRIES:** <span class='country-count'>{total_countries}</span>", unsafe_allow_html=True)

# Country selection with search
all_countries = sorted(df['country'].unique())
selected_country = st.sidebar.selectbox(
    "SELECT A COUNTRY:",
    all_countries,
    index=all_countries.index('INDIA') if 'INDIA' in all_countries else 0,
    help="TYPE TO SEARCH THROUGH ALL COUNTRIES"
)

# Region filter (group countries by region)
regions = {
    'ASIA': ['INDIA', 'CHINA', 'JAPAN', 'SOUTH KOREA', 'INDONESIA', 'PAKISTAN', 'BANGLADESH', 'PHILIPPINES', 'VIETNAM', 'THAILAND'],
    'EUROPE': ['UNITED KINGDOM', 'GERMANY', 'FRANCE', 'ITALY', 'SPAIN', 'RUSSIA', 'UKRAINE', 'POLAND', 'NETHERLANDS', 'SWEDEN'],
    'NORTH AMERICA': ['UNITED STATES', 'CANADA', 'MEXICO', 'CUBA', 'DOMINICAN REPUBLIC', 'HAITI'],
    'SOUTH AMERICA': ['BRAZIL', 'ARGENTINA', 'COLOMBIA', 'PERU', 'CHILE', 'VENEZUELA'],
    'AFRICA': ['NIGERIA', 'ETHIOPIA', 'EGYPT', 'SOUTH AFRICA', 'KENYA', 'TANZANIA', 'ALGERIA', 'SUDAN'],
    'OCEANIA': ['AUSTRALIA', 'NEW ZEALAND', 'FIJI', 'PAPUA NEW GUINEA']
}

selected_region = st.sidebar.selectbox(
    "FILTER BY REGION (OPTIONAL):",
    ['ALL REGIONS'] + list(regions.keys())
)

# Chart settings
st.sidebar.markdown("---")
st.sidebar.subheader("📈 CHART SETTINGS")
num_top_countries = st.sidebar.slider("NUMBER OF TOP COUNTRIES TO SHOW:", 5, 50, 20)

# MAIN DASHBOARD
# Filter data based on selections
if selected_region != 'ALL REGIONS':
    region_countries = regions[selected_region]
    df_filtered = df[df['country'].isin(region_countries)]
    st.info(f"SHOWING DATA FOR {selected_region} REGION ({len(region_countries)} COUNTRIES)")
else:
    df_filtered = df

# Get data for selected country (all data, no date filtering)
country_data = df_filtered[df_filtered['country'] == selected_country]

# ================= GLOBAL METRICS SECTION =================
st.markdown("<h2 class='section-header'>📊 GLOBAL VACCINATION OVERVIEW</h2>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_countries_val = df['country'].nunique()
    st.markdown(f"""
    <div class='custom-metric-card'>
        <div class='custom-metric-value'>{total_countries_val}</div>
        <div class='custom-metric-label'>TOTAL COUNTRIES</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    global_total = df.groupby('country')['total_vaccinations'].max().sum()
    formatted_total = f"{global_total:,.0f}"
    st.markdown(f"""
    <div class='custom-metric-card'>
        <div class='custom-metric-value'>{formatted_total}</div>
        <div class='custom-metric-label'>GLOBAL VACCINATIONS</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    avg_rate = df.groupby('country')['vaccination_rate'].max().mean()
    st.markdown(f"""
    <div class='custom-metric-card'>
        <div class='custom-metric-value'>{avg_rate:.1f}%</div>
        <div class='custom-metric-label'>AVG. VACCINATION RATE</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    days_covered = (df['date'].max() - df['date'].min()).days
    st.markdown(f"""
    <div class='custom-metric-card'>
        <div class='custom-metric-value'>{days_covered}</div>
        <div class='custom-metric-label'>DAYS COVERED</div>
    </div>
    """, unsafe_allow_html=True)

# ================= COUNTRY METRICS SECTION =================
st.markdown(f"<h2 class='section-header'>📍 DATA FOR {selected_country}</h2>", unsafe_allow_html=True)

if not country_data.empty:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_vax = country_data['total_vaccinations'].max()
        formatted_total_vax = f"{total_vax:,.0f}"
        st.markdown(f"""
        <div class='custom-metric-card'>
            <div class='custom-metric-value'>{formatted_total_vax}</div>
            <div class='custom-metric-label'>TOTAL VACCINATIONS</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        daily_avg = country_data['daily_vaccinations'].mean()
        formatted_daily_avg = f"{daily_avg:,.0f}"
        st.markdown(f"""
        <div class='custom-metric-card'>
            <div class='custom-metric-value'>{formatted_daily_avg}</div>
            <div class='custom-metric-label'>DAILY AVERAGE</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        people_vax = country_data['people_vaccinated'].max()
        formatted_people_vax = f"{people_vax:,.0f}"
        st.markdown(f"""
        <div class='custom-metric-card'>
            <div class='custom-metric-value'>{formatted_people_vax}</div>
            <div class='custom-metric-label'>PEOPLE VACCINATED</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        vax_rate = country_data['vaccination_rate'].max()
        st.markdown(f"""
        <div class='custom-metric-card'>
            <div class='custom-metric-value'>{vax_rate:.1f}%</div>
            <div class='custom-metric-label'>VACCINATION RATE</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.error(f"No data available for {selected_country}")

# ================= VISUALIZATION 1: Country Trend =================
st.markdown("<h2 class='section-header'>📈 COUNTRY VACCINATION TREND</h2>", unsafe_allow_html=True)

if not country_data.empty:
    tab1, tab2 = st.tabs(["TOTAL VACCINATIONS", "DAILY PROGRESS"])
    
    with tab1:
        fig1 = px.line(
            country_data,
            x='date',
            y='total_vaccinations',
            title=f'{selected_country}: TOTAL VACCINATIONS OVER TIME',
            labels={'total_vaccinations': 'TOTAL VACCINATIONS', 'date': 'DATE'},
            template='plotly_white',
            line_shape='spline'
        )
        fig1.update_traces(line=dict(width=3))
        fig1.update_xaxes(rangeslider_visible=True)
        st.plotly_chart(fig1, use_container_width=True)
    
    with tab2:
        fig2 = px.area(
            country_data.tail(90),
            x='date',
            y='daily_vaccinations',
            title=f'{selected_country}: DAILY VACCINATIONS (LAST 90 DAYS)',
            labels={'daily_vaccinations': 'DAILY VACCINATIONS', 'date': 'DATE'},
            template='plotly_white'
        )
        st.plotly_chart(fig2, use_container_width=True)

# ================= VISUALIZATION 2: Global Comparison =================
st.markdown("<h2 class='section-header'>🌐 GLOBAL COMPARISON</h2>", unsafe_allow_html=True)

# Get latest data for each country
latest_data = df.groupby('country').last().reset_index()

# Top countries visualization
col1, col2 = st.columns(2)

with col1:
    # Top countries by total vaccinations
    top_countries = latest_data.nlargest(num_top_countries, 'total_vaccinations')
    
    fig3 = px.bar(
        top_countries,
        x='total_vaccinations',
        y='country',
        orientation='h',
        title=f'TOP {num_top_countries} COUNTRIES BY TOTAL VACCINATIONS',
        labels={'total_vaccinations': 'TOTAL VACCINATIONS', 'country': 'COUNTRY'},
        color='total_vaccinations',
        color_continuous_scale='Viridis',
        hover_data=['vaccination_rate', 'population_millions']
    )
    fig3.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    # Top countries by vaccination rate
    top_rate = latest_data.nlargest(num_top_countries, 'vaccination_rate')
    
    fig4 = px.bar(
        top_rate,
        x='vaccination_rate',
        y='country',
        orientation='h',
        title=f'TOP {num_top_countries} COUNTRIES BY VACCINATION RATE',
        labels={'vaccination_rate': 'VACCINATION RATE (%)', 'country': 'COUNTRY'},
        color='vaccination_rate',
        color_continuous_scale='Plasma',
        hover_data=['total_vaccinations', 'population_millions']
    )
    fig4.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig4, use_container_width=True)

# ================= VISUALIZATION 3: Interactive World Map =================
st.markdown("<h2 class='section-header'>🗺️ GLOBAL VACCINATION MAP</h2>", unsafe_allow_html=True)

# Get latest data for EACH COUNTRY
map_country_data = df.groupby('country').last().reset_index()

# Convert country names to proper case for Plotly map recognition
def convert_country_name(country):
    """Convert uppercase country names to Plotly-recognized format"""
    special_cases = {
        'UNITED STATES': 'United States',
        'UNITED KINGDOM': 'United Kingdom',
        'SOUTH KOREA': 'South Korea',
        'NORTH KOREA': 'North Korea',
        'SOUTH AFRICA': 'South Africa',
        'SAUDI ARABIA': 'Saudi Arabia',
        'NEW ZEALAND': 'New Zealand',
        'PAPUA NEW GUINEA': 'Papua New Guinea',
        'UNITED ARAB EMIRATES': 'United Arab Emirates',
        'DOMINICAN REPUBLIC': 'Dominican Republic',
        'CZECH REPUBLIC': 'Czech Republic',
        'BOSNIA AND HERZEGOVINA': 'Bosnia and Herzegovina',
        'TRINIDAD AND TOBAGO': 'Trinidad and Tobago',
        'ANTIGUA AND BARBUDA': 'Antigua and Barbuda',
        'SAINT VINCENT AND THE GRENADINES': 'Saint Vincent and the Grenadines',
        'SAINT KITTS AND NEVIS': 'Saint Kitts and Nevis',
        'SAO TOME AND PRINCIPE': 'Sao Tome and Principe',
        'TIMOR-LESTE': 'Timor-Leste',
        'DEMOCRATIC REPUBLIC OF THE CONGO': 'Democratic Republic of the Congo',
        'CENTRAL AFRICAN REPUBLIC': 'Central African Republic'
    }
    
    if country in special_cases:
        return special_cases[country]
    
    return country.title()

map_data = map_country_data.copy()
map_data['country_plotly'] = map_data['country'].apply(convert_country_name)

try:
    fig5 = px.choropleth(
        map_data,
        locations="country_plotly",
        locationmode="country names",
        color="vaccination_rate",
        hover_name="country",
        hover_data={
            'country_plotly': False,
            'total_vaccinations': ':,.0f',
            'people_vaccinated': ':,.0f',
            'vaccination_rate': ':.1f%',
            'daily_vaccinations': ':,.0f'
        },
        title="🌍 GLOBAL VACCINATION COVERAGE",
        color_continuous_scale=px.colors.sequential.Plasma,
        range_color=[0, map_data["vaccination_rate"].max() * 1.1],
        labels={'vaccination_rate': 'VACCINATION RATE (%)'}
    )
    
    fig5.update_layout(
        height=600,
        geo=dict(
            showframe=False,
            showcoastlines=True,
            showcountries=True,
            countrycolor="lightgray",
            coastlinecolor="gray",
            landcolor="white",
            projection_type='natural earth',
            bgcolor='rgba(240,248,255,0.1)'
        ),
        coloraxis_colorbar=dict(
            title="VACCINATION<br>RATE (%)",
            thickness=20,
            len=0.75,
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02
        )
    )
    
    fig5.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>" +
                      "Total Vaccinations: %{customdata[0]:,}<br>" +
                      "People Vaccinated: %{customdata[1]:,}<br>" +
                      "Vaccination Rate: %{customdata[2]:.1f}%<br>" +
                      "Daily Vaccinations: %{customdata[3]:,}<br>" +
                      "<extra></extra>"
    )
    
    st.plotly_chart(fig5, use_container_width=True)
    st.success(f"✅ World map showing {len(map_data)} countries")
    
except Exception as e:
    st.error(f"❌ Map error: {str(e)}")
    
    # Fallback visualization
    fig5_fallback = px.scatter(
        map_country_data,
        x='country',
        y='vaccination_rate',
        size='total_vaccinations',
        color='vaccination_rate',
        title='VACCINATION RATES BY COUNTRY',
        labels={'vaccination_rate': 'Vaccination Rate (%)', 'country': 'Country'},
        hover_data=['total_vaccinations', 'people_vaccinated'],
        color_continuous_scale='Plasma'
    )
    
    fig5_fallback.update_layout(
        height=500,
        xaxis_tickangle=45,
        xaxis_title="Country",
        yaxis_title="Vaccination Rate (%)"
    )
    st.plotly_chart(fig5_fallback, use_container_width=True)

# ================= VISUALIZATION 4: Country Comparison =================
st.markdown("<h2 class='section-header'>🔍 COMPARE COUNTRIES</h2>", unsafe_allow_html=True)

compare_countries = st.multiselect(
    "SELECT COUNTRIES TO COMPARE:",
    all_countries,
    default=[selected_country, 'UNITED STATES', 'UNITED KINGDOM', 'GERMANY'] if selected_country in all_countries else all_countries[:4],
    max_selections=10
)

if compare_countries:
    compare_data = df[df['country'].isin(compare_countries)].groupby(['country', 'date']).last().reset_index()
    
    fig6 = px.line(
        compare_data,
        x='date',
        y='total_vaccinations',
        color='country',
        title='VACCINATION PROGRESS COMPARISON',
        labels={'total_vaccinations': 'TOTAL VACCINATIONS', 'date': 'DATE', 'country': 'COUNTRY'},
        template='plotly_white',
        line_dash='country'
    )
    
    fig6.update_layout(hovermode='x unified')
    st.plotly_chart(fig6, use_container_width=True)

# ================= DATA EXPLORER =================
with st.expander("📋 EXPLORE ALL COUNTRY DATA", expanded=False):
    st.dataframe(
        latest_data.sort_values('total_vaccinations', ascending=False),
        use_container_width=True,
        height=400,
        column_config={
            'country': 'COUNTRY',
            'total_vaccinations': st.column_config.NumberColumn('TOTAL VACCINATIONS', format='%d'),
            'vaccination_rate': st.column_config.ProgressColumn('VACCINATION RATE', format='%.1f%%', min_value=0, max_value=100),
            'population_millions': 'POPULATION (MILLIONS)'
        }
    )

# ================= DOWNLOAD SECTION =================
st.sidebar.markdown("---")
st.sidebar.header("📥 DOWNLOAD DATA")

# Download options
download_option = st.sidebar.radio(
    "SELECT DATA TO DOWNLOAD:",
    ['CURRENT COUNTRY', 'ALL COUNTRIES', 'TOP 50 COUNTRIES']
)

if download_option == 'CURRENT COUNTRY':
    download_data = country_data
    filename = f"PENDEMIXAI_VACCINATION_{selected_country}.csv"
elif download_option == 'ALL COUNTRIES':
    download_data = df
    filename = "PENDEMIXAI_VACCINATION_ALL_COUNTRIES.csv"
else:
    download_data = latest_data.nlargest(50, 'total_vaccinations')
    filename = "PENDEMIXAI_VACCINATION_TOP_50.csv"

csv_data = download_data.to_csv(index=False)

st.sidebar.download_button(
    label=f"📥 DOWNLOAD {download_option} DATA",
    data=csv_data,
    file_name=filename,
    mime="text/csv",
    use_container_width=True
)

# ================= INFO SECTION =================
st.sidebar.markdown("---")
st.sidebar.info(f"""
**PENDEMIXAI DASHBOARD FEATURES:**
- ✅ **{total_countries} COUNTRIES** INCLUDED
- ✅ INTERACTIVE CHARTS WITH HOVER DETAILS
- ✅ COMPARE MULTIPLE COUNTRIES
- ✅ FILTER BY REGION
- ✅ DOWNLOAD DATA IN CSV FORMAT
- ✅ SIMULATED REALISTIC VACCINATION DATA
""")

# ================= COPYRIGHT SECTION =================
st.markdown("""
<div style='text-align: center; color: #9CA3AF; font-size: 0.9rem; padding: 15px;'>
    <hr style='border: none; height: 1px; background: #E5E7EB; margin: 15px 0;'>
    © 2026 PendemixAI. All rights reserved. | 
    This dashboard is created for educational and analytical purposes.
</div>
""", unsafe_allow_html=True)