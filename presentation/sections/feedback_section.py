
from application.use_cases.record_feedback import RecordFeedback

import streamlit as st


def render_feedback_section(
    record_feedback: RecordFeedback,
    interaction_id: str,
) -> None:
    print("Rendering feedback section")
    st.divider()
    st.subheader("Feedback")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("👍 Helpful"):
            print("Helpful button clicked")
            result = record_feedback.execute(
                interaction_id=interaction_id,
                rating=1,
            )

            if result is None:
                st.info("Feedback has already been submitted.")
            else:
                st.success("Thank you for your feedback!")

    with col2:
        if st.button("👎 Not Helpful"):
            print("Not Helpful button clicked")
            record_feedback.execute(
                interaction_id=interaction_id,
                rating=-1,
            )
            st.success("Thank you for your feedbackj!")