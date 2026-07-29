import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ERPIntegrationTest(unittest.TestCase):
    def test_small_database_generation_and_validation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "test.sqlite"
            subprocess.run(
                [
                    sys.executable, str(ROOT / "generate_erp.py"),
                    "--output", str(database),
                    "--customers", "30",
                    "--vendors", "20",
                    "--invoices", "100",
                    "--payments", "50",
                    "--journals", "40",
                    "--seed", "17",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            result = subprocess.run(
                [
                    sys.executable, str(ROOT / "validate_erp.py"),
                    "--database", str(database),
                    "--customers", "30",
                    "--vendors", "20",
                    "--invoices", "100",
                    "--payments", "50",
                    "--journal-entries", "40",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
