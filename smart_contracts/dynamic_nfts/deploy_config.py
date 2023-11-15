import logging
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
import algokit_utils
from contract import DynamicNFT  # Import the Dynamic NFT contract

logger = logging.getLogger(__name__)


def deploy(
    algod_client: AlgodClient,
    indexer_client: IndexerClient,
    app_spec: algokit_utils.ApplicationSpecification,
    deployer: algokit_utils.Account,
) -> None:
    # Create an instance of the DynamicNFT client
    app_client = algokit_utils.ApplicationClient(
        algod_client,
        DynamicNFT(),  # Initialize your Dynamic NFT contract
        creator=deployer.address,
        signer=deployer.signer,  # Assuming your Account class has a signer method
        indexer_client=indexer_client,
    )

    # Deploy the Dynamic NFT application
    app_client.deploy(
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
        on_update=algokit_utils.OnUpdate.AppendApp,
    )

    # Log deployment details
    logger.info(
        f"Deployed Dynamic NFT Contract {app_spec.contract.name} "
        f"with App ID: {app_client.app_id}"
    )


# Example usage
if __name__ == "__main__":
    # Setup Algod and Indexer clients
    algod_client = AlgodClient("api-token", "http://localhost:4001")
    indexer_client = IndexerClient("indexer-token", "http://localhost:8980")

    # Define the deployer account (adjust with actual account details)
    deployer = algokit_utils.Account.from_mnemonic(
        "your 25-word mnemonic here")

    # Define application specification (adjust as per your setup)
    app_spec = algokit_utils.ApplicationSpecification(
        contract=algokit_utils.Contract(name="DynamicNFT")
    )

    # Deploy the application
    deploy(algod_client, indexer_client, app_spec, deployer)
