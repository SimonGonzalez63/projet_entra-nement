# ui_main.py
from PySide6.QtWidgets import (
    QWidget, QMainWindow, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QTableWidget, QTableWidgetItem
)
from db import get_connection


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QuayTracker - Suivi de quai")
        self.resize(900, 600)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        # -----------------------
        # Barre de filtres
        # -----------------------
        filter_layout = QHBoxLayout()

        self.status_filter = QComboBox()
        self.status_filter.addItem("Tous")
        self.status_filter.addItems(["A_FAIRE", "EN_COURS", "TERMINEE", "BLOQUEE"])
        self.status_filter.currentIndexChanged.connect(self.load_tasks)
        filter_layout.addWidget(self.status_filter)

        self.refresh_button = QPushButton("Rafraîchir")
        self.refresh_button.clicked.connect(self.load_tasks)
        filter_layout.addWidget(self.refresh_button)

        layout.addLayout(filter_layout)

        # -----------------------
        # Tableau des tâches
        # -----------------------
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Titre", "Navire", "Zone", "Statut"])
        layout.addWidget(self.table)

        # -----------------------
        # Boutons d'action
        # -----------------------
        btn_layout = QHBoxLayout()

        self.add_button = QPushButton("Ajouter tâche")
        btn_layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Modifier")
        btn_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Supprimer")
        btn_layout.addWidget(self.delete_button)

        layout.addLayout(btn_layout)

        # Charger les données
        self.load_tasks()

    def load_tasks(self):
        status = self.status_filter.currentText()
        conn = get_connection()
        cur = conn.cursor()

        query = """
        SELECT t.id, t.title, s.name, z.name, t.status
        FROM task t
        JOIN ship s ON t.ship_id = s.id
        JOIN zone z ON t.zone_id = z.id
        """
        params = ()
        if status != "Tous":
            query += " WHERE t.status = ?"
            params = (status,)

        cur.execute(query, params)
        rows = cur.fetchall()
        conn.close()

        self.table.setRowCount(len(rows))

        for row_idx, (task_id, title, ship_name, zone_name, task_status) in enumerate(rows):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(task_id)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(title))
            self.table.setItem(row_idx, 2, QTableWidgetItem(ship_name))
            self.table.setItem(row_idx, 3, QTableWidgetItem(zone_name))
            self.table.setItem(row_idx, 4, QTableWidgetItem(task_status))
