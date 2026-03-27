import flet as ft
import requests 
import datetime 
import os
import tkinter as tk 
from tkinter import filedialog 

# 🚨 PASTE YOUR REAL URL HERE! 🚨
FIREBASE_URL = "https://logistics-rfid-system-default-rtdb.asia-southeast1.firebasedatabase.app/" 

def main(page: ft.Page):
    page.window_width = 400
    page.window_height = 800
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 30
    page.bgcolor = ft.Colors.BLUE_GREY_50 
    page.scroll = ft.ScrollMode.ADAPTIVE 

    header = ft.Text("iAcademy Logistics", size=28, weight="bold", color=ft.Colors.CYAN_800)
    logo_image = ft.Image(src="RFID Logo.jpg", width=150, height=150, fit=ft.BoxFit.CONTAIN)
    status_text = ft.Text("Status: Waiting at Gate...", size=16, color=ft.Colors.BLUE_900, weight="w_600")

    driver_info = ft.Column(
        controls=[
            ft.Text("Juan Dela Cruz", size=22, weight="bold", color=ft.Colors.BLUE_900),
            ft.Text("Plate: ABC-1234", size=18, color=ft.Colors.CYAN_700),
            status_text 
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER 
    )

    # --- iACADEMY BUSINESS LOGIC DROPDOWNS ---
    task_dropdown = ft.Dropdown(
        label="Select Specific Task",
        width=300,
        options=[
            ft.dropdown.Option("Asset Collection"),
            ft.dropdown.Option("Document Routing"),
            ft.dropdown.Option("Hardware & Event Transport")
        ]
    )

    location_dropdown = ft.Dropdown(
        label="Select Destination",
        width=300,
        options=[
            ft.dropdown.Option("iACADEMY Nexus (Yakal St.)"),
            ft.dropdown.Option("iACADEMY Plaza (Buendia)"),
            ft.dropdown.Option("Government Agencies (CHED/DepEd)"),
            ft.dropdown.Option("Industry Partners (Makati/BGC)")
        ]
    )

    delivery_status_dropdown = ft.Dropdown(
        label="Delivery Status",
        width=300,
        options=[
            ft.dropdown.Option("Ongoing / In Transit"),
            ft.dropdown.Option("Successful"),
            ft.dropdown.Option("Failed: Recipient Absent"),
            ft.dropdown.Option("Failed: Item Damaged"),
            ft.dropdown.Option("Failed: Cannot Locate Address"),
            ft.dropdown.Option("Failed: Cannot Contact Person")
        ]
    )

    driver_comments = ft.TextField(
        label="Additional Comments / Notes",
        width=300,
        multiline=True, 
        min_lines=1,
        max_lines=3,
        border_color=ft.Colors.BLUE_900
    )

    selected_document = None 

    def attach_clicked(e):
        nonlocal selected_document
        status_text.value = "Opening File Explorer..."
        status_text.color = ft.Colors.AMBER_700
        page.update()
        
        try:
            root = tk.Tk()
            root.withdraw() 
            root.attributes('-topmost', True) 
            
            file_path = filedialog.askopenfilename()
            root.destroy() 
            
            if file_path:
                selected_document = os.path.basename(file_path)
                status_text.value = f"Attached: {selected_document}"
                status_text.color = ft.Colors.GREEN_700
            else:
                status_text.value = "Upload cancelled."
                status_text.color = ft.Colors.ORANGE_500
        except Exception as ex:
            status_text.value = "Error opening file explorer."
            status_text.color = ft.Colors.RED_600
            
        page.update()

    # --- UPDATED: DATABASE LOGIC WITH CLEAR_FIELDS RULE ---
    def send_log_to_database(action_type, clear_fields=True):
        nonlocal selected_document 
        
        log_data = {
            "driver_name": "Juan Dela Cruz",
            "plate_number": "ABC-1234",
            "action": action_type,
            "task": task_dropdown.value if task_dropdown.value else "Not Selected",
            "location": location_dropdown.value if location_dropdown.value else "Not Selected",
            "delivery_status": delivery_status_dropdown.value if delivery_status_dropdown.value else "Not Selected", 
            "comments": driver_comments.value if driver_comments.value else "None", 
            "document_attached": selected_document if selected_document else "None", 
            "latitude": "14.5615", 
            "longitude": "121.0156", 
            "timestamp": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        }

        try:
            endpoint = FIREBASE_URL + "logs.json"
            response = requests.post(endpoint, json=log_data)

            if response.status_code == 200:
                status_text.value = f"Success: {action_type} Logged!"
                status_text.color = ft.Colors.GREEN_600
                
                # ONLY clear the form if we are officially done with the task (Time Out)
                if clear_fields:
                    selected_document = None 
                    task_dropdown.value = None
                    location_dropdown.value = None
                    delivery_status_dropdown.value = None
                    driver_comments.value = "" 
            else:
                status_text.value = "Error: Database refused connection."
                status_text.color = ft.Colors.RED_600
        except Exception as e:
            status_text.value = "Error: No internet connection."
            status_text.color = ft.Colors.RED_600
            
        page.update()

    # --- UPDATED: BUTTON TRIGGERS ---
    def clock_in_clicked(e):
        send_log_to_database("Driver Shift Clock-In", clear_fields=True) 

    def clock_out_clicked(e):
        send_log_to_database("Driver Shift Clock-Out", clear_fields=True) 

    def task_time_in_clicked(e):
        # clear_fields=False keeps the dropdowns filled out while they work!
        send_log_to_database("Task Time In (Arrived)", clear_fields=False) 

    def task_time_out_clicked(e):
        # clear_fields=True resets the app for the next delivery
        send_log_to_database("Task Time Out (Completed)", clear_fields=True) 

    # --- BUTTON DESIGNS ---
    attendance_row = ft.Row(
        controls=[
            ft.ElevatedButton("Clock In (Shift)", icon=ft.Icons.ACCESS_TIME, bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE, on_click=clock_in_clicked),
            ft.ElevatedButton("Clock Out (Shift)", icon=ft.Icons.TIMER_OFF, bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE, on_click=clock_out_clicked),
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    upload_btn = ft.ElevatedButton(
        content=ft.Text("Attach Proof/Photo", size=14),
        icon=ft.Icons.UPLOAD_FILE, bgcolor=ft.Colors.AMBER_700, color=ft.Colors.WHITE,
        width=300, height=45, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        on_click=attach_clicked 
    )

    task_time_in_btn = ft.ElevatedButton(
        content=ft.Text("Task Time In (Arrived)", size=16), 
        icon=ft.Icons.LOCATION_ON, bgcolor=ft.Colors.TEAL_700, color=ft.Colors.WHITE,
        width=300, height=55, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        on_click=task_time_in_clicked
    )
    
    task_time_out_btn = ft.ElevatedButton(
        content=ft.Text("Submit Task & Time Out", size=16), 
        icon=ft.Icons.CHECK_CIRCLE, bgcolor=ft.Colors.BLUE_900, color=ft.Colors.WHITE,
        width=300, height=55, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        on_click=task_time_out_clicked
    )

    # Assemble the screen 
    page.add(
        header, 
        logo_image, 
        driver_info, 
        ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
        attendance_row, 
        ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
        task_dropdown,      
        location_dropdown,  
        task_time_in_btn, # <--- NEW TIME IN BUTTON!
        ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
        delivery_status_dropdown, 
        driver_comments, 
        ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
        upload_btn, 
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        task_time_out_btn # <--- NEW TIME OUT BUTTON!
    )

ft.run(main)