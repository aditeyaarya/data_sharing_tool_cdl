import sys
import os
from datetime import date

# Ensure project root is on sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.validators import all_required_present

def test_all_required_present_ok():
    ok, missing = all_required_present(
        date_value=date.today(),
        stream="AI",
        founder_name="A",
        venture_name="B",
        venture_manager_name="C",
        link="https://x.y",
    )
    assert ok is True and missing == []


def test_all_required_present_missing():
    ok, missing = all_required_present(
        date_value=None,
        stream="— Select —",
        founder_name="",
        venture_name="",
        venture_manager_name="",
        link="",
    )
    assert ok is False
    assert len(missing) >= 5