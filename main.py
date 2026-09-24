from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
import broker_api
import instruments

class MarketAlertApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.status_label = Label(text="Market Alert App (iOS)", font_size='24sp')
        self.layout.add_widget(self.status_label)
        
        self.log_label = Label(text="Press Start to monitor...", font_size='16sp')
        self.layout.add_widget(self.log_label)
        
        self.start_btn = Button(text="Start Monitoring", background_color=(0, 1, 0, 1))
        self.start_btn.bind(on_press=self.start_alerts)
        self.layout.add_widget(self.start_btn)
        
        self.stop_btn = Button(text="Stop", background_color=(1, 0, 0, 1), disabled=True)
        self.stop_btn.bind(on_press=self.stop_alerts)
        self.layout.add_widget(self.stop_btn)
        
        self.monitoring = False
        return self.layout

    def start_alerts(self, instance):
        self.monitoring = True
        self.start_btn.disabled = True
        self.stop_btn.disabled = False
        self.status_label.text = "Monitoring Active..."
        # Har 5 second mein market check karega (Jab app open hogi)
        Clock.schedule_interval(self.check_market, 5)

    def stop_alerts(self, instance):
        self.monitoring = False
        self.start_btn.disabled = False
        self.stop_btn.disabled = True
        self.status_label.text = "Monitoring Stopped."
        Clock.unschedule(self.check_market)

    def check_market(self, dt):
        if not self.monitoring:
            return False
            
        logs = []
        for symbol, data in instruments.MARKET_INSTRUMENTS.items():
            price = broker_api.get_live_price(symbol)
            target = data["target_price"]
            
            if price >= target:
                logs.append(f"ALERT: {symbol} crossed {target}! (Current: {price})")
            else:
                logs.append(f"{symbol}: {price}")
                
        self.log_label.text = "\n".join(logs)

if __name__ == '__main__':
    MarketAlertApp().run()
