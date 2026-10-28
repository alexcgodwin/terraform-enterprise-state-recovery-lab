import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class ContractTests(unittest.TestCase):
    def test_address_rename_contract(self):
        a=(ROOT/'labs/state-move/before/main.tf').read_text()
        b=(ROOT/'labs/state-move/after/main.tf').read_text()
        self.assertIn('terraform_data" "legacy',a)
        self.assertIn('terraform_data" "service',b)
        self.assertEqual(a.count('resource "terraform_data"'),b.count('resource "terraform_data"'))

    def test_no_cloud_backend_in_sandbox_fixtures(self):
        for f in (ROOT/'labs').rglob('*.tf'):
            body=f.read_text()
            self.assertNotIn('backend "s3"',body)
            self.assertNotIn('provider "aws"',body)

    def test_import_example_has_required_provider(self):
        body=(ROOT/'labs/import/main.tf').read_text()
        self.assertIn('hashicorp/random',body)
        self.assertIn('random_id" "existing',body)

if __name__=='__main__':unittest.main()
