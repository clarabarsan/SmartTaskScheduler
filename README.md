# SmartTaskScheduler
This project is an intelligent time-management and scheduling tool built in Python. Instead of just being a static to-do list, this application acts as a personal productivity assistant. You provide your tasks, their deadlines, and the estimated number of hours required to complete them. The application's algorithm then automatically generates a daily work schedule, fitting your tasks into your available working hours so you never miss a deadline.

### 🚀 Key Features
* **Automated Timeboxing:** Distributes required task hours across your available daily time slots.
* **Smart Prioritization:** Uses an Earliest Deadline First (EDF) approach to prioritize urgent tasks.

### 🐍 Python Concepts & Technologies Used
To build a flexible and efficient engine, this project integrates several key Python programming paradigms:

* **Object-Oriented Programming (OOP):** Tasks and schedules are modeled as classes and objects (e.g., `Task`, `Scheduler`) to keep the code modular, maintainable, and scalable.
* **Functional Programming:** Utilizes concepts like `lambda` functions, `map()`, and `filter()` to efficiently query and manipulate lists of tasks (e.g., instantly filtering out completed tasks or extracting urgent ones).
* **Standard Library Modules:** Heavy reliance on the `datetime` module for complex time and date mathematics, alongside other built-in utilities.
