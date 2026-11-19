# Import library
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Konfigurasi halaman
st.set_page_config(
    page_title="Titanic Survival Analytics",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Menentukan warna dashboard
BG = "#101817"
CARD = "#192622"
GREEN = "#34D399"
ORANGE = "#FB923C"
BLUE = "#38BDF8"
PURPLE = "#A78BFA"
TEXT = "#F1F5F2"

# Mengatur tampilan dashboard
st.markdown("""
<style>

/* Background animated gradient */
.stApp {
    background: linear-gradient(
        -45deg, #061C16, #0B4935,
        #087F68, #123F48, #064E3B
    );
    background-size: 400% 400%;
    animation: auroraMove 18s ease infinite;
    color: #F1F5F2;
}

@keyframes auroraMove {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

/* Header dan area utama */
[data-testid="stHeader"] {
    background: transparent !important;
}

.block-container {
    padding-top: 2.5rem;
    padding-bottom: 2rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg, #15513B, #103B2D, #071713
    ) !important;
    border-right: 1px solid #34D399;
}

/* Warna teks */
.stApp, .stApp p, .stApp label,
.stApp h1, .stApp h2, .stApp h3 {
    color: #F1F5F2;
}

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {
    color: #E2EDE7 !important;
}

/* Filter dan input */
[data-baseweb="select"] > div,
.stApp input,
.stApp textarea {
    background: #19372B !important;
    color: #FFFFFF !important;
    border-color: #426052 !important;
}

/* Chip multiselect hijau */
[data-baseweb="tag"] {
    background: linear-gradient(
        135deg, #16845B, #086B49
    ) !important;
    border: 1px solid #34D399 !important;
    color: #FFFFFF !important;
}

[data-baseweb="tag"] span {
    color: #FFFFFF !important;
}

/* Warna slider */
.stSlider {
    accent-color: #34D399 !important;
}

/* Judul dashboard */
.main-title {
    font-size: 38px;
    font-weight: 850;
    color: #FFFFFF;
}

.subtitle {
    font-size: 14px;
    color: #B5D8C8;
    margin: 8px 0 25px;
}

.section-title {
    font-size: 19px;
    font-weight: 750;
    color: #FFFFFF;
    margin: 28px 0 14px;
}

/* KPI Card animated gradient */
.kpi-card {
    background: linear-gradient(
        135deg, #236B4D, #18563E, #103B2D
    );
    background-size: 200% 200%;
    animation: cardGlow 8s ease infinite;
    border: 1px solid #34D39980;
    border-radius: 18px;
    padding: 22px;
    min-height: 135px;
    box-shadow: 0 8px 25px #00000040;
    transition: 0.3s;
}

@keyframes cardGlow {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

.kpi-card:hover {
    transform: translateY(-5px);
    border-color: #6EE7B7;
}

.kpi-label {
    color: #D1FAE5;
    font-size: 12px;
    font-weight: 600;
}

.kpi-value {
    color: #6EE7B7;
    font-size: 29px;
    font-weight: 800;
    margin-top: 12px;
}

.kpi-description {
    color: #B5D8C8;
    font-size: 11px;
    margin-top: 7px;
}

/* Grafik */
div[data-testid="stPlotlyChart"] {
    background: #192C25;
    border: 1px solid #355448;
    border-radius: 15px;
    padding: 8px;
}

/* Tabel */
div[data-testid="stDataFrame"] {
    background: #192C25 !important;
    border: 1px solid #355448;
    border-radius: 12px;
}

/* Tombol */
.stDownloadButton button {
    background: linear-gradient(
        135deg, #34D399, #059669
    ) !important;
    color: #071B13 !important;
    border: none;
    border-radius: 9px;
    font-weight: 700;
}

/* Garis dan scrollbar */
hr {
    border-color: #34D39955;
}

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #16845B;
    border-radius: 10px;
}

@media (prefers-reduced-motion: reduce) {
    .stApp, .kpi-card {
        animation: none !important;
    }
}

</style>
""", unsafe_allow_html=True)

# Membaca dataset
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv"
    return pd.read_csv(url)

try:
    df = load_data()
except Exception as e:
    st.error("Dataset gagal dimuat. Periksa koneksi internet.")
    st.code(str(e))
    st.stop()

# Membuat sidebar dan filter
st.sidebar.markdown("""
<h2 style="color:#34D399;">🚢 TITANIC ANALYTICS</h2>
<p style="color:#9BAFA5;">Passenger Data Exploration</p>
<hr>
""", unsafe_allow_html=True)

st.sidebar.subheader("FILTER DATA")

sex_options = ["Semua"] + sorted(df["sex"].dropna().unique().tolist())

selected_sex = st.sidebar.selectbox(
    "Jenis Kelamin",
    sex_options
)

class_options = sorted(df["pclass"].dropna().unique().tolist())

selected_class = st.sidebar.multiselect(
    "Kelas Penumpang",
    options=class_options,
    default=class_options,
    format_func=lambda x: f"Kelas {x}"
)

selected_survival = st.sidebar.selectbox(
    "Status Keselamatan",
    ["Semua", "Selamat", "Tidak Selamat"]
)

embarked_options = ["Semua"] + sorted(
    df["embarked"].dropna().unique().tolist()
)

selected_embarked = st.sidebar.selectbox(
    "Pelabuhan Keberangkatan",
    embarked_options
)

age_range = st.sidebar.slider(
    "Rentang Usia",
    min_value=0,
    max_value=int(df["age"].max()),
    value=(0, int(df["age"].max()))
)

st.sidebar.markdown("---")
st.sidebar.caption("Praktikum 9 | Pengantar Sains Data")
st.sidebar.caption("Dataset: Titanic")

# Melakukan filter dataset
data = df.copy()

if selected_sex != "Semua":
    data = data[data["sex"] == selected_sex]

if selected_class:
    data = data[data["pclass"].isin(selected_class)]
else:
    data = data.iloc[0:0]

if selected_survival == "Selamat":
    data = data[data["survived"] == 1]
elif selected_survival == "Tidak Selamat":
    data = data[data["survived"] == 0]

if selected_embarked != "Semua":
    data = data[data["embarked"] == selected_embarked]

data = data[data["age"].between(age_range[0], age_range[1])]

# Membuat header dashboard
st.markdown("""
<div class="main-title">
TITANIC SURVIVAL ANALYTICS
</div>
<div class="subtitle">
Exploring Passenger Survival Patterns Through Statistical Visualization
</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.caption(f"DATA OVERVIEW | {len(data):,} passenger records displayed")

# Menghitung nilai KPI
total_passengers = len(data)
total_survived = int(data["survived"].sum())
total_not_survived = total_passengers - total_survived

survival_rate = (
    total_survived / total_passengers * 100
    if total_passengers > 0 else 0
)

average_age = data["age"].mean()
average_fare = data["fare"].mean()

# Menampilkan KPI Card
st.markdown(
    '<div class="section-title">OVERVIEW STATISTICS</div>',
    unsafe_allow_html=True
)

kpis = [
    ("TOTAL PASSENGERS", f"{total_passengers:,}", "Jumlah penumpang terpilih"),
    ("SURVIVAL RATE", f"{survival_rate:.2f}%", "Persentase penumpang selamat"),
    ("AVERAGE AGE", f"{average_age:.1f}" if pd.notna(average_age) else "-", "Rata-rata usia penumpang"),
    ("AVERAGE FARE", f"${average_fare:.2f}" if pd.notna(average_fare) else "-", "Rata-rata harga tiket")
]

cols = st.columns(4)

for col, item in zip(cols, kpis):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{item[0]}</div>
            <div class="kpi-value">{item[1]}</div>
            <div class="kpi-description">{item[2]}</div>
        </div>
        """, unsafe_allow_html=True)

# Mengatur tampilan grafik
def chart_style(fig, height=380):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        font=dict(family="Arial", color=TEXT),
        title_font=dict(size=16, color=TEXT),
        height=height,
        margin=dict(l=25, r=25, t=65, b=35)
    )
    return fig

# Membuat boxplot
st.markdown(
    '<div class="section-title">01 — DISTRIBUTION ANALYSIS</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    fig_box = px.box(
        data,
        x="pclass",
        y="fare",
        color="pclass",
        color_discrete_sequence=[GREEN, BLUE, ORANGE],
        title="Ticket Fare Distribution by Passenger Class",
        labels={
            "pclass": "Passenger Class",
            "fare": "Ticket Fare"
        }
    )

    fig_box.update_layout(
        xaxis=dict(
            tickmode="array",
            tickvals=[1, 2, 3],
            ticktext=["Class 1", "Class 2", "Class 3"]
        ),
        showlegend=False
    )

    st.plotly_chart(
        chart_style(fig_box),
        use_container_width=True
    )

# Membuat histogram
with col2:
    fig_hist = px.histogram(
        data,
        x="age",
        nbins=25,
        color_discrete_sequence=[GREEN],
        title="Passenger Age Distribution",
        labels={
            "age": "Passenger Age",
            "count": "Frequency"
        }
    )

    fig_hist.update_traces(
        marker_line_color=BG,
        marker_line_width=1
    )

    st.plotly_chart(
        chart_style(fig_hist),
        use_container_width=True
    )

# Membuat barplot
st.markdown(
    '<div class="section-title">02 — PASSENGER COMPARISON</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns([1.3, 1])

with col1:
    gender_data = (
        data.groupby(["sex", "survived"])
        .size()
        .reset_index(name="Jumlah")
    )

    gender_data["Status"] = gender_data["survived"].map({
        1: "Selamat",
        0: "Tidak Selamat"
    })

    fig_bar = px.bar(
        gender_data,
        x="sex",
        y="Jumlah",
        color="Status",
        barmode="group",
        text="Jumlah",
        color_discrete_map={
            "Selamat": GREEN,
            "Tidak Selamat": ORANGE
        },
        title="Passenger Survival by Gender",
        labels={
            "sex": "Gender",
            "Jumlah": "Number of Passengers"
        }
    )

    fig_bar.update_traces(textposition="outside")

    st.plotly_chart(
        chart_style(fig_bar),
        use_container_width=True
    )

# Membuat pie chart
with col2:
    pie_data = pd.DataFrame({
        "Status": ["Selamat", "Tidak Selamat"],
        "Jumlah": [total_survived, total_not_survived]
    })

    fig_pie = px.pie(
        pie_data,
        names="Status",
        values="Jumlah",
        hole=0.58,
        color="Status",
        color_discrete_map={
            "Selamat": GREEN,
            "Tidak Selamat": ORANGE
        },
        title="Passenger Survival Proportion"
    )

    fig_pie.update_traces(
        textinfo="percent+label",
        textposition="inside",
        marker=dict(line=dict(color=BG, width=3))
    )

    st.plotly_chart(
        chart_style(fig_pie),
        use_container_width=True
    )

# Membuat heatmap korelasi
st.markdown(
    '<div class="section-title">03 — CORRELATION ANALYSIS</div>',
    unsafe_allow_html=True
)

numeric_data = data.select_dtypes(include=np.number)

if len(numeric_data) > 0:
    correlation = numeric_data.corr()

    fig_heatmap = px.imshow(
        correlation,
        text_auto=".2f",
        color_continuous_scale="RdYlGn",
        zmin=-1,
        zmax=1,
        aspect="auto",
        title="Correlation Matrix of Numerical Variables"
    )

    st.plotly_chart(
        chart_style(fig_heatmap, 480),
        use_container_width=True
    )
else:
    st.warning("Tidak terdapat variabel numerik untuk heatmap.")

# Menampilkan dataset
st.markdown(
    '<div class="section-title">04 — DATA EXPLORER</div>',
    unsafe_allow_html=True
)

st.write("Explore, search, and download the filtered Titanic dataset.")

search = st.text_input(
    "SEARCH DATASET",
    placeholder="Cari berdasarkan kata kunci..."
)

display_data = data.copy()

if search:
    mask = display_data.astype(str).apply(
        lambda col: col.str.contains(
            search,
            case=False,
            na=False
        )
    ).any(axis=1)

    display_data = display_data[mask]

st.caption(
    f"Menampilkan {len(display_data):,} dari {len(data):,} data."
)

st.dataframe(
    display_data,
    use_container_width=True,
    height=380,
    hide_index=True
)

# Mengunduh dataset
csv = display_data.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ DOWNLOAD DATASET CSV",
    data=csv,
    file_name="titanic_filtered.csv",
    mime="text/csv",
    use_container_width=True
)

# Footer dashboard
st.markdown("---")

st.markdown("""
<div style="text-align:center; padding:20px; color:#9BAFA5; font-size:12px;">
    <span style="color:#34D399; font-weight:bold;">
        TITANIC SURVIVAL ANALYTICS
    </span>
    <br><br>
    Statistical Data Exploration | Praktikum 9
    <br>
    Dataset Source: Seaborn Data Repository
</div>
""", unsafe_allow_html=True)