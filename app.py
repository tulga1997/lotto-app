import streamlit as st
import pandas as pd
from itertools import combinations
import random

st.title("Lotto New Combination Generator")

uploaded_history = st.file_uploader("Upload previous draws (CSV, 6 columns)", type="csv")
if uploaded_history:
    history_df = pd.read_csv(uploaded_history, header=None)
    previous_draws = set([tuple(sorted(map(int, row))) for row in history_df.values])

    with st.expander("Number filter"):
        selected_numbers = st.multiselect("Numbers", list(range(1,46)), default=list(range(1,46)))
        only_even = st.checkbox("Even only")
        only_odd = st.checkbox("Odd only")
        must_include = st.text_input("Must include (comma separated)", "")

    n_generate = st.number_input("How many random new combinations?", 1, 1000, 100)

    if st.button("Generate new combinations"):
        numbers = selected_numbers
        if only_even:
            numbers = [n for n in numbers if n % 2 == 0]
        if only_odd:
            numbers = [n for n in numbers if n % 2 == 1]

        combos = combinations(numbers, 6)
        unique_combos = [c for c in combos if tuple(sorted(c)) not in previous_draws]
        random.shuffle(unique_combos)
        if must_include:
            must = set(map(int, must_include.split(',')))
            unique_combos = [c for c in unique_combos if must <= set(c)]

        out_combos = unique_combos[:n_generate]
        df = pd.DataFrame(out_combos, columns=["N1", "N2", "N3", "N4", "N5", "N6"])
        st.write(df)
        csv = df.to_csv(index=False)
        st.download_button("Download new combinations", csv, file_name="new_combinations.csv")
