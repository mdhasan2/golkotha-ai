import pytest

from domain.models import MatchFeatures

def test_match_features_converts_values_to_float() -> None:
    features = MatchFeatures.from_dict(
        {
            "home_form":4,
            "away_form":3.5,
        }
    )

    assert features.to_dict() == {
            "home_form":4.0,
            "away_form":3.5,
    }

def test_match_features_rejects_none() -> None:
    with pytest.raises(ValueError):
        MatchFeatures.from_dict(
            {
                "home_form": None,
            }
        )