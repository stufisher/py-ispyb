import pytest

from starlette.types import ASGIApp

from tests.conftest import AuthClient
from tests.core.api.utils.apitest import get_elem_name, run_test, ApiTestElem

from tests.core.api.data.proposals import (
    test_data_proposal_list,
    test_data_proposal_info,
)


@pytest.mark.parametrize("test_elem", test_data_proposal_list, ids=get_elem_name)
def test_proposal_list(auth_client: AuthClient, test_elem: ApiTestElem, app: ASGIApp):
    run_test(auth_client, test_elem, app)


@pytest.mark.parametrize("test_elem", test_data_proposal_info, ids=get_elem_name)
def test_proposal_info(auth_client: AuthClient, test_elem: ApiTestElem, app: ASGIApp):
    run_test(auth_client, test_elem, app)
