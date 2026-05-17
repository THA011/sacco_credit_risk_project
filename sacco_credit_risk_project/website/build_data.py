import json
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
RAW_FILE = BASE_DIR.parent / 'data' / 'raw' / 'Risk Classification of Assets and Provisioning (3).xlsx'
SHEET_NAME = 'Risk Classification of Assets a'
OUTPUT_FILE = BASE_DIR / 'data' / 'members.json'

LOAN_COLUMNS = {
    'Full Account': 'account_id',
    'Full Name': 'full_name',
    'Member No': 'member_no',
    'Mobile No': 'mobile_no',
    'Loan Name': 'loan_name',
    'Employer ': 'employer',
    'Loan Amount': 'loan_amount',
    'Loanserial': 'loan_serial',
    'Repayment Per Month': 'repayment_per_month',
    'Date \nLoan Given': 'loan_given_date',
    'Loan Term ': 'loan_term_months',
    'Loan Amortization Type': 'amortization_type',
    'Balance': 'balance',
    'Loan Balance Expected': 'loan_balance_expected',
    'Actual Balance  ': 'actual_balance',
    'Expected Interest Paid': 'expected_interest_paid',
    'Interest balance': 'interest_balance',
    'Latest Amount Paid': 'latest_amount_paid',
    'Latest Paid Date': 'latest_paid_date',
    'Loan Arrears': 'loan_arrears',
    'Days in Arrears': 'days_in_arrears',
    'Annual  % Rate': 'annual_rate',
    ' Classification ': 'classification',
    'Loan Loss Provision Amount': 'loan_loss_provision',
    'Loan Maturity': 'loan_maturity',
    'Members Deposits': 'members_deposits'
}

LOAN_TYPE_RATES = {
    'Normal Loan': {'monthly': 1.0, 'annual': 12.0},
    'Emergency Loan': {'monthly': 1.3, 'annual': 15.6},
    'School Fees Loan': {'monthly': 1.15, 'annual': 13.8},
    'M-Cash Loan': {'monthly': 5.0, 'annual': 60.0},
    'Super Loan': {'monthly': 1.2, 'annual': 14.4}
}


def clean_mobile(value):
    if pd.isna(value):
        return None
    raw = str(int(value)) if isinstance(value, float) and value == int(value) else str(value)
    raw = raw.strip()
    if raw.startswith('+'):
        return raw
    if raw.startswith('254'):
        return '+' + raw
    if raw.startswith('0'):
        return '+254' + raw[1:]
    return raw


def clean_member_no(value):
    if pd.isna(value):
        return None
    raw = str(value).strip()
    if raw.isdigit():
        return raw.zfill(6)
    return raw


def normalize_date(value):
    if pd.isna(value):
        return None
    if hasattr(value, 'isoformat'):
        return value.isoformat()
    return str(value)


def build():
    workbook = pd.read_excel(RAW_FILE, sheet_name=SHEET_NAME, header=14)
    rows = []
    for _, row in workbook.iterrows():
        account_id = str(row.get('Full Account')).strip() if not pd.isna(row.get('Full Account')) else None
        if not account_id or account_id.lower() == 'performing' or account_id.lower() == 'nan':
            continue
        member_no = clean_member_no(row.get('Member No'))
        if not member_no or member_no.lower() == 'member no':
            continue
        record = {
            'account_id': account_id,
            'full_name': str(row.get('Full Name')).strip() if not pd.isna(row.get('Full Name')) else None,
            'member_no': member_no,
            'mobile_no': clean_mobile(row.get('Mobile No')),
            'loan_name': str(row.get('Loan Name')).strip() if not pd.isna(row.get('Loan Name')) else None,
            'employer': str(row.get('Employer ')).strip() if not pd.isna(row.get('Employer ')) else None,
            'loan_amount': float(row.get('Loan Amount')) if not pd.isna(row.get('Loan Amount')) else None,
            'loan_serial': str(row.get('Loanserial')).strip() if not pd.isna(row.get('Loanserial')) else None,
            'repayment_per_month': float(row.get('Repayment Per Month')) if not pd.isna(row.get('Repayment Per Month')) else None,
            'loan_given_date': normalize_date(row.get('Date \nLoan Given')),
            'loan_term_months': int(row.get('Loan Term ')) if not pd.isna(row.get('Loan Term ')) else None,
            'amortization_type': str(row.get('Loan Amortization Type')).strip() if not pd.isna(row.get('Loan Amortization Type')) else None,
            'balance': float(row.get('Balance')) if not pd.isna(row.get('Balance')) else None,
            'loan_balance_expected': float(row.get('Loan Balance Expected')) if not pd.isna(row.get('Loan Balance Expected')) else None,
            'actual_balance': float(row.get('Actual Balance  ')) if not pd.isna(row.get('Actual Balance  ')) else None,
            'expected_interest_paid': float(row.get('Expected Interest Paid')) if not pd.isna(row.get('Expected Interest Paid')) else None,
            'interest_balance': float(row.get('Interest balance')) if not pd.isna(row.get('Interest balance')) else None,
            'latest_amount_paid': float(row.get('Latest Amount Paid')) if not pd.isna(row.get('Latest Amount Paid')) else None,
            'latest_paid_date': normalize_date(row.get('Latest Paid Date')),
            'loan_arrears': float(row.get('Loan Arrears')) if not pd.isna(row.get('Loan Arrears')) else None,
            'days_in_arrears': int(row.get('Days in Arrears')) if not pd.isna(row.get('Days in Arrears')) else None,
            'annual_rate': float(row.get('Annual  % Rate')) if not pd.isna(row.get('Annual  % Rate')) else None,
            'classification': str(row.get(' Classification ')).strip() if not pd.isna(row.get(' Classification ')) else None,
            'loan_loss_provision': float(row.get('Loan Loss Provision Amount')) if not pd.isna(row.get('Loan Loss Provision Amount')) else None,
            'loan_maturity': normalize_date(row.get('Loan Maturity')),
            'members_deposits': float(row.get('Members Deposits')) if not pd.isna(row.get('Members Deposits')) else None
        }
        rows.append(record)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open('w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    print(f'Wrote {len(rows)} member loan records to {OUTPUT_FILE}')

if __name__ == '__main__':
    build()
