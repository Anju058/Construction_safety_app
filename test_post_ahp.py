from app import app

# Build sample form with 36 comparisons
form = {}
for i in range(9):
    for j in range(i+1, 9):
        form[f'h{i}_h{j}'] = '3' if i==0 else '1'

with app.test_client() as client:
    resp = client.post('/ahp', data=form, follow_redirects=True)
    print('Status code:', resp.status_code)
    data = resp.get_data(as_text=True)
    # Check for a few expected markers
    print('Contains weight table header:', 'Hazard Weights' in data or 'Hazard Weights' in data)
    print('Contains CR label:', 'Consistency Ratio' in data)
    # Print snippet around weights table
    start = data.find('Hazard Weights')
    if start!=-1:
        print(data[start:start+500])
    else:
        # fallback: search for percent sign occurrences
        idx = data.find('%')
        print('First % found at', idx)
    
    # Save response to file for manual inspection
    with open('last_response.html', 'w', encoding='utf-8') as f:
        f.write(data)
    print('Saved last_response.html')
