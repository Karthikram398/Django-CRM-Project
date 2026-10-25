"""Offline regression checks for deployment-supplied credentials."""
import ast
import os
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

SETTINGS = Path(__file__).resolve().parents[1] / "crm_main" / "settings.py"


class SecurityConfigurationTests(unittest.TestCase):
    def load_settings(self, environment, local_override=None):
        messages = types.ModuleType("django.contrib.messages")
        messages.constants = types.SimpleNamespace(DEBUG=10, INFO=20, SUCCESS=25, WARNING=30, ERROR=40)
        modules = {"django": types.ModuleType("django"),
                   "django.contrib": types.ModuleType("django.contrib"),
                   "django.contrib.messages": messages}
        if local_override is not None:
            local = types.ModuleType("crm_main.local_settings")
            local.SECRET_KEY = local_override
            modules["crm_main.local_settings"] = local
        namespace = {"__file__": str(SETTINGS), "__name__": "security_fixture"}
        with patch.dict(os.environ, environment, clear=True), patch.dict(sys.modules, modules):
            exec(compile(SETTINGS.read_text(), str(SETTINGS), "exec"), namespace)
        return namespace

    def test_no_literal_secret_assignments(self):
        nodes = ast.walk(ast.parse(SETTINGS.read_text()))
        secrets = {"SECRET_KEY", "SOCIAL_AUTH_FACEBOOK_SECRET"}
        for node in nodes:
            if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in secrets for t in node.targets):
                self.assertFalse(isinstance(node.value, ast.Constant), "Credential must not be hardcoded")

    def test_missing_or_empty_credentials_fail_closed(self):
        good = {"DJANGO_SECRET_KEY": "synthetic-signing-key", "SOCIAL_AUTH_FACEBOOK_SECRET": "synthetic-oauth-secret"}
        for name in good:
            missing = dict(good)
            missing.pop(name)
            with self.subTest(name=name, state="missing"), self.assertRaises(KeyError):
                self.load_settings(missing)
            for empty in ("", "   "):
                with self.subTest(name=name, state="empty"), self.assertRaises(ValueError):
                    self.load_settings({**good, name: empty})

    def test_environment_is_authoritative_over_local_settings(self):
        settings = self.load_settings(
            {"DJANGO_SECRET_KEY": "synthetic-new-key", "SOCIAL_AUTH_FACEBOOK_SECRET": "synthetic-new-oauth"},
            local_override="synthetic-old-key")
        self.assertEqual(settings["SECRET_KEY"], "synthetic-new-key")
        self.assertEqual(settings["SOCIAL_AUTH_FACEBOOK_SECRET"], "synthetic-new-oauth")


if __name__ == "__main__":
    unittest.main()
