import unittest
from payments.payment_module import MpesaPayment

class TestMpesaPayment(unittest.TestCase):

    def setUp(self):
        self.mpesa = MpesaPayment()

    def test_validate_payment_details(self):
        self.assertTrue(self.mpesa.validate_payment_details("254712345678", 100))
        self.assertFalse(self.mpesa.validate_payment_details("254712345678", -100))
        self.assertFalse(self.mpesa.validate_payment_details("123456789", 100))

    def test_is_duplicate_transaction(self):
        # This test would require a mock or a test database setup
        self.assertFalse(self.mpesa.is_duplicate_transaction("test_transaction_id"))

    def test_initiate_payment(self):
        # This test would require mocking the API call
        response = self.mpesa.initiate_payment("254712345678", 100, "https://yourdomain.com/mpesa/callback/", "test_transaction_id")
        self.assertIn("error", response)  # Expecting an error due to mock

if __name__ == "__main__":
    unittest.main()
