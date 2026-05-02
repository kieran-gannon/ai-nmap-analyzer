# AI Nmap Analyzer
# A natural language network scanning agent powered by Ollama
# Author: Kieran Gannon
# GitHub: https://github.com/yourusername

# import necessary libraries
import subprocess
from unittest import result
import ollama
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich import print
import re

# create a console object
console = Console()

# main function to run the application 
def main():
    console.print(Panel("[bold green]AI Nmap Analyzer[/bold green]", subtitle="Powered by Ollama"))
    
    # Prompt user for target IP or hostname
    while True:
        target = input("Enter the target IP or hostname to scan: ")
        if validate_target(target):
            break
        console.print("[bold red]Invalid target. Please enter a valid IP or hostname.[/bold red]")

    # Main loop to ask user for questions and run nmap commands
    while True:
        prompt = input("\nEnter your question (or 'q' to quit, 'target' to change target): ")
        if prompt.lower() == 'q':
            break
        if prompt.lower() == 'target':
            while True:
                target = input("Enter the new target IP or hostname: ")
                if validate_target(target):
                    break
                console.print("[bold red]Invalid target. Please enter a valid IP or hostname.[/bold red]")
            continue

        command = get_command_from_llm(prompt, target)
        run_nmap_command(prompt, command, target)

# Function to get nmap command from the language model based on user prompt and target
def get_command_from_llm(prompt, target):
    response = ollama.chat(model="gemma4:e4b", messages=[
        {"role": "system", "content": (
            f"You are an expert cybersecurity analyst with access to only Nmap on macOS. "
            f"Only respond with the exact nmap command needed to answer the question about {target}. "
            "No explanation. No markdown. Just the raw command."
        )},
        {"role": "user", "content": prompt}
    ])
    return response['message']['content']

# Function to run the nmap command and analyze the output with the language model
def run_nmap_command(prompt, command, target):
    console.print(f"[bold blue]Run command:[/bold blue] {command}")

    if not command.strip().startswith("nmap"):
      console.print("[bold red]Invalid command returned by AI. Skipping.[/bold red]")
      return

    run = input("y/n?: ")

    if run.lower() == "y":
        needs_sudo = "-O" in command or "-A" in command or "-sS" in command
        if needs_sudo:
            cmd = ["sudo"] + command.split()
        else:
            cmd = command.split()

        result = subprocess.run(cmd, capture_output=True, text=True)
        analysis = analyze_nmap_output(prompt, command, result.stdout)
        console.print(Panel(Markdown(analysis), title="[bold red]AI Analysis[/bold red]", border_style="red"))
        print("\n")

    if run.lower() == "n":
        console.print("[bold red]Command skipped.[/bold red]")
        return
    
# Function to analyze nmap output with the language model and provide insights based on the user's question
def analyze_nmap_output(prompt, command, output):
    response = ollama.chat(model="gemma4:e4b", messages=[
        {"role": "system", "content": (
            "You are an expert cybersecurity analyst. "
            "Answer the user's question based on the provided Nmap command and its output. "
            "Be specific and reference actual findings from the output."
        )},
        {"role": "user", "content": (
            f"My question: {prompt}\n\n"
            f"Command that was run: {command}\n\n"
            f"Output:\n{output}"
        )}
    ])
    return response['message']['content']


# Function to validate if the input is a valid IP address or hostname
def validate_target(target):
    # Basic validation for IP address or hostname
    ip_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    hostname_pattern = re.compile(r"^(?=.{1,253}$)(?!-)[a-zA-Z0-9-]{1,63}(?<!-)(?:\.[a-zA-Z0-9-]{1,63}(?<!-))*\.?$")

    if ip_pattern.match(target):
        return True
    if hostname_pattern.match(target):
        return True
    return False

# Run the main function
if __name__ == "__main__":    
    main()