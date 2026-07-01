import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import datetime

# 1 PAGE CONFIGURATION 
st.set_page_config(
    page_title="AutoEngin - Electrical Equipment Dashboard" , 
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)



st.sidebar.markdown("###project credentials")
st.sidebar.markdown("**Developer:** Eng. Yaqeen jasim alqasimi")
st.sidebar.markdown("**Specialization:** Control Systems & Automation Engineer")
st.sidebar.markdown("**Business Identity:**AutoEngine Solutions")
st.sidebar.markdown("----")



# Custom CSS for clean layout
st.markdown("""
            <style>
            h1, h2, h3, h4, h5, h6, p, span{ font-family: 'Helvetica Neue' ,Helevtica, Arial, sans-serif; }
            div.stButon > button:first-child {background-color: #0066cc; color:white}
            </style>
            """
            , unsafe_allow_html=True)

# 2 HEADER SECTION
st.title("Electrical Equipment Smart Monitoring Dashboard ")
st.subheader ("Automated analysis of active/reactive power, voltage, and current readings")
st.markdown("---")


#3 SIDEBAR CONFIGURATION
st.sidebar.header("Control Panel & Filters")
selected_equipment = st.sidebar.selectbox(
"selected_equipment to Monitor:",
["Main Transformer A" , "Backup Generator B", "Main Distribution Board 1"])

data_range = st.sidebar.date_input(
    "Data View Range:",
    [datetime.date(2026,6,1), datetime.date(2026,6,29)]

)

st.sidebar.markdown("----")
st.sidebar.info("Notice: Power parameters and power factor metrics are auttomatically computed by the integrated script engine.")


# 4 SIMULTION DATA GENERATOR
@st.cache_data
def load_simulated_data():
    np.random.seed(42)
    dates = pd.date_range(start="2026-06-01", end="2026-06-29", freq="h")

    voltage = np.random.uniform(395, 405, len(dates)) #voltage around 400v
    current = np.random.uniform(50, 150, len(dates)) #current in ampereS

    #Calculate Active and Reactive Power based on real electrical principles
    active_power = (voltage*current*np.sqrt(3) * np.random.uniform(0.82, 0.88, len(dates))) / 1000 #KW
    reactive_power = active_power* np.tan(np.arccos(np.random.uniform(0.82, 0.88, len(dates)))) #KVAR

    df = pd.DataFrame({
        'Timestamp' : dates,
        'Voltage_V': voltage,
        'Current_A': current,
        'ActivePower_KW': active_power,
        'ReactivePower_KVAR': reactive_power
    })


    return df
df_data = load_simulated_data()

#5 Engineering Metrics & KPIs
avg_active = df_data['ActivePower_KW'].mean()
avg_reactive = df_data['ReactivePower_KVAR'].mean()
apperent_power = np.sqrt(avg_active**2 + avg_reactive**2)
current_pf = avg_active / apperent_power

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Average Power Factor", value=f"{current_pf:.2f}", delta=f"{current_pf - 0.85:.2f} vs Target")
with col2:
    st.metric(label="Peak Demand Load", value=f"{df_data['ActivePower_KW'].max():.1f} KW")
with col3:
    st.metric(label="Avg Reactive Power", value=f"{avg_reactive:.1f} KVAR")
with col4:
    st.metric(label="Aavg Line Voltage", value=f"{df_data['Voltage_V'].mean():.1f}V")

    
st.markdown("----")
#6 DATA VISUALIZATION
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Power Performance Curve (Active vs Reactive Power)")
    fig_power= px.line(
        df_data,
        x='Timestamp',
        y=['ActivePower_KW', 'ReactivePower_KVAR'],
        labels={'value': 'Power(KW / KVAR)', 'Timestamp': 'Time'},
        title="Active vs Reactive Load Profiles Over Selected Period"

    )

    st.plotly_chart(fig_power, use_container_width=True)
with col_chart2:
    st.subheader("Current Consumption Distribution Histogram")
    fig_current=px.histogram(
        df_data,
        x='Current_A',
        nbins=30,
        labels={'Current_A': 'current(Amperse)', 'count': 'Frequency'},
        title='Current Distribution Profile for Peak Demand Identification',
        color_discrete_sequence=['#0066cc']

    )

    st.markdown("----")

    # 7 DATA LOG TABLE AND EXPORT
    st.subheader("Detailed Equipment Logs")
    st.dataframe(df_data.style.format({
        'Voltage_V': '{:.1f}',
        'Current_A': '{:.1f}',
        'ActivePower_KW': '{:.2f}',
        'ReactivePower_KVAR':'{:.2f}'

    })  , use_container_width="auto")

    csv_data = df_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Dowload Electrical Reading Log(CSV)",
        data=csv_data,
        file_name=f"Electrical_Report_{selected_equipment.replace('','_')}.csv",
        mime="text/csv"
    )

