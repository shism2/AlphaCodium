import os
import toml

# Path to the secrets file
secrets_path = 'alpha_codium/settings/.secrets.toml'

# Get the API key from environment variable or use the default
api_key = os.environ.get('GEMINI_API_KEY', 'AIzaSyCfplLiEgnQ1YjGOm38XNgnbjsbp6ageXA')

# Create the secrets dictionary
secrets = {
    'gemini': {
        'key': api_key
    }
}

# Write the secrets to the file
with open(secrets_path, 'w') as f:
    toml.dump(secrets, f)

print(f'Updated API key in {secrets_path}')