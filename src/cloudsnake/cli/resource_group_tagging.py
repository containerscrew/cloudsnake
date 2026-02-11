# import typer
#
# resource_group_taging = typer.Typer(
#     no_args_is_help=True,
#     pretty_exceptions_short=True,
#     pretty_exceptions_show_locals=False,
# )
#
#
# @resource_group_taging.command(
#     "get-resources", help="Get resources from Resource Group Tagging API"
# )
# @handle_aws_errors
# def get_resources(
#     ctx: typer.Context,
# ):
#     signal.signal(signal.SIGINT, signal_handler)
#     resource_group_tagging_wrapper = ResourceGroupTaggingWrapper(
#         session=ctx.obj.session,
#         profile=ctx.obj.profile,
#         region=ctx.obj.region,
#     )
#
#     console.print("Nothing to do")
