# -*- coding: utf-8 -*-

"""
Module contenant l'interface graphique pour l'application de calepinage BTC
"""

import sys
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QGroupBox, QGridLayout, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox, QSplitter)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator

from btc_model import BTCWall


class MplCanvas(FigureCanvas):
    """Canvas Matplotlib pour afficher le calepinage"""
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)


class BTCCalepineur(QMainWindow):
    """Fenêtre principale de l'application de calepinage BTC"""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Calepineur BTC")
        self.setMinimumSize(800, 600)
        
        # Initialiser l'interface
        self._init_ui()
    
    def _init_ui(self):
        """Initialise l'interface utilisateur"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Groupe pour les dimensions du mur
        dimensions_group = QGroupBox("Dimensions du mur")
        dimensions_layout = QGridLayout(dimensions_group)
        
        # Champs de saisie pour les dimensions
        self.length_input = QLineEdit()
        self.length_input.setValidator(QDoubleValidator(0, 10000, 2))
        self.width_input = QLineEdit()
        self.width_input.setValidator(QDoubleValidator(0, 1000, 2))
        self.height_input = QLineEdit()
        self.height_input.setValidator(QDoubleValidator(0, 10000, 2))
        
        # Ajouter les champs au layout
        dimensions_layout.addWidget(QLabel("Longueur (cm):"), 0, 0)
        dimensions_layout.addWidget(self.length_input, 0, 1)
        dimensions_layout.addWidget(QLabel("Épaisseur (cm):"), 1, 0)
        dimensions_layout.addWidget(self.width_input, 1, 1)
        dimensions_layout.addWidget(QLabel("Hauteur (cm):"), 2, 0)
        dimensions_layout.addWidget(self.height_input, 2, 1)
        
        # Bouton de calcul
        self.calculate_button = QPushButton("Calculer le calepinage")
        self.calculate_button.clicked.connect(self.calculate_calepinage)
        dimensions_layout.addWidget(self.calculate_button, 3, 0, 1, 2)
        
        # Ajouter le groupe de dimensions au layout principal
        main_layout.addWidget(dimensions_group)
        
        # Splitter pour séparer la visualisation et les résultats
        splitter = QSplitter(Qt.Horizontal)
        
        # Zone de visualisation
        viz_widget = QWidget()
        viz_layout = QVBoxLayout(viz_widget)
        viz_layout.addWidget(QLabel("Visualisation du calepinage"))
        
        # Canvas pour la visualisation
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        viz_layout.addWidget(self.canvas)
        
        # Légende
        legend_group = QGroupBox("Légende")
        legend_layout = QGridLayout(legend_group)
        legend_layout.addWidget(QLabel("Couche 1 - Bloc standard"), 0, 0)
        legend_layout.addWidget(QLabel("Couche 1 - Bloc 3/4"), 1, 0)
        legend_layout.addWidget(QLabel("Couche 1 - Bloc 1/2"), 2, 0)
        legend_layout.addWidget(QLabel("Couche 2 - Bloc standard"), 0, 1)
        legend_layout.addWidget(QLabel("Couche 2 - Bloc 3/4"), 1, 1)
        legend_layout.addWidget(QLabel("Couche 2 - Bloc 1/2"), 2, 1)
        viz_layout.addWidget(legend_group)
        
        # Zone de résultats
        results_widget = QWidget()
        results_layout = QVBoxLayout(results_widget)
        results_layout.addWidget(QLabel("Résultats du calepinage"))
        
        # Tableau pour les résultats
        self.results_table = QTableWidget(3, 2)
        self.results_table.setHorizontalHeaderLabels(["Type de bloc", "Quantité"])
        self.results_table.setVerticalHeaderLabels(["", "", ""])
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Remplir le tableau avec les types de blocs
        self.results_table.setItem(0, 0, QTableWidgetItem("Standard (29,5 x 14 x 9,5 cm)"))
        self.results_table.setItem(1, 0, QTableWidgetItem("3/4 (21,75 x 14 x 9,5 cm)"))
        self.results_table.setItem(2, 0, QTableWidgetItem("1/2 (14 x 14 x 9,5 cm)"))
        
        # Ajouter le tableau au layout des résultats
        results_layout.addWidget(self.results_table)
        
        # Ajouter un résumé
        self.summary_label = QLabel("Entrez les dimensions du mur et cliquez sur 'Calculer le calepinage'")
        results_layout.addWidget(self.summary_label)
        
        # Ajouter les widgets au splitter
        splitter.addWidget(viz_widget)
        splitter.addWidget(results_widget)
        
        # Ajouter le splitter au layout principal
        main_layout.addWidget(splitter)
    
    def calculate_calepinage(self):
        """Calcule le calepinage et met à jour l'interface"""
        try:
            # Récupérer les dimensions
            length = float(self.length_input.text() or 0)
            width = float(self.width_input.text() or 0)
            height = float(self.height_input.text() or 0)
            
            # Vérifier les dimensions
            if length <= 0 or width <= 0 or height <= 0:
                QMessageBox.warning(self, "Dimensions invalides", 
                                   "Veuillez entrer des dimensions positives pour le mur.")
                return
            
            # Créer le mur et calculer le calepinage
            wall = BTCWall(length, width, height)
            
            # Mettre à jour le tableau des résultats
            block_count = wall.get_block_count()
            self.results_table.setItem(0, 1, QTableWidgetItem(str(block_count["Standard"])))
            self.results_table.setItem(1, 1, QTableWidgetItem(str(block_count["3/4"])))
            self.results_table.setItem(2, 1, QTableWidgetItem(str(block_count["1/2"])))
            
            # Mettre à jour le résumé
            total_blocks = wall.get_total_blocks()
            self.summary_label.setText(
                f"Total: {total_blocks} blocs pour un mur de {length}x{width}x{height} cm")
            
            # Mettre à jour la visualisation
            self._update_visualization(wall)
            
        except ValueError as e:
            QMessageBox.warning(self, "Erreur de saisie", 
                               f"Veuillez vérifier les valeurs entrées: {str(e)}")
    
    def _update_visualization(self, wall):
        """Met à jour la visualisation du calepinage
        
        Args:
            wall (BTCWall): Objet mur avec le calepinage calculé
        """
        # Effacer le graphique précédent
        self.canvas.axes.clear()
        
        # Obtenir la matrice de calepinage
        matrix = wall.get_layout_matrix()
        
        # Définir les couleurs pour chaque type de bloc
        cmap = matplotlib.colors.ListedColormap(['white', 'lightblue', 'skyblue', 'dodgerblue', 
                                                'salmon', 'lightsalmon', 'coral'])
        bounds = [0, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5]
        norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)
        
        # Afficher la matrice
        img = self.canvas.axes.imshow(matrix, cmap=cmap, norm=norm, aspect='auto')
        
        # Ajouter des lignes de séparation pour les rangées
        num_rows = int(wall.height / wall.STANDARD_BLOCK.height)
        for i in range(1, num_rows):
            y = i * wall.STANDARD_BLOCK.height
            self.canvas.axes.axhline(y=y, color='black', linestyle='-', linewidth=0.5)
        
        # Configurer les axes
        self.canvas.axes.set_title("Plan de calepinage")
        self.canvas.axes.set_xlabel("Longueur (cm)")
        self.canvas.axes.set_ylabel("Hauteur (cm)")
        
        # Rafraîchir le canvas
        self.canvas.draw()
