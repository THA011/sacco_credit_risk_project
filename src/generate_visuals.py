import os
import json
import pandas as pd
import matplotlib.pyplot as plt


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def load_data():
    base = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
    data_path = os.path.join(base, 'website', 'data', 'members.json')
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"members.json not found at {data_path}")
    return pd.read_json(data_path)


def plot_loan_composition(df, outdir):
    df['balance'] = pd.to_numeric(df.get('balance', 0), errors='coerce').fillna(0)
    comp = df.groupby('loan_name')['balance'].sum().sort_values(ascending=False)
    top = comp.head(6)
    others = comp.iloc[6:].sum()
    if others > 0:
        top['Other'] = others
    plt.figure(figsize=(7,7))
    top.plot.pie(autopct='%1.1f%%')
    plt.title('Loan Composition (by Outstanding Balance)')
    fn = os.path.join(outdir, 'loan_composition.png')
    plt.savefig(fn, bbox_inches='tight')
    plt.close()
    return fn


def plot_classification_counts(df, outdir):
    counts = df['classification'].fillna('Unknown').value_counts()
    plt.figure(figsize=(8,5))
    counts.plot.bar(color='C0')
    plt.title('Risk Classification Counts')
    plt.ylabel('Number of Loans')
    fn = os.path.join(outdir, 'classification_counts.png')
    plt.savefig(fn, bbox_inches='tight')
    plt.close()
    return fn


def plot_arrears_hist(df, outdir):
    col = 'days_in_arrears'
    if col not in df.columns:
        return None
    vals = pd.to_numeric(df[col], errors='coerce').fillna(0)
    plt.figure(figsize=(8,4))
    plt.hist(vals, bins=50, color='C2')
    plt.title('Days in Arrears Distribution')
    plt.xlabel('Days in Arrears')
    plt.ylabel('Loans')
    fn = os.path.join(outdir, 'arrears_histogram.png')
    plt.savefig(fn, bbox_inches='tight')
    plt.close()
    return fn


def main():
    outdir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'outputs'))
    ensure_dir(outdir)
    df = load_data()
    print(f'Read {len(df)} records')
    files = []
    files.append(plot_loan_composition(df, outdir))
    files.append(plot_classification_counts(df, outdir))
    f = plot_arrears_hist(df, outdir)
    if f:
        files.append(f)
    print('Saved visuals:')
    for f in files:
        print(' -', f)


if __name__ == '__main__':
    main()
