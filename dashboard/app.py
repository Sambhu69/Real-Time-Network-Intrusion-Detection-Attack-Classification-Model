import streamlit as st
import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="IDS Security Dashboard", layout="wide")

# --- LOAD ARTIFACTS ---
@st.cache_resource
def load_pipeline():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    models_dir = os.path.join(base_dir, "models")
    
    preprocessor = joblib.load(os.path.join(models_dir, "preprocessor.joblib"))
    mi_selector = joblib.load(os.path.join(models_dir, "mi_selector.joblib"))
    xgb_bin = joblib.load(os.path.join(models_dir, "xgboost_binary.joblib"))
    
    return preprocessor, mi_selector, xgb_bin

preprocessor, mi_selector, xgb_bin = load_pipeline()

# --- DASHBOARD UI ---
st.title("🛡️ Real-Time Network Intrusion Detection System")
st.markdown("Upload a batch of network flows (CSV) to analyze them for malicious activity.")

# Sidebar for file upload
st.sidebar.header("Traffic Input")
uploaded_file = st.sidebar.file_uploader("Upload Network Data (CSV)", type=["csv"])

if uploaded_file is not None:
    # Load data
    df = pd.read_csv(uploaded_file)
    st.write(f"**Analyzing {df.shape[0]} network flows...**")
    
    # Store true labels if they exist for reference, but drop them for prediction
    if 'label' in df.columns:
        df_input = df.drop(columns=['label', 'attack_cat'], errors='ignore')
    else:
        df_input = df.copy()

    # Apply Pipeline
    try:
        # Preprocess
        X_proc = preprocessor.transform(df_input)
        cat_cols = ['proto', 'service', 'state']
        num_cols = df_input.select_dtypes(include=['int64', 'float64']).columns.tolist()
        feature_names = num_cols + list(preprocessor.named_transformers_['cat'].get_feature_names_out(cat_cols))
        X_proc_df = pd.DataFrame(X_proc, columns=feature_names)
        
        # Select Features & Predict
        X_sel = mi_selector.transform(X_proc_df)
        preds = xgb_bin.predict(X_sel)
        probs = xgb_bin.predict_proba(X_sel)[:, 1] # Probability of Attack
        
        # Add predictions to the display dataframe
        df_results = df.copy()
        df_results['Prediction'] = ["Attack" if p == 1 else "Normal" for p in preds]
        df_results['Threat Score'] = probs
        
        # --- VISUALIZATION ---
        st.markdown("---")
        st.header("Threat Summary")
        
        total_flows = len(df_results)
        attacks = df_results[df_results['Prediction'] == 'Attack'].shape[0]
        normals = total_flows - attacks
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Flows Analyzed", total_flows)
        col2.metric("Normal Traffic", normals)
        col3.metric("Critical Threats Detected", attacks, delta=f"{attacks} alerts", delta_color="inverse")
        
        # Charts
        st.subheader("Traffic Distribution")
        fig, ax = plt.subplots(figsize=(8, 3))
        sns.countplot(data=df_results, y='Prediction', palette={'Normal': 'green', 'Attack': 'red'}, ax=ax)
        st.pyplot(fig)
        
        # Data Table
        st.subheader("High-Confidence Threat Log")
        high_threats = df_results[df_results['Prediction'] == 'Attack'].sort_values(by='Threat Score', ascending=False)
        st.dataframe(high_threats.head(100)) # Show top 100 threats
        
    except Exception as e:
        st.error(f"Error processing data: {e}. Please ensure the CSV has the correct network features.")
else:
    st.info("👈 Please upload a CSV file in the sidebar to begin analysis. (Hint: Use 'cleaned_test.csv' from your data/processed folder).")