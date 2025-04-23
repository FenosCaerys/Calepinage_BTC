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

# Essayer d'importer les bibliothèques graphiques, mais continuer même si elles ne sont pas disponibles
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
                                QHeaderView, QMessageBox, QSplitter, QCheckBox)
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
    
    def __init__(self, length, width, height, is_second_wall=False, first_wall=None):
        """Initialise un mur avec ses dimensions
        
        Args:
            length (float): Longueur du mur en cm
            width (float): Epaisseur du mur en cm
            height (float): Hauteur du mur en cm
            is_second_wall (bool): Indique s'il s'agit du deuxième mur (en angle)
            first_wall (BTCWall): Référence au premier mur (pour l'angle)
        """
        self.length = length
        self.width = width
        self.height = height
        self.is_second_wall = is_second_wall
        self.first_wall = first_wall
        
        # Stockage du plan de calepinage
        self.layer1 = []  # Première couche
        self.layer2 = []  # Deuxième couche
        
        # Comptage des blocs
        self.block_count = {
            "Standard": 0,
            "3/4": 0,
            "1/2": 0
        }
        
        # Position pour la visualisation 3D
        self.position_x = 0
        self.position_y = 0
        self.position_z = 0
        self.rotation = 0
        
        # Si c'est le deuxième mur, positionner à l'angle du premier
        if is_second_wall and first_wall:
            # Positionner le deuxième mur pour former un angle droit parfait
            self.position_x = first_wall.length - width/2
            self.position_y = 0
            self.position_z = 0
            self.rotation = 90  # Rotation de 90 degrés pour l'angle droit
        
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
    
    def visualize(self, second_wall=None):
        """Visualise le calepinage avec matplotlib si disponible
        
        Args:
            second_wall (BTCWall, optional): Deuxième mur à afficher en angle droit
        """
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
        
        # Fonction pour ajouter un mur à la visualisation
        def add_wall_to_visualization(wall, ax):
            # Nombre de rangées en hauteur pour ce mur
            num_rows = math.ceil(wall.height / wall.STANDARD_BLOCK.height)
            
            # Position initiale pour ce mur
            y_pos_initial = wall.position_y
            
            # Créer les blocs 3D
            for row in range(num_rows):
                z = row * wall.STANDARD_BLOCK.height + wall.position_z
                
                # Réinitialiser la position y pour chaque nouvelle rangée
                wall.position_y = y_pos_initial
                
                # Première couche (rangées impaires)
                if row % 2 == 0 and row // 2 < len(wall.layer1):
                    blocks = wall.layer1[row // 2]
                    x_pos = wall.position_x
                    for block in blocks:
                        # Calculer les coordonnées en fonction de la rotation
                        if wall.rotation == 0:
                            # Pas de rotation (premier mur)
                            x1, y1 = x_pos, wall.position_y
                            x2, y2 = x_pos + block.length, wall.position_y
                            x3, y3 = x_pos + block.length, wall.position_y + block.width
                            x4, y4 = x_pos, wall.position_y + block.width
                            
                            # Mettre à jour la position pour le prochain bloc
                            x_pos += block.length
                        elif wall.rotation == 90:
                            # Rotation de 90 degrés (deuxième mur)
                            x1, y1 = x_pos, wall.position_y
                            x2, y2 = x_pos, wall.position_y + block.length
                            x3, y3 = x_pos - block.width, wall.position_y + block.length
                            x4, y4 = x_pos - block.width, wall.position_y
                            
                            # Mettre à jour la position pour le prochain bloc
                            wall.position_y += block.length
                        
                        # Créer les sommets du bloc
                        vertices = [
                            # Face inférieure
                            [x1, y1, z],
                            [x2, y2, z],
                            [x3, y3, z],
                            [x4, y4, z],
                            # Face supérieure
                            [x1, y1, z + block.height],
                            [x2, y2, z + block.height],
                            [x3, y3, z + block.height],
                            [x4, y4, z + block.height]
                        ]
                        
                        # Définir les faces du bloc
                        faces = [
                            [vertices[0], vertices[1], vertices[2], vertices[3]],  # Face inférieure
                            [vertices[4], vertices[5], vertices[6], vertices[7]],  # Face supérieure
                            [vertices[0], vertices[1], vertices[5], vertices[4]],  # Face avant
                            [vertices[2], vertices[3], vertices[7], vertices[6]],  # Face arrière
                            [vertices[0], vertices[3], vertices[7], vertices[4]],  # Face gauche
                            [vertices[1], vertices[2], vertices[6], vertices[5]]   # Face droite
                        ]
                        
                        # Créer la collection 3D
                        color_key = block.name
                        poly = Poly3DCollection(faces, alpha=0.9)
                        poly.set_facecolor(colors[color_key])
                        poly.set_edgecolor('black')
                        ax.add_collection3d(poly)
                
                # Deuxième couche (rangées paires)
                elif row % 2 == 1 and row // 2 < len(wall.layer2):
                    blocks = wall.layer2[row // 2]
                    x_pos = wall.position_x
                    for block in blocks:
                        # Calculer les coordonnées en fonction de la rotation
                        if wall.rotation == 0:
                            # Pas de rotation (premier mur)
                            x1, y1 = x_pos, wall.position_y
                            x2, y2 = x_pos + block.length, wall.position_y
                            x3, y3 = x_pos + block.length, wall.position_y + block.width
                            x4, y4 = x_pos, wall.position_y + block.width
                            
                            # Mettre à jour la position pour le prochain bloc
                            x_pos += block.length
                        elif wall.rotation == 90:
                            # Rotation de 90 degrés (deuxième mur)
                            x1, y1 = x_pos, wall.position_y
                            x2, y2 = x_pos, wall.position_y + block.length
                            x3, y3 = x_pos - block.width, wall.position_y + block.length
                            x4, y4 = x_pos - block.width, wall.position_y
                            
                            # Mettre à jour la position pour le prochain bloc
                            wall.position_y += block.length
                        
                        # Créer les sommets du bloc
                        vertices = [
                            # Face inférieure
                            [x1, y1, z],
                            [x2, y2, z],
                            [x3, y3, z],
                            [x4, y4, z],
                            # Face supérieure
                            [x1, y1, z + block.height],
                            [x2, y2, z + block.height],
                            [x3, y3, z + block.height],
                            [x4, y4, z + block.height]
                        ]
                        
                        # Définir les faces du bloc
                        faces = [
                            [vertices[0], vertices[1], vertices[2], vertices[3]],  # Face inférieure
                            [vertices[4], vertices[5], vertices[6], vertices[7]],  # Face supérieure
                            [vertices[0], vertices[1], vertices[5], vertices[4]],  # Face avant
                            [vertices[2], vertices[3], vertices[7], vertices[6]],  # Face arrière
                            [vertices[0], vertices[3], vertices[7], vertices[4]],  # Face gauche
                            [vertices[1], vertices[2], vertices[6], vertices[5]]   # Face droite
                        ]
                        
                        # Créer la collection 3D
                        color_key = block.name + '_2'  # Suffixe pour différencier les couleurs de la couche 2
                        poly = Poly3DCollection(faces, alpha=0.9)
                        poly.set_facecolor(colors[color_key])
                        poly.set_edgecolor('black')
                        ax.add_collection3d(poly)
        
        # Ajouter le premier mur
        add_wall_to_visualization(self, ax)
        
        # Ajouter le deuxième mur si présent
        if second_wall:
            add_wall_to_visualization(second_wall, ax)
        
        # Configurer les axes 3D
        ax.set_title("Visualisation 3D du calepinage")
        ax.set_xlabel("Longueur (cm)")
        ax.set_ylabel("Épaisseur (cm)")
        ax.set_zlabel("Hauteur (cm)")
        
        # Déterminer les limites des axes en fonction des deux murs
        if second_wall:
            max_x = max(self.length, second_wall.position_x)
            max_y = max(self.width, second_wall.position_y + second_wall.length)
            max_z = max(self.height, second_wall.height)
        else:
            max_x = self.length
            max_y = self.width
            max_z = self.height
        
        # Définir les limites des axes pour qu'ils aient la même échelle
        max_dim = max(max_x, max_y, max_z) * 1.2  # Ajouter une marge
        
        # Calculer les centres pour chaque axe
        center_x = max_x / 2
        center_y = max_y / 2
        center_z = max_z / 2
        
        # Définir les limites pour avoir la même échelle sur tous les axes
        ax.set_xlim(center_x - max_dim/2, center_x + max_dim/2)
        ax.set_ylim(center_y - max_dim/2, center_y + max_dim/2)
        ax.set_zlim(0, max_dim)  # Commencer à 0 pour la hauteur
        
        # Configurer la vue pour mieux voir l'angle entre les murs
        if second_wall:
            # Vue plus adaptée pour voir l'angle entre les deux murs
            ax.view_init(elev=30, azim=225)
        else:
            # Vue standard pour un seul mur
            ax.view_init(elev=30, azim=45)
        
        # Afficher une légende
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], color=mcolors.to_rgba('royalblue', alpha=0.8), lw=4, label='Standard - Couche 1'),
            Line2D([0], [0], color=mcolors.to_rgba('cornflowerblue', alpha=0.8), lw=4, label='3/4 - Couche 1'),
            Line2D([0], [0], color=mcolors.to_rgba('lightblue', alpha=0.8), lw=4, label='1/2 - Couche 1'),
            Line2D([0], [0], color=mcolors.to_rgba('darkorange', alpha=0.8), lw=4, label='Standard - Couche 2'),
            Line2D([0], [0], color=mcolors.to_rgba('orange', alpha=0.8), lw=4, label='3/4 - Couche 2'),
            Line2D([0], [0], color=mcolors.to_rgba('moccasin', alpha=0.8), lw=4, label='1/2 - Couche 2')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        # Ajouter des labels pour identifier les murs
        if second_wall:
            ax.text(self.length/2, self.width/2, self.height + 5, "Mur 1", color='black', 
                   fontweight='bold', ha='center', va='center', size=12)
            ax.text(second_wall.position_x, second_wall.position_y + second_wall.length/2, 
                   second_wall.height + 5, "Mur 2", color='black', 
                   fontweight='bold', ha='center', va='center', size=12)
        
        # Ajouter la visualisation 2D des deux premières couches
        if second_wall:
            # Créer une figure avec 4 sous-graphiques (2 couches pour chaque mur)
            fig2, axs = plt.subplots(2, 2, figsize=(14, 10))
            fig2.suptitle("Plan 2D des deux premières couches", fontsize=16)
            
            # Fonction pour dessiner une couche en 2D
            def draw_layer_2d(wall, layer_blocks, ax, title):
                ax.set_title(title)
                ax.set_xlabel("Longueur (cm)")
                ax.set_ylabel("Épaisseur (cm)")
                ax.grid(True)
                
                # Dessiner les blocs
                x_pos = 0
                for block in layer_blocks:
                    # Dessiner le bloc comme un rectangle
                    rect = plt.Rectangle((x_pos, 0), block.length, block.width, 
                                        facecolor=colors[block.name], 
                                        edgecolor='black', alpha=0.8)
                    ax.add_patch(rect)
                    
                    # Ajouter une étiquette au centre du bloc
                    if block.length >= 20:  # Seulement pour les blocs standard et 3/4
                        ax.text(x_pos + block.length/2, block.width/2, block.name, 
                               color='black', fontweight='bold', ha='center', va='center')
                    
                    # Mettre à jour la position pour le prochain bloc
                    x_pos += block.length
                
                # Configurer les limites du graphique
                ax.set_xlim(0, wall.length)
                ax.set_ylim(0, wall.width)
                ax.set_aspect('equal')
            
            # Dessiner la première couche du premier mur
            if len(self.layer1) > 0:
                draw_layer_2d(self, self.layer1[0], axs[0, 0], "Mur 1 - Couche 1")
            
            # Dessiner la deuxième couche du premier mur
            if len(self.layer2) > 0:
                draw_layer_2d(self, self.layer2[0], axs[0, 1], "Mur 1 - Couche 2")
            
            # Dessiner la première couche du deuxième mur
            if len(second_wall.layer1) > 0:
                draw_layer_2d(second_wall, second_wall.layer1[0], axs[1, 0], "Mur 2 - Couche 1")
            
            # Dessiner la deuxième couche du deuxième mur
            if len(second_wall.layer2) > 0:
                draw_layer_2d(second_wall, second_wall.layer2[0], axs[1, 1], "Mur 2 - Couche 2")
            
            # Ajuster l'espacement
            plt.tight_layout(rect=[0, 0, 1, 0.95])
        else:
            # Créer une figure avec 2 sous-graphiques (2 couches pour un seul mur)
            fig2, axs = plt.subplots(1, 2, figsize=(14, 6))
            fig2.suptitle("Plan 2D des deux premières couches", fontsize=16)
            
            # Fonction pour dessiner une couche en 2D
            def draw_layer_2d(wall, layer_blocks, ax, title):
                ax.set_title(title)
                ax.set_xlabel("Longueur (cm)")
                ax.set_ylabel("Épaisseur (cm)")
                ax.grid(True)
                
                # Dessiner les blocs
                x_pos = 0
                for block in layer_blocks:
                    # Dessiner le bloc comme un rectangle
                    rect = plt.Rectangle((x_pos, 0), block.length, block.width, 
                                        facecolor=colors[block.name], 
                                        edgecolor='black', alpha=0.8)
                    ax.add_patch(rect)
                    
                    # Ajouter une étiquette au centre du bloc
                    if block.length >= 20:  # Seulement pour les blocs standard et 3/4
                        ax.text(x_pos + block.length/2, block.width/2, block.name, 
                               color='black', fontweight='bold', ha='center', va='center')
                    
                    # Mettre à jour la position pour le prochain bloc
                    x_pos += block.length
                
                # Configurer les limites du graphique
                ax.set_xlim(0, wall.length)
                ax.set_ylim(0, wall.width)
                ax.set_aspect('equal')
            
            # Dessiner la première couche du mur
            if len(self.layer1) > 0:
                draw_layer_2d(self, self.layer1[0], axs[0], "Couche 1")
            
            # Dessiner la deuxième couche du mur
            if len(self.layer2) > 0:
                draw_layer_2d(self, self.layer2[0], axs[1], "Couche 2")
            
            # Ajuster l'espacement
            plt.tight_layout(rect=[0, 0, 1, 0.95])
        
        # Afficher la figure 3D
        plt.tight_layout()
        plt.show()


class ConsoleApp:
    """Application console pour le calepinage BTC"""
    
    def __init__(self):
        """Initialise l'application console"""
        self.wall = None
        self.second_wall = None
    
    def run(self):
        """Exécute l'application console"""
        print("\n=== Application de Calepinage BTC ===\n")
        print("Cette application permet de calculer le calepinage pour un mur en Blocs de Terre Comprimée.")
        
        while True:
            try:
                print("\n1. Créer un mur simple")
                print("2. Créer un mur en angle droit (deux murs)")
                print("3. Quitter")
                choice = input("\nChoisissez une option (1-3): ")
                
                if choice == "3":
                    break
                
                if choice == "1":
                    # Créer un mur simple
                    length = float(input("\nEntrez la longueur du mur (cm): "))
                    width = float(input("Entrez l'épaisseur du mur (cm): "))
                    height = float(input("Entrez la hauteur du mur (cm): "))
                    
                    if length <= 0 or width <= 0 or height <= 0:
                        print("Erreur: Les dimensions doivent être positives.")
                        continue
                    
                    self.wall = BTCWall(length, width, height)
                    self.second_wall = None  # Réinitialiser le deuxième mur
                    self.wall.print_layout()
                    
                    if HAS_MATPLOTLIB:
                        visualize = input("\nVoulez-vous visualiser le calepinage graphiquement? (o/n): ")
                        if visualize.lower() == 'o':
                            self.wall.visualize()
                
                elif choice == "2":
                    # Créer un mur en angle droit (deux murs)
                    print("\n--- Premier mur ---")
                    length1 = float(input("Entrez la longueur du premier mur (cm): "))
                    width = float(input("Entrez l'épaisseur des murs (cm): "))
                    height = float(input("Entrez la hauteur des murs (cm): "))
                    
                    if length1 <= 0 or width <= 0 or height <= 0:
                        print("Erreur: Les dimensions doivent être positives.")
                        continue
                    
                    print("\n--- Deuxième mur (en angle droit) ---")
                    length2 = float(input("Entrez la longueur du deuxième mur (cm): "))
                    
                    if length2 <= 0:
                        print("Erreur: La longueur doit être positive.")
                        continue
                    
                    # Créer les deux murs
                    self.wall = BTCWall(length1, width, height)
                    self.second_wall = BTCWall(length2, width, height, is_second_wall=True, first_wall=self.wall)
                    
                    # Afficher les résultats
                    print("\n=== Résultats pour le premier mur ===")
                    self.wall.print_layout()
                    
                    print("\n=== Résultats pour le deuxième mur ===")
                    self.second_wall.print_layout()
                    
                    # Calcul du total des blocs pour les deux murs
                    total_standard = self.wall.block_count["Standard"] + self.second_wall.block_count["Standard"]
                    total_three_quarter = self.wall.block_count["3/4"] + self.second_wall.block_count["3/4"]
                    total_half = self.wall.block_count["1/2"] + self.second_wall.block_count["1/2"]
                    total_blocks = total_standard + total_three_quarter + total_half
                    
                    print("\n=== Total des blocs pour les deux murs ===")
                    print(f"  - Blocs standard (29,5 x 14 x 9,5 cm): {total_standard}")
                    print(f"  - Blocs 3/4 (21,75 x 14 x 9,5 cm): {total_three_quarter}")
                    print(f"  - Blocs 1/2 (14 x 14 x 9,5 cm): {total_half}")
                    print(f"  - Total: {total_blocks} blocs")
                    
                    if HAS_MATPLOTLIB:
                        visualize = input("\nVoulez-vous visualiser le calepinage graphiquement? (o/n): ")
                        if visualize.lower() == 'o':
                            self.wall.visualize(self.second_wall)
                
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
            
            # Initialiser les murs
            self.wall = None
            self.second_wall = None
            
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
            
            # Option pour ajouter un deuxième mur en angle droit
            self.second_wall_checkbox = QCheckBox("Ajouter un deuxième mur en angle droit")
            self.second_wall_checkbox.stateChanged.connect(self.toggle_second_wall_input)
            dimensions_layout.addWidget(self.second_wall_checkbox, 3, 0, 1, 2)
            
            # Champ pour la longueur du deuxième mur (initialement caché)
            self.second_wall_length_label = QLabel("Longueur du deuxième mur (cm):")
            self.second_wall_length_input = QLineEdit()
            self.second_wall_length_input.setValidator(QDoubleValidator(0, 10000, 2))
            dimensions_layout.addWidget(self.second_wall_length_label, 4, 0)
            dimensions_layout.addWidget(self.second_wall_length_input, 4, 1)
            
            # Cacher initialement les champs du deuxième mur
            self.second_wall_length_label.setVisible(False)
            self.second_wall_length_input.setVisible(False)
            
            # Bouton de calcul
            self.calculate_button = QPushButton("Calculer le calepinage")
            self.calculate_button.clicked.connect(self.calculate_calepinage)
            dimensions_layout.addWidget(self.calculate_button, 5, 0, 1, 2)
            
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
            
            # Tableau pour les résultats du deuxième mur
            self.second_wall_results_label = QLabel("Résultats pour le deuxième mur")
            self.second_wall_results_label.setVisible(False)
            results_layout.addWidget(self.second_wall_results_label)
            
            self.second_wall_results_table = QTableWidget(3, 2)
            self.second_wall_results_table.setHorizontalHeaderLabels(["Type de bloc", "Quantité"])
            self.second_wall_results_table.setVerticalHeaderLabels(["", "", ""])
            self.second_wall_results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.second_wall_results_table.setVisible(False)
            
            # Remplir le tableau avec les types de blocs
            self.second_wall_results_table.setItem(0, 0, QTableWidgetItem("Standard (29,5 x 14 x 9,5 cm)"))
            self.second_wall_results_table.setItem(1, 0, QTableWidgetItem("3/4 (21,75 x 14 x 9,5 cm)"))
            self.second_wall_results_table.setItem(2, 0, QTableWidgetItem("1/2 (14 x 14 x 9,5 cm)"))
            
            results_layout.addWidget(self.second_wall_results_table)
            
            # Tableau pour les résultats totaux
            self.total_results_label = QLabel("Total des blocs pour les deux murs")
            self.total_results_label.setVisible(False)
            results_layout.addWidget(self.total_results_label)
            
            self.total_results_table = QTableWidget(3, 2)
            self.total_results_table.setHorizontalHeaderLabels(["Type de bloc", "Quantité"])
            self.total_results_table.setVerticalHeaderLabels(["", "", ""])
            self.total_results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.total_results_table.setVisible(False)
            
            # Remplir le tableau avec les types de blocs
            self.total_results_table.setItem(0, 0, QTableWidgetItem("Standard (29,5 x 14 x 9,5 cm)"))
            self.total_results_table.setItem(1, 0, QTableWidgetItem("3/4 (21,75 x 14 x 9,5 cm)"))
            self.total_results_table.setItem(2, 0, QTableWidgetItem("1/2 (14 x 14 x 9,5 cm)"))
            
            results_layout.addWidget(self.total_results_table)
            
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
        
        def toggle_second_wall_input(self, state):
            """Affiche ou cache les champs pour le deuxième mur en fonction de l'état de la case à cocher"""
            is_visible = state == Qt.Checked
            self.second_wall_length_label.setVisible(is_visible)
            self.second_wall_length_input.setVisible(is_visible)
        
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
                
                # Créer le premier mur et calculer le calepinage
                self.wall = BTCWall(length, width, height)
                
                # Vérifier si un deuxième mur est demandé
                has_second_wall = self.second_wall_checkbox.isChecked()
                self.second_wall = None
                
                if has_second_wall:
                    # Récupérer la longueur du deuxième mur
                    length2 = float(self.second_wall_length_input.text() or 0)
                    
                    if length2 <= 0:
                        QMessageBox.warning(self, "Dimensions invalides", 
                                          "Veuillez entrer une longueur positive pour le deuxième mur.")
                        return
                    
                    # Créer le deuxième mur
                    self.second_wall = BTCWall(length2, width, height, is_second_wall=True, first_wall=self.wall)
                
                # Mettre à jour le tableau des résultats pour le premier mur
                block_count = self.wall.get_block_count()
                self.results_table.setItem(0, 1, QTableWidgetItem(str(block_count["Standard"])))
                self.results_table.setItem(1, 1, QTableWidgetItem(str(block_count["3/4"])))
                self.results_table.setItem(2, 1, QTableWidgetItem(str(block_count["1/2"])))
                
                # Mettre à jour le résumé
                total_blocks = self.wall.get_total_blocks()
                self.summary_label.setText(
                    f"Total: {total_blocks} blocs pour un mur de {length}x{width}x{height} cm")
                
                # Afficher/cacher les résultats du deuxième mur
                self.second_wall_results_label.setVisible(has_second_wall)
                self.second_wall_results_table.setVisible(has_second_wall)
                self.total_results_label.setVisible(has_second_wall)
                self.total_results_table.setVisible(has_second_wall)
                
                if has_second_wall and self.second_wall:
                    # Mettre à jour le tableau des résultats pour le deuxième mur
                    block_count2 = self.second_wall.get_block_count()
                    self.second_wall_results_table.setItem(0, 1, QTableWidgetItem(str(block_count2["Standard"])))
                    self.second_wall_results_table.setItem(1, 1, QTableWidgetItem(str(block_count2["3/4"])))
                    self.second_wall_results_table.setItem(2, 1, QTableWidgetItem(str(block_count2["1/2"])))
                    
                    # Calculer et afficher les totaux
                    total_standard = block_count["Standard"] + block_count2["Standard"]
                    total_three_quarter = block_count["3/4"] + block_count2["3/4"]
                    total_half = block_count["1/2"] + block_count2["1/2"]
                    total_blocks_all = total_standard + total_three_quarter + total_half
                    
                    self.total_results_table.setItem(0, 1, QTableWidgetItem(str(total_standard)))
                    self.total_results_table.setItem(1, 1, QTableWidgetItem(str(total_three_quarter)))
                    self.total_results_table.setItem(2, 1, QTableWidgetItem(str(total_half)))
                    
                    # Mettre à jour le résumé
                    self.summary_label.setText(
                        f"Total: {total_blocks_all} blocs pour les deux murs")
                
                # Activer le bouton de visualisation si matplotlib est disponible
                if HAS_MATPLOTLIB:
                    self.visualize_button.setEnabled(True)
                
            except ValueError as e:
                QMessageBox.warning(self, "Erreur de saisie", 
                                  f"Veuillez vérifier les valeurs entrées: {str(e)}")
        
        def visualize_calepinage(self):
            """Visualise le calepinage avec matplotlib"""
            if hasattr(self, 'wall') and self.wall is not None and HAS_MATPLOTLIB:
                if hasattr(self, 'second_wall') and self.second_wall is not None:
                    self.wall.visualize(self.second_wall)
                else:
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
