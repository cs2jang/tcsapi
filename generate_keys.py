import pickle
from pathlib import Path

import streamlit_authenticator as stauth


username = ['admin', 'stcuser']
passwords = ['XXX', 'XXX']

hash_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hash_pw.pkl"
with file_path.open('wb') as file:
    pickle.dump(hash_passwords, file)
