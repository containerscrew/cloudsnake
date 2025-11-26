from __future__ import annotations

import errno
import json
import shutil
import subprocess
import logging
from typing import Optional, Dict, Any

from cloudsnake.helpers import ignore_user_entered_signals
from cloudsnake.sdk.aws import App


PLUGIN_NOT_FOUND_MSG = """
Session Manager Plugin not found.
https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html
"""


class SSMStartSessionWrapper(App):
    def __init__(
        self,
        session_response_output: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.session_response_output = session_response_output
        self.log = logging.getLogger("cloudsnake.ssm")

    @property
    def client_name(self) -> str:
        return "ssm"

    def _ensure_plugin_installed(self):
        if shutil.which("session-manager-plugin") is None:
            raise FileNotFoundError(PLUGIN_NOT_FOUND_MSG)

    def start_session_response(self, target: str) -> Dict[str, Any]:
        self.log.debug(f"ssm.start_session(Target={target})")
        res = self.client.start_session(Target=target, Reason="cloudsnake session")
        self.session_response_output = res
        return res

    def start_session(self, target: str):
        self._ensure_plugin_installed()
        self.log.info(f"Starting SSM session for {target}")
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
            self.log.info("Session closed cleanly")
            return 0

        except subprocess.CalledProcessError as e:
            self.log.error(f"SSM session failed: {e}")
            self.terminate_session()
            raise

        except OSError as ex:
            if ex.errno == errno.ENOENT:
                self.terminate_session()
                raise FileNotFoundError(PLUGIN_NOT_FOUND_MSG) from ex
            else:
                self.log.error("OS error during SSM session", exc_info=True)
                raise

    def terminate_session(self) -> None:
        if self.session_response_output and "SessionId" in self.session_response_output:
            sid = self.session_response_output["SessionId"]
            self.log.debug(f"terminate_session {sid}")
            self.client.terminate_session(SessionId=sid)
        else:
            self.log.warning("No session to terminate")
