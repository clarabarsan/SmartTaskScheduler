from datetime import datetime, timedelta

class TaskScheduler:
    # primeste lista de task-uri si programul ca dictionar
    def __init__(self, tasks, availability_schedule):
        self.tasks = tasks
        self.availability_schedule = availability_schedule
        # generated_schedule va fi rezultatul final sub forma de dictionar
        self.generated_schedule = {}

    # Sorteaza task-urile dupa deadline (Earliest Deadline First)
    def sort_tasks_by_deadline(self):
        self.tasks.sort(key=lambda t:t.deadline)

    # Transforma dictionarul de program in lista de tupluri
    def convert_schedule(self):
        available_days = []
        for date_str, hours in self.availability_schedule.daily_hours.items():
            date_obj = datetime.strptime(date_str, "%d-%m-%Y")
            available_days.append((date_obj, hours))
        return available_days

    # Logica de impartire a orelor necesare pe zilele disponibile
    # Se aplica regulile:
    #   - nu se lucreaza mai mult de 2h, dupa acest interval este necesara o pauza de 30'
    #   - nu se poate lucra in doua sesiuni consecutive (sesiune - pauza - sesiune) la acelasi deadline

    def generate_schedule(self, start_date_str):
        # Sortam task-urile dupa deadline (EDF)
        self.sort_tasks_by_deadline()

        # Transformam data in tip data
        start_date = datetime.strptime(start_date_str, "%d-%m-%Y")

        # Pregatim zilele disponibile si le sortam
        available_days = self.convert_schedule()
        available_days.sort(key=lambda x: x[0])

        self.generated_schedule = {}

        # Parcurgem fiecare zi
        for day, available_hours in available_days:
            day_str = day.strftime("%d-%m-%Y")

            # lista cu tuplurile cu detaliile fiecarui task (interval, nume, ore)
            day_tasks = []
            remaining_hours = available_hours

            # pornim ziua la ora 09:00
            current_time = datetime.strptime("09:00", "%H:%M")

            # Parcurgem task-urile
            for task in self.tasks:

                if task.is_completed:
                    continue

                # Daca deadline-ul deja a trecut si inca mai avem task-ul
                # il marcam finalizat ca sa nu apara de mai multe ori
                if day > task.deadline:
                    print(f" [EROARE DEADLINE] Timpul a expirat pentru: {str(task)}")
                    task.mark_completed()
                    continue

                if remaining_hours <= 0:
                    break

                # max 2h per sesiune
                max_session = 2

                hours_to_work = min(task.hours_needed, remaining_hours, max_session)

                if hours_to_work > 0:
                    # calculam intervalul orar
                    end_time = current_time + timedelta(hours=hours_to_work)
                    interval = f"{current_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')}"

                    # salvam task-ul
                    day_tasks.append((interval, task.name, hours_to_work))

                    # actualizam timp
                    current_time = end_time
                    task.hours_needed -= hours_to_work
                    remaining_hours -= hours_to_work

                    # daca sesiunea a fost completa (2h), adaugam pauza
                    if hours_to_work == 2 and remaining_hours >= 0.5:
                        pause_end = current_time + timedelta(minutes=30)
                        pause_interval = f"{current_time.strftime('%H:%M')}-{pause_end.strftime('%H:%M')}"

                        day_tasks.append((pause_interval, "Pauza", 0.5))

                        current_time = pause_end
                        remaining_hours -= 0.5

                    if task.hours_needed == 0:
                        task.mark_completed()

            # Daca NU avem task-uri : zi libera
            if not day_tasks:
                self.generated_schedule[day_str] = [
                    ("--", "Zi libera", available_hours)
                ]
            else:
                self.generated_schedule[day_str] = day_tasks

        # Eroare daca nu putem procesa toate task-urile (nu avem loc in calendar de ele)
        unfinished_tasks = [task for task in self.tasks if not task.is_completed]
        if unfinished_tasks:
            print()
            print(" [EROARE DE PLANIFICARE] Nu mai ai zile disponibile in program pentru a finaliza:")
            for t in unfinished_tasks:
                print(f"   -> {str(t)}")

        return self.generated_schedule