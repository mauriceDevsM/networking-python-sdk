# coding: utf-8
# (C) Copyright IBM Corp. 2020.

"""
Integration test code to execute zone firewall access rules api
"""

import os
import unittest
from dotenv import load_dotenv, find_dotenv
from ibm_cloud_networking_services.zone_firewall_access_rules_v1 import ZoneFirewallAccessRulesV1

configFile = "cis.env"

# load the .env file containing your environment variables
try:
    load_dotenv(find_dotenv(filename="cis.env"))
except:
    print('warning: no cis.env file loaded')


class TestZoneFirewallAccessRules(unittest.TestCase):
    """ Test class to call Zone Firewall Access Rules API functions """

    @unittest.skip("skipping")

    def setUp(self):
        if not os.path.exists(configFile):
            raise unittest.SkipTest(
                'External configuration not available, skipping...')

        self.endpoint = os.getenv("API_ENDPOINT")
        self.crn = os.getenv("CRN")
        self.zone_id = os.getenv("ZONE_ID")
        self.rule = ZoneFirewallAccessRulesV1.new_instance(
            crn=self.crn, zone_identifier=self.zone_id, service_name="cis_services")
        self.rule.set_service_url(self.endpoint)

        # list all rules and delete the same for clean up
        self._clean_zone_firewall_rules()

    def tearDown(self):
        """ tear down """
        # Delete the resources
        self._clean_zone_firewall_rules()
        print("Clean up complete")

    def _clean_zone_firewall_rules(self):
        resp = self.rule.list_all_zone_access_rules()
        assert resp is not None
        assert resp.status_code == 200
        for result in resp.get_result().get("result"):
            rule_id = result['id']
            resp = self.rule.delete_zone_access_rule(
                accessrule_identifier=rule_id)
            assert resp is not None
            assert resp.status_code == 200

    def test_1_zone_firewall_rule_mode_action(self):
        i = 0
        modes = {
            "block": "192.168.1.45",
            "challenge": "192.168.1.46",
            "whitelist": "192.168.1.47",
            "js_challenge": "192.168.1.48"
        }
        action = list(modes.keys())
        action_len = len(action)

        for mode, value in modes.items():
            # Create rule
            notes = "This rule is added because of event X that occurred on date xyz"
            configuration = {
                "target": "ip",
                "value": value
            }
            resp = self.rule.create_zone_access_rule(
                mode=mode, notes=notes, configuration=configuration)
            assert resp is not None
            assert resp.status_code == 200
            assert resp.get_result().get("result")["id"] is not None
            rule_id = resp.get_result().get("result")["id"]

            # update rule
            update_mode = action[(i+1) % action_len]
            i = i + 1
            notes = "This rule is updated because of event X that occurred on date xyz"
            resp = self.rule.update_zone_access_rule(
                mode=update_mode, notes=notes, accessrule_identifier=rule_id)
            assert resp is not None
            assert resp.status_code == 200
            assert resp.get_result().get("result")["mode"] == update_mode

            # get rule
            resp = self.rule.get_zone_access_rule(
                accessrule_identifier=rule_id)
            assert resp is not None
            assert resp.status_code == 200
            assert resp.get_result().get("result")["id"] == rule_id

            # delete rule
            resp = self.rule.delete_zone_access_rule(
                accessrule_identifier=rule_id)
            assert resp is not None
            assert resp.status_code == 200
            assert resp.get_result().get("result")["id"] == rule_id

    def test_1_zone_firewall_rule_config_action(self):
        config = {
            "ip": "192.168.1.14",
            "ip_range": "192.169.1.0/24",
            "asn": "AS12345"
        }
        mode = "block"

        for target, value in config.items():
            # Create rule
            notes = "This rule is added because of event X that occurred on date xyz"
            configuration = {
                "target": target,
                "value": value
            }
            resp = self.rule.create_zone_access_rule(
                mode=mode, notes=notes, configuration=configuration)
            assert resp is not None
            assert resp.status_code == 200
            assert resp.get_result().get("result")["id"] is not None
            rule_id = resp.get_result().get("result")["id"]

            # update rule
            update_mode = "challenge"
            notes = "This rule is updated because of event X that occurred on date xyz"
            resp = self.rule.update_zone_access_rule(
                mode=update_mode, notes=notes, accessrule_identifier=rule_id)
            assert resp is not None
            assert resp.status_code == 200
            assert resp.get_result().get("result")["mode"] == update_mode

            # get rule
            resp = self.rule.get_zone_access_rule(
                accessrule_identifier=rule_id)
            assert resp is not None
            assert resp.status_code == 200
            assert resp.get_result().get("result")["id"] == rule_id

            # delete rule
            resp = self.rule.delete_zone_access_rule(
                accessrule_identifier=rule_id)
            assert resp is not None
            assert resp.status_code == 200
            assert resp.get_result().get("result")["id"] == rule_id

    def test_1_zone_firewall_list_rules_action(self):
        modes = {
            "block": "192.168.1.45",
            "challenge": "192.168.1.46",
            "whitelist": "192.168.1.47",
            "js_challenge": "192.168.1.48"
        }
        rule_ids = []

        for mode, value in modes.items():
            # Create rule
            notes = "This rule is added because of event X that occurred on date xyz"
            configuration = {
                "target": "ip",
                "value": value
            }
            resp = self.rule.create_zone_access_rule(
                mode=mode, notes=notes, configuration=configuration)
            assert resp is not None
            assert resp.status_code == 200
            assert resp.get_result().get("result")["id"] is not None
            rule_ids.append(resp.get_result().get("result")["id"])

        # list all rules
        resp = self.rule.list_all_zone_access_rules()
        assert resp is not None
        assert resp.status_code == 200

        for rule_id in rule_ids:
            # delete rule
            resp = self.rule.delete_zone_access_rule(
                accessrule_identifier=rule_id)
            assert resp is not None
            assert resp.status_code == 200
            assert resp.get_result().get("result")["id"] == rule_id


if __name__ == '__main__':
    unittest.main()
