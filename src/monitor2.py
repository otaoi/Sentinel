import redis
import json
import time
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.align import Align

# CONFIG
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
GRID_SIZE = 11 

def generate_grid_map(data):
    center_idx = GRID_SIZE // 2
    grid = [["🌲" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    
    hero_sensor = next((x for x in data if "LYTTON" in x['id']), None)
    
    status_text = "SECTOR STABLE"
    status_style = "green"
    border_style = "green"

    if hero_sensor:
        s = hero_sensor['status'].lower()
        t = hero_sensor['temp']
        
        if s == "fire":
            # spread of fire visualized conveniently with emojis
            grid[center_idx][center_idx] = "🔥" 
            # inner red ring
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i==0 and j==0: continue
                    grid[center_idx+i][center_idx+j] = "🔴"
            # outer orange ting
            grid[center_idx-2][center_idx] = "🟠"
            grid[center_idx+2][center_idx] = "🟠"
            grid[center_idx][center_idx-2] = "🟠"
            grid[center_idx][center_idx+2] = "🟠"
            
            status_text = "IGNITION SPREADING - CONTAINMENT FAILED"
            status_style = "bold white on red blink"
            border_style = "red"

        elif s == "warning" or t > 40:
            # PREDICTION VISUALIZATION
            grid[center_idx][center_idx] = "⚠️ "
            grid[center_idx][center_idx+1] = "🟠"
            grid[center_idx][center_idx-1] = "🟠"

            status_text = "PREDICTION: THERMAL ANOMALY EXPANDING"
            status_style = "bold black on yellow"
            border_style = "yellow"
        else:
            grid[center_idx][center_idx] = "🌲"

    map_str = "\n"
    for row in grid:
        map_str += "  ".join(row) + "\n"
        
    legend = "\n[dim]🌲=Safe  ⚠️=Prediction  🔥=Ignition  🔴=Spread[/dim]"
    
    return Panel(
        Align.center(map_str + legend), 
        title="[bold]LIVE SECTOR MAP[/bold]", 
        subtitle=f"[{status_style}]{status_text}[/{status_style}]",
        border_style=border_style
    )

def generate_stats_panel(data):
    if not data: return Panel(Align.center("WAITING FOR STREAM..."), title="Status")
    
    avg_temp = sum(x['temp'] for x in data) / len(data)
    active_fires = sum(1 for x in data if x['status'].lower() == 'fire')
    warning_active = any(x['status'].lower() == 'warning' for x in data)
    
    if active_fires > 0:
        action = "[bold red blink]DISPATCHING ALL UNITS[/]"
        context = "IGNITION PATTERN MATCHED (LYTTON 2021)"
        alert_level = "CRITICAL (RED)"
    elif warning_active:
        action = "[bold yellow]ISSUING 48H WARNING[/]"
        context = "HISTORICAL PATTERN DETECTED"
        alert_level = "ELEVATED (YELLOW)"
    else:
        action = "[dim]MONITORING HISTORICAL ZONES[/]"
        context = "BASELINE: STABLE"
        alert_level = "NOMINAL (GREEN)"

    stats = f"""
    [bold]Active Nodes:[/bold] {len(data)}
    [bold]Avg Grid Temp:[/bold] {avg_temp:.1f}°C
    [bold]Alert Level:[/bold]   {alert_level}

    [bold underline]SYSTEM LOGIC:[/bold underline]
    {action}
    [dim]{context}[/dim]
    """
    return Panel(stats, title="Command & Control")

layout = Layout()
layout.split_column(Layout(name="header", size=3), Layout(name="body", ratio=1))
layout["body"].split_row(Layout(name="map", ratio=2), Layout(name="stats", ratio=1))

console = Console()
console.clear()
console.print("[bold green]>> INITIALIZING SENTINEL KERNEL[/]")
time.sleep(0.5)
console.print("[bold green]>> LOADING HISTORICAL GEODATA[/]")
time.sleep(0.5)
console.print("[bold green]>> CONNECTING TO REDIS STREAM[/]")
time.sleep(0.5)

with Live(layout, refresh_per_second=4, screen=True):
    while True:
        try:
            raw = r.lrange("fire_stream", 0, 50)
            if not raw:
                layout["header"].update(Panel(Align.center("SENTINEL BC OFFLINE"), style="dim"))
                layout["map"].update(Panel(Align.center("NO SIGNAL"), border_style="dim"))
                layout["stats"].update(Panel(Align.center("Start Simulator"), border_style="dim"))
                time.sleep(0.5)
                continue     
            data = [json.loads(x) for x in raw]
            layout["header"].update(Panel(Align.center("[bold green]SENTINEL'[/bold green]"), style="green"))
            layout["map"].update(generate_grid_map(data))
            layout["stats"].update(generate_stats_panel(data))
        except Exception: pass
        time.sleep(0.1)