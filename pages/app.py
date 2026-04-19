"""
Decision Intelligence Tool — Streamlit Frontend.
Run with: streamlit run pages/app.py
"""

import asyncio
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from engine.types import DecisionInput
from engine.pipeline import run_decision_pipeline
from config import settings

st.set_page_config(page_title="Decision Intelligence", page_icon="🎯", layout="wide")


def main():
    st.title("Decision Intelligence")
    st.caption("Compare your options. Get AI-powered ranked recommendations.")

    # Check API keys
    if not settings.has_any_api_key():
        st.error("No AI judge API keys configured. Set at least one: OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY")
        return

    judges = settings.available_judges()
    st.sidebar.markdown("**Available Judges**")
    for j in judges:
        st.sidebar.markdown(f"- {j}")

    # ─── Input Form ───
    with st.form("decision_form"):
        question = st.text_input(
            "What are you deciding?",
            placeholder="e.g. Which marketing strategy should we pursue?",
            max_chars=500,
        )

        st.markdown("**Options to compare** (2-10)")
        option_cols = st.columns(2)
        options = []
        for i in range(10):
            col = option_cols[i % 2]
            with col:
                opt = st.text_input(
                    f"Option {i+1}",
                    key=f"opt_{i}",
                    placeholder=f"Option {i+1}" if i < 2 else "(optional)",
                    label_visibility="collapsed" if i >= 2 else "visible",
                )
                if opt.strip():
                    options.append(opt.strip())

        st.markdown("**Evaluation criteria**")
        criteria = []
        for i in range(5):
            cols = st.columns([3, 1])
            with cols[0]:
                name = st.text_input(
                    f"Criterion {i+1}",
                    key=f"crit_name_{i}",
                    placeholder="e.g. Cost, Speed, Quality" if i == 0 else "(optional)",
                    label_visibility="collapsed" if i >= 1 else "visible",
                )
            with cols[1]:
                weight = st.slider(
                    "Weight",
                    1, 10, 5,
                    key=f"crit_weight_{i}",
                    label_visibility="collapsed",
                )
            if name.strip():
                criteria.append({"name": name.strip(), "weight": weight})

        submitted = st.form_submit_button("Analyze Options", type="primary", use_container_width=True)

    # ─── Run Pipeline ───
    if submitted:
        if len(question.strip()) < 5:
            st.error("Question must be at least 5 characters.")
            return
        if len(options) < 2:
            st.error("Provide at least 2 options.")
            return
        if len(criteria) < 1:
            st.error("Provide at least 1 criterion.")
            return

        input_data = DecisionInput(
            question=question.strip(),
            options=options,
            criteria=criteria,
        )

        progress_bar = st.progress(0, text="Starting analysis...")
        status_text = st.empty()

        step_count = [0]
        total_steps = 6

        def on_step(step: str, detail: str):
            step_count[0] += 1
            pct = min(step_count[0] / total_steps, 0.95)
            progress_bar.progress(pct, text=detail)

        with st.spinner("Running blind evaluation..."):
            try:
                result = asyncio.run(run_decision_pipeline(input_data, on_step=on_step))
            except Exception as e:
                st.error(f"Evaluation failed: {e}")
                return

        progress_bar.progress(1.0, text="Done!")

        # ─── Results ───
        st.divider()

        # Winner hero
        st.markdown(f"### Winner: **{result.winner}**")
        st.markdown(f"_{result.why_winner_won}_")

        # Confidence
        conf_color = {"high": "green", "moderate": "orange", "low": "red"}.get(result.confidence_level, "gray")
        st.markdown(
            f"**Confidence:** :{conf_color}[{result.confidence_level.upper()}] "
            f"({result.confidence_score:.0f}/100) — "
            f"{'Judges agree' if result.judges_agree else 'Judges split'} "
            f"({result.judge_count} judges)"
        )

        st.divider()

        # Ranked options
        st.markdown("### Ranked Options")
        for opt in result.ranked_options:
            with st.expander(f"#{opt.rank} — {opt.option} (Score: {opt.final_score:.1f}/10)", expanded=(opt.rank <= 2)):
                # Dimension scores
                score_cols = st.columns(min(len(opt.dimension_scores), 4))
                for i, (dim, score) in enumerate(opt.dimension_scores.items()):
                    if dim == "overall":
                        continue
                    col = score_cols[i % len(score_cols)]
                    with col:
                        label = dim.replace("_", " ").title()
                        st.metric(label, f"{score:.1f}/10")

                # Strengths & weaknesses
                if opt.strengths:
                    st.markdown("**Strengths:**")
                    for s in opt.strengths:
                        st.markdown(f"- {s}")
                if opt.weaknesses:
                    st.markdown("**Weaknesses:**")
                    for w in opt.weaknesses:
                        st.markdown(f"- {w}")

        # Meta
        st.divider()
        meta_cols = st.columns(3)
        with meta_cols[0]:
            st.metric("Latency", f"{result.latency_ms / 1000:.1f}s")
        with meta_cols[1]:
            st.metric("Est. Cost", f"${result.total_cost_usd:.4f}")
        with meta_cols[2]:
            st.metric("Run ID", result.run_id)


if __name__ == "__main__":
    main()
