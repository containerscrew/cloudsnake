import errno
import json
import logging
import subprocess

from botocore.config import Config

ERROR_MESSAGE = (
    "SessionManagerPlugin is not found. ",
    "Please refer to SessionManager Documentation here: ",
    "http://docs.aws.amazon.com/console/systems-manager/",
    "Plugin installation: https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html"
    "session-manager-plugin-not-found",
)


class SSM:
    def __init__(self, session, **kwargs):
        self.log = logging.getLogger("cloudsnake")
        self.ssm_client = self.create_ssm_client(session)
        self.kwargs = kwargs

    @staticmethod
    def create_ssm_client(session):
        config = Config(retries={"max_attempts": 10, "mode": "standard"})
        return session.client("ssm", config=config)


class StartSessionWrapper(SSM):
    def __init__(self, session, session_response_output=None, **kwargs):
        # Inheriting the properties of parent class
        super().__init__(session, **kwargs)
        self.session_response_output = session_response_output

    def start_session_response(self) -> None:
        """
            Start an SSM session and store the response.
        """
        target = self.kwargs.get("target")
        reason = self.kwargs.get("reason")
        response = self.ssm_client.start_session(
            Target=target,
            Reason=reason,
        )
        self.session_response_output = response

    def start_session(self, region: str, profile: str):
        """
           Start an SSM session using the session-manager-plugin.
           :param region: AWS region
           :param profile: AWS profile
           :return: 0 if successful, raises an error otherwise
       """
        self.start_session_response()
        target = self.kwargs.get("target")
        try:
            subprocess.check_call(
                [
                    "session-manager-plugin",
                    json.dumps(self.session_response_output),
                    region,
                    "StartSession",
                    profile,
                    json.dumps(dict(Target=target)),
                    f"https://ssm.{region}.amazonaws.com",
                ]
            )
            return 0
        except subprocess.CalledProcessError as e:
            self.log.error("Failed to start session", exc_info=True)
            print(f"Failed to start session: {e}")
            self.terminate_session()
            raise
        except OSError as ex:
            if ex.errno == errno.ENOENT:
                self.log.error("SessionManagerPlugin is not present", exc_info=True)
                print("SessionManagerPlugin is not present")
                self.terminate_session()
                raise ValueError("SessionManagerPlugin is not present") from ex
            else:
                self.log.error("OS error", exc_info=True)
                raise

    def terminate_session(self) -> None:
        """
        Terminate the SSM session.
        """
        if self.session_response_output and "SessionId" in self.session_response_output:
            self.ssm_client.terminate_session(SessionId=self.session_response_output["SessionId"])
        else:
            self.log.warning("No active session to terminate")