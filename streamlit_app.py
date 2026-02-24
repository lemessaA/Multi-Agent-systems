import asyncio
from typing import Dict, Any, List

import streamlit as st

from agents.router_agent import RouterAgent
from schemas.models import AgentRequest, AgentType, AgentResponse, MultiAgentResponse


def get_router_agent() -> RouterAgent:
    """Get or create a RouterAgent stored in session state."""
    if "router_agent" not in st.session_state:
        st.session_state.router_agent = RouterAgent()
    return st.session_state.router_agent


async def _run_query(
    router: RouterAgent, query: str, mode: str, location: str | None
) -> Dict[str, Any]:
    """Execute a query against the multi-agent router."""
    agent_type = None
    if mode == "Weather":
        agent_type = AgentType.WEATHER
    elif mode == "News":
        agent_type = AgentType.NEWS
    elif mode == "Finance":
        agent_type = AgentType.FINANCE

    request = AgentRequest(
        query=query,
        agent_type=agent_type,
        location=location or None,
    )

    result = await router.process(request)
    return result


def run_query_sync(query: str, mode: str, location: str | None) -> Dict[str, Any]:
    """Synchronous wrapper for the async query function."""
    router = get_router_agent()
    return asyncio.run(_run_query(router, query, mode, location))


def render_response(result: Dict[str, Any]) -> None:
    """Pretty-print router / agent responses in the UI."""
    st.markdown("### Results")

    execution_time = result.get("execution_time")
    if execution_time is not None:
        st.caption(f"Execution time: {execution_time:.2f}s")

    responses: List[AgentResponse] = result.get("responses", [])

    if not responses:
        st.info("No responses returned from agents.")
        return

    for idx, resp in enumerate(responses, start=1):
        agent_label = getattr(resp.agent_type, "value", str(resp.agent_type))
        with st.container(border=True):
            st.markdown(f"**Agent:** `{agent_label}`")
            st.markdown(resp.response)

            if resp.data:
                with st.expander("View agent details"):
                    if "raw_output" in resp.data:
                        st.markdown("**Raw output**")
                        st.code(str(resp.data["raw_output"]))
                    if "intermediate_steps" in resp.data:
                        st.markdown("**Intermediate steps**")
                        st.code(str(resp.data["intermediate_steps"]))


def main() -> None:
    st.set_page_config(
        page_title="Multi-Agent AI Console",
        layout="wide",
    )

    st.title("🤖 Cloud-Native intelligence Platform ")
    st.caption(
        "goal-oriented interface for your weather, news, and finance agents with intelligent routing."
    )

    with st.sidebar:
        st.subheader("AI Mode")
        mode = st.radio(
            "Routing mode",
            ["Auto (Smart Router)", "Weather", "News", "Finance"],
            index=0,
        )

        st.markdown("---")
        st.subheader("Context (optional)")
        location = st.text_input("Location (for weather/finance, optional)")

        st.markdown("---")
        st.subheader("Examples")
        st.markdown("- **Auto**: `Weather in Tokyo and latest tech news`")
        st.markdown("- **Weather**: `3-day forecast for London`")
        st.markdown("- **News**: `Top AI headlines today`")
        st.markdown("- **Finance**: `Current price of AAPL and Bitcoin`")

    st.markdown("### Ask the AI")
    query = st.text_area(
        "Natural language query",
        placeholder="Ask about weather, news, markets, or combine them in one question...",
        height=120,
    )

    col_run, col_clear = st.columns([1, 1])
    run_clicked = col_run.button("Run", type="primary", use_container_width=True)
    clear_clicked = col_clear.button("Clear", use_container_width=True)

    if clear_clicked:
        st.session_state.pop("last_result", None)
        st.experimental_rerun()

    # Show previous result if available
    last_result = st.session_state.get("last_result")
    if last_result and not run_clicked:
        render_response(last_result)

    if run_clicked:
        if not query.strip():
            st.warning("Please enter a query first.")
            return

        with st.spinner("Thinking with multi-agent router..."):
            # Normalize mode label for internal logic
            internal_mode = (
                "Auto"
                if mode.startswith("Auto")
                else mode  # "Weather", "News", "Finance"
            )
            try:
                result = run_query_sync(query=query.strip(), mode=internal_mode, location=location)
                st.session_state["last_result"] = result
                render_response(result)
            except Exception as exc:
                st.error(f"Failed to process query: {exc}")


if __name__ == "__main__":
    main()

