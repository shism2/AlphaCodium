# Google Gemini for AlphaCodium

This document explains how to use Google Gemini models with AlphaCodium.

## Overview

AlphaCodium uses Google Gemini models for powerful code generation capabilities when solving programming problems.

## Supported Models

The following Google Gemini models are supported:

### Gemini 1.5
- `gemini-1.5-pro`: A powerful model for complex code generation tasks
- `gemini-1.5-flash`: A faster model for simpler code generation tasks

### Gemini 2.0
- `gemini-2.0-pro`: The latest powerful model for complex code generation tasks
- `gemini-2.0-flash`: The latest faster model for simpler code generation tasks

## Setup

### 1. Install Required Packages

Make sure you have the required packages installed:

```bash
pip install -r requirements.txt
```

Or install the latest Google Gen AI SDK directly:

```bash
pip install -U google-genai
```

### 2. Set Up API Key

You need to obtain a Google Gemini API key from the [Google AI Studio](https://makersuite.google.com/app/apikey).

Once you have your API key, you can set it up using one of these methods:

#### Option 1: Using the setup script

Run the setup script and follow the prompts:

```bash
python setup_gemini.py
```

#### Option 2: Manual setup

Create or edit the file `alpha_codium/settings/.secrets.toml` and add your Gemini API key:

```toml
[gemini]
key = "your-gemini-api-key"
```

### 3. Configure the Model

Edit the `alpha_codium/settings/configuration.toml` file to use a Gemini model:

```toml
[config]
model = "gemini-1.5-pro"  # or "gemini-1.5-flash"
```

## Testing the Integration

You can test if the Gemini integration is working correctly by running:

```bash
python test_gemini.py
```

This will send a simple prompt to the Gemini model and print the response.

## Usage

Once configured, you can use AlphaCodium with Gemini models. All the commands and workflows are straightforward.

For example, to solve a specific problem:

```bash
python -m alpha_codium.solve_problem \
--dataset_name /path/to/dataset \
--split_name test \
--problem_number 0
```

## Troubleshooting

If you encounter issues with the Gemini integration:

1. **API Key Issues**: Make sure your API key is correct and has the necessary permissions
2. **Rate Limiting**: Be aware of Gemini's rate limits for your API key
3. **Model Availability**: Ensure the model you're trying to use is available in your region
4. **Response Format**: Gemini has its own response format which is handled by the integration

## Limitations

- The system prompt handling in Gemini uses the system_instruction parameter
- Finish reasons are not provided by Gemini API directly

## API Changes

The Gemini integration uses the new Google Gen AI SDK, which has a different API structure compared to the older google-generativeai library:

```python
# Old API (google-generativeai)
import google.generativeai as genai
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-pro")
response = model.generate_content("Hello world")

# New API (google-genai)
from google import genai
client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model="gemini-1.5-pro",
    contents="Hello world",
    config={
        "temperature": 0.2,
        "system_instruction": "You are a helpful assistant."
    }
)
```

For more information on the API changes, see the [Google Gen AI SDK migration guide](https://ai.google.dev/gemini-api/docs/migrate).

## Contributing

If you encounter issues or have suggestions for improving the Gemini integration, please open an issue or submit a pull request.