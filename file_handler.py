from models import Task, AvailabilitySchedule

class DataReader:
    def load_tasks(filepath):
        # Citeste task-urile dintr-un fisier de intrare
        tasks = []

        f = open(filepath, 'r')
        number_of_tasks = int((f.readline()).strip())

        for i in range(number_of_tasks):
            # Pentru fiecare task/linie elimin spatiile si virgulele si separ informatiile
            line = f.readline().strip()
            info = line.split(',')

            # Creez un task pe baza campurilor din info (nume, ore, deadline)
            new_task = Task(info[0].strip(), int(info[1].strip()), info[2].strip())
            tasks.append(new_task)

        f.close()

        return tasks

    def load_schedule(filepath):
        # Citeste orarul dintr-un fisier de intrare
        schedule = AvailabilitySchedule()

        f = open(filepath, 'r')
        number_of_days = int((f.readline()).strip())

        for i in range(number_of_days):
            # Pentru fiecare zi elimin spatiile si virgulele si separ informatiile
            line = f.readline().strip()
            info = line.split(',')

            # Adaug orarului pe baza campurilor din info (data, ore), ziua si orele asociate
            schedule.add_daily_availability(info[0].strip(), int(info[1].strip()))

        f.close()

        return schedule

class DataWriter:

    def export_schedule(schedule_data, filepath):
        with open(filepath, 'w') as f:

            for day, tasks in schedule_data.items():
                f.write(f"{day}\n")

                for interval, name, hours in tasks:

                    if name == "Pauza":
                        f.write(f"   [PAUZA] {interval} -> {hours}h\n")

                    elif name == "Timp liber":
                        f.write(f"   [TIMP LIBER] {interval} -> {hours}h\n")

                    elif name == "Zi liberă":
                        f.write(f"   Zi complet libera ({hours}h disponibile)\n")
                    else:
                        f.write(f"   {interval} -> {name} ({hours}h)\n")

                f.write("\n")