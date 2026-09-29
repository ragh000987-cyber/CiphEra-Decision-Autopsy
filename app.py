import os
import json
from datetime import datetime
import streamlit as st

try:
    from hindsight_client import Hindsight
except ImportError:
    Hindsight = None

st.set_page_config(page_title="CiphEra | Decision Autopsy", page_icon="🧠", layout="wide")

BANK_ID = os.getenv("HINDSIGHT_BANK_ID", "ciphera")
BASE_URL = os.getenv("HINDSIGHT_BASE_URL", "https://api.hindsight.vectorize.io")
API_KEY = os.getenv("HINDSIGHT_API_KEY", "")


def get_client():
    if Hindsight is None:
        return None
    if not API_KEY:
        return None
    return Hindsight(base_url=BASE_URL, api_key=API_KEY)


def ensure_bank(client):
    try:
        client.create_bank(
            bank_id=BANK_ID,
            name="CiphEra Decision Memory",
            disposition={"skepticism": 4, "literalism": 3, "empathy": 2},
        )
    except Exception:
        # The bank may already exist.
        pass


def sample_decisions():
    return [
        {
            "id": "D001", "decision": "Increase digital advertising budget by 30% for a product launch",
            "reason": "A previous campaign produced strong returns during a similar launch period.",
            "expected": "30% increase in sales with positive ROAS.", "actual": "Sales increased only 8% and ROAS fell.",
            "lesson": "Historical campaign performance was not comparable because the audience and offer had changed.",
        },
        {
            "id": "D002", "decision": "Launch a new feature before the quarterly review",
            "reason": "The feature was nearly complete and the team expected early user feedback to help.",
            "expected": "Higher engagement without major support issues.", "actual": "Engagement rose 4%, but support tickets doubled.",
            "lesson": "Launching before support documentation and onboarding were ready created avoidable operational cost.",
        },
        {
            "id": "D003", "decision": "Increase inventory before a festival season",
            "reason": "Demand had increased during the previous festival season.",
            "expected": "90% of additional inventory sold within the season.", "actual": "Only 58% sold; remaining stock required discounts.",
            "lesson": "Past seasonal demand was not enough; current price sensitivity and competitor supply also mattered.",
        },
        {
            "id": "D004", "decision": "Move a small service from a local server to the cloud",
            "reason": "The team expected easier scaling and lower maintenance effort.",
            "expected": "Lower operational effort with no noticeable performance loss.", "actual": "Maintenance decreased, but network latency affected response times.",
            "lesson": "Migration decisions should account for workload location and latency, not only maintenance savings.",
        },
        {
            "id": "D005", "decision": "Hire two engineers immediately for a new project",
            "reason": "The project schedule appeared aggressive and additional capacity seemed necessary.",
            "expected": "Two hires would keep the launch on schedule.", "actual": "Hiring took longer than expected and onboarding delayed the project.",
            "lesson": "Hiring capacity should be balanced against onboarding time; temporary internal allocation may be faster.",
        },
        {
            "id": "D006", "decision": "Offer a 20% discount to increase conversions",
            "reason": "A discount had previously improved conversion during a similar promotion.",
            "expected": "Conversion rate would increase enough to offset the lower margin.", "actual": "Conversion increased, but total contribution margin decreased.",
            "lesson": "Conversion improvement should be evaluated together with margin impact rather than in isolation.",
        },
        {
            "id": "D007", "decision": "Run a second marketing channel at the same budget",
            "reason": "The team wanted to diversify traffic sources.",
            "expected": "New channel would generate incremental customers.", "actual": "Much of the traffic overlapped with existing customers.",
            "lesson": "Channel diversification should measure incremental reach rather than raw traffic.",
        },
        {
            "id": "D008", "decision": "Release an internal automation tool to all teams",
            "reason": "A pilot team saved significant manual effort.",
            "expected": "Similar time savings across the organization.", "actual": "Adoption was low outside the pilot team.",
            "lesson": "Pilot success does not guarantee organization-wide adoption; workflow fit and training matter.",
        },
        {
            "id": "D009", "decision": "Expand a service into a new city",
            "reason": "The existing city had reached strong repeat usage.",
            "expected": "The new city would reach similar adoption within six months.", "actual": "Adoption remained below target because customer acquisition costs were higher.",
            "lesson": "Expansion assumptions must validate local acquisition economics rather than copy existing-city performance.",
        },
        {
            "id": "D010", "decision": "Use a previous quarter's demand forecast for the next quarter",
            "reason": "The previous forecast had been close to actual demand.",
            "expected": "Forecast error below 10%.", "actual": "Demand was 24% below forecast.",
            "lesson": "Forecast accuracy in one period does not prove the same drivers will persist in the next period.",
        },
    ]


def format_decision(d):
    return (
        f"DECISION ID: {d['id']}\n"
        f"Decision: {d['decision']}\n"
        f"Reason: {d['reason']}\n"
        f"Expected outcome: {d['expected']}\n"
        f"Actual outcome: {d['actual']}\n"
        f"Result: Compared expected and actual outcomes.\n"
        f"Lesson learned: {d['lesson']}"
    )


def seed_demo(client):
    memories = sample_decisions()
    client.retain_batch(
        bank_id=BANK_ID,
        items=[{"content": format_decision(d), "context": "CiphEra synthetic historical decision dataset"} for d in memories],
    )
    return len(memories)


def analyze_with_hindsight(client, decision, reason, expected, confidence):
    query = (
        f"Find previous decisions similar to this proposed decision: {decision}. "
        f"Reason: {reason}. Expected outcome: {expected}. "
        "Focus on comparable decisions, their expected and actual outcomes, failed assumptions, and lessons learned."
    )
    recall = client.recall(bank_id=BANK_ID, query=query, max_tokens=5000, budget="mid")
    memories = [m.text for m in recall.results]
    reflect_query = (
        "Analyze this new decision using relevant past decision experiences. "
        "Do not make the decision for the user. Identify historical patterns, risks, "
        "assumptions worth testing, and lessons that are relevant. Clearly separate evidence from inference.\n\n"
        f"NEW DECISION: {decision}\nREASON: {reason}\nEXPECTED OUTCOME: {expected}\nCONFIDENCE: {confidence}\n"
    )
    reflection = client.reflect(bank_id=BANK_ID, query=reflect_query, context="CiphEra Decision Autopsy Agent")
    return memories, reflection.text


def fallback_analysis(decision, reason, expected, confidence):
    return ["No Hindsight memories are connected yet."], (
        f"Current decision: {decision}\n\n"
        f"Reason: {reason}\nExpected: {expected}\nConfidence: {confidence}\n\n"
        "Initial analysis: identify the assumptions behind the expected outcome, define measurable success criteria, "
        "and record the actual result so CiphEra can perform an autopsy later."
    )


def autopsy_with_hindsight(client, decision, reason, expected, actual):
    query = (
        f"Decision autopsy for: {decision}. Reason: {reason}. Expected: {expected}. Actual: {actual}. "
        "Find similar historical decisions and lessons, then identify likely assumption gaps and reusable lessons."
    )
    reflection = client.reflect(
        bank_id=BANK_ID,
        query=(
            "Perform a decision autopsy. Compare expected and actual outcomes. Explain what happened, "
            "which assumptions appear unsupported by the evidence, what worked, what did not, and produce "
            "one concise reusable lesson for future similar decisions. Do not invent facts.\n\n" + query
        ),
        context="CiphEra Decision Autopsy Agent",
    )
    return reflection.text


def local_autopsy(decision, expected, actual):
    return (
        f"Decision: {decision}\n\nExpected outcome: {expected}\nActual outcome: {actual}\n\n"
        "Autopsy: The key evidence is the gap between the expected and actual outcomes. "
        "Before repeating this decision, identify which assumption caused the expectation and test whether it still holds.\n\n"
        "Reusable lesson: Future decisions of this type should compare current conditions with the historical conditions that produced the original expectation."
    )


st.markdown("# CiphEra")
st.caption("Decision Autopsy Agent — learn from what happened before making the next decision.")

client = get_client()

with st.sidebar:
    st.header("Hindsight")
    if client:
        st.success("Connected")
        if st.button("Create / verify memory bank"):
            ensure_bank(client)
            st.success(f"Bank ready: {BANK_ID}")
        if st.button("Load demo history"):
            try:
                ensure_bank(client)
                n = seed_demo(client)
                st.success(f"Stored {n} historical decisions in Hindsight.")
            except Exception as e:
                st.error(f"Could not load demo history: {e}")
    else:
        st.warning("Hindsight is not connected. Add HINDSIGHT_API_KEY to use live memory.")
        st.code("HINDSIGHT_API_KEY=your_key")

    st.divider()
    st.write("**Demo flow**")
    st.write("1. Load demo history")
    st.write("2. Analyze a new decision")
    st.write("3. Record the real outcome")
    st.write("4. Run the autopsy")
    st.write("5. Save the lesson")

if "analysis" not in st.session_state:
    st.session_state.analysis = None
if "autopsy" not in st.session_state:
    st.session_state.autopsy = None
if "decision_data" not in st.session_state:
    st.session_state.decision_data = {}

st.subheader("1. Analyze a new decision")
col1, col2 = st.columns(2)
with col1:
    decision = st.text_area("What decision are you considering?", placeholder="e.g. Increase our advertising budget by 30% next month")
    reason = st.text_area("Why are you considering it?", placeholder="e.g. A previous campaign produced strong sales")
with col2:
    expected = st.text_area("What do you expect to happen?", placeholder="e.g. Sales should increase by 20%")
    confidence = st.select_slider("Confidence in this prediction", options=["Low", "Medium", "High"], value="Medium")

if st.button("Analyze Decision", type="primary", use_container_width=True):
    if not decision or not expected:
        st.error("Enter the decision and expected outcome.")
    elif client:
        try:
            ensure_bank(client)
            memories, reflection = analyze_with_hindsight(client, decision, reason, expected, confidence)
            st.session_state.analysis = (memories, reflection)
            st.session_state.decision_data = {"decision": decision, "reason": reason, "expected": expected, "confidence": confidence}
        except Exception as e:
            st.error(f"Hindsight analysis failed: {e}")
    else:
        st.session_state.analysis = fallback_analysis(decision, reason, expected, confidence)
        st.session_state.decision_data = {"decision": decision, "reason": reason, "expected": expected, "confidence": confidence}

if st.session_state.analysis:
    memories, reflection = st.session_state.analysis
    st.divider()
    st.subheader("2. What CiphEra remembers")
    for i, memory in enumerate(memories[:5], 1):
        with st.expander(f"Past experience {i}"):
            st.write(memory)

    st.subheader("3. CiphEra analysis")
    st.info(reflection)

    st.divider()
    st.subheader("4. Record the actual outcome")
    actual = st.text_area("What actually happened?", placeholder="e.g. Sales increased by only 8%")
    if st.button("Run Decision Autopsy", use_container_width=True):
        if not actual:
            st.error("Enter the actual outcome first.")
        else:
            d = st.session_state.decision_data
            if client:
                try:
                    autopsy = autopsy_with_hindsight(client, d["decision"], d["reason"], d["expected"], actual)
                except Exception as e:
                    autopsy = local_autopsy(d["decision"], d["expected"], actual)
                    st.warning(f"Hindsight autopsy failed, showing local fallback: {e}")
            else:
                autopsy = local_autopsy(d["decision"], d["expected"], actual)
            st.session_state.autopsy = autopsy
            st.session_state.decision_data["actual"] = actual

if st.session_state.autopsy:
    st.divider()
    st.subheader("5. Decision Autopsy")
    st.write(st.session_state.autopsy)

    if st.button("Save this experience to Hindsight", type="primary", use_container_width=True):
        d = st.session_state.decision_data
        if client:
            try:
                content = (
                    f"DECISION AUTOPSY — {datetime.now().isoformat()}\n"
                    f"Decision: {d['decision']}\nReason: {d['reason']}\n"
                    f"Expected outcome: {d['expected']}\nActual outcome: {d['actual']}\n"
                    f"Autopsy and lesson: {st.session_state.autopsy}"
                )
                client.retain(bank_id=BANK_ID, content=content, context="CiphEra learned decision experience")
                st.success("Experience saved to Hindsight. Future decisions can now retrieve this lesson.")
            except Exception as e:
                st.error(f"Could not save to Hindsight: {e}")
        else:
            st.warning("Connect Hindsight first. The local demo cannot persist this lesson to Hindsight.")

st.divider()
st.caption("CiphEra demonstrates a closed learning loop: decision → prediction → outcome → autopsy → lesson → Hindsight memory → future decision.")
