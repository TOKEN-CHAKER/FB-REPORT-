import requests
import time
import sys
import os

# Colored output & animation
try:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn
except ImportError:
    print("Rich module not found. Installing...")
    os.system("pip install rich")
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

# NADEEM Logo
def print_logo():
    logo = """
╔═╗┬  ┬    ╔═╗╔╗╔╔╦╗╦═╗╔═╗
║  │  │    ╠═╝║║║ ║ ╠╦╝║╣ 
╚═╝┴─┘┴─┘  ╩  ╝╚╝ ╩ ╩╚═╚═╝
      [bold yellow]FACEBOOK REPORT TOOL[/bold yellow]
"""
    console.print(logo, style="bold red")

def get_user_name(token):
    url = "https://graph.facebook.com/me"
    params = {"access_token": token}
    try:
        res = requests.get(url, params=params, timeout=7)
        if res.status_code == 200:
            data = res.json()
            name = data.get("name", "Unknown User")
            # Safe sanitize: printable chars only, limit length
            name = "".join(ch for ch in name if ch.isprintable())[:25]
            return name
        else:
            return "Invalid Token"
    except Exception:
        return "Invalid Token"

def send_report(token, target_id, reason_key):
    url = f"https://graph.facebook.com/{target_id}/reports"
    data = {
        'access_token': token,
        'reason': reason_key
    }
    try:
        response = requests.post(url, data=data, timeout=10)
        if response.status_code == 200:
            return True, None
        else:
            try:
                error_data = response.json()
                err_msg = error_data.get("error", {}).get("message", "Unknown Error")
            except:
                err_msg = "Unknown Error"
            return False, err_msg
    except Exception as e:
        return False, str(e)

def main():
    print_logo()

    # Input token file
    token_file = console.input("[bold cyan]Enter path to token file (each token in new line): [/bold cyan]").strip()
    if not os.path.isfile(token_file):
        console.print(f"[red]Error: File '{token_file}' not found! Exiting.[/red]")
        sys.exit()

    # Read tokens
    with open(token_file, "r") as f:
        tokens = [line.strip() for line in f if line.strip()]

    if not tokens:
        console.print("[red]No tokens found in file! Exiting.[/red]")
        sys.exit()

    # Input target ID
    target_id = console.input("[bold cyan]Enter Facebook target ID to report: [/bold cyan]").strip()
    if not target_id.isdigit():
        console.print("[red]Invalid target ID! Must be numeric.[/red]")
        sys.exit()

    # Reason selection
    reasons = {
        "1": "FAKE_ACCOUNT",
        "2": "NUDITY",
        "3": "SPAM",
        "4": "HARASSMENT",
        "5": "HATE_SPEECH"
    }
    console.print("\n[bold yellow]Report Reasons:[/bold yellow]")
    console.print("[1] Fake Account")
    console.print("[2] Nudity")
    console.print("[3] Spam")
    console.print("[4] Harassment")
    console.print("[5] Hate Speech")

    reason_choice = console.input("\n[bold cyan]Select reason number (1-5): [/bold cyan]").strip()
    if reason_choice not in reasons:
        console.print("[red]Invalid reason choice! Exiting.[/red]")
        sys.exit()

    reason_key = reasons[reason_choice]

    # Delay between reports
    try:
        delay = float(console.input("[bold cyan]Enter delay between reports (seconds, e.g. 10): [/bold cyan]").strip())
        if delay < 1:
            delay = 1
    except:
        delay = 10

    console.print(f"\n[green]Starting reporting on target ID {target_id} with reason '{reason_key}' using {len(tokens)} tokens.[/green]\n")

    total = len(tokens)
    success_count = 0
    fail_count = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
        console=console,
    ) as progress:

        task = progress.add_task("[cyan]Reporting...", total=total)

        for idx, token in enumerate(tokens, start=1):
            user_name = get_user_name(token)

            success, error = send_report(token, target_id, reason_key)
            if success:
                console.print(f"[bold green]✔ Report sent successfully using token of:[/bold green] [bold bright_green]{user_name}[/bold bright_green]")
                success_count += 1
            else:
                console.print(f"[bold red]✘ Report failed using token of:[/bold red] {user_name} - [yellow]{error}[/yellow]")
                fail_count += 1

            progress.update(task, advance=1)
            time.sleep(delay)

    console.print(f"\n[bold magenta]Reporting completed![/bold magenta]")
    console.print(f"[bold green]Success:[/bold green] {success_count} | [bold red]Failed:[/bold red] {fail_count}")

if __name__ == "__main__":
    main()
