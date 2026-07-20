import pytest

from domain.models import MatchFeatures

def test_match_features_rejects_none() -> None:
    with pytest.raises(ValueError):
        MatchFeatures.from_dict(
            {
                "home_form": None,
            }
        )