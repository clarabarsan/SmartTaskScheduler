from datetime import datetime

class Task:
    # id-ul task-ului
    id_counter = 1

    # deadline string de tipul "DD-MM-YYYY"
    # hours_needed nr intreg
    # name string
    def __init__(self, name, hours_needed, deadline):
        self.task_id = Task.id_counter
        Task.id_counter += 1

        self.name = name
        self.hours_needed = hours_needed
        self.deadline = datetime.strptime(deadline, "%d-%m-%Y")
        self.is_completed = False

    # Marcheaza task-ul ca fiind finalizat
    def mark_completed(self):
        self.is_completed = True

    # Afisare task
    def __str__(self):
        return f"Sarcina '{self.name}' cu deadline {self.deadline.strftime('%d-%m-%Y')} ({self.hours_needed}h)"

class AvailabilitySchedule:
    # Dictionar de stocare al orelor disponibile in fiecare zi ('data': numar de ore)
    def __init__(self):
        self.daily_hours = {}

    # Adaugare ore disponibile intr-o anumita zi
    def add_daily_availability(self, date_str, hours):
        self.daily_hours[date_str] = hours

    # Returneaza un orar nou cu eliminarea zilelor care sunt anterioare datei curente a sistemului
    def clean_past_dates(self):
        # Preluam data de azi
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Cream un dictionar temporar in care punem doar zilele valabile
        valid_schedule = {}
        
        for date_str, hours in self.daily_hours.items():
            # Comparam datele in format daytime pentru comparare
            date_obj = datetime.strptime(date_str, "%d-%m-%Y")
            if date_obj >= today:
                valid_schedule[date_str] = hours
                
        self.daily_hours = valid_schedule

    # Returneaza cea mai apropiata data disponibila din programul ramas
    def get_first_available_date(self):
        # Daca dictionarul este gol, returnam None
        if not self.daily_hours:
            return None
            
        # Convertim cheile in obiecte datetime si gasim data minima
        dates = [datetime.strptime(date_str, "%d-%m-%Y") for date_str in self.daily_hours.keys()]
        first_date = min(dates)

        return first_date.strftime("%d-%m-%Y")
