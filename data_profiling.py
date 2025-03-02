import pandas as pd
import numpy as np
from ydata_profiling import ProfileReport
from helper import load_data

def generate_data_profile():
    df = load_data()
    
    selected_columns = ["Year", "Country", "Value"]
    df = df[selected_columns]
    
    df["Value"] = pd.to_numeric(df["Value"].astype(str).str.replace(",", "", regex=True), errors='coerce')
    
    df.loc[df["Value"].notna(), "Value"] = np.log1p(df["Value"])
    
    justification_text = (
        "### Justification for Zero Values\n"
        "Certain countries legitimately report zero values for specific indicators. "
        "For example, some nations may have no recorded CO₂ emissions, no military spending, "
        "or no export activity in a given category. These zeros are valid and should not be treated "
        "as missing or incorrect data. The profiling report maintains these values while applying "
        "log transformation to non-zero entries to reduce skewness."
    )
    
    profile = ProfileReport(
        df, 
        title="Data Profiling Report - Includes Justification for Zero Values", 
        explorative=True, 
        minimal=True,
        pool_size=4
    )
    
    profile.to_file("data_profiling_report.html")
    print("✅ Data profiling report generated: data_profiling_report.html")
    
    with open("data_profiling_justification.md", "w") as f:
        f.write(justification_text)
    print("✅ Justification for Zero Values saved: data_profiling_justification.md")
    
    try:
        profile.to_widgets()
    except Exception:
        print("Inline widgets are only available in Jupyter environments.")

if __name__ == "__main__":
    generate_data_profile()

## COMMENT ABOUT THE OUTPUT

#The dataset highlights important variations in social and economic indices as well as offers an interesting analysis of world inequalities
#between nations. The significant skewness in the Value column implies that although most nations report modest values, several show
#excessive numbers that distort the distribution. Globally, developed economies often show substantially larger economic and demographic 
#indicators—such as GDP, trade volume, or energy consumption—than smaller or less industrialized countries. The existence of nations with zero
#values accentuates this difference even more; for example, certain countries might have zero military expenditure, no CO₂ emissions, or no 
#known economic output in particular industries. These are reflections of actual government economic and policy actions, not anomalies.

#Furthermore emphasized in the report is the variety of development routes available globally. While countries with low or zero values could 
#be emerging markets, environmentally conscious nations, or conflict-torn areas where particular economic activities are absent, countries 
#with high values in particular indicators could be leading global economies or highly industrialized areas. Outliers imply that some 
#countries control important indicators, therefore affecting world averages and rendering regional comparisons indispensable in order to 
#prevent false conclusions. Applying log transformation helps the dataset to become more interpretable, so enabling better trend 
#representation free from excessive skews. In the end, this profile activity emphasizes the complexity of world development and the need of 
# taking context and policy decisions into account while evaluating worldwide statistics.