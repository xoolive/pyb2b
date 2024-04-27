import pytest
from pyb2b import b2b

import pandas as pd

today = pd.Timestamp("now")


@pytest.mark.skipif(b2b is None, reason="No key available")
def test_success() -> None:
    assert b2b is not None
    res = b2b.flightplanlist(today, origin="LFBO")
    assert res is not None
    assert res.data.shape[0] == 0 or all(res.data.origin == "LFBO")


@pytest.mark.skipif(b2b is None, reason="No key available")
def test_error() -> None:
    assert b2b is not None
    with pytest.raises(AttributeError):
        b2b.flightplanlist(today, origin="LBO")
