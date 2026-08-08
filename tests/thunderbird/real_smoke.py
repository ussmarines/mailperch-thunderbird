#!/usr/bin/env python3
"""Launch a real Thunderbird binary through geckodriver and smoke-test MailPerch.

This harness deliberately uses only Python's standard library.  It is a
release-binary smoke test, not a replacement for Thunderbird's own mach
xpcshell/mochitest harness.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import pathlib
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any

ADDON_ID = "pin-mails@MailPerch.local"
PANEL_ID = "pin-mails-panel"
TOGGLE_ID = "pin-mails-qfb-toggle"


class SmokeFailure(RuntimeError):
    pass


@dataclass
class WebDriverClient:
    host: str
    port: int
    timeout: float = 30.0
    session_id: str | None = None

    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}"

    def request(self, method: str, path: str, payload: Any | None = None) -> Any:
        data = None
        headers = {"Accept": "application/json"}
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json; charset=utf-8"
        request = urllib.request.Request(
            f"{self.base_url}{path}", data=data, headers=headers, method=method
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                raw = response.read()
        except urllib.error.HTTPError as error:
            raw = error.read()
            detail = raw.decode("utf-8", "replace")[:4000]
            raise SmokeFailure(
                f"WebDriver {method} {path} failed with HTTP {error.code}: {detail}"
            ) from error
        except OSError as error:
            raise SmokeFailure(f"WebDriver {method} {path} failed: {error}") from error
        if not raw:
            return None
        parsed = json.loads(raw)
        if isinstance(parsed, dict) and isinstance(parsed.get("value"), dict):
            value = parsed["value"]
            if value.get("error"):
                raise SmokeFailure(
                    f"WebDriver {method} {path} failed: {value.get('error')}: "
                    f"{value.get('message', '')}"
                )
        return parsed

    def wait_ready(self, deadline: float) -> None:
        last_error: Exception | None = None
        while time.monotonic() < deadline:
            try:
                response = self.request("GET", "/status")
                value = (response or {}).get("value", {})
                if value.get("ready") is True:
                    return
            except Exception as error:  # startup race only
                last_error = error
            time.sleep(0.25)
        raise SmokeFailure(f"geckodriver did not become ready: {last_error}")

    def new_session(self, binary: pathlib.Path) -> dict[str, Any]:
        payload = {
            "capabilities": {
                "alwaysMatch": {
                    "browserName": "firefox",
                    "acceptInsecureCerts": True,
                    "moz:firefoxOptions": {
                        "binary": str(binary),
                        "prefs": {
                            "app.update.auto": False,
                            "app.update.enabled": False,
                            "browser.shell.checkDefaultBrowser": False,
                            "mail.provider.enabled": False,
                            "mail.shell.checkDefaultClient": False,
                            "mailnews.start_page.enabled": False,
                            "toolkit.telemetry.enabled": False,
                        },
                    },
                }
            }
        }
        response = self.request("POST", "/session", payload)
        value = (response or {}).get("value", {})
        session_id = value.get("sessionId") or (response or {}).get("sessionId")
        if not session_id:
            raise SmokeFailure(f"WebDriver session id missing: {response}")
        self.session_id = str(session_id)
        return value.get("capabilities", {})

    def _session_path(self, suffix: str) -> str:
        if not self.session_id:
            raise SmokeFailure("WebDriver session has not been created")
        return f"/session/{self.session_id}{suffix}"

    def set_context(self, context: str) -> None:
        self.request("POST", self._session_path("/moz/context"), {"context": context})

    def install_addon(self, xpi: pathlib.Path) -> str:
        response = self.request(
            "POST",
            self._session_path("/moz/addon/install"),
            {"path": str(xpi), "temporary": True},
        )
        addon_id = (response or {}).get("value")
        if addon_id != ADDON_ID:
            raise SmokeFailure(f"Unexpected add-on id: {addon_id!r}")
        return addon_id

    def uninstall_addon(self, addon_id: str) -> None:
        self.request(
            "POST", self._session_path("/moz/addon/uninstall"), {"id": addon_id}
        )

    def execute_async(self, script: str, args: list[Any] | None = None) -> Any:
        response = self.request(
            "POST",
            self._session_path("/execute/async"),
            {"script": script, "args": args or []},
        )
        value = (response or {}).get("value")
        if isinstance(value, dict) and value.get("__mailperchSmokeError"):
            raise SmokeFailure(f"Chrome script failed: {value['__mailperchSmokeError']}")
        return value

    def full_screenshot(self) -> bytes | None:
        try:
            response = self.request("GET", self._session_path("/moz/screenshot/full"))
            encoded = (response or {}).get("value")
            if isinstance(encoded, str) and encoded:
                return base64.b64decode(encoded)
        except Exception:
            return None
        return None

    def delete_session(self) -> None:
        if not self.session_id:
            return
        try:
            self.request("DELETE", self._session_path(""))
        finally:
            self.session_id = None


RUNTIME_STATE_SCRIPT = r"""
const done = arguments[arguments.length - 1];
(async () => {
const { AddonManager } = ChromeUtils.importESModule(
  "resource://gre/modules/AddonManager.sys.mjs"
);
const { classes: Cc, interfaces: Ci } = Components;
const windowMediator = Cc["@mozilla.org/appshell/window-mediator;1"].getService(
  Ci.nsIWindowMediator
);
const addon = await AddonManager.getAddonByID("pin-mails@MailPerch.local");
const windows = [];
for (const win of windowMediator.getEnumerator("mail:3pane")) {
  windows.push(win);
}
const panes = [];
for (const win of windows) {
  const candidates = new Set();
  try {
    const current = win.document.getElementById("tabmail")?.currentAbout3Pane;
    if (current) candidates.add(current);
  } catch {}
  try {
    for (const browser of win.document.querySelectorAll("browser")) {
      const pane = browser.contentWindow;
      if (pane?.location?.href === "about:3pane") candidates.add(pane);
    }
  } catch {}
  for (const pane of candidates) {
    try {
      if (pane?.location?.href !== "about:3pane") continue;
      panes.push({
        href: pane.location.href,
        ready: Boolean(
          pane.document?.getElementById("threadTree") &&
          pane.gViewWrapper &&
          pane.quickFilterBar
        ),
        panel: Boolean(pane.document?.getElementById("pin-mails-panel")),
        toggle: Boolean(pane.document?.getElementById("pin-mails-qfb-toggle")),
        panelCount: pane.document?.querySelectorAll("#pin-mails-panel")?.length || 0,
        toggleCount: pane.document?.querySelectorAll("#pin-mails-qfb-toggle")?.length || 0,
      });
    } catch (error) {
      panes.push({error: String(error?.name || error)});
    }
  }
}
done({
  addon: addon ? {
    id: addon.id,
    active: Boolean(addon.isActive),
    version: String(addon.version || ""),
    temporarilyInstalled: Boolean(addon.temporarilyInstalled),
  } : null,
  windowCount: windows.length,
  panes,
});
})().catch(error => done({
  __mailperchSmokeError: [
    `${String(error?.name || "Error")}: ${String(error?.message || error)}`,
    String(error?.stack || ""),
  ].filter(Boolean).join("\n"),
}));
"""


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _validate_path(path: str, label: str, executable: bool = False) -> pathlib.Path:
    resolved = pathlib.Path(path).expanduser().resolve()
    if not resolved.is_file():
        raise SmokeFailure(f"{label} does not exist: {resolved}")
    if executable and not os.access(resolved, os.X_OK):
        raise SmokeFailure(f"{label} is not executable: {resolved}")
    return resolved


def _wait_for_state(
    client: WebDriverClient,
    predicate,
    description: str,
    timeout: float,
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout
    last: dict[str, Any] = {}
    while time.monotonic() < deadline:
        value = client.execute_async(RUNTIME_STATE_SCRIPT)
        if isinstance(value, dict):
            last = value
            if predicate(value):
                return value
        time.sleep(0.5)
    raise SmokeFailure(
        f"Timed out waiting for {description}. Last runtime state: "
        f"{json.dumps(last, ensure_ascii=False, sort_keys=True)}"
    )


def _panel_is_ready(state: dict[str, Any]) -> bool:
    addon = state.get("addon") or {}
    panes = state.get("panes") or []
    return bool(
        addon.get("active")
        and addon.get("id") == ADDON_ID
        and any(
            pane.get("ready")
            and pane.get("panel")
            and pane.get("toggle")
            and pane.get("panelCount") == 1
            and pane.get("toggleCount") == 1
            for pane in panes
            if isinstance(pane, dict)
        )
    )


def _panel_is_cleaned(state: dict[str, Any]) -> bool:
    addon = state.get("addon")
    panes = state.get("panes") or []
    return addon is None and all(
        not pane.get("panel") and not pane.get("toggle")
        for pane in panes
        if isinstance(pane, dict)
    )


def _write_json(path: pathlib.Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run(args: argparse.Namespace) -> int:
    binary = _validate_path(args.binary, "Thunderbird binary", executable=True)
    xpi = _validate_path(args.xpi, "MailPerch XPI")
    geckodriver = _validate_path(args.geckodriver, "geckodriver", executable=True)
    output_dir = pathlib.Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    gecko_log = output_dir / "geckodriver.log"
    result_path = output_dir / "result.json"

    port = _free_port()
    client = WebDriverClient("127.0.0.1", port, timeout=max(10.0, args.timeout))
    process: subprocess.Popen[str] | None = None
    result: dict[str, Any] = {
        "status": "failed",
        "binary": str(binary),
        "xpi": str(xpi),
        "geckodriver": str(geckodriver),
        "port": port,
        "checks": [],
    }

    try:
        with gecko_log.open("w", encoding="utf-8") as log_handle:
            process = subprocess.Popen(
                [
                    str(geckodriver),
                    "--host",
                    "127.0.0.1",
                    "--port",
                    str(port),
                    "--allow-system-access",
                    "--log",
                    "trace",
                ],
                stdout=log_handle,
                stderr=subprocess.STDOUT,
                text=True,
            )
            client.wait_ready(time.monotonic() + args.timeout)
            result["checks"].append("geckodriver-ready")

            capabilities = client.new_session(binary)
            result["capabilities"] = capabilities
            result["checks"].append("thunderbird-webdriver-session")

            client.set_context("chrome")
            result["checks"].append("chrome-context")

            addon_id = client.install_addon(xpi)
            result["checks"].append("temporary-addon-install")

            first = _wait_for_state(
                client,
                _panel_is_ready,
                "MailPerch panel injection",
                args.timeout,
            )
            result["firstInstall"] = first
            result["checks"].append("panel-and-toggle-injected-once")
            screenshot = client.full_screenshot()
            if screenshot:
                (output_dir / "mailperch-installed.png").write_bytes(screenshot)

            client.uninstall_addon(addon_id)
            cleaned = _wait_for_state(
                client,
                _panel_is_cleaned,
                "MailPerch runtime cleanup after temporary uninstall",
                args.timeout,
            )
            result["afterUninstall"] = cleaned
            result["checks"].append("runtime-cleanup-after-uninstall")

            client.install_addon(xpi)
            reinstalled = _wait_for_state(
                client,
                _panel_is_ready,
                "MailPerch panel reinjection after reinstall",
                args.timeout,
            )
            result["afterReinstall"] = reinstalled
            result["checks"].append("clean-reinstall")
            screenshot = client.full_screenshot()
            if screenshot:
                (output_dir / "mailperch-reinstalled.png").write_bytes(screenshot)

            result["status"] = "passed"
            _write_json(result_path, result)
            print("Real Thunderbird runtime smoke: OK")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return 0
    except Exception as error:
        result["error"] = f"{type(error).__name__}: {error}"
        _write_json(result_path, result)
        print(f"Real Thunderbird runtime smoke: FAILED: {error}", file=sys.stderr)
        return 1
    finally:
        try:
            client.delete_session()
        except Exception:
            pass
        if process is not None:
            try:
                process.terminate()
                process.wait(timeout=10)
            except Exception:
                try:
                    process.kill()
                except Exception:
                    pass
        if not result_path.exists():
            _write_json(result_path, result)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", required=True, help="Path to the Thunderbird executable")
    parser.add_argument("--xpi", required=True, help="Path to the MailPerch XPI")
    parser.add_argument("--geckodriver", required=True, help="Path to geckodriver")
    parser.add_argument("--output-dir", default="artifacts/thunderbird-smoke")
    parser.add_argument("--timeout", type=float, default=45.0)
    return parser.parse_args()


if __name__ == "__main__":
    raise SystemExit(run(parse_args()))
