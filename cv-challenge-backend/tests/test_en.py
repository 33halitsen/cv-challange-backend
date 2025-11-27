import unittest
from unittest.mock import patch, MagicMock
import json  # json modülünü burada import etmelisin
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import VisitorCounter_English

class TestLambdaFunction(unittest.TestCase):

    @patch('VisitorCounter_English.boto3.resource')
    def test_lambda_handler(self, mock_boto_resource):
        # Mock table ve update_item sonucu
        mock_table = MagicMock()
        mock_table.update_item.return_value = {
            'Attributes': {
                'visit_count': 5
            }
        }

        # Mock DynamoDB resource'un table fonksiyonu mock_table döndürsün
        mock_dynamodb = MagicMock()
        mock_dynamodb.Table.return_value = mock_table
        mock_boto_resource.return_value = mock_dynamodb

        # Event ve context sahte parametreleri
        fake_event = {}
        fake_context = {}

        # Lambda fonksiyonunu çağır
        result = VisitorCounter_English.lambda_handler(fake_event, fake_context)

        # Beklenen sonucu test et
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(json.loads(result['body'])['visit_count'], 5)
        self.assertEqual(result['headers']['Access-Control-Allow-Origin'], '*')

        # update_item'ın doğru şekilde çağrılıp çağrılmadığını kontrol et
        mock_table.update_item.assert_called_once_with(
            Key={'id': 'visitor_count_english'},
            UpdateExpression='ADD visit_count :inc',
            ExpressionAttributeValues={':inc': 1},
            ReturnValues='UPDATED_NEW'
        )

if __name__ == '__main__':
    unittest.main()