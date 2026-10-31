"""Check submission plan gaps."""
import sys, os
sys.path.insert(0, '.')

checks = {}

with open('requirements.txt', encoding='utf-8') as f:
    reqs = f.read()
checks['requests in requirements.txt'] = 'requests' in reqs
checks['google-generativeai in requirements.txt'] = 'google-generativeai' in reqs

with open('core/explainer.py', encoding='utf-8') as f:
    exp = f.read()
checks['st.secrets support in explainer.py'] = 'st.secrets' in exp

with open('core/engine.py', encoding='utf-8') as f:
    eng = f.read()
checks['portal health check / requests in engine.py'] = 'check_portal_health' in eng or 'import requests' in eng

with open('ui/components/sidebar.py', encoding='utf-8') as f:
    sidebar = f.read()
checks['live portal status badge in sidebar.py'] = 'check_portal_health' in sidebar and '_render_portal_sync_badge' in sidebar

checks['README.md exists'] = os.path.exists('README.md')
checks['logo_MH.png exists'] = os.path.exists('logo_MH.png')
checks['data/schemes.json exists'] = os.path.exists('data/schemes.json')
checks['.streamlit/secrets.toml example'] = os.path.exists('.streamlit/secrets.toml') or os.path.exists('.streamlit')

for k, v in checks.items():
    print(f"{'OK  ' if v else 'MISS'} {k}")
