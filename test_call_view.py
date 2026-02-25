from app import app

# Build sample form with 36 comparisons
form = {}
for i in range(9):
    for j in range(i+1, 9):
        form[f'h{i}_h{j}'] = '3' if i==0 else '1'

with app.test_request_context('/ahp', method='POST', data=form):
    # Call the view function directly
    resp = app.view_functions['ahp']()
    # resp is a rendered template string
    if isinstance(resp, str):
        data = resp
    else:
        try:
            data = resp.get_data(as_text=True)
        except Exception:
            data = str(resp)

    print('Response length:', len(data))
    # quick checks
    print('Contains "Hazard Weights"?', 'Hazard Weights' in data)
    print('Contains "%"?', '%' in data)
    # write to file
    with open('last_response_view.html', 'w', encoding='utf-8') as f:
        f.write(data)
    print('Saved last_response_view.html')
