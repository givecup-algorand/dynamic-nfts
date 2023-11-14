import pytest
from algokit_utils import (
    ApplicationClient,
    ApplicationSpecification,
    get_localnet_default_account,
)
from algosdk.v2client.algod import AlgodClient

from smart_contracts.dynamic_nfts import contract as dynamic_nfts_contract


@pytest.fixture(scope="session")
def dynamic_nfts_app_spec(algod_client: AlgodClient) -> ApplicationSpecification:
    return dynamic_nfts_contract.app.build(algod_client)


@pytest.fixture(scope="session")
def dynamic_nfts_client(
    algod_client: AlgodClient, dynamic_nfts_app_spec: ApplicationSpecification
) -> ApplicationClient:
    client = ApplicationClient(
        algod_client,
        app_spec=dynamic_nfts_app_spec,
        signer=get_localnet_default_account(algod_client),
    )
    client.create()
    return client


def test_says_hello(dynamic_nfts_client: ApplicationClient) -> None:
    result = dynamic_nfts_client.call(dynamic_nfts_contract.hello, name="World")

    assert result.return_value == "Hello, World"
