# -*- coding: utf-8 -*-

"""
Module contenant les classes et fonctions pour le calcul de calepinage BTC
"""

import math
import numpy as np


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
            width (float): Épaisseur du mur en cm
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
    
    def get_layout_matrix(self):
        """Génère une matrice représentant le calepinage pour visualisation
        
        Returns:
            numpy.ndarray: Matrice 2D représentant le calepinage
        """
        # Nombre de rangées en hauteur
        num_rows = math.ceil(self.height / self.STANDARD_BLOCK.height)
        
        # Créer une matrice vide
        # Utiliser une résolution de 1 cm pour la visualisation
        matrix = np.zeros((int(self.height), int(self.length)))
        
        # Remplir la matrice avec les blocs
        for row in range(num_rows):
            y_start = int(row * self.STANDARD_BLOCK.height)
            y_end = min(int((row + 1) * self.STANDARD_BLOCK.height), int(self.height))
            
            # Première couche (rangée impaire)
            if row % 2 == 0 and row // 2 < len(self.layer1):
                blocks = self.layer1[row // 2]
                x_pos = 0
                for block in blocks:
                    x_end = min(x_pos + int(block.length), int(self.length))
                    # Assigner une valeur différente selon le type de bloc
                    value = 1 if block.name == "Standard" else (2 if block.name == "3/4" else 3)
                    matrix[y_start:y_end, x_pos:x_end] = value
                    x_pos = x_end
            
            # Deuxième couche (rangée paire)
            elif row % 2 == 1 and row // 2 < len(self.layer2):
                blocks = self.layer2[row // 2]
                x_pos = 0
                for block in blocks:
                    x_end = min(x_pos + int(block.length), int(self.length))
                    # Assigner une valeur différente selon le type de bloc
                    value = 4 if block.name == "Standard" else (5 if block.name == "3/4" else 6)
                    matrix[y_start:y_end, x_pos:x_end] = value
                    x_pos = x_end
        
        return matrix
