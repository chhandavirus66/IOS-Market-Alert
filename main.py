import flet as ft
import time
import broker_api
import instruments

def main(page: ft.Page):
    page.title = "Market Alert (iOS)"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 400
    page.window_height = 800

    status_text = ft.Text("App Ready. Press Start.", size=20, weight=ft.FontWeight.BOLD)
    
    # Naya Feature: Source select karne ke liye Dropdown
    source_dropdown = ft.Dropdown(
        label="Select Data Source",
        options=[
            ft.dropdown.Option("Yahoo Finance"),
            ft.dropdown.Option("Custom Broker API"),
        ],
        value="Yahoo Finance",
        width=250
    )

    log_view = ft.ListView(expand=True, spacing=10, padding=20)
    is_monitoring = False

    def monitor_market():
        while is_monitoring:
            logs = []
            selected_source = source_dropdown.value
            
            for symbol, data in instruments.MARKET_INSTRUMENTS.items():
                price = broker_api.get_live_price(symbol, selected_source)
                target = data["target_price"]
                
                if price is None:
                    logs.append(ft.Text(f"⚠️ {symbol}: Data fetch error (Check Internet)", color=ft.colors.ORANGE))
                    continue
                
                if price >= target:
                    logs.append(ft.Text(f"🚨 ALERT: {symbol} crossed {target}! (Current: ₹{price})", color=ft.colors.RED, weight=ft.FontWeight.BOLD))
                else:
                    logs.append(ft.Text(f"✅ {symbol}: ₹{price} (Target: ₹{target})", color=ft.colors.GREEN))
            
            log_view.controls = logs
            page.update()
            time.sleep(5) # 5 seconds delay

    def start_click(e):
        nonlocal is_monitoring
        is_monitoring = True
        status_text.value = f"Monitoring via {source_dropdown.value}..."
        status_text.color = ft.colors.GREEN
        start_btn.disabled = True
        stop_btn.disabled = False
        source_dropdown.disabled = True # Running state mein source change karna disable kar diya
        page.update()
        page.run_task(monitor_market)

    def stop_click(e):
        nonlocal is_monitoring
        is_monitoring = False
        status_text.value = "Monitoring Stopped."
        status_text.color = ft.colors.RED
        start_btn.disabled = False
        stop_btn.disabled = True
        source_dropdown.disabled = False # Stop hone par wapas enable ho jayega
        page.update()

    start_btn = ft.ElevatedButton("Start Monitoring", on_click=start_click, bgcolor=ft.colors.GREEN, color=ft.colors.WHITE)
    stop_btn = ft.ElevatedButton("Stop", on_click=stop_click, bgcolor=ft.colors.RED, color=ft.colors.WHITE, disabled=True)

    page.add(
        status_text,
        source_dropdown, # Dropdown ko screen par add kiya gaya
        ft.Row([start_btn, stop_btn], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),
        log_view
    )

ft.app(target=main)
