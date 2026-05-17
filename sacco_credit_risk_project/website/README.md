# RUPSA SACCO Website

This website folder contains a static portal for SACCO credit risk analytics and member loan lookup.

## Structure

- `index.html` — main website interface
- `styles.css` — styling for the portal
- `app.js` — JavaScript logic for dashboard, calculator, and member search
- `build_data.py` — Python script to export the Excel dataset into JSON
- `data/members.json` — generated member loan dataset used by the website

## Usage

1. Run the data build script to regenerate the dataset:

```bash
python website/build_data.py
```

2. Serve the website from a local server (recommended):

```bash
cd website
python -m http.server 8000
```

3. Open `http://localhost:8000` in your browser.

## Search behavior

- Search by six-digit member number without `M-` (for example `000020`)
- Search by phone number (`+254725207022` or `254725207022`)
- Search by account ID (`0000000020`)

## Notes

- The calculator auto-selects interest rates by loan type.
- Member lookup uses the current Excel dataset and returns all loan records for the matching member.
- If no loans are found, the portal shows a clear "no matching member loan records found" message.
