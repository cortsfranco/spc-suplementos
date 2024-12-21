import pytest
from app.utils.security import check_rate_limit, verify_webhook_signature
from unittest.mock import patch, MagicMock

def test_rate_limit():
    with patch('app.utils.security.redis_client') as mock_redis:
        mock_redis.get.return_value = None
        assert check_rate_limit('127.0.0.1') == True
        
        mock_redis.get.return_value = b'99'
        assert check_rate_limit('127.0.0.1') == True
        
        mock_redis.get.return_value = b'100'
        assert check_rate_limit('127.0.0.1') == False

def test_webhook_signature():
    with patch('hmac.compare_digest') as mock_compare:
        mock_compare.return_value = True
        
        @verify_webhook_signature('secret')
        def test_func():
            return 'success'
            
        with patch('flask.request') as mock_request:
            mock_request.headers = {'X-Hub-Signature': 'sha1=hash'}
            mock_request.get_data.return_value = b'test data'
            
            assert test_func() == 'success' 