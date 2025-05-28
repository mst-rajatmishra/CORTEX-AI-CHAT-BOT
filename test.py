import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog, ttk
import requests
import json
import os
from itertools import cycle
import threading

class CortexAIChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("Cortex AI")
        self.root.geometry("750x650")
        self.root.configure(bg="#2c3e50")
        
        # API configuration
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        self.api_key = self.get_api_key()
        
        if not self.api_key:
            self.root.destroy()
            return
            
        self.setup_ui()
        self.loading = False
        self.loading_frames = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
        self.loading_animation = cycle(self.loading_frames)
        self.current_animation = ""
        
    def get_api_key(self):
        """Get API key from environment or user input"""
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            return api_key
            
        api_key = simpledialog.askstring(
            "🔑 Cortex AI Access", 
            "Enter your API key to access Cortex AI:",
            parent=self.root,
            show="*"
        )
        
        if not api_key:
            messagebox.showerror("Access Denied", "API key is required to use Cortex AI")
            return None
            
        return api_key
    
    def setup_ui(self):
        """Set up the user interface with Cortex branding"""
        # Main container
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header with Cortex AI logo
        header = tk.Frame(main_frame, bg="#3498db")
        header.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            header,
            text="CORTEX AI",
            font=("Helvetica", 18, "bold"),
            fg="white",
            bg="#3498db",
            padx=15,
            pady=12
        ).pack(side=tk.LEFT)
        
        # Chat display with neural network background
        self.chat_display = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            state='disabled',
            font=("Helvetica", 12),
            bg="#ecf0f1",
            fg="#2c3e50",
            padx=20,
            pady=20,
            relief=tk.FLAT,
            insertbackground="#3498db"
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Input frame with futuristic design
        input_frame = tk.Frame(main_frame, bg="#2c3e50")
        input_frame.pack(fill=tk.X, pady=(15, 0))
        
        self.user_input = tk.Entry(
            input_frame,
            font=("Helvetica", 12),
            relief=tk.FLAT,
            bg="#ecf0f1",
            fg="#2c3e50",
            insertbackground="#3498db",
            borderwidth=0,
            highlightthickness=2,
            highlightbackground="#3498db",
            highlightcolor="#3498db"
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=10)
        self.user_input.bind("<Return>", lambda e: self.send_message())
        
        self.send_btn = tk.Button(
            input_frame,
            text="SEND",
            command=self.send_message,
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            relief=tk.FLAT,
            font=("Helvetica", 10, "bold"),
            padx=25,
            borderwidth=0
        )
        self.send_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Loading indicator with Cortex branding
        self.loading_label = tk.Label(
            input_frame,
            text="",
            font=("Helvetica", 12),
            fg="#3498db",
            bg="#2c3e50"
        )
        self.loading_label.pack(side=tk.LEFT, padx=10)
        
        # Sample prompts with Cortex theme
        samples = [
            "Explain neural networks",
            "Cortex AI capabilities",
            "Future of artificial intelligence",
            "How does machine learning work?"
        ]
        
        samples_frame = tk.Frame(main_frame, bg="#2c3e50")
        samples_frame.pack(fill=tk.X, pady=(15, 0))
        
        for sample in samples:
            btn = tk.Button(
                samples_frame,
                text=sample,
                command=lambda s=sample: self.use_sample(s),
                bg="#34495e",
                fg="#ecf0f1",
                activebackground="#2c3e50",
                relief=tk.FLAT,
                font=("Helvetica", 9),
                padx=12,
                pady=4,
                borderwidth=0
            )
            btn.pack(side=tk.LEFT, padx=5, pady=5)
    
    def use_sample(self, sample):
        """Use a sample prompt"""
        self.user_input.delete(0, tk.END)
        self.user_input.insert(0, sample)
        self.send_message()
    
    def send_message(self):
        """Send message to Cortex AI"""
        message = self.user_input.get().strip()
        if not message or self.loading:
            return
            
        self.user_input.delete(0, tk.END)
        self.display_message(f"You: {message}", "user")
        
        # Disable input during processing
        self.loading = True
        self.user_input.config(state=tk.DISABLED)
        self.send_btn.config(state=tk.DISABLED)
        
        # Start loading animation
        self.animate_loading()
        
        # Run API call in separate thread
        threading.Thread(target=self.process_message, args=(message,), daemon=True).start()
    
    def animate_loading(self):
        """Show Cortex AI processing animation"""
        if self.loading:
            self.current_animation = next(self.loading_animation)
            self.loading_label.config(text=f"Cortex Processing {self.current_animation}")
            self.root.after(100, self.animate_loading)
    
    def process_message(self, message):
        """Process message with Cortex AI"""
        try:
            response = self.call_gemini_api(message)
            if response:
                # Replace any Gemini references with Cortex
                response = response.replace("Gemini", "Cortex")
                response = response.replace("gemini", "Cortex")
                self.display_message(f"Cortex: {response}", "bot")
        except Exception as e:
            self.display_message(f"Error: {str(e)}", "error")
        finally:
            self.loading = False
            self.user_input.config(state=tk.NORMAL)
            self.send_btn.config(state=tk.NORMAL)
            self.loading_label.config(text="")
            self.user_input.focus()
    
    def call_gemini_api(self, prompt):
        """Make the API call using requests"""
        headers = {'Content-Type': 'application/json'}
        params = {'key': self.api_key}
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }
        
        response = requests.post(
            self.api_url,
            headers=headers,
            params=params,
            data=json.dumps(payload),
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            raise Exception(f"API Error: {response.text}")
    
    def display_message(self, message, sender):
        """Display message in chat window with Cortex styling"""
        self.chat_display.config(state='normal')
        
        # Configure tags for different message types
        if "user" not in self.chat_display.tag_names():
            self.chat_display.tag_config("user", foreground="#3498db", lmargin1=20, lmargin2=20, rmargin=20, spacing3=10, font=("Helvetica", 12, "bold"))
            self.chat_display.tag_config("bot", foreground="#2c3e50", lmargin1=20, lmargin2=20, rmargin=20, spacing3=10, font=("Helvetica", 12))
            self.chat_display.tag_config("error", foreground="#e74c3c", lmargin1=20, lmargin2=20, rmargin=20, font=("Helvetica", 12))
        
        # Insert message with appropriate tag
        self.chat_display.insert(tk.END, message + "\n\n", sender)
        
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)  # Auto-scroll to bottom

if __name__ == "__main__":
    root = tk.Tk()
    app = CortexAIChatbot(root)
    root.mainloop()