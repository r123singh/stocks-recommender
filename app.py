import openai
import streamlit as st 

prompt = """
### **Prompt for Stock Recommendation System**  

**Objective:**  
Help new market entrants with limited budgets choose the best stocks to buy from a provided list, based on their risk tolerance, investment horizon, and goals.  

**Input Requirements:**  
1. **User Preferences**  
   - Risk Tolerance: Low / Moderate / High  
   - Investment Horizon: Short-term / Medium-term / Long-term  
   - Budget: Total amount available for investment  
   - Preferred Sectors (if any): Tech, Healthcare, Energy, etc.  

2. **Stock List**  
   - Stocks provided by the user (or predefined market-based selection)  
   - Current price data (if available)  

3. **Market Context** *(Optional but useful)*  
   - Country/region preference (e.g., US, India, EU)  
   - Interest in dividend-paying vs. growth stocks  

**Output Format:**  
- Provide **2-3 investment options** based on diversification, stability, and growth potential.  
- Each option should contain 2-3 stocks with a suggested allocation.  
- Include a **brief explanation** of why each stock is selected.  
- Ensure at least **one balanced approach** combining growth and stability.  

**Example Output:**  

✅ **Option 1: Balanced Growth & Stability (Tech + Consumer + Healthcare)**  
- **Apple (AAPL)** – $350 (Stable, blue-chip, steady growth)  
- **Nvidia (NVDA)** – $350 (AI & semiconductor boom, high growth)  
- **Pfizer (PFE)** – $300 (Healthcare stability, dividends)  

💡 *Why?* Apple offers reliability, Nvidia is a high-growth bet, and Pfizer provides stability with dividends.  

✅ **Option 2: High-Growth Tech Focus**  
- **Microsoft (MSFT)** – $500 (AI & Cloud leader, strong fundamentals)  
- **Tesla (TSLA)** – $500 (EV growth potential, but volatile)  

💡 *Why?* This option leans towards future tech, ideal for those who can handle moderate volatility.  

✅ **Option 3: Budget-Friendly High Potential Picks**  
- **SoFi Technologies (SOFI)** – $400 (Fintech growth play)  
- **Palantir (PLTR)** – $300 (AI & Big Data leader)  
- **ChargePoint (CHPT)** – $300 (EV charging infrastructure)  

💡 *Why?* These are lower-priced, high-upside stocks in emerging sectors.  

---  
"""

market_context_input1 = """

#### **User Profile 1 (Conservative Investor, Long-Term Focus)**  
- **Risk Tolerance:** Low  
- **Investment Horizon:** 5+ years  
- **Budget:** $5,000  
- **Preferred Sectors:** Consumer goods, healthcare, blue-chip tech  
- **Market Preference:** US stocks  
- **Dividend Preference:** Yes  
"""

market_context_input2 = """

#### **User Profile 2 (Moderate Investor, Medium-Term Growth Focus)**  
- **Risk Tolerance:** Moderate  
- **Investment Horizon:** 1-3 years  
- **Budget:** $2,000  
- **Preferred Sectors:** AI, Fintech, EV  
- **Market Preference:** US stocks  
- **Dividend Preference:** No  
---
"""

market_context_input3 = """
#### **User Profile 3 (Aggressive Investor, Short-Term Trading Focus)**  
- **Risk Tolerance:** High  
- **Investment Horizon:** Less than 6 months  
- **Budget:** $1,500  
- **Preferred Sectors:** High-volatility tech, crypto, biotech  
- **Market Preference:** US stocks + some speculative picks  
- **Dividend Preference:** No  
"""

stock_list = """
#### **Stock List (US Market) – Updated Prices**  
| Stock | Company | Price (USD) | Sector |  
|--------|------------|-------------|-----------|  
| **AAPL** | Apple Inc. | $185 | Technology |  
| **MSFT** | Microsoft Corp. | $410 | Technology |  
| **NVDA** | Nvidia Corp. | $700 | AI/Semiconductors |  
| **TSLA** | Tesla Inc. | $190 | EV/Automotive |  
| **PLTR** | Palantir Technologies | $21 | AI/Big Data |  
| **SOFI** | SoFi Technologies | $9 | Fintech |  
| **CHPT** | ChargePoint Holdings | $2.50 | EV Charging |  
| **JNJ** | Johnson & Johnson | $158 | Healthcare |  
| **PFE** | Pfizer Inc. | $27 | Healthcare |  
| **KO** | Coca-Cola | $60 | Consumer Goods |  
| **AMZN** | Amazon | $170 | E-Commerce |  
| **GOOGL** | Alphabet (Google) | $145 | Technology |  
"""

openai.api_key = st.secrets["API_KEY"]

def craft_options(market_context_input):
    try:
        response = openai.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": market_context_input
            }
        ]
    )
    except Exception as e:
        return "ERROR"
    return response.choices[0].message.content

st.title("Stocks Recommendation System")

profile = st.sidebar.selectbox("Select Profile", ["Investor_profile_1", "Investor_profile_2", "Investor_profile_3"])

if profile == "Investor_profile_2":
    st.write("""
        ---
        ## **📌 Stock Investment Input Template**  
        ### **2️⃣ Investor Profile**  
        ✅ **Risk Tolerance:** Moderate  
        ✅ **Investment Horizon:** Medium-term (1-3 years)  
        ✅ **Total Budget:** $2,000  
        ✅ **Preferred Sectors:** Fintech, AI, EV  
        ✅ **Market Preference:** US  
        ✅ **Dividend Preference:** No  

        💡 *System will generate recommendations based on diversification, growth potential, and budget allocation.*  
        """
        )
    if st.button("Submit", type="primary", key="invetor_profile2_btn"):
        response = craft_options(market_context_input2)
        st.write(response)
elif profile == "Investor_profile_1":
    st.write("""
        ---
        ## **📌 Stock Investment Input Template**  
        ### **1️⃣Investor Profile**  
        ✅ **Risk Tolerance:** Low  
        ✅ **Investment Horizon:** Long-term(3+ years)
        ✅ **Total Budget:** $5,000  
        ✅ **Preferred Sectors:** Consumer goods, healthcare, blue-chip tech  
        ✅ **Market Preference:** US  
        ✅ **Dividend Preference:** Yes  

        💡 *System will generate recommendations based on diversification, growth potential, and budget allocation.*  
        """
        )
    
    if st.button("Submit", type="primary", key="invetor_profile1_btn"):
        response = craft_options(market_context_input1)
        st.write(response)
elif profile == "Investor_profile_3":    
    st.write("""
        ---
        ## **📌 Stock Investment Input Template**  
        ### **3️⃣ Investor Profile**  
        ✅ **Risk Tolerance:** High  
        ✅ **Investment Horizon:** Short-term(<6 months)
        ✅ **Total Budget:** $1,500 
        ✅ **Preferred Sectors:** High-volatility tech, crypto, biotech  
        ✅ **Market Preference:** US  
        ✅ **Dividend Preference:** No  

        💡 *System will generate recommendations based on diversification, growth potential, and budget allocation.*  
        """
        )
    if st.button("Submit", type="primary", key="invetor_profile3_btn"):
        response = craft_options(market_context_input3)
        st.write(response)


        
