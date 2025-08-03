import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Project Cost Simulator",
    page_icon="💼",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        max-width: 1100px;
        margin: 0 auto;
    }
    .stButton>button {
        width: 100%;
    }
    .stNumberInput, .stSelectbox, .stSlider {
        margin-top: -10px;
    }
    .row-header {
        font-weight: bold;
        padding: 8px;
        background-color: #f0f0f0;
        border-radius: 4px;
        margin-bottom: 10px;
    }
    .result-text {
        font-size: 24px;
        font-weight: bold;
        color: green;
        margin-top: 20px;
    }
    .collapsible {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Header
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://tkmind.net/wp-content/uploads/2023/07/TKMind-180-%C3%97-60-px-1.png", width=100)
with col2:
    st.title("Project Cost Simulator")

# Currency and exchange rates
currency_symbols = {
    "USD": "$", "EUR": "€", "AED": "د.إ", "SAR": "﷼", "EGP": "£", "GBP": "£"
}

exchange_rates = {
    "USD": 1,
    "EUR": 0.88,
    "AED": 3.6725,
    "SAR": 3.75,
    "EGP": 48.6,
    "GBP": 0.77
}

# Initialize session state variables if they don't exist
if 'currency' not in st.session_state:
    st.session_state.currency = "USD"
if 'commitment_years' not in st.session_state:
    st.session_state.commitment_years = 5
if 'commitment_discount' not in st.session_state:
    st.session_state.commitment_discount = 8.0
if 'discount_1y' not in st.session_state:
    st.session_state.discount_1y = 0.0
if 'discount_2y' not in st.session_state:
    st.session_state.discount_2y = 2.0
if 'discount_3y' not in st.session_state:
    st.session_state.discount_3y = 5.0
if 'discount_5y' not in st.session_state:
    st.session_state.discount_5y = 8.0

# Main layout with two columns
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="row-header">Project Parameters</div>', unsafe_allow_html=True)
    
    # Number of Sprints
    sprints = st.slider("Number of Sprints", min_value=1, max_value=50, value=24, key="sprints")
    
    # One-off Costs
    st.markdown('<div class="collapsible">', unsafe_allow_html=True)
    st.subheader("One-off Costs")
    
    # Developers
    st.markdown("**Developers**")
    dev_col1, dev_col2 = st.columns(2)
    with dev_col1:
        dev_onsite_count = st.number_input("Onsite", min_value=0, max_value=10, value=0, key="dev_onsite_count")
    with dev_col2:
        dev_offshore_count = st.number_input("Offshore", min_value=0, max_value=10, value=2, key="dev_offshore_count")
    
    # Testers
    st.markdown("**Testers**")
    qa_col1, qa_col2 = st.columns(2)
    with qa_col1:
        qa_onsite_count = st.number_input("Onsite", min_value=0, max_value=10, value=0, key="qa_onsite_count")
    with qa_col2:
        qa_offshore_count = st.number_input("Offshore", min_value=0, max_value=10, value=2, key="qa_offshore_count")
    
    # Project Managers
    st.markdown("**Project Managers**")
    pm_col1, pm_col2 = st.columns(2)
    with pm_col1:
        pm_onsite_count = st.number_input("Onsite", min_value=0, max_value=5, value=1, key="pm_onsite_count")
    with pm_col2:
        pm_offshore_count = st.number_input("Offshore", min_value=0, max_value=5, value=0, key="pm_offshore_count")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Running Costs
    st.markdown('<div class="collapsible">', unsafe_allow_html=True)
    st.subheader("Running Costs")
    
    # Licensing Cost
    st.markdown("Licensing Cost")
    license_col1, license_col2 = st.columns(2)
    with license_col1:
        symbol = currency_symbols[st.session_state.currency]
        license_per_user = st.number_input(f"Cost ({symbol} per user/month)", 
                                          min_value=0.0, value=100.0, key="license_per_user")
    with license_col2:
        num_users = st.number_input("Users", min_value=0, max_value=1000, value=5, key="num_users")
    
    # License percentage option
    license_percentage = st.slider("Or % of One-off Costs", min_value=0, max_value=100, value=0, key="license_percentage")
    if license_percentage > 0:
        st.session_state.num_users = 0
    
    # Managed Service Cost
    st.markdown("Managed Service Cost")
    managed_service = st.slider(f"Monthly Cost ({currency_symbols[st.session_state.currency]})", 
                               min_value=0, max_value=1000, value=300, key="managed_service")
    
    # Commitment options
    st.markdown("Commitment")
    
    # Commitment selection
    commitment_col1, commitment_col2, commitment_col3, commitment_col4 = st.columns(4)
    
    # Function to handle commitment selection
    def select_commitment(years, discount):
        st.session_state.commitment_years = years
        st.session_state.commitment_discount = discount
    
    with commitment_col1:
        if st.button("1 Year\n0%", key="commit_1y"):
            select_commitment(1, st.session_state.discount_1y)
    with commitment_col2:
        if st.button("2 Years\n2%", key="commit_2y"):
            select_commitment(2, st.session_state.discount_2y)
    with commitment_col3:
        if st.button("3 Years\n5%", key="commit_3y"):
            select_commitment(3, st.session_state.discount_3y)
    with commitment_col4:
        if st.button("5 Years\n8%", key="commit_5y", type="primary"):
            select_commitment(5, st.session_state.discount_5y)
    
    # Discount adjustment controls
    with st.expander("Adjust Discount Values"):
        adj_col1, adj_col2, adj_col3, adj_col4 = st.columns(4)
        
        with adj_col1:
            st.session_state.discount_1y = st.number_input("1Y Discount (%)", 
                                                          min_value=0.0, max_value=20.0, 
                                                          value=st.session_state.discount_1y, 
                                                          step=0.5, key="adj_1y")
        with adj_col2:
            st.session_state.discount_2y = st.number_input("2Y Discount (%)", 
                                                          min_value=0.0, max_value=20.0, 
                                                          value=st.session_state.discount_2y, 
                                                          step=0.5, key="adj_2y")
        with adj_col3:
            st.session_state.discount_3y = st.number_input("3Y Discount (%)", 
                                                          min_value=0.0, max_value=20.0, 
                                                          value=st.session_state.discount_3y, 
                                                          step=0.5, key="adj_3y")
        with adj_col4:
            st.session_state.discount_5y = st.number_input("5Y Discount (%)", 
                                                          min_value=0.0, max_value=20.0, 
                                                          value=st.session_state.discount_5y, 
                                                          step=0.5, key="adj_5y")
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="row-header">Project Settings</div>', unsafe_allow_html=True)
    
    # Project Settings
    st.markdown('<div class="collapsible">', unsafe_allow_html=True)
    st.subheader("Project Settings")
    
    # Currency selection
    selected_currency = st.selectbox("Currency", 
                                   options=list(currency_symbols.keys()), 
                                   format_func=lambda x: f"{currency_symbols[x]} {x}",
                                   index=list(currency_symbols.keys()).index(st.session_state.currency),
                                   key="currency_select")
    
    # Update session state if currency changed
    if selected_currency != st.session_state.currency:
        st.session_state.currency = selected_currency
    
    # Sprint Duration
    sprint_duration = st.number_input("Sprint Duration (weeks)", 
                                   min_value=1, max_value=4, value=2, key="sprint_duration")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Daily Rates
    st.markdown('<div class="collapsible">', unsafe_allow_html=True)
    st.subheader("Daily Rates")
    
    # Developer Rates
    st.markdown("**Developer**")
    dev_rate_col1, dev_rate_col2 = st.columns(2)
    with dev_rate_col1:
        dev_onsite_rate = st.number_input("Onsite Rate", 
                                        min_value=0.0, value=700.0, 
                                        key="dev_onsite_rate")
    with dev_rate_col2:
        dev_offshore_rate = st.number_input("Offshore Rate", 
                                          min_value=0.0, value=500.0, 
                                          key="dev_offshore_rate")
    
    # Tester Rates
    st.markdown("**Tester**")
    qa_rate_col1, qa_rate_col2 = st.columns(2)
    with qa_rate_col1:
        qa_onsite_rate = st.number_input("Onsite Rate", 
                                       min_value=0.0, value=500.0, 
                                       key="qa_onsite_rate")
    with qa_rate_col2:
        qa_offshore_rate = st.number_input("Offshore Rate", 
                                         min_value=0.0, value=300.0, 
                                         key="qa_offshore_rate")
    
    # Project Manager Rates
    st.markdown("**Project Manager**")
    pm_rate_col1, pm_rate_col2 = st.columns(2)
    with pm_rate_col1:
        pm_onsite_rate = st.number_input("Onsite Rate", 
                                       min_value=0.0, value=700.0, 
                                       key="pm_onsite_rate")
    with pm_rate_col2:
        pm_offshore_rate = st.number_input("Offshore Rate", 
                                         min_value=0.0, value=500.0, 
                                         key="pm_offshore_rate")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Cost Adjustments
    st.markdown('<div class="collapsible">', unsafe_allow_html=True)
    st.subheader("Cost Adjustments")
    
    markup = st.number_input("Markup (%)", min_value=0.0, value=30.0, key="markup")
    discount = st.number_input("Additional Discount (%)", min_value=0.0, value=0.0, key="discount")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Calculate function
def calculate_cost():
    sprints_val = st.session_state.sprints
    sprint_duration_val = st.session_state.sprint_duration
    
    # Calculate days and months
    total_days = sprints_val * sprint_duration_val * 5
    months = (sprints_val * sprint_duration_val) / 4
    
    # Calculate one-off costs
    dev_cost = total_days * (
        st.session_state.dev_onsite_count * st.session_state.dev_onsite_rate +
        st.session_state.dev_offshore_count * st.session_state.dev_offshore_rate
    )
    
    qa_cost = total_days * (
        st.session_state.qa_onsite_count * st.session_state.qa_onsite_rate +
        st.session_state.qa_offshore_count * st.session_state.qa_offshore_rate
    )
    
    pm_cost = total_days * (
        st.session_state.pm_onsite_count * st.session_state.pm_onsite_rate +
        st.session_state.pm_offshore_count * st.session_state.pm_offshore_rate
    )
    
    one_off_total = dev_cost + qa_cost + pm_cost
    
    # Calculate licensing costs
    if st.session_state.license_percentage > 0:
        license_cost = (st.session_state.license_percentage / 100) * one_off_total
    else:
        license_cost = (st.session_state.license_per_user * 
                       st.session_state.num_users * months)
    
    # Calculate managed service costs
    managed_service_cost = st.session_state.managed_service * months
    
    # Calculate subtotal
    subtotal = one_off_total + license_cost + managed_service_cost
    
    # Apply markup
    total_with_markup = subtotal * (1 + st.session_state.markup / 100)
    
    # Apply discounts
    # First the additional discount
    total_after_discount = total_with_markup * (1 - st.session_state.discount / 100)
    
    # Then the commitment discount
    final_total = total_after_discount * (1 - st.session_state.commitment_discount / 100)
    
    return final_total, one_off_total, license_cost, managed_service_cost

# Calculate and display results
if True:  # This will run on every interaction
    final_total, one_off_total, license_cost, managed_service_cost = calculate_cost()
    
    # Display the grand total
    st.markdown('<div class="result-text">', unsafe_allow_html=True)
    symbol = currency_symbols[st.session_state.currency]
    st.markdown(f"Grand Total: {symbol}{final_total:,.2f}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Optional: Show breakdown
    with st.expander("Cost Breakdown"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**One-off Costs**")
            st.write(f"Developer: {symbol}{one_off_total * (st.session_state.dev_onsite_count * st.session_state.dev_onsite_rate + st.session_state.dev_offshore_count * st.session_state.dev_offshore_rate) / (st.session_state.dev_onsite_count * st.session_state.dev_onsite_rate + st.session_state.dev_offshore_count * st.session_state.dev_offshore_rate + 1e-10):,.2f}")
            st.write(f"Tester: {symbol}{one_off_total * (st.session_state.qa_onsite_count * st.session_state.qa_onsite_rate + st.session_state.qa_offshore_count * st.session_state.qa_offshore_rate) / (st.session_state.qa_onsite_count * st.session_state.qa_onsite_rate + st.session_state.qa_offshore_count * st.session_state.qa_offshore_rate + 1e-10):,.2f}")
            st.write(f"Project Manager: {symbol}{one_off_total * (st.session_state.pm_onsite_count * st.session_state.pm_onsite_rate + st.session_state.pm_offshore_count * st.session_state.pm_offshore_rate) / (st.session_state.pm_onsite_count * st.session_state.pm_onsite_rate + st.session_state.pm_offshore_count * st.session_state.pm_offshore_rate + 1e-10):,.2f}")
            st.markdown(f"**Total One-off:** {symbol}{one_off_total:,.2f}")
        
        with col2:
            st.markdown("**Running Costs**")
            st.write(f"Licensing: {symbol}{license_cost:,.2f}")
            st.write(f"Managed Service: {symbol}{managed_service_cost:,.2f}")
            st.markdown(f"**Subtotal:** {symbol}{(one_off_total + license_cost + managed_service_cost):,.2f}")
            st.write(f"Markup: {st.session_state.markup}%")
            st.write(f"Discounts: {st.session_state.discount + st.session_state.commitment_discount:.1f}%")