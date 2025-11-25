import errno
import json
import shutil
import subprocess
import logging

from cloudsnake.helpers import ignore_user_entered_signals
from cloudsnake.sdk.aws import App


PLUGIN_NOT_FOUND_MSG = """
Session Manager Plugin not found.

Install it following:
https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html
"""


class SSMStartSessionWrapper(App):
    """Encapsulates Amazon SSM Start Session actions."""

    def __init__(self, client="ssm", session_response_output=None, **kwargs):
        super().__init__(client, **kwargs)
        self.session_response_output = session_response_output
        self.log = logging.getLogger("cloudsnake.ssm")

    def _ensure_plugin_installed(self):
        if shutil.which("session-manager-plugin") is None:
            self.log.error("SessionManagerPlugin not found")
            raise FileNotFoundError(PLUGIN_NOT_FOUND_MSG)

    def start_session_response(self, target: str) -> dict:
        """Start an SSM session and store the response."""
        self.log.debug(f"Calling ssm.start_session(Target='{target}')")

        response = self.client.start_session(
            Target=target,
            Reason="Session started by cloudsnake",
        )
        self.session_response_output = response
        return response

    def start_session(self, target: str):
        """
        Start an SSM session using the session-manager-plugin.
        Uses: self.profile and self.region inherited from App.
        """
        self._ensure_plugin_installed()

        self.log.info(f"Starting SSM session for instance {target}...")
        self.start_session_response(target)

        try:
            with ignore_user_entered_signals():
                subprocess.check_call(
                    [
                        "session-manager-plugin",
                        json.dumps(self.session_response_output),
                        self.region,
                        "StartSession",
                        self.profile,
                        json.dumps({"Target": target}),
                        f"https://ssm.{self.region}.amazonaws.com",
                    ]
                )
            self.log.info("SSM session closed normally")
            return 0

        except subprocess.CalledProcessError as e:
            self.log.error(f"Failed to start SSM session: {e}", exc_info=True)
            self.terminate_session()
            raise

        except OSError as ex:
            if ex.errno == errno.ENOENT:
                self.log.error("SessionManagerPlugin is missing", exc_info=True)
                self.terminate_session()
                raise FileNotFoundError(PLUGIN_NOT_FOUND_MSG) from ex
            else:
                self.log.error("OS error during SSM session", exc_info=True)
                raise

    def terminate_session(self) -> None:
        """Terminate the SSM session."""
        if self.session_response_output and "SessionId" in self.session_response_output:
            session_id = self.session_response_output["SessionId"]
            self.log.debug(f"Terminating SSM session {session_id}")
            self.client.terminate_session(SessionId=session_id)
        else:
            self.log.warning("No active session to terminate")
