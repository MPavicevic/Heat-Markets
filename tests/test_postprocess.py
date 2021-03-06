import os
import darko as dk
import pytest
import sys

SIM_DIR = os.path.abspath('./tests/dummy_results')

@pytest.mark.skipif(sys.version_info < (3, 5), reason="requires python3.5 or higher due to incompatible pickle file in tests.")
def test_read_results_dicts():
    # Using temp dir to ensure that each time a new directory is used
    inputs, results = dk.get_sim_results(path=SIM_DIR, return_status=False, write_excel=False)
    assert isinstance(inputs, dict)
    assert isinstance(results, dict)
