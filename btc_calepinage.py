#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Application de calepinage pour les Blocs de Terre Comprimée (BTC)

Cette application permet de calculer et visualiser le calepinage
d'un mur construit en BTC en fonction de ses dimensions.
"""

import math
import os
import sys

# Essayer d'importer les bibliothèques graphiques, mais continuer mêame si elles ne sont pas disponibles
try:
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    import matplotlib.colors as mcolors
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

try:
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                                QHBoxLayout, QLabel, QLineEdit, QPushButton,
                                QGroupBox, QGridLayout, QTableWidget, QTableWidgetItem,
                                QHeaderView, QMessageBox, QSplitter)
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QDoubleValidator
    HAS_PYQT = True
except ImportError:
    HAS_PYQT = False


class BTC:
    """Classe représentant un Bloc de Terre Comprimée"""
    
    def __init__(self, name, length, width, height):
        """Initialise un bloc avec ses dimensions
        
        Args:
            name (str): Nom du type de bloc
            length (float): Longueur en cm
            width (float): Largeur en cm
            height (float): Hauteur en cm
        """
        self.name = name
        self.length = length
        self.width = width
        self.height = height
    
    def __str__(self):
        return f"{self.name} ({self.length}x{self.width}x{self.height} cm)"


class BTCWall:
    """Classe représentant un mur en BTC avec son calepinage"""
    
    # Définition des types de blocs disponibles
    STANDARD_BLOCK = BTC("Standard", 29.5, 14, 9.5)
    THREE_QUARTER_BLOCK = BTC("3/4", 21.75, 14, 9.5)
    HALF_BLOCK = BTC("1/2", 14, 14, 9.5)
    
    def __init__(self, length, width, height):
        """Initialise un mur avec ses dimensions
        
        Args:
            length (float): Longueur du mur en cm
            width (float): Epaisseur du mur en cm
            height (float): Hauteur du mur en cm
        """
        self.length = length
        self.width = width
        self.height = height
        
        # Stockage du plan de calepinage
        self.layer1 = []  # Première couche
        self.layer2 = []  # Deuxième couche
        
        # Comptage des blocs
        self.block_count = {
            "Standard": 0,
            "3/4": 0,
            "1/2": 0
        }
        
        # Calcul du calepinage
        self._calculate_layout()
    
    def _calculate_layout(self):
        """Calcule le calepinage optimal pour le mur"""
        # Nombre de rangées en hauteur
        num_rows = math.ceil(self.height / self.STANDARD_BLOCK.height)
        
        # Création des deux couches alternées
        for row in range(num_rows):
            # Première couche (rangée impaire)
            if row % 2 == 0:
                self._create_layer1()
            # Deuxième couche (rangée paire)
            else:
                self._create_layer2()
    
    def _create_layer1(self):
        """Crée le motif de la première couche"""
        remaining_length = self.length
        row = []
        
        # Commencer par un bloc standard
        while remaining_length > 0:
            # Si on peut mettre un bloc standard
            if remaining_length >= self.STANDARD_BLOCK.length:
                row.append(self.STANDARD_BLOCK)
                self.block_count["Standard"] += 1
                remaining_length -= self.STANDARD_BLOCK.length
            # Sinon, si on peut mettre un bloc 3/4
            elif remaining_length >= self.THREE_QUARTER_BLOCK.length:
                row.append(self.THREE_QUARTER_BLOCK)
                self.block_count["3/4"] += 1
                remaining_length -= self.THREE_QUARTER_BLOCK.length
            # Sinon, si on peut mettre un bloc 1/2
            elif remaining_length >= self.HALF_BLOCK.length:
                row.append(self.HALF_BLOCK)
                self.block_count["1/2"] += 1
                remaining_length -= self.HALF_BLOCK.length
            # Sinon, on arrondit à la longueur inférieure
            else:
                break
        
        self.layer1.append(row)
    
    def _create_layer2(self):
        """Crée le motif de la deuxième couche (décalée)"""
        remaining_length = self.length
        row = []
        
        # Commencer par un bloc 1/2 pour décaler
        if remaining_length >= self.HALF_BLOCK.length:
            row.append(self.HALF_BLOCK)
            self.block_count["1/2"] += 1
            remaining_length -= self.HALF_BLOCK.length
        
        # Continuer avec des blocs standards
        while remaining_length > 0:
            # Si on peut mettre un bloc standard
            if remaining_length >= self.STANDARD_BLOCK.length:
                row.append(self.STANDARD_BLOCK)
                self.block_count["Standard"] += 1
                remaining_length -= self.STANDARD_BLOCK.length
            # Sinon, si on peut mettre un bloc 3/4
            elif remaining_length >= self.THREE_QUARTER_BLOCK.length:
                row.append(self.THREE_QUARTER_BLOCK)
                self.block_count["3/4"] += 1
                remaining_length -= self.THREE_QUARTER_BLOCK.length
            # Sinon, si on peut mettre un bloc 1/2
            elif remaining_length >= self.HALF_BLOCK.length:
                row.append(self.HALF_BLOCK)
                self.block_count["1/2"] += 1
                remaining_length -= self.HALF_BLOCK.length
            # Sinon, on arrondit à la longueur inférieure
            else:
                break
        
        self.layer2.append(row)
    
    def get_block_count(self):
        """Retourne le nombre total de chaque type de bloc
        
        Returns:
            dict: Dictionnaire avec le nombre de chaque type de bloc
        """
        return self.block_count
    
    def get_total_blocks(self):
        """Retourne le nombre total de blocs
        
        Returns:
            int: Nombre total de blocs
        """
        return sum(self.block_count.values())
    
    def get_wall_layout(self):
        """Retourne la représentation du calepinage
        
        Returns:
            tuple: (layer1, layer2) contenant les blocs de chaque couche
        """
        return (self.layer1, self.layer2)
    
    def print_layout(self):
        """Affiche le calepinage sous forme de texte ASCII"""
        print(f"\nCalepinage pour un mur de {self.length}x{self.width}x{self.height} cm\n")
        
        # Nombre de rangées en hauteur
        num_rows = math.ceil(self.height / self.STANDARD_BLOCK.height)
        
        # Afficher chaque rangée
        for row in range(num_rows):
            print(f"Rangée {row+1}:")
            
            # Première couche (rangée impaire)
            if row % 2 == 0 and row // 2 < len(self.layer1):
                blocks = self.layer1[row // 2]
                print("  ", end="")
                for block in blocks:
                    if block.name == "Standard":
                        print("[===========]", end="")
                    elif block.name == "3/4":
                        print("[=======]  ", end="")
                    elif block.name == "1/2":
                        print("[====]     ", end="")
                print("\n  ", end="")
                for block in blocks:
                    if block.name == "Standard":
                        print("  Standard  ", end="")
                    elif block.name == "3/4":
                        print("   3/4     ", end="")
                    elif block.name == "1/2":
                        print("   1/2     ", end="")
                print("\n")
            
            # Deuxième couche (rangée paire)
            elif row % 2 == 1 and row // 2 < len(self.layer2):
                blocks = self.layer2[row // 2]
                print("  ", end="")
                for block in blocks:
                    if block.name == "Standard":
                        print("[===========]", end="")
                    elif block.name == "3/4":
                        print("[=======]  ", end="")
                    elif block.name == "1/2":
                        print("[====]     ", end="")
                print("\n  ", end="")
                for block in blocks:
                    if block.name == "Standard":
                        print("  Standard  ", end="")
                    elif block.name == "3/4":
                        print("   3/4     ", end="")
                    elif block.name == "1/2":
                        print("   1/2     ", end="")
                print("\n")
        
        # Afficher le récapitulatif
        print("Récapitulatif des blocs nécessaires:")
        print(f"  - Blocs standard (29,5 x 14 x 9,5 cm): {self.block_count['Standard']}")
        print(f"  - Blocs 3/4 (21,75 x 14 x 9,5 cm): {self.block_count['3/4']}")
        print(f"  - Blocs 1/2 (14 x 14 x 9,5 cm): {self.block_count['1/2']}")
        print(f"  - Total: {self.get_total_blocks()} blocs")
    
    def visualize(self):
        """Visualise le calepinage avec matplotlib si disponible"""
        if not HAS_MATPLOTLIB:
            print("Matplotlib n'est pas disponible. Impossible de visualiser graphiquement.")
            return
        
        # Créer une figure pour la visualisation 3D
        fig = plt.figure(figsize=(12, 10))
        
        # Nombre de rangées en hauteur
        num_rows = math.ceil(self.height / self.STANDARD_BLOCK.height)
        
        # Visualisation 3D du mur
        ax = fig.add_subplot(111, projection='3d')
        
        # Couleurs pour les différents types de blocs
        colors = {
            'Standard': mcolors.to_rgba('royalblue', alpha=0.8),
            '3/4': mcolors.to_rgba('cornflowerblue', alpha=0.8),
            '1/2': mcolors.to_rgba('lightblue', alpha=0.8),
            'Standard_2': mcolors.to_rgba('darkorange', alpha=0.8),
            '3/4_2': mcolors.to_rgba('orange', alpha=0.8),
            '1/2_2': mcolors.to_rgba('moccasin', alpha=0.8)
        }
        
        # Créer les blocs 3D
        for row in range(num_rows):
            y = row * self.STANDARD_BLOCK.height
            
            # Première couche (rangées impaires)
            if row % 2 == 0 and row // 2 < len(self.layer1):
                blocks = self.layer1[row // 2]
                x_pos = 0
                for block in blocks:
                    # Créer les sommets du bloc
                    vertices = [
                        # Face avant (x, y, z)
                        [x_pos, 0, y],
                        [x_pos + block.length, 0, y],
                        [x_pos + block.length, 0, y + block.height],
                        [x_pos, 0, y + block.height],
                        # Face arrière
                        [x_pos, block.width, y],
                        [x_pos + block.length, block.width, y],
                        [x_pos + block.length, block.width, y + block.height],
                        [x_pos, block.width, y + block.height]
                    ]
                    
                    # Définir les faces du bloc
                    faces = [
                        [vertices[0], vertices[1], vertices[2], vertices[3]],  # Face avant
                        [vertices[4], vertices[5], vertices[6], vertices[7]],  # Face arrière
                        [vertices[0], vertices[3], vertices[7], vertices[4]],  # Face gauche
                        [vertices[1], vertices[2], vertices[6], vertices[5]],  # Face droite
                        [vertices[3], vertices[2], vertices[6], vertices[7]],  # Face supérieure
                        [vertices[0], vertices[1], vertices[5], vertices[4]]   # Face inférieure
                    ]
                    
                    # Créer la collection 3D
                    color_key = block.name
                    poly = Poly3DCollection(faces, alpha=0.9)
                    poly.set_facecolor(colors[color_key])
                    poly.set_edgecolor('black')
                    ax.add_collection3d(poly)
                    
                    # Ajouter une étiquette au centre du bloc
                    ax.text(x_pos + block.length/2, block.width/2, y + block.height/2, 
                            block.name, color='black', fontweight='bold', ha='center', va='center')
                    
                    x_pos += block.length
            
            # Deuxième couche (rangées paires)
            elif row % 2 == 1 and row // 2 < len(self.layer2):
                blocks = self.layer2[row // 2]
                x_pos = 0
                for block in blocks:
                    # Créer les sommets du bloc
                    vertices = [
                        # Face avant (x, y, z)
                        [x_pos, 0, y],
                        [x_pos + block.length, 0, y],
                        [x_pos + block.length, 0, y + block.height],
                        [x_pos, 0, y + block.height],
                        # Face arrière
                        [x_pos, block.width, y],
                        [x_pos + block.length, block.width, y],
                        [x_pos + block.length, block.width, y + block.height],
                        [x_pos, block.width, y + block.height]
                    ]
                    
                    # Définir les faces du bloc
                    faces = [
                        [vertices[0], vertices[1], vertices[2], vertices[3]],  # Face avant
                        [vertices[4], vertices[5], vertices[6], vertices[7]],  # Face arrière
                        [vertices[0], vertices[3], vertices[7], vertices[4]],  # Face gauche
                        [vertices[1], vertices[2], vertices[6], vertices[5]],  # Face droite
                        [vertices[3], vertices[2], vertices[6], vertices[7]],  # Face supérieure
                        [vertices[0], vertices[1], vertices[5], vertices[4]]   # Face inférieure
                    ]
                    
                    # Créer la collection 3D
                    color_key = block.name + '_2'  # Suffixe pour différencier les couleurs de la couche 2
                    poly = Poly3DCollection(faces, alpha=0.9)
                    poly.set_facecolor(colors[color_key])
                    poly.set_edgecolor('black')
                    ax.add_collection3d(poly)
                    
                    # Ajouter une étiquette au centre du bloc
                    ax.text(x_pos + block.length/2, block.width/2, y + block.height/2, 
                            block.name, color='black', fontweight='bold', ha='center', va='center')
                    
                    x_pos += block.length
        
        # Configurer les axes 3D
        ax.set_title("Visualisation 3D du mur")
        ax.set_xlabel("Longueur (cm)")
        ax.set_ylabel("Épaisseur (cm)")
        ax.set_zlabel("Hauteur (cm)")
        
        # Définir les limites des axes
        ax.set_xlim(0, self.length)
        ax.set_ylim(0, self.width)
        ax.set_zlim(0, self.height)
        
        # Ajouter une légende
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor=colors['Standard'], edgecolor='black', label='Couche 1 - Standard'),
            Patch(facecolor=colors['3/4'], edgecolor='black', label='Couche 1 - 3/4'),
            Patch(facecolor=colors['1/2'], edgecolor='black', label='Couche 1 - 1/2'),
            Patch(facecolor=colors['Standard_2'], edgecolor='black', label='Couche 2 - Standard'),
            Patch(facecolor=colors['3/4_2'], edgecolor='black', label='Couche 2 - 3/4'),
            Patch(facecolor=colors['1/2_2'], edgecolor='black', label='Couche 2 - 1/2')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        # Définir un angle de vue initial
        ax.view_init(elev=30, azim=45)
        
        # Ajuster l'espacement
        plt.tight_layout()
        
        # Afficher la figure
        plt.show()


class ConsoleApp:
    """Application console pour le calepinage BTC"""
    
    def __init__(self):
        """Initialise l'application console"""
        self.wall = None
    
    def run(self):
        """Exécute l'application console"""
        print("\n=== Application de Calepinage BTC ===\n")
        print("Cette application permet de calculer le calepinage pour un mur en Blocs de Terre Comprimée.")
        
        while True:
            try:
                length = float(input("\nEntrez la longueur du mur (cm): "))
                width = float(input("Entrez l'épaisseur du mur (cm): "))
                height = float(input("Entrez la hauteur du mur (cm): "))
                
                if length <= 0 or width <= 0 or height <= 0:
                    print("Erreur: Les dimensions doivent être positives.")
                    continue
                
                self.wall = BTCWall(length, width, height)
                self.wall.print_layout()
                
                if HAS_MATPLOTLIB:
                    visualize = input("\nVoulez-vous visualiser le calepinage graphiquement? (o/n): ")
                    if visualize.lower() == 'o':
                        self.wall.visualize()
                
                again = input("\nVoulez-vous calculer un autre calepinage? (o/n): ")
                if again.lower() != 'o':
                    break
            
            except ValueError:
                print("Erreur: Veuillez entrer des valeurs numériques valides.")
            except Exception as e:
                print(f"Erreur: {str(e)}")
        
        print("\nMerci d'avoir utilisé l'application de Calepinage BTC!")


if HAS_PYQT:
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
            
            # Bouton de visualisation
            if HAS_MATPLOTLIB:
                self.visualize_button = QPushButton("Visualiser le calepinage")
                self.visualize_button.clicked.connect(self.visualize_calepinage)
                self.visualize_button.setEnabled(False)
                results_layout.addWidget(self.visualize_button)
            
            # Ajouter les widgets au splitter
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
                self.wall = BTCWall(length, width, height)
                
                # Mettre à jour le tableau des résultats
                block_count = self.wall.get_block_count()
                self.results_table.setItem(0, 1, QTableWidgetItem(str(block_count["Standard"])))
                self.results_table.setItem(1, 1, QTableWidgetItem(str(block_count["3/4"])))
                self.results_table.setItem(2, 1, QTableWidgetItem(str(block_count["1/2"])))
                
                # Mettre à jour le résumé
                total_blocks = self.wall.get_total_blocks()
                self.summary_label.setText(
                    f"Total: {total_blocks} blocs pour un mur de {length}x{width}x{height} cm")
                
                # Activer le bouton de visualisation si matplotlib est disponible
                if HAS_MATPLOTLIB:
                    self.visualize_button.setEnabled(True)
                
            except ValueError as e:
                QMessageBox.warning(self, "Erreur de saisie", 
                                  f"Veuillez vérifier les valeurs entrées: {str(e)}")
        
        def visualize_calepinage(self):
            """Visualise le calepinage avec matplotlib"""
            if hasattr(self, 'wall') and self.wall is not None and HAS_MATPLOTLIB:
                self.wall.visualize()


def main():
    """Point d'entrée principal de l'application"""
    if HAS_PYQT:
        app = QApplication(sys.argv)
        window = BTCCalepineur()
        window.show()
        sys.exit(app.exec_())
    else:
        console_app = ConsoleApp()
        console_app.run()


if __name__ == "__main__":
    main()
