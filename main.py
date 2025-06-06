import requests
import time
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt

console = Console()

LOGO = r"""
███╗   ██╗ █████╗ ██████╗ ███████╗███████╗███╗  ███╗
 ████╗  ██║██╔══██╗██╔══██╗██╔════╝██╔════╝████╗ ████║
 ██╔██╗ ██║███████║██║  ██║█████╗  █████╗  ██╔████╔██║
 ██║╚██╗██║██╔══██║██║  ██║██╔══╝  ██╔══╝  ██║╚██╔╝██║
 ██║ ╚████║██║  ██║██████╔╝███████╗███████╗██║ ╚═╝ ██║
 ╚═╝  ╚═══╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚══════╝╚═╝     ╚═╝

               [bold yellow]by Nadeem.Name[/bold yellow]
"""

REASONS = {
    "1": "Fake Account",
    "2": "Nudity",
    "3": "Spam",
    "4": "Harassment",
    "5": "Hate Speech"
}

def get_user_name(token):
    url = "https://graph.facebook.com/me"
    params = {"access_token": token}
    try:
        res = requests.get(url, params=params)
        if res.status_code == 200:
            data = res.json()
            return data.get("name", "Unknown User")
        else:
            return "Unknown User"
    except:
        return "Unknown User"

def send_report(token, target_id, reason):
    url = f"https://graph.facebook.com/{target_id}/reports"
    data = {
        'access_token': token,
        'reason': reason
    }
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception:
        return False

def main():
    console.clear()
    console.print(Panel.fit(Text(LOGO, justify="center"), border_style="yellow"))

    token_file = Prompt.ask("[bold green]Enter token file name[/bold green]", default="token.txt")

    try:
        with open(token_file, "r") as f:
            tokens = [line.strip() for line in f if line.strip()]
        if not tokens:
            console.print("[red]Token file is empty![/red]")
            return
    except FileNotFoundError:
        console.print(f"[red]File '{token_file}' not found![/red]")
        return

    target_id = Prompt.ask("[bold cyan]Enter target Facebook ID to report[/bold cyan]")

    console.print("\nSelect reason to report:")
    for k, v in REASONS.items():
        console.print(f"[yellow][{k}][/yellow] {v}")
    reason_key = Prompt.ask("[bold magenta]Select reason (1-5)[/bold magenta]", choices=["1","2","3","4","5"])

    delay = Prompt.ask("[bold blue]Enter delay between reports (seconds)[/bold blue]", default="10")
    try:
        delay = float(delay)
    except:
        delay = 10

    console.print(f"\n[bold green]Starting report process for target ID {target_id} with {len(tokens)} tokens...[/bold green]\n")

    success_count = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Sending reports...", total=len(tokens))

        for idx, token in enumerate(tokens, start=1):
            user_name = get_user_name(token)
            result = send_report(token, target_id, reason_key)
            if result:
                success_count += 1
                progress.update(task, description=f"[green]Report {idx}/{len(tokens)} sent by [bold]{user_name}[/bold]![/green]")
                console.print(f"[bold green]✔ Report sent successfully using token of:[/bold green] [yellow]{user_name}[/yellow]")
            else:
                progress.update(task, description=f"[red]Report {idx}/{len(tokens)} failed (token owner: {user_name}).[/red]")
                console.print(f"[bold red]✘ Report failed using token of:[/bold red] [yellow]{user_name}[/yellow]")
            time.sleep(delay)

    console.print(f"\n[bold yellow]Reporting finished![/bold yellow] Successful reports: [bold green]{success_count}[/bold green] out of [bold]{len(tokens)}[/bold]")

if __name__ == "__main__":
    main()
