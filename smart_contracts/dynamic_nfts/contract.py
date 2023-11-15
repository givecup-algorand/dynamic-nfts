from beaker import Application, GlobalStateValue
from pyteal import Seq, Txn, TxnType, TxnField, Int, Bytes, abi, TealType, Approve, Expr, InnerTxnBuilder, InnerTxn, Assert


class GlobalState:
    # Define global state for asset id and owner
    asset_id = GlobalStateValue(stack_type=TealType.uint64, default=Int(0))
    owner = GlobalStateValue(stack_type=TealType.bytes, default=Bytes(""))
    accessory_id = GlobalStateValue(stack_type=TealType.uint64, default=Int(0))
    case_id = GlobalStateValue(stack_type=TealType.uint64, default=Int(0))


app = Application("DynamicNFT", state=GlobalState())


@app.create
def create():
    return Seq(
        # Create the NFT (ASA) with total supply of 1
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.AssetConfig,
            TxnField.config_asset_total: Int(1),
            TxnField.config_asset_decimals: Int(0),
            TxnField.config_asset_unit_name: Bytes("UNIQUE"),
            TxnField.config_asset_name: Bytes("DynamicNFT"),
            TxnField.config_asset_url: Bytes("https://initial.url"),
        }),
        InnerTxnBuilder.Submit(),

        # Store the created asset id and owner in global state
        app.state.asset_id.set(InnerTxn.created_asset_id()),
        app.state.owner.set(Txn.sender()),

        Approve()
    )


@app.external
def update_url(v: abi.String) -> Expr:
    # Only the owner can update the URL
    return Seq(
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.AssetConfig,
            # TxnField.config_asset_id: app.state.asset_id,
            TxnField.config_asset_url: v.get(),
        }),
        InnerTxnBuilder.Submit(),
        Approve()
    )


@app.external
def integrate_accessory(accessory_id: abi.Uint64) -> Expr:
    # Verify ownership and attach accessory to Cup NFT
    return Seq(
        Assert(Txn.sender() == app.state.owner),
        app.state.accessory_id.set(accessory_id.get()),
        Approve()
    )


@app.external
def open_case(case_id: abi.Uint64) -> Expr:
    # Logic to open a Case NFT
    return Seq(
        Assert(Txn.sender() == app.state.owner),
        # logic for opening case and generating NFT
        Approve()
    )


@app.external(read_only=True)
def get_asset_id(*, output: abi.Uint64) -> Expr:
    return output.set(app.state.asset_id)
