ERROR_MESSAGE = (
    "SessionManagerPlugin is not found. ",
    "Please refer to SessionManager Documentation here: ",
    "http://docs.aws.amazon.com/console/systems-manager/",
    "Plugin installation: https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html"
    "session-manager-plugin-not-found",
)


# class SSMSession:
#     def __init__(self, session, target_id, region, profile, logger):
#         self.start_session_response = None
#         self.client = ssm_client(session)
#         self.target_id = target_id
#         self.region = region
#         self.profile = profile
#         self.logger = logger
#
#     def __start_session_response(self):
#         response = self.client.start_session(
#             Target=self.target_id,
#             Reason="ssm-connection",
#         )
#         self.start_session_response = response
#
#     def start_session(self):
#         self.__start_session_response()
#         try:
#             subprocess.check_call(
#                 [
#                     "session-manager-plugin",
#                     json.dumps(self.start_session_response),
#                     self.region,
#                     "StartSession",
#                     self.profile,
#                     json.dumps(dict(Target=self.target_id)),
#                     f"https://ssm.{self.region}.amazonaws.com",
#                 ]
#             )
#             return 0
#         except OSError as ex:
#             if ex.errno == errno.ENOENT:
#                 self.logger.debug("SessionManagerPlugin is not present", exc_info=True)
#                 print("SessionManagerPlugin is not present")
#                 self.client.terminate_session(
#                     SessionId=self.start_session_response["SessionId"]
#                 )
#                 raise ValueError("".join(ERROR_MESSAGE))
