import pandas as pd
import numpy as np
from faker import Faker
from random import randint, choice

fake = Faker()

# -------------------------
# Customers
# -------------------------

customers = []

for i in range(1, 101):
    customers.append({
        "customer_id": 1000 + i,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "country": choice(["NL", "DE", "BE", "FR"]),
        "segment": choice(["Standard","Gold","Premium"]),
        "risk_rating": choice(["LOW","MEDIUM","HIGH"])
    })

customers_df = pd.DataFrame(customers)

customers_df.to_csv(
    "data/sample-data/customers.csv",
    index=False
)

# -------------------------
# Transactions
# -------------------------

transactions = []

for i in range(1, 1001):

    transactions.append({

        "transaction_id": i,

        "customer_id":
            choice(customers_df.customer_id.tolist()),

        "amount":
            round(np.random.uniform(5,15000),2),

        "currency":
            "EUR",

        "country":
            choice(["NL","DE","BE","FR"]),

        "transaction_date":
            fake.date_between(
                start_date="-365d",
                end_date="today"
            )

    })

transactions_df = pd.DataFrame(transactions)

transactions_df.to_csv(
    "data/sample-data/transactions.csv",
    index=False
)

# -------------------------
# Fraud Cases
# -------------------------

fraud_cases = []

for i in range(1,101):

    fraud_cases.append({

        "case_id": f"F{i:04}",

        "customer_id":
            choice(customers_df.customer_id.tolist()),

        "fraud_score":
            randint(50,99),

        "status":
            choice([
                "Open",
                "Investigating",
                "Monitoring",
                "Closed"
            ])

    })

pd.DataFrame(fraud_cases).to_csv(
    "data/sample-data/fraud_cases.csv",
    index=False
)

# -------------------------
# Risk Scores
# -------------------------

risk_scores = []

for cust in customers_df.customer_id:

    risk_scores.append({

        "customer_id": cust,

        "risk_score":
            randint(1,100),

        "exposure":
            randint(10000,500000)

    })

pd.DataFrame(risk_scores).to_csv(
    "data/sample-data/risk_scores.csv",
    index=False
)

print("Sample data created")
