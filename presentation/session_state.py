
DEFAULT_STATE: dict[str, Any] = {
    "baseline_prediction": None,
}


def initialize_session_state() -> None:
    for key, default_value in DEFAULT_STATE.items():
        print(key, default_value)