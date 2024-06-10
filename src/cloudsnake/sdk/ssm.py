import errno
import json
import logging
import subprocess
from botocore.config import Config
from rich import print


ERROR_MESSAGE = (
    "SessionManagerPlugin is not found. ",
    "Please refer to SessionManager Documentation here: ",
    "http://docs.aws.amazon.com/console/systems-manager/",
    "Plugin installation: https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html"
    "session-manager-plugin-not-found",
)


class SSMStartSessionWrapper:
    def __init__(self, ssm_client, session_response_output=None, **kwargs):
        self.log = logging.getLogger("cloudsnake")
        self.session_response_output = session_response_output
        self.reason = kwargs.get("reason")
        self.ssm_client = ssm_client

    @classmethod
    def from_session(cls, session, **kwargs):
        config = Config(retries={"max_attempts": 10, "mode": "standard"})
        ssm_client = session.client("ssm", config=config)
        return cls(ssm_client, **kwargs)

    def start_session_response(self, target: str) -> None:
        """
        Start an SSM session and store the response.
        """
        response = self.ssm_client.start_session(
            Target=target,
            Reason=self.reason,
        )
        self.session_response_output = response

    def start_session(self, target: str, region: str, profile: str):
        """
        Start an SSM session using the session-manager-plugin.
        :param region: AWS region
        :param profile: AWS profile
        :return: 0 if successful, raises an error otherwise
        """
        self.start_session_response(target)
        try:
            print(
                f"[bold green]Connecting to the instance:[/bold green] {target} [red]Please wait[/red]:) :rocket:"
            )
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
            self.log.error(f"Failed to start session: {e}")
            self.terminate_session()
            raise
        except OSError as ex:
            if ex.errno == errno.ENOENT:
                self.log.error("SessionManagerPlugin is not present", exc_info=True)
                self.log.warning("SessionManagerPlugin is not present")
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
            self.ssm_client.terminate_session(
                SessionId=self.session_response_output["SessionId"]
            )
        else:
            self.log.warning("No active session to terminate")