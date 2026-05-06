from file_handler import DataReader, DataWriter
from scheduler import TaskScheduler

def main():
    # Citim datele de intrare din fisiere
    tasks = DataReader.load_tasks('io_files/input_tasks.txt')
    
    # Citim programul de disponibilitate (orele libere pe zile)
    availability = DataReader.load_schedule('io_files/input_schedule.txt')

    # Prelucram programul: dupa ce data sistemului e dupa data din program, trebuie sa o stearga
    availability.clean_past_dates()
    start_date = availability.get_first_available_date()

    if not start_date:
        print("Orarul este expirat! Actualizeaza datele disponibile")
        return
    
    # Cream obiectul scheduler, acesta contine logica de planificare a task-urilor
    scheduler = TaskScheduler(tasks, availability)
    
    # Generam programul automat
    # Pornim de la o data de start (ex: prima zi din fisierul de intrare care este valida)
    result = scheduler.generate_schedule(start_date)
    
    # Parcurgem fiecare zi din programul generat
    for day, tasks in result.items():
        print(f"\nData: {day}")

        for interval, name, hours in tasks:
            if name == "Pauză":
                print(f"   [PAUZA] {interval} -> {hours}h")
            elif name == "Timp liber":
                print(f"   [TIMP LIBER] {interval} -> {hours}h")
            elif name == "Zi liberă":
                print(f"   Zi complet libera ({hours}h disponibile)")
            else:
                print(f"   {interval} -> {name} ({hours}h)")
    DataWriter.export_schedule(result, 'output_schedule.txt')

if __name__ == "__main__":
    main()