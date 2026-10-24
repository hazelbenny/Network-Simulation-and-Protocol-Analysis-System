
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Network Protocol Analysis",
    page_icon="🌐",
    layout="wide"
)

st.title("Network Protocol Analysis Dashboard")
st.write("OSPF vs RIP v2 — Link Failure and Recovery Analysis")

st.info(
    "Enter your recorded Packet Tracer observations below. "
    "The dashboard calculates recovery time and packet-loss percentage."
)

# Previously recorded experimental observations
default_data = pd.DataFrame({
    "Protocol": ["OSPF", "OSPF", "OSPF", "RIP v2", "RIP v2", "RIP v2"],
    "Trial": [1, 2, 3, 1, 2, 3],
    "Shutdown (s)": [7.72, 9.08, 8.75, 9.85, 6.47, 8.25],
    "Recovery (s)": [14.54, 15.77, 20.48, 18.23, 17.39, 16.50],
    "Packets Sent": [11, 24, 26, 23, 22, 22],
    "Replies Received": [9, 23, 24, 19, 7, 19]
})

st.subheader("1. Experiment Data")
st.caption(
    "Edit the table if your final recorded measurements differ. "
    "Recovery (s) is the time successful replies resumed."
)

data = st.data_editor(
    default_data,
    num_rows="dynamic",
    use_container_width=True,
    key="experiment_data"
)

# Validate and calculate results
data = data.copy()

numeric_cols = [
    "Trial", "Shutdown (s)", "Recovery (s)",
    "Packets Sent", "Replies Received"
]

for col in numeric_cols:
    data[col] = pd.to_numeric(data[col], errors="coerce")

valid = (
    data["Protocol"].isin(["OSPF", "RIP v2"])
    & data[numeric_cols].notna().all(axis=1)
    & (data["Trial"] > 0)
    & (data["Shutdown (s)"] >= 0)
    & (data["Recovery (s)"] >= data["Shutdown (s)"])
    & (data["Packets Sent"] > 0)
    & (data["Replies Received"] >= 0)
    & (data["Replies Received"] <= data["Packets Sent"])
)

if not valid.all():
    st.error(
        "Some rows are invalid. Check protocol names, times, "
        "trial numbers, and packet counts."
    )
    st.stop()

data["Recovery Time (s)"] = (
    data["Recovery (s)"] - data["Shutdown (s)"]
)

data["Packets Lost"] = (
    data["Packets Sent"] - data["Replies Received"]
)

data["Packet Loss (%)"] = (
    data["Packets Lost"] / data["Packets Sent"] * 100
)

st.subheader("2. Calculated Results")

summary = data.groupby("Protocol").agg(
    Trials=("Trial", "count"),
    Average_Recovery=("Recovery Time (s)", "mean"),
    Average_Packet_Loss=("Packet Loss (%)", "mean"),
    Total_Sent=("Packets Sent", "sum"),
    Total_Received=("Replies Received", "sum"),
    Total_Lost=("Packets Lost", "sum")
).reset_index()

summary["Overall Packet Loss (%)"] = (
    summary["Total_Lost"] / summary["Total_Sent"] * 100
)

display_summary = summary.rename(columns={
    "Average_Recovery": "Avg Recovery (s)",
    "Average_Packet_Loss": "Avg Trial Loss (%)",
    "Total_Sent": "Packets Sent",
    "Total_Received": "Replies Received",
    "Total_Lost": "Packets Lost"
})

st.dataframe(
    display_summary.round(2),
    hide_index=True,
    use_container_width=True
)

# Key metrics
for protocol in ["OSPF", "RIP v2"]:
    row = summary[summary["Protocol"] == protocol]
    if not row.empty:
        st.write(f"**{protocol}**")
        c1, c2, c3 = st.columns(3)
        c1.metric(
            "Average recovery",
            f'{row["Average_Recovery"].iloc[0]:.2f} s'
        )
        c2.metric(
            "Overall packet loss",
            f'{row["Overall Packet Loss (%)"].iloc[0]:.2f}%'
        )
        c3.metric(
            "Trials",
            int(row["Trials"].iloc[0])
        )

st.subheader("3. Protocol Comparison")

left, right = st.columns(2)

with left:
    st.write("Average Recovery Time by Trial")
    fig, ax = plt.subplots()
    for protocol, group in data.groupby("Protocol"):
        ax.plot(
            group["Trial"],
            group["Recovery Time (s)"],
            marker="o",
            label=protocol
        )
    ax.set_xlabel("Trial")
    ax.set_ylabel("Recovery Time (seconds)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)

with right:
    st.write("Overall Recorded Packet Loss")
    fig, ax = plt.subplots()
    ax.bar(
        summary["Protocol"],
        summary["Overall Packet Loss (%)"]
    )
    ax.set_ylabel("Packet Loss (%)")
    ax.grid(axis="y", alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)

st.subheader("4. Trial Details")
st.dataframe(data.round(2), hide_index=True, use_container_width=True)

csv = data.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download calculated results as CSV",
    data=csv,
    file_name="protocol_experiment_results.csv",
    mime="text/csv"
)

st.caption(
    "Packet loss is calculated across each complete recorded ping run, "
    "not solely during the convergence interval. Results reflect the "
    "entered trials and should not be interpreted as a universal "
    "ranking of the protocols."
)
