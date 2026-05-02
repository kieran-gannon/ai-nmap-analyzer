# AI Nmap Analyzer

A natural language network scanning agent powered by a local LLM via Ollama. 
Ask questions in plain English and the agent determines the right Nmap command, 
asks for your approval, runs it, and explains the results.

## Features
- Natural language interface for Nmap scanning
- Human-in-the-loop command approval
- Only uses sudo when required by Nmap
- Input validation to prevent command injection
- AI powered analysis of scan results

## Requirements
- Python 3.x
- [Nmap](https://nmap.org)
- [Ollama](https://ollama.com) with gemma4 pulled

## Installation
1. Clone the repo
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`

## Example

<img width="730" height="652" alt="Screenshot 2026-05-02 at 4 29 24 PM" src="https://github.com/user-attachments/assets/610921fa-ffc2-49d9-94a7-fb75306a6907" />

Enter the target IP or hostname to scan: scanme.nmap.org
Enter your question: what OS is the server running?
Run command: nmap -O scanme.nmap.org
y/n?: y

## Usage
```bash
python main.py
```

## Disclaimer
Only use this tool against systems you own or have explicit permission to scan. Never blindly accept AI generated commands. This tool was created as a personal research project to build my skills combining cybersecurity tools with local LLMs.
