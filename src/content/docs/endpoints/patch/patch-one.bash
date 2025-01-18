curl -X PATCH http://127.0.0.1:5000/financial-portfolio/4567 \
-H "x-api-host: finance-data.api.com" \
-H "x-api-key: YOUR_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "new_balance": 60000
}'
