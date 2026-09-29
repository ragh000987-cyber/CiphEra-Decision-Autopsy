import os
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")

STATUS_COLORS = {
    "success": "#22c55e",
    "partial": "#f59e0b",
    "failure": "#ef4444",
    "unknown": "#94a3b8",
}





def api_get(path: str):
    try:
        resp = requests.get(f"{API_BASE}{path}", timeout=30)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as exc:
        st.error(f"API error: {exc}")
        return None


def api_post(path: str, payload: dict | None = None):
    try:
        resp = requests.post(f"{API_BASE}{path}", json=payload or {}, timeout=120)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as exc:
        st.error(f"API error: {exc}")
        return None


def status_badge(status: str) -> str:
    color = STATUS_COLORS.get(status, STATUS_COLORS["unknown"])
    return f'<span style="background:{color};color:white;padding:2px 10px;border-radius:12px;font-size:0.8rem;">{status}</span>'


st.set_page_config(page_title="CiphEra", page_icon="🔍", layout="wide")

st.title("CiphEra")
st.caption("Decision memory · Hindsight integration · Autopsy")

health = api_get("/health")
if health:
    st.sidebar.success(f"API: {health.get('status', 'unknown')}")
else:
    st.sidebar.error("Backend unreachable — start with: `python -m backend.main`")

hindsight = api_get("/hindsight/status")
if hindsight:
    if hindsight.get("available"):
        st.sidebar.info(f"Hindsight @ {hindsight.get('base_url')}")
    else:
        st.sidebar.warning("Hindsight client not installed")

decisions = api_get("/decisions") or []
if not decisions:
    st.stop()

decision_map = {d["id"]: d for d in decisions}
selected_id = st.sidebar.selectbox(
    "Select decision",
    options=list(decision_map.keys()),
    format_func=lambda did: decision_map[did]["title"],
)

decision = decision_map[selected_id]

col_main, col_meta = st.columns([3, 1])

with col_meta:
    st.markdown(status_badge(decision["outcome_status"]), unsafe_allow_html=True)
    st.write(f"**Date:** {decision['timestamp'][:10]}")
    if decision.get("tags"):
        st.write("**Tags:** " + ", ".join(decision["tags"]))

with col_main:
    st.subheader(decision["title"])
    st.markdown("**Context**")
    st.write(decision["context"])
    st.markdown("**Reasoning**")
    st.write(decision["reasoning"])

tab_detail, tab_autopsy, tab_hindsight = st.tabs(["Assumptions & Outcome", "Autopsy", "Hindsight"])

with tab_detail:
    st.markdown("**Assumptions**")
    for assumption in decision.get("assumptions", []):
        st.markdown(f"- {assumption}")

    st.markdown("**Outcome**")
    st.write(decision.get("outcome") or "_No outcome recorded_")

    if decision.get("evidence"):
        st.markdown("**Evidence**")
        for item in decision["evidence"]:
            st.markdown(f"- {item}")

with tab_autopsy:
    focus = st.text_input("Focus area (optional)", placeholder="e.g. premise drift, cost vs risk")
    if st.button("Run Autopsy", type="primary"):
        with st.spinner("Analyzing decision..."):
            report = api_post(f"/decisions/{selected_id}/autopsy", {"decision_id": selected_id, "focus": focus or None})
        if report:
            st.markdown("### Summary")
            st.write(report.get("summary", ""))

            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Root Causes**")
                for item in report.get("root_causes", []):
                    st.markdown(f"- {item}")
                st.markdown("**Premise Drift**")
                for item in report.get("premise_drift", []):
                    st.markdown(f"- {item}")
            with c2:
                st.markdown("**Lessons**")
                for item in report.get("lessons", []):
                    st.markdown(f"- {item}")
                st.markdown("**Recommendations**")
                for item in report.get("recommendations", []):
                    st.markdown(f"- {item}")

with tab_hindsight:
    bank_id = st.text_input("Bank ID", value="ciph-era-decisions")

    if st.button("Retain in Hindsight"):
        with st.spinner("Storing decision..."):
            result = api_post(f"/decisions/{selected_id}/retain", {"bank_id": bank_id})
        if result:
            st.success("Decision retained")
            st.json(result)

    reflect_query = st.text_area(
        "Reflect query",
        value=f"What can we learn from '{decision['title']}'?",
    )
    if st.button("Reflect"):
        with st.spinner("Reflecting..."):
            result = api_post(
                f"/decisions/{selected_id}/reflect",
                {"query": reflect_query, "bank_id": bank_id},
            )
        if result:
            st.json(result)

    recall_query = st.text_input("Recall query", placeholder="Find similar past decisions...")
    if st.button("Recall"):
        with st.spinner("Recalling..."):
            result = api_post("/hindsight/recall", {"query": recall_query, "bank_id": bank_id})
        if result:
            st.json(result)
